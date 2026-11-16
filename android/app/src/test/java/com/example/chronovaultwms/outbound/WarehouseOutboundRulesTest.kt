package com.example.chronovaultwms.outbound

import com.example.chronovaultwms.core.database.DatabaseSeeder
import org.junit.Assert.*
import org.junit.Test

class WarehouseOutboundRulesTest {
    @Test fun operatorAndPhysicalApproverAreSeparated() {
        val operator = OutboundActor("Thảo", "OPERATIONS_STAFF")
        WarehouseOutboundRules.requireOperator(operator)
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.requireManager(operator) }
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.requireOperator(OutboundActor("Admin", "SYSTEM_ADMIN")) }
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.requireOperator(OutboundActor("", "STORE_OWNER")) }
        WarehouseOutboundRules.requireManager(OutboundActor("Tâm", "WAREHOUSE_MANAGER"))
    }

    @Test fun configurationControlsConversionAndRejectsOverflow() {
        assertEquals(24, WarehouseOutboundRules.convertQuantity(2, true, 12))
        assertEquals(2, WarehouseOutboundRules.convertQuantity(2, false, 12))
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.convertQuantity(0, false, 12) }
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.convertQuantity(1, true, 0) }
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.convertQuantity(Int.MAX_VALUE, true, 10) }
    }

    @Test fun exactScanSetRejectsDuplicateMissingWrongAndEmptyPicking() {
        WarehouseOutboundRules.requireExactScanSet(listOf("A", "B"), listOf("B", "A"))
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.requireExactScanSet(listOf("A", "B"), listOf("A", "A")) }
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.requireExactScanSet(listOf("A", "B"), listOf("A")) }
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.requireExactScanSet(listOf("A", "B"), listOf("A", "C")) }
        assertThrows(IllegalArgumentException::class.java) { WarehouseOutboundRules.requireExactScanSet(emptyList(), emptyList()) }
    }

    @Test fun warehouseSeedHasRealSerialForEveryPhysicalNewUnit() {
        DatabaseSeeder.sampleWarehouseProducts.forEach { product ->
            assertEquals(product.productCode, product.stockQuantity,
                DatabaseSeeder.sampleWarehouseSerials.count { it.productCode == product.productCode && it.status in setOf("IN_STOCK", "ALLOCATED") })
        }
        assertTrue(DatabaseSeeder.sampleWarehouseSerials.none { it.status == "ALLOCATED" && it.allocatedOrderCode == null })
    }

    @Test fun fifoUnderstandsBothImportDateFormatsAndRejectsInvalidCalendarDates() {
        assertEquals(OutboundLogisticsManager.parseImportDateKey("01/11/2026 08:00"), OutboundLogisticsManager.parseImportDateKey("2026-11-01 08:00"))
        assertTrue(OutboundLogisticsManager.parseImportDateKey("31/12/2025 23:59") < OutboundLogisticsManager.parseImportDateKey("01/01/2026 00:00"))
        assertEquals(Long.MAX_VALUE, OutboundLogisticsManager.parseImportDateKey("31/02/2026"))
    }

    @Test fun invalidLegacyClearanceCannotWriteNaN() {
        assertFalse(OutboundLogisticsManager.validateClearanceVoucher(Double.NaN, 100.0).isValid)
        assertFalse(OutboundLogisticsManager.validateClearanceVoucher(1.0, Double.POSITIVE_INFINITY).isValid)
    }
}
