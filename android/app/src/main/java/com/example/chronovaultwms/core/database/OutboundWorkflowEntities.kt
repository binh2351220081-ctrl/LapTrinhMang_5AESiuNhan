package com.example.chronovaultwms.core.database

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "outbound_lines",
    primaryKeys = ["orderCode", "productCode"],
    foreignKeys = [ForeignKey(entity = OutboundOrderEntity::class, parentColumns = ["orderCode"], childColumns = ["orderCode"], onDelete = ForeignKey.CASCADE)],
    indices = [Index("productCode")]
)
data class OutboundLineEntity(
    val orderCode: String,
    val productCode: String,
    val productName: String,
    val unit: String,
    val quantity: Int,
    val convertedQuantity: Int,
    val unitCost: Double
)

/** Immutable picking snapshot: cancellations keep this history but release Serial ownership. */
@Entity(
    tableName = "outbound_allocations",
    primaryKeys = ["orderCode", "serialNumber"],
    foreignKeys = [ForeignKey(entity = OutboundOrderEntity::class, parentColumns = ["orderCode"], childColumns = ["orderCode"], onDelete = ForeignKey.CASCADE)],
    indices = [Index("serialNumber")]
)
data class OutboundAllocationEntity(
    val orderCode: String,
    val serialNumber: String,
    val productCode: String,
    val productName: String,
    val sourceLocation: String,
    val importDate: String,
    val unitCost: Double,
    val lotNumber: Int,
    val scannedAt: String = "",
    val scannedBy: String = ""
)

@Entity(tableName = "outbound_dispatches", indices = [Index(value = ["orderCode"], unique = true)])
data class OutboundDispatchEntity(
    @PrimaryKey val dispatchCode: String,
    val orderCode: String,
    val dealerId: String,
    val dealerName: String,
    val address: String,
    val dispatchedAt: String,
    val dispatchedBy: String,
    val carrier: String,
    val trackingNumber: String,
    val note: String
)

@Entity(tableName = "outbound_returns", indices = [Index("serialNumber"), Index("dispatchCode")])
data class OutboundReturnEntity(
    @PrimaryKey val returnCode: String,
    val dispatchCode: String,
    val dealerId: String,
    val serialNumber: String,
    val inspectedCondition: String,
    val reason: String,
    val targetLocation: String,
    val receivedAt: String,
    val receivedBy: String
)

@Entity(tableName = "outbound_other_dispatches", indices = [Index("serialNumber")])
data class OutboundOtherDispatchEntity(
    @PrimaryKey val dispatchCode: String,
    val serialNumber: String,
    val purpose: String,
    val reason: String,
    val sourceLocation: String,
    val dispatchedAt: String,
    val dispatchedBy: String,
    val approvedBy: String
)

/** Per-Serial stock ledger. A reservation does not change physical quantity. */
@Entity(tableName = "stock_movements", indices = [Index("serialNumber"), Index("productCode"), Index("referenceCode")])
data class StockMovementEntity(
    @PrimaryKey val movementId: String,
    val movementType: String,
    val referenceCode: String,
    val serialNumber: String,
    val productCode: String,
    val fromLocation: String,
    val toLocation: String,
    val changeQuantity: Int,
    val balanceAfter: Int,
    val actorName: String,
    val timestamp: String
)

@Entity(tableName = "outbound_sync_events", indices = [Index("createdAt")])
data class OutboundSyncEventEntity(
    @PrimaryKey val eventId: String,
    val eventType: String,
    val aggregateId: String,
    val payloadJson: String,
    val createdAt: String,
    val attempts: Int = 0,
    val lastError: String = "",
    val syncedAt: String? = null
)
