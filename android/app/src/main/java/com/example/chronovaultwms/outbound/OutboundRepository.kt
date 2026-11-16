package com.example.chronovaultwms.outbound

import androidx.room.withTransaction
import com.example.chronovaultwms.core.database.*
import com.google.gson.Gson
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.util.Locale
import java.util.UUID

/** TV3 warehouse workflow. All local state changes and their durable outbox event commit together. */
class OutboundRepository(private val database: ChronoVaultDatabase) {
    private val workflow get() = database.outboundWorkflowDao()
    private val serials get() = database.serialDao()
    private val orders get() = database.outboundOrderDao()
    private val gson = Gson()

    suspend fun loadState(): OutboundState = database.withTransaction {
        DatabaseSeeder.checkAndSeed(database.productDao(), serials, database.userDao(), database.auditLogDao(), database.dealerDao(), orders, database.dealerReceiptDao())
        importLegacyDetails()
        // stockQuantity is a derived cache for TV1. Never invent Serial inventory to match a counter.
        database.productDao().getAllProducts().forEach { refreshProductCount(it.productCode) }
        OutboundState(database.dealerDao().getAllDealers(), database.productDao().getAllProducts(),
            orders.getAllOrders().sortedByDescending { parseTimestamp(it.createdDate) }, serials.getAllSerials())
    }

    suspend fun saveDealer(dealer: DealerEntity, actor: OutboundActor) = database.withTransaction {
        WarehouseOutboundRules.requireOperator(actor)
        require(dealer.dealerId.isNotBlank() && dealer.name.isNotBlank() && dealer.address.isNotBlank()) {
            "Mã, tên đơn vị và địa chỉ nhận hàng là bắt buộc."
        }
        require(dealer.status in setOf("ACTIVE", "LOCKED", "SUSPENDED")) { "Trạng thái đơn vị nhận không hợp lệ." }
        val normalizedId = dealer.dealerId.trim()
        val previous = database.dealerDao().getDealerById(normalizedId)
        if (previous != null && previous.status != dealer.status) WarehouseOutboundRules.requireManager(actor)
        if (previous == null && dealer.status != "ACTIVE") WarehouseOutboundRules.requireManager(actor)
        if (dealer.taxCode.isNotBlank()) {
            require(database.dealerDao().findTaxCodeOwner(dealer.taxCode.trim(), normalizedId) == null) { "Mã số đơn vị/MST đã thuộc đơn vị khác." }
        }
        val contact = dealer.copy(dealerId = normalizedId, name = dealer.name.trim(), address = dealer.address.trim(),
            taxCode = dealer.taxCode.trim(), representative = dealer.representative.trim(), email = dealer.email.trim(), phone = dealer.phone.trim())
        val saved = if (previous == null) contact.copy(discountPercent = 0.0, creditLimit = 0.0, currentDebt = 0.0) else contact.copy(
            creditLimit = previous.creditLimit, currentDebt = previous.currentDebt, discountPercent = previous.discountPercent, tier = previous.tier)
        if (previous == null) database.dealerDao().insert(saved) else database.dealerDao().update(saved)
        record("UNIT_SAVED", saved.dealerId, actor, "Cập nhật hồ sơ đơn vị ${saved.name}.", saved)
    }

