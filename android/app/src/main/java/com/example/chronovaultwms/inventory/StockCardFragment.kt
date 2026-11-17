package com.example.chronovaultwms.inventory

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.chronovaultwms.R

class StockCardFragment : Fragment(R.layout.fragment_inventory_stock_card) {

    private val viewModel: InventoryViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val edtSearchKey = view.findViewById<EditText>(R.id.edtSearchCardKey)
        val btnSearch = view.findViewById<Button>(R.id.btnSearchStockCard)
        val recyclerCard = view.findViewById<RecyclerView>(R.id.recyclerStockCard)

        recyclerCard.layoutManager = LinearLayoutManager(requireContext())

        // Xử lý sự kiện tra cứu lịch sử thẻ kho
        btnSearch.setOnClickListener {
            val queryKey = edtSearchKey.text.toString().trim()
            if (queryKey.isNotEmpty()) {
                Toast.makeText(requireContext(), "Đang tra cứu lịch sử thẻ kho cho: $queryKey", Toast.LENGTH_SHORT).show()
                // Sau khi bổ sung hàm tương ứng trong ViewModel, gọi tại đây
            } else {
                Toast.makeText(requireContext(), "Vui lòng nhập mã SKU hoặc Serial cần tra cứu!", Toast.LENGTH_SHORT).show()
            }
        }
    }
}