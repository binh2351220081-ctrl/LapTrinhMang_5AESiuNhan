package com.example.chronovaultwms.outbound

import com.example.chronovaultwms.core.database.DealerEntity
import com.example.chronovaultwms.core.database.OutboundOrderEntity
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.core.database.SerialEntity
import java.text.DecimalFormat
import java.text.DecimalFormatSymbols
import java.util.Locale

/**
 * Kết quả thẩm định Lệnh điều phối xuất kho & Hạn mức bảo lãnh tài sản (MOD-03-01).
 */
data class OutboundOrderEvaluation(
    val convertedQuantity: Int,
    val availableStock: Int,
    val baseUnitValuation: Double,
    val allocationFactor: Double,
    val effectiveUnitValuation: Double,
    val totalValuation: Double,
    val collateralDeposit: Double,
    val newCustodyLiability: Double,
    val projectedCustody: Double,
    val creditLimit: Double,
    val isDealerLocked: Boolean,
    val isInvalidQuantity: Boolean,
    val isBelowMoq: Boolean,
    val isInsufficientStock: Boolean,
    val isOverCustodyLimit: Boolean,
    val excessCustodyAmount: Double,
    val canSubmit: Boolean,
    val rejectionReason: String?
)

/**
 * Dòng chỉ định trong Phiếu soạn hàng thông minh (Smart Picking List - MOD-03-02).
 * Chỉ định chính xác từng mã Serial theo thứ tự FIFO kèm tọa độ ngăn kệ 5 cấp và giá vốn đích danh.
 */
data class PickingItem(
    val lotNumber: Int,
    val serialNumber: String,
    val currentLocation: String,
    val importDate: String,
    val unitCost: Double
)

/**
 * Kết quả đối soát thời gian thực khi quét Camera/Barcode Serial đóng kiện (MOD-03-02).
 */
data class SerialValidationResult(
    val isValid: Boolean,
    val errorMessage: String? = null,
    val validatedSerial: SerialEntity? = null
)

/**
 * Kết quả thẩm định Phiếu xác nhận bàn giao & giải phóng hạn mức bảo lãnh (TC-05).
 */
data class ClearanceValidationResult(
    val isValid: Boolean,
    val errorMessage: String? = null,
    val remainingCustody: Double = 0.0
)

/**
 * Kết quả kiểm tra xuất kho phi thương mại: Bảo hành hãng hoặc Tiêu hủy (MOD-03-03).
 */
data class NonCommercialDispatchResult(
    val isValid: Boolean,
    val targetStatus: String? = null,
    val errorMessage: String? = null
)

/**
 * Kết quả tiếp nhận hàng hoàn trả về kho tổng & phân loại chất lượng (MOD-03-04).
 */
data class ReturnInspectionResult(
    val isValid: Boolean,
    val targetStatus: String? = null,
    val targetWarehouseZone: String? = null,
    val errorMessage: String? = null
)

/**
 * Động cơ nghiệp vụ Kho vận Xuất kho (Outbound Logistics Engine) - Phân hệ 3 (TV3: Tô Đức Thảo).
 * Thuần túy điều phối lưu chuyển tài sản kho (Inbound/Outbound Storage Hub), không có nghiệp vụ mua bán.
 */
object OutboundLogisticsManager {

    const val UNITS_PER_BOX = 10

    const val ORDER_RESERVED = "RESERVED"
    const val ORDER_DRAFT = "DRAFT"
    const val ORDER_PACKING = "PACKING"
    const val ORDER_COMPLETED = "COMPLETED"
    const val ORDER_CANCELLED = "CANCELLED"

    const val DEALER_ACTIVE = "ACTIVE"

    const val SERIAL_IN_STOCK = "IN_STOCK"
    const val SERIAL_ALLOCATED = "ALLOCATED"
    const val SERIAL_DISPLAY = "DISPLAY"
    const val SERIAL_DEFECTIVE = "DEFECTIVE"
    const val SERIAL_DISPATCHED = "DISPATCHED"
    const val SERIAL_DELIVERED = "DELIVERED"
    const val SERIAL_WARRANTY = "BAO_HANH"
    const val SERIAL_DESTROYED = "DA_TIEU_HUY"
    const val SERIAL_LIQUIDATED = "DA_THANH_LY"

    const val PURPOSE_WARRANTY = "BAO_HANH_HANG"
    const val PURPOSE_DESTROY = "TIEU_HUY"
    const val PURPOSE_LIQUIDATION = "THANH_LY"

    private val vndFormat: DecimalFormat
        get() = DecimalFormat("#,###", DecimalFormatSymbols(Locale.US))

