package com.example.chronovaultwms.dashboard.ui.view

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View
import com.example.chronovaultwms.dashboard.model.MonthlyRevenue
import kotlin.math.max

class RevenueBarChartView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null
) : View(context, attrs) {
    private var values: List<MonthlyRevenue> = emptyList()
    private val barPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.parseColor("#D4AF37") }
    private val labelPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#667085"); textAlign = Paint.Align.CENTER; textSize = 12f * resources.displayMetrics.scaledDensity
    }
    private val valuePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.parseColor("#1A2332"); textAlign = Paint.Align.CENTER; textSize = 10f * resources.displayMetrics.scaledDensity
    }

    fun submitData(newValues: List<MonthlyRevenue>) { values = newValues; invalidate() }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (values.isEmpty()) return
        val chartTop = paddingTop + 28f
        val chartBottom = height - paddingBottom - 32f
        val usableHeight = max(1f, chartBottom - chartTop)
        val slot = (width - paddingLeft - paddingRight).toFloat() / values.size
        val maxValue = values.maxOf { it.revenue }.coerceAtLeast(1.0)
        values.forEachIndexed { index, item ->
            val center = paddingLeft + slot * index + slot / 2f
            val barWidth = slot * .52f
            val barHeight = (item.revenue / maxValue * usableHeight).toFloat()
            canvas.drawRoundRect(RectF(center - barWidth / 2, chartBottom - barHeight, center + barWidth / 2, chartBottom), 12f, 12f, barPaint)
            canvas.drawText(item.monthLabel, center, height - paddingBottom.toFloat(), labelPaint)
            canvas.drawText(String.format("%.1f tỷ", item.revenue / 1_000_000_000), center, chartBottom - barHeight - 8f, valuePaint)
        }
    }
}
