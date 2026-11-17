package com.example.chronovaultwms.outbound

import com.example.chronovaultwms.core.database.OutboundOrderEntity
import com.example.chronovaultwms.core.database.OutboundSyncEventEntity
import com.google.gson.Gson
import com.google.gson.JsonParser
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import okhttp3.HttpUrl
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.time.Instant
import java.util.concurrent.TimeUnit

data class OutboundSyncConfig(val baseUrl: String, val token: String)
data class OutboundSyncReport(val sent: Int, val pending: Int, val error: String? = null)

interface OutboundSyncQueue {
    suspend fun pending(): List<OutboundSyncEventEntity>
    suspend fun acknowledge(eventId: String, timestamp: String)
    suspend fun fail(eventId: String, message: String)
    suspend fun count(): Int
}

/** Durable event transport: retry retains the same ID; only a matching server ACK marks it sent. */
object OutboundNetworkClient {
    const val EVENT_STOCK_RESERVED = "EVENT_STOCK_RESERVED"
    const val EVENT_DISPATCH_COMPLETED = "EVENT_DISPATCH_COMPLETED"
    private val mutex = Mutex()
    private val gson = Gson()
    private val jsonType = "application/json; charset=utf-8".toMediaType()
    private val client = OkHttpClient.Builder().connectTimeout(5, TimeUnit.SECONDS)
        .readTimeout(8, TimeUnit.SECONDS).writeTimeout(8, TimeUnit.SECONDS)
        .callTimeout(12, TimeUnit.SECONDS).build()

    fun formatBearerHeader(rawToken: String?): String {
        val value = rawToken?.trim().orEmpty()
        require(value.isNotEmpty()) { "Chưa cấu hình token đồng bộ." }
        val token = if (value.startsWith("Bearer ", true)) value.substring(7).trim() else value
        require(token.isNotEmpty() && '\n' !in token && '\r' !in token) { "Token đồng bộ không hợp lệ." }
        return "Bearer $token"
    }

    fun eventsUrl(baseUrl: String): HttpUrl {
        val base = baseUrl.trim().toHttpUrlOrNull()
            ?: throw IllegalArgumentException("Địa chỉ máy chủ phải bắt đầu bằng http:// hoặc https://.")
        require(base.username.isEmpty() && base.password.isEmpty() && base.query == null && base.fragment == null) {
            "Không đặt thông tin đăng nhập hoặc tham số trong địa chỉ máy chủ."
        }
        return base.newBuilder().encodedPath("/api/v1/warehouse/events").build()
    }

    fun buildEventPayload(event: OutboundSyncEventEntity): String {
        val data = JsonParser().parse(event.payloadJson)
        require(data.isJsonObject || data.isJsonArray) { "Nội dung sự kiện không hợp lệ." }
        return gson.toJson(mapOf("eventId" to event.eventId, "eventType" to event.eventType,
            "aggregateId" to event.aggregateId, "createdAt" to event.createdAt, "payload" to data))
    }

    suspend fun syncPending(queue: OutboundSyncQueue, config: OutboundSyncConfig): OutboundSyncReport = mutex.withLock {
        withContext(Dispatchers.IO) {
            val url = try { eventsUrl(config.baseUrl) } catch (e: IllegalArgumentException) {
                return@withContext OutboundSyncReport(0, queue.count(), e.message)
            }
            val bearer = try { formatBearerHeader(config.token) } catch (e: IllegalArgumentException) {
                return@withContext OutboundSyncReport(0, queue.count(), e.message)
            }
            var sent = 0
            while (true) {
                currentCoroutineContext().ensureActive()
                val batch = queue.pending()
                if (batch.isEmpty()) break
                for (event in batch) {
                    currentCoroutineContext().ensureActive()
                    try {
                        val request = Request.Builder().url(url).header("Authorization", bearer)
                            .header("Idempotency-Key", event.eventId)
                            .post(buildEventPayload(event).toRequestBody(jsonType)).build()
                        client.newCall(request).execute().use { response ->
                            check(response.isSuccessful) { "Máy chủ từ chối đồng bộ (HTTP ${response.code})." }
                            val ack = JsonParser().parse(response.body?.string().orEmpty()).asJsonObject
                            check(ack.get("success")?.asBoolean == true && ack.get("eventId")?.asString == event.eventId) {
                                "Máy chủ chưa xác nhận đúng sự kiện; dữ liệu vẫn được giữ để gửi lại."
                            }
                        }
                        queue.acknowledge(event.eventId, Instant.now().toString())
                        sent++
                    } catch (e: CancellationException) {
                        throw e
                    } catch (e: Exception) {
                        val error = e.message?.take(240) ?: "Không kết nối được máy chủ."
                        queue.fail(event.eventId, error)
                        return@withContext OutboundSyncReport(sent, queue.count(), error)
                    }
                }
            }
            OutboundSyncReport(sent, queue.count())
        }
    }

    // Original event shape remains available to consumers while they adopt the durable envelope.
    fun buildStockReservedPayload(order: OutboundOrderEntity): String = gson.toJson(mapOf(
        "eventType" to EVENT_STOCK_RESERVED, "orderCode" to order.orderCode,
        "dealerId" to order.dealerId, "productCode" to order.productCode,
        "quantity" to order.convertedQuantity, "serialNumbers" to emptyList<String>(),
        "actorName" to order.createdBy.ifBlank { "Tô Đức Thảo" }, "timestamp" to order.createdDate))

    fun buildDispatchCompletedPayload(order: OutboundOrderEntity, serials: List<String>, timestamp: String): String =
        gson.toJson(mapOf("eventType" to EVENT_DISPATCH_COMPLETED, "orderCode" to order.orderCode,
            "dealerId" to order.dealerId, "productCode" to order.productCode,
            "quantity" to order.convertedQuantity, "serialNumbers" to serials,
            "actorName" to order.dispatchedBy.ifBlank { "Tô Đức Thảo" }, "timestamp" to timestamp))
}
