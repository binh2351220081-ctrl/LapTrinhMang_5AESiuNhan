package com.example.chronovaultwms.outbound

import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.core.database.OutboundOrderEntity
import com.example.chronovaultwms.databinding.ItemOutboundOrderBinding
import java.text.DecimalFormat

class OutboundOrderAdapter(
    private var orders: List<OutboundOrderEntity>,
    private val onDispatchClick: (OutboundOrderEntity) -> Unit
) : RecyclerView.Adapter<OutboundOrderAdapter.OrderViewHolder>() {

    private val formatter = DecimalFormat("#,###")

    fun updateData(newOrders: List<OutboundOrderEntity>) {
        orders = newOrders
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): OrderViewHolder {
        val binding = ItemOutboundOrderBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return OrderViewHolder(binding)
    }

    override fun onBindViewHolder(holder: OrderViewHolder, position: Int) {
        holder.bind(orders[position])
    }

    override fun getItemCount(): Int = orders.size

    inner class OrderViewHolder(private val binding: ItemOutboundOrderBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(order: OutboundOrderEntity) {
            binding.tvOrderCode.text = order.orderCode
            binding.tvOrderDealerName.text = "🏪 ${order.dealerName}"
            binding.tvOrderCreatedDate.text = "🕒 Ngày đặt: ${order.createdDate}"
            binding.tvOrderProductSummary.text = "⌚ ${order.productName}"
            binding.tvOrderQuantitySummary.text = "Quy cách: ${order.convertedQuantity} chiếc lẻ (Chiết khấu ${(order.discountPercent * 100).toInt()}%)"
            binding.tvOrderTotalAmount.text = "${formatter.format(order.totalAmount)} đ"
            binding.tvOrderDeposit.text = "Đã cọc: ${formatter.format(order.depositAmount)} đ"
            binding.tvOrderRemainingDebt.text = "Còn nợ: ${formatter.format(order.remainingDebt)} đ"

            when (order.status) {
                "RESERVED" -> {
                    binding.tvOrderStatus.text = "🔒 Đã Giữ Chỗ (Reserved)"
                    binding.tvOrderStatus.setTextColor(Color.parseColor("#D97706"))
                    binding.btnDispatchOrder.visibility = View.VISIBLE
                    binding.btnDispatchOrder.text = "📦 Quét Serial Xuất Kho"
                }
                "COMPLETED" -> {
                    binding.tvOrderStatus.text = "✓ Đã Xuất Bàn Giao (Completed)"
                    binding.tvOrderStatus.setTextColor(Color.parseColor("#059669"))
                    binding.btnDispatchOrder.visibility = View.VISIBLE
                    binding.btnDispatchOrder.text = "🔍 Xem Biên Bản A4"
                }
                "CANCELLED" -> {
                    binding.tvOrderStatus.text = "✕ Đã Hủy Đơn"
                    binding.tvOrderStatus.setTextColor(Color.parseColor("#DC2626"))
                    binding.btnDispatchOrder.visibility = View.GONE
                }
                else -> {
                    binding.tvOrderStatus.text = order.status
                    binding.btnDispatchOrder.visibility = View.VISIBLE
                }
            }

            binding.btnDispatchOrder.setOnClickListener {
                onDispatchClick(order)
            }
        }
    }
}

