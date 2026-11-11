package com.example.chronovaultwms.outbound

import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.core.widget.addTextChangedListener
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.chronovaultwms.R
import com.example.chronovaultwms.core.database.AuditLogEntity
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.DatabaseSeeder
import com.example.chronovaultwms.core.database.DealerEntity
import com.example.chronovaultwms.core.database.DealerReceiptEntity
import com.example.chronovaultwms.core.database.OutboundOrderEntity
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.databinding.DialogCreateOutboundOrderBinding
import com.example.chronovaultwms.databinding.DialogDispatchOrderBinding
import com.example.chronovaultwms.databinding.DialogReceiptVoucherBinding
import com.example.chronovaultwms.databinding.FragmentOutboundOrderBinding
import com.example.chronovaultwms.product.ProductListFragment
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.DecimalFormat
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Phân hệ 3: Quản lý Khách Sỉ & Bán Sỉ - Phân Phối Xuất Hàng
 * Phụ trách: TV3 - Tô Đức Thảo (Operations Staff)
 * Các tính năng trọng tâm:
 *   1. Quản lý danh bạ Đại lý B2B & Hạn mức tín dụng (Credit Limit Enforcement)
 *   2. Khởi tạo Đơn bán sỉ, tự động chiết khấu & Khóa giữ chỗ tồn kho (Inventory Reservation)
 *   3. Quy trình Xuất kho 2 bước & Quét Serial Camera đối soát thời gian thực
 *   4. Lập Phiếu Thu tiền nợ đại lý & Khôi phục hạn mức nợ
 */
class OutboundOrderFragment : Fragment() {

    private var _binding: FragmentOutboundOrderBinding? = null
    private val binding get() = _binding!!

    private lateinit var database: ChronoVaultDatabase
    private val formatter = DecimalFormat("#,###")

    private var currentTab = "ORDERS" // "ORDERS" or "DEALERS"
    private var allDealers = listOf<DealerEntity>()
    private var allOrders = listOf<OutboundOrderEntity>()
    private var allProducts = listOf<ProductEntity>()

    private lateinit var orderAdapter: OutboundOrderAdapter
    private lateinit var dealerAdapter: DealerAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentOutboundOrderBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        database = ChronoVaultDatabase.getInstance(requireContext())

