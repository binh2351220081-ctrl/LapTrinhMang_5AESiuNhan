package com.example.chronovaultwms.outbound

import com.example.chronovaultwms.core.database.DatabaseSeeder
import com.example.chronovaultwms.core.database.OutboundOrderEntity
import com.example.chronovaultwms.core.database.SerialEntity
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Assert.assertThrows
import org.junit.Test

/**
 * Bộ kiểm thử đơn vị (Unit Test) Phân hệ 3: Điều Phối Xuất Kho & Đơn Vị Tiếp Nhận (TV3 - Tô Đức Thảo).
 * Kiểm chứng toàn bộ dữ liệu mẫu DatabaseSeeder và 6 kịch bản TC-01..TC-06 trong 2 file báo cáo TV3.
 */
class OutboundLogisticsManagerTest {

    private fun galleWatchDealer() = DatabaseSeeder.sampleDealers.first { it.dealerId == "DL-GALLE" }
    // A deliberately larger stock fixture isolates the optional legacy valuation arithmetic.
    private fun rolexSubmariner() = DatabaseSeeder.sampleProducts.first { it.productCode == "RLX-126610LN" }.copy(stockQuantity = 14)
    private fun ds2026001() = DatabaseSeeder.sampleOrders.first { it.orderCode == "DS-2026-001" }

    @Test
    fun databaseSeeder_matchesReportAppendixAAndLogisticsData() {
        val galle = galleWatchDealer()
        assertEquals("Galle Watch Việt Nam", galle.name)
        assertEquals("VIP", galle.tier)
        assertEquals(0.25, galle.discountPercent, 0.0001)
        assertEquals(3_000_000_000.0, galle.creditLimit, 0.01)
        assertEquals(1_800_000_000.0, galle.currentDebt, 0.01)
        assertEquals("ACTIVE", galle.status)

        val rolex = DatabaseSeeder.sampleProducts.first { it.productCode == "RLX-126610LN" }
        assertEquals("Rolex Submariner Date 41mm", rolex.name)
        assertEquals(350_000_000.0, rolex.wholesalePrice, 0.01)
        assertEquals(14, rolex.stockQuantity)

        val order = ds2026001()
        assertEquals(350_000_000.0, order.unitPrice, 0.01)
        assertEquals(0.25, order.discountPercent, 0.0001)
        assertEquals(525_000_000.0, order.totalAmount, 0.01)
        assertEquals(150_000_000.0, order.depositAmount, 0.01)
        assertEquals(375_000_000.0, order.remainingDebt, 0.01)
        assertEquals("DRAFT", order.status)

        val serialLot1 = DatabaseSeeder.sampleSerials.first { it.serialNumber == "RLX-SUB-2026-001" }
        assertEquals("IN_STOCK", serialLot1.status)
        assertEquals("Kệ K1-A02-B03", serialLot1.currentLocation)
        assertEquals(285_000_000.0, serialLot1.unitCost, 0.01)

        val serialLot2 = DatabaseSeeder.sampleSerials.first { it.serialNumber == "RLX-SUB-2026-002" }
        assertEquals("IN_STOCK", serialLot2.status)
        assertEquals("Két VIP-02", serialLot2.currentLocation)
        assertEquals(295_000_000.0, serialLot2.unitCost, 0.01)

        val totalCustody = DatabaseSeeder.sampleDealers.sumOf { it.currentDebt }
        assertEquals(3_950_000_000.0, totalCustody, 0.01)

        val tv3Logs = DatabaseSeeder.sampleAuditLogs.filter { it.actorName == "Tô Đức Thảo" }
        assertTrue(tv3Logs.isNotEmpty())
        assertEquals("LẬP_LỆNH_XUẤT_NHÁP", tv3Logs.first().action)
    }

    @Test
    fun tc01_exceedingAssetCustodyLimit_blocksOutboundApproval() {
        val eval = OutboundLogisticsManager.evaluateOutboundOrder(
            dealer = galleWatchDealer(),
            product = rolexSubmariner(),
            isBox = false,
            quantity = 5,
            collateralDeposit = 0.0,
            reservedQuantity = 0
        )

        assertEquals(5, eval.convertedQuantity)
        assertEquals(1_312_500_000.0, eval.totalValuation, 0.01)
        assertEquals(1_312_500_000.0, eval.newCustodyLiability, 0.01)
        assertEquals(3_112_500_000.0, eval.projectedCustody, 0.01)
        assertEquals(112_500_000.0, eval.excessCustodyAmount, 0.01)
        assertTrue(eval.isOverCustodyLimit)
        assertFalse(eval.canSubmit)
        assertNotNull(eval.rejectionReason)
        assertTrue(eval.rejectionReason!!.contains("HẠN MỨC BẢO LÃNH"))
    }

