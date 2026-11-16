package com.example.chronovaultwms.dashboard.export

import android.content.ContentValues
import android.content.Context
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import com.example.chronovaultwms.dashboard.model.ReportTable
import java.io.File

object ReportExportManager {
    fun exportCsv(context: Context, report: ReportTable): String {
        val fileName = "ChronoVault_${report.type.name}_${report.period.from}_${report.period.to}.csv"
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
            val directory = File(context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), "ChronoVault").apply { mkdirs() }
            val file = File(directory, fileName)
            file.bufferedWriter(Charsets.UTF_8).use { writeCsv(it, report) }
            return file.absolutePath
        }
        val values = ContentValues().apply {
            put(MediaStore.Downloads.DISPLAY_NAME, fileName)
            put(MediaStore.Downloads.MIME_TYPE, "text/csv")
            put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/ChronoVault")
        }
        val uri = requireNotNull(context.contentResolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values))
        context.contentResolver.openOutputStream(uri)?.bufferedWriter(Charsets.UTF_8).use { writer ->
            requireNotNull(writer)
            writeCsv(writer, report)
        }
        return fileName
    }

    private fun writeCsv(writer: java.io.Writer, report: ReportTable) {
        writer.write("\uFEFF")
        writer.appendLine(report.title)
        writer.appendLine("Từ ngày,${report.period.from}")
        writer.appendLine("Đến ngày,${report.period.to}")
        writer.appendLine(report.headers.joinToString(",", transform = ::escape))
        report.rows.forEach { writer.appendLine(it.values.joinToString(",", transform = ::escape)) }
        writer.appendLine()
        writer.appendLine(escape(report.summary))
    }
    private fun escape(value: String) = "\"${value.replace("\"", "\"\"")}\""
}
