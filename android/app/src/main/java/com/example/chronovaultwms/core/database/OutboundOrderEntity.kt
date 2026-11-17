package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.ColumnInfo
import androidx.room.PrimaryKey

/**
 * Thực thể Lệnh Điều Phối Xuất Kho Outbound
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 * Cơ chế: Khóa giữ chỗ tồn kho (Inventory Reservation) & Quét Serial đóng kiện xuất kho
 */
@Entity(tableName = "outbound_orders")
data class OutboundOrderEntity(
    @PrimaryKey
    val orderCode: String,            // Mã lệnh điều phối xuất kho (VD: DS-2026-001)
    val dealerId: String,             // Mã đơn vị tiếp nhận hàng
    val dealerName: String,           // Tên đơn vị / chi nhánh tiếp nhận
    val productCode: String,          // Mã SKU đồng hồ yêu cầu xuất
    val productName: String,          // Tên mẫu mã đồng hồ
    val unit: String,                 // ĐVT xuất: PIECE (Chiếc) hoặc BOX (Thùng)
    val quantity: Int,                // Số lượng yêu cầu theo ĐVT
    val convertedQuantity: Int,       // Số lượng quy đổi ra chiếc lẻ để khóa giữ chỗ
    val unitPrice: Double,            // Giá trị định giá bảo hiểm lưu kho / chiếc
    val discountPercent: Double,      // Hệ số phân bổ điều chuyển theo hạng đơn vị nhận
    val totalAmount: Double,          // Tổng giá trị định giá tài sản lô hàng xuất
    val depositAmount: Double,        // Giá trị ký quỹ bảo lãnh trách nhiệm (nếu có)
    val remainingDebt: Double,        // Giá trị trách nhiệm bảo lãnh phát sinh
    val status: String = "RESERVED",  // PENDING, RESERVED, COMPLETED, CANCELLED
    val createdDate: String,          // Ngày giờ lập lệnh xuất (VD: 10/11/2026 14:10)
    val dispatchedSerials: String = "", // Tương thích dữ liệu v5; bảng allocations lưu từng Serial
    @ColumnInfo(defaultValue = "''") val note: String = "",
    @ColumnInfo(defaultValue = "''") val createdBy: String = "",
    @ColumnInfo(defaultValue = "''") val approvedBy: String = "",
    @ColumnInfo(defaultValue = "''") val approvedAt: String = "",
    @ColumnInfo(defaultValue = "''") val dispatchedBy: String = "",
    @ColumnInfo(defaultValue = "''") val dispatchedAt: String = "",
    @ColumnInfo(defaultValue = "''") val cancelReason: String = ""
)

