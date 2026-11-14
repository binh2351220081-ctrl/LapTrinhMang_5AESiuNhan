package com.example.chronovaultwms.dashboard.export

import android.content.Context
import android.print.PrintAttributes
import android.print.PrintManager
import android.webkit.WebView
import android.webkit.WebViewClient
import com.example.chronovaultwms.dashboard.model.ReportTable

object ReportPrintManager {
    fun printA4(context: Context, report: ReportTable) {
        val webView = WebView(context)
        webView.settings.defaultTextEncodingName = "utf-8"
        webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView, url: String?) {
                val manager = context.getSystemService(Context.PRINT_SERVICE) as PrintManager
                manager.print("ChronoVault - ${report.title}", view.createPrintDocumentAdapter("ChronoVault_${report.type.name}"),
                    PrintAttributes.Builder().setMediaSize(PrintAttributes.MediaSize.ISO_A4).setColorMode(PrintAttributes.COLOR_MODE_COLOR).build())
            }
        }
        webView.loadDataWithBaseURL(null, toHtml(report), "text/html", "UTF-8", null)
    }

    private fun toHtml(report: ReportTable): String {
        val header = report.headers.joinToString("") { "<th>${html(it)}</th>" }
        val rows = report.rows.joinToString("") { row -> "<tr>${row.values.joinToString("") { "<td>${html(it)}</td>" }}</tr>" }
        return """<!doctype html><html><head><meta charset="utf-8"><style>
            @page{size:A4;margin:14mm}body{font-family:sans-serif;color:#172033;font-size:11px}
            h1{color:#1A2332}table{width:100%;border-collapse:collapse}th{background:#1A2332;color:white;text-align:left}
            th,td{border:1px solid #ddd;padding:7px}tr:nth-child(even){background:#F6F4EF}.summary{margin-top:14px;font-weight:bold}
            </style></head><body><h1>${html(report.title)}</h1><p>${report.period.from} - ${report.period.to}</p>
            <table><thead><tr>$header</tr></thead><tbody>$rows</tbody></table><div class="summary">${html(report.summary)}</div></body></html>"""
    }
    private fun html(value: String) = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
}
