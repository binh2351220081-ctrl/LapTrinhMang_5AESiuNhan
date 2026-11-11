package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Thực thể Phiếu Thu Tiền Sỉ / Thu Nợ Đại Lý (Receipt Voucher)
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 * Quản lý dòng tiền thu hồi nợ B2B và khôi phục hạn mức tín dụng
 */
@Entity(tableName = "dealer_receipts")
data class DealerReceiptEntity(
    @PrimaryKey
    val receiptId: String,            // Mã phiếu thu (VD: PT-2026-001)
    val dealerId: String,             // Mã đại lý thanh toán
    val dealerName: String,           // Tên đại lý
    val amount: Double,               // Số tiền nộp (VNĐ)
    val paymentMethod: String,        // CHUYEN_KHOAN, TIEN_MAT
    val referenceDoc: String,         // Chứng từ ủy nhiệm chi ngân hàng
    val date: String,                 // Ngày giờ nộp tiền
    val note: String = ""             // Ghi chú thu tiền
)