    suspend fun createDraft(dealerId: String, requests: List<OutboundLineRequest>, note: String, actor: OutboundActor): String = database.withTransaction {
        WarehouseOutboundRules.requireOperator(actor)
        val dealer = requireNotNull(database.dealerDao().getDealerById(dealerId)) { "Không tìm thấy đơn vị nhận." }
        require(dealer.status == "ACTIVE") { "Đơn vị nhận đang bị khóa hoặc ngừng tiếp nhận." }
        require(requests.isNotEmpty()) { "Lệnh xuất phải có ít nhất một mặt hàng." }
        require(requests.map { it.productCode }.distinct().size == requests.size) { "Một SKU chỉ được xuất hiện một lần; hãy gộp số lượng." }
        val code = newCode("DS")
        val lines = requests.map { input ->
            val product = requireNotNull(database.productDao().getProductByCode(input.productCode)) { "Không tìm thấy SKU ${input.productCode}." }
            require(product.status != "DISCONTINUED") { "SKU ${product.productCode} đã ngừng sử dụng." }
            val converted = WarehouseOutboundRules.convertQuantity(input.quantity, input.isBox, product.conversionRate)
            require(converted >= product.minDispatchQuantity) { "SKU ${product.productCode} yêu cầu tối thiểu ${product.minDispatchQuantity} chiếc." }
            val available = serials.getSerialsByProduct(product.productCode).count { it.status == "IN_STOCK" && it.allocatedOrderCode == null }
            require(converted <= available) { "SKU ${product.productCode} chỉ còn $available Serial khả dụng; yêu cầu $converted." }
            val unitCost = serials.getSerialsByProduct(product.productCode).filter { it.status == "IN_STOCK" }.map { it.unitCost }.average().takeIf { it.isFinite() } ?: 0.0
            OutboundLineEntity(code, product.productCode, product.name, if (input.isBox) "BOX" else "PIECE", input.quantity, converted, unitCost)
        }
        val first = lines.first()
        orders.insert(OutboundOrderEntity(code, dealer.dealerId, dealer.name, first.productCode,
            if (lines.size == 1) first.productName else "${lines.size} mã hàng", first.unit, first.quantity,
            lines.sumOf { it.convertedQuantity }, first.unitCost, 0.0, lines.sumOf { it.unitCost * it.convertedQuantity },
            0.0, 0.0, "DRAFT", now(), note = note.trim(), createdBy = actor.name))
        workflow.insertLines(lines)
        record("OUTBOUND_DRAFT_CREATED", code, actor, "Lập lệnh nháp $code cho ${dealer.name}; ${lines.size} SKU.", mapOf("order" to orders.getOrderByCode(code), "lines" to lines))
        code
    }

    suspend fun approveOrder(code: String, actor: OutboundActor) = database.withTransaction {
        WarehouseOutboundRules.requireManager(actor)
        val order = requireOrder(code)
        if (order.status in setOf("RESERVED", "PACKING")) {
            ensureLegacyReservation(order)
            return@withTransaction
        }
        require(order.status == "DRAFT") { "Chỉ có thể duyệt lệnh nháp." }
        val dealer = requireNotNull(database.dealerDao().getDealerById(order.dealerId)) { "Đơn vị nhận không tồn tại." }
        require(dealer.status == "ACTIVE") { "Đơn vị nhận không còn hoạt động." }
        reserveExactSerials(order)
        val allocated = workflow.allocations(code)
        val approved = order.copy(status = "RESERVED", approvedBy = actor.name, approvedAt = now(),
            totalAmount = allocated.sumOf { it.unitCost }, unitPrice = allocated.filter { it.productCode == order.productCode }.map { it.unitCost }.average(),
            discountPercent = 0.0, depositAmount = 0.0, remainingDebt = 0.0)
        orders.update(approved)
        record("EVENT_STOCK_RESERVED", code, actor, "Duyệt và phân bổ Serial đích danh cho $code.", mapOf("order" to approved, "allocations" to workflow.allocations(code)))
    }

    suspend fun startPacking(code: String, actor: OutboundActor) = database.withTransaction {
        WarehouseOutboundRules.requireOperator(actor)
        val order = requireOrder(code)
        require(order.status in setOf("RESERVED", "PACKING")) { "Chỉ soạn hàng cho lệnh đã được duyệt giữ chỗ." }
        ensureLegacyReservation(order)
        if (order.status == "RESERVED") {
            orders.update(order.copy(status = "PACKING"))
            record("OUTBOUND_PACKING_STARTED", code, actor, "Bắt đầu soạn hàng $code.", mapOf("orderCode" to code))
        }
    }

    suspend fun cancelOrder(code: String, reason: String, actor: OutboundActor) = database.withTransaction {
        WarehouseOutboundRules.requireOperator(actor)
        require(reason.isNotBlank()) { "Vui lòng nhập lý do hủy lệnh." }
        val order = requireOrder(code)
        if (order.status == "CANCELLED") return@withTransaction
        require(order.status in setOf("DRAFT", "RESERVED", "PACKING")) { "Không được hủy lệnh đã xuất kho." }
        if (order.createdBy.isNotBlank() && order.createdBy != actor.name && actor.role == "OPERATIONS_STAFF") {
            error("Chỉ người lập hoặc Thủ kho mới được hủy lệnh này.")
        }
        workflow.allocations(code).forEach { allocation ->
            val serial = serials.getSerialByNumber(allocation.serialNumber)
            if (serial?.allocatedOrderCode == code && serial.status == "ALLOCATED") {
                serials.update(serial.copy(status = "IN_STOCK", allocatedOrderCode = null))
            }
        }
        orders.update(order.copy(status = "CANCELLED", cancelReason = reason.trim()))
        record("OUTBOUND_CANCELLED", code, actor, "Hủy $code, giải phóng giữ chỗ. Lý do: ${reason.trim()}", mapOf("orderCode" to code, "reason" to reason.trim()))
    }

