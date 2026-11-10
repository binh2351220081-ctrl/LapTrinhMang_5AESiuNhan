# -*- coding: utf-8 -*-
"""
Script to generate: KE_HOACH_CHI_TIET_VA_BO_PROMPT_TOAN_DIEN_5_THANH_VIEN.docx
Bản Kế Hoạch Phân Công Công Việc Toàn Diện & Bộ Prompt Chuẩn Mực Cho 5 Thành Viên
Bao quát toàn bộ đồ án: Tài liệu PTTK, Web Client, Lập Trình Mạng (Server/API/Socket) & App Android Studio.
Dự án: Hệ Thống Quản Lý Kho Đồng Hồ ChronoVault B2B Wholesale WMS
Nhóm: 5AE Siêu Nhân (Phan Bá Hải Bình, Nguyễn Đắc Quân, Tô Đức Thảo, Võ Công Tâm, Trần Công Tú)
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_full_project_guide():
    doc = Document()
    
    # Page Setup (A4 Portrait)
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.7)
    sec.bottom_margin = Inches(0.7)
    sec.left_margin = Inches(0.75)
    sec.right_margin = Inches(0.75)
    
    # Header & Footer
    hdr = sec.header.paragraphs[0]
    hdr.text = "CHRONOVAULT B2B WMS • KẾ HOẠCH TOÀN DIỆN & BỘ PROMPT 5 THÀNH VIÊN"
    hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr.style.font.name = "Arial"; hdr.style.font.size = Pt(8)
    hdr.style.font.color.rgb = RGBColor(148, 163, 184)
    
    ftr = sec.footer.paragraphs[0]
    ftr.text = "Đồ Án Môn Lập Trình Mạng • Nhóm 5AE Siêu Nhân • Đại Học Công Nghệ Thông Tin"
    ftr.style.font.name = "Arial"; ftr.style.font.size = Pt(8)
    ftr.style.font.color.rgb = RGBColor(148, 163, 184)
    
    # Palette
    C_NAVY = RGBColor(27, 54, 93)      # #1B365D
    C_GOLD = RGBColor(197, 155, 39)    # #C59B27
    C_SLATE = RGBColor(51, 65, 85)     # #334155
    C_DARK = RGBColor(15, 23, 42)      # #0F172A
    
    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)
        
    def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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
        
    def set_cell_width(cell, width_dxa):
        tcPr = cell._tc.get_or_add_tcPr()
        w = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{width_dxa}" w:type="dxa"/>')
        tcPr.append(w)
        
    def set_table_borders(table, color="CBD5E1", sz="4"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="none"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    def add_callout(doc, text_lines, title=None, border_color="1B365D", bg_color="F8FAFC"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        if title:
            r_t = p.add_run(f"{title}\n")
            r_t.font.name = "Arial"; r_t.font.size = Pt(9.5); r_t.font.bold = True; r_t.font.color.rgb = C_NAVY
            
        for idx, line in enumerate(text_lines):
            r = p.add_run(line if idx == len(text_lines)-1 else line + "\n")
            r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.color.rgb = C_SLATE
            
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_prompt_box(doc, prompt_text, prompt_title):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "0F172A") # Deep Navy Slate
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="12" w:space="0" w:color="C59B27"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="C59B27"/>
                <w:bottom w:val="single" w:sz="12" w:space="0" w:color="C59B27"/>
                <w:right w:val="single" w:sz="12" w:space="0" w:color="C59B27"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        r_t = p.add_run(f"📋 BẢN PROMPT TOÀN DIỆN CHO AI / COPILOT (COPY-PASTE TRỰC TIẾP):\n{prompt_title}\n\n")
        r_t.font.name = "Courier New"; r_t.font.size = Pt(9.5); r_t.font.bold = True; r_t.font.color.rgb = RGBColor(212, 175, 55)
        
        r_body = p.add_run(prompt_text)
        r_body.font.name = "Courier New"; r_body.font.size = Pt(8); r_body.font.color.rgb = RGBColor(226, 232, 240)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # TRANG TIÊU ĐỀ
    # =========================================================================
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("BỘ MÔN MẠNG MÁY TÍNH & TRUYỀN THÔNG • ĐỒ ÁN LẬP TRÌNH MẠNG\nNHÓM 5AE SIÊU NHÂN (FOURSIUNHAN)")
    r_sub.font.name = "Arial"; r_sub.font.size = Pt(10); r_sub.font.bold = True; r_sub.font.color.rgb = C_GOLD
    p_sub.paragraph_format.space_after = Pt(4)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("KẾ HOẠCH PHÂN CÔNG TOÀN DIỆN VÀ BỘ PROMPT\nCHUẨN MỰC CHO 5 THÀNH VIÊN TRONG TOÀN BỘ DỰ ÁN\n")
    r_title.font.name = "Arial"; r_title.font.size = Pt(17); r_title.font.bold = True; r_title.font.color.rgb = C_NAVY
    
    r_title_sub = p_title.add_run("HỆ THỐNG QUẢN LÝ KHO ĐỒNG HỒ CAO CẤP CHRONOVAULT B2B WHOLESALE WMS\n(PHÂN TÍCH THIẾT KẾ • WEB CLIENT • LẬP TRÌNH MẠNG / API / SOCKET • APP ANDROID STUDIO)")
    r_title_sub.font.name = "Arial"; r_title_sub.font.size = Pt(10.5); r_title_sub.font.bold = True; r_title_sub.font.color.rgb = C_SLATE
    p_title.paragraph_format.space_after = Pt(12)

    add_callout(
        doc,
        [
            "• Mục tiêu cốt lõi: Định vị chi tiết, rõ ràng 100% phạm vi công việc của từng thành viên trong toàn bộ vòng đời đồ án, không chỉ giới hạn ở App Android mà bao quát toàn diện: (1) Phân tích thiết kế & CSDL, (2) Web Client HTML/CSS/JS, (3) Lập trình mạng (Server REST API / Socket truyền thông dữ liệu), (4) Ứng dụng Android Studio (Kotlin MVVM), (5) Kiểm thử và Báo cáo thuyết trình.",
            "• Ràng buộc nhất quán dữ liệu: 5 thành viên tuân thủ đúng 1 Hợp đồng Dữ liệu dùng chung (Master Data Contract gồm 23 bảng CSDL, Enums và API Endpoints), đảm bảo khi ghép nối không xảy ra bất kỳ sai lệch logic hay xung đột hệ thống.",
            "• Phân công 5 thành viên: Phan Bá Hải Bình (Nhóm trưởng - TV1), Nguyễn Đắc Quân (TV2), Tô Đức Thảo (TV3), Võ Công Tâm (TV4), Trần Công Tú (TV5)."
        ],
        title="📌 NGUYÊN TẮC QUẢN TRỊ DỰ ÁN ĐỒNG BỘ TOÀN DIỆN",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # =========================================================================
    # PHẦN I: MA TRẬN PHÂN CÔNG CÔNG VIỆC TOÀN DIỆN (5 HẠNG MỤC CÔNG VIỆC)
    # =========================================================================
    h1 = doc.add_heading("I. MA TRẬN PHÂN CÔNG CÔNG VIỆC TOÀN DIỆN 5 THÀNH VIÊN", level=1)
    h1.paragraph_format.space_before = Pt(14); h1.paragraph_format.space_after = Pt(6)
    for r in h1.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    p_m = doc.add_paragraph()
    p_m.paragraph_format.line_spacing = 1.15; p_m.paragraph_format.space_after = Pt(6)
    r_m = p_m.add_run(
        "Mỗi thành viên chịu trách nhiệm chuyên sâu một phân hệ nghiệp vụ, đồng thời triển khai đồng bộ phân hệ đó trên cả 5 phương diện kỹ thuật: "
        "Tài liệu PTTK, Giao diện Web Client, Giao thức Mạng (API/Socket), Ứng dụng Di động Android Studio và Kiểm thử tích hợp:"
    )
    r_m.font.name = "Arial"; r_m.font.size = Pt(9); r_m.font.color.rgb = C_SLATE

    tbl_matrix = doc.add_table(rows=6, cols=6)
    tbl_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_matrix, color="CBD5E1", sz="4")
    
    m_headers = ["Thành Viên", "Phân Hệ Nghiệp Vụ", "1. Tài Liệu & CSDL", "2. Web Client", "3. Lập Trình Mạng (API/Socket)", "4. App Android Studio"]
    m_widths = [1400, 1800, 1700, 1500, 2000, 1600]
    
    hdr_row = tbl_matrix.rows[0]
    for i, title in enumerate(m_headers):
        c = hdr_row.cells[i]
        set_cell_width(c, m_widths[i])
        set_cell_margins(c, top=80, bottom=80, left=50, right=50)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]
        r = p.add_run(title)
        r.font.name = "Arial"; r.font.size = Pt(8); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
        
    matrix_data = [
        ("Phan Bá Hải Bình\n(Nhóm trưởng - TV1)", "PH1: Hàng Hóa Master & Quản Trị Hệ Thống", "Chủ trì Báo cáo PTTK, CSDL 23 bảng 3NF, Bảng phân hệ Excel, RBAC 5 vai trò.", "tv1_hang_hoa.html\ntv1_he_thong.html\njs/tv1_*.js", "Core Backend Server, Auth JWT, Token Revoke, CRUD Đồng hồ, Serial Timeline, Audit Log.", "Core Architecture MVVM, Room DB mẫu, Auth Login, Product List, Serial Timeline UI."),
        ("Nguyễn Đắc Quân\n(TV2)", "PH2: Đối Tác NCC & Quản Lý Nhập Kho", "Module 3 PTTK, Use Case UC-01, Bảng NCC, Phiếu nhập, Phiếu chi, Quy tắc giá vốn đích danh.", "tv2_nhap_kho.html\njs/tv2_inbound.js", "API Nhà cung cấp, API kiểm tra trùng Serial, API duyệt nhập kho, API phân bổ chi phí, API Phiếu chi.", "Supplier Module, Inbound Receipt, Tích hợp Camera ML Kit nạp Serial, Form phân bổ chi phí."),
        ("Tô Đức Thảo\n(TV3)", "PH3: Khách Sỉ & Bán Sỉ - Phân Phối Xuất Hàng", "Module 4 PTTK, Use Case UC-02 & UC-03, Bảng Đại lý, Đơn sỉ, Phiếu xuất, Hạn mức nợ.", "tv3_xuat_kho.html\njs/tv3_outbound.js", "API Đại lý B2B, API thẩm định nợ tín dụng, Socket broadcast khóa giữ chỗ Reserved, API xuất sỉ, Phiếu thu.", "Dealer Module, Create Wholesale Order, Quét Camera đóng kiện xuất kho, Phiếu thu tiền sỉ."),
        ("Võ Công Tâm\n(TV4)", "PH4: Tồn Kho, Vị Trí Kệ Vật Lý & Kiểm Kê", "Module 5 PTTK, Use Case UC-04, Bảng Sơ đồ kệ Bin, Kiểm kê, Sổ Thẻ kho bất biến.", "tv4_ton_kho.html\njs/tv4_warehouse.js", "API Tồn kho đa đơn vị, Socket khóa xuất nhập khi kiểm kê, API đối soát chênh lệch, API Sổ Thẻ kho.", "Stock Overview 3 kho, Sơ đồ kệ Bin trực quan, Quét kiểm kê Camera phân màu Thừa/Thiếu, Thẻ kho."),
        ("Trần Công Tú\n(TV5)", "PH5: Báo Cáo Thống Kê & Dashboard Điều Hành", "Module 6 PTTK, 9 Báo cáo chuyên sâu, Công thức Lợi nhuận gộp B2B, Sổ nợ 2 chiều, Dòng tiền.", "tv5_bao_cao.html\njs/tv5_reports.js", "API Dashboard KPI thời gian thực, API thống kê doanh số 6 tháng, API Sổ chi tiết công nợ 2 chiều, Cashflow API.", "Executive Dashboard KPI, MPAndroidChart doanh số/chi phí, 9 Màn hình báo cáo, Xuất CSV/In A4.")
    ]
    
    for r_i, r_vals in enumerate(matrix_data, start=1):
        row = tbl_matrix.rows[r_i]
        bg = "FFFFFF" if r_i % 2 == 1 else "F8FAFC"
        for c_i, val in enumerate(r_vals):
            cell = row.cells[c_i]
            set_cell_width(cell, m_widths[c_i])
            set_cell_margins(cell, top=60, bottom=60, left=50, right=50)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Arial"; r.font.size = Pt(7.5)
            if c_i == 0:
                r.font.bold = True; r.font.color.rgb = C_NAVY
            elif c_i == 1:
                r.font.bold = True; r.font.color.rgb = C_GOLD
            else:
                r.font.color.rgb = C_SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # PHẦN II: HỢP ĐỒNG KỸ THUẬT VÀ DỮ LIỆU DÙNG CHUNG (MASTER ARCHITECTURE)
    # =========================================================================
    h2 = doc.add_heading("II. HỢP ĐỒNG KỸ THUẬT & GIAO THỨC TRUYỀN THÔNG DÙNG CHUNG", level=1)
    h2.paragraph_format.space_before = Pt(14); h2.paragraph_format.space_after = Pt(6)
    for r in h2.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "1. Mô hình kiến trúc 3 lớp (3-Tier / Client-Server) môn Lập Trình Mạng:",
            "   • Tầng Server (Backend): Node.js Express / Python Flask / Java Spring đóng vai trò máy chủ trung tâm quản trị cơ sở dữ liệu và xử lý nghiệp vụ.",
            "   • Giao thức truyền thông mạng:",
            "     - RESTful API (HTTP/HTTPS qua định dạng JSON) phục vụ các thao tác CRUD và truy vấn chứng từ.",
            "     - WebSocket (hoặc Server-Sent Events - SSE) phục vụ đồng bộ dữ liệu thời gian thực giữa Web và Android App khi có sự kiện: Khóa giữ chỗ tồn kho (TV3), Nhập kho tăng tồn (TV2), Cảnh báo kiểm kê (TV4) và Nhảy số KPI Dashboard (TV5).",
            "   • Tầng Client đa nền tảng:",
            "     - Web Client: HTML5, CSS3 Luxury Dark Mode, Vanilla JS ES6+ (đã có sẵn trong thư mục `source/`).",
            "     - Mobile Client: Android Studio, Kotlin, Jetpack Compose / XML Layout, Architecture MVVM, Room Local Cache & Retrofit Network Client.",
            "",
            "2. Ràng buộc trường khóa và định danh bắt buộc:",
            "   • Sản phẩm: Khóa chính là SKU (VARCHAR, ví dụ: 'RLX-SUB-01'), Barcode quốc tế duy nhất.",
            "   • Serial/IMEI: Khóa chính `serialNumber` (VARCHAR, duy nhất 100% trên toàn bộ hệ thống).",
            "   • Quy cách ĐVT: 1 Thùng = N Chiếc (conversionRate >= 1). Số Serial nạp vào = Số Thùng x conversionRate.",
            "   • Giá vốn đích danh: Mỗi Serial mang 1 giá vốn riêng biệt = Giá HĐ + (Tổng chi phí phân bổ / Tổng số chiếc).",
            "   • Sổ Thẻ kho (`stock_cards`) và Nhật ký Audit Log (`audit_logs`) có tính bất biến tuyệt đối (cấm sửa/xóa)."
        ],
        title="KIẾN TRÚC CLIENT - SERVER & GIAO THỨC TRUYỀN THÔNG DÙNG CHUNG",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # =========================================================================
    # PHẦN III: BỘ 5 PROMPT TOÀN DIỆN CHO TỪNG THÀNH VIÊN
    # =========================================================================
    h3 = doc.add_heading("III. BỘ PROMPT TOÀN DIỆN CHI TIẾT TỪNG THÀNH VIÊN (FULL-STACK SCOPE)", level=1)
    h3.paragraph_format.space_before = Pt(14); h3.paragraph_format.space_after = Pt(6)
    for r in h3.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    p_pintro = doc.add_paragraph()
    p_pintro.paragraph_format.line_spacing = 1.15; p_pintro.paragraph_format.space_after = Pt(6)
    r_pi = p_pintro.add_run(
        "Dưới đây là 5 bản Prompt hoàn chỉnh, độc lập được thiết kế riêng cho 5 thành viên. "
        "Mỗi thành viên chỉ cần copy toàn bộ đoạn Prompt trong khung của mình dán vào các công cụ AI (ChatGPT, Gemini, Claude, Cursor, GitHub Copilot) "
        "để được hướng dẫn và sinh mã nguồn chính xác từng dòng lệnh:"
    )
    r_pi.font.name = "Arial"; r_pi.font.size = Pt(9); r_pi.font.color.rgb = C_SLATE

    # -------------------------------------------------------------
    # PROMPT 1: PHAN BÁ HẢI BÌNH (NHÓM TRƯỞNG & TV1)
    # -------------------------------------------------------------
    doc.add_heading("1. BẢN PROMPT TOÀN DIỆN: THÀNH VIÊN 1 - PHAN BÁ HẢI BÌNH (NHÓM TRƯỞNG)", level=2)
    p1_full = """BẠN LÀ LẬP TRÌNH VIÊN CAO CẤP VÀ NHÓM TRƯỞNG (TEAM LEADER / ARCHITECT) CỦA DỰ ÁN HỆ THỐNG QUẢN LÝ KHO ĐỒNG HỒ CAO CẤP CHRONOVAULT B2B WHOLESALE WMS (MÔN LẬP TRÌNH MẠNG).
