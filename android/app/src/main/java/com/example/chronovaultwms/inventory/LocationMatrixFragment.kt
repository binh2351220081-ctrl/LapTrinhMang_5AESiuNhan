package com.example.chronovaultwms.inventory

import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.GridLayout
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.chronovaultwms.R

class LocationMatrixFragment : Fragment(R.layout.fragment_inventory_location_matrix) {

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val gridK1 = view.findViewById<GridLayout>(R.id.gridK1)
        val gridK2 = view.findViewById<GridLayout>(R.id.gridK2)

        setupBinGrid(gridK1, listOf("K1-A01", "K1-A02", "K1-B01", "K1-B02", "K1-C01"))
        setupBinGrid(gridK2, listOf("K2-A01", "K2-A02", "K2-B01"))
    }

    private fun setupBinGrid(grid: GridLayout, bins: List<String>) {
        grid.removeAllViews()
        for (bin in bins) {
            val cellView = TextView(requireContext()).apply {
                text = bin
                setTextColor(Color.WHITE)
                gravity = View.TEXT_ALIGNMENT_CENTER
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
                    // Mở danh sách Serial hoặc dialog điều chuyển RelocateBinDialog
                }
            }
            grid.addView(cellView)
        }
    }
}