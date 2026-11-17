package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.ColumnInfo
import androidx.room.PrimaryKey

/**
 * Thực thể Đơn vị / Chi nhánh tiếp nhận hàng xuất kho
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 * Quản lý hạn mức bảo lãnh trách nhiệm tài sản (Asset Custody Limit) và giá trị hàng hóa đang lưu giữ
 */
@Entity(tableName = "dealers")
data class DealerEntity(
    @PrimaryKey
    val dealerId: String,          // Mã đơn vị tiếp nhận (VD: DL-GALLE, DL-HAITRIEU)
    val name: String,              // Tên chi nhánh / đơn vị tiếp nhận (VD: Galle Watch Việt Nam)
    val tier: String,              // Phân hạng ưu tiên điều phối (VIP, SILVER, BRONZE)
    val discountPercent: Double,   // Hệ số phân bổ ưu tiên điều chuyển (VD: 0.25 = 25%)
    val creditLimit: Double,       // Hạn mức bảo lãnh tài sản tối đa (VNĐ)
    val currentDebt: Double,       // Giá trị tài sản đang giữ chưa hoàn tất bàn giao (VNĐ)
    val phone: String,             // Số điện thoại liên hệ kho nhận
    val address: String,           // Địa chỉ kho nhận hàng thực tế
    val taxCode: String,           // Mã số doanh nghiệp / Mã chi nhánh
    val status: String = "ACTIVE", // ACTIVE, LOCKED, SUSPENDED
    @ColumnInfo(defaultValue = "''") val representative: String = "",
    @ColumnInfo(defaultValue = "''") val email: String = ""
)

