package com.example.chronovaultwms.core.database

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

object DatabaseSeeder {
    private val initialProductCatalog = listOf(
        ProductEntity(
            productCode = "RLX-126610LN",
            name = "Rolex Submariner Date 41mm",
            brand = "Rolex",
            category = "Diver",
            wholesalePrice = 350000000.0,
            retailPrice = 365000000.0,
            stockQuantity = 14,
            caseDiameter = "41mm",
            dialColor = "Đen Cerachrom",
            movementType = "Automatic Cal. 3235",
            waterResistance = "300m / 30ATM",
            conversionRate = 10,
            minDispatchQuantity = 2
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

    val sampleSerials = listOf(
        SerialEntity(
            serialNumber = "RLX-SUB-2026-001",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B03",
            importDate = "15/10/2026 09:30",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 1 (Hàng mới nguyên seal): Đạt chuẩn COSC (+1s/ngày), Thẻ NFC kích hoạt 5 năm bảo hành"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-004",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B04",
            importDate = "15/10/2026 09:35",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 1 (Hàng mới nguyên seal): Chuẩn COSC (0s/ngày), sẵn sàng xuất kho theo FIFO"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-002",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Két VIP-02",
            importDate = "25/10/2026 14:15",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2 (Giá vốn 295tr): Lưu Két VIP-02, đối soát chống xuất nhầm lô (TC-06)"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-005",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B05",
            importDate = "25/10/2026 14:20",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2 (Hàng mới nguyên seal): Chuẩn COSC (+1s/ngày), sẵn sàng phân bổ"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-006",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B06",
            importDate = "25/10/2026 14:22",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal, đầy đủ thẻ bảo hành NFC"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-007",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B07",
            importDate = "25/10/2026 14:25",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-008",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B08",
            importDate = "25/10/2026 14:28",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal, chuẩn COSC"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-009",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B09",
            importDate = "25/10/2026 14:30",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-010",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A02-B10",
            importDate = "25/10/2026 14:32",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-011",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A03-B01",
            importDate = "25/10/2026 14:35",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-012",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A03-B02",
            importDate = "25/10/2026 14:38",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-013",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A03-B03",
            importDate = "25/10/2026 14:40",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-014",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A03-B04",
            importDate = "25/10/2026 14:42",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-015",
            productCode = "RLX-126610LN",
            status = "IN_STOCK",
            currentLocation = "Kệ K1-A03-B05",
            importDate = "25/10/2026 14:45",
            unitCost = 295000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Lô 2: Nguyên seal nhà máy"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-003",
            productCode = "RLX-126610LN",
            status = "DELIVERED",
            currentLocation = "Đã bàn giao cho Đơn vị nhận",
            importDate = "05/10/2026 10:00",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = "Đồng Hồ Hải Triều (Lệnh #PX-2026-45)",
            qcNotes = "Bàn giao kho vận thành công, kèm biên bản niêm phong"
        ),
        SerialEntity(
            serialNumber = "RLX-SUB-2026-ERR",
            productCode = "RLX-126610LN",
            status = "DEFECTIVE",
            currentLocation = "Kho Lỗi C-01 (Cách ly)",
            importDate = "12/10/2026 08:00",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Hấp hơi mặt kính - Cách ly chờ xuất bảo hành hãng (TC-04)"
        ),
        SerialEntity(
            serialNumber = "RX-9921",
            productCode = "RLX-126610LN",
            status = "DEFECTIVE",
            currentLocation = "Kho Lỗi C-01 (Cách ly)",
            importDate = "12/10/2026 08:00",
            unitCost = 285000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Hàng trầy xước vỏ - Cách ly chờ xuất bảo hành hãng (TC-05)"
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
            status = "IN_STOCK",
            currentLocation = "Két Sắt VIP-02",
            importDate = "22/10/2026 16:40",
            unitCost = 680000000.0,
            supplierName = "Rolex Geneva SA (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Hàng mới nguyên seal, sẵn sàng phân bổ theo lệnh xuất kho"
        ),
        SerialEntity(
            serialNumber = "OMG-SPEED-2026-001",
            productCode = "OMG-310304250",
            status = "DISPATCHED",
            currentLocation = "Đã bàn giao (Lệnh #DS-2026-002)",
            importDate = "10/10/2026 08:45",
            unitCost = 145000000.0,
            supplierName = "Omega Bienne HQ (Thụy Sĩ)",
            dealerName = "Đồng Hồ Hải Triều",
            qcNotes = "METAS Master Chronometer kháng từ 15,000 Gauss - Đã xuất kho DS-2026-002"
        ),
        SerialEntity(
            serialNumber = "OMG-SPEED-2026-002",
            productCode = "OMG-310304250",
            status = "DISPATCHED",
            currentLocation = "Đã bàn giao (Lệnh #DS-2026-002)",
            importDate = "10/10/2026 08:50",
            unitCost = 145000000.0,
            supplierName = "Omega Bienne HQ (Thụy Sĩ)",
            dealerName = "Đồng Hồ Hải Triều",
            qcNotes = "METAS Master Chronometer - Đã xuất kho DS-2026-002"
        ),
        SerialEntity(
            serialNumber = "OMG-SPEED-2026-003",
            productCode = "OMG-310304250",
            status = "IN_STOCK",
            currentLocation = "Kệ K2-B04",
            importDate = "11/10/2026 09:00",
            unitCost = 145000000.0,
            supplierName = "Omega Bienne HQ (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "METAS Master Chronometer, hàng mới nguyên seal sẵn sàng điều phối"
        ),
        SerialEntity(
            serialNumber = "CAR-SAN-2026-001",
            productCode = "CAR-WSSA0029",
            status = "IN_STOCK",
            currentLocation = "Kệ K3-C01",
            importDate = "08/11/2026 09:00",
            unitCost = 155000000.0,
            supplierName = "Cartier Manufacture (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Hàng mới nguyên seal, sẵn sàng xuất cho Lệnh DS-2026-003"
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
            username = "quan_inbound",
            password = "123",
            fullName = "Nguyễn Đắc Quân",
            role = "OPERATIONS_STAFF",
            department = "Nhân Viên Nhập Kho & NCC (TV2)",
            email = "quan_ltm@dau.edu.vn",
            status = "ACTIVE"
        ),
        UserEntity(
            userId = "USR-006",
            username = "thao_outbound",
            password = "123",
            fullName = "Tô Đức Thảo",
            role = "OPERATIONS_STAFF",
            department = "Nhân Viên Xuất Kho & Đại Lý (TV3)",
            email = "thao_ltm@dau.edu.vn",
            status = "ACTIVE"
        ),
        UserEntity(
            userId = "USR-007",
            username = "tu_accountant",
            password = "123",
            fullName = "Trần Công Tú",
            role = "ACCOUNTANT",
            department = "Tác nhân 5: Kế Toán Kho, Giá Vốn & Công Nợ (TV5)",
            email = "tu_ltm@dau.edu.vn",
            status = "ACTIVE"
        )
    )

    val sampleAuditLogs = listOf(
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
        ),
        AuditLogEntity(
            timestamp = "10/11/2026 14:10:15",
            actorName = "Tô Đức Thảo",
            role = "OPERATIONS_STAFF",
            action = "LẬP_LỆNH_XUẤT_NHÁP",
            details = "Lập nháp lệnh điều phối DS-2026-001 cho Chi nhánh Galle Watch: 2 chiếc Rolex Submariner, chờ Thủ kho duyệt.",
            ipAddress = "192.168.1.103 - Outbound Terminal"
        )
    )

    val sampleDealers = listOf(
        DealerEntity(
            dealerId = "DL-GALLE",
            name = "Galle Watch Việt Nam",
            tier = "VIP",
            discountPercent = 0.25,
            creditLimit = 3000000000.0,
            currentDebt = 1800000000.0,
            phone = "0988.123.456",
            address = "41 Thi Sách, Hai Bà Trưng, Hà Nội",
            taxCode = "0101892831",
            status = "ACTIVE"
        ),
        DealerEntity(
            dealerId = "DL-HAITRIEU",
            name = "Đồng Hồ Hải Triều",
            tier = "VIP",
            discountPercent = 0.30,
            creditLimit = 2500000000.0,
            currentDebt = 1200000000.0,
            phone = "0977.654.321",
            address = "160 Âu Cơ, P.9, Tân Bình, TP.HCM",
            taxCode = "0312548910",
            status = "ACTIVE"
        ),
        DealerEntity(
            dealerId = "DL-BOSSLUX",
            name = "Boss Luxury Watch",
            tier = "SILVER",
            discountPercent = 0.25,
            creditLimit = 1500000000.0,
            currentDebt = 600000000.0,
            phone = "0944.888.999",
            address = "60 Ngô Quyền, Hoàn Kiếm, Hà Nội",
            taxCode = "0108923412",
            status = "ACTIVE"
        ),
        DealerEntity(
            dealerId = "DL-DANGQUANG",
            name = "Đăng Quang Watch",
            tier = "SILVER",
            discountPercent = 0.25,
            creditLimit = 1000000000.0,
            currentDebt = 350000000.0,
            phone = "0966.333.222",
            address = "55 Trần Đăng Ninh, Cầu Giấy, Hà Nội",
            taxCode = "0105829103",
            status = "ACTIVE"
        ),
        DealerEntity(
            dealerId = "DL-XWATCH",
            name = "Xwatch Luxury",
            tier = "BRONZE",
            discountPercent = 0.20,
            creditLimit = 500000000.0,
            currentDebt = 0.0,
            phone = "0933.777.111",
            address = "472 Xã Đàn, Đống Đa, Hà Nội",
            taxCode = "0106948271",
            status = "ACTIVE"
        )
    )

    val sampleOrders = listOf(
        OutboundOrderEntity(
            orderCode = "DS-2026-001",
            dealerId = "DL-GALLE",
            dealerName = "Galle Watch Việt Nam",
            productCode = "RLX-126610LN",
            productName = "Rolex Submariner Date 41mm",
            unit = "PIECE",
            quantity = 2,
            convertedQuantity = 2,
            unitPrice = 350000000.0,
            discountPercent = 0.25,
            totalAmount = 525000000.0,
            depositAmount = 150000000.0,
            remainingDebt = 375000000.0,
            status = "DRAFT",
            createdDate = "10/11/2026 14:10",
            dispatchedSerials = "",
            note = "Xuất bán buôn đợt 1",
            createdBy = "Tô Đức Thảo"
        ),
        OutboundOrderEntity(
            orderCode = "DS-2026-002",
            dealerId = "DL-HAITRIEU",
            dealerName = "Đồng Hồ Hải Triều",
            productCode = "OMG-310304250",
            productName = "Omega Speedmaster Professional Moonwatch",
            unit = "PIECE",
            quantity = 2,
            convertedQuantity = 2,
            unitPrice = 165000000.0,
            discountPercent = 0.30,
            totalAmount = 231000000.0,
            depositAmount = 100000000.0,
            remainingDebt = 131000000.0,
            status = "COMPLETED",
            createdDate = "09/11/2026 16:45",
            dispatchedSerials = "OMG-SPEED-2026-001, OMG-SPEED-2026-002",
            note = "Xuất giao đại lý Hải Triều - Chi nhánh Bạch Đằng",
            createdBy = "Tô Đức Thảo",
            approvedBy = "Phan Bá Hải Bình",
            approvedAt = "09/11/2026 16:50",
            dispatchedBy = "Tô Đức Thảo",
            dispatchedAt = "09/11/2026 17:15"
        ),
        OutboundOrderEntity(
            orderCode = "DS-2026-003",
            dealerId = "DL-BOSSLUX",
            dealerName = "Boss Luxury Watch",
            productCode = "CAR-WSSA0029",
            productName = "Cartier Santos de Cartier Medium",
            unit = "PIECE",
            quantity = 1,
            convertedQuantity = 1,
            unitPrice = 180000000.0,
            discountPercent = 0.25,
            totalAmount = 135000000.0,
            depositAmount = 50000000.0,
            remainingDebt = 85000000.0,
            status = "DRAFT",
            createdDate = "10/11/2026 15:20",
            dispatchedSerials = "",
            note = "Đơn đặt hàng VIP chi nhánh",
            createdBy = "Tô Đức Thảo"
        )
    )

    val sampleReceipts = listOf(
        DealerReceiptEntity(
            receiptId = "PT-2026-001",
            dealerId = "DL-GALLE",
            dealerName = "Galle Watch Việt Nam",
            amount = 200000000.0,
            paymentMethod = "CHUYEN_KHOAN",
            referenceDoc = "UNC-VCB-88391",
            date = "09/11/2026 15:30",
            note = "Xác nhận bàn giao & giải phóng hạn mức bảo lãnh lô Rolex tháng 10 (TC-05)"
        ),
        DealerReceiptEntity(
            receiptId = "PT-2026-002",
            dealerId = "DL-HAITRIEU",
            dealerName = "Đồng Hồ Hải Triều",
            amount = 100000000.0,
            paymentMethod = "CHUYEN_KHOAN",
            referenceDoc = "UNC-TCB-99201",
            date = "10/11/2026 09:15",
            note = "Ký quỹ bảo lãnh điều phối xuất kho lô Omega Moonwatch"
        )
    )

    /** Consistent warehouse demo: every new-stock unit has a real Serial; drafts do not reserve. */
    val sampleWarehouseSerials: List<SerialEntity>
        get() = sampleSerials.map { serial ->
            if (serial.status == "ALLOCATED" && serial.allocatedOrderCode == null) {
                serial.copy(status = "IN_STOCK", dealerName = null)
            } else serial
        }

    val sampleWarehouseProducts: List<ProductEntity>
        get() = initialProductCatalog.map { product ->
            product.copy(stockQuantity = sampleWarehouseSerials.count {
                it.productCode == product.productCode && it.status in setOf("IN_STOCK", "ALLOCATED")
            })
        }

    val sampleProducts: List<ProductEntity>
        get() = sampleWarehouseProducts

    suspend fun checkAndSeed(
        productDao: ProductDao,
        serialDao: SerialDao,
        userDao: UserDao,
        auditLogDao: AuditLogDao,
        dealerDao: DealerDao? = null,
        outboundOrderDao: OutboundOrderDao? = null,
        dealerReceiptDao: DealerReceiptDao? = null
    ) = withContext(Dispatchers.IO) {
        if (productDao.getProductCount() == 0) {
            productDao.insertAll(sampleWarehouseProducts)
        }
        if (serialDao.countSerials() == 0) {
            serialDao.insertAll(sampleWarehouseSerials)
        }
        val existingUsers = userDao.getAllUsers()
        if (existingUsers.isEmpty() || existingUsers.any { it.role == "DIRECTOR" }) {
            userDao.insertAll(sampleUsers)
        }
        if (auditLogDao.countLogs() == 0) {
            auditLogDao.insertAll(sampleAuditLogs)
        }
        dealerDao?.let {
            if (it.countDealers() == 0) {
                it.insertAll(sampleDealers)
            }
        }
        outboundOrderDao?.let {
            if (it.countOrders() == 0) {
                it.insertAll(sampleOrders.map { order ->
                    if (order.status == "RESERVED") order.copy(status = "DRAFT", createdBy = "Dữ liệu mẫu",
                        note = "Lệnh mẫu cần Thủ kho duyệt trước khi giữ chỗ.", depositAmount = 0.0,
                        remainingDebt = 0.0, discountPercent = 0.0)
                    else order
                })
            }
        }
        dealerReceiptDao?.let {
            if (it.countReceipts() == 0) {
                it.insertAll(sampleReceipts)
            }
        }
    }
}
