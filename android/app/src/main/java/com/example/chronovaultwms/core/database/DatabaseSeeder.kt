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
        // Serials cho Rolex Submariner (RLX-126610LN)
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

        // Serials cho Rolex Daytona (RLX-116500LN)
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

        // Serials cho Omega Speedmaster Moonwatch (OMG-310304250)
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
            serialNumber = "OMG-SPD-2026-002",
            productCode = "OMG-310304250",
            status = "IN_STOCK",
            currentLocation = "Kệ K2-B04",
            importDate = "10/10/2026 08:45",
            unitCost = 145000000.0,
            supplierName = "Omega Bienne HQ (Thụy Sĩ)",
            dealerName = null,
            qcNotes = "Đạt chuẩn NASA Qualification, phụ kiện kính lúp & dây velcro đầy đủ"
        ),

        // Serials cho Patek Philippe Nautilus (PP-57111R001)
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

        // Serials cho Audemars Piguet Royal Oak (AP-16202ST)
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
        ),

        // Serials cho Grand Seiko Snowflake (GS-SBGA211)
        SerialEntity(
            serialNumber = "GS-SNO-2026-001",
            productCode = "GS-SBGA211",
            status = "IN_STOCK",
            currentLocation = "Kệ K3-A05",
            importDate = "28/10/2026 09:00",
            unitCost = 125000000.0,
            supplierName = "Grand Seiko Shinshu Studio (Nhật Bản)",
            dealerName = null,
            qcNotes = "Bộ máy Spring Drive trôi tuyệt đối, đánh bóng Zaratsu hoàn hảo"
        )
    )

    suspend fun checkAndSeed(productDao: ProductDao, serialDao: SerialDao) = withContext(Dispatchers.IO) {
        if (productDao.getProductCount() == 0) {
            productDao.insertAll(sampleProducts)
        }
        if (serialDao.countSerials() == 0) {
            serialDao.insertAll(sampleSerials)
        }
    }
}
