package com.example.chronovaultwms.outbound

import android.graphics.Typeface
import android.media.AudioManager
import android.media.ToneGenerator
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.InputType
import android.view.HapticFeedbackConstants
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.core.widget.addTextChangedListener
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.chronovaultwms.R
import com.example.chronovaultwms.core.auth.SessionManager
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.DealerEntity
import com.example.chronovaultwms.core.database.OutboundOrderEntity
import com.example.chronovaultwms.databinding.FragmentOutboundOrderBinding
import com.example.chronovaultwms.product.ProductListFragment
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.mlkit.vision.codescanner.GmsBarcodeScanning
import java.text.NumberFormat
import java.text.Normalizer
import java.util.Locale

/** TV3 warehouse operations. The repository owns persistence and permission checks. */
class OutboundOrderFragment : Fragment() {
    private var _binding: FragmentOutboundOrderBinding? = null
    private val binding get() = _binding!!
    private lateinit var model: OutboundViewModel
    private lateinit var session: SessionManager
    private lateinit var orderAdapter: OutboundOrderAdapter
    private lateinit var dealerAdapter: DealerAdapter
    private var state: OutboundState? = null
    private var showingUnits = false
    private var statusCodes = listOf("")
    private val dialogs = mutableSetOf<AlertDialog>()
    private val pending = mutableMapOf<Int, (OutboundUiResult) -> Unit>()
    private val money = NumberFormat.getNumberInstance(Locale.forLanguageTag("vi-VN"))

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentOutboundOrderBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        session = SessionManager(requireContext())
        model = ViewModelProvider(this)[OutboundViewModel::class.java]
        orderAdapter = OutboundOrderAdapter(emptyList(), ::showOrder)
        dealerAdapter = DealerAdapter(emptyList(), ::showDealer)
        binding.rvOutboundContent.layoutManager = LinearLayoutManager(requireContext())
        binding.rvOutboundContent.adapter = orderAdapter
        binding.btnBackToProducts.setOnClickListener {
            if (!parentFragmentManager.popBackStackImmediate()) parentFragmentManager.beginTransaction().replace(R.id.fragmentContainer, ProductListFragment()).commit()
        }
        binding.btnRefreshOutbound.setOnClickListener { model.refresh() }
        binding.btnSyncOutbound.setOnClickListener {
            OutboundSyncSettings.show(requireContext(), ChronoVaultDatabase.getInstance(requireContext()), actor()) { model.refresh() }
        }
        binding.tabOrders.setOnClickListener { selectTab(false) }
        binding.tabDealers.setOnClickListener { selectTab(true) }
        binding.btnNewOutbound.setOnClickListener { if (showingUnits) editDealer(null) else createDraft() }
        binding.btnCustomerReturn.setOnClickListener { showReturn() }
        binding.btnOtherDispatch.setOnClickListener { showOtherDispatch() }
        binding.etOutboundSearch.addTextChangedListener { renderList() }
        binding.spOutboundStatus.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, child: View?, position: Int, id: Long) = renderList()
            override fun onNothingSelected(parent: AdapterView<*>?) = Unit
        }
        model.state.observe(viewLifecycleOwner) { data ->
            state = data
            binding.tvKpiTotalOrders.text = "${data.orders.size} lệnh"
            binding.tvKpiCompletedOrders.text = "${data.orders.count { it.status == "COMPLETED" }} đã xuất"
            binding.tvKpiReservedItems.text = "${data.orders.filter { it.status in setOf("RESERVED", "PACKING") }.sumOf { it.convertedQuantity }} giữ chỗ"
            renderList()
        }
        model.busy.observe(viewLifecycleOwner) { busy ->
            binding.progressOutbound.visibility = if (busy) View.VISIBLE else View.GONE
            binding.btnRefreshOutbound.isEnabled = !busy
            binding.btnNewOutbound.isEnabled = !busy && canOperate()
            binding.btnCustomerReturn.isEnabled = !busy && canConfirm()
            binding.btnOtherDispatch.isEnabled = !busy && canConfirm()
            dialogs.forEach { dialog -> dialog.getButton(AlertDialog.BUTTON_POSITIVE)?.isEnabled = !busy && dialog.window?.decorView?.tag != "NO_SUBMIT" }
        }
        model.results.observe(viewLifecycleOwner) { event ->
            if (!event.consume()) return@observe
            if (event.error != null) {
                pending.remove(event.requestId)
                notify(event.error, error = true)
            } else {
                val result = event.result ?: return@observe
                pending.remove(event.requestId)?.invoke(result)
                result.message?.let { notify(it) }
            }
        }
        selectTab(false)
        model.refresh()
    }

    private fun actor() = OutboundActor(session.getFullName().orEmpty(), session.getRole().orEmpty())
    private fun canOperate() = session.isLoggedIn() && session.getRole() in setOf("OPERATIONS_STAFF", "WAREHOUSE_MANAGER", "STORE_OWNER")
    private fun canConfirm() = session.isLoggedIn() && session.getRole() in setOf("WAREHOUSE_MANAGER", "STORE_OWNER")

    private fun selectTab(units: Boolean) {
        showingUnits = units
        binding.btnNewOutbound.text = if (units) "Thêm đơn vị" else "Lập lệnh"
        binding.etOutboundSearch.hint = if (units) "Tìm mã, tên, địa chỉ đơn vị…" else "Tìm mã lệnh, đơn vị, SKU…"
        binding.rvOutboundContent.adapter = if (units) dealerAdapter else orderAdapter
        statusCodes = if (units) listOf("", "ACTIVE", "LOCKED", "SUSPENDED") else listOf("", "DRAFT", "RESERVED", "PACKING", "COMPLETED", "CANCELLED")
        val labels = statusCodes.map { if (it.isEmpty()) "Tất cả trạng thái" else if (units) outboundUnitStatus(it) else outboundOrderStatus(it) }
        binding.spOutboundStatus.adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, labels)
        renderList()
    }

    private fun renderList() {
        val ui = _binding ?: return
        val data = state ?: return
        ui.tvSessionOutbound.text = "${session.getFullName().orEmpty().ifBlank { "Chưa đăng nhập" }} • ${roleLabel(session.getRole().orEmpty())}"
        val query = normalizeSearch(ui.etOutboundSearch.text.toString())
        val status = statusCodes.getOrNull(ui.spOutboundStatus.selectedItemPosition).orEmpty()
        val size = if (showingUnits) {
            val filtered = data.dealers.filter { (status.isEmpty() || it.status == status) && normalizeSearch("${it.dealerId} ${it.name} ${it.address} ${it.taxCode} ${it.phone}").contains(query) }
            dealerAdapter.updateData(filtered); filtered.size
        } else {
            val filtered = data.orders.filter { (status.isEmpty() || it.status == status) && normalizeSearch("${it.orderCode} ${it.dealerName} ${it.productCode} ${it.productName}").contains(query) }
            orderAdapter.updateData(filtered); filtered.size
        }
        ui.tvEmptyOutbound.visibility = if (size == 0) View.VISIBLE else View.GONE
        ui.btnNewOutbound.visibility = if (canOperate()) View.VISIBLE else View.GONE
        ui.btnCustomerReturn.visibility = if (canConfirm()) View.VISIBLE else View.GONE
        ui.btnOtherDispatch.visibility = if (canConfirm()) View.VISIBLE else View.GONE
    }

    private fun showDealer(dealer: DealerEntity) {
        val actions = mutableListOf<Pair<String, () -> Unit>>()
        if (canOperate()) actions += "Sửa hồ sơ" to { editDealer(dealer) }
        if (canConfirm() && dealer.currentDebt > 0) actions += "Lập phiếu thu / Giải phóng bảo lãnh" to { showReceiptDialog(dealer) }
        val msg = "Mã: ${dealer.dealerId}\n${outboundUnitStatus(dealer.status)}\nĐịa chỉ nhận: ${dealer.address}\nNgười liên hệ: ${dealer.representative}\nĐiện thoại: ${dealer.phone}\nEmail: ${dealer.email}\nMã số đơn vị: ${dealer.taxCode}\nDư nợ hiện tại: ${money.format(dealer.currentDebt)} đ / Hạn mức: ${money.format(dealer.creditLimit)} đ"
        MaterialAlertDialogBuilder(requireContext()).setTitle(dealer.name)
            .setMessage(msg)
            .setPositiveButton(if (canOperate()) "Sửa hồ sơ" else "Đóng") { _, _ -> if (canOperate()) editDealer(dealer) }
            .setNegativeButton("Đóng", null)
            .also { builder ->
                if (actions.isNotEmpty()) {
                    builder.setNeutralButton("Thao tác") { _, _ ->
                        MaterialAlertDialogBuilder(requireContext()).setTitle(dealer.name)
                            .setItems(actions.map { it.first }.toTypedArray()) { _, index -> actions[index].second() }.show()
                    }
                }
            }.show()
    }

    private fun showReceiptDialog(dealer: DealerEntity) {
        val form = Form()
        form.label("${dealer.dealerId} · ${dealer.name}", bold = true)
        form.label("Dư nợ hiện tại: ${money.format(dealer.currentDebt)} đ · Hạn mức: ${money.format(dealer.creditLimit)} đ")
        val amount = form.edit("Số tiền thu / giải phóng bảo lãnh *", inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL)
        val method = form.spinner("Hình thức thanh toán", listOf("Chuyển khoản (UNC)", "Tiền mặt"))
        val refDoc = form.edit("Chứng từ tham chiếu / Số UNC *")
        val note = form.edit("Ghi chú thu hồi công nợ")
        formDialog("Phiếu thu tiền sỉ / Giải phóng bảo lãnh", form, "Tạo phiếu thu") { dialog ->
            val amtVal = amount.text.toString().toDoubleOrNull() ?: 0.0
            if (amtVal <= 0.0) { amount.error = "Số tiền phải lớn hơn 0"; return@formDialog }
            if (amtVal > dealer.currentDebt) { amount.error = "Không vượt quá dư nợ (${money.format(dealer.currentDebt)} đ)"; return@formDialog }
            if (required(refDoc)) {
                submit(dialog) { id ->
                    model.recordReceipt(id, dealer.dealerId, amtVal, if (method.selectedItemPosition == 0) "CHUYEN_KHOAN" else "TIEN_MAT", refDoc.text.toString().trim(), note.text.toString().trim(), actor())
                }
            }
        }
    }

    private fun editDealer(existing: DealerEntity?) {
        val form = Form()
        val code = form.edit("Mã đơn vị *", existing?.dealerId.orEmpty()).apply { isEnabled = existing == null }
        val name = form.edit("Tên đơn vị *", existing?.name.orEmpty())
        val address = form.edit("Địa chỉ nhận hàng *", existing?.address.orEmpty(), multiline = true)
        val representative = form.edit("Người liên hệ / nhận hàng *", existing?.representative.orEmpty())
        val phone = form.edit("Điện thoại *", existing?.phone.orEmpty(), inputType = InputType.TYPE_CLASS_PHONE)
        val email = form.edit("Email", existing?.email.orEmpty(), inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_EMAIL_ADDRESS)
        val tax = form.edit("Mã số doanh nghiệp / chi nhánh", existing?.taxCode.orEmpty())
        val statuses = listOf("ACTIVE", "LOCKED", "SUSPENDED")
        val status = form.spinner("Trạng thái tiếp nhận", statuses.map(::outboundUnitStatus)).apply {
            setSelection(statuses.indexOf(existing?.status ?: "ACTIVE").coerceAtLeast(0)); isEnabled = canConfirm()
        }
        if (!canConfirm()) form.label("Thủ kho hoặc chủ kho quyết định tạm khóa/ngừng tiếp nhận.")
        formDialog(if (existing == null) "Thêm đơn vị nhận hàng" else "Sửa đơn vị nhận hàng", form, "Lưu hồ sơ") { dialog ->
            if (required(code, name, address, representative, phone)) {
                val dealer = (existing ?: DealerEntity(code.text.toString().trim().uppercase(Locale.ROOT), "", "BRONZE", 0.0, 0.0, 0.0, "", "", "")).copy(
                    name = name.text.toString().trim(), address = address.text.toString().trim(), phone = phone.text.toString().trim(),
                    representative = representative.text.toString().trim(), email = email.text.toString().trim(), taxCode = tax.text.toString().trim(), status = statuses[status.selectedItemPosition])
                submit(dialog) { id -> model.saveDealer(id, dealer, actor()) }
            }
        }
    }

    private fun createDraft() {
        val data = state ?: return
        val units = data.dealers.filter { it.status == "ACTIVE" }
        val products = data.products.filter { it.status != "DISCONTINUED" }
        if (units.isEmpty() || products.isEmpty()) { notify("Cần có đơn vị nhận đang hoạt động và danh mục hàng."); return }
        val form = Form()
        val dealer = form.spinner("Đơn vị nhận hàng *", units.map { "${it.dealerId} · ${it.name}" })
        val product = form.spinner("Mẫu đồng hồ", products.map { item -> "${item.productCode} · ${item.name} (khả dụng ${data.serials.count { it.productCode == item.productCode && it.status == "IN_STOCK" }})" })
        val productHint = form.label("")
        fun updateProductHint() {
            val item = products[product.selectedItemPosition.coerceAtLeast(0)]
            productHint.text = "Quy cách: 1 thùng = ${item.conversionRate} chiếc. Định mức xuất tối thiểu: ${item.minDispatchQuantity} chiếc."
        }
        product.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, child: View?, position: Int, id: Long) = updateProductHint()
            override fun onNothingSelected(parent: AdapterView<*>?) = Unit
        }
        updateProductHint()
        val unit = form.spinner("Đơn vị tính", listOf("Chiếc", "Thùng / kiện"))
        val quantity = form.edit("Số lượng *", "1", inputType = InputType.TYPE_CLASS_NUMBER)
        val basket = form.label("Chưa có mặt hàng. Thêm ít nhất một dòng để lưu lệnh.")
        val lines = mutableListOf<OutboundLineRequest>()
        val titles = mutableListOf<String>()
        fun redraw() { basket.text = titles.mapIndexed { index, value -> "${index + 1}. $value" }.joinToString("\n").ifBlank { "Chưa có mặt hàng." } }
        form.button("+ Thêm mặt hàng vào lệnh") {
            val selected = products[product.selectedItemPosition]
            val count = quantity.text.toString().toIntOrNull() ?: 0
            if (count <= 0) quantity.error = "Nhập số nguyên lớn hơn 0"
            else if (lines.any { it.productCode == selected.productCode }) notify("Mẫu hàng đã có. Xóa dòng cũ trước khi đổi số lượng.")
            else {
                val box = unit.selectedItemPosition == 1
                val pieces = count.toLong() * if (box) selected.conversionRate else 1
                if (pieces <= 0 || pieces > Int.MAX_VALUE) quantity.error = "Số lượng quy đổi không hợp lệ"
                else { lines.add(OutboundLineRequest(selected.productCode, box, count)); titles.add("${selected.productCode}: $count ${if (box) "thùng × ${selected.conversionRate}" else "chiếc"} = $pieces chiếc"); redraw() }
            }
        }
        form.button("Xóa một dòng đã thêm") {
            if (lines.isNotEmpty()) MaterialAlertDialogBuilder(requireContext()).setTitle("Chọn dòng cần xóa").setItems(titles.toTypedArray()) { _, index -> lines.removeAt(index); titles.removeAt(index); redraw() }.show()
        }
        val note = form.edit("Lý do / yêu cầu xuất *", multiline = true)
        form.label("Lệnh nháp chưa giữ hàng. Thủ kho/chủ kho duyệt mới phân bổ Serial và khóa giữ chỗ.")
        formDialog("Lập lệnh xuất kho", form, "Lưu nháp") { dialog ->
            if (lines.isEmpty()) notify("Thêm ít nhất một mặt hàng.")
            else if (required(note)) submit(dialog) { id -> model.createDraft(id, units[dealer.selectedItemPosition].dealerId, lines.toList(), note.text.toString().trim(), actor()) }
        }
    }

    private fun showOrder(order: OutboundOrderEntity) {
        val actions = mutableListOf<Pair<String, () -> Unit>>()
        if (order.status == "DRAFT" && canConfirm()) actions += "Duyệt và giữ chỗ" to { confirm("Duyệt ${order.orderCode}?", "Phân bổ Serial FIFO và giữ hàng cho đơn vị nhận.") { dialog -> submit(dialog) { id -> model.approve(id, order.orderCode, actor()) } } }
        if (order.status in setOf("RESERVED", "PACKING") && canOperate()) actions += "Soạn hàng và quét Serial" to { submit { id -> model.openPicking(id, order, actor()) } }
        if (order.status in setOf("DRAFT", "RESERVED", "PACKING") && canOperate()) actions += "Hủy lệnh / giải phóng giữ chỗ" to { cancel(order) }
        if (order.status == "COMPLETED") actions += "Xem / in phiếu xuất bàn giao" to { submit { id -> model.document(id, order.orderCode) } }
        val info = "${order.dealerName}\n${order.productName}\nSố lượng: ${order.convertedQuantity} chiếc\n${outboundOrderStatus(order.status)}\nNgười lập: ${order.createdBy}\nNgười duyệt: ${order.approvedBy}\nGhi chú: ${order.note}" + if (order.cancelReason.isNotBlank()) "\nLý do hủy: ${order.cancelReason}" else ""
        MaterialAlertDialogBuilder(requireContext()).setTitle(order.orderCode).setMessage(info).setPositiveButton("Đóng", null)
            .also { builder -> if (actions.isNotEmpty()) builder.setNeutralButton("Thao tác") { _, _ -> MaterialAlertDialogBuilder(requireContext()).setTitle(order.orderCode).setItems(actions.map { it.first }.toTypedArray()) { _, index -> actions[index].second() }.show() } }.show()
    }

    private fun cancel(order: OutboundOrderEntity) {
        val form = Form(); val reason = form.edit("Lý do hủy *", multiline = true)
        formDialog("Hủy ${order.orderCode}", form, "Xác nhận hủy") { dialog -> if (required(reason)) submit(dialog) { id -> model.cancel(id, order.orderCode, reason.text.toString().trim(), actor()) } }
    }

    private fun showPicking(order: OutboundOrderEntity, picks: List<OutboundPick>, previousScans: List<String>) {
        if (picks.isEmpty()) { notify("Không có Serial được phân bổ cho lệnh này.", true); return }
        val form = Form()
        form.label("${order.orderCode} · ${order.dealerName}", bold = true)
        form.label(picks.joinToString("\n\n") { "${it.productCode} · ${it.serialNumber}\nLô ${it.lotNumber} · ${it.currentLocation}\nNhập ${it.importDate} · Giá vốn ${money.format(it.unitCost)} đ" })
        val input = form.edit("Quét / nhập Serial", inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_CAP_CHARACTERS)
        val progress = form.label("")
        val scanned = previousScans.toMutableSet()
        val carrier = form.edit("Đơn vị / người vận chuyển")
        val tracking = form.edit("Mã vận đơn / tham chiếu bàn giao")
        if (!canConfirm()) form.label("Kết quả quét được lưu. Thủ kho/chủ kho đăng nhập và mở lại lệnh để xác nhận xuất vật lý.")
        lateinit var dialog: AlertDialog
        fun update() {
            progress.text = "Đã quét ${scanned.size}/${picks.size} Serial\n" + scanned.joinToString("\n") { "✓ $it" }
            val ready = canConfirm() && scanned.size == picks.size && scanned.containsAll(picks.map { it.serialNumber })
            dialog.window?.decorView?.tag = if (ready) null else "NO_SUBMIT"
            dialog.getButton(AlertDialog.BUTTON_POSITIVE)?.isEnabled = ready && model.busy.value != true
        }
        fun scan(code: String) {
            if (!dialog.isShowing || model.busy.value == true) return
            val id = model.requestId()
            pending[id] = { result -> result.scannedSerials?.let { scanned.clear(); scanned.addAll(it); input.setText(""); feedback(); update() } }
            model.recordScan(id, order.orderCode, code, actor())
        }
        form.button("Thêm mã Serial") { scan(input.text.toString()) }
        form.button("Mở camera quét mã") { camera { scan(it) } }
        input.setOnEditorActionListener { _, _, _ -> scan(input.text.toString()); true }
        dialog = formDialog("Soạn hàng và đối soát", form, "Xác nhận xuất") { current ->
            if (scanned.size != picks.size) notify("Cần quét đủ Serial trong Picking List.")
            else submit(current) { id -> model.complete(id, order.orderCode, scanned.toList(), carrier.text.toString().trim(), tracking.text.toString().trim(), actor()) }
        }
        update()
    }

    private fun showDocument(document: OutboundDocument) {
        val details = "Phiếu: ${document.code}\nLệnh: ${document.orderCode}\nĐơn vị nhận: ${document.dealerName}\nĐịa chỉ: ${document.address}\nXuất: ${document.createdAt}\nNgười lập: ${document.createdBy}\nNgười duyệt: ${document.approvedBy}\nNgười xuất: ${document.dispatchedBy}\nVận chuyển: ${document.carrier}\nVận đơn: ${document.trackingNumber}\n\n" + document.serials.joinToString("\n") { "${it.productCode} · ${it.serialNumber} · ${it.currentLocation}" }
        MaterialAlertDialogBuilder(requireContext()).setTitle("Phiếu xuất kiêm bàn giao").setMessage(details).setPositiveButton("In / Lưu PDF") { _, _ -> OutboundPrintManager.print(requireContext(), document) }.setNegativeButton("Đóng", null).show()
    }

    private fun showReturn() {
        val data = state ?: return
        val units = data.dealers
        val candidates = data.serials.filter { it.status in setOf("DISPATCHED", "DELIVERED") }
        if (units.isEmpty() || candidates.isEmpty()) { notify("Chưa có Serial đã xuất để nhận hoàn trả."); return }
        val form = Form()
        val dealer = form.spinner("Đơn vị gửi trả *", units.map { "${it.dealerId} · ${it.name}" })
        val serial = form.edit("Serial hoàn trả *", inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_CAP_CHARACTERS)
        form.button("Camera quét Serial trả") { camera { serial.setText(it) } }
        form.button("Tra danh sách đã xuất") { MaterialAlertDialogBuilder(requireContext()).setTitle("Serial đã xuất").setItems(candidates.map { "${it.serialNumber} · ${it.dealerName.orEmpty()}" }.toTypedArray()) { _, index -> serial.setText(candidates[index].serialNumber) }.show() }
        val condition = form.spinner("Kết quả kiểm định *", listOf("Hàng mới nguyên seal → Kho Mới", "Hàng lỗi/trầy xước → Kho Lỗi"))
        val reason = form.edit("Lý do / biên bản kiểm định *", multiline = true)
        form.label("Đối chiếu đơn vị nhận và chứng từ xuất gốc. Không nhận trả trùng cho cùng lần xuất.")
        formDialog("Tiếp nhận hoàn trả", form, "Xác nhận nhận trả") { dialog ->
            if (required(serial, reason)) submit(dialog) { id -> model.receiveReturn(id, units[dealer.selectedItemPosition].dealerId, serial.text.toString().trim().uppercase(Locale.ROOT), if (condition.selectedItemPosition == 0) "HANG_MOI" else "DEFECTIVE", reason.text.toString().trim(), actor()) }
        }
    }

    private fun showOtherDispatch() {
        val serials = state?.serials.orEmpty().filter { it.status in setOf("DEFECTIVE", "DISPLAY") }
        if (serials.isEmpty()) { notify("Không có hàng lỗi hoặc trưng bày phù hợp để xuất bảo hành/tiêu hủy."); return }
        val form = Form()
        val serial = form.spinner("Serial cần xuất *", serials.map { "${it.serialNumber} · ${it.status} · ${it.currentLocation}" })
        val purpose = form.spinner("Mục đích *", listOf("Gửi bảo hành hãng", "Tiêu hủy — cần chủ kho phê duyệt", "Xuất bán thanh lý (Hàng trưng bày)"))
        val reason = form.edit("Lý do / biên bản kỹ thuật *", multiline = true)
        form.label("Chỉ chủ kho được xác nhận tiêu hủy. Phiếu xuất khác lưu Serial, người thực hiện và biến động kho.")
        formDialog("Xuất kho khác", form, "Xác nhận xuất") { dialog ->
            if (required(reason)) {
                if (purpose.selectedItemPosition == 1 && session.getRole() != "STORE_OWNER") notify("Cần tài khoản chủ kho để phê duyệt tiêu hủy.", true)
                else {
                    val purCode = when (purpose.selectedItemPosition) {
                        0 -> "BAO_HANH_HANG"
                        1 -> "TIEU_HUY"
                        else -> "THANH_LY"
                    }
                    submit(dialog) { id -> model.otherDispatch(id, serials[serial.selectedItemPosition].serialNumber, purCode, reason.text.toString().trim(), actor()) }
                }
            }
        }
    }

    private fun camera(onCode: (String) -> Unit) {
        if (!isAdded || model.busy.value == true) return
        GmsBarcodeScanning.getClient(requireActivity()).startScan()
            .addOnSuccessListener { barcode -> if (_binding != null) barcode.rawValue?.takeIf { it.isNotBlank() }?.let(onCode) }
            .addOnCanceledListener { if (_binding != null) notify("Đã đóng camera. Bạn vẫn có thể nhập hoặc dùng máy quét mã.") }
            .addOnFailureListener { if (_binding != null) notify("Camera chưa sẵn sàng. Kiểm tra Google Play Services/kết nối lần đầu hoặc nhập mã Serial.", true) }
    }

    private fun feedback() {
        view?.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS)
        runCatching { val tone = ToneGenerator(AudioManager.STREAM_NOTIFICATION, 60); tone.startTone(ToneGenerator.TONE_PROP_ACK, 100); Handler(Looper.getMainLooper()).postDelayed({ tone.release() }, 150) }
    }

    private fun submit(dialog: AlertDialog? = null, operation: (Int) -> Unit) {
        if (model.busy.value == true) return
        val id = model.requestId()
        pending[id] = { result ->
            dialog?.dismiss()
            if (_binding != null) { result.picking?.let { picks -> result.order?.let { showPicking(it, picks, result.scannedSerials.orEmpty()) } }; result.document?.let(::showDocument) }
        }
        operation(id)
    }

    private fun confirm(title: String, message: String, action: (AlertDialog) -> Unit) { val form = Form(); form.label(message); formDialog(title, form, "Xác nhận", action) }
    private fun formDialog(title: String, form: Form, positive: String, action: (AlertDialog) -> Unit): AlertDialog {
        val dialog = MaterialAlertDialogBuilder(requireContext()).setTitle(title).setView(form.root).setPositiveButton(positive, null).setNegativeButton("Đóng", null).create()
        dialogs.add(dialog)
        dialog.setOnDismissListener { dialogs.remove(dialog) }
        dialog.setOnShowListener { dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener { if (model.busy.value != true) action(dialog) } }
        dialog.show()
        return dialog
    }
    private fun required(vararg fields: EditText): Boolean {
        var valid = true
        fields.forEach { if (it.text.toString().isBlank()) { it.error = "Thông tin bắt buộc"; valid = false } }
        return valid
    }
    private fun notify(message: String, error: Boolean = false) { if (isAdded) { if (error) view?.performHapticFeedback(HapticFeedbackConstants.LONG_PRESS); Toast.makeText(requireContext(), message, if (error) Toast.LENGTH_LONG else Toast.LENGTH_SHORT).show() } }
    private fun roleLabel(role: String) = when (role) { "OPERATIONS_STAFF" -> "Nhân viên kho"; "WAREHOUSE_MANAGER" -> "Thủ kho"; "STORE_OWNER" -> "Chủ kho"; "SYSTEM_ADMIN" -> "Quản trị hệ thống — xem"; "ACCOUNTANT" -> "Kế toán — xem"; else -> "Chưa xác thực" }

    private inner class Form {
        val root: View = layoutInflater.inflate(R.layout.dialog_outbound_form, null)
        private val fields = root.findViewById<LinearLayout>(R.id.outboundFormFields)
        fun label(text: String, bold: Boolean = false): TextView = TextView(requireContext()).also { it.text = text; it.textSize = 13f; it.setPadding(0, dp(8), 0, dp(5)); if (bold) it.setTypeface(it.typeface, Typeface.BOLD); fields.addView(it) }
        fun edit(title: String, value: String = "", inputType: Int = InputType.TYPE_CLASS_TEXT, multiline: Boolean = false): EditText {
            label(title)
            return EditText(requireContext()).also { it.inputType = inputType or if (multiline) InputType.TYPE_TEXT_FLAG_MULTI_LINE else 0; it.setText(value); it.textSize = 14f; it.setSingleLine(!multiline); it.importantForAutofill = View.IMPORTANT_FOR_AUTOFILL_NO; fields.addView(it, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)) }
        }
        fun spinner(title: String, choices: List<String>): Spinner { label(title); return Spinner(requireContext()).also { it.adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, choices); fields.addView(it, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, dp(48))) } }
        fun button(title: String, action: () -> Unit): Button = Button(requireContext()).also { it.text = title; it.isAllCaps = false; it.setOnClickListener { if (model.busy.value != true) action() }; fields.addView(it) }
    }
    private fun dp(value: Int) = (value * resources.displayMetrics.density).toInt()
    private fun normalizeSearch(value: String) = Normalizer.normalize(value.trim().lowercase(Locale.ROOT), Normalizer.Form.NFD).replace(Regex("\\p{M}+"), "").replace('đ', 'd')
    override fun onDestroyView() { dialogs.toList().forEach { it.dismiss() }; dialogs.clear(); pending.clear(); _binding = null; super.onDestroyView() }
}
