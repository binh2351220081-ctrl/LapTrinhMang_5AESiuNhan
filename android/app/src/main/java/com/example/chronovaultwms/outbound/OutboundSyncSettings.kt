package com.example.chronovaultwms.outbound

import android.content.Context
import android.text.InputType
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/** Explicit server configuration; no invented login token or silent offline success. */
object OutboundSyncSettings {
    fun show(context: Context, database: ChronoVaultDatabase, actor: OutboundActor, onChanged: () -> Unit) {
        val prefs = context.getSharedPreferences("outbound_sync", Context.MODE_PRIVATE)
        val padding = (20 * context.resources.displayMetrics.density).toInt()
        val layout = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(padding, padding / 2, padding, padding / 2)
        }
        val status = TextView(context).apply {
            text = "Đồng bộ nhật ký xuất kho với máy chủ. Dữ liệu chưa gửi được giữ trong máy."
        }
        val server = EditText(context).apply {
            hint = "Máy chủ: https://... hoặc http://IP-máy-tính:8080"
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_URI
            setText(prefs.getString("url", ""))
        }
        val token = EditText(context).apply {
            hint = "Token do máy chủ cấp"
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            setText(prefs.getString("token", ""))
        }
        layout.addView(status)
        layout.addView(server)
        layout.addView(token)
        val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
        val dialog = MaterialAlertDialogBuilder(context).setTitle("Đồng bộ xuất kho")
            .setView(layout).setPositiveButton("Gửi dữ liệu", null)
            .setNeutralButton("Lưu cấu hình", null).setNegativeButton("Đóng", null).create()
        dialog.setOnDismissListener { scope.cancel() }
        dialog.setOnShowListener {
            fun save() = prefs.edit().putString("url", server.text.toString().trim())
                .putString("token", token.text.toString().trim()).apply()
            val send = dialog.getButton(androidx.appcompat.app.AlertDialog.BUTTON_POSITIVE)
            dialog.getButton(androidx.appcompat.app.AlertDialog.BUTTON_NEUTRAL).setOnClickListener {
                save()
                status.text = "Đã lưu cấu hình cho ${actor.name}."
            }
            send.setOnClickListener {
                save()
                send.isEnabled = false
                status.text = "Đang gửi dữ liệu…"
                scope.launch {
                    try {
                        val dao = database.outboundWorkflowDao()
                        val queue = object : OutboundSyncQueue {
                            override suspend fun pending() = dao.pendingEvents()
                            override suspend fun acknowledge(eventId: String, timestamp: String) = dao.markSynced(eventId, timestamp)
                            override suspend fun fail(eventId: String, message: String) = dao.markFailed(eventId, message)
                            override suspend fun count() = dao.pendingCount()
                        }
                        val result = OutboundNetworkClient.syncPending(queue,
                            OutboundSyncConfig(server.text.toString(), token.text.toString()))
                        status.text = "Đã gửi: ${result.sent} • Còn chờ: ${result.pending}" +
                            (result.error?.let { "\n$it" } ?: "\nMáy chủ đã xác nhận dữ liệu.")
                        onChanged()
                    } catch (e: CancellationException) {
                        throw e
                    } catch (e: Exception) {
                        status.text = "Chưa đồng bộ: ${e.message ?: "Lỗi kết nối"}"
                    } finally {
                        send.isEnabled = true
                    }
                }
            }
            scope.launch {
                val count = withContext(Dispatchers.IO) { database.outboundWorkflowDao().pendingCount() }
                status.text = "Có $count sự kiện chờ gửi.\nMáy chủ nhận nhật ký; việc phân bổ hàng giữa nhiều máy cần dịch vụ kho dùng chung."
            }
        }
        dialog.show()
    }
}