    fun formatVnd(amount: Double): String = vndFormat.format(amount)

    /**
     * Chuẩn hóa mã SKU hỗ trợ cả ký hiệu mã sản phẩm đầy đủ và mã rút gọn (RLX-SUB-126610LN <-> RLX-126610LN).
     */
    fun normalizeProductCode(code: String): String {
        val trimmed = code.trim().uppercase(Locale.ROOT)
        return if (trimmed == "RLX-SUB-126610LN") "RLX-126610LN" else trimmed
    }

    /**
     * Quy đổi đơn vị tính 2 cấp (Thùng -> Chiếc lẻ).
     */
    fun convertQuantity(
        isBox: Boolean,
        quantity: Int,
        conversionRate: Int = UNITS_PER_BOX
    ): Int {
        if (quantity <= 0 || conversionRate <= 0) return 0
        return try { if (isBox) Math.multiplyExact(quantity, conversionRate) else quantity }
        catch (_: ArithmeticException) { 0 }
    }

    /**
     * Tổng hợp số lượng đang bị khóa giữ chỗ (RESERVED) theo từng mã SKU từ danh sách Lệnh điều phối.
     */
    fun calculateReservedByProduct(orders: List<OutboundOrderEntity>): Map<String, Int> {
        return orders
            .filter { it.status in setOf(ORDER_RESERVED, ORDER_PACKING) }
            .groupBy { it.productCode }
            .mapValues { (_, items) -> items.sumOf { it.convertedQuantity } }
    }

    /**
     * Tính tồn khả dụng thực tế chống xuất âm kho: Available = Physical - Reserved.
     */
    fun calculateAvailableStock(physicalStock: Int, reservedQuantity: Int): Int {
        return (physicalStock - reservedQuantity).coerceAtLeast(0)
    }

    /**
     * Thẩm định toàn diện điều kiện khởi tạo & duyệt Lệnh điều phối xuất kho (MOD-03-01):
     *   1. Trạng thái đơn vị tiếp nhận (`ACTIVE`).
     *   2. Định mức xuất tối thiểu (MOQ) và số lượng quy đổi (> 0).
     *   3. Tồn khả dụng (Reservation Engine: Available = Physical - Reserved).
     *   4. Hạn mức bảo lãnh trách nhiệm tài sản (Custody Limit: currentDebt + newLiability <= creditLimit).
     */
    fun evaluateOutboundOrder(
        dealer: DealerEntity,
        product: ProductEntity,
        isBox: Boolean,
        quantity: Int,
        collateralDeposit: Double,
        reservedQuantity: Int,
        minOrderQty: Int = product.minDispatchQuantity,
        conversionRate: Int = product.conversionRate,
        pendingReservedExposure: Double? = null
    ): OutboundOrderEvaluation {
        val convertedQty = convertQuantity(isBox, quantity, conversionRate)
        val availableStock = calculateAvailableStock(product.stockQuantity, reservedQuantity)

        val baseUnitValuation = product.wholesalePrice
        val allocationFactor = dealer.discountPercent.coerceIn(0.0, 0.5)
        val effectiveUnitValuation = baseUnitValuation * (1.0 - allocationFactor)
        val totalValuation = effectiveUnitValuation * convertedQty

        val pendingExposure = pendingReservedExposure ?: (reservedQuantity * effectiveUnitValuation)
        val sanitizedDeposit = collateralDeposit.coerceAtLeast(0.0)
        val newCustodyLiability = (totalValuation - sanitizedDeposit).coerceAtLeast(0.0)
        val projectedCustody = dealer.currentDebt + pendingExposure + newCustodyLiability

        val isExcessDeposit = collateralDeposit > totalValuation
        val isDealerLocked = dealer.status != DEALER_ACTIVE
        val isInvalidQuantity = quantity <= 0 || convertedQty <= 0 || conversionRate <= 0
        val isBelowMoq = !isInvalidQuantity && convertedQty < minOrderQty
        val isInsufficientStock = !isInvalidQuantity && convertedQty > availableStock
        val isOverCustodyLimit = projectedCustody > dealer.creditLimit
        val excessCustodyAmount = (projectedCustody - dealer.creditLimit).coerceAtLeast(0.0)

        val rejectionReason = when {
            listOf(collateralDeposit, dealer.currentDebt, dealer.creditLimit, product.wholesalePrice, dealer.discountPercent, pendingExposure).any { !it.isFinite() } ->
                "Giá trị tài sản/bảo lãnh phải là số hữu hạn hợp lệ."
            isExcessDeposit ->
                "⚠️ Tiền đặt cọc/bảo lãnh (${formatVnd(collateralDeposit)} đ) không được vượt quá tổng giá trị đơn hàng (${formatVnd(totalValuation)} đ)!"
            isDealerLocked ->
                "⚠️ Đơn vị tiếp nhận ${dealer.name} đang ở trạng thái ${dealer.status}, bị khóa quyền điều phối!"
            isInvalidQuantity ->
                "⚠️ Số lượng yêu cầu xuất kho phải lớn hơn 0!"
            isBelowMoq ->
                "⚠️ Số lượng quy đổi ($convertedQty chiếc) chưa đạt định mức xuất tối thiểu (MOQ: $minOrderQty chiếc)!"
            isInsufficientStock ->
                "⚠️ Vượt quá Tồn khả dụng! Yêu cầu $convertedQty chiếc nhưng chỉ còn $availableStock chiếc khả dụng (Vật lý: ${product.stockQuantity}, Giữ chỗ: $reservedQuantity)."
            isOverCustodyLimit ->
                "⚠️ CẢNH BÁO: ĐƠN HÀNG VƯỢT HẠN MỨC BẢO LÃNH TÀI SẢN / HẠN MỨC TÍN DỤNG CỦA ĐẠI LÝ ${dealer.name}! (${formatVnd(projectedCustody)} đ > ${formatVnd(dealer.creditLimit)} đ, vượt ${formatVnd(excessCustodyAmount)} đ)."
            else -> null
        }

        return OutboundOrderEvaluation(
            convertedQuantity = convertedQty,
            availableStock = availableStock,
            baseUnitValuation = baseUnitValuation,
            allocationFactor = allocationFactor,
            effectiveUnitValuation = effectiveUnitValuation,
            totalValuation = totalValuation,
            collateralDeposit = sanitizedDeposit,
            newCustodyLiability = newCustodyLiability,
            projectedCustody = projectedCustody,
            creditLimit = dealer.creditLimit,
            isDealerLocked = isDealerLocked,
            isInvalidQuantity = isInvalidQuantity,
            isBelowMoq = isBelowMoq,
            isInsufficientStock = isInsufficientStock,
            isOverCustodyLimit = isOverCustodyLimit,
            excessCustodyAmount = excessCustodyAmount,
            canSubmit = rejectionReason == null,
            rejectionReason = rejectionReason
        )
    }

