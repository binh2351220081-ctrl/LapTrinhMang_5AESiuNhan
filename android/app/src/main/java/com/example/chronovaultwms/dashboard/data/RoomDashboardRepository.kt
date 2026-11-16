package com.example.chronovaultwms.dashboard.data

import androidx.room.withTransaction
import com.example.chronovaultwms.core.database.*
import com.example.chronovaultwms.dashboard.model.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.withContext
import java.text.NumberFormat
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.TextStyle
import java.time.temporal.ChronoUnit
import java.util.Locale

/** TV5 integration reads actual warehouse documents. A dispatch is not a sale or cash receipt. */
class RoomDashboardRepository(private val database: ChronoVaultDatabase) : DashboardRepository {
    override fun observeDashboard(): Flow<DashboardSnapshot> = database.invalidationTracker.createFlow(
        "products", "serials", "outbound_orders", "outbound_dispatches", "outbound_allocations",
        "outbound_returns", "outbound_other_dispatches", "stock_movements", "audit_logs"
    ).map { loadSnapshot() }

    private data class Data(
        val products: List<ProductEntity>, val serials: List<SerialEntity>, val orders: List<OutboundOrderEntity>,
        val dispatches: List<OutboundDispatchEntity>, val allocations: Map<String, List<OutboundAllocationEntity>>,
        val returns: List<OutboundReturnEntity>, val other: List<OutboundOtherDispatchEntity>,
        val movements: List<StockMovementEntity>, val logs: List<AuditLogEntity>
    )

    private suspend fun loadData(): Data = database.withTransaction {
        DatabaseSeeder.checkAndSeed(database.productDao(), database.serialDao(), database.userDao(),
            database.auditLogDao(), database.dealerDao(), database.outboundOrderDao(), database.dealerReceiptDao())
        val workflow = database.outboundWorkflowDao()
        val dispatches = workflow.allDispatches()
        Data(database.productDao().getAllProducts(), database.serialDao().getAllSerials(),
            database.outboundOrderDao().getAllOrders(), dispatches,
            dispatches.associate { it.orderCode to workflow.allocations(it.orderCode) },
            workflow.allReturns(), workflow.allOtherDispatches(), workflow.allMovements(), database.auditLogDao().getAllLogs())
    }

    private suspend fun loadSnapshot(): DashboardSnapshot = withContext(Dispatchers.IO) {
        val data = loadData()
        val warehouse = data.serials.filter { it.status in PHYSICAL_STATUSES }
        val dispatched = data.dispatches.flatMap { data.allocations[it.orderCode].orEmpty() }
        val dispatchedValue = dispatched.sumOf { it.unitCost }
        val currentMonth = LocalDate.now().withDayOfMonth(1)
        val monthly = (5 downTo 0).map { offset ->
            val month = currentMonth.minusMonths(offset.toLong())
            val value = data.dispatches.filter { parseDate(it.dispatchedAt)?.withDayOfMonth(1) == month }
                .sumOf { data.allocations[it.orderCode].orEmpty().sumOf { serial -> serial.unitCost } }
            MonthlyRevenue(month.month.getDisplayName(TextStyle.SHORT, VI), value)
        }
        val top = dispatched.groupBy { it.productCode }.map { (code, rows) ->
            TopProduct(code, rows.first().productName, rows.size, rows.sumOf { it.unitCost })
        }.sortedByDescending { it.quantitySold }.take(5)
        DashboardSnapshot(
            periodLabel = "Nhập – xuất – tồn • chứng từ Room dùng chung",
            kpis = DashboardKpis(warehouse.sumOf { it.unitCost }, dispatchedValue,
                data.orders.count { it.status in setOf("DRAFT", "RESERVED", "PACKING") },
                data.serials.count { it.status == "IN_STOCK" && it.allocatedOrderCode == null },
                if (dispatched.isEmpty()) 0.0 else data.returns.size * 100.0 / dispatched.size),
            monthlyRevenue = monthly,
            costStructure = listOf(
                CostSlice("Hàng mới", warehouse.filter { it.status == "IN_STOCK" }.sumOf { it.unitCost }),
                CostSlice("Giữ chỗ", warehouse.filter { it.status == "ALLOCATED" }.sumOf { it.unitCost }),
                CostSlice("Trưng bày", warehouse.filter { it.status == "DISPLAY" }.sumOf { it.unitCost }),
                CostSlice("Hàng lỗi", warehouse.filter { it.status in setOf("DEFECT", "DEFECTIVE", "RETURNED") }.sumOf { it.unitCost })
            ), topProducts = top,
            recentActivities = data.logs.sortedByDescending { sortableDate(it.timestamp) }.take(6).map {
                AuditActivity(it.timestamp, it.action.replace('_', ' '), it.details, it.role)
            }
        )
    }

