package com.example.chronovaultwms.dashboard

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.chronovaultwms.R
import com.example.chronovaultwms.dashboard.model.DashboardSnapshot
import com.example.chronovaultwms.dashboard.ui.DashboardViewModel
import com.example.chronovaultwms.dashboard.ui.ReportContainerFragment
import com.example.chronovaultwms.dashboard.ui.adapter.ActivityAdapter
import com.example.chronovaultwms.dashboard.ui.adapter.TopProductAdapter
import com.example.chronovaultwms.databinding.FragmentDashboardOverviewBinding
import com.example.chronovaultwms.product.ProductListFragment
import kotlinx.coroutines.launch
import java.text.NumberFormat
import java.util.Locale

/** TV5 - Trần Công Tú: Dashboard và báo cáo, đọc dữ liệu liên phân hệ qua Room DAO dùng chung. */
class DashboardOverviewFragment : Fragment() {
    private var _binding: FragmentDashboardOverviewBinding? = null
    private val binding get() = _binding!!
    private val viewModel: DashboardViewModel by viewModels()
    private val topProductAdapter = TopProductAdapter()
    private val activityAdapter = ActivityAdapter()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, state: Bundle?): View {
        _binding = FragmentDashboardOverviewBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, state: Bundle?) {
        binding.rvTopProducts.apply { layoutManager = LinearLayoutManager(requireContext()); adapter = topProductAdapter }
        binding.rvActivities.apply { layoutManager = LinearLayoutManager(requireContext()); adapter = activityAdapter }
        binding.btnDashboardReports.setOnClickListener { open(ReportContainerFragment()) }
        binding.btnDashboardProducts.setOnClickListener { open(ProductListFragment()) }
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.dashboard.collect { it?.let(::render) }
            }
        }
    }

    private fun open(fragment: Fragment) {
        parentFragmentManager.beginTransaction().replace(R.id.fragmentContainer, fragment).addToBackStack(null).commit()
    }

    private fun render(snapshot: DashboardSnapshot) = with(binding) {
        tvPeriod.text = snapshot.periodLabel
        tvInventoryValue.text = money(snapshot.kpis.inventoryAssetValue)
        tvRevenue.text = money(snapshot.kpis.wholesaleRevenue)
        tvNewOrders.text = snapshot.kpis.newWholesaleOrders.toString()
        tvAvailableStock.text = "${snapshot.kpis.availableStock} chiếc"
        tvReturnRate.text = String.format(Locale.forLanguageTag("vi-VN"), "%.2f%%", snapshot.kpis.returnRatePercent)
        tvReturnRate.setTextColor(ContextCompat.getColor(requireContext(), if (snapshot.kpis.returnRatePercent > 2) R.color.dashboard_danger else R.color.dashboard_success))
        revenueChart.submitData(snapshot.monthlyRevenue)
        costChart.submitData(snapshot.costStructure)
        topProductAdapter.submitList(snapshot.topProducts)
        activityAdapter.submitList(snapshot.recentActivities)
    }

    private fun money(value: Double) = NumberFormat.getCurrencyInstance(Locale.forLanguageTag("vi-VN")).format(value)
    override fun onDestroyView() { super.onDestroyView(); _binding = null }
}
