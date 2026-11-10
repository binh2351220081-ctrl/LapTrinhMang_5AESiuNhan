package com.example.chronovaultwms.core.database

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

object DatabaseSeeder {
    private val sampleProducts = listOf(
        ProductEntity(
            productCode = "RLX-126610LN",
            name = "Rolex Submariner Date 41mm",
            brand = "Rolex",
            category = "Diver",
            wholesalePrice = 320000000.0,
            retailPrice = 365000000.0,
            stockQuantity = 14,
            caseDiameter = "41mm",
            dialColor = "Đen Cerachrom",
            movementType = "Automatic Cal. 3235",
            waterResistance = "300m / 30ATM"
        ),
        ProductEntity(
            productCode = "RLX-116500LN",
            name = "Rolex Cosmograph Daytona Panda",
            brand = "Rolex",
            category = "Chronograph",
            wholesalePrice = 750000000.0,
            retailPrice = 850000000.0,
            stockQuantity = 6,
            caseDiameter = "40mm",
            dialColor = "Trắng Panda",
            movementType = "Automatic Cal. 4130",
            waterResistance = "100m / 10ATM"
        ),
        ProductEntity(
            productCode = "OMG-310304250",
            name = "Omega Speedmaster Professional Moonwatch",
            brand = "Omega",
            category = "Chronograph",
            wholesalePrice = 165000000.0,
            retailPrice = 195000000.0,
            stockQuantity = 22,
            caseDiameter = "42mm",
            dialColor = "Đen mờ Step Dial",
            movementType = "Co-Axial Master Chronometer 3861",
            waterResistance = "50m / 5ATM"
        ),
        ProductEntity(
            productCode = "OMG-210304220",
            name = "Omega Seamaster Diver 300M Co-Axial",
            brand = "Omega",
            category = "Diver",
            wholesalePrice = 125000000.0,
            retailPrice = 145000000.0,
            stockQuantity = 18,
            caseDiameter = "42mm",
            dialColor = "Xanh gợn sóng Laser",
            movementType = "Automatic Cal. 8800",
            waterResistance = "300m / 30ATM"
        ),
        ProductEntity(
            productCode = "PP-57111R001",
            name = "Patek Philippe Nautilus 5711/1R Rose Gold",
            brand = "Patek Philippe",
            category = "Complications",
            wholesalePrice = 2100000000.0,
            retailPrice = 2350000000.0,
            stockQuantity = 2,
            caseDiameter = "40mm",
            dialColor = "Nâu ánh vàng Sunburst",
            movementType = "Calibre 26-330 S C",
            waterResistance = "120m / 12ATM"
        ),
        ProductEntity(
            productCode = "AP-16202ST",
            name = "Audemars Piguet Royal Oak Jumbo Extra-Thin",
            brand = "Audemars Piguet",
            category = "Luxury Sports",
            wholesalePrice = 1650000000.0,
            retailPrice = 1850000000.0,
            stockQuantity = 3,
            caseDiameter = "39mm",
            dialColor = "Xanh Bleu Nuit Petite Tapisserie",
            movementType = "Calibre 7121",
            waterResistance = "50m / 5ATM"
        ),
        ProductEntity(
            productCode = "CAR-WSSA0029",
            name = "Cartier Santos de Cartier Medium",
            brand = "Cartier",
            category = "Dress",
            wholesalePrice = 180000000.0,
            retailPrice = 205000000.0,
            stockQuantity = 12,
            caseDiameter = "35.1mm",
            dialColor = "Bạc mạ kim xanh",
            movementType = "Automatic 1847 MC",
            waterResistance = "100m / 10ATM"
        ),
        ProductEntity(
            productCode = "GS-SBGA211",
            name = "Grand Seiko Heritage Spring Drive Snowflake",
            brand = "Grand Seiko",
            category = "Dress",
            wholesalePrice = 145000000.0,
            retailPrice = 168000000.0,
            stockQuantity = 9,
            caseDiameter = "41mm",
            dialColor = "Trắng bông tuyết Snowflake",
            movementType = "Spring Drive 9R65 (±1s/ngày)",
            waterResistance = "100m / 10ATM"
        ),
        ProductEntity(
            productCode = "TUD-M79030N",
            name = "Tudor Black Bay Fifty-Eight 39mm",
            brand = "Tudor",
            category = "Diver",
            wholesalePrice = 88000000.0,
            retailPrice = 105000000.0,
            stockQuantity = 25,
            caseDiameter = "39mm",
            dialColor = "Đen mạ vàng Gilt",
            movementType = "Manufacture Calibre MT5402",
            waterResistance = "200m / 20ATM"
        ),
        ProductEntity(
            productCode = "IWC-IW371605",
            name = "IWC Portugieser Chronograph",
            brand = "IWC Schaffhausen",
            category = "Chronograph",
            wholesalePrice = 195000000.0,
            retailPrice = 228000000.0,
            stockQuantity = 8,
            caseDiameter = "41mm",
            dialColor = "Bạc mạ kim xanh",
            movementType = "Automatic Calibre 69355",
            waterResistance = "30m / 3ATM"
        )
    )

