package com.example.chronovaultwms.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update

/**
 * Data Access Object cho Đơn Hàng Bán Sỉ B2B
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 */
@Dao
interface OutboundOrderDao {
    @Query("SELECT * FROM outbound_orders ORDER BY createdDate DESC")
    suspend fun getAllOrders(): List<OutboundOrderEntity>

    @Query("SELECT * FROM outbound_orders WHERE orderCode = :code LIMIT 1")
    suspend fun getOrderByCode(code: String): OutboundOrderEntity?

    @Query("SELECT * FROM outbound_orders WHERE status = :status ORDER BY createdDate DESC")
    suspend fun getOrdersByStatus(status: String): List<OutboundOrderEntity>

    @Query("SELECT COUNT(*) FROM outbound_orders")
    suspend fun countOrders(): Int

    @Query("SELECT COALESCE(SUM(convertedQuantity), 0) FROM outbound_orders WHERE productCode = :productCode AND status = 'RESERVED'")
    suspend fun getReservedQuantity(productCode: String): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(orders: List<OutboundOrderEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(order: OutboundOrderEntity)

    @Update
    suspend fun update(order: OutboundOrderEntity)

    @Query("UPDATE outbound_orders SET status = :status, dispatchedSerials = :serials WHERE orderCode = :orderCode")
    suspend fun markCompleted(orderCode: String, serials: String, status: String = "COMPLETED")
}

