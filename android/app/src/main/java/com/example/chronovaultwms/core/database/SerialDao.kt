package com.example.chronovaultwms.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update

@Dao
interface SerialDao {
    @Query("SELECT * FROM serials WHERE productCode = :productCode ORDER BY serialNumber ASC")
    suspend fun getSerialsByProduct(productCode: String): List<SerialEntity>

    @Query("SELECT * FROM serials WHERE serialNumber = :serialNumber LIMIT 1")
    suspend fun getSerialByNumber(serialNumber: String): SerialEntity?

    @Query("SELECT * FROM serials ORDER BY importDate DESC")
    suspend fun getAllSerials(): List<SerialEntity>

    @Query("SELECT COUNT(*) FROM serials")
    suspend fun countSerials(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(serials: List<SerialEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(serial: SerialEntity)

    @Update
    suspend fun update(serial: SerialEntity)

    @Query("UPDATE serials SET status = 'ALLOCATED', allocatedOrderCode = :orderCode WHERE serialNumber = :serialNumber AND status = 'IN_STOCK' AND allocatedOrderCode IS NULL")
    suspend fun reserve(serialNumber: String, orderCode: String): Int

    @Query("SELECT COUNT(*) FROM serials WHERE productCode = :productCode AND status IN ('IN_STOCK', 'ALLOCATED')")
    suspend fun newPhysicalCount(productCode: String): Int

    @Query("SELECT COUNT(*) FROM serials WHERE productCode = :productCode AND status IN ('IN_STOCK', 'ALLOCATED', 'DISPLAY', 'DEFECTIVE', 'DEFECT')")
    suspend fun warehouseCount(productCode: String): Int
}

