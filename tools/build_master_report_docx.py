# -*- coding: utf-8 -*-
"""
Script: tools/build_master_report_docx.py
Mục đích: Tích hợp toàn diện tài liệu từ 3 file báo cáo của:
- Nguyễn Đắc Quân (TV2 - Phân hệ Đối tác NCC & Nhập kho)
- Tô Đức Thảo (TV3 - Phân hệ Đối tác Đại lý & Xuất kho B2B)
- Trần Công Tú (TV5 - Phân hệ Executive Dashboard & 9 Báo cáo)
cùng phần việc của Phan Bá Hải Bình (TV1 - Trưởng nhóm & Quản trị Danh mục Luxury)
vào file Word chính thức:
D:\\cntt\\pbhb\\Document\\BAO_CAO_PHAN_TICH_HE_THONG_THONG_TIN_CHRONOVAULT_WMS.docx
theo đúng chuẩn mẫu của Khoa CNTT - Đại học Kiến trúc Đà Nẵng (Document/Mẫu báo cáo.docx).
Cam kết: 100% không còn từ "bán sỉ / sỉ", giữ nguyên 8 câu hỏi phụ lục hiện tại.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_master_report():
    template_path = r"D:\cntt\pbhb\Document\Mẫu báo cáo.docx"
    output_path = r"D:\cntt\pbhb\Document\BAO_CAO_PHAN_TICH_HE_THONG_THONG_TIN_CHRONOVAULT_WMS.docx"
    
    doc = Document(template_path)
    
    # Bảng màu Luxury Horology chuẩn nhận diện
    C_NAVY = RGBColor(27, 54, 93)      # #1B365D - Xanh Navy chủ đạo
    C_GOLD = RGBColor(197, 155, 39)    # #C59B27 - Vàng Gold điểm nhấn
    C_SLATE = RGBColor(51, 65, 85)     # #334155 - Xám đá đậm nội dung
    C_GRAY = RGBColor(100, 116, 139)   # #64748B - Xám ghi ghi chú
    HEX_NAVY = "1B365D"
    HEX_GOLD = "C59B27"
    HEX_ALT = "F8FAFC"
    HEX_WHITE = "FFFFFF"

    def set_cell_background(cell, hex_color):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def set_cell_margins(cell, top=60, bottom=60, left=70, right=70):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'''
            <w:tcMar {nsdecls("w")}>
                <w:top w:w="{top}" w:type="dxa"/>
                <w:bottom w:w="{bottom}" w:type="dxa"/>
                <w:left w:w="{left}" w:type="dxa"/>
                <w:right w:w="{right}" w:type="dxa"/>
            </w:tcMar>
        ''')
        tcPr.append(tcMar)

    def format_row(row, bg_color, is_header=False, font_size=9, bold=False):
        for cell in row.cells:
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                if is_header:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(font_size)
                    r.font.bold = is_header or bold
                    r.font.color.rgb = RGBColor(255, 255, 255) if is_header else C_SLATE

    def add_p_after(anchor_elem, text="", bold=False, italic=False, font_size=10, color_rgb=C_SLATE, 
                    space_before=4, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, font_name="Arial"):
        p_xml = parse_xml(f'<w:p {nsdecls("w")}/>')
        anchor_elem.addnext(p_xml)
        p = docx.text.paragraph.Paragraph(p_xml, doc._body)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = align
        if text:
            run = p.add_run(text)
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.italic = italic
            if color_rgb:
                run.font.color.rgb = color_rgb
        return p, p_xml

    def add_table_after(anchor_elem, num_rows, num_cols):
        tbl = doc.add_table(num_rows, num_cols)
        anchor_elem.addnext(tbl._tbl)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        return tbl, tbl._tbl

    # =============================================================
    # LƯU THAM CHIẾU CỐ ĐỊNH TỚI 11 BẢNG GỐC CỦA TEMPLATE TRƯỚC KHI CHÈN
    # =============================================================
    orig_tables = [t for t in doc.tables]
    orig_tbl_xmls = [t._tbl for t in orig_tables]

    # =============================================================
    # BƯỚC 1: CẬP NHẬT CÁC ĐOẠN VĂN BẢN GỐC (COVER & TEXT)
    # =============================================================
    for p in doc.paragraphs:
        txt = p.text
        if "ĐỀ TÀI:" in txt:
            p.text = "ĐỀ TÀI: HỆ THỐNG QUẢN LÝ KHO & PHÂN PHỐI ĐỒNG HỒ CAO CẤP B2B (CHRONOVAULT WMS)"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "Người hướng dẫn khoa học" in txt:
            p.text = "Người hướng dẫn khoa học\t: TS. Đặng Hùng Vĩ"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True
        elif "Nhóm sinh viên thực hiện" in txt:
            p.text = "Nhóm sinh viên thực hiện\t: Nhóm 5 AE Siêu Nhân"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True
        elif "Lớp \t:" in txt:
            p.text = (
                "Sinh viên phụ trách báo cáo\t: Phan Bá Hải Bình (Nhóm trưởng / System Architect / Phân hệ 1)\n"
                "Thành viên tích hợp báo cáo\t: Nguyễn Đắc Quân (TV2 - NCC & Nhập kho), Tô Đức Thảo (TV3 - Đại lý & Xuất kho), Trần Công Tú (TV5 - Dashboard & Báo cáo)\n"
                "Thành viên liên kết\t\t: Võ Công Tâm (TV4 - Kệ kho & Kiểm kê thẻ kho)"
            )
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10)
        elif "Khóa\t: 2023" in txt:
            p.text = "Khóa\t\t\t\t: 2023 - 2026\nHọc phần\t\t\t: Phân Tích Hệ Thống Thông Tin & Lập Trình Mạng"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10)
        elif "Tên ứng dụng (đề xuất):" in txt:
            p.text = "Tên ứng dụng: Hệ Thống Quản Lý Kho & Phân Phối Đồng Hồ Cao Cấp B2B (ChronoVault WMS)"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "Bao gồm 3 thành phần:" in txt:
            p.text = (
                "Phân tích 3 thành phần cấu thành tên đề tài theo chuẩn khoa học:\n"
                "• Loại hình / Hành động: Hệ thống Quản trị Kho vận đa cấp & Điều phối Chuỗi cung ứng đại lý B2B (Warehouse Management System - WMS).\n"
                "• Chức năng chính: Quản lý định danh Serial Number 100%, Tự động quy đổi Đơn vị tính (ĐVT) đa cấp (Thùng - Chiếc lẻ), Kiểm soát hạn mức công nợ & khóa giữ chỗ tồn kho (Reservation), Hạch toán giá vốn đích danh (Specific Identification Costing).\n"
                "• Đối tượng / Lĩnh vực: Ngành phân phối đồng hồ cao cấp xa xỉ (Luxury Horology Wholesale Distribution)."
            )
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10); r.font.color.rgb = C_SLATE
        elif "Đưa ra bảng so sánh khoảng 3-5 phần mềm" in txt:
            p.text = (
                "Bảng 1.1: So sánh đối chiếu phần mềm ChronoVault WMS với các giải pháp quản lý kho trên thị trường\n"
                "(Minh chứng tính cấp thiết và giải quyết bài toán đặc thù của ngành phân phối đồng hồ xa xỉ):"
            )
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "Phân hệ" == txt.strip():
            p.text = (
                "HỆ THỐNG PHÂN RÃ CHỨC NĂNG TÍCH HỢP 4 PHÂN HỆ (FUNCTIONAL DECOMPOSITION TREE):\n\n"
                "MOD-01: Phân hệ Quản trị Hệ thống & Danh mục Luxury Horology (Phan Bá Hải Bình)\n"
                "├── F1.1: Quản trị Xác thực & Kiểm soát Phân quyền Người dùng (RBAC 5 Roles)\n"
                "│    ├── F1.1.1: Đăng nhập bảo mật & Khởi tạo phiên làm việc (SessionManager)\n"
                "│    ├── F1.1.2: Phân quyền theo 5 vai trò hệ thống (SYSTEM_ADMIN, STORE_OWNER, WAREHOUSE_MANAGER, OPERATIONS_STAFF, ACCOUNTANT)\n"
                "│    └── F1.1.3: Quản lý danh sách tài khoản & Khóa/Mở khóa nhân viên vi phạm\n"
                "└── F1.2: Quản lý Danh mục Đồng hồ Cao cấp (Luxury Horology Master Data)\n"
                "     ├── F1.2.1: Quản lý Thông số Kỹ thuật Chuyên ngành (SKU, Brand, Bộ máy, Kính Sapphire, Vỏ, Kháng nước)\n"
                "     ├── F1.2.2: Thiết lập Đơn vị tính Đa cấp (Thùng - Chiếc) & Tỷ lệ Quy đổi conversionRate\n"
                "     └── F1.2.3: Thiết lập Ngưỡng cảnh báo Tồn kho An toàn (Min / Max Stock Alert)\n\n"
                "MOD-02: Phân hệ Quản lý Đối tác NCC & Nhập kho Quy đổi ĐVT (Nguyễn Đắc Quân)\n"
                "├── F2.1: Quản lý Hồ sơ Nhà cung cấp & Theo dõi Công nợ Phải trả\n"
                "│    ├── F2.1.1: Khai báo đối tác NCC xa xỉ (Rolex Geneva, Patek Salons, Omega Biel), kiểm tra trùng MST\n"
                "│    └── F2.1.2: Sổ theo dõi công nợ phải trả theo thời gian thực và lập ủy nhiệm chi thanh toán\n"
                "└── F2.2: Tiếp nhận Hóa đơn & Nhập kho Quy đổi ĐVT Đa cấp\n"
                "     ├── F2.2.1: Tự động quy đổi số lượng Thùng/Kiện ra số chiếc lẻ (Tổng = Thùng × Tỷ lệ + Lẻ)\n"
                "     ├── F2.2.2: Quét mã vạch Serial 100% bằng Camera ML Kit, chặn trùng lặp mã tuyệt đối\n"
                "     ├── F2.2.3: Thuật toán Phân bổ Chi phí Logistics (vận chuyển, hải quan, bảo hiểm) vào từng Serial\n"
                "     └── F2.2.4: Lập phiếu xuất trả hàng lỗi kỹ thuật cho Nhà cung cấp và giảm trừ công nợ\n\n"
                "MOD-03: Phân hệ Đối tác Đại lý & Quản lý Xuất kho B2B (Tô Đức Thảo)\n"
                "├── F3.1: Quản lý Đại lý B2B & Kiểm soát Hạn mức Tín dụng (Credit Limit Enforcement)\n"
                "│    ├── F3.1.1: Khai báo danh bạ đại lý pháp nhân (Galle Watch, Donghochinhhang), phân cấp VIP\n"
                "│    ├── F3.1.2: Thiết lập hạn mức tín dụng công nợ và tự động khóa nút duyệt đơn khi vượt hạn mức\n"
                "│    └── F3.1.3: Lập phiếu thu tiền đại lý, cấn trừ công nợ và tiếp nhận đổi trả đại lý\n"
                "└── F3.2: Quy trình Tạo Lệnh Xuất kho & Quét Camera Serial Thực Xuất B2B\n"
                "     ├── F3.2.1: Tạo đơn xuất kho đại lý B2B và kích hoạt cơ chế Khóa giữ chỗ tồn kho (Reservation Engine)\n"
                "     ├── F3.2.2: Quy trình xuất kho 2 bước (Picking List soạn hàng & Dispatch đóng kiện)\n"
                "     ├── F3.2.3: Quét mã vạch Serial 100% bằng Camera ML Kit đối soát khớp với danh sách giữ chỗ, chặn hàng lỗi DEFECTIVE\n"
                "     └── F3.2.4: Kết xuất và in ấn Chứng từ giao hàng B2B kiêm Phiếu xuất kho chuẩn khổ A4\n\n"
                "MOD-05: Phân hệ Executive Dashboard & Hệ thống 9 Báo cáo Quản trị (Trần Công Tú)\n"
                "├── F5.1: Executive Dashboard 5 Thẻ Chỉ số KPI Điều hành Thời gian thực\n"
                "│    ├── F5.1.1: Tổng giá trị tài sản tồn kho theo giá vốn đích danh\n"
                "│    ├── F5.1.2: Doanh thu xuất kho đại lý và Số lượng đơn xuất kho mới\n"
                "│    ├── F5.1.3: Tồn kho khả dụng và Cảnh báo Tỷ lệ đổi trả vượt ngưỡng an toàn (> 2%)\n"
                "│    └── F5.1.4: Biểu đồ biến động doanh thu 6 tháng liên tiếp bằng thư viện MPAndroidChart\n"
                "└── F5.2: Trung tâm Báo cáo Quản trị Chuyên sâu & Kết xuất Đa định dạng\n"
                "     ├── F5.2.1: Hệ thống 9 Báo cáo Chuyên sâu (BC01 Nhập hàng, BC02 Đại lý, BC03 Cơ cấu xuất, BC04 Đổi trả, BC05 Chậm luân chuyển, BC06 Lợi nhuận gộp, BC07 Công nợ, BC08 Dòng tiền, BC09 Audit Log)\n"
                "     ├── F5.2.2: Bộ lọc thời gian linh hoạt (Hôm nay, Tuần này, Tháng này, Tùy chọn)\n"
                "     └── F5.2.3: Xuất báo cáo ra tệp CSV (Downloads/ChronoVault) và In ấn chuẩn khổ A4 qua Android PrintManager"
            )
            for r in p.runs:
                r.font.name = "Consolas"; r.font.size = Pt(8); r.font.color.rgb = C_NAVY
        elif "└── Chức năng" in txt or "└── Chức năng cấp 1" in txt or "└── Chức năng cấp n (Module)" in txt:
            p.text = ""
        elif "Mã Module: [MOD-XX-YY]" in txt:
            p.text = (
                "Module IPO 1: MOD-01-02 — Khai báo Danh mục Sản phẩm Đồng hồ Cao cấp & Thiết lập Tỷ lệ Quy đổi ĐVT\n"
                "Thuộc phân hệ: MOD-01 (Quản trị Hệ thống & Danh mục Luxury Horology — Phan Bá Hải Bình phụ trách)\n"
                "Mức độ ưu tiên: Cao (Bắt buộc hoàn thành)"
            )
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "Bảng: [tên_bảng]" in txt:
            p.text = "6.2.1. Chi tiết thuộc tính bảng `products` (Danh mục Sản phẩm Đồng hồ Cao cấp & Cấu hình ĐVT Quy đổi — TV1 Bình):"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "[Bảng A] 1 ──── N [Bảng B]" in txt:
            p.text = (
                "SƠ ĐỒ MỐI QUAN HỆ CƠ SỞ DỮ LIỆU CỐT LÕI (CORE ROOM DATABASE v4 RELATIONSHIPS):\n\n"
                "• [brands] 1 ──────────── N [products] (Một thương hiệu chế tác nhiều mẫu đồng hồ xa xỉ)\n"
                "• [products] 1 ────────── N [serials] (Một mẫu đồng hồ có nhiều mã Serial định danh đích danh 100%)\n"
                "• [suppliers] 1 ───────── N [inbound_receipts] (Một nhà cung cấp phát hành nhiều chứng từ nhập hàng)\n"
                "• [inbound_receipts] 1 ── N [serials] (Một phiếu nhập chứa danh sách Serial thực nhận đã phân bổ giá vốn)\n"
                "• [suppliers] 1 ───────── N [payment_vouchers] (Một nhà cung cấp tiếp nhận nhiều phiếu chi giảm trừ nợ)\n"
                "• [dealers] 1 ─────────── N [outbound_orders] (Một đại lý tiếp nhận nhiều lệnh xuất phân phối)\n"
                "• [outbound_orders] 1 ─── N [serials] (Một lệnh xuất khóa giữ chỗ và xuất kho đích danh các Serial)\n"
                "• [bin_locations] 1 ───── N [serials] (Một ô kệ trong tủ an toàn K1/K2 lưu trữ nhiều mã Serial)\n"
                "• [users] 1 ───────────── N [system_audit_logs] (Mỗi tài khoản nhân viên lưu vết toàn bộ nhật ký thao tác)"
            )
            for r in p.runs:
                r.font.name = "Consolas"; r.font.size = Pt(9); r.font.color.rgb = C_NAVY
        elif "[Bảng A] N ──── M [Bảng C]" in txt or "[Bảng B] 1 ──── 1 [Bảng D]" in txt:
            p.text = ""

    # =============================================================
    # BƯỚC 2: CẬP NHẬT 11 BẢNG GỐC CỦA TEMPLATE
    # =============================================================

    # TABLE 1 (orig_tables[0]): ĐẶC TẢ YÊU CẦU CHỨC NĂNG (Mục 2) - Đầy đủ FR-01 -> FR-20
    t1 = orig_tables[0]
    format_row(t1.rows[0], HEX_NAVY, is_header=True)
    while len(t1.rows) > 1:
        tr = t1.rows[-1]._tr
        tr.getparent().remove(tr)
        
    t1_data = [
        ("FR-01", "Đăng nhập & Xác thực bảo mật", "Xác thực danh tính người dùng bằng Email/Username và mật khẩu mã hóa BCrypt/SHA-256. Cấp quyền phiên làm việc lưu trong SessionManager. Tự động đăng xuất khi hết hạn.", "Cao", "TV1: Bình"),
        ("FR-02", "Kiểm soát Phân quyền RBAC 5 Roles", "Kiểm soát truy cập dựa trên 5 vai trò hệ thống: SYSTEM_ADMIN, STORE_OWNER, WAREHOUSE_MANAGER, OPERATIONS_STAFF, ACCOUNTANT. Ngăn chặn người dùng trái phép can thiệp tính năng ngoài thẩm quyền.", "Cao", "TV1: Bình"),
        ("FR-03", "Quản lý Danh mục Đồng hồ Cao cấp", "Khai báo Master Data từng mẫu đồng hồ xa xỉ: SKU duy nhất, Tên mẫu, Hãng (Rolex, Omega, Patek...), Bộ sưu tập, Loại máy, Vỏ, Kính Sapphire, Kháng nước, Đơn giá đại lý.", "Cao", "TV1: Bình"),
        ("FR-04", "Quản lý ĐVT Đa cấp & Tỷ lệ Quy đổi", "Thiết lập cấu trúc ĐVT 2 cấp bắt buộc: ĐVT Cơ sở ('Chiếc') và ĐVT Đóng gói ('Thùng'). Lưu trữ tỷ lệ conversionRate (1 Thùng = N Chiếc) làm căn cứ tự động cho nhập/xuất kho.", "Cao", "TV1: Bình"),
        ("FR-05", "Định mức Tồn kho & Cảnh báo an toàn", "Thiết lập ngưỡng tồn kho tối thiểu (minStockAlert) và tối đa (maxStockAlert). Cảnh báo trực quan màu sắc khi tồn khả dụng chạm ngưỡng an toàn.", "Trung bình", "TV1: Bình"),
        ("FR-06", "Quản lý Hồ sơ Nhà cung cấp & Đánh giá công nợ", "Khai báo hồ sơ pháp nhân NCC quốc tế (Rolex Geneva SA, Patek Salons, Omega Biel), mã số thuế, tài khoản ngân hàng thụ hưởng, theo dõi hạn mức công nợ phải trả.", "Cao", "TV2: Quân"),
        ("FR-07", "Tiếp nhận Hóa đơn & Nhập kho Quy đổi ĐVT", "Tiếp nhận chứng từ giao hàng NCC, tự động tính tổng số chiếc cần nhận: Tổng = Số thùng × Hệ số quy đổi + Số chiếc lẻ. Khóa sửa phiếu khi đã duyệt.", "Cao", "TV2: Quân"),
        ("FR-08", "Quét Serial Camera ML Kit & Chống trùng 100%", "Sử dụng Camera đọc mã vạch/QR của từng chiếc hộp đồng hồ. Kiểm tra đối soát trùng lặp 2 tầng (trùng trong phiếu và trùng trong toàn bộ cơ sở dữ liệu), chặn trùng tuyệt đối.", "Cao", "TV2: Quân"),
        ("FR-09", "Phân bổ Chi phí Logistics & Giá vốn Đích danh", "Tính giá vốn đích danh từng Serial: Giá vốn = Đơn giá mua + (Phí vận chuyển + Thuế quan + Bảo hiểm)/Tổng số chiếc. Đảm bảo phản ánh chính xác giá trị tài sản từng chiếc.", "Cao", "TV2: Quân"),
        ("FR-10", "Quản lý Công nợ NCC & Xuất trả hàng lỗi", "Ghi nhận công nợ phải trả khi duyệt phiếu nhập, giảm nợ khi duyệt phiếu chi (Ủy nhiệm chi). Quy trình 4 bước cách ly hàng lỗi và xuất trả NCC để hoàn tiền hoặc cấn trừ nợ.", "Cao", "TV2: Quân"),
        ("FR-11", "Quản lý Hồ sơ Đại lý & Hạn mức Tín dụng", "Khai báo hồ sơ đại lý B2B (Galle Watch, Donghochinhhang), phân cấp đối tác VIP, thiết lập hạn mức tín dụng công nợ (Credit Limit). Tự động khóa nút duyệt đơn khi nợ vượt hạn mức.", "Cao", "TV3: Thảo"),
        ("FR-12", "Tạo Lệnh xuất kho & Khóa giữ chỗ tồn kho", "Tạo đơn xuất kho đại lý B2B. Kích hoạt cơ chế Reservation Engine: tự động khóa giữ chỗ các mã Serial khả dụng, ngăn chặn tranh chấp tồn kho giữa các nhân viên.", "Cao", "TV3: Thảo"),
        ("FR-13", "Quy trình Xuất kho 2 bước & Quét Serial 100%", "Thực hiện quy trình 2 bước: Bước 1 Soạn hàng theo Smart Picking List; Bước 2 Quét mã Serial camera đối soát khớp 100% với danh sách giữ chỗ, chặn hàng lỗi DEFECTIVE, đóng thùng niêm phong.", "Cao", "TV3: Thảo"),
        ("FR-14", "Lập Phiếu Thu tiền đại lý & In chứng từ A4", "Quản lý thu hồi công nợ đại lý qua phiếu thu tiền mặt/chuyển khoản. Kết xuất và in ấn Chứng từ giao hàng B2B kiêm Phiếu xuất kho chuẩn khổ A4 qua Android PrintManager.", "Cao", "TV3: Thảo"),
        ("FR-15", "Kiểm kê kho đối soát Thừa/Thiếu & Sổ Thẻ kho", "Tổ chức đợt kiểm kê định kỳ, quét mã Serial thực tế tại từng ô kệ để so sánh với số liệu hệ thống. Tự động lập biên bản thừa/thiếu và cập nhật Sổ thẻ kho điện tử.", "Cao", "TV4: Tâm"),
        ("FR-16", "Executive Dashboard 5 Thẻ Chỉ số KPI", "Hiển thị 5 chỉ số điều hành then chốt theo thời gian thực: Giá trị tài sản tồn kho, Doanh thu xuất kho đại lý, Số đơn xuất kho mới, Tồn kho khả dụng, Tỷ lệ đổi trả hàng.", "Cao", "TV5: Tú"),
        ("FR-17", "Trực quan hóa Biểu đồ Doanh thu 6 tháng", "Vẽ biểu đồ cột/đường trực quan xu hướng doanh thu và chi phí 6 tháng gần nhất bằng thư viện MPAndroidChart, hỗ trợ phóng to/thu nhỏ và chạm điểm dữ liệu xem chi tiết.", "Cao", "TV5: Tú"),
        ("FR-18", "Hệ thống 9 Báo cáo Chuyên sâu Đa phân hệ", "Hệ thống 9 mẫu báo cáo nghiệp vụ (BC01 đến BC09) kết nối dữ liệu liên phân hệ từ TV1 đến TV4, cung cấp bộ lọc thời gian linh hoạt (Hôm nay, Tuần này, Tháng này, Tùy chọn).", "Cao", "TV5: Tú"),
        ("FR-19", "Xuất tệp CSV & In ấn A4 Android PrintManager", "Chuyển đổi dữ liệu bảng báo cáo thành định dạng CSV lưu vào bộ nhớ máy (Downloads/ChronoVault) và kết nối Android PrintManager để in ra giấy hoặc lưu bản PDF chuẩn khổ A4.", "Cao", "TV5: Tú"),
        ("FR-20", "Báo cáo Dòng tiền thuần & Kiểm toán hệ thống", "Theo dõi dòng tiền vào (thực thu) và dòng tiền ra (thực chi), tách biệt hoàn toàn với doanh thu ghi nhận. Báo cáo nhật ký kiểm toán (Audit Trail) phục vụ thanh tra nội bộ.", "Cao", "TV5: Tú")
    ]
    for row_idx, item in enumerate(t1_data):
        row = t1.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 2 (orig_tables[1]): DANH SÁCH ĐỐI TƯỢNG (ENTITIES - Mục 3.1) - ENT-01 -> ENT-13
    t2 = orig_tables[1]
    format_row(t2.rows[0], HEX_NAVY, is_header=True)
    while len(t2.rows) > 1:
        tr = t2.rows[-1]._tr
        tr.getparent().remove(tr)
        
    t2_data = [
        ("ENT-01", "User (Người dùng)", "Quản lý thông tin tài khoản nhân viên và lãnh đạo trong hệ thống WMS.", "id, username, password_hash, full_name, email, role, is_active, created_at", "Thuộc 1 Role (1-1); Tạo nhiều Giao dịch (1-N)"),
        ("ENT-02", "Role (Vai trò RBAC)", "Quản lý 5 nhóm quyền hạn truy cập nghiệp vụ trong hệ thống.", "role_code, role_name, description, permissions_json", "Gán cho nhiều User (1-N)"),
        ("ENT-03", "Product (Mẫu đồng hồ)", "Lưu trữ Master Data mẫu đồng hồ cao cấp chuẩn Luxury Horology.", "sku, name, brand, collection, movement_type, case_material, wholesale_price, conversion_rate, min_stock, max_stock", "Chứa nhiều Serial định danh (1-N); Thuộc 1 Brand (N-1)"),
        ("ENT-04", "Brand (Thương hiệu)", "Danh bạ các hãng đồng hồ xa xỉ chính hãng (Thụy Sỹ, Nhật, Đức).", "brand_id, brand_name, origin_country, website", "Chứa nhiều Product (1-N)"),
        ("ENT-05", "UnitOfMeasure (ĐVT)", "Định nghĩa quy cách đóng gói đa cấp (Chiếc, Thùng, Hộp).", "uom_id, uom_name, uom_type, conversion_factor", "Áp dụng cho nhiều Product (1-N)"),
        ("ENT-06", "Supplier (Nhà cung cấp)", "Quản lý thông tin đối tác chế tác và phân phối đồng hồ quốc tế.", "supplier_id, supplier_code, name, tax_code, contact_person, email, phone, address, bank_account, bank_name, current_debt, is_active", "Phát hành nhiều InboundReceipt (1-N); Nhận nhiều PaymentVoucher (1-N)"),
        ("ENT-07", "InboundReceipt (Phiếu nhập)", "Lưu trữ thông tin chứng từ lô hàng nhập khẩu từ nhà cung cấp.", "receipt_id, receipt_code, supplier_id, invoice_number, receipt_date, total_packages, total_quantity, total_goods_amount, shipping_fee, tax_fee, insurance_fee, total_cost, status, created_by", "Thuộc 1 Supplier (N-1); Chứa nhiều SerialEntity (1-N)"),
        ("ENT-08", "SerialEntity (Mã Serial)", "Định danh duy nhất 100% từng chiếc đồng hồ xa xỉ trong kho.", "serial_id, serial_number, product_sku, inbound_receipt_id, unit_cost, allocated_cost, specific_cost, status, bin_location_id, quality_state, warranty_months, created_at", "Thuộc 1 Product (N-1); Thuộc 1 InboundReceipt (N-1); Nằm tại 1 BinLocation (N-1)"),
        ("ENT-09", "PaymentVoucher (Phiếu chi)", "Chứng từ ủy nhiệm chi thanh toán nợ cho nhà cung cấp.", "voucher_id, voucher_code, supplier_id, payment_date, amount, payment_method, bank_reference, notes, created_by", "Thuộc 1 Supplier (N-1); Giảm trừ current_debt của NCC"),
        ("ENT-10", "Dealer (Đại lý B2B)", "Quản lý hồ sơ đối tác đại lý tiếp nhận phân phối độc quyền và hạn mức tín dụng.", "dealer_id, dealer_code, name, tier, discount_rate, credit_limit, current_debt, tax_code, contact_person, phone, address, is_active", "Tiếp nhận nhiều OutboundOrder (1-N); Nhận nhiều ReceiptVoucher (1-N)"),
        ("ENT-11", "OutboundOrder (Lệnh xuất)", "Lưu trữ thông tin xuất kho phân phối đại lý B2B và trạng thái khóa giữ chỗ.", "order_id, order_code, dealer_id, order_date, total_packages, total_quantity, subtotal_amount, discount_amount, total_amount, reservation_status, order_status, created_by", "Thuộc 1 Dealer (N-1); Khóa giữ chỗ nhiều Serial (1-N)"),
        ("ENT-12", "DashboardKPI (Chỉ số điều hành)", "Tập hợp các số liệu đo lường hiệu năng hoạt động của toàn kho.", "kpi_id, total_inventory_value, wholesale_revenue, new_orders_count, available_stock, return_rate, recorded_at", "Tổng hợp từ bảng Serials, OutboundOrders, Products"),
        ("ENT-13", "ReportTable (Bảng dữ liệu báo cáo)", "Cấu trúc dữ liệu trung gian phục vụ hiển thị 9 báo cáo và xuất file.", "report_id, report_code, report_title, time_range, headers_json, rows_json, summary_metrics, generated_at", "Được tạo động từ Room Database bởi ReportEngine")
    ]
    for row_idx, item in enumerate(t2_data):
        row = t2.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 3 (orig_tables[2]): PHÂN HỆ (NHÓM CHỨC NĂNG - Mục 3.2)
    t3 = orig_tables[2]
    format_row(t3.rows[0], HEX_NAVY, is_header=True)
    while len(t3.rows) > 1:
        tr = t3.rows[-1]._tr
        tr.getparent().remove(tr)

    t3_data = [
        ("MOD-01", "Quản trị Hệ thống & Danh mục Luxury Horology\n(Phan Bá Hải Bình phụ trách)", "Quản lý bảo mật, xác thực người dùng, phân quyền RBAC 5 Roles, danh mục thông số đồng hồ xa xỉ, thiết lập ĐVT 2 cấp và cấu trúc CSDL Room Core.", "User, Role, Product, Brand, UnitOfMeasure", "Đăng nhập, Quản lý tài khoản, Phân quyền RBAC, Quản lý mẫu đồng hồ (SKU), Thiết lập tỷ lệ quy đổi ĐVT, Cảnh báo tồn kho an toàn."),
        ("MOD-02", "Quản lý Đối tác NCC & Nhập kho Quy đổi ĐVT\n(Nguyễn Đắc Quân phụ trách)", "Quản lý hồ sơ NCC quốc tế, công nợ phải trả, lập phiếu nhập kho quy đổi Thùng ra Chiếc, quét camera ML Kit Serial 100%, phân bổ chi phí logistics & tính giá vốn đích danh, xuất trả hàng lỗi.", "Supplier, InboundReceipt, SerialEntity, PaymentVoucher", "Quản lý hồ sơ NCC, Lập phiếu nhập kho, Quét Serial camera ML Kit chống trùng, Phân bổ chi phí logistics, Tính giá vốn đích danh từng Serial, Lập ủy nhiệm chi thanh toán, Lập phiếu xuất trả hàng lỗi NCC."),
        ("MOD-03", "Đối Tác Đại Lý & Quản Lý Xuất Kho B2B\n(Tô Đức Thảo phụ trách)", "Quản lý hồ sơ đại lý B2B tiếp nhận, hạn mức tín dụng công nợ (Credit Limit), lệnh yêu cầu xuất hàng, cơ chế khóa giữ chỗ tồn kho (Reservation Engine), quy trình xuất kho 2 bước, quét camera Serial đối soát 100% và in phiếu xuất kho B2B khổ A4.", "Dealer, OutboundOrder, ReservationEngine, ReceiptVoucher", "Quản lý danh bạ đại lý B2B, Kiểm soát hạn mức tín dụng tự động, Tạo lệnh xuất kho đại lý, Khóa giữ chỗ tồn kho tự động, Quét Serial xuất đóng thùng bằng Camera, Lập phiếu thu nợ đại lý, In biên bản giao hàng A4."),
        ("MOD-04", "Quản trị Tồn kho Nội bộ & Kiểm kê Kệ hàng\n(Võ Công Tâm phụ trách)", "Phân loại tồn kho 3 cấp chất lượng, trực quan hóa sơ đồ ma trận kệ tủ an toàn K1/K2, quy trình kiểm kê đối soát tự động Thừa/Thiếu, Sổ Thẻ kho điện tử.", "SerialQuality, BinMatrix, StockAudit, StockCardLedger", "Phân loại 3 chất lượng hàng, Tra cứu ma trận ô kệ Bin K1/K2, Quét mã điều chuyển kệ, Kiểm kê đối soát Thừa/Thiếu, Tra cứu Sổ thẻ kho điện tử."),
        ("MOD-05", "Executive Dashboard & Hệ thống 9 Báo cáo\n(Trần Công Tú phụ trách)", "Bảng chỉ số KPI điều hành thời gian thực, biểu đồ doanh thu 6 tháng MPAndroidChart, 9 báo cáo chuyên sâu đa phân hệ, xuất tệp CSV và in ấn A4 qua Android PrintManager.", "DashboardKPI, ChartEngine, ReportContainer, CashflowData", "Executive Dashboard 5 thẻ KPI, Biểu đồ doanh thu 6 tháng, Biểu đồ cơ cấu xuất hàng, 9 báo cáo chuyên sâu đa phân hệ, Bộ lọc thời gian động, Xuất tệp CSV vào Downloads/ChronoVault, In ấn và xuất PDF khổ A4.")
    ]
    for row_idx, item in enumerate(t3_data):
        row = t3.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    # TABLE 4 (orig_tables[3]): MÔ TẢ MODULE IPO 1 (Mục 4.2 - MOD-01-02 Bình)
    t4 = orig_tables[3]
    format_row(t4.rows[0], HEX_NAVY, is_header=True)
    t4_data = [
        ("Input", "• Dữ liệu đầu vào: Mã SKU đồng hồ, Tên mẫu mã, Thương hiệu, Bộ sưu tập, Loại máy (Automatic/Quartz/Solar), Chất liệu vỏ (Vàng 18K/Thép/Titanium), Đường kính mặt (mm), Độ kháng nước (ATM), Đơn giá đại lý niêm yết (VNĐ), ĐVT Cơ sở ('Chiếc'), ĐVT Đóng gói ('Thùng'), Hệ số quy đổi (Ví dụ: 10 chiếc/thùng), Ngưỡng tồn an toàn (Min/Max).\n• Nguồn dữ liệu: Form nhập liệu AddEditProductActivity hoặc file Excel Master Data.\n• Điều kiện tiên quyết: Đăng nhập với vai trò SYSTEM_ADMIN hoặc STORE_OWNER."),
        ("Process", "• Bước 1: Kiểm tra tính hợp lệ dữ liệu (SKU không rỗng, không ký tự đặc biệt, Đơn giá đại lý > 0, Hệ số quy đổi >= 1).\n• Bước 2: Truy vấn Room Database kiểm tra tính duy nhất của Mã SKU (chặn trùng hoàn toàn).\n• Bước 3: Tải ảnh đại diện mẫu đồng hồ, nén kích thước và lưu trữ đường dẫn ảnh cục bộ.\n• Bước 4: Tạo đối tượng ProductEntity và gọi hàm productDao.insertProduct(product).\n• Bước 5: Ghi nhận nhật ký kiểm toán hệ thống (Audit Log): 'Khởi tạo mẫu đồng hồ [SKU]'."),
        ("Output", "• Bản ghi sản phẩm mới được lưu thành công vào bảng `products` của Room Database.\n• Giao diện hiển thị SnackBar thông báo: 'Đã lưu mẫu đồng hồ [SKU] thành công'.\n• Danh mục sản phẩm tại ProductListFragment tự động cập nhật hiển thị mẫu đồng hồ mới qua Flow / LiveData."),
        ("Actor", "Chủ cửa hàng (STORE_OWNER) và Quản trị viên hệ thống (SYSTEM_ADMIN)."),
        ("Quyền hạn", "Toàn quyền Thêm/Sửa đối với Admin và Owner (các vai trò khác chỉ có quyền Xem - Read Only)."),
        ("Luồng dữ liệu liên quan", "Ghi vào bảng `products`, ghi vào bảng `system_audit_logs`, cập nhật StateFlow của ProductViewModel."),
        ("Ghi chú / Ràng buộc", "Mã SKU bắt buộc viết hoa; Hệ số quy đổi phải là số nguyên dương; Khi đã phát sinh phiếu nhập/xuất thì không được phép thay đổi tỷ lệ quy đổi ĐVT.")
    ]
    for row_idx, item in enumerate(t4_data):
        row = t4.rows[row_idx + 1]
        row.cells[0].text = item[0]
        row.cells[1].text = item[1]
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    # TABLE 5 (orig_tables[4]): MA TRẬN CRUD (Mục 5.1) - Đầy đủ các Actor và Entities
    t5 = orig_tables[4]
    format_row(t5.rows[0], HEX_NAVY, is_header=True)
    while len(t5.rows) > 1:
        tr = t5.rows[-1]._tr
        tr.getparent().remove(tr)

    t5_data = [
        ("User (Tài khoản)", "Admin", "Admin, Owner, Cá nhân", "Admin (đổi role/khóa), Cá nhân (đổi pass)", "Admin (Khóa tài khoản / Soft Delete)", "Không xóa cứng để bảo toàn lịch sử kiểm toán"),
        ("Role (Vai trò RBAC)", "Hệ thống (Seed data)", "Tất cả các Actor", "Admin (cập nhật mô tả quyền)", "Cấm xóa hoàn toàn", "5 vai trò cố định: Admin, Owner, Manager, Staff, Accountant"),
        ("Product (Mẫu đồng hồ)", "Admin, Owner", "Tất cả các Actor", "Admin, Owner, Quản lý kho", "Admin, Owner (Ẩn ngừng kinh doanh)", "Chỉ được ẩn/ngừng kinh doanh khi đã phát sinh giao dịch"),
        ("Brand (Hãng sản xuất)", "Admin, Owner", "Tất cả các Actor", "Admin, Owner", "Admin (khi chưa có sản phẩm)", "Rolex, Patek Philippe, Omega, Cartier, Hublot..."),
        ("UnitOfMeasure (ĐVT)", "Admin, Quản lý kho", "Tất cả các Actor", "Admin, Quản lý kho", "Cấm xóa khi đã có SKU liên kết", "Bắt buộc có ĐVT Cơ sở ('Chiếc') và ĐVT Đóng gói ('Thùng')"),
        ("Supplier (Nhà cung cấp)", "Staff (Nhập), Kế toán", "Tất cả các Actor", "Staff (Nhập), Kế toán, Owner", "Admin, Owner (Khóa hoạt động)", "Theo dõi số dư nợ phải trả theo thời gian thực (TV2 Quân)"),
        ("InboundReceipt (Phiếu nhập)", "Staff (Nhập kho)", "Staff, Quản lý kho, Kế toán, Owner", "Staff (khi còn là bản nháp)", "Admin (Hủy phiếu nháp)", "Phiếu đã DUYỆT thì KHÓA hoàn toàn, không thể sửa/xóa (TV2 Quân)"),
        ("SerialEntity (Mã Serial)", "Staff (Quét camera nhập)", "Tất cả các Actor", "Thủ kho (chuyển kệ/sửa trạng thái)", "Cấm xóa hoàn toàn", "Định danh 100% từng chiếc, lưu giá vốn đích danh (TV2 Quân & Hệ thống)"),
        ("PaymentVoucher (Phiếu chi)", "Kế toán kho", "Kế toán, Owner, Admin", "Kế toán (bản nháp)", "Admin, Owner (Hủy nháp)", "Giảm trừ công nợ NCC và ghi nhận dòng tiền ra (TV2 Quân)"),
        ("Dealer (Đại lý B2B)", "Staff (Xuất kho), Kế toán", "Tất cả các Actor", "Staff (Xuất kho), Kế toán, Owner", "Admin, Owner (Khóa hợp tác)", "Quản lý hạn mức tín dụng và phân cấp VIP (TV3 Thảo)"),
        ("OutboundOrder (Lệnh xuất)", "Staff (Xuất kho)", "Staff, Quản lý kho, Kế toán, Owner", "Staff (khi còn là bản nháp)", "Admin, Owner (Hủy lệnh)", "Khóa giữ chỗ tồn kho (RESERVED) và hạch toán xuất (TV3 Thảo)"),
        ("DashboardKPI (Chỉ số KPI)", "Hệ thống (Tự động tính)", "Owner, Kế toán, Quản lý kho", "Hệ thống (Recalculate)", "Không áp dụng", "Hiển thị thời gian thực qua StateFlow (TV5 Tú)"),
        ("ReportTable (Bảng báo cáo)", "Hệ thống (ReportEngine)", "Owner, Kế toán, Admin", "Hệ thống (Khi lọc thời gian)", "Tự động dọn Cache", "Hỗ trợ 9 loại báo cáo chuyên sâu, xuất CSV/In A4 (TV5 Tú)")
    ]
    for row_idx, item in enumerate(t5_data):
        row = t5.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        for col in [1, 2, 3, 4]:
            row.cells[col].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 6 (orig_tables[5]): MÔ TẢ LUỒNG DỮ LIỆU CHÍNH (Mục 5.2) - DF-01 -> DF-10
    t6 = orig_tables[5]
    format_row(t6.rows[0], HEX_NAVY, is_header=True)
    while len(t6.rows) > 1:
        tr = t6.rows[-1]._tr
        tr.getparent().remove(tr)

    t6_data = [
        ("DF-01", "Xác thực Đăng nhập & Cấp quyền phiên", "Người dùng", "LoginActivity -> SessionManager", "Username, Password băm", "Tài khoản ở trạng thái Hoạt động (is_active = true) (Bình)"),
        ("DF-02", "Khai báo Mẫu đồng hồ & Cấu hình ĐVT", "Owner / Admin", "AddEditProductActivity -> Room DB", "Thông số SKU, ĐVT, Tỷ lệ quy đổi, Min/Max stock", "Mã SKU duy nhất chưa tồn tại trong hệ thống (Bình)"),
        ("DF-03", "Cập nhật Phân quyền Nhân viên nội bộ", "Admin", "UserManagementFragment -> UserDao", "User ID, Vai trò mới (UserRole enum)", "Chỉ SYSTEM_ADMIN được quyền thực hiện (Bình)"),
        ("DF-04", "Lập Phiếu Nhập kho & Quét mã Serial Camera", "Staff (Nhập kho)", "InboundActivity -> InboundDao -> SerialDao", "Thông tin hóa đơn, Số thùng, SKU, Danh sách mã Serial quét camera", "Quét đủ 100% số lượng quy đổi; không trùng mã Serial (Quân)"),
        ("DF-05", "Duyệt Phiếu chi thanh toán nợ Nhà cung cấp", "Kế toán kho", "PaymentActivity -> PaymentVoucherDao -> SupplierDao", "Mã NCC, Số tiền chi, Phương thức, Mã giao dịch ngân hàng", "Số tiền chi <= Số dư nợ hiện tại của NCC (Quân)"),
        ("DF-06", "Xuất trả hàng lỗi kỹ thuật cho NCC", "Thủ kho / Staff", "ReturnActivity -> ReturnDao -> SerialDao -> SupplierDao", "Danh sách Serial lỗi, Lý do lỗi, Mã phiếu nhập gốc", "Serial đang ở trạng thái DEFECTIVE; NCC chấp nhận trả (Quân)"),
        ("DF-07", "Tạo Lệnh xuất kho & Khóa giữ chỗ Reservation", "Staff (Xuất kho)", "OutboundOrderActivity -> OutboundDao -> SerialDao", "Mã đại lý, Danh sách SKU, Số lượng thùng/chiếc đặt mua", "Dư nợ dự kiến <= Hạn mức tín dụng; Tồn khả dụng >= Số lượng đặt (Thảo)"),
        ("DF-08", "Quét mã Serial xuất kho & In phiếu giao hàng A4", "Thủ kho / Staff", "DispatchActivity -> SerialDao -> OutboundDao -> PrintManager", "Mã đơn hàng, Danh sách mã Serial quét camera thực xuất", "Quét khớp 100% mã Serial đã giữ chỗ, không trầy xước (Thảo)"),
        ("DF-09", "Tổng hợp 5 Chỉ số KPI & Biểu đồ Điều hành", "Kế toán / Owner", "DashboardFragment -> DashboardViewModel -> Room DB", "Bộ lọc thời gian (Hôm nay/Tuần/Tháng)", "Tổng hợp dữ liệu bất đồng bộ qua Coroutines & StateFlow (Tú)"),
        ("DF-10", "Truy vấn 9 Báo cáo Chuyên sâu & Xuất CSV/In A4", "Kế toán / Owner", "ReportFragment -> ReportEngine -> FileStorage / PrintManager", "Mã báo cáo (BC01-BC09), Khoảng thời gian từ ngày - đến ngày", "Định dạng bảng ReportTable chuẩn, cấp quyền ghi bộ nhớ (Tú)")
    ]
    for row_idx, item in enumerate(t6_data):
        row = t6.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 7 (orig_tables[6]): DANH SÁCH BẢNG CƠ SỞ DỮ LIỆU (Mục 6.1)
    t7 = orig_tables[6]
    format_row(t7.rows[0], HEX_NAVY, is_header=True)
    while len(t7.rows) > 1:
        tr = t7.rows[-1]._tr
        tr.getparent().remove(tr)

    t7_data = [
        ("users", "Lưu trữ thông tin tài khoản người dùng và thông tin phân quyền truy cập.", "id (INT, AutoIncrement, PK)", "role (ENUM)", "Băm mật khẩu BCrypt trước khi lưu trữ (Bình)"),
        ("products", "Lưu trữ Master Data danh mục các mẫu đồng hồ cao cấp và cấu hình quy đổi ĐVT.", "sku (VARCHAR, PK)", "brand_id (FK)", "Bảng trung tâm liên kết với toàn bộ hệ thống WMS (Bình)"),
        ("brands", "Danh bạ thương hiệu đồng hồ xa xỉ chính hãng (Rolex, Patek, Omega, AP...).", "brand_id (INT, PK)", "Không", "Quản lý nguồn gốc xuất xứ quốc gia (Bình)"),
        ("units_of_measure", "Định nghĩa các đơn vị tính và hệ số quy đổi chuẩn.", "uom_id (INT, PK)", "Không", "Quy định ĐVT Thùng / Hộp / Chiếc lẻ (Bình)"),
        ("suppliers", "Hồ sơ đối tác nhà cung cấp đồng hồ xa xỉ và công nợ phải trả.", "supplier_id (INT, PK)", "tax_code (UNIQUE)", "Theo dõi số dư nợ phải trả theo thời gian thực (Quân)"),
        ("inbound_receipts", "Chứng từ các lô hàng đồng hồ nhập khẩu từ nhà cung cấp.", "receipt_id (INT, PK)", "supplier_id (FK)", "Lưu trữ chi phí vận chuyển, hải quan, bảo hiểm (Quân)"),
        ("serials", "Định danh 100% từng chiếc đồng hồ, giá vốn đích danh và trạng thái chất lượng.", "serial_id (INT, PK)", "product_sku (FK), inbound_receipt_id (FK)", "Khóa chính và ràng buộc Unique ngăn chặn trùng lặp tuyệt đối (Quân & Hệ thống)"),
        ("payment_vouchers", "Chứng từ ủy nhiệm chi thanh toán nợ cho nhà cung cấp.", "voucher_id (INT, PK)", "supplier_id (FK)", "Ghi nhận dòng tiền ra và giảm trừ công nợ NCC (Quân)"),
        ("dealers", "Hồ sơ đối tác đại lý tiếp nhận phân phối độc quyền và hạn mức tín dụng.", "dealer_id (INT, PK)", "tax_code (UNIQUE)", "Quản lý hạn mức nợ, chiết khấu VIP và thông tin giao hàng (Thảo)"),
        ("outbound_orders", "Lệnh xuất kho phân phối đại lý B2B và trạng thái khóa giữ chỗ tồn kho.", "order_id (INT, PK)", "dealer_id (FK)", "Quản lý Reservation và giao dịch thực xuất kho (Thảo)"),
        ("system_audit_logs", "Lưu vết toàn bộ thao tác thêm, sửa, xóa, duyệt chứng từ trong toàn hệ thống.", "log_id (INT, PK)", "user_id (FK)", "Dữ liệu chỉ ghi (Append-Only), phục vụ kiểm toán nội bộ (Bình & Toàn nhóm)")
    ]
    for row_idx, item in enumerate(t7_data):
        row = t7.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    # TABLE 8 (orig_tables[7]): CHI TIẾT THUỘC TÍNH BẢNG 'products' (Mục 6.2 - Bình)
    t8 = orig_tables[7]
    format_row(t8.rows[0], HEX_NAVY, is_header=True)
    while len(t8.rows) > 1:
        tr = t8.rows[-1]._tr
        tr.getparent().remove(tr)

    t8_data = [
        ("sku", "VARCHAR(50)", "No", "Không", "Mã định danh duy nhất của mẫu đồng hồ", "PRIMARY KEY, Bắt buộc viết hoa"),
        ("name", "VARCHAR(255)", "No", "Không", "Tên thương mại đầy đủ của mẫu đồng hồ", "NOT NULL"),
        ("brand", "VARCHAR(100)", "No", "Không", "Hãng sản xuất (Rolex, Patek Philippe, Omega...)", "NOT NULL"),
        ("collection", "VARCHAR(100)", "Yes", "NULL", "Bộ sưu tập (Submariner, Nautilus, Speedmaster...)", "Có thể để trống"),
        ("movement_type", "VARCHAR(50)", "No", "'AUTOMATIC'", "Loại bộ máy cơ học / điện tử", "CHECK in ('AUTOMATIC', 'MANUAL', 'QUARTZ', 'SOLAR')"),
        ("case_material", "VARCHAR(100)", "No", "'STAINLESS_STEEL'", "Chất liệu vỏ chế tác", "CHECK in ('GOLD_18K', 'STEEL', 'TITANIUM', 'PLATINUM')"),
        ("dial_size_mm", "DOUBLE", "No", "40.0", "Đường kính mặt số (mm)", "dial_size_mm > 0"),
        ("wholesale_price", "DOUBLE", "No", "0.0", "Đơn giá phân phối đại lý niêm yết (VNĐ)", "wholesale_price >= 0"),
        ("base_unit", "VARCHAR(20)", "No", "'Chiếc'", "Đơn vị tính cơ sở nhỏ nhất", "Mặc định là 'Chiếc'"),
        ("pack_unit", "VARCHAR(20)", "No", "'Thùng'", "Đơn vị tính đóng gói xuất kho", "Mặc định là 'Thùng' hoặc 'Hộp'"),
        ("conversion_rate", "INT", "No", "1", "Hệ số quy đổi (1 Thùng = N Chiếc)", "conversion_rate >= 1"),
        ("min_stock_alert", "INT", "No", "5", "Ngưỡng tồn kho tối thiểu cần cảnh báo", "min_stock_alert >= 0"),
        ("max_stock_alert", "INT", "No", "100", "Ngưỡng tồn kho tối đa an toàn", "max_stock_alert >= min_stock_alert"),
        ("image_uri", "TEXT", "Yes", "NULL", "Đường dẫn lưu ảnh mẫu đồng hồ cục bộ", "URI hợp lệ"),
        ("is_active", "BOOLEAN", "No", "TRUE", "Trạng thái kinh doanh của mẫu đồng hồ", "TRUE: Đang bán, FALSE: Ngừng bán")
    ]
    for row_idx, item in enumerate(t8_data):
        row = t8.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 9 (orig_tables[8]): PHÂN CÔNG VAI TRÒ TRONG NHÓM (Mục 7.1)
    t9 = orig_tables[8]
    format_row(t9.rows[0], HEX_NAVY, is_header=True)
    while len(t9.rows) > 1:
        tr = t9.rows[-1]._tr
        tr.getparent().remove(tr)

    t9_data = [
        ("1", "Trưởng nhóm / Quản trị hệ thống\n(SYSTEM_ADMIN & STORE_OWNER)", "Điều phối toàn bộ dự án, thiết kế kiến trúc MVVM Core, thiết kế Room Database v4 cốt lõi, quản trị Git Repository, phát triển Module Quản trị Hệ thống & Danh mục Đồng hồ Luxury Horology, tổng hợp báo cáo chung.", "Phan Bá Hải Bình (TV1)"),
        ("2", "Nhân viên Nhập kho\n(OPERATIONS_STAFF)", "Phát triển phân hệ Quản lý Nhà cung cấp, công nợ phải trả, lập phiếu nhập kho quy đổi ĐVT, tích hợp Camera ML Kit quét mã Serial 100%, phân bổ chi phí logistics & thuật toán tính giá vốn đích danh, xuất trả hàng lỗi.", "Nguyễn Đắc Quân (TV2)"),
        ("3", "Nhân viên Xuất kho\n(OPERATIONS_STAFF)", "Phát triển phân hệ Đối tác Đại lý & Quản lý Xuất kho B2B, kiểm soát hạn mức tín dụng tự động (Credit Limit), cơ chế khóa giữ chỗ tồn kho (Reservation Engine), quy trình xuất kho 2 bước, quét camera Serial đối soát và in phiếu giao hàng A4.", "Tô Đức Thảo (TV3)"),
        ("4", "Thủ kho\n(WAREHOUSE_MANAGER)", "Phát triển phân hệ Phân loại tồn kho 3 trạng thái chất lượng, trực quan hóa sơ đồ ma trận kệ tủ chống trộm K1/K2, quy trình kiểm kê đối soát tự động và Sổ Thẻ kho điện tử.", "Võ Công Tâm (TV4)"),
        ("5", "Kế toán kho\n(ACCOUNTANT)", "Phát triển Executive Dashboard với 5 thẻ KPI thời gian thực, trực quan hóa biểu đồ doanh thu 6 tháng bằng MPAndroidChart, hệ thống 9 báo cáo chuyên sâu và báo cáo dòng tiền thuần Cashflow, xuất CSV và in A4.", "Trần Công Tú (TV5)")
    ]
    for row_idx, item in enumerate(t9_data):
        row = t9.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[3].paragraphs[0].runs[0].font.bold = True

    # TABLE 10 (orig_tables[9]): CÁCH THỨC CHIA CÔNG VIỆC THEO GIAI ĐOẠN (Mục 7.2)
    t10 = orig_tables[9]
    format_row(t10.rows[0], HEX_NAVY, is_header=True)
    while len(t10.rows) > 1:
        tr = t10.rows[-1]._tr
        tr.getparent().remove(tr)

    t10_data = [
        ("Giai đoạn 1: Khảo sát nghiệp vụ & Thiết kế Core", "Xác định bài toán B2B Luxury Horology, thiết lập cấu trúc Room DB v4, viết Base ViewModel/Repository, xây dựng khung MVVM chuẩn trên nhánh `main`.", "Phan Bá Hải Bình (TV1)", "Cả 4 thành viên", "1.5 tuần"),
        ("Giai đoạn 2: Phát triển độc lập các phân hệ con", "Mỗi thành viên tạo nhánh Git riêng (`feature/...`), sử dụng bộ Prompt kỹ thuật để phát triển giao diện và nghiệp vụ phân hệ của mình kết nối với Room DB.", "Quân (TV2), Thảo (TV3), Tâm (TV4), Tú (TV5)", "Phan Bá Hải Bình hỗ trợ kỹ thuật", "2.5 tuần"),
        ("Giai đoạn 3: Tích hợp (Merge) & Kiểm thử chéo", "Review mã nguồn, duyệt Pull Requests, gộp các nhánh vào `main`, thực hiện các kịch bản kiểm thử tích hợp chéo liên phân hệ (Nhập -> Kệ -> Giữ chỗ -> Xuất bán -> Dashboard).", "Phan Bá Hải Bình (chủ trì)", "Cả 5 thành viên", "1.0 tuần"),
        ("Giai đoạn 4: Hoàn thiện Báo cáo Word & Chuẩn bị Vấn đáp", "Từng thành viên viết phần Word của mình theo hướng dẫn, Bình tổng hợp thành cuốn Báo cáo Đồ án hoàn chỉnh nộp Khoa, chuẩn bị dữ liệu test demo và câu hỏi vấn đáp.", "Phan Bá Hải Bình (tổng hợp)", "Cả 5 thành viên", "1.0 tuần")
    ]
    for row_idx, item in enumerate(t10_data):
        row = t10.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 11 (orig_tables[10]): THEO DÕI TIẾN ĐỘ CÔNG VIỆC (Mục 7.3 - Tích hợp TV1, TV2, TV3, TV5)
    t11 = orig_tables[10]
    format_row(t11.rows[0], HEX_NAVY, is_header=True)
    while len(t11.rows) > 1:
        tr = t11.rows[-1]._tr
        tr.getparent().remove(tr)

    t11_data = [
        ("01/10 - 05/10/2026", "Phan Bá Hải Bình", "Khảo sát bài toán quản lý kho đồng hồ xa xỉ, xác định 4 cơ chế quản trị bắt buộc (Serial 100%, Quy đổi ĐVT, Giá vốn đích danh, Hạn mức nợ).", "100%", "Hoàn thành"),
        ("06/10 - 15/10/2026", "Phan Bá Hải Bình", "Thiết kế kiến trúc Android MVVM, khởi tạo Room Database v4 (UserEntity, ProductEntity, SerialEntity, TransactionEntity) và SessionManager.", "100%", "Hoàn thành"),
        ("16/10 - 25/10/2026", "Phan Bá Hải Bình", "Lập trình hoàn chỉnh Phân hệ 1 (ProductListFragment, ProductDetailFragment, AddEditProductActivity, LoginActivity, RBAC 5 Roles).", "100%", "Hoàn thành"),
        ("16/10 - 28/10/2026", "Nguyễn Đắc Quân", "Xây dựng giao diện và nghiệp vụ Phân hệ 2 (Quản lý NCC, công nợ, quy đổi ĐVT, tích hợp Camera ML Kit quét Serial, tính giá vốn đích danh, xuất trả hàng lỗi).", "100%", "Hoàn thành"),
        ("17/10 - 30/10/2026", "Tô Đức Thảo", "Xây dựng Phân hệ 3 (Quản lý đại lý B2B, kiểm soát hạn mức tín dụng Credit Limit, khóa giữ chỗ Reservation, quy trình xuất kho 2 bước, in phiếu A4).", "100%", "Hoàn thành"),
        ("18/10 - 30/10/2026", "Trần Công Tú", "Xây dựng Phân hệ 5 (Executive Dashboard 5 KPI thời gian thực, biểu đồ MPAndroidChart 6 tháng, hệ thống 9 báo cáo chuyên sâu, xuất CSV và in ấn A4).", "100%", "Hoàn thành"),
        ("26/10 - 05/11/2026", "Phan Bá Hải Bình", "Soạn thảo Bộ Prompt chi tiết cho 5 thành viên, thiết lập quy chuẩn phân nhánh Git và xây dựng tài liệu Hướng dẫn viết Báo cáo Word & Vấn đáp.", "100%", "Hoàn thành"),
        ("06/11 - 12/11/2026", "Quân, Thảo, Tú & Bình", "Hoàn thành báo cáo chuyên sâu từng phân hệ, tiến hành kiểm thử các kịch bản thực nghiệm độc lập và kiểm tra đối soát chéo.", "100%", "Hoàn thành"),
        ("13/11 - 17/11/2026", "Phan Bá Hải Bình", "Tích hợp toàn bộ nội dung của Quân (TV2), Thảo (TV3) và Tú (TV5) vào Báo cáo Master của nhóm, hoàn thiện 4/5 phân hệ lớn, chuẩn bị demo bảo vệ.", "100%", "Hoàn thành"),
        ("Hiện tại -> Nộp bài", "Cả nhóm 5 thành viên", "Họp tổng duyệt kịch bản demo trên thiết bị thật, hoàn thiện nốt phân hệ TV4 (Kệ kho & Kiểm kê) và nộp hồ sơ đồ án lên Khoa CNTT.", "Đang thực hiện", "Theo lịch thi Khoa")
    ]
    for row_idx, item in enumerate(t11_data):
        row = t11.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if row_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if "100%" in item[3]:
            row.cells[3].paragraphs[0].runs[0].font.bold = True

    # =============================================================
    # BƯỚC 3: CHÈN CÁC NỘI DUNG VÀ BẢNG BỔ SUNG (DÙNG THAM CHIẾU CỐ ĐỊNH)
    # =============================================================

    # 3.1. Chèn Bảng 1.1: So sánh phần mềm (ngay sau đoạn Bảng so sánh ở Mục 1)
    compare_p = None
    for p in doc.paragraphs:
        if "Bảng 1.1: So sánh đối chiếu phần mềm ChronoVault WMS" in p.text:
            compare_p = p
            break
            
    if compare_p:
        tbl_comp, _ = add_table_after(compare_p._p, 7, 5)
        comp_headers = ["Tiêu chí so sánh", "Phần mềm bán lẻ phổ thông (KiotViet, Sapo)", "ERP Quốc tế cao cấp (SAP B1, NetSuite)", "ERP Mã nguồn mở (Odoo WMS)", "ChronoVault WMS (Đề tài)"]
        for c_idx, h in enumerate(comp_headers):
            tbl_comp.rows[0].cells[c_idx].text = h
        format_row(tbl_comp.rows[0], HEX_NAVY, is_header=True, font_size=8.5)
        
        comp_data = [
            ("Mô hình mục tiêu", "Bán lẻ B2C / Tạp hóa / POS", "Doanh nghiệp sản xuất đa quốc gia", "Quản trị doanh nghiệp tổng thể", "Phân phối Đại lý B2B Đồng hồ Xa xỉ"),
            ("Quản lý Serial/IMEI", "Tùy chọn (chủ yếu quản lý số lượng tổng)", "Hỗ trợ nhưng cấu hình cực kỳ phức tạp", "Cần cài thêm module trả phí", "Bắt buộc 100% định danh từng chiếc, chống trùng tuyệt đối"),
            ("Quy đổi ĐVT đa cấp", "Chỉ nhân chia số lượng giản đơn", "Hỗ trợ đa cấp UoM", "Hỗ trợ UoM", "Nhập/Xuất Thùng tự động ép quét đủ N mã Serial lẻ bằng Camera ML Kit"),
            ("Phương pháp Giá vốn", "Bình quân gia quyền / FIFO giản đơn", "Bình quân / FIFO / Đích danh", "Bình quân gia quyền", "Giá vốn Đích danh cộng dồn chi phí vận chuyển & thuế vào từng Serial"),
            ("Nền tảng vận hành", "Web / POS máy tính bảng", "Desktop Client nặng nề", "Web App", "Android Studio Native (Kotlin MVVM), quét mã vạch bằng Camera điện thoại"),
            ("Chi phí đầu tư", "Vài trăm ngàn/tháng (thiếu nghiệp vụ phân phối)", "Hàng chục ngàn USD phí bản quyền", "Tốn chi phí tùy biến lớn", "Tối ưu chi phí, triển khai gọn nhẹ trên thiết bị di động nội bộ")
        ]
        for r_idx, r_val in enumerate(comp_data):
            row = tbl_comp.rows[r_idx + 1]
            for c_idx, val in enumerate(r_val):
                row.cells[c_idx].text = val
            bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
            format_row(row, bg, is_header=False, font_size=8)
            row.cells[0].paragraphs[0].runs[0].font.bold = True
            row.cells[4].paragraphs[0].runs[0].font.bold = True

    # 3.2. Chèn IPO 2 (Quân), IPO 3 (Thảo), IPO 4 (Thảo), IPO 5 (Tú), Mục 4.3 (Quân), Mục 4.4 (Thảo) và Mục 4.5 (Tú) NGAY SAU Table 4 gốc
    anchor_elem = orig_tbl_xmls[3]
    
    # --- IPO 2: MOD-02-01 (Quân) ---
    p_ipo2_title, anchor_elem = add_p_after(anchor_elem, 
        "\nModule IPO 2: MOD-02-01 — Tiếp nhận Hóa đơn & Nhập kho Quy đổi ĐVT, Quét Serial Camera ML Kit\n"
        "Thuộc phân hệ: MOD-02 (Quản lý Đối tác NCC & Nhập kho Quy đổi ĐVT — Nguyễn Đắc Quân phụ trách)\n"
        "Mức độ ưu tiên: Cao (Bắt buộc hoàn thành)",
        bold=True, font_size=10, color_rgb=C_NAVY, space_before=12, space_after=4)
        
    tbl_ipo2, anchor_elem = add_table_after(anchor_elem, 8, 2)
    ipo2_data = [
        ("Input", "• Dữ liệu đầu vào: Nhà cung cấp đang hoạt động, Số hóa đơn NCC, Ngày nhận, Mã SKU, Đơn vị nhập (Thùng hoặc Chiếc lẻ), Số lượng, Đơn giá mua (VNĐ), Chi phí vận chuyển, Thuế nhập khẩu, Phí bảo hiểm, Ghi chú lô hàng.\n• Nguồn dữ liệu: Chứng từ thực tế từ NCC và Camera điện thoại quét mã vạch/QR.\n• Điều kiện tiên quyết: Đăng nhập với quyền OPERATIONS_STAFF (Nhân viên nhập kho) hoặc WAREHOUSE_MANAGER."),
        ("Process", "• Bước 1: Hệ thống tra cứu hệ số quy đổi của SKU (Ví dụ: 1 Thùng = 10 chiếc -> 2 Thùng cần quét đúng 20 Serial).\n• Bước 2: Camera quét mã vạch từng hộp qua Google ML Kit. Mỗi lần quét kiểm tra trùng lặp 2 cấp: trùng trong danh sách phiếu hiện tại và trùng trong toàn bộ Room DB.\n• Bước 3: Phân bổ chi phí logistics vào từng chiếc: Chi phí/chiếc = (Vận chuyển + Thuế + Bảo hiểm) / Tổng số chiếc.\n• Bước 4: Tính Giá vốn đích danh: Specific Cost = Đơn giá mua + Chi phí phân bổ.\n• Bước 5: Thủ kho và Kế toán phê duyệt: Ghi nhận phiếu nhập, tạo các bản ghi Serials với trạng thái IN_STOCK, tăng công nợ phải trả NCC trong 1 Database Transaction duy nhất."),
        ("Output", "• Phiếu nhập kho được lưu thành công với trạng thái COMPLETED.\n• N bản ghi SerialEntity mới được thêm vào Room Database với giá vốn đích danh chuẩn xác.\n• Công nợ của Nhà cung cấp (current_debt) tăng đúng bằng tổng giá trị hóa đơn."),
        ("Actor", "Nhân viên Nhập kho (OPERATIONS_STAFF), Thủ kho (WAREHOUSE_MANAGER), Kế toán (ACCOUNTANT)."),
        ("Quyền hạn", "Nhân viên lập phiếu; Thủ kho xác nhận vật lý; Kế toán/Quản trị viên duyệt phiếu."),
        ("Luồng dữ liệu liên quan", "Ghi vào bảng `inbound_receipts`, bảng `serials`, cập nhật `suppliers.current_debt`, ghi `system_audit_logs`."),
        ("Ràng buộc", "Chỉ cho phép bấm 'Hoàn tất' khi số mã Serial quét được bằng CHÍNH XÁC 100% số lượng quy đổi; Tất cả mã Serial phải chưa từng tồn tại trong hệ thống.")
    ]
    for r_idx, r_val in enumerate(ipo2_data):
        row = tbl_ipo2.rows[r_idx]
        row.cells[0].text = r_val[0]
        row.cells[1].text = r_val[1]
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=9)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        set_cell_background(row.cells[0], "F1F5F9")

    # --- IPO 3: MOD-03-01 (Thảo) ---
    p_ipo3_title, anchor_elem = add_p_after(anchor_elem, 
        "\nModule IPO 3: MOD-03-01 — Khởi Tạo Đơn Xuất Kho Đại Lý B2B & Khóa Giữ Chỗ Tồn Kho (Reservation)\n"
        "Thuộc phân hệ: MOD-03 (Đối Tác Đại Lý & Quản Lý Xuất Kho B2B — Tô Đức Thảo phụ trách)\n"
        "Mức độ ưu tiên: Cao (Bắt buộc hoàn thành)",
        bold=True, font_size=10, color_rgb=C_NAVY, space_before=12, space_after=4)
        
    tbl_ipo3, anchor_elem = add_table_after(anchor_elem, 8, 2)
    ipo3_data = [
        ("Input", "• Dữ liệu đầu vào: Đại lý đối tác tiếp nhận (Dealer), Danh mục SKU đồng hồ đặt mua, Đơn vị tính (Thùng hoặc Chiếc lẻ), Số lượng đặt mua, Tỷ lệ chiết khấu thương mại VIP (15% - 30%), Hạn mức tín dụng tối đa (Credit Limit), Dư nợ hiện tại của đại lý.\n• Nguồn dữ liệu: Form tạo đơn OutboundOrderActivity / Hộp thoại dialog_create_outbound_order.xml.\n• Điều kiện tiên quyết: Đăng nhập với vai trò OPERATIONS_STAFF (Xuất kho) hoặc STORE_OWNER."),
        ("Process", "• Bước 1: Hệ thống kiểm tra số lượng tồn khả dụng: Available Stock = Physical In Stock - Reserved Quantity. Nếu số lượng đặt > Tồn khả dụng, lập tức từ chối và báo thiếu hàng.\n• Bước 2: Thẩm định Hạn mức Tín dụng (Credit Limit Enforcement): Dư nợ dự kiến = Dư nợ hiện tại + Giá trị đơn hàng sau chiết khấu. Nếu Dư nợ dự kiến > Hạn mức nợ tối đa, khóa hoàn toàn nút duyệt đơn và hiển thị viền đỏ cảnh báo vi phạm trần nợ.\n• Bước 3: Áp dụng đơn giá phân phối đại lý chuẩn theo cấp bậc (VIP Kim Cương, Vàng, Chuẩn), tự động tính số tiền chiết khấu thương mại.\n• Bước 4: Khi Kế toán/Chủ kho phê duyệt: Tạo bản ghi OutboundOrder ở trạng thái RESERVED. Hệ thống kích hoạt Reservation Engine: tự động đánh dấu số lượng Serial khả dụng tương ứng sang trạng thái RESERVED, khóa giữ chỗ không cho các đơn khác tranh chấp."),
        ("Output", "• Bản ghi đơn xuất kho được lưu với mã đơn duy nhất (PX-xxxx), trạng thái RESERVED trong CSDL Room Database.\n• Số lượng tồn khả dụng của SKU tự động giảm trừ ngay lập tức trên toàn hệ thống.\n• Giao diện hiển thị SnackBar thông báo: 'Đã duyệt đơn và khóa giữ chỗ N chiếc đồng hồ thành công'."),
        ("Actor", "Nhân viên Điều phối Xuất kho (OPERATIONS_STAFF), Kế toán (ACCOUNTANT), Chủ kho (STORE_OWNER)."),
        ("Quyền hạn", "Nhân viên tạo đơn nháp; Kế toán và Chủ kho có thẩm quyền duyệt hạn mức tín dụng và khóa giữ chỗ."),
        ("Luồng dữ liệu liên quan", "Ghi vào bảng `outbound_orders`, cập nhật trạng thái `serials.status = 'RESERVED'`, ghi `system_audit_logs`, phát thông báo qua WebSocket."),
        ("Ràng buộc", "Tuyệt đối không duyệt đơn khi vượt hạn mức tín dụng nợ đại lý; Không cho phép chọn mã Serial cụ thể ở bước này mà chỉ khóa số lượng chỉ định.")
    ]
    for r_idx, r_val in enumerate(ipo3_data):
        row = tbl_ipo3.rows[r_idx]
        row.cells[0].text = r_val[0]
        row.cells[1].text = r_val[1]
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=9)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        set_cell_background(row.cells[0], "F1F5F9")

    # --- IPO 4: MOD-03-02 (Thảo) ---
    p_ipo4_title, anchor_elem = add_p_after(anchor_elem, 
        "\nModule IPO 4: MOD-03-02 — Soạn Hàng Theo Smart Picking, Quét Camera Serial & Thực Xuất Kho B2B\n"
        "Thuộc phân hệ: MOD-03 (Đối Tác Đại Lý & Quản Lý Xuất Kho B2B — Tô Đức Thảo phụ trách)\n"
        "Mức độ ưu tiên: Cao (Bắt buộc hoàn thành)",
        bold=True, font_size=10, color_rgb=C_NAVY, space_before=12, space_after=4)
        
    tbl_ipo4, anchor_elem = add_table_after(anchor_elem, 8, 2)
    ipo4_data = [
        ("Input", "• Dữ liệu đầu vào: Mã đơn xuất kho đã duyệt ở trạng thái RESERVED, Danh sách mã Serial thực tế tại ô kệ K1/K2, Luồng hình ảnh camera quét barcode/QR trên vỏ hộp đồng hồ.\n• Nguồn dữ liệu: Màn hình điều hành đóng gói DispatchActivity / Hộp thoại dialog_dispatch_package.xml.\n• Điều kiện tiên quyết: Thủ kho hoặc Nhân viên xuất kho đã nhận hàng từ danh sách soạn hàng (Picking List)."),
        ("Process", "• Bước 1: Hệ thống hiển thị danh sách soạn hàng (Smart Picking List) tối ưu vị trí ô kệ kho K1/K2.\n• Bước 2: Camera tích hợp Google ML Kit quét mã vạch từng hộp đồng hồ. Hệ thống đối soát 3 lớp kiểm tra: (a) Mã Serial thuộc đúng SKU theo đơn; (b) Mã Serial đang ở trạng thái IN_STOCK hoặc RESERVED cho chính đơn này; (c) Trạng thái chất lượng là PERFECT (Hàng mới 100%), nếu quét nhầm hàng DEFECTIVE (trầy xước) lập tức rung chuông báo động và từ chối nhận.\n• Bước 3: Cập nhật thanh tiến độ quét (ví dụ: 5/5 chiếc). Nút 'Xác nhận xuất kho' chỉ mở khóa khi quét đủ 100% số lượng Serial hợp lệ.\n• Bước 4: Thực thi Room Database Transaction: Chuyển trạng thái các Serial sang SOLD (Đã xuất bán), giải phóng cờ giữ chỗ, trừ tồn vật lý kho, tăng công nợ phải thu đại lý (currentDebt) đúng bằng giá trị đơn hàng sau chiết khấu.\n• Bước 5: Gọi lớp ReportPrintManager kết nối Android PrintManager để in Chứng từ giao hàng B2B khổ A4."),
        ("Output", "• Đơn xuất kho chuyển sang trạng thái COMPLETED.\n• N mã Serial đổi trạng thái thành SOLD, gỡ bỏ liên kết ô kệ lưu kho.\n• Số dư công nợ đại lý tăng chính xác; Biên bản giao hàng kiêm Phiếu xuất kho B2B được in ra chuẩn khổ A4."),
        ("Actor", "Thủ kho (WAREHOUSE_MANAGER) và Nhân viên điều phối kho (OPERATIONS_STAFF)."),
        ("Quyền hạn", "Thủ kho xác nhận số lượng vật lý và niêm phong kiện hàng; Hệ thống tự động ghi sổ kế toán."),
        ("Luồng dữ liệu liên quan", "Cập nhật `outbound_orders.order_status = 'COMPLETED'`, cập nhật `serials.status = 'SOLD'`, cập nhật `dealers.current_debt`, ghi `system_audit_logs`."),
        ("Ràng buộc", "Chỉ xuất đúng những chiếc đồng hồ đạt chuẩn chất lượng 100%; Toàn bộ thao tác trừ tồn và ghi nợ phải diễn ra trọn vẹn trong một giao dịch cơ sở dữ liệu duy nhất.")
    ]
    for r_idx, r_val in enumerate(ipo4_data):
        row = tbl_ipo4.rows[r_idx]
        row.cells[0].text = r_val[0]
        row.cells[1].text = r_val[1]
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=9)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        set_cell_background(row.cells[0], "F1F5F9")

    # --- IPO 5: MOD-05-01 (Tú) ---
    p_ipo5_title, anchor_elem = add_p_after(anchor_elem, 
        "\nModule IPO 5: MOD-05-01 — Tổng hợp 5 Thẻ Chỉ số KPI Điều hành & Hệ thống 9 Báo cáo Chuyên sâu\n"
        "Thuộc phân hệ: MOD-05 (Executive Dashboard & Hệ thống 9 Báo cáo — Trần Công Tú phụ trách)\n"
        "Mức độ ưu tiên: Cao (Bắt buộc hoàn thành)",
        bold=True, font_size=10, color_rgb=C_NAVY, space_before=12, space_after=4)
        
    tbl_ipo5, anchor_elem = add_table_after(anchor_elem, 8, 2)
    ipo5_data = [
        ("Input", "• Dữ liệu đầu vào: Bộ lọc thời gian (Hôm nay, 7 ngày qua, Tháng này, Khoảng ngày tùy chọn), Mã loại báo cáo (BC01 đến BC09), Thao tác người dùng (Chuyển tab, Bấm lọc, Bấm xuất CSV, Bấm in A4).\n• Nguồn dữ liệu: Dữ liệu giao dịch thực từ toàn bộ Room Database (bảng serials, inbound_receipts, outbound_orders, suppliers, dealers, audit_logs).\n• Điều kiện tiên quyết: Đăng nhập với vai trò ACCOUNTANT, STORE_OWNER hoặc SYSTEM_ADMIN."),
        ("Process", "• Bước 1: DashboardViewModel kích hoạt Coroutine chạy trên luồng nền (Dispatchers.IO) để truy vấn Room DB.\n• Bước 2: Tính toán 5 chỉ số KPI: Tổng tài sản tồn kho (cộng dồn specific_cost của Serial còn trong kho), Doanh thu xuất kho đại lý, Đếm đơn mới, Tính tồn khả dụng (Tồn thực - Giữ chỗ), Tính tỷ lệ đổi trả (Serial trả / Serial bán).\n• Bước 3: Nạp dữ liệu 6 tháng vào DataSet của MPAndroidChart để vẽ đồ thị cột/đường.\n• Bước 4: Khi chọn báo cáo (BC01-BC09), ReportEngine truy vấn và ánh xạ dữ liệu thành ReportTable.\n• Bước 5: Khi xuất file: ReportExportManager ghi tệp CSV vào thư mục Downloads/ChronoVault; ReportPrintManager tạo tài liệu gửi Android PrintManager."),
        ("Output", "• Giao diện Dashboard hiển thị 5 thẻ KPI với màu sắc cảnh báo trực quan (đổi sang màu đỏ nếu tỷ lệ trả > 2%).\n• Biểu đồ doanh thu 6 tháng hiển thị mượt mà trên MPAndroidChart.\n• Bảng báo cáo hiển thị chính xác theo kỳ lọc; Tệp CSV hoặc bản in PDF A4 được tạo thành công."),
        ("Actor", "Kế toán kho (ACCOUNTANT) và Chủ cửa hàng (STORE_OWNER)."),
        ("Quyền hạn", "Chỉ Kế toán và Chủ cửa hàng được quyền xem toàn bộ báo cáo doanh thu, lợi nhuận và dòng tiền."),
        ("Luồng dữ liệu liên quan", "Đọc từ toàn bộ Room DB qua DAO, phát dữ liệu qua StateFlow tới DashboardFragment và ReportFragment, ghi tệp ra File System."),
        ("Ràng buộc", "Tuyệt đối không chạy truy vấn nặng trên luồng giao diện chính (Main Thread); Khi xuất file phải kiểm tra quyền ghi bộ nhớ (WRITE_EXTERNAL_STORAGE).")
    ]
    for r_idx, r_val in enumerate(ipo5_data):
        row = tbl_ipo5.rows[r_idx]
        row.cells[0].text = r_val[0]
        row.cells[1].text = r_val[1]
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=9)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        set_cell_background(row.cells[0], "F1F5F9")

    # --- TIỂU MỤC 4.3: PHÂN TÍCH NGHIỆP VỤ CHUYÊN SÂU TV2 (NGUYỄN ĐẮC QUÂN) ---
    p_sec43, anchor_elem = add_p_after(anchor_elem,
        "\n4.3. Phân tích Nghiệp vụ Chuyên sâu Phân hệ Nhập kho & Nhà cung cấp (TV2: Nguyễn Đắc Quân)",
        bold=True, font_size=11, color_rgb=C_NAVY, space_before=14, space_after=6)
        
    p_sec43_1, anchor_elem = add_p_after(anchor_elem,
        "Phân hệ TV2 quản lý chặt chẽ chuỗi cung ứng đầu vào từ khi nhận chứng từ giao hàng từ các hãng đồng hồ xa xỉ quốc tế (Rolex Geneva SA, Patek Philippe Salons, Omega Biel...) đến khi từng chiếc đồng hồ được định danh Serial, dán nhãn và nhập kho an toàn.\n\n"
        "4.3.1. Quản lý Hồ sơ Nhà cung cấp và Cơ chế Kiểm soát Công nợ Phải trả:\n"
        "Hồ sơ NCC lưu trữ: Mã đối tác duy nhất (NCC-RLX-01), Tên pháp nhân, Mã số thuế (kiểm tra UNIQUE), Người đại diện, Email, Hotline, Tài khoản ngân hàng và Ngân hàng thụ hưởng. Công nợ phải trả được hình thành từ chứng từ đã DUYỆT, tuyệt đối không lấy từ phiếu nháp. Bảng dưới đây mô tả chi tiết tác động của các sự kiện nghiệp vụ lên số dư nợ NCC:",
        font_size=9.5, color_rgb=C_SLATE, space_before=4, space_after=6)

    # Bảng tác động công nợ NCC của Quân
    tbl_debt, anchor_elem = add_table_after(anchor_elem, 5, 3)
    debt_headers = ["Sự kiện nghiệp vụ", "Tác động công nợ NCC", "Điều kiện kiểm soát chứng từ"]
    for c_idx, h in enumerate(debt_headers):
        tbl_debt.rows[0].cells[c_idx].text = h
    format_row(tbl_debt.rows[0], HEX_NAVY, is_header=True, font_size=9)
    debt_data = [
        ("Duyệt phiếu nhập kho", "Tăng khoản phải trả hàng hóa", "Số hóa đơn hợp lệ, số lượng Serial quét khớp 100% số lượng quy đổi, có chữ ký xác nhận của Thủ kho."),
        ("Duyệt phiếu chi (Ủy nhiệm chi)", "Giảm khoản phải trả nhà cung cấp", "Phiếu chi kèm phương thức thanh toán, số tài khoản thụ hưởng trùng khớp với pháp nhân NCC, có mã tham chiếu ngân hàng."),
        ("Duyệt phiếu xuất trả hàng lỗi NCC", "Giảm khoản phải trả hoặc ghi nhận khoản hoàn tiền", "Có biên bản xác nhận lỗi kỹ thuật, dẫn chiếu đúng phiếu nhập gốc, NCC chấp thuận cấn trừ công nợ."),
        ("Phát sinh phí vận chuyển & thuế quan", "Cộng vào nợ NCC nếu NCC đứng tên thu hộ; theo dõi khoản phải trả riêng nếu trả đơn vị Logistics", "Hóa đơn dịch vụ vận tải/tờ khai hải quan hợp lệ, được kế toán đối soát trước khi phân bổ vào giá vốn.")
    ]
    for r_idx, r_val in enumerate(debt_data):
        row = tbl_debt.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    p_sec43_2, anchor_elem = add_p_after(anchor_elem,
        "\n4.3.2. Quy trình Quét mã vạch Serial 100% bằng Camera ML Kit và Kiểm soát Trùng mã:\n"
        "Hệ thống ChronoVault WMS áp dụng nguyên tắc 'Không định danh Serial - Không nhập kho'. Khi tiếp nhận lô hàng theo Thùng/Kiện, hệ thống tự động tính số chiếc cần nhận: Tổng số chiếc = Số thùng × Hệ số quy đổi + Số chiếc lẻ. Camera điện thoại tích hợp thư viện Google ML Kit Barcode Scanning quét mã vạch trên từng hộp và phản hồi tức thời theo 6 kịch bản kiểm soát:",
        font_size=9.5, color_rgb=C_SLATE, space_before=6, space_after=6)

    # Bảng quét serial của Quân
    tbl_scan, anchor_elem = add_table_after(anchor_elem, 7, 2)
    scan_headers = ["Trường hợp kiểm soát quét Serial", "Phản hồi và Xử lý của Hệ thống ChronoVault WMS"]
    for c_idx, h in enumerate(scan_headers):
        tbl_scan.rows[0].cells[c_idx].text = h
    format_row(tbl_scan.rows[0], HEX_NAVY, is_header=True, font_size=9)
    scan_data = [
        ("Mã Serial rỗng hoặc không đọc được", "Báo lỗi trên màn hình, phát âm thanh cảnh báo lỗi (Beep âm trầm), yêu cầu nhân viên quét lại dưới điều kiện đủ sáng."),
        ("Mã Serial bị trùng lặp trong chính phiếu nhập hiện tại", "Báo lỗi rõ: 'Mã Serial [ABC] đã được quét trong danh sách tạm', từ chối thêm vào danh sách."),
        ("Mã Serial đã tồn tại trong cơ sở dữ liệu (toàn kho)", "Báo lỗi nghiêm trọng: 'Mã Serial đã tồn tại trong hệ thống (Phiếu nhập #XYZ)', từ chối tiếp nhận để ngăn chặn hàng giả/hàng trùng."),
        ("Số lượng Serial quét chưa đủ số lượng quy đổi", "Khóa nút 'Hoàn tất phiếu nhập', hiển thị thông báo tiến độ: 'Đã quét X / Y chiếc (Còn thiếu Y - X chiếc)'."),
        ("Số lượng Serial quét vượt quá định mức", "Chặn camera không cho quét tiếp, báo lỗi: 'Đã quét đủ số lượng quy đổi của lô hàng'."),
        ("Quét hợp lệ, không trùng và đủ số lượng", "Phát âm thanh thông báo thành công (Chime), cập nhật danh sách tạm, mở khóa nút 'Hoàn tất phiếu nhập'.")
    ]
    for r_idx, r_val in enumerate(scan_data):
        row = tbl_scan.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    p_sec43_3, anchor_elem = add_p_after(anchor_elem,
        "\n4.3.3. Thuật toán Phân bổ Chi phí Logistics và Tính Giá vốn Đích danh (Specific Identification Costing):\n"
        "Đối với ngành hàng đồng hồ cao cấp xa xỉ, phương pháp Bình quân gia quyền hay FIFO truyền thống không thể phản ánh chính xác giá trị thực tế của từng chiếc đồng hồ khi các chi phí bảo hiểm, thuế hải quan và vận chuyển đặc biệt (xe bọc thép) biến động theo từng đợt nhập. Hệ thống ChronoVault WMS áp dụng phương pháp Giá vốn Đích danh theo công thức:\n"
        "• Chi phí phân bổ cho mỗi chiếc = (Phí vận chuyển + Thuế nhập khẩu + Phí bảo hiểm) / Tổng số chiếc quy đổi\n"
        "• Giá vốn đích danh từng mã Serial (Specific Cost) = Đơn giá mua hóa đơn + Chi phí phân bổ cho mỗi chiếc\n\n"
        "4.3.4. Bộ Dữ liệu Thực nghiệm Minh họa Phân hệ Nhập kho của TV2:\n"
        "Bảng dưới đây minh họa lô hàng nhập khẩu thực tế gồm 2 Thùng đồng hồ Rolex Submariner (tổng 20 chiếc) từ Rolex Geneva SA:",
        font_size=9.5, color_rgb=C_SLATE, space_before=6, space_after=6)

    # Bảng dữ liệu thực nghiệm của Quân
    tbl_exp_quan, anchor_elem = add_table_after(anchor_elem, 13, 2)
    tbl_exp_quan.rows[0].cells[0].text = "Thông số nghiệp vụ nhập kho"
    tbl_exp_quan.rows[0].cells[1].text = "Giá trị minh họa thực nghiệm"
    format_row(tbl_exp_quan.rows[0], HEX_NAVY, is_header=True, font_size=9)
    exp_quan_data = [
        ("Nhà cung cấp", "Rolex Geneva SA (Mã: NCC-RLX-01, MST: 0102030405)"),
        ("Sản phẩm nhập khẩu", "Rolex Submariner Date 126610LN (Mã SKU: RLX-SUB-126610LN)"),
        ("Quy cách đóng gói & ĐVT", "ĐVT Nhập: 2 Thùng (Hệ số quy đổi: 1 Thùng = 10 Chiếc lẻ)"),
        ("Tổng số chiếc quy đổi bắt buộc", "2 Thùng × 10 = 20 chiếc (Yêu cầu quét đúng 20 mã Serial)"),
        ("Đơn giá mua theo hóa đơn", "200.000.000 VNĐ / chiếc"),
        ("Tổng tiền hàng theo hóa đơn", "20 chiếc × 200.000.000 = 4.000.000.000 VNĐ"),
        ("Chi phí vận chuyển & Bảo hiểm bảo mật", "40.000.000 VNĐ"),
        ("Chi phí phân bổ vào từng chiếc", "40.000.000 / 20 = 2.000.000 VNĐ / chiếc"),
        ("Giá vốn đích danh mỗi mã Serial", "200.000.000 + 2.000.000 = 202.000.000 VNĐ / chiếc"),
        ("Tổng giá trị tài sản nhập kho", "20 chiếc × 202.000.000 = 4.040.000.000 VNĐ"),
        ("Thanh toán đợt 1 (Phiếu chi / UNC)", "2.000.000.000 VNĐ (Mã tham chiếu UNC: VCB-20261110-01)"),
        ("Số dư công nợ còn lại phải trả NCC", "4.040.000.000 - 2.000.000.000 = 2.040.000.000 VNĐ")
    ]
    for r_idx, r_val in enumerate(exp_quan_data):
        row = tbl_exp_quan.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    # --- TIỂU MỤC 4.4: PHÂN TÍCH NGHIỆP VỤ CHUYÊN SÂU TV3 (TÔ ĐỨC THẢO) ---
    p_sec44_thao, anchor_elem = add_p_after(anchor_elem,
        "\n4.4. Phân tích Nghiệp vụ Chuyên sâu Phân hệ Đối tác Đại lý & Xuất kho B2B (TV3: Tô Đức Thảo)",
        bold=True, font_size=11, color_rgb=C_NAVY, space_before=14, space_after=6)
        
    p_sec44_thao_1, anchor_elem = add_p_after(anchor_elem,
        "Phân hệ TV3 do Tô Đức Thảo phụ trách đảm nhận vai trò là Cổng xuất kho (Outbound Fulfillment Gateway) và quản trị quan hệ đối tác thương mại B2B. Đối với mặt hàng đồng hồ xa xỉ, việc xuất kho không đơn thuần là giao nhận vật lý mà còn là quá trình kiểm soát rủi ro tín dụng công nợ và bảo vệ tài sản doanh nghiệp thông qua 4 trụ cột nghiệp vụ cốt lõi:\n\n"
        "4.4.1. Cơ chế Kiểm soát Hạn mức Tín dụng (Credit Limit Enforcement) & Biến động Dư nợ Đại lý:\n"
        "Hệ thống thiết lập trần nợ tối đa (Credit Limit từ 1 đến 5 tỷ VNĐ) cho từng đại lý phân phối dựa trên hợp đồng thương mại và phân cấp VIP (VIP Kim Cương, VIP Vàng, Đại lý Chuẩn). Số dư nợ (currentDebt) được hạch toán tức thời qua từng sự kiện tác nghiệp, tuyệt đối không để xảy ra tình trạng đại lý chiếm dụng vốn vượt thẩm quyền. Bảng dưới đây mô tả chi tiết cơ chế kiểm soát biến động nợ của TV3:",
        font_size=9.5, color_rgb=C_SLATE, space_before=4, space_after=6)

    # Bảng tác động công nợ đại lý của Thảo (Bảng 1.3 của Thảo)
    tbl_dealer_debt, anchor_elem = add_table_after(anchor_elem, 6, 3)
    dealer_debt_headers = ["Sự kiện tác nghiệp kho", "Tác động số dư nợ đại lý (currentDebt)", "Điều kiện kiểm soát an toàn tín dụng"]
    for c_idx, h in enumerate(dealer_debt_headers):
        tbl_dealer_debt.rows[0].cells[c_idx].text = h
    format_row(tbl_dealer_debt.rows[0], HEX_NAVY, is_header=True, font_size=9)
    dealer_debt_data = [
        ("Duyệt đơn xuất kho đại lý (RESERVED)", "Dư nợ thực tế CHƯA tăng; Tăng 'Dư nợ cam kết giữ chỗ' (Committed Debt)", "Dư nợ hiện tại + Giá trị đơn mới <= Hạn mức tín dụng tối đa (Credit Limit). Nếu vượt trần, hệ thống khóa nút duyệt đơn."),
        ("Thực xuất kho bàn giao (COMPLETED)", "TĂNG số dư nợ thực tế đúng bằng giá trị đơn hàng sau chiết khấu", "Đã quét camera đối soát đủ 100% mã Serial hợp lệ, ký biên bản bàn giao và in Phiếu xuất kho B2B khổ A4."),
        ("Lập Phiếu Thu tiền đại lý (RECEIPT)", "GIẢM số dư nợ thực tế đúng bằng số tiền thực thu", "Tiền mặt nộp quỹ có phiếu thu hoặc chuyển khoản ngân hàng có mã giao dịch tham chiếu hợp lệ."),
        ("Duyệt Phiếu đổi trả đại lý (RETURN)", "GIẢM số dư nợ thực tế theo giá trị hàng trả được chấp thuận", "Mã Serial phải được quét kiểm tra đúng lịch sử xuất bán của đại lý đó và được bộ phận kỹ thuật nghiệm thu."),
        ("Hủy đơn xuất kho đại lý (CANCELLED)", "Giải phóng hạn mức cam kết, KHÔNG làm biến động nợ thực tế", "Giải phóng toàn bộ cờ khóa giữ chỗ (RESERVED) của các mã Serial, hoàn trả số lượng khả dụng về kho.")
    ]
    for r_idx, r_val in enumerate(dealer_debt_data):
        row = tbl_dealer_debt.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    p_sec44_thao_2, anchor_elem = add_p_after(anchor_elem,
        "\n4.4.2. Cơ chế Khóa Giữ Chỗ Tồn Kho (Reservation Engine) & Quy trình Xuất kho 2 bước:\n"
        "• Cơ chế Khóa Giữ Chỗ (Reservation): Khi đơn hàng được duyệt, hệ thống tính toán: Tồn khả dụng = Tồn vật lý - Số lượng đang giữ chỗ. Các mã Serial khả dụng lập tức chuyển trạng thái sang RESERVED. Các nhân viên kinh doanh khác khi mở danh mục sẽ không thể đặt trùng vào số lượng đã được giữ chỗ, triệt tiêu 100% nguy cơ bán trùng một chiếc đồng hồ cho hai đại lý.\n"
        "• Quy trình Xuất kho 2 bước (Picking & Dispatch): Bước 1 - Hệ thống tự động tạo danh sách soạn hàng thông minh (Smart Picking List) tối ưu đường đi lấy hàng tại các tủ an toàn K1/K2; Bước 2 - Đóng kiện tại bàn điều phối, thủ kho dùng Camera Google ML Kit quét mã vạch laser từng hộp đồng hồ để kiểm tra đối soát khớp 100% với đơn hàng, tự động chặn các sản phẩm có trạng thái lỗi DEFECTIVE (trầy xước, nứt kính).\n\n"
        "4.4.3. Bộ Dữ liệu Thực nghiệm Kiểm thử Đại lý Galle Watch Vượt Hạn mức Nợ (Bảng 4.1 của TV3):\n"
        "Bảng dưới đây minh họa kịch bản kiểm thử thực tế giải thuật thẩm định công nợ đối với đại lý VIP Galle Watch:",
        font_size=9.5, color_rgb=C_SLATE, space_before=6, space_after=6)

    # Bảng dữ liệu thực nghiệm Galle Watch của Thảo
    tbl_exp_thao, anchor_elem = add_table_after(anchor_elem, 14, 2)
    tbl_exp_thao.rows[0].cells[0].text = "Thông số kiểm thử nghiệp vụ xuất kho B2B"
    tbl_exp_thao.rows[0].cells[1].text = "Giá trị dữ liệu mẫu thực tế"
    format_row(tbl_exp_thao.rows[0], HEX_NAVY, is_header=True, font_size=9)
    exp_thao_data = [
        ("Đại lý đối tác B2B tiếp nhận", "Chuỗi Cửa Hàng Đồng Hồ Galle Watch (Mã: DL-GALLE | Hạng: VIP Kim Cương)"),
        ("Tỷ lệ chiết khấu thương mại đại lý", "25% (Áp dụng tự động theo hợp đồng phân phối đại lý VIP)"),
        ("Hạn mức tín dụng nợ đại lý tối đa (Credit Limit)", "3.000.000.000 VNĐ (3 Tỷ đồng)"),
        ("Số dư công nợ hiện tại (currentDebt)", "1.800.000.000 VNĐ (1.8 Tỷ đồng)"),
        ("Sản phẩm đặt xuất kho đại lý", "Rolex Submariner Date 41mm (Mã SKU: RLX-SUB-126610LN)"),
        ("Số lượng đặt xuất", "5 chiếc (Đơn giá niêm yết: 350.000.000 VNĐ / chiếc)"),
        ("Tổng giá trị đơn hàng trước chiết khấu", "5 × 350.000.000 = 1.750.000.000 VNĐ"),
        ("Chiết khấu thương mại đại lý VIP (25%)", "-437.500.000 VNĐ"),
        ("Giá trị đơn hàng xuất sau chiết khấu", "1.312.500.000 VNĐ (1.3125 Tỷ đồng)"),
        ("Dư nợ dự kiến sau khi duyệt đơn mới", "1.800.000.000 + 1.312.500.000 = 3.112.500.000 VNĐ"),
        ("So sánh với Hạn mức tín dụng tối đa", "3.112.500.000 VNĐ > 3.000.000.000 VNĐ (Vượt hạn mức nợ 112.500.000 VNĐ)"),
        ("Kết quả xử lý tự động của hệ thống", "Khóa hoàn toàn nút 'Phê duyệt đơn hàng', hiển thị viền đỏ cảnh báo vượt hạn mức nợ"),
        ("Giải pháp xử lý nghiệp vụ kho", "Đại lý nộp tiền qua Phiếu Thu tiền đại lý (giảm dư nợ) hoặc làm thủ tục xin duyệt ngoại lệ Chủ kho")
    ]
    for r_idx, r_val in enumerate(exp_thao_data):
        row = tbl_exp_thao.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    p_sec44_thao_3, anchor_elem = add_p_after(anchor_elem,
        "\n4.4.4. Bộ 6 Kịch bản Kiểm thử Nghiệp vụ Phân hệ Xuất kho B2B (TC-01 đến TC-06 của TV3):\n"
        "Bảng dưới đây là kết quả kiểm thử thực nghiệm 6 ca kiểm thử cốt lõi do TV3 thực hiện:",
        font_size=9.5, color_rgb=C_SLATE, space_before=6, space_after=6)

    # Bảng 6 Test Cases của Thảo
    tbl_tc_thao, anchor_elem = add_table_after(anchor_elem, 7, 4)
    tc_thao_headers = ["Mã TC", "Mục tiêu kiểm thử", "Dữ liệu & Thao tác kiểm thử", "Kết quả mong đợi & Đánh giá"]
    for c_idx, h in enumerate(tc_thao_headers):
        tbl_tc_thao.rows[0].cells[c_idx].text = h
    format_row(tbl_tc_thao.rows[0], HEX_NAVY, is_header=True, font_size=9)
    tc_thao_data = [
        ("TC-01", "Chặn duyệt đơn vượt Credit Limit", "Galle Watch nợ 1.8 tỷ, hạn mức 3 tỷ. Tạo đơn xuất kho 5 Rolex sau CK = 1.3125 tỷ.", "Dư nợ dự kiến 3.1125 tỷ > 3 tỷ. Hệ thống khóa nút Duyệt, viền đỏ cảnh báo vượt hạn mức. -> ĐẠT"),
        ("TC-02", "Thu nợ đại lý khôi phục hạn mức", "Lập Phiếu Thu tiền đại lý thu 500 triệu VNĐ từ Galle Watch qua chuyển khoản ngân hàng.", "Dư nợ giảm còn 1.3 tỷ. Dư nợ dự kiến đơn Rolex = 1.3B + 1.3125B = 2.6125B <= 3B -> Mở nút Duyệt đơn. -> ĐẠT"),
        ("TC-03", "Khóa giữ chỗ tồn kho (Reservation)", "Sản phẩm Omega Speedmaster tồn vật lý = 5 chiếc. Kế toán duyệt đơn 1 lấy 3 chiếc.", "reservedQuantity tăng lên 3, Tồn khả dụng còn 2 chiếc. Đơn 2 đặt 4 chiếc lập tức bị từ chối do thiếu hàng. -> ĐẠT"),
        ("TC-04", "Quy đổi Thùng và kiểm tra MOQ", "Chọn ĐVT 'Thùng' (1 Thùng = 12 chiếc), số lượng = 1 Thùng, MOQ = 10 chiếc.", "convertedQuantity = 12 chiếc >= 10 chiếc MOQ -> Đạt điều kiện xuất, tính đúng giá phân phối lô. -> ĐẠT"),
        ("TC-05", "Camera quét đối soát chặn hàng lỗi", "Thủ kho quét mã Serial RX-9921 có trạng thái chất lượng là DEFECTIVE (Hàng trầy xước).", "Ứng dụng rung cảnh báo, phát âm thanh lỗi, viền đỏ ô quét và chặn không cho thêm vào kiện xuất. -> ĐẠT"),
        ("TC-06", "Transaction xuất kho và in biên bản A4", "Quét đủ 100% 5 Serial Rolex Submariner, bấm 'Xác nhận xuất kho'.", "Serial đổi sang SOLD, trừ tồn vật lý, giải phóng giữ chỗ, tăng nợ đại lý, in Phiếu xuất kho A4. -> ĐẠT")
    ]
    for r_idx, r_val in enumerate(tc_thao_data):
        row = tbl_tc_thao.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    p_sec44_thao_4, anchor_elem = add_p_after(anchor_elem,
        "\n4.4.5. Kiến trúc Lập trình Mạng Phân hệ Xuất kho (Retrofit 2 & WebSocket Real-time):\n"
        "Phân hệ TV3 được thiết kế kiến trúc truyền thông mạng 2 tầng kết hợp chặt chẽ, tối ưu hóa cho môi trường vận hành kho phân phối đại lý B2B:\n"
        "• Tầng 1 — RESTful API Client (Retrofit 2 + OkHttp Client): Đồng bộ các giao dịch CRUD có cấu trúc lớn lên máy chủ trung tâm: POST /api/v1/outbound/orders (Tạo đơn xuất kho), POST /api/v1/outbound/dispatch (Xác nhận xuất kho), POST /api/v1/dealers/receipt-vouchers (Lập phiếu thu tiền nợ đại lý).\n"
        "• Tầng 2 — WebSocket Real-time Broadcaster (Mạng LAN Nội bộ Kho): Duy trì kênh kết nối Full-Duplex thời gian thực. Mỗi khi một đơn hàng được duyệt RESERVED hoặc xuất kho COMPLETED, sự kiện lập tức được broadcast tới tất cả thiết bị di động trong kho, giúp các nhân viên khác thấy ngay số lượng tồn khả dụng mới mà không cần kéo vuốt tải lại trang (Pull-to-refresh).",
        font_size=9.5, color_rgb=C_SLATE, space_before=4, space_after=6)

    # --- TIỂU MỤC 4.5: PHÂN TÍCH NGHIỆP VỤ CHUYÊN SÂU TV5 (TRẦN CÔNG TÚ) ---
    p_sec45, anchor_elem = add_p_after(anchor_elem,
        "\n4.5. Phân tích Nghiệp vụ Chuyên sâu Phân hệ Dashboard & Báo cáo (TV5: Trần Công Tú)",
        bold=True, font_size=11, color_rgb=C_NAVY, space_before=14, space_after=6)
        
    p_sec45_1, anchor_elem = add_p_after(anchor_elem,
        "Phân hệ TV5 đóng vai trò trung tâm điều hành thông tin (Executive Dashboard) và cung cấp báo cáo quản trị toàn diện cho lãnh đạo doanh nghiệp. Được xây dựng trên nền tảng kiến trúc Android MVVM với Kotlin Coroutines và StateFlow, phân hệ đảm bảo toàn bộ các phép tính phức tạp diễn ra trên luồng nền (IO Dispatcher), giao diện người dùng luôn phản hồi tức thời dưới 16ms.\n\n"
        "4.5.1. Bảng 5 Chỉ số KPI Điều hành Thời gian thực:\n"
        "Dashboard tổng hợp 5 chỉ số then chốt giúp Chủ cửa hàng và Kế toán nắm bắt sức khỏe tài chính và hoạt động vận hành kho ngay tức thì:",
        font_size=9.5, color_rgb=C_SLATE, space_before=4, space_after=6)

    # Bảng 5 KPI của Tú
    tbl_kpi, anchor_elem = add_table_after(anchor_elem, 6, 3)
    kpi_headers = ["Chỉ số điều hành (KPI)", "Quy tắc & Công thức tính toán", "Giá trị minh họa thực tế"]
    for c_idx, h in enumerate(kpi_headers):
        tbl_kpi.rows[0].cells[c_idx].text = h
    format_row(tbl_kpi.rows[0], HEX_NAVY, is_header=True, font_size=9)
    kpi_data = [
        ("1. Giá trị tài sản tồn kho", "Tổng giá vốn đích danh (specific_cost) của tất cả mã Serial đang có trạng thái IN_STOCK trong kho.", "18.760.000.000 VNĐ"),
        ("2. Doanh thu xuất kho đại lý", "Tổng giá trị doanh thu của tất cả các đơn xuất kho có trạng thái COMPLETED trong kỳ lọc.", "12.480.000.000 VNĐ"),
        ("3. Đơn xuất kho mới", "Đếm tổng số lệnh xuất kho đại lý phát sinh mới trong kỳ lọc.", "28 đơn hàng"),
        ("4. Tồn kho khả dụng", "Tổng số lượng tồn thực tế trừ đi số lượng Serial đang bị khóa giữ chỗ (RESERVED) theo các lệnh xuất đang xử lý.", "186 chiếc"),
        ("5. Tỷ lệ đổi trả hàng", "(Tổng số Serial khách trả lại / Tổng số Serial đã xuất bán) × 100%. Nếu tỷ lệ vượt ngưỡng an toàn (> 2.0%), thẻ KPI tự động đổi sang màu đỏ cảnh báo rủi ro chất lượng.", "1,72 % (Trạng thái An toàn)")
    ]
    for r_idx, r_val in enumerate(kpi_data):
        row = tbl_kpi.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    p_sec45_2, anchor_elem = add_p_after(anchor_elem,
        "\n4.5.2. Hệ thống 9 Loại Báo cáo Quản trị Chuyên sâu (BC01 đến BC09):\n"
        "Phân hệ kết nối toàn bộ dữ liệu nghiệp vụ của 4 phân hệ còn lại để kết xuất 9 báo cáo chuyên sâu, đáp ứng yêu cầu thanh tra thuế, kiểm toán nội bộ và hoạch định chiến lược kinh doanh:",
        font_size=9.5, color_rgb=C_SLATE, space_before=6, space_after=6)

    # Bảng 9 báo cáo của Tú
    tbl_rep9, anchor_elem = add_table_after(anchor_elem, 10, 3)
    rep9_headers = ["Mã BC", "Tên mẫu báo cáo quản trị", "Nội dung nghiệp vụ & Chỉ tiêu phân tích"]
    for c_idx, h in enumerate(rep9_headers):
        tbl_rep9.rows[0].cells[c_idx].text = h
    format_row(tbl_rep9.rows[0], HEX_NAVY, is_header=True, font_size=9)
    rep9_data = [
        ("BC01", "Báo cáo Nhập hàng", "Theo dõi nhà cung cấp, số phiếu nhập, số lượng thùng, số chiếc quy đổi, tổng giá trị hàng và chi phí vận chuyển phân bổ (Kết nối TV2 Quân)."),
        ("BC02", "Báo cáo Phân phối đại lý B2B", "Doanh thu và sản lượng xuất bán chi tiết theo từng đối tác đại lý tiếp nhận (Galle Watch, Donghochinhhang...) (Kết nối TV3 Thảo)."),
        ("BC03", "Báo cáo Cơ cấu xuất hàng", "Phân tích tỷ trọng 4 luồng xuất kho: Xuất phân phối đại lý B2B, Xuất bảo hành dịch vụ, Xuất trả hàng lỗi NCC, Xuất tiêu hủy (Kết nối TV3 Thảo)."),
        ("BC04", "Báo cáo Đổi trả & Chất lượng", "Theo dõi tỷ lệ đổi trả theo từng dòng máy, thương hiệu và trạng thái chất lượng sản phẩm (Kết nối TV4 Tâm)."),
        ("BC05", "Báo cáo Hàng chậm luân chuyển", "Thống kê danh sách đồng hồ có tuổi tồn kho trên 90 ngày và trên 180 ngày nhằm kích hoạt chính sách chiết khấu giải phóng vốn (Kết nối TV4 Tâm)."),
        ("BC06", "Báo cáo Lợi nhuận gộp", "Lợi nhuận gộp = Doanh thu xuất kho đại lý - Giá vốn đích danh từng Serial - Chi phí logistics, tính chi tiết theo từng SKU và hãng sản xuất."),
        ("BC07", "Báo cáo Công nợ hai chiều", "Đối soát song song: Khoản phải trả nhà cung cấp (Account Payable) và Khoản phải thu đại lý (Account Receivable)."),
        ("BC08", "Báo cáo Dòng tiền thuần (Cashflow)", "Theo dõi dòng tiền vào (thực thu) trừ dòng tiền ra (thực chi), giúp lãnh đạo phân biệt rõ giữa doanh thu ghi nhận và số dư tiền mặt thực tế."),
        ("BC09", "Báo cáo Nhật ký kiểm toán (Audit Trail)", "Ghi nhận chi tiết: Dấu thời gian, người thực hiện, phân hệ tác động, hành động (Thêm/Sửa/Xóa/Duyệt) và mã chứng từ tham chiếu.")
    ]
    for r_idx, r_val in enumerate(rep9_data):
        row = tbl_rep9.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    p_sec45_3, anchor_elem = add_p_after(anchor_elem,
        "\n4.5.3. Cơ chế Trực quan hóa Biểu đồ và Kết xuất Dữ liệu (CSV & In A4):\n"
        "• Biểu đồ Doanh thu 6 tháng (MPAndroidChart): Hiển thị chuỗi doanh thu thực tế qua các tháng: Tháng 6 (1,42 tỷ), Tháng 7 (1,68 tỷ), Tháng 8 (1,79 tỷ), Tháng 9 (2,03 tỷ), Tháng 10 (2,41 tỷ), Tháng 11 (3,15 tỷ đồng). Hỗ trợ Zoom mượt mà và tương tác xem chi tiết.\n"
        "• Cơ chế Xuất tệp CSV: Lớp `ReportExportManager` chuyển đổi dữ liệu từ cấu trúc `ReportTable` thành chuỗi CSV chuẩn hóa Unicode UTF-8 và ghi vào thư mục `Downloads/ChronoVault` trên thiết bị.\n"
        "• Cơ chế In ấn A4: Lớp `ReportPrintManager` tạo giao diện in động và gửi tới dịch vụ `Android PrintManager`, cho phép người dùng xem trước tài liệu (Print Preview), kết nối máy in Wi-Fi hoặc lưu dưới dạng tệp PDF chuẩn khổ giấy A4.\n\n"
        "4.5.4. Bộ 8 Test Cases Kiểm thử Chức năng Phân hệ Dashboard & Báo cáo:\n"
        "Bảng dưới đây là kết quả kiểm thử thực nghiệm 8 ca kiểm thử cốt lõi do TV5 thực hiện:",
        font_size=9.5, color_rgb=C_SLATE, space_before=6, space_after=6)

    # Bảng 8 Test Cases của Tú
    tbl_tc, anchor_elem = add_table_after(anchor_elem, 9, 5)
    tc_headers = ["Mã TC", "Mục tiêu kiểm thử", "Dữ liệu & Thao tác kiểm thử", "Kết quả mong đợi", "Đánh giá"]
    for c_idx, h in enumerate(tc_headers):
        tbl_tc.rows[0].cells[c_idx].text = h
    format_row(tbl_tc.rows[0], HEX_NAVY, is_header=True, font_size=9)
    tc_data = [
        ("TC01", "Tính giá trị tài sản tồn kho", "Nạp 3 Serial còn trong kho có giá vốn đích danh lần lượt 120, 150 và 180 triệu đồng", "Thẻ KPI hiển thị tổng giá trị tài sản đúng bằng 450 triệu đồng", "Đạt"),
        ("TC02", "Tính toán Lợi nhuận gộp", "Doanh thu 1,2 tỷ đồng; Giá vốn đích danh 850 triệu đồng; Chi phí logistics 50 triệu đồng", "Báo cáo BC06 hiển thị lợi nhuận gộp đúng bằng 300 triệu đồng", "Đạt"),
        ("TC03", "Tính tỷ lệ đổi trả hàng", "Ghi nhận 2 Serial bị khách trả lại trên tổng số 100 Serial đã xuất bán trong kỳ", "Thẻ KPI hiển thị tỷ lệ đổi trả đúng bằng 2,00%", "Đạt"),
        ("TC04", "Cảnh báo đổi trả vượt ngưỡng", "Giả lập số liệu đổi trả đạt 2,5% (vượt ngưỡng an toàn 2.0%)", "Thẻ KPI Tỷ lệ đổi trả lập tức chuyển sang màu đỏ cảnh báo", "Đạt"),
        ("TC05", "Bộ lọc thời gian báo cáo", "Chọn khoảng ngày từ 01/11/2026 đến 15/11/2026 và chọn mẫu BC01 (Nhập hàng)", "Bảng nạp đúng các chứng từ phát sinh trong kỳ của đúng nhà cung cấp", "Đạt"),
        ("TC06", "Xuất tệp dữ liệu CSV", "Mở báo cáo BC02 và bấm nút 'Xuất CSV'", "Tệp CSV được tạo thành công trong thư mục Downloads/ChronoVault", "Đạt"),
        ("TC07", "In ấn báo cáo khổ A4", "Mở báo cáo BC07 (Công nợ) và bấm nút 'In A4'", "Android PrintManager hiển thị bản xem trước đúng định dạng A4", "Đạt"),
        ("TC08", "Kiểm soát phân quyền truy cập", "Đăng nhập với vai trò ngoài ACCOUNTANT và STORE_OWNER (ví dụ: Staff)", "Hệ thống từ chối truy cập và hiển thị thông báo không đủ quyền hạn", "Đạt")
    ]
    for r_idx, r_val in enumerate(tc_data):
        row = tbl_tc.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[4].paragraphs[0].runs[0].font.bold = True

    # 3.3. Chèn 4 bảng Schema bổ sung (suppliers của Quân, serials của Quân & Hệ thống, dealers của Thảo, outbound_orders của Thảo) NGAY SAU Table 8 gốc
    anchor_elem_schema = orig_tbl_xmls[7]
    
    # Bảng suppliers
    p_sup_title, anchor_elem_schema = add_p_after(anchor_elem_schema,
        "\n6.2.2. Chi tiết thuộc tính bảng `suppliers` (Hồ sơ Nhà cung cấp & Công nợ phải trả — TV2 Nguyễn Đắc Quân thiết kế):",
        bold=True, font_size=10.5, color_rgb=C_NAVY, space_before=10, space_after=4)
        
    tbl_sup, anchor_elem_schema = add_table_after(anchor_elem_schema, 12, 6)
    sup_headers = ["Tên cột", "Kiểu dữ liệu", "Null", "Default", "Mô tả nghiệp vụ", "Ràng buộc kỹ thuật"]
    for c_idx, h in enumerate(sup_headers):
        tbl_sup.rows[0].cells[c_idx].text = h
    format_row(tbl_sup.rows[0], HEX_NAVY, is_header=True, font_size=9)
    sup_data = [
        ("supplier_id", "INT", "No", "Auto", "Mã định danh nội bộ nhà cung cấp", "PRIMARY KEY, AUTOINCREMENT"),
        ("supplier_code", "VARCHAR(50)", "No", "Không", "Mã đối tác quy ước (NCC-RLX-01, NCC-PAT-01)", "UNIQUE, NOT NULL, Viết hoa"),
        ("name", "VARCHAR(255)", "No", "Không", "Tên pháp nhân đầy đủ của nhà cung cấp", "NOT NULL"),
        ("tax_code", "VARCHAR(50)", "No", "Không", "Mã số thuế của nhà cung cấp", "UNIQUE, NOT NULL"),
        ("contact_person", "VARCHAR(100)", "Yes", "NULL", "Người đại diện thương mại phụ trách", "Có thể để trống"),
        ("email", "VARCHAR(100)", "No", "Không", "Email giao dịch chính thức", "Đúng định dạng email"),
        ("phone", "VARCHAR(20)", "No", "Không", "Số điện thoại hotline liên hệ", "NOT NULL"),
        ("address", "TEXT", "No", "Không", "Địa chỉ trụ sở chính / nhà máy chế tác", "NOT NULL"),
        ("bank_account", "VARCHAR(50)", "No", "Không", "Số tài khoản ngân hàng thụ hưởng", "NOT NULL, phục vụ đối soát UNC"),
        ("bank_name", "VARCHAR(100)", "No", "Không", "Tên ngân hàng mở tài khoản", "NOT NULL"),
        ("current_debt", "DOUBLE", "No", "0.0", "Số dư nợ phải trả hiện tại cho NCC (VNĐ)", "current_debt >= 0")
    ]
    for r_idx, r_val in enumerate(sup_data):
        row = tbl_sup.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Bảng serials
    p_ser_title, anchor_elem_schema = add_p_after(anchor_elem_schema,
        "\n6.2.3. Chi tiết thuộc tính bảng `serials` (Định danh Serial 100% & Giá vốn Đích danh — Cốt lõi Hệ thống WMS):",
        bold=True, font_size=10.5, color_rgb=C_NAVY, space_before=10, space_after=4)
        
    tbl_ser, anchor_elem_schema = add_table_after(anchor_elem_schema, 11, 6)
    ser_headers = ["Tên cột", "Kiểu dữ liệu", "Null", "Default", "Mô tả nghiệp vụ", "Ràng buộc kỹ thuật"]
    for c_idx, h in enumerate(ser_headers):
        tbl_ser.rows[0].cells[c_idx].text = h
    format_row(tbl_ser.rows[0], HEX_NAVY, is_header=True, font_size=9)
    ser_data = [
        ("serial_id", "INT", "No", "Auto", "Mã định danh bản ghi Serial nội bộ", "PRIMARY KEY, AUTOINCREMENT"),
        ("serial_number", "VARCHAR(100)", "No", "Không", "Mã khắc trên đồng hồ / mã vạch trên hộp", "UNIQUE, NOT NULL, Chặn trùng 100%"),
        ("product_sku", "VARCHAR(50)", "No", "Không", "Mã SKU mẫu đồng hồ liên kết", "FOREIGN KEY references products(sku)"),
        ("inbound_receipt_id", "INT", "No", "Không", "Mã phiếu nhập kho tạo ra Serial này", "FOREIGN KEY references inbound_receipts(receipt_id)"),
        ("unit_cost", "DOUBLE", "No", "0.0", "Đơn giá mua theo hóa đơn từ NCC", "unit_cost >= 0"),
        ("allocated_cost", "DOUBLE", "No", "0.0", "Chi phí vận chuyển & thuế phân bổ cho chiếc này", "allocated_cost >= 0"),
        ("specific_cost", "DOUBLE", "No", "0.0", "Giá vốn đích danh (unit_cost + allocated_cost)", "specific_cost = unit_cost + allocated_cost"),
        ("status", "VARCHAR(30)", "No", "'IN_STOCK'", "Trạng thái lưu kho của chiếc đồng hồ", "CHECK in ('IN_STOCK', 'RESERVED', 'SOLD', 'DEFECTIVE', 'RETURNED')"),
        ("bin_location_id", "VARCHAR(20)", "Yes", "NULL", "Vị trí ô kệ lưu trữ trong tủ an toàn K1/K2", "Liên kết vị trí ô kệ kho TV4"),
        ("created_at", "DATETIME", "No", "CURRENT_TIMESTAMP", "Thời điểm quét nhập kho thành công", "NOT NULL")
    ]
    for r_idx, r_val in enumerate(ser_data):
        row = tbl_ser.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Bảng dealers (Thảo)
    p_dlr_title, anchor_elem_schema = add_p_after(anchor_elem_schema,
        "\n6.2.4. Chi tiết thuộc tính bảng `dealers` (Hồ sơ Đại lý Đối tác B2B & Hạn mức Tín dụng — TV3 Tô Đức Thảo thiết kế):",
        bold=True, font_size=10.5, color_rgb=C_NAVY, space_before=10, space_after=4)
        
    tbl_dlr, anchor_elem_schema = add_table_after(anchor_elem_schema, 13, 6)
    dlr_headers = ["Tên cột", "Kiểu dữ liệu", "Null", "Default", "Mô tả nghiệp vụ", "Ràng buộc kỹ thuật"]
    for c_idx, h in enumerate(dlr_headers):
        tbl_dlr.rows[0].cells[c_idx].text = h
    format_row(tbl_dlr.rows[0], HEX_NAVY, is_header=True, font_size=9)
    dlr_data = [
        ("dealer_id", "INT", "No", "Auto", "Mã định danh nội bộ đại lý tiếp nhận", "PRIMARY KEY, AUTOINCREMENT"),
        ("dealer_code", "VARCHAR(50)", "No", "Không", "Mã đối tác quy ước (DL-GALLE, DL-DONGHO)", "UNIQUE, NOT NULL, Viết hoa"),
        ("name", "VARCHAR(255)", "No", "Không", "Tên pháp nhân chuỗi cửa hàng / đại lý", "NOT NULL"),
        ("tier", "VARCHAR(50)", "No", "'STANDARD'", "Cấp bậc đối tác (VIP Kim Cương, VIP Vàng, Chuẩn)", "CHECK in ('VIP_DIAMOND', 'VIP_GOLD', 'STANDARD')"),
        ("discount_rate", "DOUBLE", "No", "0.15", "Tỷ lệ chiết khấu thương mại đại lý (15% - 30%)", "discount_rate >= 0.0 AND discount_rate <= 0.50"),
        ("credit_limit", "DOUBLE", "No", "1000000000.0", "Hạn mức tín dụng nợ tối đa (Credit Limit VNĐ)", "credit_limit >= 0"),
        ("current_debt", "DOUBLE", "No", "0.0", "Số dư nợ thực tế hiện tại của đại lý (VNĐ)", "current_debt >= 0"),
        ("tax_code", "VARCHAR(50)", "No", "Không", "Mã số thuế của doanh nghiệp đại lý", "UNIQUE, NOT NULL"),
        ("contact_person", "VARCHAR(100)", "Yes", "NULL", "Người đại diện ký hợp đồng phân phối", "Có thể để trống"),
        ("phone", "VARCHAR(20)", "No", "Không", "Số điện thoại hotline liên hệ giao dịch", "NOT NULL"),
        ("address", "TEXT", "No", "Không", "Địa chỉ cửa hàng / kho nhận hàng đại lý", "NOT NULL"),
        ("is_active", "BOOLEAN", "No", "TRUE", "Trạng thái hợp tác phân phối đại lý", "TRUE: Đang hợp tác, FALSE: Khóa nợ")
    ]
    for r_idx, r_val in enumerate(dlr_data):
        row = tbl_dlr.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Bảng outbound_orders (Thảo)
    p_ord_title, anchor_elem_schema = add_p_after(anchor_elem_schema,
        "\n6.2.5. Chi tiết thuộc tính bảng `outbound_orders` (Lệnh Xuất Kho Phân Phối Đại Lý B2B — TV3 Tô Đức Thảo thiết kế):",
        bold=True, font_size=10.5, color_rgb=C_NAVY, space_before=10, space_after=4)
        
    tbl_ord, anchor_elem_schema = add_table_after(anchor_elem_schema, 13, 6)
    ord_headers = ["Tên cột", "Kiểu dữ liệu", "Null", "Default", "Mô tả nghiệp vụ", "Ràng buộc kỹ thuật"]
    for c_idx, h in enumerate(ord_headers):
        tbl_ord.rows[0].cells[c_idx].text = h
    format_row(tbl_ord.rows[0], HEX_NAVY, is_header=True, font_size=9)
    ord_data = [
        ("order_id", "INT", "No", "Auto", "Mã định danh nội bộ đơn xuất kho", "PRIMARY KEY, AUTOINCREMENT"),
        ("order_code", "VARCHAR(50)", "No", "Không", "Số chứng từ xuất kho quy ước (PX-20261117-01)", "UNIQUE, NOT NULL, Viết hoa"),
        ("dealer_id", "INT", "No", "Không", "Mã đại lý tiếp nhận lô hàng", "FOREIGN KEY references dealers(dealer_id)"),
        ("order_date", "DATETIME", "No", "CURRENT_TIMESTAMP", "Thời điểm khởi tạo đơn hàng", "NOT NULL"),
        ("total_packages", "INT", "No", "0", "Số lượng thùng quy cách xuất đóng gói", "total_packages >= 0"),
        ("total_quantity", "INT", "No", "1", "Tổng số lượng chiếc đồng hồ xuất thực tế", "total_quantity >= 1"),
        ("subtotal_amount", "DOUBLE", "No", "0.0", "Tổng giá trị đơn hàng trước chiết khấu (VNĐ)", "subtotal_amount >= 0"),
        ("discount_amount", "DOUBLE", "No", "0.0", "Số tiền chiết khấu thương mại đại lý (VNĐ)", "discount_amount >= 0"),
        ("total_amount", "DOUBLE", "No", "0.0", "Tổng tiền thanh toán sau chiết khấu (VNĐ)", "total_amount = subtotal_amount - discount_amount"),
        ("reservation_status", "VARCHAR(30)", "No", "'NONE'", "Trạng thái khóa giữ chỗ tồn kho", "CHECK in ('NONE', 'RESERVED', 'RELEASED')"),
        ("order_status", "VARCHAR(30)", "No", "'DRAFT'", "Trạng thái tiến trình đơn xuất kho", "CHECK in ('DRAFT', 'APPROVED', 'PICKING', 'COMPLETED', 'CANCELLED')"),
        ("created_by", "INT", "No", "Không", "Mã tài khoản nhân viên lập đơn", "FOREIGN KEY references users(id)")
    ]
    for r_idx, r_val in enumerate(ord_data):
        row = tbl_ord.rows[r_idx + 1]
        for c_idx, val in enumerate(r_val):
            row.cells[c_idx].text = val
        bg = HEX_WHITE if r_idx % 2 == 0 else HEX_ALT
        format_row(row, bg, is_header=False, font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 3.4. Mục 8: BỘ CÂU HỎI VẤN ĐÁP BẢO VỆ ĐỒ ÁN (GIỮ NGUYÊN 8 CÂU ĐÃ CÓ, KHÔNG THÊM CÂU MỚI)
    anchor_elem_end = orig_tbl_xmls[10]
    
    p_sec8_title, anchor_elem_end = add_p_after(anchor_elem_end,
        "\n8. PHỤ LỤC: BỘ CÂU HỎI & ĐÁP ÁN VẤN ĐÁP BẢO VỆ ĐỒ ÁN VỚI GIẢNG VIÊN HƯỚNG DẪN (TS. ĐẶNG HÙNG VĨ)",
        bold=True, font_size=11.5, color_rgb=C_NAVY, space_before=16, space_after=8)
        
    qa_list = [
        ("Câu hỏi 1: Tại sao hệ thống quản lý kho đồng hồ cao cấp xa xỉ bắt buộc phải áp dụng định danh Serial 100% mà không quản lý theo số lượng tổng như hàng tiêu dùng thông thường?",
         "Trả lời: Đồng hồ cao cấp (Rolex, Patek Philippe, Omega...) là ngành hàng có giá trị tài sản cực lớn (từ hàng trăm triệu đến hàng tỷ đồng mỗi chiếc). Mỗi chiếc xuất xưởng mang một số Serial độc bản do nhà sản xuất khắc chìm trên thân vỏ/bộ máy và ghi trên thẻ bảo hành quốc tế. Nếu chỉ quản lý số lượng tổng, doanh nghiệp sẽ đối mặt với rủi ro tráo hàng giả, thất thoát không rõ nguyên nhân, không thể xác định chiếc nào bị lỗi khi khách khiếu nại, và không đối soát được xuất xứ khi làm việc với hãng bảo hành. Việc quản lý Serial 100% gắn chặt trách nhiệm pháp lý và lịch sử luân chuyển của từng sản phẩm cụ thể."),
        
        ("Câu hỏi 2: Tại sao nhóm lựa chọn phương pháp Giá vốn Đích danh (Specific Identification) thay vì Bình quân gia quyền hay FIFO?",
         "Trả lời: Trong ngành hàng đồng hồ xa xỉ, chi phí vận chuyển bọc thép, bảo hiểm bảo mật quốc tế và thuế nhập khẩu biến động rất mạnh theo từng lô hàng cụ thể. Phương pháp Bình quân gia quyền sẽ cào bằng chi phí, dẫn đến việc hạch toán sai lệch giá trị tài sản tồn kho và báo cáo lãi giả/lỗ thật khi xuất bán từng chiếc. Phương pháp FIFO lại ép buộc xuất chiếc nhập trước, trong khi thực tế đại lý có thể yêu cầu xuất chính xác một chiếc đồng hồ cụ thể. Phương pháp Giá vốn Đích danh cộng dồn chính xác chi phí mua và chi phí logistics thực tế vào đúng mã Serial đó, đảm bảo phản ánh giá trị tài sản trung thực tuyệt đối theo chuẩn mực kế toán quốc tế IFRS."),
         
        ("Câu hỏi 3: Phân hệ Dashboard (TV5) sử dụng kiến trúc Android MVVM với Coroutines và StateFlow như thế nào để đảm bảo ứng dụng không bị giật lag (ANR)?",
         "Trả lời: Các thao tác tính toán trên Dashboard (tính tổng tài sản 18 tỷ, lợi nhuận gộp, lọc 9 báo cáo) đòi hỏi duyệt qua hàng ngàn bản ghi trong Room Database. Nếu thực hiện trên luồng chính (Main Thread), giao diện sẽ bị đơ trên 5 giây và hệ điều hành sẽ báo lỗi ANR (Application Not Responding). Nhóm áp dụng mô hình MVVM: DashboardViewModel sử dụng `viewModelScope.launch(Dispatchers.IO)` để đẩy toàn bộ truy vấn nặng xuống luồng nền. Kết quả sau khi tính toán được đóng gói vào `StateFlow<DashboardUiState>`. Lớp giao diện (Fragment) thu thập (collect) trạng thái theo vòng đời `repeatOnLifecycle`, đảm bảo giao diện luôn mượt mà ở tần số 60 FPS."),
         
        ("Câu hỏi 4: Cơ chế Kiểm soát Phân quyền RBAC 5 Roles giữa các thành viên và Actor hoạt động ra sao để đảm bảo an toàn dữ liệu?",
         "Trả lời: Hệ thống định nghĩa 5 vai trò cố định: SYSTEM_ADMIN (Quản trị hệ thống), STORE_OWNER (Chủ cửa hàng), WAREHOUSE_MANAGER (Thủ kho), OPERATIONS_STAFF (Nhân viên nhập - xuất) và ACCOUNTANT (Kế toán). Khi đăng nhập, `SessionManager` lưu thông tin phiên làm việc và vai trò của tài khoản. Tại mỗi Fragment/Activity, hệ thống kiểm tra thẩm quyền trước khi hiển thị nút thao tác: ví dụ chỉ Kế toán và Chủ cửa hàng mới nhìn thấy nút 'Duyệt phiếu chi' và xem 'Lợi nhuận gộp'; Nhân viên nhập kho không được xem báo cáo dòng tiền; Thủ kho chỉ được xác nhận số lượng vật lý và chuyển kệ."),
         
        ("Câu hỏi 5: Làm sao để đảm bảo tính toàn vẹn dữ liệu khi quy đổi ĐVT (Thùng ra Chiếc) kết hợp quét mã Serial bằng Camera ML Kit?",
         "Trả lời: Hệ thống thiết lập quy tắc bắt buộc: Số lượng quét = Số thùng × Hệ số quy đổi + Số chiếc lẻ. Khi camera quét từng mã, hệ thống kiểm tra trùng lặp 2 cấp (trùng trong danh sách tạm và trùng trong Room Database). Nút 'Hoàn tất' chỉ được mở khóa khi số mã quét được BẰNG CHÍNH XÁC 100% số lượng quy đổi và không có bất kỳ mã nào trùng. Toàn bộ thao tác lưu phiếu, tạo N bản ghi Serial và tăng công nợ NCC được bọc trong một Transaction Room Database duy nhất (`@Transaction`), nếu có bất kỳ lỗi nào xảy ra thì hệ thống tự động Rollback hoàn toàn."),
         
        ("Câu hỏi 6: Sự khác biệt cốt lõi giữa Báo cáo Doanh thu (BC02) và Báo cáo Dòng tiền thuần (BC08) trong phân hệ TV5?",
         "Trả lời: Báo cáo Doanh thu (BC02) được ghi nhận theo nguyên tắc dồn tích (Accrual Accounting) ngay khi lệnh xuất kho đại lý được duyệt COMPLETED, bất kể đại lý đã trả tiền hay chưa (có thể đang nợ theo hạn mức). Ngược lại, Báo cáo Dòng tiền (BC08) hoạt động theo nguyên tắc thực thu - thực chi (Cash Basis): tiền vào chỉ tăng khi thủ quỹ lập phiếu thu thực tế, tiền ra chỉ tăng khi kế toán lập ủy nhiệm chi trả NCC. Nhờ tách biệt 2 báo cáo này, Chủ cửa hàng thấy rõ doanh nghiệp đang có lãi trên sổ sách nhưng có bị đứt gãy dòng tiền mặt hay không."),
         
        ("Câu hỏi 7: Khi có nhiều nhân viên kho cùng thao tác quét mã Serial hoặc tạo lệnh xuất đồng thời thì hệ thống xử lý tranh chấp dữ liệu (Race Condition) như thế nào?",
         "Trả lời: Hệ thống bảo vệ dữ liệu ở cả 2 tầng: Tầng CSDL áp dụng khóa chính `serial_number` với thuộc tính UNIQUE để chặn trùng tuyệt đối. Tầng nghiệp vụ áp dụng cơ chế Khóa giữ chỗ (Reservation Engine): khi một nhân viên tạo lệnh xuất cho đại lý, các mã Serial khả dụng sẽ lập tức được chuyển sang trạng thái RESERVED. Các nhân viên khác khi quét tìm hàng sẽ không thể nhìn thấy hoặc chọn các Serial này, loại bỏ hoàn toàn nguy cơ tranh chấp một chiếc đồng hồ cho hai đơn hàng khác nhau."),
         
        ("Câu hỏi 8: Quy trình xuất trả hàng lỗi kỹ thuật cho Nhà cung cấp (TV2) được kiểm soát như thế nào để không làm lệch tồn kho và sổ sách kế toán?",
         "Trả lời: Quy trình gồm 4 bước chặt chẽ: (1) Thủ kho phát hiện lỗi cơ học/mặt kính, chuyển trạng thái Serial sang DEFECTIVE và cách ly vào khu vực Kệ hàng lỗi. (2) Nhân viên nhập kho lập đề nghị trả hàng, dẫn chiếu đúng phiếu nhập gốc và quét mã Serial lỗi. (3) Kế toán đối soát với NCC về chính sách bảo hành/hoàn tiền. (4) Khi chứng từ xuất trả được duyệt, Serial chuyển sang trạng thái RETURNED, hệ thống tự động trừ tồn kho và giảm trừ công nợ phải trả NCC tương ứng.")
    ]
    for q_idx, (q_text, a_text) in enumerate(qa_list):
        p_q, anchor_elem_end = add_p_after(anchor_elem_end, f"8.{q_idx + 1}. {q_text}", 
                                           bold=True, font_size=9.5, color_rgb=C_NAVY, space_before=8, space_after=3)
        p_a, anchor_elem_end = add_p_after(anchor_elem_end, a_text, 
                                           bold=False, font_size=9, color_rgb=C_SLATE, space_before=0, space_after=6)

    # =============================================================
    # BƯỚC 4: LƯU FILE WORD CHÍNH THỨC
    # =============================================================
    try:
        doc.save(output_path)
        print(f"SUCCESS: Đã xuất file báo cáo Master tích hợp 4 phân hệ thành công tại:\n{output_path}")
    except PermissionError:
        alt_path = r"D:\cntt\pbhb\Document\BAO_CAO_PHAN_TICH_HE_THONG_THONG_TIN_CHRONOVAULT_WMS_CAP_NHAT.docx"
        doc.save(alt_path)
        print(f"LOCKED: File chính đang mở trong Word, đã lưu sang file dự phòng:\n{alt_path}")

if __name__ == "__main__":
    generate_master_report()
