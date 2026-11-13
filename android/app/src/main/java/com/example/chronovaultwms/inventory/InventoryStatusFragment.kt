package com.example.chronovaultwms.inventory

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.chronovaultwms.R
import com.google.android.material.tabs.TabLayout

class InventoryStatusFragment : Fragment(R.layout.fragment_inventory_status) {

    private val viewModel: InventoryViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

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
    }
}