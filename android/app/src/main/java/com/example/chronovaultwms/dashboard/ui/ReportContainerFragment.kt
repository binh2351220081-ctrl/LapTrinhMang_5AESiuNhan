package com.example.chronovaultwms.dashboard.ui

import android.app.DatePickerDialog
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.chronovaultwms.R
import com.example.chronovaultwms.dashboard.DashboardOverviewFragment
import com.example.chronovaultwms.dashboard.export.ReportExportManager
import com.example.chronovaultwms.dashboard.export.ReportPrintManager
import com.example.chronovaultwms.dashboard.model.ReportTable
import com.example.chronovaultwms.dashboard.model.ReportType
import com.example.chronovaultwms.dashboard.ui.adapter.ReportRowAdapter
import com.example.chronovaultwms.databinding.FragmentDashboardReportContainerBinding
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.format.DateTimeFormatter

class ReportContainerFragment : Fragment() {
    private var _binding: FragmentDashboardReportContainerBinding? = null
    private val binding get() = _binding!!
    private val viewModel: ReportViewModel by viewModels()
    private val rowAdapter = ReportRowAdapter()
    private var currentReport: ReportTable? = null
    private val dateFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy")

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, state: Bundle?): View {
        _binding = FragmentDashboardReportContainerBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, state: Bundle?) {
        binding.rvReportRows.apply { layoutManager = LinearLayoutManager(requireContext()); adapter = rowAdapter }
        val reportTypes = ReportType.entries
        binding.reportTypeDropdown.setAdapter(ArrayAdapter(requireContext(), android.R.layout.simple_list_item_1, reportTypes.map { it.displayName }))
        binding.reportTypeDropdown.setText(reportTypes.first().displayName, false)
        binding.reportTypeDropdown.setOnItemClickListener { _, _, position, _ -> viewModel.selectType(reportTypes[position]) }
        binding.btnFromDate.setOnClickListener { showDatePicker(true) }
        binding.btnToDate.setOnClickListener { showDatePicker(false) }
        binding.btnExportCsv.setOnClickListener { exportCurrentReport() }
        binding.btnPrint.setOnClickListener { currentReport?.let { ReportPrintManager.printA4(requireContext(), it) } }
        binding.btnDashboardBack.setOnClickListener { returnToDashboard() }
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) { viewModel.state.collect(::render) }
        }
    }

    private fun render(state: ReportUiState) = with(binding) {
        btnFromDate.text = "Từ ${state.range.from.format(dateFormatter)}"
        btnToDate.text = "Đến ${state.range.to.format(dateFormatter)}"
        reportTypeDropdown.setText(state.selectedType.displayName, false)
        btnExportCsv.isEnabled = !state.loading && state.report != null
        btnPrint.isEnabled = !state.loading && state.report != null
        state.error?.let { tvReportSummary.text = it }
        state.report?.let { report ->
            currentReport = report
            tvReportSummary.text = if (state.loading) "Đang tổng hợp dữ liệu liên phân hệ…" else report.summary
            rowAdapter.submitData(report.headers, report.rows)
        }
    }

    private fun showDatePicker(isFrom: Boolean) {
        val current = if (isFrom) viewModel.state.value.range.from else viewModel.state.value.range.to
        DatePickerDialog(requireContext(), { _, year, month, day ->
            val picked = LocalDate.of(year, month + 1, day)
            if (isFrom) viewModel.setFrom(picked) else viewModel.setTo(picked)
        }, current.year, current.monthValue - 1, current.dayOfMonth).show()
    }

    private fun exportCurrentReport() {
        val report = currentReport ?: return
        runCatching { ReportExportManager.exportCsv(requireContext(), report) }
            .onSuccess { Toast.makeText(requireContext(), "Đã xuất báo cáo: $it", Toast.LENGTH_LONG).show() }
            .onFailure { Toast.makeText(requireContext(), "Xuất CSV thất bại: ${it.message}", Toast.LENGTH_LONG).show() }
    }

    private fun returnToDashboard() {
        if (!parentFragmentManager.popBackStackImmediate()) {
            parentFragmentManager.beginTransaction()
                .replace(R.id.fragmentContainer, DashboardOverviewFragment())
                .commit()
        }
    }

    override fun onDestroyView() { super.onDestroyView(); _binding = null }
}
