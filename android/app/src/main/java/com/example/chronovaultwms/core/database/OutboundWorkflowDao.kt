package com.example.chronovaultwms.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface OutboundWorkflowDao {
    @Query("SELECT * FROM outbound_lines WHERE orderCode = :orderCode ORDER BY productCode")
    suspend fun orderLines(orderCode: String): List<OutboundLineEntity>

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertLines(lines: List<OutboundLineEntity>)

    @Query("UPDATE outbound_lines SET unitCost = :unitCost WHERE orderCode = :orderCode AND productCode = :productCode")
    suspend fun updateLineCost(orderCode: String, productCode: String, unitCost: Double)

    @Query("SELECT * FROM outbound_allocations WHERE orderCode = :orderCode ORDER BY productCode, importDate, serialNumber")
    suspend fun allocations(orderCode: String): List<OutboundAllocationEntity>

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertAllocations(allocations: List<OutboundAllocationEntity>)

    @Query("UPDATE outbound_allocations SET scannedAt = :timestamp, scannedBy = :actorName WHERE orderCode = :orderCode AND serialNumber = :serialNumber AND scannedAt = ''")
    suspend fun recordScan(orderCode: String, serialNumber: String, timestamp: String, actorName: String): Int

    @Query("SELECT * FROM outbound_dispatches WHERE orderCode = :orderCode LIMIT 1")
    suspend fun dispatchForOrder(orderCode: String): OutboundDispatchEntity?

    @Query("SELECT * FROM outbound_dispatches WHERE dispatchCode = :dispatchCode LIMIT 1")
    suspend fun dispatchByCode(dispatchCode: String): OutboundDispatchEntity?

    @Query("SELECT * FROM outbound_dispatches ORDER BY dispatchedAt DESC")
    suspend fun allDispatches(): List<OutboundDispatchEntity>

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertDispatch(dispatch: OutboundDispatchEntity)

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertReturn(record: OutboundReturnEntity)

    @Query("SELECT * FROM outbound_returns ORDER BY receivedAt DESC")
    suspend fun allReturns(): List<OutboundReturnEntity>

    @Query("SELECT * FROM outbound_returns WHERE dispatchCode = :dispatchCode AND serialNumber = :serialNumber ORDER BY receivedAt DESC LIMIT 1")
    suspend fun returnForDispatchSerial(dispatchCode: String, serialNumber: String): OutboundReturnEntity?

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertOtherDispatch(record: OutboundOtherDispatchEntity)

    @Query("SELECT * FROM outbound_other_dispatches ORDER BY dispatchedAt DESC")
    suspend fun allOtherDispatches(): List<OutboundOtherDispatchEntity>

    @Query("SELECT * FROM outbound_other_dispatches WHERE serialNumber = :serialNumber ORDER BY dispatchedAt DESC LIMIT 1")
    suspend fun latestOtherForSerial(serialNumber: String): OutboundOtherDispatchEntity?

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertMovement(movement: StockMovementEntity)

    @Query("SELECT * FROM stock_movements ORDER BY timestamp DESC, movementId DESC")
    suspend fun allMovements(): List<StockMovementEntity>

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertSyncEvent(event: OutboundSyncEventEntity)

    @Query("SELECT * FROM outbound_sync_events WHERE syncedAt IS NULL ORDER BY createdAt ASC, eventId ASC LIMIT 100")
    suspend fun pendingEvents(): List<OutboundSyncEventEntity>

    @Query("SELECT COUNT(*) FROM outbound_sync_events WHERE syncedAt IS NULL")
    suspend fun pendingCount(): Int

    @Query("UPDATE outbound_sync_events SET syncedAt = :syncedAt, lastError = '' WHERE eventId = :eventId AND syncedAt IS NULL")
    suspend fun markSynced(eventId: String, syncedAt: String)

    @Query("UPDATE outbound_sync_events SET attempts = attempts + 1, lastError = :error WHERE eventId = :eventId AND syncedAt IS NULL")
    suspend fun markFailed(eventId: String, error: String)
}