    private val sampleSerials = listOf(
        SerialEntity(
            serialNumber = "RLX-SUB-2026-001",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Két Sắt VIP-01 (Kho A)",
            importDate = "15/10/2026 09:30",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Đạt chuẩn COSC (+1s/ngày), Thẻ NFC kích hoạt 5 năm bảo hành"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-002",
            productCode = "RLX-126610LN",
            status = "ALLOCATED",
            currentLocation = "Kệ A1-02 (Khay xuất hàng)",
            importDate = "18/10/2026 14:15",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = "Đại lý LuxWatch Sài Gòn (Đơn #SO-2026-88)",
            qcNotes = "Chuẩn COSC (0s/ngày), Đã khóa giữ chỗ chờ thanh toán"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-003",
            productCode = "RLX-126610LN",
            status = "DELIVERED",
            currentLocation = "Đã bàn giao cho Đại lý",
            importDate = "05/10/2026 10:00",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = "Đồng Hồ Hải Triều (Đơn #SO-2026-45)",
            qcNotes = "Bàn giao thành công, kích hoạt BH điện tử chính hãng"
        ),
        SerialEntity(
            serialNumber = "RLX-DTN-2026-001",
            productCode = "RLX-116500LN",
            status = "IN_STOCK",
            currentLocation = "Két Sắt VIP-02 (Kho A)",
            importDate = "20/10/2026 11:20",
            unitCost = 680000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Superlative Chronometer chuẩn xác, nguyên seal 100% nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-DTN-2026-002",
            productCode = "RLX-116500LN",
            status = "ALLOCATED",
            currentLocation = "Két Sắt VIP-02",
            importDate = "22/10/2026 16:40",
            unitCost = 680000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = "Đại lý Galle Watch Hà Nội",
            qcNotes = "Đã nhận cọc 50%, kiểm định seal hoàn hảo"
        ),
        SerialEntity(
            serialNumber = "OMG-SPD-2026-001",
            productCode = "OMG-310304250",
            status = "IN_STOCK",
            currentLocation = "Kệ K2-B04",
            importDate = "10/10/2026 08:45",
            unitCost = 145000000.0,
            supplierName = "Omega Bienne HQ (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "METAS Master Chronometer kháng từ 15,000 Gauss"
        ),
        SerialEntity(
            serialNumber = "PP-NAU-2026-001",
            productCode = "PP-57111R001",
            status = "IN_STOCK",
            currentLocation = "Két Sắt Kim Cương Master",
            importDate = "01/10/2026 15:30",
            unitCost = 1750000000.0,
            supplierName = "Patek Philippe Plan-les-Ouates",
            dealerName = null,
            qcNotes = "Patek Philippe Seal, Chứng chỉ bảo tàng Geneva chính hiệu"
        ),
        SerialEntity(
            serialNumber = "AP-RO-2026-001",
            productCode = "AP-16202ST",
            status = "IN_STOCK",
            currentLocation = "Két Sắt Kim Cương Master",
            importDate = "05/10/2026 10:15",
            unitCost = 1420000000.0,
            supplierName = "Audemars Piguet Le Brassus",
            dealerName = null,
            qcNotes = "Họa tiết Petite Tapisserie thủ công, Calibre 7121 siêu mỏng"
        )
    )

