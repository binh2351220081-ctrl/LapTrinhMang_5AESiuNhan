package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey
    val productCode: String,
    val name: String,
    val brand: String,
    val retailPrice: Double
)

