package com.example.chronovaultwms.dashboard.ui.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.dashboard.model.AuditActivity
import com.example.chronovaultwms.databinding.ItemDashboardActivityBinding

class ActivityAdapter : RecyclerView.Adapter<ActivityAdapter.ViewHolder>() {
    private var items: List<AuditActivity> = emptyList()
    fun submitList(newItems: List<AuditActivity>) { items = newItems; notifyDataSetChanged() }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = ViewHolder(
        ItemDashboardActivityBinding.inflate(LayoutInflater.from(parent.context), parent, false)
    )
    override fun onBindViewHolder(holder: ViewHolder, position: Int) = holder.bind(items[position])
    override fun getItemCount() = items.size

    class ViewHolder(private val binding: ItemDashboardActivityBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(item: AuditActivity) = with(binding) {
            tvActivityTime.text = item.timeLabel
            tvActivityTitle.text = item.title
            tvActivityDetail.text = "${item.detail}\nNguồn: ${item.sourceModule}"
        }
    }
}
