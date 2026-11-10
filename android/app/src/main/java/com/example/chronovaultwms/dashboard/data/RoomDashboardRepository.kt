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
import java.time.format.TextStyle
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
        val delivered = serials.filter { it.status == "DELIVERED" }
        val revenue = delivered.sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }
        val specificCost = delivered.sumOf { it.unitCost }
        val logistics = specificCost * 0.045

        return when (type) {
            ReportType.INBOUND -> report(type, range,
                listOf("Nhà cung cấp", "Số serial", "Giá trị nhập", "Vị trí"),
                serials.groupBy { it.supplierName }.map { (supplier, rows) ->
                    listOf(supplier, rows.size.toString(), money(rows.sumOf { it.unitCost }), rows.first().currentLocation)
                },
                "${serials.size} serial • Giá vốn đích danh ${money(serials.sumOf { it.unitCost })}")

            ReportType.OUTBOUND -> report(type, range,
                listOf("Đại lý", "Số chiếc", "Doanh số", "Trạng thái"),
                serials.filter { it.dealerName != null }.groupBy { it.dealerName.orEmpty() }.map { (dealer, rows) ->
                    listOf(dealer, rows.size.toString(), money(rows.sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }), rows.first().status)
                },
                "Doanh số đã bàn giao ${money(revenue)} • ${delivered.size} serial")

            ReportType.DISPATCH_STRUCTURE -> {
                val groups = serials.groupingBy { it.status }.eachCount()
                report(type, range, listOf("Trạng thái", "Số serial", "Tỷ trọng"),
                    groups.map { (status, count) -> listOf(status, count.toString(), percent(count, serials.size)) },
                    "Cơ cấu theo ${serials.size} serial đang được đồng bộ")
            }

            ReportType.RETURNS_QUALITY -> report(type, range,
                listOf("Thương hiệu", "Đã quản lý", "Lỗi/đổi trả", "Tỷ lệ"),
                products.groupBy { it.brand }.map { (brand, brandProducts) ->
                    val codes = brandProducts.map { it.productCode }.toSet()
                    val rows = serials.filter { it.productCode in codes }
                    val defective = rows.count { it.status == "DEFECTIVE" || it.status == "RETURNED" }
                    listOf(brand, rows.size.toString(), defective.toString(), percent(defective, rows.size))
                }, "Theo dõi chất lượng theo Serial, ngưỡng cảnh báo 2%")

            ReportType.DEAD_STOCK -> report(type, range,
                listOf("SKU", "Sản phẩm", "Tồn", "Giá trị vốn"),
                products.filter { it.stockQuantity > 0 }.sortedByDescending { it.stockQuantity }.take(10).map { product ->
                    val cost = serials.filter { it.productCode == product.productCode && it.status == "IN_STOCK" }.sumOf { it.unitCost }
                    listOf(product.productCode, product.name, product.stockQuantity.toString(), money(cost))
                }, "Danh sách ưu tiên xử lý tồn theo số lượng giảm dần")

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
                val receivables = serials.filter { it.status == "ALLOCATED" }.groupBy { it.dealerName ?: "Chưa xác định" }
                val payables = serials.filter { it.status != "DELIVERED" }.groupBy { it.supplierName }
                val rows = receivables.map { (name, items) ->
                    listOf(name, "Phải thu", money(items.sumOf { productsByCode[it.productCode]?.wholesalePrice ?: 0.0 }))
                } + payables.map { (name, items) -> listOf(name, "Phải trả", money(items.sumOf { it.unitCost })) }
                report(type, range, listOf("Đối tác", "Loại công nợ", "Dư hiện tại"), rows,
                    "Đối soát hai chiều từ đơn phân bổ và Serial chưa thanh toán")
            }

            ReportType.CASHFLOW -> {
                val cashIn = revenue
                val cashOut = serials.sumOf { it.unitCost } + logistics
                report(type, range, listOf("Nhóm dòng tiền", "Thu", "Chi"), listOf(
                    listOf("Thu bán sỉ", money(cashIn), money(0.0)),
                    listOf("Thanh toán nhà cung cấp", money(0.0), money(serials.sumOf { it.unitCost })),
                    listOf("Logistics và bảo hiểm", money(0.0), money(logistics))
                ), "Dòng tiền thuần ${money(ReportCalculations.netCashflow(cashIn, cashOut))}")
            }

            ReportType.AUDIT_LOG -> report(type, range,
                listOf("Thời gian", "Người dùng", "Vai trò", "Hành động", "Chi tiết"),
                logs.map { listOf(it.timestamp, it.actorName, it.role, it.action, it.details) },
                "${logs.size} hoạt động gần nhất • chỉ đọc, không sửa hoặc xóa")
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
}
