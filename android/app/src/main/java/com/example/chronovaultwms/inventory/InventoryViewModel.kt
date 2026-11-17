package com.example.chronovaultwms.inventory

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.core.database.SerialEntity
import com.example.chronovaultwms.core.database.AuditLogEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class InventoryViewModel(application: Application) : AndroidViewModel(application) {
    private val database = ChronoVaultDatabase.getInstance(application)
    private val productDao = database.productDao()
    private val serialDao = database.serialDao()
    private val auditLogDao = database.auditLogDao()

    private val _serialList = MutableLiveData<List<SerialEntity>>()
    val serialList: LiveData<List<SerialEntity>> get() = _serialList

    private val _auditResult = MutableLiveData<AuditComparisonResult>()
    val auditResult: LiveData<AuditComparisonResult> get() = _auditResult

    private fun getCurrentTimestamp(): String {
        return SimpleDateFormat("dd/MM/yyyy HH:mm:ss", Locale.getDefault()).format(Date())
    }

    fun loadSerialsByQuality(qualityStatus: String) {
        viewModelScope.launch(Dispatchers.IO) {
            val list = serialDao.getSerialsByQuality(qualityStatus)
            _serialList.postValue(list)
        }
    }

    fun loadSerialsByBin(binLocation: String) {
        viewModelScope.launch(Dispatchers.IO) {
            val list = serialDao.getSerialsByBin(binLocation)
            _serialList.postValue(list)
        }
    }

    fun changeSerialQuality(serialNumber: String, newQuality: String, reason: String, username: String) {
        viewModelScope.launch(Dispatchers.IO) {
            serialDao.updateSerialQuality(serialNumber, newQuality)
            auditLogDao.insert(
                AuditLogEntity(
                    timestamp = getCurrentTimestamp(),
                    actorName = username,
                    role = "STAFF",
                    action = "CHANGE_QUALITY",
                    details = "Serial: $serialNumber chuyển sang $newQuality. Lý do: $reason"
                )
            )
        }
    }

    fun relocateSerialBin(serialNumber: String, newBin: String, username: String) {
        viewModelScope.launch(Dispatchers.IO) {
            serialDao.updateSerialBin(serialNumber, newBin)
            auditLogDao.insert(
                AuditLogEntity(
                    timestamp = getCurrentTimestamp(),
                    actorName = username,
                    role = "STAFF",
                    action = "RELOCATE_BIN",
                    details = "Điều chuyển Serial: $serialNumber sang kệ $newBin"
                )
            )
        }
    }

    fun performStockAudit(targetBinOrCategory: String, scannedSerials: List<String>, username: String) {
        viewModelScope.launch(Dispatchers.IO) {
            val systemSerials = serialDao.getSerialsByBin(targetBinOrCategory).map { it.serialNumber }

            val matched = scannedSerials.intersect(systemSerials.toSet()).toList()
            val surplus = scannedSerials.subtract(systemSerials.toSet()).toList()
            val deficit = systemSerials.subtract(scannedSerials.toSet()).toList()

            _auditResult.postValue(AuditComparisonResult(matched, surplus, deficit))

            auditLogDao.insert(
                AuditLogEntity(
                    timestamp = getCurrentTimestamp(),
                    actorName = username,
                    role = "STAFF",
                    action = "STOCK_AUDIT",
                    details = "Kiểm kê khu vực $targetBinOrCategory. Khớp: ${matched.size}, Thừa: ${surplus.size}, Thiếu: ${deficit.size}"
                )
            )
        }
    }
}

data class AuditComparisonResult(
    val matched: List<String>,
    val surplus: List<String>,
    val deficit: List<String>
)