    suspend fun pickingList(code: String): List<OutboundPick> = database.withTransaction {
        val order = requireOrder(code)
        require(order.status in setOf("RESERVED", "PACKING", "COMPLETED")) { "Lệnh chưa được duyệt giữ chỗ." }
        if (order.status != "COMPLETED") ensureLegacyReservation(order)
        workflow.allocations(code).map { it.toPick() }
    }

    suspend fun validateScan(code: String, input: String, alreadyScanned: List<String>): SerialEntity = database.withTransaction {
        val order = requireOrder(code)
        require(order.status in setOf("RESERVED", "PACKING")) { "Lệnh không còn ở trạng thái cho phép đóng kiện." }
        val number = input.trim().uppercase(Locale.ROOT)
        require(number.isNotBlank()) { "Vui lòng quét hoặc nhập mã Serial." }
        require(alreadyScanned.none { it.equals(number, ignoreCase = true) }) { "Serial $number đã được quét rồi." }
        val allocations = workflow.allocations(code)
        require(allocations.isNotEmpty()) { "Picking List chưa sẵn sàng; tải lại lệnh trước khi quét." }
        require(alreadyScanned.size < allocations.size) { "Đã quét đủ số Serial của phiếu." }
        require(allocations.any { it.serialNumber.equals(number, ignoreCase = true) }) { "Serial $number không thuộc Picking List của lệnh này." }
        val serial = requireNotNull(serials.getSerialByNumber(number)) { "Không tìm thấy Serial $number." }
        require(serial.status == "ALLOCATED" && serial.allocatedOrderCode == code) { "Serial $number không còn được giữ chỗ hợp lệ cho lệnh này (${serial.status})." }
        serial
    }

    suspend fun scannedSerials(code: String): List<String> = database.withTransaction {
        workflow.allocations(code).filter { it.scannedAt.isNotBlank() }.map { it.serialNumber }
    }

    suspend fun recordScan(code: String, input: String, actor: OutboundActor): List<String> = database.withTransaction {
        WarehouseOutboundRules.requireOperator(actor)
        val previous = workflow.allocations(code).filter { it.scannedAt.isNotBlank() }.map { it.serialNumber }
        val serial = validateScan(code, input, previous)
        check(workflow.recordScan(code, serial.serialNumber, now(), actor.name) == 1) { "Serial này đã được quét trên phiên khác; hãy tải lại." }
        record("OUTBOUND_SERIAL_SCANNED", code, actor, "Quét đối soát ${serial.serialNumber} cho $code.",
            mapOf("orderCode" to code, "serialNumber" to serial.serialNumber, "scannedBy" to actor.name))
        previous + serial.serialNumber
    }