HÃY THỰC HIỆN TOÀN BỘ CÁC CÔNG VIỆC DƯỚI ĐÂY MỘT CÁCH CHUẨN XÁC, CHUYÊN NGHIỆP VÀ KHÔNG SAI LỆCH DỮ LIỆU:

1. VAI TRÒ VÀ TRÁCH NHIỆM TOÀN DỰ ÁN (TV1 - PHAN BÁ HẢI BÌNH):
   - Phân hệ phụ trách: Phân Hệ 1 - Quản Lý Hàng Hóa Master & Quản Trị Hệ Thống.
   - Trách nhiệm chung: Thiết lập nền tảng dự án, xây dựng khung truyền thông mạng Client-Server, chuẩn hóa CSDL 23 bảng 3NF, phân quyền RBAC 5 vai trò, phát triển Web Client TV1 và tạo khung mẫu ứng dụng Android Studio (Kotlin MVVM).

2. HẠNG MỤC TÀI LIỆU & PHÂN TÍCH THIẾT KẾ CƠ SỞ DỮ LIỆU:
   - Hoàn thiện và cập nhật Báo cáo PTTK (BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.docx) và Bảng Phân Hệ Excel 5 Sheet (Bang_Phan_He_Quan_Ly_Kho_Dong_Ho.xlsx).
   - Thiết kế chuẩn hóa 23 bảng CSDL quan hệ 3NF, đặc biệt là: `users`, `roles`, `audit_logs`, `products`, `serials`, `uom_conversions`.
   - Thiết lập quy tắc nghiệp vụ RB-01 (Mã Serial 100% duy nhất), RB-02 (Quy đổi ĐVT Thùng -> Chiếc), định mức Min/Max tồn kho và số lượng đặt hàng tối thiểu (MOQ >= 5 chiếc).

