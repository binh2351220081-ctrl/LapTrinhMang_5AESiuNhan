package com.example.chronovaultwms.dashboard.ui.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.dashboard.model.TopProduct
import com.example.chronovaultwms.databinding.ItemDashboardTopProductBinding
import java.text.NumberFormat
import java.util.Locale

class TopProductAdapter : RecyclerView.Adapter<TopProductAdapter.ViewHolder>() {
    private var items: List<TopProduct> = emptyList()
    fun submitList(newItems: List<TopProduct>) { items = newItems; notifyDataSetChanged() }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = ViewHolder(
        ItemDashboardTopProductBinding.inflate(LayoutInflater.from(parent.context), parent, false)
    )
    override fun onBindViewHolder(holder: ViewHolder, position: Int) = holder.bind(items[position], position)
    override fun getItemCount() = items.size

    class ViewHolder(private val binding: ItemDashboardTopProductBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(item: TopProduct, position: Int) = with(binding) {
            tvRank.text = (position + 1).toString()
            tvProductName.text = item.name
            tvProductSku.text = item.sku
            tvProductMetric.text = "${item.quantitySold} chiếc\n${NumberFormat.getCurrencyInstance(Locale.forLanguageTag("vi-VN")).format(item.revenue)}"
        }
    }
}