    /**
     * Chuyển đổi chuỗi ngày giờ nhập kho ("dd/MM/yyyy HH:mm" hoặc "dd/MM/yyyy") thành khóa số YYYYMMDDHHMM
     * để sắp xếp FIFO chính xác qua các tháng/năm mà không phụ thuộc Locale.
     */
    fun parseImportDateKey(importDate: String): Long {
        return runCatching {
            val parts = importDate.trim().replace('T', ' ').split(" ")
            val date = if ('/' in parts[0]) {
                val bits = parts[0].split('/').map(String::toInt)
                java.time.LocalDate.of(bits[2], bits[1], bits[0])
            } else java.time.LocalDate.parse(parts[0])
            val timeParts = parts.getOrNull(1)?.split(':')
            val hour = timeParts?.getOrNull(0)?.toInt() ?: 0
            val minute = timeParts?.getOrNull(1)?.toInt() ?: 0
            java.time.LocalDateTime.of(date, java.time.LocalTime.of(hour, minute)).toEpochSecond(java.time.ZoneOffset.UTC)
        }.getOrDefault(Long.MAX_VALUE)
    }

    private fun buildLotIndexMap(productSerials: List<SerialEntity>): Map<Pair<String, Double>, Int> {
        val sortedLots = productSerials
            .filter { it.status == SERIAL_IN_STOCK }
            .sortedWith(compareBy<SerialEntity> { parseImportDateKey(it.importDate) }.thenBy { it.serialNumber })
            .map { it.importDate.substringBefore(" ") to it.unitCost }
            .distinct()
        return sortedLots.mapIndexed { idx, key -> key to (idx + 1) }.toMap()
    }

    /**
     * Xác định số thứ tự Lô nhập của một Serial dựa trên ngày nhập & giá vốn đích danh.
     */
    fun inferLotNumber(serial: SerialEntity, allProductSerials: List<SerialEntity>): Int {
        val lotMap = buildLotIndexMap(allProductSerials.filter { it.productCode == serial.productCode })
        val key = serial.importDate.substringBefore(" ") to serial.unitCost
        return lotMap[key] ?: 1
    }

