package com.example.chronovaultwms.product

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.databinding.ItemProductBinding
import java.text.DecimalFormat

class ProductAdapter(
    private var products: List<ProductEntity>,
    private val onItemClick: (ProductEntity) -> Unit
) : RecyclerView.Adapter<ProductAdapter.ProductViewHolder>() {

    private val currencyFormatter = DecimalFormat("#,###")

    inner class ProductViewHolder(private val binding: ItemProductBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(product: ProductEntity) {
            binding.tvBrand.text = product.brand.uppercase()
            binding.tvProductName.text = product.name
            binding.tvProductCode.text = "Mã SKU: ${product.productCode}"
            binding.tvSpecs.text = "${product.caseDiameter} • ${product.movementType} • ${product.waterResistance}"
            binding.tvWholesalePrice.text = "${currencyFormatter.format(product.wholesalePrice)} ₫"
            binding.tvStockBadge.text = "Tồn: ${product.stockQuantity} chiếc"

            binding.root.setOnClickListener {
                onItemClick(product)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val binding = ItemProductBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ProductViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        holder.bind(products[position])
    }

    override fun getItemCount(): Int = products.size

    fun updateList(newList: List<ProductEntity>) {
        products = newList
        notifyDataSetChanged()
    }
}