    suspend fun completeDispatch(code: String, scannedNumbers: List<String>, carrier: String, trackingNumber: String, actor: OutboundActor): OutboundDocument = database.withTransaction {
        WarehouseOutboundRules.requireManager(actor)
        val order = requireOrder(code)
        val allocations = workflow.allocations(code)
        val scanned = scannedNumbers.map { it.trim().uppercase(Locale.ROOT) }
        WarehouseOutboundRules.requireExactScanSet(allocations.map { it.serialNumber }, scanned)
        if (order.status == "COMPLETED") return@withTransaction documentInsideTransaction(code)
        WarehouseOutboundRules.requireExactScanSet(allocations.map { it.serialNumber }, allocations.filter { it.scannedAt.isNotBlank() }.map { it.serialNumber })
        require(order.status in setOf("RESERVED", "PACKING")) { "Chỉ xuất lệnh đã duyệt và đang soạn hàng." }
        val dealer = requireNotNull(database.dealerDao().getDealerById(order.dealerId)) { "Không tìm thấy đơn vị nhận." }
        require(dealer.status == "ACTIVE") { "Đơn vị nhận đã bị khóa; không thể bàn giao." }
        val currentSerials = allocations.map { allocation ->
            val serial = requireNotNull(serials.getSerialByNumber(allocation.serialNumber)) { "Serial ${allocation.serialNumber} không còn tồn tại." }
            require(serial.status == "ALLOCATED" && serial.allocatedOrderCode == code && serial.productCode == allocation.productCode) {
                "Serial ${serial.serialNumber} không còn hợp lệ; dừng toàn bộ phiếu xuất."
            }
            serial
        }
        val time = now()
        val dispatchCode = newCode("PX")
        val dispatch = OutboundDispatchEntity(dispatchCode, code, dealer.dealerId, dealer.name, dealer.address,
            time, actor.name, carrier.trim(), trackingNumber.trim(), order.note)
        workflow.insertDispatch(dispatch)
        currentSerials.forEach { serial ->
            val destination = "Đã xuất bàn giao: ${dealer.name}"
            serials.update(serial.copy(status = "DISPATCHED", allocatedOrderCode = null, dealerId = dealer.dealerId,
                dealerName = dealer.name, currentLocation = destination, lastDispatchCode = dispatchCode, lastDispatchAt = time))
            movement("OUTBOUND", dispatchCode, serial, serial.currentLocation, destination, -1, actor)
        }
        currentSerials.map { it.productCode }.distinct().forEach { refreshProductCount(it) }
        val updatedDebt = dealer.currentDebt + order.remainingDebt.coerceAtLeast(0.0)
        database.dealerDao().update(dealer.copy(currentDebt = updatedDebt))
        orders.update(order.copy(status = "COMPLETED", dispatchedSerials = scanned.joinToString(", "), dispatchedBy = actor.name, dispatchedAt = time))
        record("EVENT_DISPATCH_COMPLETED", code, actor, "Xác nhận phiếu $dispatchCode: xuất ${scanned.size} Serial cho ${dealer.name}.",
            mapOf("dispatch" to dispatch, "lines" to workflow.orderLines(code), "serials" to allocations))
        documentInsideTransaction(code)
    }

    suspend fun receiveReturn(dealerId: String, input: String, condition: String, reason: String, actor: OutboundActor): String = database.withTransaction {
        WarehouseOutboundRules.requireManager(actor)
        require(reason.isNotBlank()) { "Vui lòng nhập lý do hoàn trả/biên bản kiểm định." }
        require(condition in setOf("HANG_MOI", "PERFECT", "DEFECTIVE")) { "Tình trạng kiểm định không hợp lệ." }
        val serial = requireNotNull(serials.getSerialByNumber(input.trim().uppercase(Locale.ROOT))) { "Không tìm thấy Serial hoàn trả." }
        val previousReturn = serial.lastDispatchCode?.let { workflow.returnForDispatchSerial(it, serial.serialNumber) }
        if (serial.status in setOf("IN_STOCK", "DEFECTIVE") && previousReturn?.dealerId == dealerId &&
            previousReturn.inspectedCondition == condition && previousReturn.reason == reason.trim()) {
            return@withTransaction previousReturn.returnCode
        }
        require(serial.status in setOf("DISPATCHED", "DELIVERED", "SOLD")) { "Serial chưa xuất hoặc đã nhận trả trước đó." }
        require(serial.dealerId == dealerId && serial.lastDispatchCode != null) { "Không có chứng từ xuất đích danh cho đơn vị này." }
        val dispatch = requireNotNull(workflow.dispatchByCode(serial.lastDispatchCode)) { "Không tìm thấy phiếu xuất gốc; cần đối soát dữ liệu cũ trước khi nhận." }
        require(dispatch.dealerId == dealerId && workflow.allocations(dispatch.orderCode).any { it.serialNumber == serial.serialNumber }) { "Nguồn gốc Serial không khớp phiếu xuất gốc." }
        val newSeal = condition in setOf("HANG_MOI", "PERFECT")
        val target = if (newSeal) "Kho Mới - Khu tiếp nhận hoàn trả" else "Kho Lỗi C-01 - Chờ kiểm định"
        val code = newCode("TS")
        workflow.insertReturn(OutboundReturnEntity(code, dispatch.dispatchCode, dealerId, serial.serialNumber,
            condition, reason.trim(), target, now(), actor.name))
        serials.update(serial.copy(status = if (newSeal) "IN_STOCK" else "DEFECTIVE", currentLocation = target,
            allocatedOrderCode = null, dealerId = null, dealerName = null))
        refreshProductCount(serial.productCode)
        val returningDealer = database.dealerDao().getDealerById(dealerId)
        if (returningDealer != null) {
            val returnValuation = serial.unitCost
            val reducedDebt = (returningDealer.currentDebt - returnValuation).coerceAtLeast(0.0)
            database.dealerDao().update(returningDealer.copy(currentDebt = reducedDebt))
        }
        movement("RETURN_DEALER", code, serial, serial.currentLocation, target, 1, actor)
        record("OUTBOUND_RETURN_RECEIVED", code, actor, "Nhận trả ${serial.serialNumber}, phiếu gốc ${dispatch.dispatchCode}; $target.",
            mapOf("returnCode" to code, "dispatchCode" to dispatch.dispatchCode, "serialNumber" to serial.serialNumber, "condition" to condition, "reason" to reason.trim()))
        code
    }

