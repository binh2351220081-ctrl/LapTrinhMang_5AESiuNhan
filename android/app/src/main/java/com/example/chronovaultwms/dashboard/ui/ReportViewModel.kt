package com.example.chronovaultwms.dashboard.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.dashboard.data.RoomDashboardRepository
import com.example.chronovaultwms.dashboard.model.DateRange
import com.example.chronovaultwms.dashboard.model.ReportTable
import com.example.chronovaultwms.dashboard.model.ReportType
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate

data class ReportUiState(
    val range: DateRange = DateRange(LocalDate.now().minusMonths(6), LocalDate.now()),
    val selectedType: ReportType = ReportType.INBOUND,
    val report: ReportTable? = null,
    val loading: Boolean = false,
    val error: String? = null
)

class ReportViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = RoomDashboardRepository(ChronoVaultDatabase.getInstance(application))
    private val _state = MutableStateFlow(ReportUiState())
    val state: StateFlow<ReportUiState> = _state.asStateFlow()

    init { refresh() }

    fun selectType(type: ReportType) {
        _state.value = _state.value.copy(selectedType = type)
        refresh()
    }

    fun setFrom(date: LocalDate) {
        val current = _state.value
        _state.value = current.copy(range = DateRange(date, maxOf(date, current.range.to)))
        refresh()
    }

    fun setTo(date: LocalDate) {
        val current = _state.value
        _state.value = current.copy(range = DateRange(minOf(date, current.range.from), date))
        refresh()
    }

    private fun refresh() = viewModelScope.launch {
        val current = _state.value
        _state.value = current.copy(loading = true, error = null)
        runCatching { repository.loadReport(current.selectedType, current.range) }
            .onSuccess { _state.value = _state.value.copy(report = it, loading = false) }
            .onFailure { _state.value = _state.value.copy(loading = false, error = it.message) }
    }
}
