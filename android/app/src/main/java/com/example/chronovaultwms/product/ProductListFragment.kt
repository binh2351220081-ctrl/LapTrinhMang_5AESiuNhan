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
import com.example.chronovaultwms.core.auth.SessionManager
import com.example.chronovaultwms.core.database.AuditLogDao
import com.example.chronovaultwms.core.database.AuditLogEntity
import com.example.chronovaultwms.core.database.ChronoVaultDatabase
import com.example.chronovaultwms.core.database.DatabaseSeeder
import com.example.chronovaultwms.core.database.ProductDao
import com.example.chronovaultwms.core.database.ProductEntity
import com.example.chronovaultwms.core.database.SerialDao
import com.example.chronovaultwms.core.database.SerialEntity
import com.example.chronovaultwms.core.database.UserDao
import com.example.chronovaultwms.core.database.UserEntity
import com.example.chronovaultwms.databinding.DialogLoginBinding
import com.example.chronovaultwms.databinding.DialogProductAddBinding
import com.example.chronovaultwms.databinding.DialogProductSerialTimelineBinding
import com.example.chronovaultwms.databinding.DialogSystemManagementBinding
import com.example.chronovaultwms.databinding.DialogUserEditBinding
import com.example.chronovaultwms.databinding.FragmentProductListBinding
import com.example.chronovaultwms.databinding.ItemAuditLogBinding
import com.example.chronovaultwms.databinding.ItemProductTimelineStepBinding
import com.example.chronovaultwms.databinding.ItemUserAccountBinding
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Phân hệ 1: Quản trị Hàng hóa, Hệ thống & Serial Number
 * Phụ trách: TV1 - Phan Bá Hải Bình
 * Chức năng: 
 *   - Phần A: F1.1 (Thêm sản phẩm), F1.2 & F1.3 (Timeline Serial Lifecycle)
 *   - Phần B: F1.6 (Xác thực đăng nhập), F1.7 (Phân quyền RBAC), F1.8 (Audit Log Trail), F1.9 (Đổi Gmail / Sửa hồ sơ)
 */
class ProductListFragment : Fragment() {

    private var _binding: FragmentProductListBinding? = null
    private val binding get() = _binding!!

    private lateinit var database: ChronoVaultDatabase
    private lateinit var productDao: ProductDao
    private lateinit var serialDao: SerialDao
    private lateinit var userDao: UserDao
    private lateinit var auditLogDao: AuditLogDao
    private lateinit var sessionManager: SessionManager

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

        // Khởi tạo Database DAO & Session
        database = ChronoVaultDatabase.getInstance(requireContext())
        productDao = database.productDao()
        serialDao = database.serialDao()
        userDao = database.userDao()
        auditLogDao = database.auditLogDao()
        sessionManager = SessionManager(requireContext())

        setupRecyclerView()
        setupSearch()
        setupListeners()

        // Nạp CSDL và kiểm tra phiên đăng nhập
        loadProductsAndCheckAuth()
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

        binding.btnSystemSettings.setOnClickListener {
            showSystemManagementDialog()
        }

        binding.btnNavOutbound.setOnClickListener {
            parentFragmentManager.beginTransaction()
                .replace(R.id.fragmentContainer, com.example.chronovaultwms.outbound.OutboundOrderFragment())
                .addToBackStack(null)
                .commit()
        }

        // Bấm vào tên người dùng ở Header để đổi ngay Gmail / Hồ sơ cá nhân
        binding.tvLoggedInUser.setOnClickListener {
            viewLifecycleOwner.lifecycleScope.launch {
                val currentUserId = sessionManager.getUserId() ?: "USR-001"
                val currentUser = withContext(Dispatchers.IO) { userDao.getUserById(currentUserId) }
                if (currentUser != null) {
                    showEditUserDialog(currentUser)
                }
            }
        }