    /**
     * Sinh Phiếu soạn hàng thông minh (Smart Picking List - MOD-03-02, Câu hỏi 6):
     * Chỉ định đích danh Serial khả dụng (`IN_STOCK`) theo thứ tự FIFO (nhập trước xuất trước),
     * kèm theo tọa độ ngăn kệ 5 cấp (`currentLocation`) và giá vốn đích danh (`unitCost`).
     */
    fun generateSmartPickingList(
        productSerials: List<SerialEntity>,
        productCode: String,
        requiredQty: Int
    ): List<PickingItem> {
        if (requiredQty <= 0) return emptyList()
        val normSku = normalizeProductCode(productCode)
        val sameSkuSerials = productSerials.filter { normalizeProductCode(it.productCode) == normSku }
        val lotMap = buildLotIndexMap(sameSkuSerials)

        return sameSkuSerials
            .filter { it.status == SERIAL_IN_STOCK }
            .sortedWith(compareBy<SerialEntity> { parseImportDateKey(it.importDate) }.thenBy { it.serialNumber })
            .take(requiredQty)
            .map { serial ->
                val lotKey = serial.importDate.substringBefore(" ") to serial.unitCost
                PickingItem(
                    lotNumber = lotMap[lotKey] ?: 1,
                    serialNumber = serial.serialNumber,
                    currentLocation = serial.currentLocation,
                    importDate = serial.importDate,
                    unitCost = serial.unitCost
                )
            }
    }

    /**
     * Kiểm tra đối khớp chéo thời gian thực (Real-time Cross-check) khi quét Serial xuất kho (FR-09, TC-03, TC-04, TC-06):
     *   - Không rỗng và chưa được quét trùng trong cùng kiện hàng.
     *   - Tồn tại trong CSDL và đúng mã SKU của Lệnh xuất.
     *   - Trạng thái bắt buộc là `IN_STOCK` (Hàng mới nguyên seal; chặn tuyệt đối `DEFECTIVE`, `DISPLAY`, `ALLOCATED`, `DISPATCHED`).
     *   - Thuộc đúng danh sách Serial / Lô chỉ định trong Smart Picking List (chặn xuất sai lô & sai giá vốn).
     */
    fun validateScannedSerial(
        inputSerial: String,
        order: OutboundOrderEntity,
        serialEntity: SerialEntity?,
        pickingList: List<PickingItem>,
        alreadyScanned: List<String>,
        allProductSerials: List<SerialEntity> = emptyList()
    ): SerialValidationResult {
        val trimmed = inputSerial.trim()
        if (trimmed.isEmpty()) {
            return SerialValidationResult(false, "Vui lòng nhập hoặc quét mã Serial!")
        }
        if (alreadyScanned.any { it.equals(trimmed, ignoreCase = true) }) {
            return SerialValidationResult(false, "Mã Serial $trimmed đã được quét rồi!")
        }
        if (alreadyScanned.size >= order.convertedQuantity) {
            return SerialValidationResult(false, "Đã quét đủ ${order.convertedQuantity} chiếc cần xuất!")
        }
        if (serialEntity == null) {
            return SerialValidationResult(false, "Lỗi: Không tìm thấy Serial $trimmed trong hệ thống!")
        }
        if (normalizeProductCode(serialEntity.productCode) != normalizeProductCode(order.productCode)) {
            return SerialValidationResult(
                false,
                "Lỗi: Serial $trimmed thuộc mã SKU ${serialEntity.productCode}, không khớp với mã SKU ${order.productCode} của Lệnh xuất!"
            )
        }
        if (serialEntity.status != SERIAL_IN_STOCK) {
            val statusDesc = when (serialEntity.status) {
                SERIAL_DEFECTIVE -> "Hàng lỗi kỹ thuật cách ly (DEFECTIVE)"
                SERIAL_DISPLAY -> "Hàng mẫu trưng bày (DISPLAY)"
                SERIAL_ALLOCATED -> "Đã khóa giữ chỗ cho lệnh khác (ALLOCATED)"
                SERIAL_DISPATCHED, SERIAL_DELIVERED -> "Đã xuất kho bàn giao trước đó (${serialEntity.status})"
                else -> serialEntity.status
            }
            return SerialValidationResult(
                false,
                "Lỗi: Serial ${serialEntity.serialNumber} có trạng thái $statusDesc, không được phép xuất kho!"
            )
        }
        if (pickingList.isEmpty()) {
            return SerialValidationResult(
                false,
                "Danh sách chỉ định xuất kho (Picking List) đang rỗng hoặc chưa được khởi tạo!"
            )
        }
        if (pickingList.none { it.serialNumber == serialEntity.serialNumber }) {
            val lotNum = inferLotNumber(serialEntity, allProductSerials.ifEmpty { listOf(serialEntity) })
            return SerialValidationResult(
                false,
                "Cảnh báo sai lô: Serial ${serialEntity.serialNumber} thuộc Lô $lotNum (Giá vốn ${formatVnd(serialEntity.unitCost)} đ tại ${serialEntity.currentLocation}), không khớp với danh sách Lô cần xuất trong Picking List!"
            )
        }
        return SerialValidationResult(true, null, serialEntity)
    }

