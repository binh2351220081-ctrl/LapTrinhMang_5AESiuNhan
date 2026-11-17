package com.example.chronovaultwms.outbound

import androidx.room.Room
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.example.chronovaultwms.core.database.*
import com.example.chronovaultwms.dashboard.data.RoomDashboardRepository
import com.example.chronovaultwms.dashboard.model.DateRange
import com.example.chronovaultwms.dashboard.model.ReportType
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.runBlocking
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import java.time.LocalDate

@RunWith(AndroidJUnit4::class)
class OutboundRepositoryInstrumentedTest {
    private lateinit var db: ChronoVaultDatabase
    private lateinit var repository: OutboundRepository
    private val operator = OutboundActor("Tô Đức Thảo", "OPERATIONS_STAFF")
    private val manager = OutboundActor("Võ Công Tâm", "WAREHOUSE_MANAGER")
    private val owner = OutboundActor("Chủ kho", "STORE_OWNER")

    @Before fun setup() = runBlocking {
        db = Room.inMemoryDatabaseBuilder(InstrumentationRegistry.getInstrumentation().targetContext, ChronoVaultDatabase::class.java).build()
        repository = OutboundRepository(db)
        db.productDao().insert(ProductEntity("SKU-A", "Đồng hồ A", "Test", "Test", 100.0, 0.0, 5, "40", "Đen", "Cơ", "10ATM", conversionRate = 2))
        db.dealerDao().insert(DealerEntity("UNIT-A", "Đơn vị A", "NORMAL", 0.0, 0.0, 0.0, "0900000000", "Kho nhận A", "MST-A"))
        db.dealerDao().insert(DealerEntity("UNIT-B", "Đơn vị A", "NORMAL", 0.0, 0.0, 0.0, "0900000001", "Kho nhận B", "MST-B"))
        (1..5).forEach { number ->
            db.serialDao().insert(SerialEntity("A-$number", "SKU-A", "IN_STOCK", "K1-A0$number", "0$number/01/2026 08:00", 100.0, "Đơn vị giao"))
        }
    }

    @After fun teardown() { db.close() }

    private suspend fun draft(quantity: Int) = repository.createDraft("UNIT-A", listOf(OutboundLineRequest("SKU-A", false, quantity)), "Xuất điều phối", operator)

    @Test fun reservationCancelDispatchReturnPreserveTheStockLedger() = runBlocking {
        val cancelled = draft(2)
        repository.approveOrder(cancelled, manager)
        assertEquals(2, db.serialDao().getAllSerials().count { it.status == "ALLOCATED" })
        assertEquals(5, db.serialDao().newPhysicalCount("SKU-A"))
        repository.cancelOrder(cancelled, "Đơn vị nhận đổi lịch", operator)
        assertEquals(5, db.serialDao().getAllSerials().count { it.status == "IN_STOCK" })

        val code = draft(2)
        repository.approveOrder(code, manager)
        repository.startPacking(code, operator)
        val numbers = repository.pickingList(code).map { it.serialNumber }
        assertEquals(listOf("A-1", "A-2"), numbers)
        numbers.forEach { repository.recordScan(code, it, operator) }
        assertEquals(numbers, repository.scannedSerials(code))
        val document = repository.completeDispatch(code, numbers, "Xe kho", "VD-001", manager)
        val repeated = repository.completeDispatch(code, numbers, "Xe kho", "VD-001", manager)
        assertEquals(document.code, repeated.code)
        assertEquals(3, db.serialDao().newPhysicalCount("SKU-A"))
        assertEquals(2, db.outboundWorkflowDao().allMovements().size)
        assertEquals(0.0, db.dealerDao().getDealerById("UNIT-A")!!.currentDebt, 0.0)

        val returnCode = repository.receiveReturn("UNIT-A", numbers.first(), "HANG_MOI", "Nguyên seal, xác nhận nhập lại", manager)
        assertEquals(returnCode, repository.receiveReturn("UNIT-A", numbers.first(), "HANG_MOI", "Nguyên seal, xác nhận nhập lại", manager))
        assertEquals(4, db.serialDao().newPhysicalCount("SKU-A"))
        assertEquals(3, db.outboundWorkflowDao().allMovements().size)
        assertTrue(db.outboundWorkflowDao().pendingCount() > 0)
        val reports = RoomDashboardRepository(db)
        val range = DateRange(LocalDate.of(2000, 1, 1), LocalDate.of(2100, 1, 1))
        val outboundReport = reports.loadReport(ReportType.OUTBOUND, range)
        assertEquals(document.code, outboundReport.rows.single().values[0])
        assertEquals("2", outboundReport.rows.single().values[4])
        val returnsReport = reports.loadReport(ReportType.RETURNS_QUALITY, range)
        assertEquals(returnCode, returnsReport.rows.single().values[0])
        assertEquals(document.code, returnsReport.rows.single().values[1])
        val ledger = reports.loadReport(ReportType.CASHFLOW, range)
        assertEquals(3, ledger.rows.size)
        assertEquals(-1, ledger.rows.sumOf { it.values[5].toInt() })
    }

