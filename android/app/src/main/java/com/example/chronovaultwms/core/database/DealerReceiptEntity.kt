package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Thực thể Phiếu Xác Nhận Bàn Giao & Giải Phóng Bảo Lãnh Tài Sản
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 * Quản lý giải phóng trách nhiệm tài sản lưu giữ và khôi phục hạn mức điều phối
 */
@Entity(tableName = "dealer_receipts")
data class DealerReceiptEntity(
    @PrimaryKey
    val receiptId: String,            // Mã phiếu giải phóng (VD: PT-2026-001)
    val dealerId: String,             // Mã đơn vị tiếp nhận hoàn tất đối soát
    val dealerName: String,           // Tên đơn vị tiếp nhận
    val amount: Double,               // Giá trị tài sản được giải phóng (VNĐ)
    val paymentMethod: String,        // CHUYEN_KHOAN, TIEN_MAT
    val referenceDoc: String,         // Chứng từ biên bản bàn giao / UNC ngân hàng
    val date: String,                 // Ngày giờ xác nhận bàn giao
    val note: String = ""             // Ghi chú giải phóng bảo lãnh
)

