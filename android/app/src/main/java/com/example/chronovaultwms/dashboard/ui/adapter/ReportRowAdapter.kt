package com.example.chronovaultwms.dashboard.ui.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.dashboard.model.ReportRow
import com.example.chronovaultwms.databinding.ItemDashboardReportRowBinding

class ReportRowAdapter : RecyclerView.Adapter<ReportRowAdapter.ViewHolder>() {
    private var headers: List<String> = emptyList()
    private var rows: List<ReportRow> = emptyList()
    fun submitData(newHeaders: List<String>, newRows: List<ReportRow>) {
        headers = newHeaders; rows = newRows; notifyDataSetChanged()
    }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = ViewHolder(
        ItemDashboardReportRowBinding.inflate(LayoutInflater.from(parent.context), parent, false)
    )
    override fun onBindViewHolder(holder: ViewHolder, position: Int) = holder.bind(headers, rows[position])
    override fun getItemCount() = rows.size

    class ViewHolder(private val binding: ItemDashboardReportRowBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(headers: List<String>, row: ReportRow) = with(binding) {
            tvReportRowTitle.text = row.values.firstOrNull().orEmpty()
            tvReportRowDetail.text = headers.drop(1).zip(row.values.drop(1)).joinToString("\n") { (header, value) -> "$header: $value" }
        }
    }
}