    override suspend fun loadReport(type: ReportType, range: DateRange): ReportTable = withContext(Dispatchers.IO) {
        val data = loadData()
        val products = data.products.associateBy { it.productCode }
        val serials = data.serials.filter { inRange(it.importDate, range) }
        val dispatches = data.dispatches.filter { inRange(it.dispatchedAt, range) }
        val returns = data.returns.filter { inRange(it.receivedAt, range) }
        val other = data.other.filter { inRange(it.dispatchedAt, range) }
        val allocations = dispatches.flatMap { data.allocations[it.orderCode].orEmpty() }
        fun report(headers: List<String>, rows: List<List<String>>, summary: String) =
            ReportTable(type, type.displayName, range, headers, rows.map(::ReportRow), summary)
        when (type) {
            ReportType.INBOUND -> report(listOf("Đơn vị giao", "Số Serial", "Giá trị nhập", "Ngày nhập"),
                serials.groupBy { it.supplierName }.map { (name, rows) ->
                    listOf(name, rows.size.toString(), money(rows.sumOf { it.unitCost }), rows.minByOrNull { sortableDate(it.importDate) }?.importDate.orEmpty())
                }, "${serials.size} Serial nhập trong kỳ • theo ngày nhập đã ghi nhận")
            ReportType.OUTBOUND -> report(listOf("Phiếu xuất", "Lệnh", "Đơn vị nhận", "Ngày xuất", "Số chiếc", "Người xác nhận"),
                dispatches.map { listOf(it.dispatchCode, it.orderCode, it.dealerName, it.dispatchedAt,
                    data.allocations[it.orderCode].orEmpty().size.toString(), it.dispatchedBy.ifBlank { "Chưa có dữ liệu cũ" }) },
                "${dispatches.size} phiếu xuất • ${allocations.size} chiếc • ${money(allocations.sumOf { it.unitCost })} giá trị đích danh")
            ReportType.DISPATCH_STRUCTURE -> {
                val warranty = other.count { it.purpose == "BAO_HANH_HANG" }
                val disposal = other.count { it.purpose == "TIEU_HUY" }
                val total = allocations.size + other.size
                report(listOf("Loại xuất", "Số chiếc", "Tỷ trọng"), listOf(
                    listOf("Bàn giao đơn vị nhận", allocations.size.toString(), percent(allocations.size, total)),
                    listOf("Gửi bảo hành", warranty.toString(), percent(warranty, total)),
                    listOf("Tiêu hủy", disposal.toString(), percent(disposal, total))
                ), "$total chiếc thực xuất theo chứng từ trong kỳ")
            }
            ReportType.RETURNS_QUALITY -> report(listOf("Phiếu trả", "Phiếu xuất gốc", "Serial", "Kiểm định", "Kho nhận lại", "Ngày nhận"),
                returns.map { listOf(it.returnCode, it.dispatchCode, it.serialNumber, it.inspectedCondition, it.targetLocation, it.receivedAt) },
                "${returns.size} chiếc hoàn trả • phân loại mới/lỗi theo kiểm định thực tế")
            ReportType.DEAD_STOCK -> {
                val aged = data.serials.filter { it.status == "IN_STOCK" }.mapNotNull { serial ->
                    parseDate(serial.importDate)?.let { date ->
                        val days = ChronoUnit.DAYS.between(date, range.to)
                        if (days > 90) serial to days else null
                    }
                }
                report(listOf("SKU", "Serial", "Số ngày lưu", "Vị trí", "Giá trị"),
                    aged.sortedByDescending { it.second }.map { (serial, days) ->
                        listOf(serial.productCode, serial.serialNumber, days.toString(), serial.currentLocation, money(serial.unitCost))
                    }, "${aged.size} chiếc chưa phân bổ, lưu kho trên 90 ngày tại ngày kết thúc")
            }
            ReportType.GROSS_PROFIT -> report(listOf("Phiếu xuất", "SKU", "Serial", "Vị trí xuất", "Giá trị đích danh"),
                dispatches.flatMap { dispatch -> data.allocations[dispatch.orderCode].orEmpty().map {
                    listOf(dispatch.dispatchCode, it.productCode, it.serialNumber, it.sourceLocation, money(it.unitCost))
                } }, "Tổng giá trị hàng xuất ${money(allocations.sumOf { it.unitCost })} • không hạch toán doanh thu")
            ReportType.TWO_WAY_DEBT -> {
                val units = dispatches.map { it.dealerId }.union(returns.map { it.dealerId }.toSet())
                report(listOf("Đơn vị nhận", "Số phiếu xuất", "Số chiếc xuất", "Số chiếc trả"), units.map { id ->
                    val sent = dispatches.filter { it.dealerId == id }
                    listOf(sent.firstOrNull()?.dealerName ?: id, sent.size.toString(),
                        sent.sumOf { data.allocations[it.orderCode].orEmpty().size }.toString(), returns.count { it.dealerId == id }.toString())
                }, "Đối soát giao nhận theo phiếu trong kỳ; không phát sinh công nợ bán hàng")
            }
            ReportType.CASHFLOW -> {
                val movements = data.movements.filter { inRange(it.timestamp, range) }
                report(listOf("Thời gian", "Chứng từ", "Loại", "SKU", "Serial", "+/-", "Tồn sau", "Người thực hiện"),
                    movements.map { listOf(it.timestamp, it.referenceCode, it.movementType, it.productCode,
                        it.serialNumber, it.changeQuantity.toString(), it.balanceAfter.toString(), it.actorName) },
                    "${movements.size} dòng Thẻ kho đã lưu; dữ liệu cũ chưa có Thẻ kho không được tự suy diễn")
            }
            ReportType.AUDIT_LOG -> {
                val logs = data.logs.filter { inRange(it.timestamp, range) }
                report(listOf("Thời gian", "Người dùng", "Vai trò", "Hành động", "Chi tiết"),
                    logs.map { listOf(it.timestamp, it.actorName, it.role, it.action, it.details) }, "${logs.size} nhật ký trong kỳ")
            }
        }
    }

    private fun inRange(value: String, range: DateRange): Boolean = parseDate(value)?.let {
        !it.isBefore(range.from) && !it.isAfter(range.to)
    } ?: false
    private fun parseDate(value: String): LocalDate? = runCatching { LocalDate.parse(value.take(10)) }.getOrNull()
        ?: runCatching { LocalDate.parse(value.take(10), DateTimeFormatter.ofPattern("dd/MM/yyyy")) }.getOrNull()
    private fun sortableDate(value: String) = parseDate(value)?.toString().orEmpty() + value.drop(10)
    private fun money(value: Double) = NumberFormat.getCurrencyInstance(VI).format(value)
    private fun percent(part: Int, total: Int) = if (total == 0) "0,00%" else String.format(VI, "%.2f%%", part * 100.0 / total)
    private companion object {
        val VI: Locale = Locale.forLanguageTag("vi-VN")
        val PHYSICAL_STATUSES = setOf("IN_STOCK", "ALLOCATED", "DISPLAY", "DEFECTIVE", "DEFECT", "RETURNED")
    }
}