        setupAdapters()
        setupListeners()
        loadData()
    }

    private fun setupAdapters() {
        orderAdapter = OutboundOrderAdapter(emptyList()) { order ->
            if (order.status == "RESERVED") {
                showDispatchOrderDialog(order)
            } else if (order.status == "COMPLETED") {
                showCompletedOrderDetail(order)
            }
        }

        dealerAdapter = DealerAdapter(emptyList()) { dealer ->
            showReceiptVoucherDialog(dealer)
        }

        binding.rvOutboundContent.layoutManager = LinearLayoutManager(requireContext())
        binding.rvOutboundContent.adapter = orderAdapter
    }

    private fun setupListeners() {
        binding.btnBackToProducts.setOnClickListener {
            parentFragmentManager.beginTransaction()
                .replace(R.id.fragmentContainer, ProductListFragment())
                .commit()
        }

        binding.tabOrders.setOnClickListener {
            switchTab("ORDERS")
        }

        binding.tabDealers.setOnClickListener {
            switchTab("DEALERS")
        }

        binding.fabCreateOrder.setOnClickListener {
            showCreateOrderDialog()
        }
    }

    private fun switchTab(tab: String) {
        currentTab = tab
        if (tab == "ORDERS") {
            binding.tabOrders.setBackgroundColor(Color.parseColor("#D4AF37"))
            binding.tabOrders.setTextColor(Color.parseColor("#0F1722"))
            binding.tabDealers.setBackgroundColor(Color.TRANSPARENT)
            binding.tabDealers.setTextColor(Color.WHITE)
            binding.rvOutboundContent.adapter = orderAdapter
            binding.fabCreateOrder.visibility = View.VISIBLE
        } else {
            binding.tabDealers.setBackgroundColor(Color.parseColor("#D4AF37"))
            binding.tabDealers.setTextColor(Color.parseColor("#0F1722"))
            binding.tabOrders.setBackgroundColor(Color.TRANSPARENT)
            binding.tabOrders.setTextColor(Color.WHITE)
            binding.rvOutboundContent.adapter = dealerAdapter
            binding.fabCreateOrder.visibility = View.GONE
        }
    }

    private fun loadData() {
        lifecycleScope.launch(Dispatchers.IO) {
            // Seed sample data if empty
            DatabaseSeeder.checkAndSeed(
                database.productDao(),
                database.serialDao(),
                database.userDao(),
                database.auditLogDao(),
                database.dealerDao(),
                database.outboundOrderDao(),
                database.dealerReceiptDao()
            )

            allDealers = database.dealerDao().getAllDealers()
            allOrders = database.outboundOrderDao().getAllOrders()
            allProducts = database.productDao().getAllProducts()

            withContext(Dispatchers.Main) {
                orderAdapter.updateData(allOrders)
                dealerAdapter.updateData(allDealers)
                updateKpis()
            }
        }
    }

    private fun updateKpis() {
        val totalOrders = allOrders.size
        val totalDebt = allDealers.sumOf { it.currentDebt }
        val reservedItems = allOrders.filter { it.status == "RESERVED" }.sumOf { it.convertedQuantity }

        binding.tvKpiTotalOrders.text = "$totalOrders Đơn"
        binding.tvKpiTotalDebt.text = "${(totalDebt / 1_000_000_000.0).format(2)} Tỷ đ"
        binding.tvKpiReservedItems.text = "$reservedItems Chiếc"
    }

    private fun Double.format(digits: Int) = String.format(Locale.US, "%.${digits}f", this)

    /**
     * F3.2.1 - F3.2.6: Khởi tạo đơn bán sỉ & Thẩm định Hạn mức nợ tự động (Credit Limit)
     */
    private fun showCreateOrderDialog() {
        if (allDealers.isEmpty() || allProducts.isEmpty()) {
            Toast.makeText(requireContext(), "Dữ liệu đang tải, vui lòng thử lại!", Toast.LENGTH_SHORT).show()
            return
        }

        val dialogBinding = DialogCreateOutboundOrderBinding.inflate(layoutInflater)
        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setView(dialogBinding.root)
            .create()

        val dealerNames = allDealers.map { "${it.name} (${it.tier} - CK ${(it.discountPercent * 100).toInt()}%)" }
        val productNames = allProducts.map { "${it.name} - Tồn: ${it.stockQuantity}" }
        val units = listOf("Chiếc lẻ (Piece)", "Thùng/Kiện (Box - 10 chiếc)")

        dialogBinding.spDealer.adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, dealerNames)
        dialogBinding.spProduct.adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, productNames)
        dialogBinding.spUnit.adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, units)

        fun recalculate(): Boolean {
            val dealer = allDealers.getOrNull(dialogBinding.spDealer.selectedItemPosition) ?: return false
            val product = allProducts.getOrNull(dialogBinding.spProduct.selectedItemPosition) ?: return false
            val isBox = dialogBinding.spUnit.selectedItemPosition == 1
            val qty = dialogBinding.etQuantity.text.toString().toIntOrNull() ?: 1
            val convertedQty = if (isBox) qty * 10 else qty

            val unitPrice = product.wholesalePrice
            val discountRate = dealer.discountPercent
            val finalUnitPrice = unitPrice * (1.0 - discountRate)
            val totalAmount = finalUnitPrice * convertedQty

            val deposit = dialogBinding.etDepositAmount.text.toString().toDoubleOrNull() ?: 0.0
            val remainingDebt = (totalAmount - deposit).coerceAtLeast(0.0)
            val projectedDebt = dealer.currentDebt + remainingDebt
            val isOverLimit = projectedDebt > dealer.creditLimit

            dialogBinding.tvCalcPreview.text = "Số lượng quy đổi: $convertedQty chiếc\n" +
                    "Đơn giá gốc: ${formatter.format(unitPrice)} đ/chiếc\n" +
                    "Chiết khấu (${(discountRate * 100).toInt()}%): -${formatter.format(unitPrice * discountRate)} đ/chiếc\n" +
                    "Đơn giá sau CK: ${formatter.format(finalUnitPrice)} đ/chiếc\n" +
                    "Tổng giá trị đơn: ${formatter.format(totalAmount)} đ\n" +
                    "Công nợ phát sinh: ${formatter.format(remainingDebt)} đ\n" +
                    "Dư nợ dự kiến sau đơn: ${formatter.format(projectedDebt)} đ (Hạn mức: ${formatter.format(dealer.creditLimit)} đ)"

            if (isOverLimit) {
                dialogBinding.tvCreditCheckWarning.text = "⚠️ CẢNH BÁO: ĐẠI LÝ VƯỢT HẠN MỨC NỢ! (${formatter.format(projectedDebt)} > ${formatter.format(dealer.creditLimit)} đ). Cần thanh toán nợ cũ!"
                dialogBinding.tvCreditCheckWarning.setBackgroundColor(Color.parseColor("#FEE2E2"))
                dialogBinding.tvCreditCheckWarning.setTextColor(Color.parseColor("#DC2626"))
                dialogBinding.btnSubmitOrder.isEnabled = false
            } else {
                dialogBinding.tvCreditCheckWarning.text = "✓ Hợp lệ: Dư nợ nằm trong Hạn mức Tín dụng cho phép."
                dialogBinding.tvCreditCheckWarning.setBackgroundColor(Color.parseColor("#ECFDF5"))
                dialogBinding.tvCreditCheckWarning.setTextColor(Color.parseColor("#059669"))
                dialogBinding.btnSubmitOrder.isEnabled = true
            }

            return !isOverLimit
        }

        dialogBinding.spDealer.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(p0: AdapterView<*>?, p1: View?, p2: Int, p3: Long) { recalculate() }
            override fun onNothingSelected(p0: AdapterView<*>?) {}
        }
        dialogBinding.spProduct.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(p0: AdapterView<*>?, p1: View?, p2: Int, p3: Long) { recalculate() }
            override fun onNothingSelected(p0: AdapterView<*>?) {}
        }
        dialogBinding.spUnit.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(p0: AdapterView<*>?, p1: View?, p2: Int, p3: Long) { recalculate() }
            override fun onNothingSelected(p0: AdapterView<*>?) {}
        }
        dialogBinding.etQuantity.addTextChangedListener { recalculate() }
        dialogBinding.etDepositAmount.addTextChangedListener { recalculate() }

        recalculate()

        dialogBinding.btnCancelOrder.setOnClickListener { dialog.dismiss() }
        dialogBinding.btnSubmitOrder.setOnClickListener {
            val dealer = allDealers[dialogBinding.spDealer.selectedItemPosition]
            val product = allProducts[dialogBinding.spProduct.selectedItemPosition]
            val isBox = dialogBinding.spUnit.selectedItemPosition == 1
            val qty = dialogBinding.etQuantity.text.toString().toIntOrNull() ?: 1
            val convertedQty = if (isBox) qty * 10 else qty

            // Kiểm tra tồn kho khả dụng (Available Stock)
            lifecycleScope.launch(Dispatchers.IO) {
                val reservedNow = database.outboundOrderDao().getReservedQuantity(product.productCode)
                val available = product.stockQuantity - reservedNow

                if (convertedQty > available) {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(
                            requireContext(),
                            "Lỗi: Số lượng đặt ($convertedQty) vượt quá tồn khả dụng ($available chiếc)!",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                    return@launch
                }

                val unitPrice = product.wholesalePrice
                val discountRate = dealer.discountPercent
                val finalUnitPrice = unitPrice * (1.0 - discountRate)
                val totalAmount = finalUnitPrice * convertedQty
                val deposit = dialogBinding.etDepositAmount.text.toString().toDoubleOrNull() ?: 0.0
                val remainingDebt = (totalAmount - deposit).coerceAtLeast(0.0)

                val newOrderCode = "DS-2026-00${allOrders.size + 1}"
                val currentTime = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(Date())

                val newOrder = OutboundOrderEntity(
                    orderCode = newOrderCode,
                    dealerId = dealer.dealerId,
                    dealerName = dealer.name,
                    productCode = product.productCode,
                    productName = product.name,
                    unit = if (isBox) "BOX" else "PIECE",
                    quantity = qty,
                    convertedQuantity = convertedQty,
                    unitPrice = unitPrice,
                    discountPercent = discountRate,
                    totalAmount = totalAmount,
                    depositAmount = deposit,
                    remainingDebt = remainingDebt,
                    status = "RESERVED",
                    createdDate = currentTime
                )

                database.outboundOrderDao().insert(newOrder)

                // Ghi vết Audit Log
                database.auditLogDao().insert(
                    AuditLogEntity(
                        timestamp = currentTime,
                        actorName = "Tô Đức Thảo",
                        role = "OPERATIONS_STAFF",
                        action = "DUYỆT_ĐƠN_SỈ_GIỮ_CHỖ",
                        details = "Duyệt đơn sỉ $newOrderCode cho ${dealer.name}: $convertedQty chiếc ${product.name} (Khóa giữ chỗ: $convertedQty chiếc).",
                        ipAddress = "192.168.1.103 - Outbound Terminal"
                    )
                )

                withContext(Dispatchers.Main) {
                    dialog.dismiss()
                    Toast.makeText(requireContext(), "✓ Đã duyệt đơn $newOrderCode và khóa giữ chỗ thành công!", Toast.LENGTH_SHORT).show()
                    loadData()
                }
            }
        }

        dialog.show()
    }

    /**
     * F3.2.9 - F3.2.10: Quy trình Quét Serial Đóng Kiện & Xác Nhận Xuất Kho B2B
     */
    private fun showDispatchOrderDialog(order: OutboundOrderEntity) {
        val dialogBinding = DialogDispatchOrderBinding.inflate(layoutInflater)
        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setView(dialogBinding.root)
            .create()

        dialogBinding.tvDispatchOrderHeader.text = "Đơn sỉ: ${order.orderCode} • Đại lý: ${order.dealerName}"
        dialogBinding.tvDispatchProductInfo.text = "Sản phẩm: ${order.productName} (${order.productCode})"
        dialogBinding.tvDispatchRequiredQty.text = "Số lượng xuất kho: ${order.convertedQuantity} chiếc lẻ (Cần quét đủ ${order.convertedQuantity} mã Serial)"

        val scannedSerials = mutableListOf<String>()

        lifecycleScope.launch(Dispatchers.IO) {
            val inStockSerials = database.serialDao().getSerialsByProduct(order.productCode)
                .filter { it.status == "IN_STOCK" }
                .map { it.serialNumber }

            withContext(Dispatchers.Main) {
                if (inStockSerials.isNotEmpty()) {
                    dialogBinding.tvAvailableSerialsHint.text = "💡 Gợi ý Serial trên kệ: ${inStockSerials.take(3).joinToString(", ")}"
                } else {
                    dialogBinding.tvAvailableSerialsHint.text = "⚠️ Chưa có mã Serial khả dụng trong kho cho mã này."
                }
            }
        }

        fun updateScannedUI() {
            dialogBinding.tvScannedCountStatus.text = "Danh Sách Serial Đã Quét (${scannedSerials.size}/${order.convertedQuantity}):"
            if (scannedSerials.isEmpty()) {
                dialogBinding.tvScannedList.text = "Chưa quét mã Serial nào..."
            } else {
                dialogBinding.tvScannedList.text = scannedSerials.mapIndexed { idx, s -> "${idx + 1}. ✓ $s (Đích danh - Hàng Mới)" }.joinToString("\n")
            }
            dialogBinding.btnConfirmDispatch.isEnabled = scannedSerials.size == order.convertedQuantity
        }

        updateScannedUI()

        dialogBinding.btnAddSerial.setOnClickListener {
            val input = dialogBinding.etSerialInput.text.toString().trim()
            if (input.isEmpty()) {
                Toast.makeText(requireContext(), "Vui lòng nhập hoặc quét mã Serial!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            if (scannedSerials.contains(input)) {
                Toast.makeText(requireContext(), "Mã Serial $input đã được quét rồi!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            if (scannedSerials.size >= order.convertedQuantity) {
                Toast.makeText(requireContext(), "Đã quét đủ số lượng cần xuất!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            lifecycleScope.launch(Dispatchers.IO) {
                val serialEntity = database.serialDao().getSerialByNumber(input)
                withContext(Dispatchers.Main) {
                    if (serialEntity == null) {
                        Toast.makeText(requireContext(), "Lỗi: Không tìm thấy Serial $input trong hệ thống!", Toast.LENGTH_SHORT).show()
                    } else if (serialEntity.productCode != order.productCode) {
                        Toast.makeText(requireContext(), "Lỗi: Serial này thuộc mã SKU ${serialEntity.productCode}, không khớp với đơn hàng!", Toast.LENGTH_SHORT).show()
                    } else if (serialEntity.status == "DISPATCHED" || serialEntity.status == "DEFECTIVE") {
                        Toast.makeText(requireContext(), "Lỗi: Serial $input có trạng thái ${serialEntity.status}, không được phép xuất sỉ!", Toast.LENGTH_SHORT).show()
                    } else {
                        scannedSerials.add(input)
                        dialogBinding.etSerialInput.setText("")
                        updateScannedUI()
                        Toast.makeText(requireContext(), "✓ Đã nhận diện Serial $input", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }

        dialogBinding.btnCloseDispatch.setOnClickListener { dialog.dismiss() }

        dialogBinding.btnConfirmDispatch.setOnClickListener {
            if (scannedSerials.size < order.convertedQuantity) {
                Toast.makeText(requireContext(), "Chưa quét đủ số lượng Serial!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            lifecycleScope.launch(Dispatchers.IO) {
                val currentTime = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(Date())

                // 1. Cập nhật trạng thái Serial sang DISPATCHED (ĐÃ BÁN)
                scannedSerials.forEach { sn ->
                    val s = database.serialDao().getSerialByNumber(sn)
                    if (s != null) {
                        database.serialDao().update(
                            s.copy(
                                status = "DISPATCHED",
                                dealerName = order.dealerName
                            )
                        )
                    }
                }

                // 2. Cập nhật Order sang COMPLETED
                database.outboundOrderDao().markCompleted(
                    orderCode = order.orderCode,
                    serials = scannedSerials.joinToString(", ")
                )

                // 3. Tăng công nợ của đại lý tương ứng với remainingDebt
                val dealer = database.dealerDao().getDealerById(order.dealerId)
                if (dealer != null) {
                    val newDebt = dealer.currentDebt + order.remainingDebt
                    database.dealerDao().updateDebt(dealer.dealerId, newDebt)
                }

                // 4. Trừ tồn kho vật lý của Product
                val product = database.productDao().getProductByCode(order.productCode)
                if (product != null) {
                    val newStock = (product.stockQuantity - order.convertedQuantity).coerceAtLeast(0)
                    database.productDao().updateProduct(product.copy(stockQuantity = newStock))
                }

                // 5. Ghi Audit Log
                database.auditLogDao().insert(
                    AuditLogEntity(
                        timestamp = currentTime,
                        actorName = "Tô Đức Thảo",
                        role = "OPERATIONS_STAFF",
                        action = "XUẤT_KHO_B2B_HOÀN_TẤT",
                        details = "Hoàn tất đóng kiện xuất sỉ đơn ${order.orderCode} giao ${order.dealerName}. Đã xuất ${scannedSerials.size} Serial: ${scannedSerials.joinToString(", ")}.",
                        ipAddress = "192.168.1.103 - Dispatch Terminal"
                    )
                )

                withContext(Dispatchers.Main) {
                    dialog.dismiss()
                    Toast.makeText(requireContext(), "✓ Xuất kho thành công đơn ${order.orderCode}!", Toast.LENGTH_LONG).show()
                    loadData()
                }
            }
        }

        dialog.show()
    }

    /**
     * F3.1.5: Lập Phiếu Thu tiền nợ Đại lý (Receipt Voucher)
     */
    private fun showReceiptVoucherDialog(dealer: DealerEntity) {
        val dialogBinding = DialogReceiptVoucherBinding.inflate(layoutInflater)
        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setView(dialogBinding.root)
            .create()

        dialogBinding.tvReceiptDealerInfo.text = "Đại lý: ${dealer.name}\nDư nợ hiện tại: ${formatter.format(dealer.currentDebt)} đ (Hạn mức: ${formatter.format(dealer.creditLimit)} đ)"

        val methods = listOf("Chuyển Khoản Ngân Hàng (Ủy Nhiệm Chi)", "Tiền Mặt Tại Quầy")
        dialogBinding.spPaymentMethod.adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, methods)

        dialogBinding.btnCancelReceipt.setOnClickListener { dialog.dismiss() }

        dialogBinding.btnSubmitReceipt.setOnClickListener {
            val amount = dialogBinding.etReceiptAmount.text.toString().toDoubleOrNull() ?: 0.0
            if (amount <= 0) {
                Toast.makeText(requireContext(), "Vui lòng nhập số tiền hợp lệ!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            if (amount > dealer.currentDebt) {
                Toast.makeText(requireContext(), "Số tiền thu không được lớn hơn dư nợ hiện tại (${formatter.format(dealer.currentDebt)} đ)!", Toast.LENGTH_LONG).show()
                return@setOnClickListener
            }

            val method = if (dialogBinding.spPaymentMethod.selectedItemPosition == 0) "CHUYEN_KHOAN" else "TIEN_MAT"
            val refDoc = dialogBinding.etReferenceDoc.text.toString().trim()
            val note = dialogBinding.etReceiptNote.text.toString().trim()
            val currentTime = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault()).format(Date())
            val receiptId = "PT-2026-00${(10..99).random()}"

            lifecycleScope.launch(Dispatchers.IO) {
                // 1. Tạo Phiếu Thu
                val receipt = DealerReceiptEntity(
                    receiptId = receiptId,
                    dealerId = dealer.dealerId,
                    dealerName = dealer.name,
                    amount = amount,
                    paymentMethod = method,
                    referenceDoc = refDoc,
                    date = currentTime,
                    note = note
                )
                database.dealerReceiptDao().insert(receipt)

                // 2. Cập nhật giảm dư nợ của Đại lý
                val newDebt = dealer.currentDebt - amount
                database.dealerDao().updateDebt(dealer.dealerId, newDebt)

                // 3. Ghi vết Audit Log
                database.auditLogDao().insert(
                    AuditLogEntity(
                        timestamp = currentTime,
                        actorName = "Tô Đức Thảo",
                        role = "OPERATIONS_STAFF",
                        action = "LẬP_PHIẾU_THU_NỢ_SỈ",
                        details = "Lập phiếu thu $receiptId: Thu ${formatter.format(amount)} đ từ đại lý ${dealer.name} qua $method ($refDoc). Dư nợ còn lại: ${formatter.format(newDebt)} đ.",
                        ipAddress = "192.168.1.103 - Outbound Terminal"
                    )
                )

                withContext(Dispatchers.Main) {
                    dialog.dismiss()
                    Toast.makeText(requireContext(), "✓ Đã thu ${formatter.format(amount)} đ từ ${dealer.name}. Khôi phục hạn mức mua hàng!", Toast.LENGTH_LONG).show()
                    loadData()
                }
            }
        }

        dialog.show()
    }

    private fun showCompletedOrderDetail(order: OutboundOrderEntity) {
        MaterialAlertDialogBuilder(requireContext())
            .setTitle("BIÊN BẢN BÀN GIAO KIÊM PHIẾU XUẤT KHO B2B")
            .setMessage(
                "Mã phiếu xuất: ${order.orderCode}\n" +
                "Đại lý nhận hàng: ${order.dealerName}\n" +
                "Ngày giờ xuất kho: ${order.createdDate}\n" +
                "Mẫu đồng hồ: ${order.productName}\n" +
                "Số lượng bàn giao: ${order.convertedQuantity} chiếc lẻ\n" +
                "Tổng giá trị đơn: ${formatter.format(order.totalAmount)} đ\n" +
                "Đã đặt cọc: ${formatter.format(order.depositAmount)} đ\n" +
                "Công nợ hạch toán: ${formatter.format(order.remainingDebt)} đ\n\n" +
                "📋 DANH SÁCH SERIAL ĐÍCH DANH ĐÃ XUẤT GIAO:\n${order.dispatchedSerials}\n\n" +
                "Chứng từ có giá trị pháp lý và kích hoạt bảo hành chính hãng toàn cầu."
            )
            .setPositiveButton("Đóng", null)
            .show()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
