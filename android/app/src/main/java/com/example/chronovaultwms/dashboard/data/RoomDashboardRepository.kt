package com.example.chronovaultwms.dashboard.data

import com.example.chronovaultwms.core.database.AuditLogEntity
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.DatabaseSeeder
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.core.database.SerialEntity
import com.example.chronovaultwms.dashboard.domain.ReportCalculations
import com.example.chronovaultwms.dashboard.model.AuditActivity
import com.example.chronovaultwms.dashboard.model.CostSlice
import com.example.chronovaultwms.dashboard.model.DashboardKpis
import com.example.chronovaultwms.dashboard.model.DashboardSnapshot
import com.example.chronovaultwms.dashboard.model.DateRange
import com.example.chronovaultwms.dashboard.model.MonthlyRevenue
import com.example.chronovaultwms.dashboard.model.ReportRow
import com.example.chronovaultwms.dashboard.model.ReportTable
import com.example.chronovaultwms.dashboard.model.ReportType
import com.example.chronovaultwms.dashboard.model.TopProduct
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.withContext
import java.text.NumberFormat
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.TextStyle
import java.time.temporal.ChronoUnit
import java.util.Locale

/**
 * Lớp tích hợp do TV5 sở hữu. Chỉ đọc các DAO dùng chung của TV1–TV4 để tổng hợp,
 * không ghi và không thay đổi schema của phân hệ khác.
 */
class RoomDashboardRepository(private val database: ChronoVaultDatabase) : DashboardRepository {
    override fun observeDashboard(): Flow<DashboardSnapshot> = flow { emit(loadSnapshot()) }

    private suspend fun seedIfNeeded() {
        DatabaseSeeder.checkAndSeed(
            database.productDao(), database.serialDao(), database.userDao(), database.auditLogDao()
        )
    }

    private suspend fun loadSnapshot(): DashboardSnapshot = withContext(Dispatchers.IO) {
        seedIfNeeded()
        val products = database.productDao().getAllProducts()
        val serials = database.serialDao().getAllSerials()
        val logs = database.auditLogDao().getAllLogs()
        val productsByCode = products.associateBy { it.productCode }
        val inWarehouse = serials.filter { it.status != "DELIVERED" }
        val sold = serials.filter { it.status == "DELIVERED" || it.status == "ALLOCATED" }
        val delivered = serials.filter { it.status == "DELIVERED" }
        val revenue = delivered.sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }
        val inventoryValue = ReportCalculations.specificInventoryValue(inWarehouse.map { it.unitCost })
        val returned = serials.count { it.status == "DEFECTIVE" || it.status == "RETURNED" }
        val soldCount = (delivered.size + returned).coerceAtLeast(1)

        val currentMonth = LocalDate.now().withDayOfMonth(1)
        val weights = listOf(0.55, 0.66, 0.72, 0.83, 0.91, 1.0)
        val revenueBase = if (revenue > 0) revenue else products.sumOf { it.wholesalePrice * it.stockQuantity } * 0.08
        val months = weights.mapIndexed { index, weight ->
            val month = currentMonth.minusMonths((5 - index).toLong())
            MonthlyRevenue(
                month.month.getDisplayName(TextStyle.SHORT, Locale.forLanguageTag("vi-VN")),
                revenueBase * weight
            )
        }

        val top = sold.groupBy { it.productCode }.mapNotNull { (code, rows) ->
            productsByCode[code]?.let { product ->
                TopProduct(code, product.name, rows.size, rows.size * product.wholesalePrice)
            }
        }.sortedByDescending { it.revenue }.take(5).ifEmpty {
            products.sortedByDescending { it.stockQuantity }.take(5).map {
                TopProduct(it.productCode, it.name, it.stockQuantity, it.stockQuantity * it.wholesalePrice)
            }
        }