    /**
     * Thẩm định Phiếu xác nhận bàn giao & giải phóng hạn mức bảo lãnh tài sản (TC-05).
     */
    fun validateClearanceVoucher(amount: Double, currentCustody: Double): ClearanceValidationResult {
        if (!amount.isFinite() || !currentCustody.isFinite() || currentCustody < 0.0 || amount <= 0.0) {
            return ClearanceValidationResult(false, "Vui lòng nhập giá trị giải phóng bảo lãnh hợp lệ (> 0)!")
        }
        if (amount > currentCustody) {
            return ClearanceValidationResult(
                false,
                "Giá trị giải phóng (${formatVnd(amount)} đ) không được vượt quá giá trị tài sản đang giữ (${formatVnd(currentCustody)} đ)!"
            )
        }
        return ClearanceValidationResult(true, null, (currentCustody - amount).coerceAtLeast(0.0))
    }

    /**
     * Kiểm tra quy tắc xuất kho phi thương mại (MOD-03-03): Bảo hành hãng / Tiêu hủy phế phẩm.
     */
    fun evaluateNonCommercialDispatch(
        serial: SerialEntity,
        purpose: String,
        actorRole: String
    ): NonCommercialDispatchResult {
        if (purpose !in setOf(PURPOSE_WARRANTY, PURPOSE_DESTROY, PURPOSE_LIQUIDATION, "LIQUIDATION", "THANH_LY")) {
            return NonCommercialDispatchResult(false, errorMessage = "Mục đích xuất phi thương mại không hợp lệ: $purpose")
        }
        if (purpose == PURPOSE_DESTROY && actorRole != "STORE_OWNER") {
            return NonCommercialDispatchResult(
                false,
                errorMessage = "Nghiêm cấm xuất tiêu hủy tài sản khi chưa có phê duyệt của Chủ kho (STORE_OWNER)!"
            )
        }
        if (serial.status !in setOf(SERIAL_DEFECTIVE, SERIAL_DISPLAY)) {
            return NonCommercialDispatchResult(
                false,
                errorMessage = "Chỉ cho phép xuất bảo hành/tiêu hủy đối với hàng lỗi (DEFECTIVE) hoặc hàng trưng bày (DISPLAY)!"
            )
        }
        val targetStatus = when (purpose) {
            PURPOSE_WARRANTY -> SERIAL_WARRANTY
            PURPOSE_DESTROY -> SERIAL_DESTROYED
            else -> SERIAL_LIQUIDATED
        }
        return NonCommercialDispatchResult(true, targetStatus = targetStatus)
    }

    /**
     * Kiểm tra tiếp nhận hàng hoàn trả về kho tổng & phân loại tái nhập kho (MOD-03-04).
     */
    fun evaluateWarehouseReturn(
        serial: SerialEntity?,
        returningDealerName: String,
        inspectedCondition: String
    ): ReturnInspectionResult {
        if (serial == null) {
            return ReturnInspectionResult(false, errorMessage = "Không tìm thấy mã Serial hoàn trả trong CSDL!")
        }
        if (serial.status !in setOf(SERIAL_DISPATCHED, SERIAL_DELIVERED)) {
            return ReturnInspectionResult(
                false,
                errorMessage = "Serial ${serial.serialNumber} không ở trạng thái đã xuất bàn giao (${serial.status}), từ chối nhập hoàn trả!"
            )
        }
        val ownerName = serial.dealerName ?: ""
        if (ownerName.isBlank() || returningDealerName.isBlank() || !ownerName.trim().equals(returningDealerName.trim(), ignoreCase = true)) {
            return ReturnInspectionResult(
                false,
                errorMessage = "Serial ${serial.serialNumber} không thuộc lịch sử bàn giao của đơn vị $returningDealerName!"
            )
        }
        val isNewSeal = inspectedCondition.equals("HANG_MOI", ignoreCase = true) ||
            inspectedCondition.equals("PERFECT", ignoreCase = true)
        return if (isNewSeal) {
            ReturnInspectionResult(true, SERIAL_IN_STOCK, "Kho Mới (Khu K1)")
        } else {
            ReturnInspectionResult(true, SERIAL_DEFECTIVE, "Kho Lỗi C-01")
        }
    }
}