    // 5 Người dùng đại diện chuẩn xác cho 5 Tác Nhân Nghiệp Vụ (5 Actors) theo tài liệu đồ án
    val sampleUsers = listOf(
        UserEntity(
            userId = "USR-001",
            username = "binh_admin",
            password = "admin123",
            fullName = "Phan Bá Hải Bình",
            role = "SYSTEM_ADMIN",
            department = "Tác nhân 1: Quản Trị Hệ Thống & Bảo Mật (TV1)",
            email = "binh_2351220081@dau.edu.vn",
            status = "ACTIVE"
        ),
        UserEntity(
            userId = "USR-002",
            username = "owner_boss",
            password = "admin123",
            fullName = "Chủ Cửa Hàng (Store Owner)",
            role = "STORE_OWNER",
            department = "Tác nhân 2: Chủ Cửa Hàng / Ban Điều Hành Tối Cao",
            email = "owner_chronovault@gmail.com",
            status = "ACTIVE"
        ),
        UserEntity(
            userId = "USR-003",
            username = "tam_manager",
            password = "123",
            fullName = "Võ Công Tâm",
            role = "WAREHOUSE_MANAGER",
            department = "Tác nhân 3: Thủ Kho (Quản Lý Điều Hành Kho Kệ) (TV4)",
            email = "tam_ltm@dau.edu.vn",
            status = "ACTIVE"
        ),
        UserEntity(
            userId = "USR-004",
            username = "quan_thao_ops",
            password = "123",
            fullName = "Nguyễn Đắc Quân & Tô Đức Thảo",
            role = "OPERATIONS_STAFF",
            department = "Tác nhân 4: Nhân Viên Nhập - Xuất Kho (TV2 & TV3)",
            email = "ops_ltm@dau.edu.vn",
            status = "ACTIVE"
        ),
        UserEntity(
            userId = "USR-005",
            username = "tu_accountant",
            password = "123",
            fullName = "Trần Công Tú",
            role = "ACCOUNTANT",
            department = "Tác nhân 5: Kế Toán Kho, Giá Vốn & Công Nợ (TV5)",
            email = "tu_ltm@dau.edu.vn",
            status = "ACTIVE"
        )
    )

    private val sampleAuditLogs = listOf(
        AuditLogEntity(
            timestamp = "10/11/2026 08:00:12",
            actorName = "Phan Bá Hải Bình",
            role = "SYSTEM_ADMIN",
            action = "KHỞI_TẠO_HỆ_THỐNG",
            details = "Khởi tạo thành công cơ sở dữ liệu Room v3 với chuẩn hóa 5 Tác Nhân Nghiệp Vụ.",
            ipAddress = "192.168.1.100 - Master Terminal"
        ),
        AuditLogEntity(
            timestamp = "10/11/2026 08:35:40",
            actorName = "Phan Bá Hải Bình",
            role = "SYSTEM_ADMIN",
            action = "NẠP_DANH_MỤC",
            details = "Nạp danh mục 10 mẫu đồng hồ xa xỉ (Rolex, Omega, Patek Philippe, Audemars Piguet...).",
            ipAddress = "192.168.1.100 - Master Terminal"
        ),
        AuditLogEntity(
            timestamp = "10/11/2026 09:15:22",
            actorName = "Phan Bá Hải Bình",
            role = "SYSTEM_ADMIN",
            action = "CẤU_HÌNH_RBAC",
            details = "Kích hoạt ma trận phân quyền 5 Tác Nhân: Admin, Chủ Cửa Hàng, Thủ Kho, NV Kho, Kế Toán.",
            ipAddress = "192.168.1.100 - Master Terminal"
        ),
        AuditLogEntity(
            timestamp = "10/11/2026 10:20:05",
            actorName = "Nguyễn Đắc Quân",
            role = "OPERATIONS_STAFF",
            action = "NHẬP_KHO_LÔ_HÀNG",
            details = "Xác nhận phiếu nhập khẩu PN-2026-01: 5 chiếc Rolex Submariner từ Rolex Geneva SA.",
            ipAddress = "192.168.1.102 - Inbound Terminal"
        ),
        AuditLogEntity(
            timestamp = "10/11/2026 11:05:48",
            actorName = "Trần Công Tú",
            role = "ACCOUNTANT",
            action = "PHÂN_BỔ_GIÁ_VỐN",
            details = "Hạch toán chi phí logistics và gán giá vốn đích danh cho Serial RLX-SUB-2026-002.",
            ipAddress = "192.168.1.105 - Accounting Terminal"
        )
    )

    suspend fun checkAndSeed(
        productDao: ProductDao,
        serialDao: SerialDao,
        userDao: UserDao,
        auditLogDao: AuditLogDao
    ) = withContext(Dispatchers.IO) {
        if (productDao.getProductCount() == 0) {
            productDao.insertAll(sampleProducts)
        }
        if (serialDao.countSerials() == 0) {
            serialDao.insertAll(sampleSerials)
        }
        val existingUsers = userDao.getAllUsers()
        if (existingUsers.isEmpty() || existingUsers.any { it.role == "DIRECTOR" }) {
            userDao.insertAll(sampleUsers)
        }
        if (auditLogDao.countLogs() == 0) {
            auditLogDao.insertAll(sampleAuditLogs)
        }
    }
}
