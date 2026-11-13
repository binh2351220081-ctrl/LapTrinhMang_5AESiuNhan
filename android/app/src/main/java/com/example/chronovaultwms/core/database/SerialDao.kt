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
    
    @Query("SELECT * FROM serials WHERE qualityStatus = :status")
    suspend fun getSerialsByQuality(status: String): List<SerialEntity>

    @Query("SELECT * FROM serials WHERE locationBin = :bin")
    suspend fun getSerialsByBin(bin: String): List<SerialEntity>

    @Query("UPDATE serials SET qualityStatus = :newQuality WHERE serialNumber = :serial")
    suspend fun updateSerialQuality(serial: String, newQuality: String)

    @Query("UPDATE serials SET locationBin = :newBin WHERE serialNumber = :serial")
    suspend fun updateSerialBin(serial: String, newBin: String)
}

