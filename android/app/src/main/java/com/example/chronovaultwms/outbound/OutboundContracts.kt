package com.example.chronovaultwms.outbound

import com.example.chronovaultwms.core.database.DealerEntity
import com.example.chronovaultwms.core.database.OutboundLineEntity
import com.example.chronovaultwms.core.database.OutboundOrderEntity
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.core.database.SerialEntity

data class OutboundActor(val name: String, val role: String)

data class OutboundLineRequest(val productCode: String, val isBox: Boolean, val quantity: Int)

data class OutboundState(
    val dealers: List<DealerEntity>,
    val products: List<ProductEntity>,
    val orders: List<OutboundOrderEntity>,
    val serials: List<SerialEntity>
)

data class OutboundPick(
    val serialNumber: String,
    val productCode: String,
    val productName: String,
    val currentLocation: String,
    val importDate: String,
    val unitCost: Double,
    val lotNumber: Int
)

data class OutboundDocument(
    val code: String,
    val orderCode: String,
    val dealerName: String,
    val address: String,
    val createdAt: String,
    val createdBy: String,
    val approvedBy: String,
    val dispatchedBy: String,
    val carrier: String,
    val trackingNumber: String,
    val note: String,
    val serials: List<OutboundPick>,
    val lines: List<OutboundLineEntity>
)

/** Pure invariants also used by unit tests; no Android/session fallback grants mutation access. */
object WarehouseOutboundRules {
    fun requireOperator(actor: OutboundActor) {
        require(actor.name.isNotBlank() && actor.role in setOf("OPERATIONS_STAFF", "WAREHOUSE_MANAGER", "STORE_OWNER")) { "Bạn không có quyền tác nghiệp xuất kho." }
    }
    fun requireManager(actor: OutboundActor) {
        require(actor.name.isNotBlank() && actor.role in setOf("WAREHOUSE_MANAGER", "STORE_OWNER")) { "Thao tác cần Thủ kho hoặc Chủ kho xác nhận." }
    }
    fun convertQuantity(quantity: Int, isBox: Boolean, conversionRate: Int): Int {
        require(quantity > 0 && conversionRate > 0) { "Số lượng và hệ số quy đổi phải lớn hơn 0." }
        return try { if (isBox) Math.multiplyExact(quantity, conversionRate) else quantity }
        catch (_: ArithmeticException) { throw IllegalArgumentException("Số lượng quy đổi vượt giới hạn cho phép.") }
    }
    fun requireExactScanSet(required: List<String>, scanned: List<String>) {
        require(required.isNotEmpty()) { "Picking List chưa có dữ liệu." }
        require(scanned.distinct().size == scanned.size) { "Danh sách quét chứa Serial trùng lặp." }
        require(scanned.size == required.size && scanned.toSet() == required.toSet()) { "Phải quét đúng và đủ 100% Serial trong Picking List." }
    }
}
