package com.example.chronovaultwms.core.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [
        ProductEntity::class,
        SerialEntity::class,
        UserEntity::class,
        AuditLogEntity::class,
        DealerEntity::class,
        OutboundOrderEntity::class,
        DealerReceiptEntity::class,
        OutboundLineEntity::class,
        OutboundAllocationEntity::class,
        OutboundDispatchEntity::class,
        OutboundReturnEntity::class,
        OutboundOtherDispatchEntity::class,
        StockMovementEntity::class,
        OutboundSyncEventEntity::class
    ],
    version = 6,
    exportSchema = false
)
abstract class ChronoVaultDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao
    abstract fun serialDao(): SerialDao
    abstract fun userDao(): UserDao
    abstract fun auditLogDao(): AuditLogDao
    abstract fun dealerDao(): DealerDao
    abstract fun outboundOrderDao(): OutboundOrderDao
    abstract fun dealerReceiptDao(): DealerReceiptDao
    abstract fun outboundWorkflowDao(): OutboundWorkflowDao

    companion object {
        @Volatile
        private var INSTANCE: ChronoVaultDatabase? = null

        fun getInstance(context: Context): ChronoVaultDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    ChronoVaultDatabase::class.java,
                    "chronovault_wms.db"
                )
                .addMigrations(OutboundMigrations.MIGRATION_5_6)
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