    @Test fun competingApprovalsCannotAllocateTheSameSerial() = runBlocking {
        val one = draft(3)
        val two = draft(3)
        val results = listOf(one, two).map { code -> async(Dispatchers.IO) { runCatching { repository.approveOrder(code, manager) }.isSuccess } }.awaitAll()
        assertEquals(1, results.count { it })
        assertEquals(3, db.serialDao().getAllSerials().count { it.status == "ALLOCATED" })
        assertEquals(2, db.serialDao().getAllSerials().count { it.status == "IN_STOCK" })
    }

    @Test fun multiSkuOrderReservesAndDispatchesEveryLine() = runBlocking {
        db.productDao().insert(ProductEntity("SKU-B", "Đồng hồ B", "Test", "Test", 200.0, 0.0, 2, "40", "Trắng", "Cơ", "10ATM"))
        (1..2).forEach { db.serialDao().insert(SerialEntity("B-$it", "SKU-B", "IN_STOCK", "K2-B0$it", "01/01/2026", 200.0, "Đơn vị giao")) }
        val code = repository.createDraft("UNIT-A", listOf(OutboundLineRequest("SKU-A", true, 1), OutboundLineRequest("SKU-B", false, 1)), "Hai SKU", operator)
        repository.approveOrder(code, manager)
        val picks = repository.pickingList(code)
        assertEquals(3, picks.size)
        picks.forEach { repository.recordScan(code, it.serialNumber, operator) }
        val document = repository.completeDispatch(code, picks.map { it.serialNumber }, "Xe kho", "VD-MULTI", manager)
        assertEquals(2, document.lines.size)
        assertEquals(3, document.serials.size)
        assertEquals(3, db.serialDao().newPhysicalCount("SKU-A"))
        assertEquals(1, db.serialDao().newPhysicalCount("SKU-B"))
    }

    @Test fun rolesScansAndDealerIdentityAreCheckedAtCommit() = runBlocking {
        val code = draft(2)
        assertTrue(runCatching { repository.approveOrder(code, operator) }.isFailure)
        repository.approveOrder(code, manager)
        val numbers = repository.pickingList(code).map { it.serialNumber }
        assertTrue(runCatching { repository.completeDispatch(code, numbers, "", "", manager) }.isFailure)
        repository.recordScan(code, numbers.first(), operator)
        assertTrue(runCatching { repository.recordScan(code, numbers.first(), operator) }.isFailure)
        repository.recordScan(code, numbers.last(), operator)
        assertTrue(runCatching { repository.completeDispatch(code, numbers, "", "", operator) }.isFailure)
        repository.completeDispatch(code, numbers, "", "", manager)
        assertTrue(runCatching { repository.receiveReturn("UNIT-B", numbers.first(), "HANG_MOI", "Sai đơn vị", manager) }.isFailure)
        assertEquals("DISPATCHED", db.serialDao().getSerialByNumber(numbers.first())!!.status)
    }

    @Test fun aSerialChangedAfterScanningRollsBackTheWholeDispatch() = runBlocking {
        val code = draft(2)
        repository.approveOrder(code, manager)
        val numbers = repository.pickingList(code).map { it.serialNumber }
        numbers.forEach { repository.recordScan(code, it, operator) }
        val damaged = db.serialDao().getSerialByNumber(numbers.last())!!
        db.serialDao().update(damaged.copy(status = "DEFECTIVE"))
        assertTrue(runCatching { repository.completeDispatch(code, numbers, "", "", manager) }.isFailure)
        assertEquals("ALLOCATED", db.serialDao().getSerialByNumber(numbers.first())!!.status)
        assertNull(db.outboundWorkflowDao().dispatchForOrder(code))
        assertTrue(db.outboundWorkflowDao().allMovements().isEmpty())
    }

    @Test fun destructionRequiresOwnerAndCreatesARealDocument() = runBlocking {
        val defective = SerialEntity("ERR-1", "SKU-A", "DEFECTIVE", "Kho Lỗi C-01", "01/01/2026", 100.0, "Đơn vị giao")
        db.serialDao().insert(defective)
        assertTrue(runCatching { repository.recordOtherDispatch("ERR-1", "TIEU_HUY", "Biên bản BB-01", manager) }.isFailure)
        assertEquals("DEFECTIVE", db.serialDao().getSerialByNumber("ERR-1")!!.status)
        val code = repository.recordOtherDispatch("ERR-1", "TIEU_HUY", "Biên bản BB-01", owner)
        assertEquals(code, repository.recordOtherDispatch("ERR-1", "TIEU_HUY", "Biên bản BB-01", owner))
        assertEquals("LIQUIDATED", db.serialDao().getSerialByNumber("ERR-1")!!.status)
        assertEquals(1, db.outboundWorkflowDao().allOtherDispatches().size)
        assertEquals(-1, db.outboundWorkflowDao().allMovements().single().changeQuantity)
    }
}
