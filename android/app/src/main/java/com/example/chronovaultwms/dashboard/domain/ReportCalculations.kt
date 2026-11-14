package com.example.chronovaultwms.dashboard.domain

object ReportCalculations {
    fun specificInventoryValue(serialCosts: Iterable<Double>): Double = serialCosts.sum()
    fun grossProfit(revenue: Double, specificCost: Double, logisticsCost: Double): Double =
        revenue - specificCost - logisticsCost
    fun endingBalance(opening: Double, debit: Double, credit: Double): Double = opening + debit - credit
    fun netCashflow(cashIn: Double, cashOut: Double): Double = cashIn - cashOut
    fun returnRatePercent(returnedQuantity: Int, soldQuantity: Int): Double =
        if (soldQuantity == 0) 0.0 else returnedQuantity * 100.0 / soldQuantity
}