    @Test
    fun tc02_validOutboundOrder_reservesInventoryAndChecksAvailableStock() {
        val eval = OutboundLogisticsManager.evaluateOutboundOrder(
            dealer = galleWatchDealer(),
            product = rolexSubmariner(),
            isBox = false,
            quantity = 2,
            collateralDeposit = 150_000_000.0,
            reservedQuantity = 0
        )

        assertEquals(2, eval.convertedQuantity)
        assertEquals(525_000_000.0, eval.totalValuation, 0.01)
        assertEquals(375_000_000.0, eval.newCustodyLiability, 0.01)
        assertEquals(2_175_000_000.0, eval.projectedCustody, 0.01)
        assertFalse(eval.isOverCustodyLimit)
        assertTrue(eval.canSubmit)

        // Sau khi DS-2026-001 (2 chiếc) giữ chỗ, tồn khả dụng của Rolex giảm từ 14 xuống 12 chiếc
        val reservedMap = OutboundLogisticsManager.calculateReservedByProduct(DatabaseSeeder.sampleOrders.map {
            if (it.orderCode == "DS-2026-001") it.copy(status = "RESERVED") else it
        })
        val rolexReserved = reservedMap["RLX-126610LN"] ?: 0
        assertEquals(2, rolexReserved)
        assertEquals(12, OutboundLogisticsManager.calculateAvailableStock(14, rolexReserved))

        // Một lệnh khác yêu cầu 13 chiếc (> 12 chiếc khả dụng) phải bị chặn chống xuất âm kho
        val overStockEval = OutboundLogisticsManager.evaluateOutboundOrder(
            dealer = DatabaseSeeder.sampleDealers.first { it.dealerId == "DL-XWATCH" }.copy(creditLimit = 10_000_000_000.0),
            product = rolexSubmariner(),
            isBox = false,
            quantity = 13,
            collateralDeposit = 0.0,
            reservedQuantity = rolexReserved
        )
        assertTrue(overStockEval.isInsufficientStock)
        assertFalse(overStockEval.canSubmit)
    }

