package com.example.chronovaultwms.dashboard.ui.view

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View
import com.example.chronovaultwms.dashboard.model.CostSlice
import kotlin.math.min

class CostDonutChartView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null
) : View(context, attrs) {
    private var values: List<CostSlice> = emptyList()
    private val colors = listOf("#1A2332", "#D4AF37", "#667085", "#A98319").map(Color::parseColor)
    private val arcPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.STROKE; strokeWidth = 30f * resources.displayMetrics.density }
    private val textPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.parseColor("#172033"); textSize = 12f * resources.displayMetrics.scaledDensity }

    fun submitData(newValues: List<CostSlice>) { values = newValues; invalidate() }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        if (values.isEmpty()) return
        val size = min(width * .48f, height * .74f)
        val centerX = paddingLeft + size / 2f + 16f
        val centerY = height / 2f
        val radius = size / 2f - arcPaint.strokeWidth / 2f
        val oval = RectF(centerX - radius, centerY - radius, centerX + radius, centerY + radius)
        val total = values.sumOf { it.amount }.coerceAtLeast(1.0)
        var start = -90f
        values.forEachIndexed { index, item ->
            val sweep = (item.amount / total * 360).toFloat()
            arcPaint.color = colors[index % colors.size]
            canvas.drawArc(oval, start, sweep, false, arcPaint)
            start += sweep
        }
        val legendX = width * .56f
        values.forEachIndexed { index, item ->
            val y = paddingTop + 28f + index * 34f
            val dot = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = colors[index % colors.size] }
            canvas.drawCircle(legendX, y, 7f, dot)
            canvas.drawText("${item.label}: ${String.format("%.1f%%", item.amount * 100 / total)}", legendX + 18f, y + 5f, textPaint)
        }
    }
}
