package com.example.chronovaultwms.outbound

import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.core.database.OutboundOrderEntity

class OutboundOrderAdapter(private var orders: List<OutboundOrderEntity>, private val onClick: (OutboundOrderEntity) -> Unit) : RecyclerView.Adapter<OutboundOrderAdapter.Holder>() {
    fun updateData(items: List<OutboundOrderEntity>) { orders = items; notifyDataSetChanged() }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder = Holder(outboundRow(parent))
    override fun getItemCount() = orders.size
    override fun onBindViewHolder(holder: Holder, position: Int) {
        val order = orders[position]
        holder.title.text = "${order.orderCode} • ${outboundOrderStatus(order.status)}"
        holder.detail.text = "${order.dealerName}\n${order.productName} • ${order.convertedQuantity} chiếc\nLập: ${order.createdDate} • ${order.createdBy.ifBlank { "Dữ liệu cũ" }}"
        holder.itemView.setOnClickListener { onClick(order) }
    }
    class Holder(row: LinearLayout) : RecyclerView.ViewHolder(row) {
        val title: TextView = row.getChildAt(0) as TextView
        val detail: TextView = row.getChildAt(1) as TextView
    }
}

internal fun outboundOrderStatus(status: String) = when (status) {
    "DRAFT" -> "Nháp / Chờ duyệt"
    "RESERVED" -> "Đã giữ chỗ"
    "PACKING" -> "Đang soạn hàng"
    "COMPLETED" -> "Đã xuất bàn giao"
    "CANCELLED" -> "Đã hủy"
    else -> status
}
