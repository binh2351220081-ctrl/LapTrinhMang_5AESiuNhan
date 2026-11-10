package com.example.chronovaultwms.product

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.widget.SearchView
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.DatabaseSeeder
import com.example.chronovaultwms.core.database.ProductDao
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.databinding.FragmentProductListBinding
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * Phân hệ Quản lý Danh mục Đồng hồ & Serial Number
 * Phụ trách: TV1 - Phan Bá Hải Bình
 * Chức năng: F1.1 - F1.9 (Tra cứu đồng hồ, Thông số kỹ thuật, Timeline vòng đời Serial, In mã vạch)
 */
class ProductListFragment : Fragment() {

    private var _binding: FragmentProductListBinding? = null
    private val binding get() = _binding!!

    private lateinit var productDao: ProductDao
    private lateinit var adapter: ProductAdapter
    private var allProducts: List<ProductEntity> = emptyList()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentProductListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Khởi tạo Database DAO
        val database = ChronoVaultDatabase.getInstance(requireContext())
        productDao = database.productDao()

        setupRecyclerView()
        setupSearch()
        setupListeners()

        // Tải dữ liệu từ Room Database
        loadProducts()
    }

    private fun setupRecyclerView() {
        adapter = ProductAdapter(emptyList()) { product ->
            showProductDetailDialog(product)
        }
        binding.rvProducts.layoutManager = LinearLayoutManager(requireContext())
        binding.rvProducts.adapter = adapter
    }

    private fun setupSearch() {
        binding.searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String?): Boolean {
                filterProducts(query)
                return true
            }

            override fun onQueryTextChange(newText: String?): Boolean {
                filterProducts(newText)
                return true
            }
        })
    }

    private fun setupListeners() {
        binding.tvFilterReset.setOnClickListener {
            binding.searchView.setQuery("", false)
            adapter.updateList(allProducts)
            binding.tvTotalCount.text = "Tổng danh mục: ${allProducts.size} mẫu đồng hồ"
        }

        binding.fabAddProduct.setOnClickListener {
            showAddProductDialog()
        }
    }

    private fun loadProducts() {
        viewLifecycleOwner.lifecycleScope.launch {
            // Nạp sẵn 10 mẫu đồng hồ xa xỉ mẫu nếu CSDL rỗng lần đầu
            DatabaseSeeder.checkAndSeed(productDao)

            // Lấy danh sách sản phẩm từ Room
            allProducts = withContext(Dispatchers.IO) {
                productDao.getAllProducts()
            }

            adapter.updateList(allProducts)
            binding.tvTotalCount.text = "Tổng danh mục: ${allProducts.size} mẫu đồng hồ"
        }
    }

    private fun filterProducts(query: String?) {
        if (query.isNullOrBlank()) {
            adapter.updateList(allProducts)
            binding.tvTotalCount.text = "Tổng danh mục: ${allProducts.size} mẫu đồng hồ"
        } else {
            val filtered = allProducts.filter {
                it.name.contains(query, ignoreCase = true) ||
                it.productCode.contains(query, ignoreCase = true) ||
                it.brand.contains(query, ignoreCase = true)
            }
            adapter.updateList(filtered)
            binding.tvTotalCount.text = "Tìm thấy: ${filtered.size} kết quả"
        }
    }

    private fun showProductDetailDialog(product: ProductEntity) {
        val details = """
            • Thương hiệu: ${product.brand}
            • Phân loại: ${product.category}
            • Mã SKU: ${product.productCode}
            • Đường kính mặt: ${product.caseDiameter}
            • Màu mặt số: ${product.dialColor}
            • Bộ máy: ${product.movementType}
            • Chống nước: ${product.waterResistance}
            • Tồn kho: ${product.stockQuantity} chiếc
            • Giá sỉ B2B: %,.0f ₫
            • Giá niêm yết hãng: %,.0f ₫
        """.trimIndent().format(product.wholesalePrice, product.retailPrice)

        MaterialAlertDialogBuilder(requireContext())
            .setTitle(product.name)
            .setMessage(details)
            .setPositiveButton("Xem Serial Timeline (F1.3)") { _, _ ->
                Toast.makeText(
                    requireContext(),
                    "Mở dòng thời gian ${product.stockQuantity} Serials của ${product.productCode}",
                    Toast.LENGTH_SHORT
                ).show()
            }
            .setNegativeButton("Đóng", null)
            .show()
    }

    private fun showAddProductDialog() {
        Toast.makeText(requireContext(), "Mở biểu mẫu Thêm Mới Đồng Hồ (F1.1)", Toast.LENGTH_SHORT).show()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
