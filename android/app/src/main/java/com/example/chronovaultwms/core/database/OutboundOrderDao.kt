package com.example.chronovaultwms.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update

/**
 * Data Access Object cho Lệnh Điều Phối Xuất Kho Outbound
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

    @Query("SELECT COUNT(*) FROM serials WHERE productCode = :productCode AND status = 'ALLOCATED' AND allocatedOrderCode IS NOT NULL")
    suspend fun getReservedQuantity(productCode: String): Int

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertAll(orders: List<OutboundOrderEntity>)

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insert(order: OutboundOrderEntity)

    @Update
    suspend fun update(order: OutboundOrderEntity)

    @Query("UPDATE outbound_orders SET status = :status, dispatchedSerials = :serials WHERE orderCode = :orderCode")
    suspend fun markCompleted(orderCode: String, serials: String, status: String = "COMPLETED")
}

