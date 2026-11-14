package com.example.chronovaultwms.dashboard.data

import com.example.chronovaultwms.dashboard.model.DashboardSnapshot
import com.example.chronovaultwms.dashboard.model.DateRange
import com.example.chronovaultwms.dashboard.model.ReportTable
import com.example.chronovaultwms.dashboard.model.ReportType
import kotlinx.coroutines.flow.Flow

interface DashboardRepository {
    fun observeDashboard(): Flow<DashboardSnapshot>
    suspend fun loadReport(type: ReportType, range: DateRange): ReportTable
}
