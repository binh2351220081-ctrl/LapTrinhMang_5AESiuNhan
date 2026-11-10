# -*- coding: utf-8 -*-
"""
Script: tools/generate_report_binh_docx.py
Mục đích: Điền toàn bộ dữ liệu phần việc của Phan Bá Hải Bình (TV1 - Trưởng nhóm & Quản trị Danh mục Luxury)
vào đúng mẫu chuẩn của Khoa CNTT - ĐH Kiến trúc Đà Nẵng (Document/Mẫu báo cáo.docx)
và xuất ra file Word: Document/BAO_CAO_PHAN_TICH_HE_THONG_THONG_TIN_CHRONOVAULT_WMS.docx
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_report_for_binh():
    template_path = r"D:\cntt\pbhb\Document\Mẫu báo cáo.docx"
    output_path = r"D:\cntt\pbhb\Document\BAO_CAO_PHAN_TICH_HE_THONG_THONG_TIN_CHRONOVAULT_WMS.docx"
    
    doc = Document(template_path)
    
    # Colors
    C_NAVY = RGBColor(27, 54, 93)      # #1B365D
    C_GOLD = RGBColor(197, 155, 39)    # #C59B27
    C_SLATE = RGBColor(51, 65, 85)     # #334155
    C_GRAY = RGBColor(100, 116, 139)   # #64748B
    
    def set_cell_background(cell, hex_color):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def set_cell_margins(cell, top=70, bottom=70, left=80, right=80):
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

    # -------------------------------------------------------------
    # 1. CẬP NHẬT TRANG BÌA (Cover page paragraphs)
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        txt = p.text
        if "ĐỀ TÀI:" in txt:
            p.text = "ĐỀ TÀI: HỆ THỐNG QUẢN LÝ KHO & PHÂN PHỐI BÁN SỈ ĐỒNG HỒ CAO CẤP B2B (CHRONOVAULT WMS)"
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
            p.text = "Thành viên phụ trách báo cáo\t: Phan Bá Hải Bình (Nhóm trưởng / System Architect)"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.italic = True
        elif "Khóa\t: 2023" in txt:
            p.text = "Các thành viên phân hệ con\t: Nguyễn Đắc Quân (TV2), Tô Đức Thảo (TV3), Võ Công Tâm (TV4), Trần Công Tú (TV5)\nKhóa\t\t\t\t: 2023 - 2026"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10)

    # -------------------------------------------------------------
    # 2. CẬP NHẬT MỤC 1: ĐẶT TÊN ĐỀ TÀI & BẢNG SO SÁNH
    # -------------------------------------------------------------
    for i, p in enumerate(doc.paragraphs):
        if "Tên ứng dụng (đề xuất):" in p.text:
            p.text = "Tên ứng dụng: Hệ Thống Quản Lý Kho & Phân Phối Bán Sỉ Đồng Hồ Cao Cấp B2B (ChronoVault WMS)"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "Bao gồm 3 thành phần:" in p.text:
            p.text = (
                "Phân tích 3 thành phần cấu thành tên đề tài theo chuẩn khoa học:\n"
                "• Loại hình / Hành động: Hệ thống Quản trị Kho vận đa cấp & Điều phối Chuỗi cung ứng B2B (Warehouse Management System - WMS).\n"
                "• Chức năng chính: Quản lý định danh Serial Number 100%, Tự động quy đổi Đơn vị tính (ĐVT) đa cấp (Thùng - Chiếc lẻ), Kiểm soát hạn mức công nợ & khóa giữ chỗ, Hạch toán giá vốn đích danh (Specific Identification Costing).\n"
                "• Đối tượng / Lĩnh vực: Ngành phân phối đồng hồ cao cấp xa xỉ (Luxury Horology Wholesale Distribution)."
            )
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10); r.font.color.rgb = C_SLATE
        elif "Đưa ra bảng so sánh khoảng 3-5 phần mềm" in p.text:
            p.text = (
                "Bảng 1.1: So sánh đối chiếu phần mềm ChronoVault WMS với các giải pháp quản lý kho trên thị trường\n"
                "(Minh chứng tính cấp thiết và giải quyết bài toán đặc thù của ngành phân phối đồng hồ xa xỉ):"
            )
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "4.1. Cấu trúc phân rã chức năng" in p.text:
            pass
        elif "Phân hệ" == p.text.strip():
            p.text = (
                "MOD-01: Phân hệ Quản trị Hệ thống & Danh mục Luxury Horology (Phan Bá Hải Bình)\n"
                "├── F1.1: Quản trị Xác thực & Kiểm soát Phân quyền Người dùng (RBAC)\n"
                "│    ├── F1.1.1: Đăng nhập bảo mật & Khởi tạo phiên làm việc (SessionManager)\n"
                "│    ├── F1.1.2: Phân quyền theo 5 vai trò hệ thống (SYSTEM_ADMIN, STORE_OWNER, WAREHOUSE_MANAGER, OPERATIONS_STAFF, ACCOUNTANT)\n"
                "│    └── F1.1.3: Quản lý danh sách tài khoản & Khóa/Mở khóa nhân viên vi phạm\n"
                "└── F1.2: Quản lý Danh mục Đồng hồ Cao cấp (Luxury Horology Master Data)\n"
                "     ├── F1.2.1: Quản lý Thông số Kỹ thuật Chuyên ngành (SKU, Brand, Bộ máy, Kính Sapphire, Vỏ, Kháng nước)\n"
                "     ├── F1.2.2: Thiết lập Đơn vị tính Đa cấp (Thùng - Chiếc) & Tỷ lệ Quy đổi conversionRate\n"
                "     └── F1.2.3: Thiết lập Ngưỡng cảnh báo Tồn kho An toàn (Min / Max Stock Alert)"
            )
            for r in p.runs:
                r.font.name = "Consolas"; r.font.size = Pt(9.5); r.font.color.rgb = C_NAVY
        elif "└── Chức năng" in p.text or "└── Chức năng cấp 1" in p.text or "└── Chức năng cấp n (Module)" in p.text:
            p.text = "" # Xóa các dòng template cũ
        elif "Mã Module: [MOD-XX-YY]" in p.text:
            p.text = (
                "Mã Module: MOD-01-02\n"
                "Tên Module: Khai báo Danh mục Sản phẩm Đồng hồ Cao cấp & Thiết lập Tỷ lệ Quy đổi ĐVT\n"
                "Thuộc phân hệ: MOD-01 (Quản trị Hệ thống & Danh mục Luxury Horology)\n"
                "Mức độ ưu tiên: Cao (Bắt buộc hoàn thành)"
            )
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "Bảng: [tên_bảng]" in p.text:
            p.text = "Bảng: products (Danh mục Sản phẩm Đồng hồ Cao cấp & Cấu hình ĐVT Quy đổi)"
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = C_NAVY
        elif "[Bảng A] 1 ──── N [Bảng B]" in p.text:
            p.text = (
                "Sơ đồ Mối quan hệ Cơ sở dữ liệu Cốt lõi (Core ERD Relationships do Phan Bá Hải Bình thiết kế):\n"
                "• [brands] 1 ──────────── N [products] (Một hãng có nhiều mẫu đồng hồ)\n"
                "• [products] 1 ────────── N [serials] (Một mẫu đồng hồ có nhiều mã Serial định danh đích danh 100%)\n"
                "• [units_of_measure] 1 ── N [products] (Quy định ĐVT Thùng / Chiếc và tỷ lệ quy đổi)\n"
                "• [roles] 1 ───────────── N [users] (Một vai trò RBAC gán cho nhiều tài khoản người dùng)\n"
                "• [users] 1 ───────────── N [system_audit_logs] (Một người dùng ghi nhận nhiều nhật ký kiểm toán)"
            )
            for r in p.runs:
                r.font.name = "Consolas"; r.font.size = Pt(9.5); r.font.color.rgb = C_NAVY
        elif "[Bảng A] N ──── M [Bảng C]" in p.text or "[Bảng B] 1 ──── 1 [Bảng D]" in p.text:
            p.text = ""

    # -------------------------------------------------------------
    # 3. ĐIỀN DỮ LIỆU CÁC BẢNG (TABLES 1 ĐẾN 11)
    # -------------------------------------------------------------
    
    # TABLE 1: ĐẶC TẢ YÊU CẦU CHỨC NĂNG (Mục 2)
    # Format header
    t1 = doc.tables[0]
    format_row(t1.rows[0], "1B365D", is_header=True)
    # Xóa các dòng template cũ (trừ header)
    while len(t1.rows) > 1:
        tr = t1.rows[-1]._tr
        tr.getparent().remove(tr)
    
    t1_data = [
        ("FR-01", "Đăng nhập & Xác thực bảo mật", "Xác thực danh tính người dùng bằng Email/Username và mật khẩu mã hóa (BCrypt/SHA-256). Cấp quyền phiên làm việc lưu trong SessionManager. Tự động đăng xuất khi hết hạn.", "Cao", "System Admin / Store Owner"),
        ("FR-02", "Kiểm soát Phân quyền RBAC", "Kiểm soát truy cập dựa trên 5 vai trò hệ thống: SYSTEM_ADMIN (Quản trị hệ thống), STORE_OWNER (Chủ cửa hàng), WAREHOUSE_MANAGER (Thủ kho), OPERATIONS_STAFF (Nhân viên nhập - xuất kho), ACCOUNTANT (Kế toán kho). Ngăn chặn người dùng trái phép can thiệp chức năng ngoài quyền hạn.", "Cao", "System Admin"),
        ("FR-03", "Quản lý Danh mục Đồng hồ Cao cấp", "Khai báo và quản lý hồ sơ Master Data từng mẫu đồng hồ xa xỉ: Mã SKU duy nhất, Tên mẫu, Hãng (Rolex, Omega, Patek...), Bộ sưu tập, Loại máy (Automatic, Quartz, Solar), Chất liệu vỏ (Vàng 18K, Thép, Titanium), Mặt kính Sapphire, Độ chống nước, Upload ảnh sản phẩm.", "Cao", "Store Owner / System Admin"),
        ("FR-04", "Quản lý ĐVT Đa cấp & Tỷ lệ Quy đổi", "Thiết lập cấu trúc Đơn vị tính 2 cấp bắt buộc: ĐVT Cơ sở ('Chiếc') và ĐVT Đóng gói ('Thùng' hoặc 'Hộp'). Lưu trữ tỷ lệ quy đổi conversionRate (1 Thùng = N Chiếc) làm căn cứ tự động cho phân hệ Nhập kho (TV2) và Xuất kho (TV3).", "Cao", "Warehouse Manager"),
        ("FR-05", "Định mức Tồn kho & Cảnh báo an toàn", "Thiết lập mức tồn kho tối thiểu (minStockAlert) và tối đa (maxStockAlert) cho từng mẫu đồng hồ. Hiển thị cảnh báo trực quan màu vàng/đỏ khi tồn khả dụng chạm ngưỡng an toàn.", "Trung bình", "Store Owner / Quản lý kho"),
        ("FR-06 -> FR-20", "[Các phân hệ của TV2, TV3, TV4, TV5]", "Bao gồm các yêu cầu chức năng về Nhập kho NCC (TV2), Phân phối Bán sỉ & Khóa giữ chỗ (TV3), Ma trận Kệ Bin & Kiểm kê (TV4), Executive Dashboard & 9 Báo cáo (TV5) do các thành viên tương ứng hoàn thiện.", "Cao", "Nhóm 5 AE Siêu Nhân")
    ]
    for row_idx, item in enumerate(t1_data):
        row = t1.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 2: DANH SÁCH ĐỐI TƯỢNG (ENTITIES - Mục 3.1)
    t2 = doc.tables[1]
    format_row(t2.rows[0], "1B365D", is_header=True)
    while len(t2.rows) > 1:
        tr = t2.rows[-1]._tr
        tr.getparent().remove(tr)
        
    t2_data = [
        ("ENT-01", "User (Người dùng)", "Quản lý thông tin tài khoản nhân viên và lãnh đạo trong hệ thống WMS.", "id, username, password_hash, full_name, email, role, is_active, created_at", "Thuộc 1 Role (1-1); Tạo nhiều Giao dịch (1-N)"),
        ("ENT-02", "Role (Vai trò)", "Quản lý 5 nhóm quyền hạn truy cập nghiệp vụ trong hệ thống.", "role_code, role_name, description, permissions_json", "Gán cho nhiều User (1-N)"),
        ("ENT-03", "Product (Sản phẩm Đồng hồ)", "Lưu trữ Master Data mẫu đồng hồ cao cấp chuẩn Luxury Horology.", "sku, name, brand, collection, movement_type, case_material, wholesale_price, conversion_rate, min_stock, max_stock", "Chứa nhiều Serial định danh (1-N); Thuộc 1 Brand (N-1)"),
        ("ENT-04", "Brand (Thương hiệu)", "Danh bạ các hãng đồng hồ xa xỉ chính hãng (Thụy Sỹ, Nhật, Đức).", "brand_id, brand_name, origin_country, website", "Chứa nhiều Product (1-N)"),
        ("ENT-05", "UnitOfMeasure (Đơn vị tính)", "Định nghĩa quy cách đóng gói đa cấp (Chiếc, Thùng, Hộp).", "uom_id, uom_name, uom_type, conversion_factor", "Áp dụng cho nhiều Product (1-N)"),
        ("ENT-06..ENT-15", "[Entities TV2 - TV5]", "Supplier, InboundReceipt, Dealer, OutboundOrder, Serial, BinLocation, AuditRecord, ReportData...", "[Do TV2, TV3, TV4, TV5 phụ trách]", "[Kết nối qua Room DB chung]")
    ]
    for row_idx, item in enumerate(t2_data):
        row = t2.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 3: PHÂN HỆ (NHÓM CHỨC NĂNG - Mục 3.2)
    t3 = doc.tables[2]
    format_row(t3.rows[0], "1B365D", is_header=True)
    while len(t3.rows) > 1:
        tr = t3.rows[-1]._tr
        tr.getparent().remove(tr)

    t3_data = [
        ("MOD-01", "Quản trị Hệ thống & Danh mục Luxury Horology\n(Phan Bá Hải Bình phụ trách)", "Quản lý bảo mật, xác thực người dùng, phân quyền RBAC 5 Roles, danh mục thông số đồng hồ xa xỉ, thiết lập ĐVT 2 cấp và cấu trúc CSDL Room Core.", "User, Role, Product, Brand, UnitOfMeasure", "Đăng nhập, Quản lý tài khoản, Phân quyền RBAC, Quản lý mẫu đồng hồ (SKU), Thiết lập tỷ lệ quy đổi ĐVT, Cảnh báo tồn kho an toàn."),
        ("MOD-02", "Quản lý Đối tác NCC & Nhập kho Quy đổi ĐVT\n(Nguyễn Đắc Quân phụ trách)", "Quản lý hồ sơ NCC, nhập kho quy đổi Thùng ra Chiếc, quét camera Serial, phân bổ chi phí & tính giá vốn đích danh, xuất trả hàng lỗi NCC.", "Supplier, InboundReceipt, SerialEntity, PaymentVoucher", "Quản lý NCC, Lập phiếu nhập kho, Quét Serial camera ML Kit, Phân bổ chi phí, Tính giá vốn đích danh, Lập phiếu chi nợ NCC."),
        ("MOD-03", "Quản lý Đại lý B2B & Phân phối Xuất kho\n(Tô Đức Thảo phụ trách)", "Quản lý hồ sơ đại lý sỉ, hạn mức nợ, chiết khấu hạng đại lý, đơn đặt hàng sỉ, cơ chế khóa giữ chỗ kho và quét camera Serial xuất kho.", "Dealer, OutboundOrder, ReservationEngine, ReceiptVoucher", "Quản lý đại lý, Kiểm soát hạn mức nợ, Tạo đơn sỉ, Khóa giữ chỗ tồn kho, Quét Serial xuất đóng thùng, Lập phiếu thu nợ đại lý."),
        ("MOD-04", "Quản trị Tồn kho Nội bộ & Kiểm kê Kệ hàng\n(Võ Công Tâm phụ trách)", "Phân loại tồn kho 3 cấp chất lượng, trực quan hóa sơ đồ ma trận kệ tủ chống trộm K1/K2, quy trình kiểm kê đối soát tự động, Sổ Thẻ kho điện tử.", "SerialQuality, BinMatrix, StockAudit, StockCardLedger", "Phân loại 3 chất lượng hàng, Tra cứu ma trận ô kệ Bin K1/K2, Quét mã điều chuyển kệ, Kiểm kê đối soát Thừa/Thiếu, Tra cứu Sổ thẻ kho."),
        ("MOD-05", "Executive Dashboard & Hệ thống 9 Báo cáo\n(Trần Công Tú phụ trách)", "Bảng chỉ số KPI điều hành thời gian thực, biểu đồ doanh thu 6 tháng MPAndroidChart, 9 báo cáo chuyên sâu và báo cáo dòng tiền thuần Cashflow.", "DashboardKPI, ChartEngine, ReportContainer, CashflowData", "Executive Dashboard 5 thẻ KPI, Biểu đồ doanh thu 6 tháng, Biểu đồ chi phí, Top 10 sản phẩm bán chạy, 9 báo cáo chuyên sâu đa phân hệ, Xuất CSV/In ấn A4.")
    ]
    for row_idx, item in enumerate(t3_data):
        row = t3.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if row_idx == 0:
            row.cells[0].paragraphs[0].runs[0].font.bold = True

    # TABLE 4: MÔ TẢ MODULE IPO (Mục 4.2 - Phần việc của Bình)
    t4 = doc.tables[3]
    format_row(t4.rows[0], "1B365D", is_header=True)
    
    t4_data = [
        ("Input", "• Dữ liệu đầu vào: Mã SKU đồng hồ, Tên mẫu mã, Thương hiệu, Bộ sưu tập, Loại máy (Automatic/Quartz/Solar), Chất liệu vỏ (Vàng 18K/Thép/Titanium), Đường kính mặt (mm), Độ kháng nước (ATM), Giá bán sỉ niêm yết (VNĐ), ĐVT Cơ sở ('Chiếc'), ĐVT Đóng gói ('Thùng'), Hệ số quy đổi (Ví dụ: 10 chiếc/thùng), Ngưỡng tồn an toàn (Min/Max).\n• Nguồn dữ liệu: Form nhập liệu AddEditProductActivity hoặc file Excel Master Data nhập khẩu ban đầu.\n• Điều kiện tiên quyết: Người dùng đã đăng nhập với vai trò SYSTEM_ADMIN hoặc STORE_OWNER."),
        ("Process", "• Bước 1: Hệ thống kiểm tra tính hợp lệ dữ liệu (Mã SKU không được để trống, không được chứa ký tự đặc biệt, Giá sỉ > 0, Hệ số quy đổi >= 1).\n• Bước 2: Truy vấn cơ sở dữ liệu Room Database để kiểm tra tính duy nhất của Mã SKU (chặn trùng lặp SKU tuyệt đối).\n• Bước 3: Tải ảnh đại diện mẫu đồng hồ, nén kích thước và lưu trữ đường dẫn ảnh cục bộ.\n• Bước 4: Tạo đối tượng ProductEntity và gọi hàm `productDao.insertProduct(product)`.\n• Bước 5: Ghi nhận nhật ký kiểm toán hệ thống (Audit Log): 'Người dùng [username] đã khởi tạo mẫu đồng hồ [SKU]'."),
        ("Output", "• Bản ghi sản phẩm mới được lưu thành công vào bảng `products` của Room Database.\n• Giao diện hiển thị SnackBar / Toast thông báo: 'Đã lưu mẫu đồng hồ [SKU] thành công'.\n• Danh mục sản phẩm tại ProductListFragment tự động cập nhật hiển thị mẫu đồng hồ mới qua Flow / LiveData."),
        ("Actor", "Chủ cửa hàng (STORE_OWNER) và Quản trị viên hệ thống (SYSTEM_ADMIN)."),
        ("Quyền hạn", "Quyền Quản trị viên và Chủ cửa hàng (Các vai trò khác chỉ có quyền Xem - Read Only)."),
        ("Luồng dữ liệu liên quan", "Ghi vào bảng `products`, ghi vào bảng `audit_logs`, cập nhật StateFlow của ProductViewModel."),
        ("Ghi chú / Ràng buộc", "Mã SKU bắt buộc viết hoa; Hệ số quy đổi phải là số nguyên dương; Khi đã phát sinh phiếu nhập/xuất thì không được phép thay đổi tỷ lệ quy đổi ĐVT.")
    ]
    for row_idx, item in enumerate(t4_data):
        row = t4.rows[row_idx + 1]
        row.cells[0].text = item[0]
        row.cells[1].text = item[1]
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    # TABLE 5: MA TRẬN CRUD (Mục 5.1 - Phần việc của Bình)
    t5 = doc.tables[4]
    format_row(t5.rows[0], "1B365D", is_header=True)
    while len(t5.rows) > 1:
        tr = t5.rows[-1]._tr
        tr.getparent().remove(tr)

    t5_data = [
        ("User (Tài khoản)", "Admin", "Admin, Owner, Cá nhân", "Admin (đổi role/khóa), Cá nhân (đổi pass)", "Admin (Khóa tài khoản / Soft Delete)", "Không xóa cứng để bảo toàn lịch sử giao dịch"),
        ("Role (Vai trò RBAC)", "Hệ thống (Seed data)", "Tất cả các Actor", "Admin (cập nhật mô tả quyền)", "Cấm xóa hoàn toàn", "5 vai trò cố định: Admin, Owner, Manager, Staff, Accountant"),
        ("Product (Mẫu đồng hồ)", "Admin, Owner", "Tất cả các Actor", "Admin, Owner, Quản lý kho", "Admin, Owner (Ẩn kinh doanh)", "Chỉ được ẩn/ngừng kinh doanh khi đã có giao dịch"),
        ("Brand (Hãng sản xuất)", "Admin, Owner", "Tất cả các Actor", "Admin, Owner", "Admin (khi chưa có sản phẩm)", "Rolex, Patek Philippe, Omega, Cartier, Hublot..."),
        ("UnitOfMeasure (ĐVT)", "Admin, Quản lý kho", "Tất cả các Actor", "Admin, Quản lý kho", "Cấm xóa khi đã có SKU liên kết", "Bắt buộc có ĐVT Cơ sở ('Chiếc') và ĐVT Đóng gói ('Thùng')"),
        ("[Entities TV2 - TV5]", "[Do Quân, Thảo, Tâm, Tú điền cho các đối tượng Inbound, Outbound, Serial, Audit, Report]", "", "", "", "")
    ]
    for row_idx, item in enumerate(t5_data):
        row = t5.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        for col in [1, 2, 3, 4]:
            row.cells[col].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 6: MÔ TẢ LUỒNG DỮ LIỆU CHÍNH (Mục 5.2 - Phần việc của Bình)
    t6 = doc.tables[5]
    format_row(t6.rows[0], "1B365D", is_header=True)
    while len(t6.rows) > 1:
        tr = t6.rows[-1]._tr
        tr.getparent().remove(tr)

    t6_data = [
        ("DF-01", "Xác thực Đăng nhập & Cấp quyền phiên", "Người dùng", "LoginActivity -> SessionManager", "Username, Password băm", "Tài khoản ở trạng thái Hoạt động (is_active = true)"),
        ("DF-02", "Khai báo Mẫu đồng hồ & Cấu hình ĐVT", "Owner / Admin", "AddEditProductActivity -> Room DB", "Thông số SKU, ĐVT, Tỷ lệ quy đổi, Min/Max stock", "Mã SKU duy nhất chưa tồn tại trong hệ thống"),
        ("DF-03", "Cập nhật Phân quyền Nhân viên nội bộ", "Admin", "UserManagementFragment -> UserDao", "User ID, Vai trò mới (UserRole enum)", "Chỉ SYSTEM_ADMIN được thực hiện"),
        ("DF-04 -> DF-10", "[Các luồng Nhập kho, Xuất sỉ, Kiểm kê, Báo cáo]", "[TV2 - TV5]", "[Inbound / Outbound / Inventory / Dashboard]", "[Do các thành viên tương ứng hoàn thiện]", "")
    ]
    for row_idx, item in enumerate(t6_data):
        row = t6.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 7: DANH SÁCH BẢNG (Mục 6.1 - CSDL do Bình thiết kế)
    t7 = doc.tables[6]
    format_row(t7.rows[0], "1B365D", is_header=True)
    while len(t7.rows) > 1:
        tr = t7.rows[-1]._tr
        tr.getparent().remove(tr)

    t7_data = [
        ("users", "Lưu trữ thông tin tài khoản người dùng và thông tin phân quyền truy cập.", "id (INT, AutoIncrement)", "role (ENUM)", "Băm mật khẩu trước khi lưu trữ"),
        ("products", "Lưu trữ Master Data danh mục các mẫu đồng hồ cao cấp và cấu hình quy đổi ĐVT.", "sku (VARCHAR, PK)", "brand_id (FK)", "Bảng trung tâm liên kết với toàn bộ hệ thống"),
        ("brands", "Danh bạ thương hiệu đồng hồ xa xỉ chính hãng.", "brand_id (INT, PK)", "Không", "Rolex, Patek, Omega, Cartier, AP, Hublot..."),
        ("units_of_measure", "Định nghĩa các đơn vị tính và hệ số quy đổi.", "uom_id (INT, PK)", "Không", "Quy đổi chuẩn 1 Thùng = N Chiếc lẻ"),
        ("system_audit_logs", "Lưu vết toàn bộ thao tác thêm, sửa, xóa, duyệt chứng từ trong toàn hệ thống.", "log_id (INT, PK)", "user_id (FK)", "Dữ liệu chỉ ghi, tuyệt đối không được sửa xóa"),
        ("[Bảng TV2 - TV5]", "suppliers, inbound_receipts, dealers, outbound_orders, serials, bin_locations, audits...", "[PK do TV tương ứng thiết kế]", "[FK kết nối]", "[Kết nối toàn vẹn trong Room DB v4]")
    ]
    for row_idx, item in enumerate(t7_data):
        row = t7.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    # TABLE 8: CHI TIẾT THUỘC TÍNH BẢNG (Mục 6.2 - Chi tiết bảng 'products' do Bình thiết kế)
    t8 = doc.tables[7]
    format_row(t8.rows[0], "1B365D", is_header=True)
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
        ("wholesale_price", "DOUBLE", "No", "0.0", "Đơn giá bán sỉ niêm yết (VNĐ)", "wholesale_price >= 0"),
        ("base_unit", "VARCHAR(20)", "No", "'Chiếc'", "Đơn vị tính cơ sở nhỏ nhất", "Mặc định là 'Chiếc'"),
        ("pack_unit", "VARCHAR(20)", "No", "'Thùng'", "Đơn vị tính đóng gói bán sỉ", "Mặc định là 'Thùng' hoặc 'Hộp'"),
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
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 9: PHÂN CÔNG VAI TRÒ TRONG NHÓM (Mục 7.1 - Vai trò Leader)
    t9 = doc.tables[8]
    format_row(t9.rows[0], "1B365D", is_header=True)
    while len(t9.rows) > 1:
        tr = t9.rows[-1]._tr
        tr.getparent().remove(tr)

    t9_data = [
        ("1", "Trưởng nhóm / Quản trị hệ thống\n(SYSTEM_ADMIN)", "Điều phối toàn bộ dự án, thiết kế kiến trúc MVVM Core, thiết kế Room Database v4 cốt lõi, quản trị Git Repository, phát triển Module Quản trị Hệ thống & Danh mục Đồng hồ Luxury Horology, tổng hợp báo cáo chung.", "Phan Bá Hải Bình (TV1)"),
        ("2", "Nhân viên Nhập kho\n(OPERATIONS_STAFF)", "Phát triển phân hệ Quản lý Nhà cung cấp, công nợ phải trả, lập phiếu nhập kho quy đổi ĐVT, tích hợp Camera quét mã Serial và thuật toán tính giá vốn đích danh.", "Nguyễn Đắc Quân (TV2)"),
        ("3", "Nhân viên Xuất kho\n(OPERATIONS_STAFF)", "Phát triển phân hệ Quản lý Đại lý sỉ B2B, kiểm soát hạn mức nợ tự động, cơ chế khóa giữ chỗ tồn kho (Reservation), quy trình xuất kho 2 bước và in hóa đơn B2B.", "Tô Đức Thảo (TV3)"),
        ("4", "Thủ kho\n(WAREHOUSE_MANAGER)", "Phát triển phân hệ Phân loại tồn kho 3 trạng thái chất lượng, trực quan hóa sơ đồ ma trận kệ tủ chống trộm K1/K2, quy trình kiểm kê đối soát tự động và Sổ Thẻ kho điện tử.", "Võ Công Tâm (TV4)"),
        ("5", "Kế toán kho\n(ACCOUNTANT)", "Phát triển Executive Dashboard với 5 thẻ KPI thời gian thực, trực quan hóa biểu đồ doanh thu 6 tháng bằng MPAndroidChart, hệ thống 9 báo cáo chuyên sâu và báo cáo dòng tiền thuần Cashflow.", "Trần Công Tú (TV5)")
    ]
    for row_idx, item in enumerate(t9_data):
        row = t9.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[3].paragraphs[0].runs[0].font.bold = True

    # TABLE 10: CÁCH THỨC CHIA CÔNG VIỆC THEO GIAI ĐOẠN (Mục 7.2)
    t10 = doc.tables[9]
    format_row(t10.rows[0], "1B365D", is_header=True)
    while len(t10.rows) > 1:
        tr = t10.rows[-1]._tr
        tr.getparent().remove(tr)

    t10_data = [
        ("Giai đoạn 1: Khảo sát nghiệp vụ & Thiết kế Core", "Xác định bài toán B2B Luxury Horology, thiết lập cấu trúc Room DB v4, viết Base ViewModel/Repository, xây dựng khung MVVM chuẩn trên nhánh `main`.", "Phan Bá Hải Bình (TV1)", "Cả 4 thành viên", "1.5 tuần"),
        ("Giai đoạn 2: Phát triển độc lập các phân hệ con", "Mỗi thành viên tạo nhánh Git riêng (`feature/...`), sử dụng bộ Prompt kỹ thuật để phát triển giao diện và nghiệp vụ phân hệ của mình kết nối với Room DB.", "Quân (TV2), Thảo (TV3), Tâm (TV4), Tú (TV5)", "Phan Bá Hải Bình hỗ trợ kỹ thuật", "2.5 tuần"),
        ("Giai đoạn 3: Tích hợp (Merge) & Kiểm thử chéo", "Review mã nguồn, gộp các nhánh vào `main`, thực hiện 4 kịch bản kiểm thử tích hợp chéo liên phân hệ (Nhập -> Tồn kệ -> Giữ chỗ -> Xuất bán -> Dashboard).", "Phan Bá Hải Bình (chủ trì)", "Cả 5 thành viên", "1.0 tuần"),
        ("Giai đoạn 4: Hoàn thiện Báo cáo Word & Chuẩn bị Vấn đáp", "Từng thành viên viết phần Word của mình theo hướng dẫn, Bình tổng hợp thành cuốn Báo cáo Đồ án hoàn chỉnh nộp Khoa, chuẩn bị dữ liệu test demo và câu hỏi vấn đáp.", "Phan Bá Hải Bình (tổng hợp)", "Cả 5 thành viên", "1.0 tuần")
    ]
    for row_idx, item in enumerate(t10_data):
        row = t10.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # TABLE 11: THEO DÕI TIẾN ĐỘ CÔNG VIỆC (Mục 7.3 - Cá nhân Phan Bá Hải Bình)
    t11 = doc.tables[10]
    format_row(t11.rows[0], "1B365D", is_header=True)
    while len(t11.rows) > 1:
        tr = t11.rows[-1]._tr
        tr.getparent().remove(tr)

    t11_data = [
        ("01/10 - 05/10/2026", "Phan Bá Hải Bình", "Khảo sát bài toán quản lý kho đồng hồ xa xỉ, xác định 4 cơ chế quản trị bắt buộc (Serial 100%, Quy đổi ĐVT, Giá vốn đích danh, Hạn mức nợ).", "100%", "Hoàn thành"),
        ("06/10 - 15/10/2026", "Phan Bá Hải Bình", "Thiết kế kiến trúc Android MVVM, khởi tạo Room Database v4 (UserEntity, ProductEntity, SerialEntity, TransactionEntity) và SessionManager.", "100%", "Hoàn thành"),
        ("16/10 - 25/10/2026", "Phan Bá Hải Bình", "Lập trình hoàn chỉnh Phân hệ 1 (ProductListFragment, ProductDetailFragment, AddEditProductActivity, LoginActivity, RBAC 5 Roles).", "100%", "Hoàn thành"),
        ("26/10 - 05/11/2026", "Phan Bá Hải Bình", "Soạn thảo Bộ Prompt chi tiết cho 5 thành viên, thiết lập quy chuẩn phân nhánh Git và xây dựng tài liệu Hướng dẫn viết Báo cáo Word & Vấn đáp.", "100%", "Hoàn thành"),
        ("06/11 - 10/11/2026", "Phan Bá Hải Bình", "Điền hoàn chỉnh dữ liệu phần việc Trưởng nhóm & Phân hệ 1 vào file Mẫu báo cáo của Khoa CNTT (ĐH Kiến trúc Đà Nẵng).", "100%", "Hoàn thành"),
        ("Hiện tại -> Nộp bài", "Cả nhóm 5 thành viên", "Tập hợp phần viết của 4 thành viên, ghép nối thành cuốn Đồ án hoàn chỉnh và chuẩn bị demo trực tiếp với TS. Đặng Hùng Vĩ.", "Đang thực hiện", "Theo lịch thi Khoa")
    ]
    for row_idx, item in enumerate(t11_data):
        row = t11.add_row()
        for c_idx, val in enumerate(item):
            row.cells[c_idx].text = val
        bg = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        format_row(row, bg, is_header=False)
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if "100%" in item[3]:
            row.cells[3].paragraphs[0].runs[0].font.bold = True

    # Lưu file
    try:
        doc.save(output_path)
        print(f"SUCCESS: Report saved at {output_path}")
    except PermissionError:
        alt_path = r"D:\cntt\pbhb\Document\BAO_CAO_PHAN_TICH_HE_THONG_THONG_TIN_CHRONOVAULT_WMS_CAP_NHAT.docx"
        doc.save(alt_path)
        print(f"LOCKED: File gốc đang mở trong Word, đã lưu bản cập nhật chuẩn tại: {alt_path}")

if __name__ == "__main__":
    create_report_for_binh()