    suspend fun recordOtherDispatch(input: String, purpose: String, reason: String, actor: OutboundActor): String = database.withTransaction {
        WarehouseOutboundRules.requireManager(actor)
        require(reason.isNotBlank()) { "Lý do và căn cứ kiểm định là bắt buộc." }
        val serial = requireNotNull(serials.getSerialByNumber(input.trim().uppercase(Locale.ROOT))) { "Không tìm thấy Serial." }
        val normalizedPurpose = when (purpose) {
            "WARRANTY", "BAO_HANH_HANG" -> "BAO_HANH_HANG"
            "DISPOSE", "TIEU_HUY" -> "TIEU_HUY"
            "LIQUIDATE", "LIQUIDATION", "THANH_LY" -> "THANH_LY"
            else -> error("Mục đích xuất khác không hợp lệ.")
        }
        if (normalizedPurpose == "TIEU_HUY") require(actor.role == "STORE_OWNER") { "Tiêu hủy cần Chủ kho xác nhận phê duyệt và biên bản kiểm định." }
        val previous = workflow.latestOtherForSerial(serial.serialNumber)
        val expectedStatus = when (normalizedPurpose) {
            "BAO_HANH_HANG" -> "WARRANTY"
            "TIEU_HUY" -> "LIQUIDATED"
            else -> "DA_THANH_LY"
        }
        if (serial.status == expectedStatus && previous?.purpose == normalizedPurpose && previous.reason == reason.trim()) {
            return@withTransaction previous.dispatchCode
        }
        require(serial.status in setOf("DEFECTIVE", "DEFECT", "DISPLAY") && serial.allocatedOrderCode == null) { "Chỉ xuất bảo hành/tiêu hủy hàng lỗi hoặc hàng trưng bày chưa được giữ chỗ." }
        val code = newCode("XK")
        val targetStatus = expectedStatus
        val target = when (normalizedPurpose) {
            "BAO_HANH_HANG" -> "Đã gửi Trung tâm bảo hành"
            "TIEU_HUY" -> "Đã xuất tiêu hủy"
            else -> "Đã xuất bán thanh lý (Display)"
        }
        workflow.insertOtherDispatch(OutboundOtherDispatchEntity(code, serial.serialNumber, normalizedPurpose, reason.trim(), serial.currentLocation,
            now(), actor.name, actor.name))
        serials.update(serial.copy(status = targetStatus, currentLocation = target))
        refreshProductCount(serial.productCode)
        movement(if (targetStatus == "WARRANTY") "WARRANTY" else if (targetStatus == "DA_THANH_LY") "LIQUIDATION" else "DISPOSAL", code, serial, serial.currentLocation, target, -1, actor)
        record("OUTBOUND_OTHER_DISPATCHED", code, actor, "$normalizedPurpose Serial ${serial.serialNumber}; lý do: ${reason.trim()}.",
            mapOf("dispatchCode" to code, "serialNumber" to serial.serialNumber, "purpose" to normalizedPurpose, "reason" to reason.trim()))
        code
    }