    @Test
    fun tc03_duplicateSerialScan_blocksDuplicateInSamePackage() {
        val order = ds2026001()
        val rolexSerials = DatabaseSeeder.sampleSerials.filter { it.productCode == order.productCode }
        val pickingList = OutboundLogisticsManager.generateSmartPickingList(rolexSerials, order.productCode, order.convertedQuantity)
        val s1 = rolexSerials.first { it.serialNumber == "RLX-SUB-2026-001" }

        val firstScan = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = "RLX-SUB-2026-001",
            order = order,
            serialEntity = s1,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertTrue(firstScan.isValid)

        val duplicateScan = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = "RLX-SUB-2026-001",
            order = order,
            serialEntity = s1,
            pickingList = pickingList,
            alreadyScanned = listOf("RLX-SUB-2026-001"),
            allProductSerials = rolexSerials
        )
        assertFalse(duplicateScan.isValid)
        assertTrue(duplicateScan.errorMessage!!.contains("đã được quét rồi"))
    }

    @Test
    fun tc04_wrongSkuOrDefectiveOrDisplayOrAllocatedSerial_blocksDispatch() {
        val order = ds2026001()
        val rolexSerials = DatabaseSeeder.sampleSerials.filter { it.productCode == order.productCode }
        val pickingList = OutboundLogisticsManager.generateSmartPickingList(rolexSerials, order.productCode, order.convertedQuantity)

        // 1. Quét nhầm SKU Omega vào lệnh Rolex
        val omegaSerial = DatabaseSeeder.sampleSerials.first { it.serialNumber == "OMG-SPEED-2026-001" }
        val wrongSkuResult = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = omegaSerial.serialNumber,
            order = order,
            serialEntity = omegaSerial,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertFalse(wrongSkuResult.isValid)
        assertTrue(wrongSkuResult.errorMessage!!.contains("không khớp với mã SKU"))

        // 2. Quét nhầm Serial hàng lỗi cách ly (DEFECTIVE: RLX-SUB-2026-ERR hoặc RX-9921 theo báo cáo TC-05)
        val defectiveSerial = DatabaseSeeder.sampleSerials.first { it.serialNumber == "RLX-SUB-2026-ERR" }
        val defectiveResult = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = defectiveSerial.serialNumber,
            order = order,
            serialEntity = defectiveSerial,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertFalse(defectiveResult.isValid)
        assertTrue(defectiveResult.errorMessage!!.contains("DEFECTIVE"))

        val rx9921Serial = DatabaseSeeder.sampleSerials.first { it.serialNumber == "RX-9921" }
        val rx9921Result = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = rx9921Serial.serialNumber,
            order = order,
            serialEntity = rx9921Serial,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertFalse(rx9921Result.isValid)
        assertTrue(rx9921Result.errorMessage!!.contains("DEFECTIVE"))

        // Đối soát SKU chuẩn hóa: RLX-SUB-126610LN tương đương RLX-126610LN
        assertEquals("RLX-126610LN", OutboundLogisticsManager.normalizeProductCode("RLX-SUB-126610LN"))
        assertEquals("RLX-126610LN", OutboundLogisticsManager.normalizeProductCode("RLX-126610LN"))
        val normalizedOrder = order.copy(productCode = "RLX-SUB-126610LN")
        val validSerial = rolexSerials.first { it.serialNumber == "RLX-SUB-2026-001" }
        val normSkuResult = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = validSerial.serialNumber,
            order = normalizedOrder,
            serialEntity = validSerial,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertTrue(normSkuResult.isValid)

        // 3. Quét nhầm hàng trưng bày (DISPLAY) hoặc hàng đã khóa giữ chỗ khác (ALLOCATED)
        val displaySerial = defectiveSerial.copy(serialNumber = "RLX-SUB-DISP", status = "DISPLAY")
        val displayResult = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = displaySerial.serialNumber,
            order = order,
            serialEntity = displaySerial,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertFalse(displayResult.isValid)
        assertTrue(displayResult.errorMessage!!.contains("DISPLAY"))

        val allocatedSerial = defectiveSerial.copy(serialNumber = "RLX-SUB-ALLOC", status = "ALLOCATED")
        val allocResult = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = allocatedSerial.serialNumber,
            order = order,
            serialEntity = allocatedSerial,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertFalse(allocResult.isValid)
        assertTrue(allocResult.errorMessage!!.contains("ALLOCATED"))
    }

    @Test
    fun tc05_clearanceVoucher_reducesCustodyAndRestoresDispatchLimit() {
        val galle = galleWatchDealer()
        val clearance = OutboundLogisticsManager.validateClearanceVoucher(
            amount = 200_000_000.0,
            currentCustody = galle.currentDebt
        )

        assertTrue(clearance.isValid)
        assertEquals(1_600_000_000.0, clearance.remainingCustody, 0.01)

        // Sau khi giải phóng 200tr, tổng giữ còn 1.6 tỷ nên lệnh 5 chiếc Rolex (1.3125 tỷ) sẽ hợp lệ (2.9125B <= 3.0B)
        val reEvaluated = OutboundLogisticsManager.evaluateOutboundOrder(
            dealer = galle.copy(currentDebt = clearance.remainingCustody),
            product = rolexSubmariner(),
            isBox = false,
            quantity = 5,
            collateralDeposit = 0.0,
            reservedQuantity = 0
        )
        assertTrue(reEvaluated.canSubmit)
        assertEquals(2_912_500_000.0, reEvaluated.projectedCustody, 0.01)

        // Vượt quá số đang giữ hoặc <= 0 phải bị từ chối
        assertFalse(OutboundLogisticsManager.validateClearanceVoucher(0.0, galle.currentDebt).isValid)
        assertFalse(OutboundLogisticsManager.validateClearanceVoucher(1_900_000_000.0, galle.currentDebt).isValid)
    }

    @Test
    fun tc06_smartPickingListFifoAndWrongLotBatchRejection() {
        val order = ds2026001() // 2 chiếc Rolex Submariner
        val rolexSerials = DatabaseSeeder.sampleSerials.filter { it.productCode == order.productCode }

        // FIFO phải chỉ định 2 chiếc Lô 1 (nhập 15/10, vốn 285tr): -001 và -004
        val pickingList = OutboundLogisticsManager.generateSmartPickingList(
            productSerials = rolexSerials,
            productCode = order.productCode,
            requiredQty = order.convertedQuantity
        )

        assertEquals(2, pickingList.size)
        assertEquals("RLX-SUB-2026-001", pickingList[0].serialNumber)
        assertEquals("Kệ K1-A02-B03", pickingList[0].currentLocation)
        assertEquals(285_000_000.0, pickingList[0].unitCost, 0.01)
        assertEquals(1, pickingList[0].lotNumber)

        assertEquals("RLX-SUB-2026-004", pickingList[1].serialNumber)
        assertEquals("Kệ K1-A02-B04", pickingList[1].currentLocation)
        assertEquals(285_000_000.0, pickingList[1].unitCost, 0.01)

        // Nếu NV đến nhầm Két VIP-02 lấy chiếc Lô 2 (RLX-SUB-2026-002, vốn 295tr) quét vào lệnh -> BỊ CHẶN!
        val lot2Serial = rolexSerials.first { it.serialNumber == "RLX-SUB-2026-002" }
        val wrongLotScan = OutboundLogisticsManager.validateScannedSerial(
            inputSerial = lot2Serial.serialNumber,
            order = order,
            serialEntity = lot2Serial,
            pickingList = pickingList,
            alreadyScanned = emptyList(),
            allProductSerials = rolexSerials
        )
        assertFalse(wrongLotScan.isValid)
        assertNotNull(wrongLotScan.errorMessage)
        assertTrue(wrongLotScan.errorMessage!!.contains("Lô 2"))
        assertTrue(wrongLotScan.errorMessage!!.contains("Két VIP-02"))
        assertTrue(wrongLotScan.errorMessage!!.contains("295,000,000"))

        // Verify cross-month chronological FIFO ordering key (Oct 15 < Oct 25 < Nov 01)
        assertTrue(
            OutboundLogisticsManager.parseImportDateKey("15/10/2026 09:30") <
                OutboundLogisticsManager.parseImportDateKey("01/11/2026 08:00")
        )
    }

    @Test
    fun unitConversionBoxToPiece_moq_andLockedBranchChecks() {
        assertEquals(10, OutboundLogisticsManager.convertQuantity(isBox = true, quantity = 1))
        assertEquals(0, OutboundLogisticsManager.convertQuantity(isBox = true, quantity = 0))

        // MOQ enforcement: đặt 2 chiếc khi yêu cầu MOQ = 5 -> bị chặn
        val belowMoq = OutboundLogisticsManager.evaluateOutboundOrder(
            dealer = galleWatchDealer().copy(creditLimit = 10_000_000_000.0),
            product = rolexSubmariner(),
            isBox = false,
            quantity = 2,
            collateralDeposit = 0.0,
            reservedQuantity = 0,
            minOrderQty = 5
        )
        assertTrue(belowMoq.isBelowMoq)
        assertFalse(belowMoq.canSubmit)

        // Chi nhánh đang LOCKED -> bị chặn
        val lockedDealer = galleWatchDealer().copy(status = "LOCKED")
        val lockedEval = OutboundLogisticsManager.evaluateOutboundOrder(
            dealer = lockedDealer,
            product = rolexSubmariner(),
            isBox = false,
            quantity = 1,
            collateralDeposit = 0.0,
            reservedQuantity = 0
        )
        assertTrue(lockedEval.isDealerLocked)
        assertFalse(lockedEval.canSubmit)

        // Box quy đổi 1 thùng = 10 chiếc trong khả dụng (14)
        val omega = DatabaseSeeder.sampleProducts.first { it.productCode == "OMG-310304250" }.copy(stockQuantity = 22) // arithmetic fixture
        val boxEval = OutboundLogisticsManager.evaluateOutboundOrder(
            dealer = DatabaseSeeder.sampleDealers.first { it.dealerId == "DL-HAITRIEU" }.copy(creditLimit = 5_000_000_000.0),
            product = omega,
            isBox = true,
            quantity = 1,
            collateralDeposit = 0.0,
            reservedQuantity = 0
        )
        assertEquals(10, boxEval.convertedQuantity)
        assertTrue(boxEval.canSubmit)
    }

    @Test
    fun nonCommercialDispatchAndWarehouseReturn_enforceApprovalAndOrigin() {
        val defectiveSerial = DatabaseSeeder.sampleSerials.first { it.serialNumber == "RLX-SUB-2026-ERR" }

        // Xuất tiêu hủy: NV Kho thường bị chặn; Chỉ STORE_OWNER mới được duyệt
        val deniedDestroy = OutboundLogisticsManager.evaluateNonCommercialDispatch(
            serial = defectiveSerial,
            purpose = OutboundLogisticsManager.PURPOSE_DESTROY,
            actorRole = "OPERATIONS_STAFF"
        )
        assertFalse(deniedDestroy.isValid)

        val approvedDestroy = OutboundLogisticsManager.evaluateNonCommercialDispatch(
            serial = defectiveSerial,
            purpose = OutboundLogisticsManager.PURPOSE_DESTROY,
            actorRole = "STORE_OWNER"
        )
        assertTrue(approvedDestroy.isValid)
        assertEquals(OutboundLogisticsManager.SERIAL_DESTROYED, approvedDestroy.targetStatus)

        val warrantyResult = OutboundLogisticsManager.evaluateNonCommercialDispatch(
            serial = defectiveSerial,
            purpose = OutboundLogisticsManager.PURPOSE_WARRANTY,
            actorRole = "OPERATIONS_STAFF"
        )
        assertTrue(warrantyResult.isValid)
        assertEquals(OutboundLogisticsManager.SERIAL_WARRANTY, warrantyResult.targetStatus)

        // Xuất bán thanh lý hàng trưng bày (F4.3.3)
        val displaySerial = defectiveSerial.copy(serialNumber = "RLX-SUB-DISP", status = "DISPLAY")
        val liquidationResult = OutboundLogisticsManager.evaluateNonCommercialDispatch(
            serial = displaySerial,
            purpose = OutboundLogisticsManager.PURPOSE_LIQUIDATION,
            actorRole = "OPERATIONS_STAFF"
        )
        assertTrue(liquidationResult.isValid)
        assertEquals(OutboundLogisticsManager.SERIAL_LIQUIDATED, liquidationResult.targetStatus)

        // Tiếp nhận hoàn trả (MOD-03-04): Đúng đơn vị từng xuất mới nhận, phân loại Kho Mới / Kho Lỗi C-01
        val dispatchedOmega = DatabaseSeeder.sampleSerials.first { it.serialNumber == "OMG-SPEED-2026-001" }
        val wrongDealerReturn = OutboundLogisticsManager.evaluateWarehouseReturn(
            serial = dispatchedOmega,
            returningDealerName = "Galle Watch",
            inspectedCondition = "HANG_MOI"
        )
        assertFalse(wrongDealerReturn.isValid)

        val validNewReturn = OutboundLogisticsManager.evaluateWarehouseReturn(
            serial = dispatchedOmega,
            returningDealerName = "Đồng Hồ Hải Triều",
            inspectedCondition = "HANG_MOI"
        )
        assertTrue(validNewReturn.isValid)
        assertEquals(OutboundLogisticsManager.SERIAL_IN_STOCK, validNewReturn.targetStatus)
        assertEquals("Kho Mới (Khu K1)", validNewReturn.targetWarehouseZone)

        val validDefectiveReturn = OutboundLogisticsManager.evaluateWarehouseReturn(
            serial = dispatchedOmega,
            returningDealerName = "Đồng Hồ Hải Triều",
            inspectedCondition = "DEFECTIVE"
        )
        assertTrue(validDefectiveReturn.isValid)
        assertEquals(OutboundLogisticsManager.SERIAL_DEFECTIVE, validDefectiveReturn.targetStatus)
        assertEquals("Kho Lỗi C-01", validDefectiveReturn.targetWarehouseZone)
    }

    @Test
    fun outboundNetworkClient_formatsBearerHeaderAndBuildsRfc8259JsonPayloads() {
        assertEquals("Bearer eyJhbGci", OutboundNetworkClient.formatBearerHeader("eyJhbGci"))
        assertEquals("Bearer already_prefixed", OutboundNetworkClient.formatBearerHeader("Bearer already_prefixed"))
        assertThrows(IllegalArgumentException::class.java) { OutboundNetworkClient.formatBearerHeader(null) }

        val order = ds2026001()
        val reservedJson = OutboundNetworkClient.buildStockReservedPayload(order)
        assertTrue(reservedJson.contains("\"eventType\":\"EVENT_STOCK_RESERVED\""))
        assertTrue(reservedJson.contains("\"orderCode\":\"DS-2026-001\""))
        assertTrue(reservedJson.contains("\"dealerId\":\"DL-GALLE\""))
        assertTrue(reservedJson.contains("\"actorName\":\"Tô Đức Thảo\""))

        val dispatchedJson = OutboundNetworkClient.buildDispatchCompletedPayload(
            order = order,
            serials = listOf("RLX-SUB-2026-001", "RLX-SUB-2026-004"),
            timestamp = "26/03/2026 14:30"
        )
        assertTrue(dispatchedJson.contains("\"eventType\":\"EVENT_DISPATCH_COMPLETED\""))
        assertTrue(dispatchedJson.contains("RLX-SUB-2026-001"))
        assertTrue(dispatchedJson.contains("RLX-SUB-2026-004"))
        assertTrue(dispatchedJson.contains("26/03/2026 14:30"))
    }
}