        binding.btnLogout.setOnClickListener {
            sessionManager.clearSession()
            Toast.makeText(requireContext(), "Đã đăng xuất khỏi hệ thống", Toast.LENGTH_SHORT).show()
            showLoginDialog()
        }
    }

    private fun loadProductsAndCheckAuth() {
        viewLifecycleOwner.lifecycleScope.launch {
            // Nạp dữ liệu mẫu ban đầu gồm Sản phẩm, Serials, 5 Tài khoản, Đại lý, Đơn sỉ và Nhật ký nếu CSDL rỗng
            DatabaseSeeder.checkAndSeed(
                productDao,
                serialDao,
                userDao,
                auditLogDao,
                database.dealerDao(),
                database.outboundOrderDao(),
                database.dealerReceiptDao()
            )

            // Lấy danh sách sản phẩm từ Room
            allProducts = withContext(Dispatchers.IO) {
                productDao.getAllProducts()
            }

            adapter.updateList(allProducts)
            binding.tvTotalCount.text = "Tổng danh mục: ${allProducts.size} mẫu đồng hồ"

            // Kiểm tra trạng thái phiên đăng nhập
            val currentRole = sessionManager.getRole()
            if (!sessionManager.isLoggedIn() || currentRole == "DIRECTOR") {
                sessionManager.saveSession("jwt_token_demo", "USR-001", "Phan Bá Hải Bình", "SYSTEM_ADMIN")
            }
            updateUserHeader()
        }
    }

    private fun updateUserHeader() {
        val name = sessionManager.getFullName() ?: "Phan Bá Hải Bình"
        val role = sessionManager.getRole() ?: "SYSTEM_ADMIN"
        val roleTitle = when (role) {
            "SYSTEM_ADMIN" -> "Quản Trị Hệ Thống"
            "STORE_OWNER" -> "Chủ Cửa Hàng"
            "WAREHOUSE_MANAGER" -> "Thủ Kho"
            "OPERATIONS_STAFF" -> "NV Kho"
            "ACCOUNTANT" -> "Kế Toán Kho"
            else -> role
        }
        binding.tvLoggedInUser.text = "👤 $name ($roleTitle) • ✏️ Đổi Gmail"
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

    /**
     * F1.6: Hộp thoại Đăng Nhập & Đăng Nhập Nhanh 1-Chạm Demo
     */
    private fun showLoginDialog() {
        val dialogBinding = DialogLoginBinding.inflate(layoutInflater)
        val dialog = AlertDialog.Builder(requireContext())
            .setView(dialogBinding.root)
            .setCancelable(false)
            .create()

        fun performLogin(usernameInput: String, passwordInput: String) {
            viewLifecycleOwner.lifecycleScope.launch {
                val user = withContext(Dispatchers.IO) {
                    userDao.login(usernameInput, passwordInput)
                }

                if (user != null) {
                    sessionManager.saveSession(
                        token = "jwt_${user.userId}",
                        userId = user.userId,
                        fullName = user.fullName,
                        role = user.role
                    )

                    // Ghi vết vào Audit Log
                    val currentTime = SimpleDateFormat("dd/MM/yyyy HH:mm:ss", Locale.getDefault()).format(Date())
                    val log = AuditLogEntity(
                        timestamp = currentTime,
                        actorName = user.fullName,
                        role = user.role,
                        action = "ĐĂNG_NHẬP",
                        details = "Đăng nhập thành công với chức danh ${user.department}.",
                        ipAddress = "192.168.1.100 - Mobile Terminal"
                    )
                    withContext(Dispatchers.IO) {
                        auditLogDao.insertLog(log)
                    }

                    updateUserHeader()
                    dialog.dismiss()
                    Toast.makeText(
                        requireContext(),
                        "Xin chào ${user.fullName} (${user.role})!",
                        Toast.LENGTH_LONG
                    ).show()
                } else {
                    Toast.makeText(
                        requireContext(),
                        "Sai tên đăng nhập hoặc mật khẩu!",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }

        dialogBinding.btnLoginSubmit.setOnClickListener {
            val u = dialogBinding.etLoginUsername.text.toString().trim()
            val p = dialogBinding.etLoginPassword.text.toString().trim()
            if (u.isNotEmpty() && p.isNotEmpty()) {
                performLogin(u, p)
            }
        }

        // 5 Nút Đăng Nhập Nhanh 1-Chạm cho 5 Tác Nhân Chuẩn Hóa
        dialogBinding.btnQuickBinh.setOnClickListener {
            performLogin("binh_admin", "admin123")
        }
        dialogBinding.btnQuickOwner.setOnClickListener {
            performLogin("owner_boss", "admin123")
        }
        dialogBinding.btnQuickTam.setOnClickListener {
            performLogin("tam_manager", "123")
        }
        dialogBinding.btnQuickOps.setOnClickListener {
            performLogin("quan_thao_ops", "123")
        }
        dialogBinding.btnQuickTu.setOnClickListener {
            performLogin("tu_accountant", "123")
        }

        dialog.show()
    }

    /**
     * F1.7 & F1.8: Hộp thoại Quản trị Hệ Thống: 3 Tab (Tài khoản, Ma trận RBAC, Audit Log Trail)
     */
    private fun showSystemManagementDialog() {
        val dialogBinding = DialogSystemManagementBinding.inflate(layoutInflater)
        val dialog = AlertDialog.Builder(requireContext())
            .setView(dialogBinding.root)
            .create()

        fun loadAccountsList() {
            viewLifecycleOwner.lifecycleScope.launch {
                val users = withContext(Dispatchers.IO) { userDao.getAllUsers() }
                dialogBinding.containerAccountsList.removeAllViews()
                users.forEach { user ->
                    val userItemBinding = ItemUserAccountBinding.inflate(layoutInflater, dialogBinding.containerAccountsList, false)
                    userItemBinding.tvUserFullName.text = user.fullName
                    userItemBinding.tvUserUsername.text = "@${user.username} • Mã ${user.userId}"
                    userItemBinding.tvUserRoleBadge.text = user.role
                    userItemBinding.tvUserDepartment.text = "🏢 ${user.department}"
                    userItemBinding.tvUserEmail.text = "✉️ ${user.email}"
                    userItemBinding.tvUserIcon.text = when (user.role) {
                        "SYSTEM_ADMIN" -> "🛡️"
                        "STORE_OWNER" -> "👑"
                        "WAREHOUSE_MANAGER" -> "🏢"
                        "OPERATIONS_STAFF" -> "📦"
                        "ACCOUNTANT" -> "💰"
                        else -> "👤"
                    }

                    // Phân quyền RBAC: Quản trị hệ thống (SYSTEM_ADMIN) hoặc Chủ cửa hàng (STORE_OWNER) hoặc chính chủ tài khoản mới có quyền sửa
                    val currentRole = sessionManager.getRole() ?: "SYSTEM_ADMIN"
                    val currentUserId = sessionManager.getUserId() ?: "USR-001"
                    val isAdmin = (currentRole == "SYSTEM_ADMIN" || currentRole == "STORE_OWNER")
                    val canEdit = isAdmin || (currentUserId == user.userId)

                    if (canEdit) {
                        userItemBinding.btnEditAccount.visibility = View.VISIBLE
                        userItemBinding.btnEditAccount.setOnClickListener {
                            showEditUserDialog(user) {
                                loadAccountsList()
                            }
                        }
                    } else {
                        userItemBinding.btnEditAccount.visibility = View.GONE
                    }

                    dialogBinding.containerAccountsList.addView(userItemBinding.root)
                }
            }
        }

        // Tab Switching Logic
        fun switchTab(selectedTab: String) {
            dialogBinding.layoutSectionAccounts.visibility = if (selectedTab == "accounts") View.VISIBLE else View.GONE
            dialogBinding.layoutSectionRoles.visibility = if (selectedTab == "roles") View.VISIBLE else View.GONE
            dialogBinding.layoutSectionLogs.visibility = if (selectedTab == "logs") View.VISIBLE else View.GONE

            dialogBinding.btnTabAccounts.backgroundTintList = ContextCompat.getColorStateList(
                requireContext(),
                if (selectedTab == "accounts") R.color.accent_gold else android.R.color.transparent
            )
            dialogBinding.btnTabRoles.backgroundTintList = ContextCompat.getColorStateList(
                requireContext(),
                if (selectedTab == "roles") R.color.accent_gold else android.R.color.transparent
            )
            dialogBinding.btnTabLogs.backgroundTintList = ContextCompat.getColorStateList(
                requireContext(),
                if (selectedTab == "logs") R.color.accent_gold else android.R.color.transparent
            )
        }

        dialogBinding.btnTabAccounts.setOnClickListener { switchTab("accounts") }
        dialogBinding.btnTabRoles.setOnClickListener { switchTab("roles") }
        dialogBinding.btnTabLogs.setOnClickListener { switchTab("logs") }

        // Load Dữ liệu Người Dùng & Audit Logs từ Room Database
        viewLifecycleOwner.lifecycleScope.launch {
            loadAccountsList()

            val logs = withContext(Dispatchers.IO) { auditLogDao.getAllLogs() }
            dialogBinding.containerLogsList.removeAllViews()
            logs.forEach { logItem ->
                val logBinding = ItemAuditLogBinding.inflate(layoutInflater, dialogBinding.containerLogsList, false)
                logBinding.tvLogAction.text = logItem.action
                logBinding.tvLogTimestamp.text = logItem.timestamp
                logBinding.tvLogActor.text = logItem.actorName
                logBinding.tvLogDetails.text = logItem.details
                logBinding.tvLogTerminal.text = "Địa chỉ: ${logItem.ipAddress}"
                dialogBinding.containerLogsList.addView(logBinding.root)
            }
        }

        dialogBinding.btnCloseSystemMgmt.setOnClickListener {
            dialog.dismiss()
        }

        dialog.show()
    }

    /**
     * F1.9: Hộp thoại Chỉnh Sửa Hồ Sơ, Đổi Gmail, Họ Tên, Mật Khẩu trực tiếp trong app
     */
    private fun showEditUserDialog(user: UserEntity, onUpdated: (() -> Unit)? = null) {
        val currentRole = sessionManager.getRole() ?: "SYSTEM_ADMIN"
        val currentUserId = sessionManager.getUserId() ?: "USR-001"
        val isAdmin = (currentRole == "SYSTEM_ADMIN" || currentRole == "STORE_OWNER")
        if (!isAdmin && currentUserId != user.userId) {
            Toast.makeText(
                requireContext(),
                "⛔ Bạn không có quyền quản trị để sửa tài khoản của người khác!",
                Toast.LENGTH_LONG
            ).show()
            return
        }

        val editBinding = DialogUserEditBinding.inflate(layoutInflater)
        val editDialog = AlertDialog.Builder(requireContext())
            .setView(editBinding.root)
            .create()

        editBinding.tvEditSubtitle.text = "Tài khoản: @${user.username} (${user.role}) • Mã ${user.userId}"
        editBinding.etEditFullName.setText(user.fullName)
        editBinding.etEditEmail.setText(user.email)
        editBinding.etEditDepartment.setText(user.department)

        editBinding.btnCancelEdit.setOnClickListener {
            editDialog.dismiss()
        }

        editBinding.btnSaveUserEdit.setOnClickListener {
            val newFullName = editBinding.etEditFullName.text.toString().trim()
            val newEmail = editBinding.etEditEmail.text.toString().trim()
            val newDept = editBinding.etEditDepartment.text.toString().trim()
            val newPass = editBinding.etEditPassword.text.toString().trim()

            if (newFullName.isEmpty()) {
                editBinding.tilEditFullName.error = "Vui lòng nhập họ và tên"
                return@setOnClickListener
            }
            if (newEmail.isEmpty() || !newEmail.contains("@")) {
                editBinding.tilEditEmail.error = "Địa chỉ Gmail không hợp lệ (cần có @)"
                return@setOnClickListener
            }

            val updatedUser = user.copy(
                fullName = newFullName,
                email = newEmail,
                department = newDept.ifEmpty { user.department },
                password = if (newPass.isNotEmpty()) newPass else user.password
            )

            viewLifecycleOwner.lifecycleScope.launch {
                withContext(Dispatchers.IO) {
                    userDao.updateUser(updatedUser)

                    // Ghi nhận Audit Log
                    val currentTime = SimpleDateFormat("dd/MM/yyyy HH:mm:ss", Locale.getDefault()).format(Date())
                    val log = AuditLogEntity(
                        timestamp = currentTime,
                        actorName = sessionManager.getFullName() ?: user.fullName,
                        role = sessionManager.getRole() ?: user.role,
                        action = "CẬP_NHẬT_HỒ_SƠ",
                        details = "Cập nhật Gmail thành '$newEmail', Họ tên: '$newFullName' cho tài khoản @${user.username}.",
                        ipAddress = "192.168.1.100 - Mobile Terminal"
                    )
                    auditLogDao.insertLog(log)
                }

                // Nếu đang chỉnh sửa tài khoản hiện tại, cập nhật lại Session & Header
                if (sessionManager.getUserId() == user.userId) {
                    sessionManager.saveSession(
                        sessionManager.getToken() ?: "jwt_${user.userId}",
                        user.userId,
                        newFullName,
                        user.role
                    )
                    updateUserHeader()
                }

                editDialog.dismiss()
                Toast.makeText(requireContext(), "✅ Đã đổi Gmail thành công: $newEmail", Toast.LENGTH_LONG).show()
                onUpdated?.invoke()
            }
        }

        editDialog.show()
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

        val brands = arrayOf(
            "Rolex", "Omega", "Patek Philippe", "Audemars Piguet",
            "Cartier", "Grand Seiko", "Tudor", "IWC Schaffhausen", "Hublot", "Breitling"
        )
        val brandAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_dropdown_item_1line, brands)
        dialogBinding.actvBrand.setAdapter(brandAdapter)
        dialogBinding.actvBrand.setText(brands[0], false)

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

            val actorName = sessionManager.getFullName() ?: "Phan Bá Hải Bình"
            val actorRole = sessionManager.getRole() ?: "SYSTEM_ADMIN"
            val auditLog = AuditLogEntity(
                timestamp = SimpleDateFormat("dd/MM/yyyy HH:mm:ss", Locale.getDefault()).format(Date()),
                actorName = actorName,
                role = actorRole,
                action = "THÊM_ĐỒNG_HỒ",
                details = "Thêm mới mẫu $name (SKU: $sku) với số lượng $stock chiếc vào kho.",
                ipAddress = "192.168.1.100 - Mobile Terminal"
            )

            viewLifecycleOwner.lifecycleScope.launch {
                withContext(Dispatchers.IO) {
                    productDao.insertProduct(newProduct)
                    serialDao.insert(newSerial)
                    auditLogDao.insertLog(auditLog)
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

            val serialDisplayList = serialList.map { "${it.serialNumber} (${it.status})" }
            val serialDropdownAdapter = ArrayAdapter(
                requireContext(),
                android.R.layout.simple_dropdown_item_1line,
                serialDisplayList
            )
            dialogBinding.actvSerialSelector.setAdapter(serialDropdownAdapter)
            dialogBinding.actvSerialSelector.setText(serialDisplayList[0], false)

            fun renderTimelineForSerial(serial: SerialEntity) {
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

                    if (index == steps.size - 1) {
                        stepBinding.viewTimelineLine.visibility = View.INVISIBLE
                    }

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

            renderTimelineForSerial(serialList[0])

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