    suspend fun recordReceiptVoucher(
        dealerId: String,
        amount: Double,
        paymentMethod: String,
        referenceDoc: String,
        note: String,
        actor: OutboundActor
    ): String = database.withTransaction {
        WarehouseOutboundRules.requireManager(actor)
        val dealer = requireNotNull(database.dealerDao().getDealerById(dealerId)) { "Không tìm thấy đơn vị nhận." }
        val eval = OutboundLogisticsManager.validateClearanceVoucher(amount, dealer.currentDebt)
        require(eval.isValid) { eval.errorMessage ?: "Số tiền giải phóng bảo lãnh không hợp lệ." }
        val receiptId = newCode("PT")
        val receipt = DealerReceiptEntity(
            receiptId = receiptId,
            dealerId = dealer.dealerId,
            dealerName = dealer.name,
            amount = amount,
            paymentMethod = paymentMethod,
            referenceDoc = referenceDoc.trim(),
            date = now(),
            note = note.trim()
        )
        database.dealerReceiptDao().insert(receipt)
        val updatedDealer = dealer.copy(currentDebt = eval.remainingCustody)
        database.dealerDao().update(updatedDealer)
        record(
            "EVENT_DEBT_CLEARED",
            receiptId,
            actor,
            "Lập phiếu thu/giải phóng nợ $receiptId: thu ${OutboundLogisticsManager.formatVnd(amount)} đ cho ${dealer.name}, dư nợ còn ${OutboundLogisticsManager.formatVnd(eval.remainingCustody)} đ.",
            receipt
        )
        receiptId
    }

    suspend fun dispatchDocument(code: String): OutboundDocument = database.withTransaction { documentInsideTransaction(code) }

    private suspend fun documentInsideTransaction(code: String): OutboundDocument {
        val order = requireOrder(code)
        val dispatch = requireNotNull(workflow.dispatchForOrder(code)) { "Lệnh chưa có phiếu xuất hoàn tất." }
        return OutboundDocument(dispatch.dispatchCode, code, dispatch.dealerName, dispatch.address, dispatch.dispatchedAt,
            order.createdBy, order.approvedBy, dispatch.dispatchedBy, dispatch.carrier, dispatch.trackingNumber, dispatch.note,
            workflow.allocations(code).map { it.toPick() }, workflow.orderLines(code))
    }

    private suspend fun reserveExactSerials(order: OutboundOrderEntity) {
        val lines = workflow.orderLines(order.orderCode)
        require(lines.isNotEmpty()) { "Lệnh thiếu chi tiết mặt hàng." }
        val picks = lines.flatMap { line ->
            val product = requireNotNull(database.productDao().getProductByCode(line.productCode)) { "Không tìm thấy SKU ${line.productCode}." }
            require(product.status != "DISCONTINUED" && line.convertedQuantity >= product.minDispatchQuantity) { "SKU ${line.productCode} không đạt điều kiện xuất hiện tại." }
            val candidates = serials.getSerialsByProduct(line.productCode).filter { it.status == "IN_STOCK" && it.allocatedOrderCode == null }
                .sortedWith(compareBy<SerialEntity> { OutboundLogisticsManager.parseImportDateKey(it.importDate) }.thenBy { it.serialNumber })
            require(candidates.size >= line.convertedQuantity) { "SKU ${line.productCode} chỉ còn ${candidates.size} Serial khả dụng; không thể duyệt ${line.convertedQuantity}." }
            candidates.take(line.convertedQuantity).map { serial ->
                require(serial.unitCost.isFinite() && serial.unitCost >= 0.0) { "Giá trị Serial ${serial.serialNumber} không hợp lệ; cần đối soát trước khi xuất." }
                OutboundAllocationEntity(order.orderCode, serial.serialNumber, serial.productCode, line.productName,
                    serial.currentLocation, serial.importDate, serial.unitCost, OutboundLogisticsManager.inferLotNumber(serial, candidates))
            }
        }
        picks.forEach { check(serials.reserve(it.serialNumber, order.orderCode) == 1) { "Serial ${it.serialNumber} vừa được lệnh khác giữ chỗ; hãy tải lại." } }
        workflow.insertAllocations(picks)
        picks.groupBy { it.productCode }.forEach { (productCode, allocated) ->
            workflow.updateLineCost(order.orderCode, productCode, allocated.map { it.unitCost }.average())
        }
    }

