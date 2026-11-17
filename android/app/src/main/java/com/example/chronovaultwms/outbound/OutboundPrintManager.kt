package com.example.chronovaultwms.outbound

import android.content.Context
import android.os.Bundle
import android.os.CancellationSignal
import android.os.ParcelFileDescriptor
import android.print.PageRange
import android.print.PrintAttributes
import android.print.PrintDocumentAdapter
import android.print.PrintManager
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast

/** Uses Android's print dialog, which also offers Save as PDF. No HTML data is fetched online. */
object OutboundPrintManager {
    fun print(context: Context, document: OutboundDocument) {
        val manager = context.getSystemService(Context.PRINT_SERVICE) as? PrintManager ?: return
        val webView = WebView(context)
        webView.settings.javaScriptEnabled = false
        webView.settings.allowFileAccess = false
        webView.settings.allowContentAccess = false
        webView.webViewClient = object : WebViewClient() {
            private var printed = false
            override fun onPageFinished(view: WebView, url: String?) {
                if (printed) return
                printed = true
                val delegate = view.createPrintDocumentAdapter("ChronoVault_${document.code}")
                val adapter = object : PrintDocumentAdapter() {
                    override fun onStart() = delegate.onStart()
                    override fun onLayout(oldAttributes: PrintAttributes?, newAttributes: PrintAttributes?, cancellationSignal: CancellationSignal?, callback: LayoutResultCallback?, extras: Bundle?) =
                        delegate.onLayout(oldAttributes, newAttributes, cancellationSignal, callback, extras)
                    override fun onWrite(pages: Array<out PageRange>?, destination: ParcelFileDescriptor?, cancellationSignal: CancellationSignal?, callback: WriteResultCallback?) =
                        delegate.onWrite(pages, destination, cancellationSignal, callback)
                    override fun onFinish() {
                        delegate.onFinish()
                        view.destroy()
                    }
                }
                runCatching {
                    manager.print("Phiếu xuất ${document.code}", adapter, PrintAttributes.Builder().setMediaSize(PrintAttributes.MediaSize.ISO_A4).setColorMode(PrintAttributes.COLOR_MODE_MONOCHROME).build())
                }.onFailure {
                    view.destroy()
                    Toast.makeText(context, "Không mở được dịch vụ in. Vui lòng thử lại.", Toast.LENGTH_LONG).show()
                }
            }
        }
        webView.loadDataWithBaseURL(null, buildHtml(document), "text/html", "UTF-8", null)
    }

    internal fun buildHtml(document: OutboundDocument): String {
        val rows = document.lines.joinToString("") {
            "<tr><td>${html(it.productCode)}</td><td>${html(it.productName)}</td><td>${it.quantity} ${if (it.unit == "BOX") "thùng" else "chiếc"}</td><td>${it.convertedQuantity}</td></tr>"
        }
        val serialRows = document.serials.mapIndexed { index, serial ->
            "<tr><td>${index + 1}</td><td>${html(serial.productCode)}</td><td>${html(serial.serialNumber)}</td><td>${html(serial.currentLocation)}</td></tr>"
        }.joinToString("")
        return """<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>
            @page { size: A4; margin: 15mm; } body { font-family: sans-serif; font-size: 11pt; color: #111; }
            h1 { font-size: 17pt; text-align: center; margin: 12pt 0 4pt; } h2 { font-size: 12pt; margin-top: 18pt; }
            p { line-height: 1.5; margin: 5pt 0; } table { width: 100%; border-collapse: collapse; margin-top: 8pt; }
            th, td { border: 1px solid #999; padding: 6pt; text-align: left; overflow-wrap: anywhere; }
            th { background: #eee; } thead { display: table-header-group; } tr { page-break-inside: avoid; }
            .signatures { display: table; width: 100%; margin-top: 25pt; break-inside: avoid; }
            .signature { display: table-cell; width: 25%; text-align: center; height: 85pt; font-size: 10pt; }
            .meta { font-size: 10pt; color: #444; } .note { white-space: pre-wrap; }
            </style></head><body><p><b>CHRONOVAULT WMS</b> · Quản lý kho chứa đồng hồ</p>
            <h1>PHIẾU XUẤT KHO KIÊM BIÊN BẢN BÀN GIAO</h1>
            <p style="text-align:center">Số phiếu: <b>${html(document.code)}</b> · Lệnh: ${html(document.orderCode)}</p>
            <p>Ngày giờ xuất: <b>${html(document.createdAt)}</b></p>
            <p>Đơn vị nhận: <b>${html(document.dealerName)}</b></p><p>Địa chỉ nhận: ${html(document.address)}</p>
            <p>Đơn vị/người vận chuyển: ${html(document.carrier.ifBlank { "Không ghi nhận" })} · Mã vận đơn: ${html(document.trackingNumber.ifBlank { "Không ghi nhận" })}</p>
            <h2>Danh sách hàng xuất</h2><table><thead><tr><th>Mã SKU</th><th>Mẫu đồng hồ</th><th>Số lượng theo ĐVT</th><th>Quy đổi chiếc</th></tr></thead><tbody>$rows</tbody></table>
            <h2>Bảng kê Serial đích danh (${document.serials.size} chiếc)</h2><table><thead><tr><th>STT</th><th>SKU</th><th>Serial</th><th>Vị trí xuất phát</th></tr></thead><tbody>$serialRows</tbody></table>
            <p class="note">Lý do/ghi chú: ${html(document.note)}</p>
            <p class="meta">Người lập: ${html(document.createdBy)} · Người duyệt: ${html(document.approvedBy)} · Người xuất: ${html(document.dispatchedBy)}</p>
            <div class="signatures"><div class="signature"><b>Người lập</b><br>(Ký, ghi rõ họ tên)</div><div class="signature"><b>Thủ kho xác nhận</b><br>(Ký, ghi rõ họ tên)</div><div class="signature"><b>Người vận chuyển</b><br>(Ký, ghi rõ họ tên)</div><div class="signature"><b>Đơn vị nhận</b><br>(Ký, ghi rõ họ tên)</div></div>
            </body></html>""".trimIndent()
    }

    private fun html(value: String) = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#39;")
}
