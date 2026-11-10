package com.example.chronovaultwms.dashboard.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.dashboard.data.RoomDashboardRepository
import com.example.chronovaultwms.dashboard.model.DashboardSnapshot
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn

class DashboardViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = RoomDashboardRepository(ChronoVaultDatabase.getInstance(application))
    val dashboard: StateFlow<DashboardSnapshot?> = repository.observeDashboard()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)
}
