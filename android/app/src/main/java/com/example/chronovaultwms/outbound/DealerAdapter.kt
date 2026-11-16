package com.example.chronovaultwms.outbound

import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.core.database.DealerEntity

class DealerAdapter(private var dealers: List<DealerEntity>, private val onClick: (DealerEntity) -> Unit) : RecyclerView.Adapter<DealerAdapter.Holder>() {
    fun updateData(items: List<DealerEntity>) { dealers = items; notifyDataSetChanged() }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder = Holder(outboundRow(parent))
    override fun getItemCount() = dealers.size
    override fun onBindViewHolder(holder: Holder, position: Int) {
        val dealer = dealers[position]
        holder.title.text = dealer.name
        holder.detail.text = "${dealer.dealerId} • ${outboundUnitStatus(dealer.status)}\n${dealer.address}\nLiên hệ: ${dealer.representative.ifBlank { "Chưa cập nhật" }} • ${dealer.phone}"
        holder.itemView.setOnClickListener { onClick(dealer) }
    }
    class Holder(row: LinearLayout) : RecyclerView.ViewHolder(row) {
        val title: TextView = row.getChildAt(0) as TextView
        val detail: TextView = row.getChildAt(1) as TextView
    }
}

internal fun outboundUnitStatus(status: String) = when (status) { "ACTIVE" -> "Đang nhận hàng"; "LOCKED" -> "Tạm khóa"; "SUSPENDED" -> "Ngừng tiếp nhận"; else -> status }

internal fun outboundRow(parent: ViewGroup): LinearLayout {
    val context = parent.context
    fun dp(value: Int) = (value * context.resources.displayMetrics.density).toInt()
    return LinearLayout(context).apply {
        orientation = LinearLayout.VERTICAL
        layoutParams = RecyclerView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply { bottomMargin = dp(10) }
        setPadding(dp(16), dp(14), dp(16), dp(14))
        background = GradientDrawable().apply { setColor(Color.WHITE); cornerRadius = dp(10).toFloat(); setStroke(dp(1), Color.rgb(220, 226, 232)) }
        addView(TextView(context).apply { textSize = 15f; setTextColor(Color.rgb(19, 36, 52)); setTypeface(typeface, Typeface.BOLD) })
        addView(TextView(context).apply { textSize = 12f; setTextColor(Color.rgb(75, 89, 101)); setPadding(0, dp(7), 0, 0); setLineSpacing(dp(3).toFloat(), 1f) })
        isClickable = true
        isFocusable = true
    }
}
