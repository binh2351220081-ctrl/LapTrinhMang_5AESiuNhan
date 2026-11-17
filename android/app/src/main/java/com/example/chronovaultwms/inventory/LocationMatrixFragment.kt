package com.example.chronovaultwms.inventory

import android.app.AlertDialog
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.GridLayout
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import com.example.chronovaultwms.R
import com.example.chronovaultwms.core.auth.SessionManager

class LocationMatrixFragment : Fragment(R.layout.fragment_inventory_location_matrix) {

    private val viewModel: InventoryViewModel by viewModels()
    private lateinit var sessionManager: SessionManager

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        sessionManager = SessionManager(requireContext())

        val gridK1 = view.findViewById<GridLayout>(R.id.gridK1)
        val gridK2 = view.findViewById<GridLayout>(R.id.gridK2)

        setupBinGrid(gridK1, listOf("K1-A01", "K1-A02", "K1-B01", "K1-B02", "K1-C01"))
        setupBinGrid(gridK2, listOf("K2-A01", "K2-A02", "K2-B01"))

        // Gắn sự kiện mở dialog điều chuyển vị trí kệ
        view.findViewById<Button>(R.id.btnRelocateBin).setOnClickListener {
            showRelocateDialog()
        }
    }

    private fun setupBinGrid(grid: GridLayout, bins: List<String>) {
        grid.removeAllViews()
        for (bin in bins) {
            val cellView = TextView(requireContext()).apply {
                text = bin
                setTextColor(Color.WHITE)
                gravity = android.view.Gravity.CENTER
                // Giả lập màu trạng thái: Xanh (Trống), Vàng (Chứa hàng), Đỏ (Đầy)
                setBackgroundColor(Color.parseColor("#4CAF50"))
                setPadding(16, 24, 16, 24)
                layoutParams = GridLayout.LayoutParams().apply {
                    width = 220
                    height = 160
                    setMargins(8, 8, 8, 8)
                }
                setOnClickListener {
                    Toast.makeText(context, "Chọn ngăn kệ: $bin", Toast.LENGTH_SHORT).show()
                    // Sau này có thể mở danh sách Serial cụ thể trong ngăn này tại đây
                }
            }
            grid.addView(cellView)
        }
    }

    private fun showRelocateDialog() {
        val dialogView = layoutInflater.inflate(R.layout.dialog_inventory_relocate, null)
        val edtSerial = dialogView.findViewById<EditText>(R.id.edtRelocateSerial)
        val edtNewBin = dialogView.findViewById<EditText>(R.id.edtNewBinLocation)
        val btnCancel = dialogView.findViewById<Button>(R.id.btnCancelRelocate)
        val btnConfirm = dialogView.findViewById<Button>(R.id.btnConfirmRelocate)

        val dialog = AlertDialog.Builder(requireContext())
            .setView(dialogView)
            .create()

        btnCancel.setOnClickListener { dialog.dismiss() }

        btnConfirm.setOnClickListener {
            val serialNumber = edtSerial.text.toString().trim()
            val newBin = edtNewBin.text.toString().trim()
            val currentUsername = sessionManager.getFullName() ?: "Warehouse Operator"

            if (serialNumber.isEmpty() || newBin.isEmpty()) {
                Toast.makeText(requireContext(), "Vui lòng nhập đầy đủ mã Serial và mã ngăn kệ mới!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            // Gọi ViewModel cập nhật vị trí ngăn kệ trong Database Room DB
            viewModel.relocateSerialBin(serialNumber, newBin, currentUsername)
            Toast.makeText(requireContext(), "Đã điều chuyển Serial đến ngăn $newBin thành công!", Toast.LENGTH_SHORT).show()
            dialog.dismiss()
        }

        dialog.show()
    }
}