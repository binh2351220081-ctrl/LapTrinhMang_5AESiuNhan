package com.example.chronovaultwms.inventory

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.example.chronovaultwms.R
import com.example.chronovaultwms.core.auth.SessionManager

class StockAuditActivity : AppCompatActivity() {

    private val viewModel: InventoryViewModel by viewModels()
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_stock_audit) // Khởi tạo layout kiểm kê

        sessionManager = SessionManager(this)
        
        // Kiểm tra quyền hạn Quản lý kho hoặc Nhân viên vận hành
        val currentUser = sessionManager.getCurrentUser() 

        val btnStartAudit = findViewById<Button>(R.id.btnStartAudit)
        val txtAuditSummary = findViewById<TextView>(R.id.txtAuditSummary)

        btnStartAudit.setOnClickListener {
            // Giả lập quét danh sách Serial thực tế qua Camera/Barcode
            val scannedList = listOf("ROLEX-001", "ROLEX-002", "SURPLUS-999")
            val targetBin = "K1-A01"

            viewModel.performStockAudit(targetBin, scannedList, currentUser ?: "Admin")
        }

        viewModel.auditResult.observe(this) { result ->
            txtAuditSummary.text = """
                Khớp đúng: ${result.matched.size}
                Thừa kho: ${result.surplus.size}
                Thiếu kho: ${result.deficit.size}
            """.trimIndent()
        }
    }
}