package com.example.chronovaultwms.dashboard.model

import java.time.LocalDate

data class DashboardKpis(
    val inventoryAssetValue: Double,
    val wholesaleRevenue: Double,
    val newWholesaleOrders: Int,
    val availableStock: Int,
    val returnRatePercent: Double
)

data class MonthlyRevenue(val monthLabel: String, val revenue: Double)
data class CostSlice(val label: String, val amount: Double)
data class TopProduct(val sku: String, val name: String, val quantitySold: Int, val revenue: Double)
data class AuditActivity(val timeLabel: String, val title: String, val detail: String, val sourceModule: String)

data class DashboardSnapshot(
    val periodLabel: String,
    val kpis: DashboardKpis,
    val monthlyRevenue: List<MonthlyRevenue>,
    val costStructure: List<CostSlice>,
    val topProducts: List<TopProduct>,
    val recentActivities: List<AuditActivity>
)

data class DateRange(val from: LocalDate, val to: LocalDate) {
    init { require(!to.isBefore(from)) { "Ngày kết thúc phải bằng hoặc sau ngày bắt đầu" } }
}

enum class ReportType(val displayName: String) {
    INBOUND("1. Báo cáo nhập hàng"),
    OUTBOUND("2. Xuất kho theo đơn vị nhận"),
    DISPATCH_STRUCTURE("3. Cơ cấu xuất hàng"),
    RETURNS_QUALITY("4. Đổi trả & chất lượng bộ máy"),
    DEAD_STOCK("5. Hàng chậm luân chuyển (Dead Stock)"),
    GROSS_PROFIT("6. Giá trị hàng xuất theo Serial"),
    TWO_WAY_DEBT("7. Đối soát bàn giao và hoàn trả"),
    CASHFLOW("8. Sổ biến động kho"),
    AUDIT_LOG("9. Nhật ký kiểm toán toàn hệ thống")
}

data class ReportRow(val values: List<String>)

data class ReportTable(
    val type: ReportType,
    val title: String,
    val period: DateRange,
    val headers: List<String>,
    val rows: List<ReportRow>,
    val summary: String
)
