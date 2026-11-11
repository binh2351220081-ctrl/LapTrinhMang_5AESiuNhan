package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Thực thể Đại lý B2B (B2B Wholesale Dealer)
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 * Quản lý hạn mức tín dụng (Credit Limit) và dư nợ phân phối sỉ
 */
@Entity(tableName = "dealers")
data class DealerEntity(
    @PrimaryKey
    val dealerId: String,          // Mã đại lý (VD: DL-GALLE, DL-HAITRIEU)
    val name: String,              // Tên chuỗi đại lý (VD: Galle Watch Việt Nam)
    val tier: String,              // Phân hạng (VIP, SILVER, BRONZE)
    val discountPercent: Double,   // Tỷ lệ chiết khấu sỉ (VD: 0.30 = 30%)
    val creditLimit: Double,       // Hạn mức tín dụng tối đa (VNĐ)
    val currentDebt: Double,       // Dư nợ hiện tại (VNĐ)
    val phone: String,             // Số điện thoại liên hệ
    val address: String,           // Địa chỉ kho giao nhận
    val taxCode: String,           // Mã số thuế doanh nghiệp
    val status: String = "ACTIVE"  // ACTIVE, LOCKED, SUSPENDED
)

