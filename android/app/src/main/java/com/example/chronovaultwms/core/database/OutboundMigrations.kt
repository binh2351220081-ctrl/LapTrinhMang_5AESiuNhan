package com.example.chronovaultwms.core.database

import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

/** Additive migration: v5 orders, contacts, serials and receipts are retained. */
object OutboundMigrations {
    val MIGRATION_5_6 = object : Migration(5, 6) {
        override fun migrate(db: SupportSQLiteDatabase) {
            db.execSQL("ALTER TABLE products ADD COLUMN conversionRate INTEGER NOT NULL DEFAULT 10")
            db.execSQL("ALTER TABLE products ADD COLUMN minDispatchQuantity INTEGER NOT NULL DEFAULT 1")
            db.execSQL("ALTER TABLE dealers ADD COLUMN representative TEXT NOT NULL DEFAULT ''")
            db.execSQL("ALTER TABLE dealers ADD COLUMN email TEXT NOT NULL DEFAULT ''")
            listOf("dealerId", "allocatedOrderCode", "lastDispatchCode", "lastDispatchAt").forEach {
                db.execSQL("ALTER TABLE serials ADD COLUMN $it TEXT")
            }
            listOf("note", "createdBy", "approvedBy", "approvedAt", "dispatchedBy", "dispatchedAt", "cancelReason").forEach {
                db.execSQL("ALTER TABLE outbound_orders ADD COLUMN $it TEXT NOT NULL DEFAULT ''")
            }
            db.execSQL("""CREATE TABLE IF NOT EXISTS outbound_lines (
                orderCode TEXT NOT NULL, productCode TEXT NOT NULL, productName TEXT NOT NULL,
                unit TEXT NOT NULL, quantity INTEGER NOT NULL, convertedQuantity INTEGER NOT NULL,
                unitCost REAL NOT NULL, PRIMARY KEY(orderCode, productCode),
                FOREIGN KEY(orderCode) REFERENCES outbound_orders(orderCode) ON UPDATE NO ACTION ON DELETE CASCADE)""")
            db.execSQL("CREATE INDEX IF NOT EXISTS index_outbound_lines_productCode ON outbound_lines(productCode)")
            db.execSQL("""CREATE TABLE IF NOT EXISTS outbound_allocations (
                orderCode TEXT NOT NULL, serialNumber TEXT NOT NULL, productCode TEXT NOT NULL,
                productName TEXT NOT NULL, sourceLocation TEXT NOT NULL, importDate TEXT NOT NULL,
                unitCost REAL NOT NULL, lotNumber INTEGER NOT NULL, scannedAt TEXT NOT NULL, scannedBy TEXT NOT NULL, PRIMARY KEY(orderCode, serialNumber),
                FOREIGN KEY(orderCode) REFERENCES outbound_orders(orderCode) ON UPDATE NO ACTION ON DELETE CASCADE)""")
            db.execSQL("CREATE INDEX IF NOT EXISTS index_outbound_allocations_serialNumber ON outbound_allocations(serialNumber)")
            db.execSQL("""CREATE TABLE IF NOT EXISTS outbound_dispatches (
                dispatchCode TEXT NOT NULL PRIMARY KEY, orderCode TEXT NOT NULL, dealerId TEXT NOT NULL,
                dealerName TEXT NOT NULL, address TEXT NOT NULL, dispatchedAt TEXT NOT NULL,
                dispatchedBy TEXT NOT NULL, carrier TEXT NOT NULL, trackingNumber TEXT NOT NULL, note TEXT NOT NULL)""")
            db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS index_outbound_dispatches_orderCode ON outbound_dispatches(orderCode)")
            db.execSQL("""CREATE TABLE IF NOT EXISTS outbound_returns (
                returnCode TEXT NOT NULL PRIMARY KEY, dispatchCode TEXT NOT NULL, dealerId TEXT NOT NULL,
                serialNumber TEXT NOT NULL, inspectedCondition TEXT NOT NULL, reason TEXT NOT NULL,
                targetLocation TEXT NOT NULL, receivedAt TEXT NOT NULL, receivedBy TEXT NOT NULL)""")
            db.execSQL("CREATE INDEX IF NOT EXISTS index_outbound_returns_serialNumber ON outbound_returns(serialNumber)")
            db.execSQL("CREATE INDEX IF NOT EXISTS index_outbound_returns_dispatchCode ON outbound_returns(dispatchCode)")
            db.execSQL("""CREATE TABLE IF NOT EXISTS outbound_other_dispatches (
                dispatchCode TEXT NOT NULL PRIMARY KEY, serialNumber TEXT NOT NULL, purpose TEXT NOT NULL,
                reason TEXT NOT NULL, sourceLocation TEXT NOT NULL, dispatchedAt TEXT NOT NULL,
                dispatchedBy TEXT NOT NULL, approvedBy TEXT NOT NULL)""")
            db.execSQL("CREATE INDEX IF NOT EXISTS index_outbound_other_dispatches_serialNumber ON outbound_other_dispatches(serialNumber)")
            db.execSQL("""CREATE TABLE IF NOT EXISTS stock_movements (
                movementId TEXT NOT NULL PRIMARY KEY, movementType TEXT NOT NULL, referenceCode TEXT NOT NULL,
                serialNumber TEXT NOT NULL, productCode TEXT NOT NULL, fromLocation TEXT NOT NULL,
                toLocation TEXT NOT NULL, changeQuantity INTEGER NOT NULL, balanceAfter INTEGER NOT NULL,
                actorName TEXT NOT NULL, timestamp TEXT NOT NULL)""")
            listOf("serialNumber", "productCode", "referenceCode").forEach {
                db.execSQL("CREATE INDEX IF NOT EXISTS index_stock_movements_$it ON stock_movements($it)")
            }
            db.execSQL("""CREATE TABLE IF NOT EXISTS outbound_sync_events (
                eventId TEXT NOT NULL PRIMARY KEY, eventType TEXT NOT NULL, aggregateId TEXT NOT NULL,
                payloadJson TEXT NOT NULL, createdAt TEXT NOT NULL, attempts INTEGER NOT NULL,
                lastError TEXT NOT NULL, syncedAt TEXT)""")
            db.execSQL("CREATE INDEX IF NOT EXISTS index_outbound_sync_events_createdAt ON outbound_sync_events(createdAt)")

            // Preserve the one-SKU representation of existing orders as an explicit detail row.
            db.execSQL("""INSERT INTO outbound_lines
                SELECT orderCode, productCode, productName, unit, quantity, convertedQuantity, unitPrice
                FROM outbound_orders""")
            // A migration record is clearly marked; no invented approval/dispatch actor is assigned.
            db.execSQL("""INSERT INTO outbound_dispatches
                SELECT 'PX-MIG-' || o.orderCode, o.orderCode, o.dealerId, o.dealerName,
                    COALESCE(d.address, ''), o.createdDate, '', '', '', 'Chuyển dữ liệu v5; ngày xuất/người xác nhận chưa được ghi riêng'
                FROM outbound_orders o LEFT JOIN dealers d ON d.dealerId = o.dealerId
                WHERE o.status = 'COMPLETED'""")
            db.execSQL("""INSERT INTO outbound_allocations
                SELECT o.orderCode, s.serialNumber, s.productCode, o.productName, s.currentLocation,
                    s.importDate, s.unitCost, 1, '', ''
                FROM outbound_orders o JOIN serials s
                    ON (',' || REPLACE(o.dispatchedSerials, ' ', '') || ',') LIKE ('%,' || s.serialNumber || ',%')
                WHERE o.status = 'COMPLETED'""")
            db.execSQL("""UPDATE serials SET
                dealerId = (SELECT o.dealerId FROM outbound_orders o JOIN outbound_allocations a ON a.orderCode = o.orderCode
                    WHERE a.serialNumber = serials.serialNumber AND o.status = 'COMPLETED' ORDER BY o.createdDate DESC LIMIT 1),
                lastDispatchCode = (SELECT 'PX-MIG-' || a.orderCode FROM outbound_allocations a JOIN outbound_orders o ON o.orderCode=a.orderCode
                    WHERE a.serialNumber = serials.serialNumber AND o.status='COMPLETED' ORDER BY o.createdDate DESC LIMIT 1)
                WHERE status IN ('DISPATCHED', 'DELIVERED', 'SOLD')""")
        }
    }
}
