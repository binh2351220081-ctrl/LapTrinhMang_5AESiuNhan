package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.ColumnInfo
import androidx.room.PrimaryKey

@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey
    val productCode: String,        // Mã SKU (VD: RLX-SUB-126610LN)
    val name: String,               // Tên đầy đủ (VD: Rolex Submariner Date 41mm)
    val brand: String,              // Thương hiệu (Rolex, Omega, Patek Philippe...)
    val category: String,           // Phân loại (Diver, Chronograph, Dress, Pilot...)
    val wholesalePrice: Double,     // Giá trị khai báo / Định giá xuất kho lưu ký (VNĐ)
    val retailPrice: Double,        // Giá niêm yết hãng (VNĐ)
    val stockQuantity: Int,         // Số lượng tồn kho (Chiếc)
    val caseDiameter: String,       // Đường kính mặt (VD: 41mm)
    val dialColor: String,          // Màu mặt số (VD: Đen tuyền, Xanh sunburst)
    val movementType: String,       // Bộ máy (VD: Automatic Calibre 3235)
    val waterResistance: String,    // Độ chống nước (VD: 300m / 30ATM)
    val status: String = "ACTIVE",  // Trạng thái (ACTIVE, LOW_STOCK, DISCONTINUED)
    @ColumnInfo(defaultValue = "10") val conversionRate: Int = 10,
    @ColumnInfo(defaultValue = "1") val minDispatchQuantity: Int = 1
)
