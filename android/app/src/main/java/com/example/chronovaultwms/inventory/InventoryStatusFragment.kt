package com.example.chronovaultwms.inventory

import android.app.AlertDialog
import android.os.Bundle
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import com.example.chronovaultwms.R
import com.example.chronovaultwms.core.auth.SessionManager
import com.google.android.material.tabs.TabLayout

class InventoryStatusFragment : Fragment(R.layout.fragment_inventory_status) {

    private val viewModel: InventoryViewModel by viewModels()
    private lateinit var sessionManager: SessionManager

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        sessionManager = SessionManager(requireContext())

        val tabLayout = view.findViewById<TabLayout>(R.id.tabLayoutQuality)
        tabLayout.addTab(tabLayout.newTab().setText("Mới Chuẩn"))
        tabLayout.addTab(tabLayout.newTab().setText("Trưng Bày"))
        tabLayout.addTab(tabLayout.newTab().setText("Lỗi / Chờ Xử Lý"))

        // Mặc định load nhóm HANG_MOI
        viewModel.loadSerialsByQuality("HANG_MOI")

        tabLayout.addOnTabSelectedListener(object : TabLayout.OnTabSelectedListener {
            override fun onTabSelected(tab: TabLayout.Tab?) {
                when (tab?.position) {
                    0 -> viewModel.loadSerialsByQuality("HANG_MOI")
                    1 -> viewModel.loadSerialsByQuality("TRUNG_BAY")
                    2 -> viewModel.loadSerialsByQuality("HANG_LOI")
                }
            }
            override fun onTabUnselected(tab: TabLayout.Tab?) {}
            override fun onTabReselected(tab: TabLayout.Tab?) {}
        })

        // Gắn sự kiện mở dialog đổi trạng thái chất lượng
        view.findViewById<Button>(R.id.btnOpenChangeQualityDialog).setOnClickListener {
            showChangeQualityDialog()
        }
    }

    private fun showChangeQualityDialog() {
        val dialogView = layoutInflater.inflate(R.layout.dialog_inventory_change_quality, null)
        val edtSerialNumber = dialogView.findViewById<EditText>(R.id.edtSerialNumber)
        val spinnerStatus = dialogView.findViewById<Spinner>(R.id.spinnerQualityStatus)
        val edtReason = dialogView.findViewById<EditText>(R.id.edtReason)
        val btnCancel = dialogView.findViewById<Button>(R.id.btnCancel)
        val btnConfirm = dialogView.findViewById<Button>(R.id.btnConfirm)

        val statuses = arrayOf("HANG_MOI", "TRUNG_BAY", "HANG_LOI")
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, statuses)
        spinnerStatus.adapter = adapter

        val dialog = AlertDialog.Builder(requireContext())
            .setView(dialogView)
            .create()

        btnCancel.setOnClickListener { dialog.dismiss() }

        btnConfirm.setOnClickListener {
            val serialNumber = edtSerialNumber.text.toString().trim()
            val newQuality = spinnerStatus.selectedItem.toString()
            val reason = edtReason.text.toString().trim()
            val currentUsername = sessionManager.getFullName() ?: "System Operator"

            if (serialNumber.isEmpty() || reason.isEmpty()) {
                Toast.makeText(requireContext(), "Vui lòng nhập đầy đủ mã Serial và lý do kỹ thuật!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Gọi ViewModel thực hiện đổi trạng thái và ghi Audit Log
            viewModel.changeSerialQuality(serialNumber, newQuality, reason, currentUsername)
            Toast.makeText(requireContext(), "Đã chuyển đổi trạng thái thành công!", Toast.LENGTH_SHORT).show()
            dialog.dismiss()
        }

        dialog.show()
    }
}