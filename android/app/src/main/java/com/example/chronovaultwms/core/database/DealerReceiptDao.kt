package com.example.chronovaultwms.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

/**
 * Data Access Object cho Phiếu Thu Tiền Sỉ
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 */
@Dao
interface DealerReceiptDao {
    @Query("SELECT * FROM dealer_receipts ORDER BY date DESC")
    suspend fun getAllReceipts(): List<DealerReceiptEntity>

    @Query("SELECT * FROM dealer_receipts WHERE dealerId = :dealerId ORDER BY date DESC")
    suspend fun getReceiptsByDealer(dealerId: String): List<DealerReceiptEntity>

    @Query("SELECT COUNT(*) FROM dealer_receipts")
    suspend fun countReceipts(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(receipt: DealerReceiptEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(receipts: List<DealerReceiptEntity>)
}

