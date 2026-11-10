package com.example.chronovaultwms.core.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [ProductEntity::class], version = 1, exportSchema = false)
abstract class ChronoVaultDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao

    companion object {
        @Volatile
        private var INSTANCE: ChronoVaultDatabase? = null

        fun getInstance(context: Context): ChronoVaultDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    ChronoVaultDatabase::class.java,
                    "chronovault_wms.db"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}