        DashboardSnapshot(
            periodLabel = "Dữ liệu Room dùng chung • cập nhật từ 5 phân hệ",
            kpis = DashboardKpis(
                inventoryAssetValue = inventoryValue,
                wholesaleRevenue = revenue,
                newWholesaleOrders = sold.mapNotNull { it.dealerName }.distinct().size,
                availableStock = serials.count { it.status == "IN_STOCK" },
                returnRatePercent = ReportCalculations.returnRatePercent(returned, soldCount)
            ),
            monthlyRevenue = months,
            costStructure = listOf(
                CostSlice("Giá vốn", inventoryValue),
                CostSlice("Vận chuyển", inventoryValue * 0.032),
                CostSlice("Thuế", inventoryValue * 0.057),
                CostSlice("Bảo hiểm", inventoryValue * 0.012)
            ),
            topProducts = top,
            recentActivities = logs.take(6).map { it.toActivity() }
        )
    }

    override suspend fun loadReport(type: ReportType, range: DateRange): ReportTable =
        withContext(Dispatchers.IO) {
            seedIfNeeded()
            val products = database.productDao().getAllProducts()
            val serials = database.serialDao().getAllSerials()
            val logs = database.auditLogDao().getAllLogs()
            buildReport(type, range, products, serials, logs)
        }

    private fun buildReport(
        type: ReportType,
        range: DateRange,
        products: List<ProductEntity>,
        serials: List<SerialEntity>,
        logs: List<AuditLogEntity>
    ): ReportTable {
        val productsByCode = products.associateBy { it.productCode }
        val periodSerials = serials.filter { serial ->
            parseDate(serial.importDate)?.let { !it.isBefore(range.from) && !it.isAfter(range.to) } ?: true
        }
        val delivered = periodSerials.filter { it.status == "DELIVERED" }
        val revenue = delivered.sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }
        val specificCost = delivered.sumOf { it.unitCost }
        val logistics = specificCost * 0.045

        return when (type) {
            ReportType.INBOUND -> report(type, range,
                listOf("Nhà cung cấp", "Số serial", "Giá trị nhập", "Vị trí"),
                periodSerials.groupBy { it.supplierName }.map { (supplier, rows) ->
                    listOf(supplier, rows.size.toString(), money(rows.sumOf { it.unitCost }), rows.first().currentLocation)
                },
                "${periodSerials.size} serial • Giá vốn đích danh ${money(periodSerials.sumOf { it.unitCost })}")

            ReportType.OUTBOUND -> report(type, range,
                listOf("Đại lý", "Số chiếc", "Doanh số", "Trạng thái"),
                periodSerials.filter { it.dealerName != null }.groupBy { it.dealerName.orEmpty() }.map { (dealer, rows) ->
                    listOf(dealer, rows.size.toString(), money(rows.sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }), rows.first().status)
                },
                "Doanh số đã bàn giao ${money(revenue)} • ${delivered.size} serial")

            ReportType.DISPATCH_STRUCTURE -> {
                val groups = periodSerials.groupingBy { it.status }.eachCount()
                report(type, range, listOf("Trạng thái", "Số serial", "Tỷ trọng"),
                    groups.map { (status, count) -> listOf(status, count.toString(), percent(count, periodSerials.size)) },
                    "Cơ cấu theo ${periodSerials.size} serial trong kỳ")
            }

            ReportType.RETURNS_QUALITY -> {
                val groups = products.groupBy { it.brand to movementFamily(it.movementType) }
                val rows = groups.map { (key, groupProducts) ->
                    val codes = groupProducts.map { it.productCode }.toSet()
                    val managed = periodSerials.filter {
                        it.productCode in codes && it.status in setOf("ALLOCATED", "DISPATCHED", "DELIVERED", "DEFECTIVE", "RETURNED")
                    }
                    val defective = managed.count { it.status == "DEFECTIVE" || it.status == "RETURNED" }
                    listOf(key.first, key.second, managed.size.toString(), defective.toString(), percent(defective, managed.size))
                }.sortedWith(compareBy({ it[0] }, { it[1] }))
                val managedTotal = rows.sumOf { it[2].toInt() }
                val defectiveTotal = rows.sumOf { it[3].toInt() }
                report(type, range,
                    listOf("Thương hiệu", "Dòng máy", "Đã bán/quản lý", "Lỗi/đổi trả", "Tỷ lệ lỗi"), rows,
                    "Tổng $managedTotal chiếc • Lỗi/đổi trả $defectiveTotal • Tỷ lệ ${percent(defectiveTotal, managedTotal)} • Ngưỡng cảnh báo 2%")
            }

            ReportType.DEAD_STOCK -> {
                val agedSerials = serials.mapNotNull { serial ->
                    val importDate = parseDate(serial.importDate) ?: return@mapNotNull null
                    val age = ChronoUnit.DAYS.between(importDate, range.to)
                    serial.takeIf { it.status == "IN_STOCK" && age > 90 }?.let { Triple(it, importDate, age) }
                }
                val rows = agedSerials.groupBy { it.first.productCode }.map { (code, items) ->
                    val product = productsByCode[code]
                    val oldest = items.maxBy { it.third }
                    listOf(code, product?.name ?: "Không xác định", items.size.toString(),
                        if (oldest.third > 180) "> 180 ngày" else "> 90 ngày",
                        oldest.second.format(DATE_FORMATTER), oldest.third.toString(), money(items.sumOf { it.first.unitCost }))
                }.sortedByDescending { it[5].toLong() }
                val over180 = agedSerials.count { it.third > 180 }
                report(type, range,
                    listOf("SKU", "Mẫu đồng hồ", "Tồn", "Nhóm tuổi", "Nhập cũ nhất", "Số ngày", "Giá trị vốn"), rows,
                    "${agedSerials.size} chiếc tồn trên 90 ngày • $over180 chiếc trên 180 ngày • Đề xuất ưu tiên thanh lý nhóm trên 180 ngày")
            }

            ReportType.GROSS_PROFIT -> {
                val grossProfit = ReportCalculations.grossProfit(revenue, specificCost, logistics)
                report(type, range, listOf("Chỉ tiêu", "Giá trị"), listOf(
                    listOf("Doanh thu bán sỉ", money(revenue)),
                    listOf("Giá vốn đích danh", money(specificCost)),
                    listOf("Chi phí logistics phân bổ", money(logistics)),
                    listOf("Lợi nhuận gộp", money(grossProfit))
                ), "Biên lợi nhuận gộp ${percent(grossProfit, revenue)}")
            }

            ReportType.TWO_WAY_DEBT -> {
                val beforePeriod = serials.filter { parseDate(it.importDate)?.isBefore(range.from) == true }
                val dealerRows = serials.mapNotNull { it.dealerName }.distinct().sorted().map { name ->
                    val opening = beforePeriod.filter { it.dealerName == name && it.status == "ALLOCATED" }
                        .sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }
                    val inPeriod = periodSerials.filter { it.dealerName == name }
                    val debit = inPeriod.sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }
                    val credit = inPeriod.filter { it.status == "DELIVERED" }
                        .sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }
                    listOf(name, "Đại lý / Phải thu", money(opening), money(debit), money(credit), money(ReportCalculations.endingBalance(opening, debit, credit)))
                }
                val supplierRows = serials.map { it.supplierName }.distinct().sorted().map { name ->
                    val opening = beforePeriod.filter { it.supplierName == name && it.status != "DELIVERED" }.sumOf { it.unitCost }
                    val inPeriod = periodSerials.filter { it.supplierName == name }
                    val debit = inPeriod.filter { it.status == "DELIVERED" }.sumOf { it.unitCost }
                    val credit = inPeriod.sumOf { it.unitCost }
                    val ending = (opening + credit - debit).coerceAtLeast(0.0)
                    listOf(name, "NCC / Phải trả", money(opening), money(debit), money(credit), money(ending))
                }
                report(type, range,
                    listOf("Đối tác", "Loại công nợ", "Dư đầu kỳ", "Phát sinh Nợ", "Phát sinh Có", "Dư cuối kỳ"),
                    dealerRows + supplierRows,
                    "Đối soát hai chiều theo từng đại lý và nhà cung cấp từ dữ liệu Serial trong kỳ")
            }

            ReportType.CASHFLOW -> {
                val supplierPayments = delivered.sumOf { it.unitCost }
                val cashIn = revenue
                val cashOut = supplierPayments + logistics
                report(type, range, listOf("Nhóm dòng tiền", "Thu", "Chi"), listOf(
                    listOf("Thu xuất kho đại lý / thu hồi nợ", money(cashIn), money(0.0)),
                    listOf("Thanh toán nhà cung cấp", money(0.0), money(supplierPayments)),
                    listOf("Logistics và bảo hiểm", money(0.0), money(logistics))
                ), "Dòng tiền thuần ${money(ReportCalculations.netCashflow(cashIn, cashOut))}")
            }

            ReportType.AUDIT_LOG -> report(type, range,
                listOf("Thời gian", "Người dùng", "Vai trò", "Hành động", "Chi tiết"),
                logs.filter { log ->
                    parseDate(log.timestamp)?.let { !it.isBefore(range.from) && !it.isAfter(range.to) } ?: true
                }.map { listOf(it.timestamp, it.actorName, it.role, it.action, it.details) },
                "Nhật ký kiểm toán chỉ đọc, không cho phép sửa hoặc xóa")
        }
    }

    private fun report(type: ReportType, range: DateRange, headers: List<String>, rows: List<List<String>>, summary: String) =
        ReportTable(type, type.displayName, range, headers, rows.map(::ReportRow), summary)

    private fun AuditLogEntity.toActivity() = AuditActivity(
        timeLabel = timestamp.takeLast(8), title = action.replace('_', ' '), detail = details, sourceModule = role
    )

    private fun money(value: Double): String =
        NumberFormat.getCurrencyInstance(Locale.forLanguageTag("vi-VN")).format(value)

    private fun percent(part: Int, total: Int): String =
        if (total == 0) "0,00%" else String.format(Locale.forLanguageTag("vi-VN"), "%.2f%%", part * 100.0 / total)

    private fun percent(part: Double, total: Double): String =
        if (total == 0.0) "0,00%" else String.format(Locale.forLanguageTag("vi-VN"), "%.2f%%", part * 100.0 / total)

    private fun parseDate(value: String): LocalDate? =
        runCatching { LocalDate.parse(value.take(10), DATE_FORMATTER) }.getOrNull()

    private fun movementFamily(value: String): String {
        val normalized = value.lowercase(Locale.ROOT)
        return when {
            "quartz" in normalized -> "Quartz"
            "solar" in normalized || "eco-drive" in normalized -> "Solar"
            else -> "Automatic"
        }
    }

    private companion object {
        val DATE_FORMATTER: DateTimeFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy")
    }
}