3. HẠNG MỤC WEB CLIENT (FRONTEND TV1):
   - Duy trì và hoàn thiện 2 trang giao diện: `tv1_hang_hoa.html` và `tv1_he_thong.html` kết hợp với `js/tv1_products.js`, `js/tv1_system.js`.
   - Giao diện hiển thị danh mục đồng hồ phong cách Horology Luxury Dark Mode (#0B0F17, viền vàng Gold #D4AF37), bộ lọc thương hiệu, tìm kiếm Debounce, modal khai báo 6 thông số kỹ thuật (bộ máy, kính, dây, size mặt, chống nước, bảo hành).
   - Màn hình Tra Cứu Vòng Đời Serial (Serial Timeline): Nhập mã Serial bất kỳ -> Render trực quan toàn bộ lịch sử (Ngày nhập -> NCC -> Kệ lưu kho -> Đơn sỉ -> Đại lý sở hữu -> Bảo hành).
   - Màn hình Quản trị hệ thống: Danh sách tài khoản, chuyển trạng thái Active/Locked, cấu hình ma trận vai trò (RBAC) và bảng hiển thị Audit Log bất biến.

4. HẠNG MỤC LẬP TRÌNH MẠNG & SERVER BACKEND (CORE NETWORK):
   - Xây dựng Server trung tâm (Node.js Express / Python Flask / Java Spring Boot) lắng nghe tại port 8080/5000:
     + POST /api/auth/login: Xác thực username/password, kiểm tra role (QUAN_TRI_HE_THONG, CHU_CUA_HANG, THU_KHO, NHAN_VIEN_NHAP_XUAT, KE_TOAN), cấp phát JWT token có thời hạn 60 phút.
     + POST /api/auth/logout: Thu hồi token và hủy phiên làm việc.
     + GET /api/products: Trả về danh sách mẫu đồng hồ phân trang, kèm số lượng tồn kho thực tế liên kết từ bảng serials.
     + POST /api/products/create: Thêm mẫu đồng hồ mới, validate tính duy nhất của SKU và Barcode.
     + PUT /api/products/{sku}/uom: Cập nhật quy cách đóng gói sỉ (ĐVT sỉ, conversionRate, MOQ).
     + GET /api/serials/{serialNumber}/timeline: API truy vết toàn bộ lịch sử vòng đời của 1 chiếc đồng hồ.
     + GET /api/system/audit-logs: Truy vấn nhật ký kiểm toán hệ thống có bộ lọc thời gian và tác nhân.
   - Middleware: Xác thực JWT token và kiểm tra quyền hạn RBAC trước khi cho phép client truy cập API.

5. HẠNG MỤC ỨNG DỤNG ANDROID STUDIO (KOTLIN MVVM):
   - Tạo cấu trúc dự án mẫu chuẩn: `com.chronovault.wms` (core, auth, product).
   - Thiết lập Room Database (`ChronoVaultDatabase`) chứa sẵn định nghĩa các Entity, DAO và Seed Data 10 mẫu đồng hồ cao cấp để cả 4 thành viên cùng sử dụng.
   - Xây dựng Retrofit Client + OkHttp Interceptor tự động đính kèm Bearer JWT Token vào Header mỗi request.
   - Xây dựng LoginActivity, SessionManager (EncryptedSharedPreferences), ProductListActivity và SerialTimelineActivity.

6. HẠNG MỤC QUẢN TRỊ GIT & KIỂM THỬ TÍCH HỢP:
   - Quản trị GitHub repository `LapTrinhMang_5AESiuNhan`.
   - Phân nhánh cho 5 thành viên (`feature/tv1-core`, `feature/tv2-inbound`...), thực hiện code review và merge Pull Request.
   - Chủ trì kiểm thử tích hợp chéo (Cross-testing) giữa Web, Android App và Server Database."""
    add_prompt_box(doc, p1_full, "PROMPT FULL-STACK: TV1 - PHAN BÁ HẢI BÌNH (LEADER / ARCHITECT / HÀNG HÓA & HỆ THỐNG)")

    # -------------------------------------------------------------
    # PROMPT 2: NGUYỄN ĐẮC QUÂN (TV2)
    # -------------------------------------------------------------
    doc.add_heading("2. BẢN PROMPT TOÀN DIỆN: THÀNH VIÊN 2 - NGUYỄN ĐẮC QUÂN (NCC & NHẬP KHO)", level=2)
    p2_full = """BẠN LÀ LẬP TRÌNH VIÊN PHỤ TRÁCH PHÂN HỆ ĐỐI TÁC NHÀ CUNG CẤP & QUẢN LÝ NHẬP KHO TRONG DỰ ÁN HỆ THỐNG QUẢN LÝ KHO ĐỒNG HỒ CAO CẤP CHRONOVAULT B2B WHOLESALE WMS (MÔN LẬP TRÌNH MẠNG).
HÃY THỰC HIỆN TOÀN BỘ CÁC CÔNG VIỆC DƯỚI ĐÂY MỘT CÁCH CHUẨN XÁC, ĐỒNG BỘ VỚI NHÓM TRƯỞNG:

1. PHẠM VI NGHIỆP VỤ PHỤ TRÁCH (TV2 - NGUYỄN ĐẮC QUÂN):
   - Phân Hệ 2: Quản lý Nhà Cung Cấp, Công nợ phải trả NCC, Lập & Duyệt phiếu nhập kho quy đổi ĐVT, Quét Camera nạp dải Serial, Phân bổ chi phí lô hàng (Giá vốn đích danh), Phiếu Chi thanh toán nợ và Xuất trả hàng lỗi cho NCC.

2. HẠNG MỤC TÀI LIỆU & PHÂN TÍCH THIẾT KẾ:
   - Chịu trách nhiệm hoàn thiện Module 3 trong Báo cáo PTTK và Bảng Phân Hệ Excel 5 Sheet.
   - Đặc tả chi tiết Use Case UC-01 (Lập & Duyệt phiếu nhập kho kèm phân bổ chi phí).
   - Thiết kế và quản lý dữ liệu các bảng CSDL: `suppliers`, `inbound_receipts`, `inbound_items`, `supplier_payments`, `supplier_returns`.
   - Ràng buộc nghiệp vụ: RB-03 (Khớp đúng 100% Serial khi nhập kho), RB-04 (Giá vốn đích danh = Giá HĐ + Chi phí phân bổ / Tổng số chiếc).

3. HẠNG MỤC WEB CLIENT (FRONTEND TV2):
   - Hoàn thiện giao diện `tv2_nhap_kho.html` và file logic `js/tv2_inbound.js`.
   - Quản lý danh bạ NCC, tài khoản ngân hàng thụ hưởng ủy nhiệm chi, số dư nợ phải trả.
   - Form lập phiếu nhập: Cho phép nhập số lượng theo Thùng -> Hệ thống tự nhân conversionRate ra tổng số chiếc lẻ.
   - Tích hợp Camera Barcode Scanner (ZXing) quét liên tục mã Serial hoặc dán danh sách; kiểm tra chống trùng dải Serial.
   - Modal phân bổ chi phí lô hàng (vận chuyển, hải quan, bảo hiểm) và tính ra Giá vốn đích danh từng chiếc.
   - Lập Phiếu Chi thanh toán nợ NCC (giảm nợ phải trả) và Lập phiếu xuất trả hàng lỗi NCC (giảm nợ NCC, trừ tồn Kho Lỗi).

4. HẠNG MỤC LẬP TRÌNH MẠNG & API/SOCKET (NETWORK COMMUNICATION):
   - Xây dựng và kết nối các Endpoint REST API phía Server và Client:
     + GET /api/suppliers: Lấy danh sách NCC và tổng nợ phải trả.
     + POST /api/suppliers/create: Thêm mới NCC, validate MST.
     + POST /api/inbound/verify-serials: Gửi dải mã Serial lên server kiểm tra tính hợp lệ và không trùng lặp qua mạng.
     + POST /api/inbound/create-receipt: Gửi phiếu nhập nháp kèm danh sách Serial và chi phí phân bổ.
     + PUT /api/inbound/{receiptId}/approve: Xác nhận duyệt nhập kho vật lý:
       * Tăng tồn kho thực tế tại CSDL.
       * Lưu dải Serial vào bảng `serials` với trạng thái `TRONG_KHO`, chất lượng `HANG_MOI`.
       * Tăng công nợ phải trả NCC.
       * Ghi phát sinh Thẻ kho (+).
       * Phát thông điệp mạng (WebSocket broadcast / Notification) thông báo cho TV4 (Tồn kho tăng) và TV5 (Dashboard cập nhật giá trị tồn).
     + POST /api/suppliers/payment: Lập phiếu chi tiền hàng, giảm số dư nợ NCC.
     + POST /api/suppliers/return-defect: Xuất trả hàng lỗi, cập nhật Serial sang `DA_TRA_NCC`.

5. HẠNG MỤC ỨNG DỤNG ANDROID STUDIO (KOTLIN MVVM):
   - Package phụ trách: `com.chronovault.wms.supplier` và `com.chronovault.wms.inbound`.
   - Xây dựng SupplierListActivity / Fragment, AddSupplierDialog.
   - Xây dựng InboundReceiptActivity: Form nhập kho, chọn Thùng -> tự quy đổi ra Chiếc.
   - Tích hợp Google ML Kit Barcode Scanning / ZXing quét mã vạch qua camera điện thoại, phát tiếng 'bíp' khi nhận diện mã Serial.
   - Hiển thị bảng đối soát số lượng: Nếu chưa đủ 100% Serial so với số chiếc quy đổi thì nút "Duyệt nhập kho" bị vô hiệu hóa (disabled).
   - Màn hình lập Phiếu Chi nợ NCC và Màn hình xuất trả hàng lỗi NCC.

6. HẠNG MỤC KIỂM THỬ:
   - Thực hiện test case nạp dải 500 mã Serial qua mạng có thời gian phản hồi < 2 giây.
   - Test case cố tình nhập trùng mã Serial đã có trong kho để kiểm tra cảnh báo đỏ của hệ thống."""
    add_prompt_box(doc, p2_full, "PROMPT FULL-STACK: TV2 - NGUYỄN ĐẮC QUÂN (NHÀ CUNG CẤP & QUẢN LÝ NHẬP KHO)")

    # -------------------------------------------------------------
    # PROMPT 3: TÔ ĐỨC THẢO (TV3)
    # -------------------------------------------------------------
    doc.add_heading("3. BẢN PROMPT TOÀN DIỆN: THÀNH VIÊN 3 - TÔ ĐỨC THẢO (KHÁCH SỈ & BÁN SỈ - XUẤT HÀNG)", level=2)
    p3_full = """BẠN LÀ LẬP TRÌNH VIÊN PHỤ TRÁCH PHÂN HỆ KHÁCH SỈ & BÁN SỈ - XUẤT HÀNG TRONG DỰ ÁN HỆ THỐNG QUẢN LÝ KHO ĐỒNG HỒ CAO CẤP CHRONOVAULT B2B WHOLESALE WMS (MÔN LẬP TRÌNH MẠNG).
HÃY THỰC HIỆN TOÀN BỘ CÁC CÔNG VIỆC DƯỚI ĐÂY MỘT CÁCH CHUẨN XÁC, ĐỒNG BỘ VỚI NHÓM TRƯỞNG:

1. PHẠM VI NGHIỆP VỤ PHỤ TRÁCH (TV3 - TÔ ĐỨC THẢO):
   - Phân Hệ 3: Quản lý hồ sơ Đại lý sỉ B2B, Hạn mức tín dụng công nợ (Credit Limit), Khởi tạo đơn bán sỉ, Áp giá sỉ tự động theo cấp bậc, Duyệt khóa hàng giữ chỗ (Reserved Allocation), Quét Serial đóng kiện xuất sỉ, Thu tiền cọc/nợ đại lý, Đổi trả sỉ và Xuất khác (Bảo hành/Hủy).

2. HẠNG MỤC TÀI LIỆU & PHÂN TÍCH THIẾT KẾ:
   - Chịu trách nhiệm hoàn thiện Module 4 trong Báo cáo PTTK và Bảng Phân Hệ Excel 5 Sheet.
   - Đặc tả chi tiết Use Case UC-02 (Tạo đơn bán sỉ & Khóa giữ chỗ Reserved) và UC-03 (Quét Serial đóng kiện xuất sỉ).
   - Thiết kế và quản lý dữ liệu các bảng CSDL: `dealers`, `wholesale_orders`, `order_items`, `outbound_dispatches`, `dealer_receipts`, `customer_returns`.
   - Ràng buộc nghiệp vụ: RB-05 (Số lượng đặt >= MOQ), RB-07 (Giá sỉ theo hạng VIP/Bạc/Đồng), RB-08 (Thẩm định nợ: Dư nợ + Đơn mới - Cọc <= Hạn mức nợ), RB-09 (Khóa giữ chỗ Reserved khi duyệt đơn), RB-10 (Giải phóng giữ chỗ khi hủy đơn).

3. HẠNG MỤC WEB CLIENT (FRONTEND TV3):
   - Hoàn thiện giao diện `tv3_xuat_kho.html` và file logic `js/tv3_outbound.js`.
   - Danh sách đại lý B2B phân hạng (VIP, Bạc, Đồng), hiển thị hạn mức nợ và dư nợ.
   - Form lên đơn bán sỉ: Chọn đại lý -> Hệ thống tự động áp giá sỉ và chiết khấu; kiểm tra MOQ; kiểm tra tồn kho khả dụng thời gian thực.
   - Thẩm định tín dụng và duyệt đơn: Khi duyệt đơn, tự động chuyển số lượng sang trạng thái Giữ chỗ (Reserved) để không bị bán trùng lặp cho đơn khác.
   - Màn hình Quét Serial đóng kiện xuất kho: Thủ kho dùng camera quét Serial trên kệ; hệ thống kiểm tra Serial thuộc đúng SKU, trạng thái Trong kho và Hàng mới.
   - Lập Phiếu Thu tiền sỉ (giảm nợ, khôi phục hạn mức) và Biên bản bàn giao hàng B2B A4.

4. HẠNG MỤC LẬP TRÌNH MẠNG & API/SOCKET (NETWORK COMMUNICATION):
   - Xây dựng và kết nối các Endpoint REST API & WebSocket:
     + GET /api/dealers: Lấy danh sách đại lý, hạng và hạn mức nợ còn lại.
     + POST /api/dealers/create: Thêm mới đại lý, cấu hình Credit Limit và thời hạn nợ (Net 15/30).
     + POST /api/orders/create: Gửi đơn sỉ nháp lên server.
     + PUT /api/orders/{orderId}/approve: Thẩm định tín dụng và phê duyệt đơn:
       * Tăng số lượng giữ chỗ `reservedQty`, giảm tồn khả dụng `availableQty`.
       * Phát thông điệp mạng WebSocket: `EVENT_STOCK_RESERVED` báo cho toàn mạng biết số lượng khả dụng đã giảm.
     + PUT /api/orders/{orderId}/cancel: Hủy đơn sỉ, phát sự kiện giải phóng giữ chỗ `EVENT_STOCK_RELEASED`.
     + POST /api/outbound/dispatch: Xác nhận xuất kho thành công:
       * Giảm tồn thực tế, giải phóng giữ chỗ.
       * Cập nhật Serial sang `DA_BAN`, gán mã đại lý và ngày bảo hành.
       * Tăng dư nợ đại lý, ghi phát sinh Thẻ kho (-).
       * Phát thông điệp `EVENT_DISPATCH_COMPLETED` sang TV4 và TV5.
     + POST /api/dealers/payment-receipt: Thu tiền sỉ, giảm dư nợ đại lý.

5. HẠNG MỤC ỨNG DỤNG ANDROID STUDIO (KOTLIN MVVM):
   - Package phụ trách: `com.chronovault.wms.dealer` và `com.chronovault.wms.outbound`.
   - Xây dựng DealerListFragment, DealerDetailActivity.
   - Xây dựng CreateWholesaleOrderActivity: Chọn mẫu đồng hồ, kiểm tra MOQ, hiển thị đơn giá VIP/Bạc/Đồng tự động, hiển thị số tiền cọc bắt buộc.
   - Xây dựng DispatchOrderActivity (Đóng gói xuất sỉ): Tích hợp camera quét mã Serial từng chiếc, kiểm tra đối soát thời gian thực.
   - Màn hình lập Phiếu Thu tiền sỉ và Màn hình tiếp nhận đổi trả hàng sỉ.

6. HẠNG MỤC KIỂM THỬ:
   - Kiểm thử kịch bản vượt hạn mức tín dụng: Đơn hàng mới làm dư nợ vượt Credit Limit -> Hệ thống bắt buộc chặn và yêu cầu duyệt ngoại lệ từ Chủ cửa hàng.
   - Kiểm thử tính năng khóa giữ chỗ: Khi đơn đã duyệt nhưng chưa xuất, tồn khả dụng giảm đi và các đơn khác không thể đặt vượt số lượng còn lại."""
    add_prompt_box(doc, p3_full, "PROMPT FULL-STACK: TV3 - TÔ ĐỨC THẢO (KHÁCH SỈ & BÁN SỈ - XUẤT HÀNG)")

    # -------------------------------------------------------------
    # PROMPT 4: VÕ CÔNG TÂM (TV4)
    # -------------------------------------------------------------
    doc.add_heading("4. BẢN PROMPT TOÀN DIỆN: THÀNH VIÊN 4 - VÕ CÔNG TÂM (TỒN KHO, VỊ TRÍ KỆ & KIỂM KÊ)", level=2)
    p4_full = """BẠN LÀ LẬP TRÌNH VIÊN PHỤ TRÁCH PHÂN HỆ QUẢN LÝ TỒN KHO, VỊ TRÍ KỆ VẬT LÝ VÀ KIỂM KÊ TRONG DỰ ÁN HỆ THỐNG QUẢN LÝ KHO ĐỒNG HỒ CAO CẤP CHRONOVAULT B2B WHOLESALE WMS (MÔN LẬP TRÌNG MẠNG).
HÃY THỰC HIỆN TOÀN BỘ CÁC CÔNG VIỆC DƯỚI ĐÂY MỘT CÁCH CHUẨN XÁC, ĐỒNG BỘ VỚI NHÓM TRƯỞNG:

1. PHẠM VI NGHIỆP VỤ PHỤ TRÁCH (TV4 - VÕ CÔNG TÂM):
   - Phân Hệ 4: Theo dõi tồn kho đa đơn vị (Thùng + Chiếc), Quản lý 3 trạng thái chất lượng kho (Kho Mới, Kho Trưng Bày, Kho Lỗi), Sơ đồ ngăn kệ vật lý Bin [Khu-Dãy-Tầng-Ngăn], Tổ chức kiểm kê kho quét Serial, Đối soát chênh lệch Thừa/Thiếu, Lập phiếu cân bằng kho và Quản lý Sổ Thẻ kho điện tử (`so_the_kho`).

2. HẠNG MỤC TÀI LIỆU & PHÂN TÍCH THIẾT KẾ:
   - Chịu trách nhiệm hoàn thiện Module 5 trong Báo cáo PTTK và Bảng Phân Hệ Excel 5 Sheet.
   - Đặc tả chi tiết Use Case UC-04 (Kiểm kê kho & Cân bằng sai lệch tồn theo Serial).
   - Thiết kế và quản lý dữ liệu các bảng CSDL: `shelves`, `stock_audits`, `audit_serial_details`, `stock_cards` (Thẻ kho).
   - Ràng buộc nghiệp vụ: RB-13 (Khóa xuất nhập khu vực khi kiểm kê), RB-14 (Phân loại Serial Khớp/Thừa/Thiếu), RB-15 (Cân bằng chênh lệch > 10 triệu Chủ cửa hàng duyệt), RB-16 (Sổ Thẻ kho bất biến 100%), RB-18 (Tách bạch 3 kho chất lượng).

3. HẠNG MỤC WEB CLIENT (FRONTEND TV4):
   - Hoàn thiện giao diện `tv4_ton_kho.html` và file logic `js/tv4_warehouse.js`.
   - Bảng tồn kho tổng hợp đa đơn vị hiển thị song song số Thùng quy đổi và tổng số Chiếc lẻ khả dụng; phân tách rõ Tồn thực tế, Tồn giữ chỗ và Tồn khả dụng.
   - 3 Tab lọc trạng thái kho: Kho Hàng Mới, Kho Hàng Trưng Bày, Kho Hàng Lỗi.
   - Sơ đồ mặt bằng vị trí kệ kho vật lý trực quan: Hiển thị danh sách ngăn kệ, sức chứa tối đa và tỷ lệ lấp đầy (Capacity %); cảnh báo đỏ khi kệ đầy.
   - Chức năng Kiểm kê quét Camera: Quét thực tế dải Serial tại kệ; hệ thống tự động so khớp và tính ra danh sách Serial Khớp, Thừa, Thiếu.
   - Lập Phiếu cân bằng kho sau kiểm kê và Truy xuất Sổ Thẻ kho điện tử ghi vết lịch sử biến động (+/-).

4. HẠNG MỤC LẬP TRÌNH MẠNG & API/SOCKET (NETWORK COMMUNICATION):
   - Xây dựng và kết nối các Endpoint REST API & WebSocket:
     + GET /api/inventory/overview: Trả về số liệu tồn kho tổng hợp đa đơn vị và tổng giá trị tồn theo giá vốn đích danh.
     + GET /api/shelves: Lấy sơ đồ vị trí kệ, sức chứa và danh sách Serial đang lưu tại từng kệ.
     + PUT /api/shelves/{shelfId}/relocate: Điều chuyển Serial sang ngăn kệ mới qua mạng.
     + POST /api/audit/start: Kích hoạt đợt kiểm kê; phát broadcast WebSocket `EVENT_AUDIT_LOCKED` tạm khóa xuất nhập khu vực kiểm kê.
     + POST /api/audit/submit-scan: Gửi dải mã Serial quét thực tế lên server đối soát.
     + POST /api/audit/balance: Lập phiếu cân bằng kho, điều chỉnh số liệu tồn trong CSDL, ghi dòng phát sinh Thẻ kho bất biến và mở khóa khu vực (`EVENT_AUDIT_UNLOCKED`).
     + GET /api/stock-cards/{sku}: Truy xuất toàn bộ lịch sử biến động Sổ Thẻ kho của một mẫu đồng hồ.

5. HẠNG MỤC ỨNG DỤNG ANDROID STUDIO (KOTLIN MVVM):
   - Package phụ trách: `com.chronovault.wms.inventory` và `com.chronovault.wms.audit`.
   - Xây dựng StockOverviewFragment: 3 Tab kho chất lượng, hiển thị số Thùng + Chiếc, các badge cảnh báo tồn Min/Max.
   - Xây dựng ShelvesLayoutActivity: Trực quan hóa danh sách ngăn kệ dạng Grid với thanh Progress Bar đo tỷ lệ lấp đầy sức chứa.
   - Xây dựng StockAuditActivity: Tích hợp camera quét liên tục mã Serial tại kệ; giao diện phân màu đối soát trực quan (Xanh: Khớp đúng, Vàng: Thừa, Đỏ: Thiếu).
   - Xây dựng StockCardActivity: Màn hình xem nhật ký Sổ Thẻ kho điện tử dạng Timeline.

6. HẠNG MỤC KIỂM THỬ:
   - Kiểm thử kịch bản đồng thời (Concurrency): Giả lập 2 client cùng thao tác xuất nhập đồng thời để kiểm tra tính toàn vẹn dữ liệu, đảm bảo không bị xuất âm kho.
   - Kiểm thử tính bất biến của Sổ Thẻ kho: Đảm bảo không có bất kỳ lệnh UPDATE/DELETE nào tác động lên bảng `stock_cards`."""
    add_prompt_box(doc, p4_full, "PROMPT FULL-STACK: TV4 - VÕ CÔNG TÂM (TỒN KHO, VỊ TRÍ KỆ & KIỂM KÊ)")

    # -------------------------------------------------------------
    # PROMPT 5: TRẦN CÔNG TÚ (TV5)
    # -------------------------------------------------------------
    doc.add_heading("5. BẢN PROMPT TOÀN DIỆN: THÀNH VIÊN 5 - TRẦN CÔNG TÚ (DASHBOARD & BÁO CÁO THỐNG KÊ)", level=2)
    p5_full = """BẠN LÀ LẬP TRÌNH VIÊN PHỤ TRÁCH PHÂN HỆ BÁO CÁO THỐNG KÊ & DASHBOARD ĐIỀU HÀNH TRONG DỰ ÁN HỆ THỐNG QUẢN LÝ KHO ĐỒNG HỒ CAO CẤP CHRONOVAULT B2B WHOLESALE WMS (MÔN LẬP TRÌNH MẠNG).
HÃY THỰC HIỆN TOÀN BỘ CÁC CÔNG VIỆC DƯỚI ĐÂY MỘT CÁCH CHUẨN XÁC, ĐỒNG BỘ VỚI NHÓM TRƯỞNG:

1. PHẠM VI NGHIỆP VỤ PHỤ TRÁCH (TV5 - TRẦN CÔNG TÚ):
   - Phân Hệ 5: Executive Dashboard trung tâm điều hành thời gian thực, Biểu đồ trực quan doanh thu và chi phí 6 tháng, Bảng xếp hạng Top sản phẩm bán chạy, Hệ thống 9 báo cáo chuyên sâu đa phân hệ, Sổ chi tiết công nợ B2B 2 chiều (Đại lý & NCC) và Báo cáo Dòng tiền thuần (Cashflow).

2. HẠNG MỤC TÀI LIỆU & PHÂN TÍCH THIẾT KẾ:
   - Chịu trách nhiệm hoàn thiện Module 6 trong Báo cáo PTTK và Bảng Phân Hệ Excel 5 Sheet.
   - Đặc tả chi tiết 9 mẫu báo cáo kỹ thuật, công thức tính toán Lợi nhuận gộp B2B (Doanh thu - Giá vốn đích danh - Chi phí logistics).
   - Thiết kế cấu trúc bảng đối soát công nợ 2 chiều (Dư đầu kỳ, Phát sinh nợ, Phát sinh có, Dư cuối kỳ) và công thức dòng tiền thuần (Net Cashflow = Tiền thu vào - Tiền chi ra).

3. HẠNG MỤC WEB CLIENT (FRONTEND TV5):
   - Hoàn thiện giao diện `tv5_bao_cao.html` và file logic `js/tv5_reports.js`.
   - Màn hình Executive Dashboard với 5 thẻ KPI thời gian thực: Tổng giá trị tài sản tồn kho theo giá vốn đích danh, Doanh thu phân phối sỉ, Số đơn hàng sỉ mới, Tồn khả dụng và Tỷ lệ đổi trả hàng sỉ (< 2.0%).
   - Tích hợp HTML5 Canvas vẽ biểu đồ doanh số 6 tháng gần nhất và biểu đồ cơ cấu chi phí nhập hàng.
   - Bảng xếp hạng Top mẫu đồng hồ bán chạy nhất kênh sỉ.
   - Hệ thống 9 báo cáo chuyên sâu với bộ lọc thời gian và tính năng xuất file CSV/Excel hoặc in PDF A4.
   - Modal Sổ chi tiết công nợ 2 chiều và Báo cáo Dòng tiền thu/chi thực tế.

4. HẠNG MỤC LẬP TRÌNH MẠNG & API/SOCKET (NETWORK COMMUNICATION):
   - Xây dựng và kết nối các Endpoint REST API & WebSocket tổng hợp:
     + GET /api/dashboard/kpi: Tổng hợp số liệu từ các phân hệ trả về 5 chỉ số KPI điều hành.
     + GET /api/dashboard/sales-chart: Lấy dữ liệu doanh số và chi phí theo từng tháng phục vụ vẽ biểu đồ.
     + GET /api/reports/inbound: Báo cáo nhập hàng theo NCC và chi phí phân bổ.
     + GET /api/reports/outbound: Báo cáo xuất sỉ theo đại lý và cấp bậc.
     + GET /api/reports/dead-stock: Báo cáo hàng tồn lâu ngày chậm luân chuyển (> 90 ngày).
     + GET /api/reports/gross-profit: Báo cáo lợi nhuận gộp B2B chi tiết theo từng dòng sản phẩm.
     + GET /api/reports/debt-ledger: Bảng đối soát chi tiết công nợ 2 chiều (Đại lý & NCC).
     + GET /api/reports/cashflow: Báo cáo dòng tiền thực tế thu/chi theo mốc thời gian.
     + Lắng nghe WebSocket: Khi TV2 duyệt nhập kho, TV3 xuất sỉ hoặc thu/chi tiền, Server phát tín hiệu để màn hình Dashboard tự động nhảy số thời gian thực mà không cần F5 trình duyệt.

5. HẠNG MỤC ỨNG DỤNG ANDROID STUDIO (KOTLIN MVVM):
   - Package phụ trách: `com.chronovault.wms.dashboard` và `com.chronovault.wms.reports`.
   - Xây dựng DashboardFragment sang trọng với 5 thẻ KPI Cards (nền đen Onyx, viền vàng Gold).
   - Tích hợp thư viện `MPAndroidChart` (BarChart, LineChart, PieChart) vẽ biểu đồ doanh số và cơ cấu chi phí.
   - Xây dựng ReportViewerActivity: Hiển thị 9 loại báo cáo dạng bảng biểu phân trang mượt mà.
   - Tính năng xuất báo cáo ra file CSV lưu vào thư mục Downloads của điện thoại và tính năng In ấn báo cáo chuẩn A4 qua Android PrintManager.

6. HẠNG MỤC KIỂM THỬ:
   - Đối soát tính toán số liệu tài chính: Kiểm tra đảm bảo Tổng doanh thu, Tổng giá trị tồn kho, Công nợ và Dòng tiền hiển thị trên Dashboard khớp đúng 100% với dữ liệu giao dịch thực tế từ 4 phân hệ kia."""
    add_prompt_box(doc, p5_full, "PROMPT FULL-STACK: TV5 - TRẦN CÔNG TÚ (DASHBOARD & BÁO CÁO THỐNG KÊ)")

    # =========================================================================
    # PHẦN IV: QUY TRÌNH PHỐI HỢP NHÓM & TIẾN ĐỘ THỰC HIỆN
    # =========================================================================
    h4 = doc.add_heading("IV. TIẾN ĐỘ THỰC HIỆN VÀ QUY TRÌNH PHỐI HỢP GIT WORKFLOW", level=1)
    h4.paragraph_format.space_before = Pt(14); h4.paragraph_format.space_after = Pt(6)
    for r in h4.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "1. Lộ trình 4 giai đoạn hoàn thành đồ án:",
            "   • Giai đoạn 1 (Tuần 1): Hoàn thiện Tài liệu PTTK, CSDL 23 bảng 3NF, Bảng phân hệ Excel và chốt Master Data Contract.",
            "   • Giai đoạn 2 (Tuần 2): Hoàn thiện toàn bộ Web Client (HTML/CSS/JS) và Server Backend REST API/Socket trung tâm.",
            "   • Giai đoạn 3 (Tuần 3): Phát triển ứng dụng Android Studio (Kotlin MVVM) cho 5 phân hệ theo đúng bộ Prompt trên.",
            "   • Giai đoạn 4 (Tuần 4): Kiểm thử tích hợp chéo liên phân hệ, sửa lỗi (bug fixing), đóng gói báo cáo và thuyết trình.",
            "",
            "2. Quy định phân nhánh Git trên repository `LapTrinhMang_5AESiuNhan`:",
            "   • Nhánh `main`: Nhánh ổn định cao nhất, chỉ Nhóm trưởng (Phan Bá Hải Bình) mới có quyền merge code.",
            "   • Mỗi thành viên làm việc trên nhánh riêng mang tên phân hệ của mình:",
            "     - Phan Bá Hải Bình: git checkout -b feature/tv1-core-product",
            "     - Nguyễn Đắc Quân: git checkout -b feature/tv2-inbound-supplier",
            "     - Tô Đức Thảo: git checkout -b feature/tv3-outbound-dealer",
            "     - Võ Công Tâm: git checkout -b feature/tv4-inventory-audit",
            "     - Trần Công Tú: git checkout -b feature/tv5-dashboard-reports",
            "   • Khi hoàn thành: Tạo Pull Request (PR) mô tả rõ các chức năng đã làm để Nhóm trưởng review trước khi merge."
        ],
        title="KẾ HOẠCH TIẾN ĐỘ VÀ QUY CHUẨN LÀM VIỆC NHÓM",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # Save to disk
    output_filename = "KE_HOACH_CHI_TIET_VA_BO_PROMPT_TOAN_DIEN_5_THANH_VIEN.docx"
    output_path = os.path.join(r"D:\cntt\pbhb", output_filename)
    doc.save(output_path)
    
    # Also save to Document folder
    doc_path = os.path.join(r"D:\cntt\pbhb\Document", output_filename)
    doc.save(doc_path)
    print(f"SUCCESS: Created document at {output_path} and {doc_path}")

if __name__ == "__main__":
    build_full_project_guide()

