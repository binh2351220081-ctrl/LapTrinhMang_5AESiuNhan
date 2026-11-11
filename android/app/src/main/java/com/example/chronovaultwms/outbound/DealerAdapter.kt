package com.example.chronovaultwms.outbound

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.core.database.DealerEntity
import com.example.chronovaultwms.databinding.ItemOutboundDealerBinding
import java.text.DecimalFormat

class DealerAdapter(
    private var dealers: List<DealerEntity>,
    private val onCollectDebtClick: (DealerEntity) -> Unit
) : RecyclerView.Adapter<DealerAdapter.DealerViewHolder>() {

    private val formatter = DecimalFormat("#,###")

    fun updateData(newDealers: List<DealerEntity>) {
        dealers = newDealers
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DealerViewHolder {
        val binding = ItemOutboundDealerBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return DealerViewHolder(binding)
    }

    override fun onBindViewHolder(holder: DealerViewHolder, position: Int) {
        holder.bind(dealers[position])
    }

    override fun getItemCount(): Int = dealers.size

    inner class DealerViewHolder(private val binding: ItemOutboundDealerBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(dealer: DealerEntity) {
            binding.tvDealerName.text = dealer.name
            binding.tvDealerTier.text = "⭐ ${dealer.tier} (CK ${(dealer.discountPercent * 100).toInt()}%)"
            binding.tvDealerAddress.text = "📍 ${dealer.address} • 📞 ${dealer.phone}"
            binding.tvCurrentDebt.text = "${formatter.format(dealer.currentDebt)} đ"
            binding.tvCreditLimit.text = "${formatter.format(dealer.creditLimit)} đ"

            val usagePercent = if (dealer.creditLimit > 0) {
                ((dealer.currentDebt / dealer.creditLimit) * 100).toInt().coerceIn(0, 100)
            } else 0
            binding.pbCreditUsage.progress = usagePercent

            binding.btnCollectDebt.setOnClickListener {
                onCollectDebtClick(dealer)
            }
        }
    }
}

