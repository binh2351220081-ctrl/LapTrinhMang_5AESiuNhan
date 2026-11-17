package com.example.chronovaultwms.outbound

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.DealerEntity
import com.example.chronovaultwms.core.database.OutboundOrderEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/** The ViewModel owns requests; the Fragment only gathers input and renders results. */
class OutboundViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = OutboundRepository(ChronoVaultDatabase.getInstance(application))
    private val mutableState = MutableLiveData<OutboundState>()
    private val mutableBusy = MutableLiveData(false)
    private val mutableResult = MutableLiveData<OutboundUiEvent>()
    val state: LiveData<OutboundState> = mutableState
    val busy: LiveData<Boolean> = mutableBusy
    val results: LiveData<OutboundUiEvent> = mutableResult
    private var nextRequest = 0

    fun requestId(): Int = ++nextRequest

    fun refresh() = execute(0) { OutboundUiResult() }

    fun saveDealer(id: Int, dealer: DealerEntity, actor: OutboundActor) = execute(id) {
        repository.saveDealer(dealer, actor)
        OutboundUiResult(message = "Đã lưu đơn vị nhận hàng.")
    }

    fun createDraft(id: Int, dealerId: String, lines: List<OutboundLineRequest>, note: String, actor: OutboundActor) = execute(id) {
        val code = repository.createDraft(dealerId, lines, note, actor)
        OutboundUiResult(message = "Đã lưu lệnh nháp $code. Hàng chỉ được giữ chỗ sau khi duyệt.")
    }

    fun approve(id: Int, code: String, actor: OutboundActor) = execute(id) {
        repository.approveOrder(code, actor)
        OutboundUiResult(message = "Đã duyệt $code và phân bổ Serial cho lệnh.")
    }

    fun cancel(id: Int, code: String, reason: String, actor: OutboundActor) = execute(id) {
        repository.cancelOrder(code, reason, actor)
        OutboundUiResult(message = "Đã hủy $code và giải phóng hàng giữ chỗ.")
    }

    fun openPicking(id: Int, order: OutboundOrderEntity, actor: OutboundActor) = execute(id) {
        repository.startPacking(order.orderCode, actor)
        OutboundUiResult(order = order, picking = repository.pickingList(order.orderCode), scannedSerials = repository.scannedSerials(order.orderCode))
    }

    fun recordScan(id: Int, code: String, input: String, actor: OutboundActor) = execute(id, reload = false) {
        OutboundUiResult(scannedSerials = repository.recordScan(code, input, actor))
    }

    fun complete(id: Int, code: String, scanned: List<String>, carrier: String, tracking: String, actor: OutboundActor) = execute(id) {
        val document = repository.completeDispatch(code, scanned, carrier, tracking, actor)
        OutboundUiResult(message = "Đã hoàn tất xuất kho $code.", document = document)
    }

    fun document(id: Int, code: String) = execute(id, reload = false) {
        OutboundUiResult(document = repository.dispatchDocument(code))
    }

    fun receiveReturn(id: Int, dealerId: String, serial: String, condition: String, reason: String, actor: OutboundActor) = execute(id) {
        val code = repository.receiveReturn(dealerId, serial, condition, reason, actor)
        OutboundUiResult(message = "Đã ghi nhận phiếu hoàn trả $code.")
    }

    fun otherDispatch(id: Int, serial: String, purpose: String, reason: String, actor: OutboundActor) = execute(id) {
        val code = repository.recordOtherDispatch(serial, purpose, reason, actor)
        OutboundUiResult(message = "Đã lưu phiếu xuất khác $code.")
    }

    fun recordReceipt(id: Int, dealerId: String, amount: Double, paymentMethod: String, referenceDoc: String, note: String, actor: OutboundActor) = execute(id) {
        val receiptId = repository.recordReceiptVoucher(dealerId, amount, paymentMethod, referenceDoc, note, actor)
        OutboundUiResult(message = "Đã lập phiếu thu $receiptId và giải phóng hạn mức cho đại lý.")
    }

    private fun execute(id: Int, reload: Boolean = true, operation: suspend () -> OutboundUiResult) {
        if (mutableBusy.value == true) return
        mutableBusy.value = true
        viewModelScope.launch {
            try {
                val result = withContext(Dispatchers.IO) { operation() }
                if (reload) mutableState.value = withContext(Dispatchers.IO) { repository.loadState() }
                if (id != 0 || result.message != null) mutableResult.value = OutboundUiEvent(id, result)
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (error: Exception) {
                mutableResult.value = OutboundUiEvent(id, error = error.message ?: "Không thể xử lý yêu cầu. Vui lòng thử lại.")
            } finally {
                mutableBusy.value = false
            }
        }
    }
}

data class OutboundUiResult(
    val message: String? = null,
    val order: OutboundOrderEntity? = null,
    val picking: List<OutboundPick>? = null,
    val scannedSerials: List<String>? = null,
    val document: OutboundDocument? = null
)

class OutboundUiEvent(val requestId: Int, val result: OutboundUiResult? = null, val error: String? = null) {
    private var consumed = false
    fun consume(): Boolean = if (consumed) false else { consumed = true; true }
}
