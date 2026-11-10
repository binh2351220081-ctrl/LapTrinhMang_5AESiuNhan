package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Thực thể Serial Number định danh từng chiếc đồng hồ (100% Serialization)
 * Thuộc Phân hệ 1: Quản trị Hàng hóa & Hệ thống (TV1 - Phan Bá Hải Bình)
 * Nguyên lý: Specific Identification (Giá vốn đích danh) & Vòng đời vòng lặp
 */
@Entity(tableName = "serials")
data class SerialEntity(
    @PrimaryKey
    val serialNumber: String,          // Mã Serial duy nhất (VD: RLX-SUB-2026-001)
    val productCode: String,           // Mã SKU liên kết (VD: RLX-SUB-126610LN)
    val status: String,                // IN_STOCK, ALLOCATED, DISPATCHED, DELIVERED, DEFECTIVE
    val currentLocation: String,       // Vị trí vật lý (VD: Két Sắt VIP-01, Kệ K1-A02)
    val importDate: String,            // Ngày nhập kho (VD: 15/10/2026 09:30)
    val unitCost: Double,              // Giá vốn đích danh gồm thuế & bảo hiểm (VNĐ)
    val supplierName: String,          // Nhà cung ứng (VD: Rolex Geneva SA - Thụy Sĩ)
    val dealerName: String? = null,    // Đại lý nhận sỉ (nếu đã phân bổ hoặc xuất)
    val qcNotes: String = ""           // Kết quả kiểm định QC (VD: Chuẩn COSC +1s/ngày)
)

