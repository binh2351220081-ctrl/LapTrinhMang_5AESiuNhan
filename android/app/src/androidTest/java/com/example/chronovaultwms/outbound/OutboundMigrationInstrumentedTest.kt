package com.example.chronovaultwms.outbound

import android.database.sqlite.SQLiteDatabase
import androidx.room.Room
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.OutboundMigrations
import kotlinx.coroutines.runBlocking
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.util.UUID

@RunWith(AndroidJUnit4::class)
class OutboundMigrationInstrumentedTest {
    @Test fun version5MigratesThroughRoomValidationWithoutDroppingHistory() = runBlocking {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val name = "migration-tv3-${UUID.randomUUID()}.db"
        val file = context.getDatabasePath(name)
        file.parentFile!!.mkdirs()
        SQLiteDatabase.openOrCreateDatabase(file, null).use { old ->
            old.execSQL("CREATE TABLE products (productCode TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, brand TEXT NOT NULL, category TEXT NOT NULL, wholesalePrice REAL NOT NULL, retailPrice REAL NOT NULL, stockQuantity INTEGER NOT NULL, caseDiameter TEXT NOT NULL, dialColor TEXT NOT NULL, movementType TEXT NOT NULL, waterResistance TEXT NOT NULL, status TEXT NOT NULL)")
            old.execSQL("CREATE TABLE serials (serialNumber TEXT NOT NULL PRIMARY KEY, productCode TEXT NOT NULL, status TEXT NOT NULL, currentLocation TEXT NOT NULL, importDate TEXT NOT NULL, unitCost REAL NOT NULL, supplierName TEXT NOT NULL, dealerName TEXT, qcNotes TEXT NOT NULL)")
            old.execSQL("CREATE TABLE users (userId TEXT NOT NULL PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, fullName TEXT NOT NULL, role TEXT NOT NULL, department TEXT NOT NULL, email TEXT NOT NULL, status TEXT NOT NULL)")
            old.execSQL("CREATE TABLE audit_logs (logId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, timestamp TEXT NOT NULL, actorName TEXT NOT NULL, role TEXT NOT NULL, action TEXT NOT NULL, details TEXT NOT NULL, ipAddress TEXT NOT NULL)")
            old.execSQL("CREATE TABLE dealers (dealerId TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, tier TEXT NOT NULL, discountPercent REAL NOT NULL, creditLimit REAL NOT NULL, currentDebt REAL NOT NULL, phone TEXT NOT NULL, address TEXT NOT NULL, taxCode TEXT NOT NULL, status TEXT NOT NULL)")
            old.execSQL("CREATE TABLE outbound_orders (orderCode TEXT NOT NULL PRIMARY KEY, dealerId TEXT NOT NULL, dealerName TEXT NOT NULL, productCode TEXT NOT NULL, productName TEXT NOT NULL, unit TEXT NOT NULL, quantity INTEGER NOT NULL, convertedQuantity INTEGER NOT NULL, unitPrice REAL NOT NULL, discountPercent REAL NOT NULL, totalAmount REAL NOT NULL, depositAmount REAL NOT NULL, remainingDebt REAL NOT NULL, status TEXT NOT NULL, createdDate TEXT NOT NULL, dispatchedSerials TEXT NOT NULL)")
            old.execSQL("CREATE TABLE dealer_receipts (receiptId TEXT NOT NULL PRIMARY KEY, dealerId TEXT NOT NULL, dealerName TEXT NOT NULL, amount REAL NOT NULL, paymentMethod TEXT NOT NULL, referenceDoc TEXT NOT NULL, date TEXT NOT NULL, note TEXT NOT NULL)")
            old.execSQL("INSERT INTO products VALUES ('OLD-SKU','Hàng cũ','Test','Test',100,120,1,'40','Đen','Cơ','10ATM','ACTIVE')")
            old.execSQL("INSERT INTO dealers VALUES ('OLD-UNIT','Đơn vị cũ','VIP',0.25,1000,200,'090','Kho cũ','MST-OLD','ACTIVE')")
            old.execSQL("INSERT INTO serials VALUES ('OLD-SN','OLD-SKU','DISPATCHED','Đã bàn giao','01/11/2026',80,'Đơn vị giao','Đơn vị cũ','QC cũ')")
            old.execSQL("INSERT INTO outbound_orders VALUES ('OLD-ORDER','OLD-UNIT','Đơn vị cũ','OLD-SKU','Hàng cũ','PIECE',1,1,100,0.25,75,25,50,'COMPLETED','02/11/2026 08:00','OLD-SN')")
            old.execSQL("INSERT INTO outbound_orders VALUES ('OLD-RESERVED','OLD-UNIT','Đơn vị cũ','OLD-SKU','Hàng cũ','PIECE',1,1,100,0,100,0,100,'RESERVED','03/11/2026 08:00','')")
            old.execSQL("INSERT INTO dealer_receipts VALUES ('OLD-PT','OLD-UNIT','Đơn vị cũ',123,'TIEN_MAT','REF-OLD','02/11/2026','Phiếu lịch sử')")
            old.execSQL("INSERT INTO audit_logs(timestamp,actorName,role,action,details,ipAddress) VALUES ('01/11/2026','Người cũ','OPERATIONS_STAFF','OLD','Lịch sử giữ nguyên','local')")
            old.version = 5
        }
        val migrated = Room.databaseBuilder(context, ChronoVaultDatabase::class.java, name)
            .addMigrations(OutboundMigrations.MIGRATION_5_6).build()
        try {
            // The first DAO access executes Room's actual migration and full schema validation.
            val product = migrated.productDao().getProductByCode("OLD-SKU")!!
            assertEquals("Hàng cũ", product.name)
            assertEquals(10, product.conversionRate)
            assertEquals(1, product.minDispatchQuantity)
            assertEquals("", migrated.dealerDao().getDealerById("OLD-UNIT")!!.representative)
            assertEquals(200.0, migrated.dealerDao().getDealerById("OLD-UNIT")!!.currentDebt, 0.0)
            assertEquals(123.0, migrated.dealerReceiptDao().getAllReceipts().single().amount, 0.0)
            assertEquals("RESERVED", migrated.outboundOrderDao().getOrderByCode("OLD-RESERVED")!!.status)
            assertEquals("", migrated.outboundOrderDao().getOrderByCode("OLD-ORDER")!!.approvedBy)
            assertEquals(1, migrated.auditLogDao().getAllLogs().size)
            assertEquals(1, migrated.outboundWorkflowDao().orderLines("OLD-ORDER").size)
            assertEquals("OLD-SN", migrated.outboundWorkflowDao().allocations("OLD-ORDER").single().serialNumber)
            assertEquals("OLD-UNIT", migrated.serialDao().getSerialByNumber("OLD-SN")!!.dealerId)
            assertNotNull(migrated.outboundWorkflowDao().dispatchForOrder("OLD-ORDER"))
            assertEquals(0, migrated.outboundWorkflowDao().pendingCount())
        } finally {
            migrated.close()
            context.deleteDatabase(name)
        }
    }
}
