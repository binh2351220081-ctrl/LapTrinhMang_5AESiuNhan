package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Thực thể Đơn Bán Sỉ & Phân Phối Outbound B2B
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 * Cơ chế: Khóa giữ chỗ (Inventory Reservation) & Quét Serial xuất kho
 */
@Entity(tableName = "outbound_orders")
data class OutboundOrderEntity(
    @PrimaryKey
    val orderCode: String,            // Mã đơn sỉ (VD: DS-2026-001)
    val dealerId: String,             // Mã đại lý nhận hàng
    val dealerName: String,           // Tên chuỗi đại lý
    val productCode: String,          // Mã SKU đồng hồ đặt sỉ
    val productName: String,          // Tên mẫu mã đồng hồ
    val unit: String,                 // ĐVT đặt: PIECE (Chiếc) hoặc BOX (Thùng)
    val quantity: Int,                // Số lượng đặt theo ĐVT
    val convertedQuantity: Int,       // Số lượng quy đổi ra chiếc lẻ
    val unitPrice: Double,            // Đơn giá bán sỉ niêm yết
    val discountPercent: Double,      // Tỷ lệ chiết khấu theo hạng đại lý
    val totalAmount: Double,          // Tổng giá trị đơn sau chiết khấu
    val depositAmount: Double,        // Số tiền đặt cọc thu trước
    val remainingDebt: Double,        // Công nợ sỉ còn lại
    val status: String = "RESERVED",  // PENDING, RESERVED, COMPLETED, CANCELLED
    val createdDate: String,          // Ngày lập đơn (VD: 10/11/2026 14:30)
    val dispatchedSerials: String = ""// Danh sách Serial đã quét xuất kho (ngăn cách bởi dấu phẩy)
)

