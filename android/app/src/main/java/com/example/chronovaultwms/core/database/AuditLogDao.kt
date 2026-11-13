package com.example.chronovaultwms.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface AuditLogDao {
    @Query("SELECT * FROM audit_logs ORDER BY logId DESC LIMIT 100")
    suspend fun getAllLogs(): List<AuditLogEntity>

    @Query("SELECT COUNT(*) FROM audit_logs")
    suspend fun countLogs(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLog(log: AuditLogEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(logs: List<AuditLogEntity>)
}