    private suspend fun ensureLegacyReservation(order: OutboundOrderEntity) {
        if (workflow.allocations(order.orderCode).isEmpty()) {
            // v5 reserved quantities did not identify Serials. Adopt only if the full order is available.
            reserveExactSerials(order)
            record("LEGACY_RESERVATION_LINKED", order.orderCode, OutboundActor("Chuyển dữ liệu v5", "SYSTEM_MIGRATION"),
                "Gắn Serial đích danh cho lệnh đã giữ chỗ từ v5; không tạo mới phê duyệt.",
                mapOf("orderCode" to order.orderCode, "allocations" to workflow.allocations(order.orderCode)))
        }
    }

    private suspend fun importLegacyDetails() {
        orders.getAllOrders().forEach { order ->
            if (workflow.orderLines(order.orderCode).isEmpty()) {
                workflow.insertLines(listOf(OutboundLineEntity(order.orderCode, order.productCode, order.productName,
                    order.unit, order.quantity, order.convertedQuantity, order.unitPrice)))
            }
            if (order.status == "COMPLETED" && workflow.dispatchForOrder(order.orderCode) == null) {
                val dealer = database.dealerDao().getDealerById(order.dealerId)
                val code = "PX-MIG-${order.orderCode}"
                workflow.insertDispatch(OutboundDispatchEntity(code, order.orderCode, order.dealerId, order.dealerName,
                    dealer?.address.orEmpty(), order.dispatchedAt.ifBlank { order.createdDate }, order.dispatchedBy, "", "", "Dữ liệu chuyển từ v5; chưa ghi riêng thông tin bàn giao."))
                val allocations = order.dispatchedSerials.split(',').map { it.trim() }.filter { it.isNotBlank() }.mapNotNull { sn ->
                    serials.getSerialByNumber(sn)?.let { serial ->
                        if (serial.status in setOf("DISPATCHED", "DELIVERED", "SOLD") && serial.dealerId == null) {
                            serials.update(serial.copy(dealerId = order.dealerId, lastDispatchCode = code, lastDispatchAt = order.dispatchedAt.ifBlank { order.createdDate }))
                        }
                        OutboundAllocationEntity(order.orderCode, serial.serialNumber, serial.productCode, order.productName,
                            serial.currentLocation, serial.importDate, serial.unitCost, 1)
                    }
                }
                if (allocations.isNotEmpty()) workflow.insertAllocations(allocations)
            }
        }
    }

    private suspend fun refreshProductCount(productCode: String) {
        val product = database.productDao().getProductByCode(productCode) ?: return
        val physical = serials.newPhysicalCount(productCode)
        if (product.stockQuantity != physical) database.productDao().updateProduct(product.copy(stockQuantity = physical))
    }

    private suspend fun movement(type: String, reference: String, serial: SerialEntity, from: String, to: String, change: Int, actor: OutboundActor) {
        workflow.insertMovement(StockMovementEntity(UUID.randomUUID().toString(), type, reference, serial.serialNumber,
            serial.productCode, from, to, change, serials.warehouseCount(serial.productCode), actor.name, now()))
    }

    private suspend fun record(type: String, aggregate: String, actor: OutboundActor, detail: String, payload: Any) {
        val time = now()
        database.auditLogDao().insertLog(AuditLogEntity(timestamp = time, actorName = actor.name, role = actor.role, action = type, details = detail, ipAddress = "Thiết bị kho cục bộ"))
        workflow.insertSyncEvent(OutboundSyncEventEntity(UUID.randomUUID().toString(), type, aggregate, gson.toJson(payload), time))
    }

    private suspend fun requireOrder(code: String) = requireNotNull(orders.getOrderByCode(code)) { "Không tìm thấy lệnh $code." }
    private fun OutboundAllocationEntity.toPick() = OutboundPick(serialNumber, productCode, productName, sourceLocation, importDate, unitCost, lotNumber)
    private fun newCode(prefix: String) = "$prefix-${LocalDate.now(ZoneId.of("Asia/Ho_Chi_Minh")).year}-${UUID.randomUUID()}"
    private fun now(): String = LocalDateTime.now(ZoneId.of("Asia/Ho_Chi_Minh")).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS"))
    private fun parseTimestamp(value: String): String = if (value.length >= 10 && value[4] == '-') value else
        runCatching { LocalDateTime.parse(value, DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm")).toString() }.getOrDefault(value)
}
