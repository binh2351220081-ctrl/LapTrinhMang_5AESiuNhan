package com.example.chronovaultwms.product

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.widget.SearchView
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.chronovaultwms.R
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.DatabaseSeeder
import com.example.chronovaultwms.core.database.ProductDao
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.core.database.SerialDao
import com.example.chronovaultwms.core.database.SerialEntity
import com.example.chronovaultwms.databinding.DialogProductAddBinding
import com.example.chronovaultwms.databinding.DialogProductSerialTimelineBinding
import com.example.chronovaultwms.databinding.FragmentProductListBinding
import com.example.chronovaultwms.databinding.ItemProductTimelineStepBinding
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Phân hệ Quản lý Danh mục Hàng hóa & Serial Number
 * Phụ trách: TV1 - Phan Bá Hải Bình
 * Chức năng: F1.1 (Thêm sản phẩm mới), F1.2 & F1.3 (Tra cứu vòng đời Serial Number Timeline)
 */
class ProductListFragment : Fragment() {

    private var _binding: FragmentProductListBinding? = null
    private val binding get() = _binding!!

    private lateinit var productDao: ProductDao
    private lateinit var serialDao: SerialDao
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
        serialDao = database.serialDao()

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
            // Nạp dữ liệu mẫu gồm 10 mẫu đồng hồ và Serial nếu cơ sở dữ liệu rỗng
            DatabaseSeeder.checkAndSeed(productDao, serialDao)

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
                showSerialTimelineDialog(product)
            }
            .setNegativeButton("Đóng", null)
            .show()
    }

    /**
     * F1.1: Biểu mẫu thêm mới mẫu đồng hồ Luxury vào cơ sở dữ liệu Room
     */
    private fun showAddProductDialog() {
        val dialogBinding = DialogProductAddBinding.inflate(layoutInflater)
        val dialog = AlertDialog.Builder(requireContext())
            .setView(dialogBinding.root)
            .create()

        // Dropdown Thương hiệu
        val brands = arrayOf(
            "Rolex", "Omega", "Patek Philippe", "Audemars Piguet",
            "Cartier", "Grand Seiko", "Tudor", "IWC Schaffhausen", "Hublot", "Breitling"
        )
        val brandAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, brands)
        dialogBinding.actvBrand.setAdapter(brandAdapter)
        dialogBinding.actvBrand.setText(brands[0], false)

        // Dropdown Phân loại
        val categories = arrayOf("Diver", "Chronograph", "Dress", "Luxury Sports", "Complications", "Pilot", "GMT")
        val categoryAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, categories)
        dialogBinding.actvCategory.setAdapter(categoryAdapter)
        dialogBinding.actvCategory.setText(categories[0], false)

        dialogBinding.btnCancel.setOnClickListener {
            dialog.dismiss()
        }

        dialogBinding.btnSaveProduct.setOnClickListener {
            val sku = dialogBinding.etSku.text.toString().trim()
            val name = dialogBinding.etName.text.toString().trim()
            val brand = dialogBinding.actvBrand.text.toString().trim()
            val category = dialogBinding.actvCategory.text.toString().trim()
            val wholesalePriceStr = dialogBinding.etWholesalePrice.text.toString().trim()
            val retailPriceStr = dialogBinding.etRetailPrice.text.toString().trim()
            val stockStr = dialogBinding.etStockQuantity.text.toString().trim()
            val caseDiameter = dialogBinding.etCaseDiameter.text.toString().trim()
            val dialColor = dialogBinding.etDialColor.text.toString().trim()
            val movement = dialogBinding.etMovement.text.toString().trim()
            val waterResistance = dialogBinding.etWaterResistance.text.toString().trim()

            // Validate dữ liệu
            if (sku.isEmpty()) {
                dialogBinding.tilSku.error = "Vui lòng nhập mã SKU"
                return@setOnClickListener
            }
            if (name.isEmpty()) {
                dialogBinding.tilName.error = "Vui lòng nhập tên mẫu đồng hồ"
                return@setOnClickListener
            }
            val wholesalePrice = wholesalePriceStr.toDoubleOrNull()
            if (wholesalePrice == null || wholesalePrice <= 0) {
                dialogBinding.tilWholesalePrice.error = "Giá sỉ không hợp lệ"
                return@setOnClickListener
            }
            val retailPrice = retailPriceStr.toDoubleOrNull() ?: (wholesalePrice * 1.15)
            val stock = stockStr.toIntOrNull() ?: 1

            val newProduct = ProductEntity(
                productCode = sku,
                name = name,
                brand = brand,
                category = category,
                wholesalePrice = wholesalePrice,
                retailPrice = retailPrice,
                stockQuantity = stock,
                caseDiameter = caseDiameter.ifEmpty { "40mm" },
                dialColor = dialColor.ifEmpty { "Đen" },
                movementType = movement.ifEmpty { "Automatic" },
                waterResistance = waterResistance.ifEmpty { "100m" }
            )

            // Tự động tạo 1 Serial khởi tạo cho đồng hồ mới này
            val currentTime = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(Date())
            val cleanSku = sku.replace(Regex("[^A-Za-z0-9]"), "")
            val newSerial = SerialEntity(
                serialNumber = "${cleanSku}-2026-001",
                productCode = sku,
                status = "IN_STOCK",
                currentLocation = "Kệ K1-A01 (Khu Nhập Mới)",
                importDate = currentTime,
                unitCost = wholesalePrice * 0.85,
                supplierName = "$brand International Official",
                dealerName = null,
                qcNotes = "Nhập mới nguyên hộp, thẻ bảo hành điện tử chính hãng"
            )

            viewLifecycleOwner.lifecycleScope.launch {
                withContext(Dispatchers.IO) {
                    productDao.insert(newProduct)
                    serialDao.insert(newSerial)
                    allProducts = productDao.getAllProducts()
                }

                adapter.updateList(allProducts)
                binding.tvTotalCount.text = "Tổng danh mục: ${allProducts.size} mẫu đồng hồ"
                dialog.dismiss()
                Toast.makeText(requireContext(), "✅ Đã thêm thành công: $name", Toast.LENGTH_LONG).show()
            }
        }

        dialog.show()
    }

    /**
     * F1.2 & F1.3: Hộp thoại Tra cứu Timeline Vòng đời Serial Number
     */
    private fun showSerialTimelineDialog(product: ProductEntity) {
        viewLifecycleOwner.lifecycleScope.launch {
            // Truy vấn toàn bộ Serial của đồng hồ này từ Room
            val serialList = withContext(Dispatchers.IO) {
                serialDao.getSerialsByProduct(product.productCode)
            }

            if (serialList.isEmpty()) {
                Toast.makeText(
                    requireContext(),
                    "Chưa có số Serial nào cho mẫu đồng hồ này!",
                    Toast.LENGTH_SHORT
                ).show()
                return@launch
            }

            val dialogBinding = DialogProductSerialTimelineBinding.inflate(layoutInflater)
            val dialog = AlertDialog.Builder(requireContext())
                .setView(dialogBinding.root)
                .create()

            dialogBinding.tvTimelineWatchName.text = product.name
            dialogBinding.tvTimelineSku.text = "Mã SKU: ${product.productCode} • ${product.brand}"

            // Dropdown chọn số Serial
            val serialDisplayList = serialList.map { "${it.serialNumber} (${it.status})" }
            val serialDropdownAdapter = ArrayAdapter(
                requireContext(),
                android.R.layout.simple_dropdown_item_1line,
                serialDisplayList
            )
            dialogBinding.actvSerialSelector.setAdapter(serialDropdownAdapter)
            dialogBinding.actvSerialSelector.setText(serialDisplayList[0], false)

            // Hàm hiển thị Timeline chi tiết cho Serial được chọn
            fun renderTimelineForSerial(serial: SerialEntity) {
                // Badge trạng thái
                when (serial.status) {
                    "IN_STOCK" -> {
                        dialogBinding.tvSerialStatusBadge.text = "IN_STOCK (Đang lưu kho)"
                        dialogBinding.tvSerialStatusBadge.backgroundTintList =
                            ContextCompat.getColorStateList(requireContext(), R.color.badge_stock_bg)
                        dialogBinding.tvSerialStatusBadge.setTextColor(
                            ContextCompat.getColor(requireContext(), R.color.badge_stock_text)
                        )
                    }
                    "ALLOCATED" -> {
                        dialogBinding.tvSerialStatusBadge.text = "ALLOCATED (Đã khóa giữ chỗ)"
                        dialogBinding.tvSerialStatusBadge.backgroundTintList =
                            ContextCompat.getColorStateList(requireContext(), R.color.badge_low_bg)
                        dialogBinding.tvSerialStatusBadge.setTextColor(
                            ContextCompat.getColor(requireContext(), R.color.badge_low_text)
                        )
                    }
                    else -> {
                        dialogBinding.tvSerialStatusBadge.text = "${serial.status} (Đã bàn giao)"
                        dialogBinding.tvSerialStatusBadge.backgroundTintList =
                            ContextCompat.getColorStateList(requireContext(), R.color.primary)
                        dialogBinding.tvSerialStatusBadge.setTextColor(
                            ContextCompat.getColor(requireContext(), R.color.white)
                        )
                    }
                }

                dialogBinding.tvSerialLocation.text = "📍 Vị trí kệ: ${serial.currentLocation}"
                dialogBinding.tvSerialCost.text =
                    "💰 Giá vốn đích danh: %,.0f ₫ (gồm thuế + BH)".format(serial.unitCost)
                dialogBinding.tvSerialQc.text = "🛡️ Thẩm định QC: ${serial.qcNotes}"

                // Dựng 6 bước Timeline vận hành WMS
                dialogBinding.layoutTimelineSteps.removeAllViews()

                val steps = listOf(
                    Triple(
                        "1. 📦 Nhập Khẩu Quốc Tế & Thông Quan",
                        serial.importDate,
                        "Vận chuyển đường hàng không chuyên dụng từ ${serial.supplierName}. Kiểm tra niêm phong hải quan hợp lệ."
                    ),
                    Triple(
                        "2. 🔍 Thẩm Định Kỹ Thuật & Giám Định Máy",
                        serial.importDate,
                        "${serial.qcNotes}. Đo sai số máy điện tử, kiểm tra áp suất chống nước đạt chuẩn."
                    ),
                    Triple(
                        "3. 📍 Nhập Kho & Phân Bổ Ngăn Kệ Vật Lý",
                        serial.importDate,
                        "Đã lưu trữ an toàn tại vị trí ${serial.currentLocation}. Kích hoạt mã định danh RFID/Barcode theo dõi."
                    ),
                    Triple(
                        "4. 🔒 Khóa Hàng Giữ Chỗ Đơn Sỉ B2B (Allocation)",
                        if (serial.status == "ALLOCATED" || serial.status == "DELIVERED") "Đã xác nhận" else "Sẵn sàng",
                        if (serial.dealerName != null) "Đã khóa tự động giữ chỗ cho: ${serial.dealerName}." else "Hàng khả dụng sẵn sàng phân bổ cho các đại lý bán buôn."
                    ),
                    Triple(
                        "5. 🚚 Quét Barcode Xuất Bến & Bàn Giao Vận Chuyển",
                        if (serial.status == "DELIVERED") "Hoàn thành" else "Chờ xuất bến",
                        if (serial.status == "DELIVERED") "Đã quét xuất kho Serial ${serial.serialNumber}, bàn giao xe vận tải có niêm phong bảo mật." else "Đang chờ lệnh xuất kho và phiếu xuất kho được duyệt."
                    ),
                    Triple(
                        "6. 🛡️ Bàn Giao Đại Lý & Kích Hoạt Bảo Hành Điện Tử",
                        if (serial.status == "DELIVERED") "Đã kích hoạt" else "Chưa kích hoạt",
                        if (serial.status == "DELIVERED") "Đại lý đã ký nhận biên bản bàn giao. Đã kích hoạt bảo hành chính hãng toàn cầu 5 năm." else "Bảo hành sẽ được tự động kích hoạt ngay khi hoàn tất giao hàng."
                    )
                )

                steps.forEachIndexed { index, (title, time, desc) ->
                    val stepBinding = ItemProductTimelineStepBinding.inflate(
                        layoutInflater,
                        dialogBinding.layoutTimelineSteps,
                        false
                    )
                    stepBinding.tvStepTitle.text = title
                    stepBinding.tvStepTime.text = time
                    stepBinding.tvStepDesc.text = desc

                    // Ẩn đường kẻ ở bước cuối cùng
                    if (index == steps.size - 1) {
                        stepBinding.viewTimelineLine.visibility = View.INVISIBLE
                    }

                    // Đổi màu bước đã hoàn thành
                    val isCompleted = when (index) {
                        0, 1, 2 -> true
                        3 -> serial.status == "ALLOCATED" || serial.status == "DELIVERED"
                        4, 5 -> serial.status == "DELIVERED"
                        else -> false
                    }

                    if (isCompleted) {
                        stepBinding.viewTimelineDot.backgroundTintList =
                            ContextCompat.getColorStateList(requireContext(), R.color.accent_gold)
                        stepBinding.tvStepTitle.setTextColor(
                            ContextCompat.getColor(requireContext(), R.color.primary)
                        )
                    } else {
                        stepBinding.viewTimelineDot.backgroundTintList =
                            ContextCompat.getColorStateList(requireContext(), R.color.border_color)
                        stepBinding.tvStepTitle.setTextColor(
                            ContextCompat.getColor(requireContext(), R.color.text_secondary)
                        )
                    }

                    dialogBinding.layoutTimelineSteps.addView(stepBinding.root)
                }
            }

            // Render mặc định cho Serial đầu tiên
            renderTimelineForSerial(serialList[0])

            // Lắng nghe sự kiện chọn Serial khác trong Dropdown
            dialogBinding.actvSerialSelector.setOnItemClickListener { _, _, position, _ ->
                renderTimelineForSerial(serialList[position])
            }

            dialogBinding.btnCloseTimeline.setOnClickListener {
                dialog.dismiss()
            }

            dialog.show()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
