package com.example.chronovaultwms.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update

/**
 * Data Access Object cho Đơn vị / Chi nhánh tiếp nhận hàng xuất kho
 * Phụ trách: Phân hệ 3 (TV3 - Tô Đức Thảo)
 */
@Dao
interface DealerDao {
    @Query("SELECT * FROM dealers ORDER BY name ASC")
    suspend fun getAllDealers(): List<DealerEntity>

    @Query("SELECT * FROM dealers WHERE dealerId = :id LIMIT 1")
    suspend fun getDealerById(id: String): DealerEntity?

    @Query("SELECT COUNT(*) FROM dealers")
    suspend fun countDealers(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(dealers: List<DealerEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(dealer: DealerEntity)

    @Update
    suspend fun update(dealer: DealerEntity)

    @Query("UPDATE dealers SET currentDebt = :newDebt WHERE dealerId = :dealerId")
    suspend fun updateDebt(dealerId: String, newDebt: Double)

    @Query("SELECT * FROM dealers WHERE taxCode = :taxCode AND dealerId != :excludingId LIMIT 1")
    suspend fun findTaxCodeOwner(taxCode: String, excludingId: String): DealerEntity?
}

