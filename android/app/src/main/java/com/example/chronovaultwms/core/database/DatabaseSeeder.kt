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
            productCode = "PP-5711-1A",
            name = "Patek Philippe Nautilus Blue Dial",
            brand = "Patek Philippe",
            category = "Luxury Sport",
            wholesalePrice = 2850000000.0,
            retailPrice = 3200000000.0,
            stockQuantity = 3,
            caseDiameter = "40mm",
            dialColor = "Xanh Lam Gradient",
            movementType = "Automatic Cal. 324 S C",
            waterResistance = "120m / 12ATM"
        ),
        ProductEntity(
            productCode = "AP-15500ST",
            name = "Audemars Piguet Royal Oak Selfwinding",
            brand = "Audemars Piguet",
            category = "Luxury Sport",
            wholesalePrice = 1150000000.0,
            retailPrice = 1350000000.0,
            stockQuantity = 5,
            caseDiameter = "41mm",
            dialColor = "Xanh Grande Tapisserie",
            movementType = "Automatic Calibre 4302",
            waterResistance = "50m / 5ATM"
        ),
        ProductEntity(
            productCode = "CAR-WSSA0018",
            name = "Cartier Santos de Cartier Large",
            brand = "Cartier",
            category = "Dress",
            wholesalePrice = 175000000.0,
            retailPrice = 205000000.0,
            stockQuantity = 11,
            caseDiameter = "39.8mm",
            dialColor = "Trắng Opaline cọc số La Mã",
            movementType = "Automatic Cal. 1847 MC",
            waterResistance = "100m / 10ATM"
        ),
        ProductEntity(
            productCode = "GS-SBGA211",
            name = "Grand Seiko Heritage 'Snowflake'",
            brand = "Grand Seiko",
            category = "Dress",
            wholesalePrice = 135000000.0,
            retailPrice = 158000000.0,
            stockQuantity = 16,
            caseDiameter = "41mm",
            dialColor = "Trắng vân tuyết Bông tuyết",
            movementType = "Spring Drive Cal. 9R65",
            waterResistance = "100m / 10ATM"
        ),
        ProductEntity(
            productCode = "TUD-M79030N",
            name = "Tudor Black Bay Fifty-Eight 39mm",
            brand = "Tudor",
            category = "Diver",
            wholesalePrice = 85000000.0,
            retailPrice = 99000000.0,
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

    suspend fun checkAndSeed(dao: ProductDao) = withContext(Dispatchers.IO) {
        if (dao.getProductCount() == 0) {
            dao.insertAll(sampleProducts)
        }
    }
}

