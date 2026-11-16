package com.example.chronovaultwms.dashboard.domain

import org.junit.Assert.assertEquals
import org.junit.Test

class ReportCalculationsTest {
    @Test fun inventoryValueUsesSpecificSerialCosts() =
        assertEquals(450.0, ReportCalculations.specificInventoryValue(listOf(100.0, 150.0, 200.0)), 0.0)

    @Test fun grossProfitSubtractsCostAndLogistics() =
        assertEquals(250.0, ReportCalculations.grossProfit(1000.0, 700.0, 50.0), 0.0)

    @Test fun endingBalanceSupportsTwoWayDebt() =
        assertEquals(750.0, ReportCalculations.endingBalance(500.0, 400.0, 150.0), 0.0)

    @Test fun returnRateIsZeroWhenNothingSold() =
        assertEquals(0.0, ReportCalculations.returnRatePercent(2, 0), 0.0)
}
