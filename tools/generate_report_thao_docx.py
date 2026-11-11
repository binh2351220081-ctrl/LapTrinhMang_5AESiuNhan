"""
Script tạo Báo cáo Phân tích Thiết kế Hệ thống Thông tin - TV3: Tô Đức Thảo
Định dạng: Microsoft Word (.docx) chuyên nghiệp chuẩn học thuật
Phiên bản: Hoàn thiện 100% - Kho Chứa Đồng Hồ Thuần Túy (Không Bán Hàng / Không Mua Bán)
Tác giả: Tô Đức Thảo (TV3) - Nhóm 5 AE Siêu Nhân - ChronoVault WMS
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def build_thao_report():
    doc = Document()

    # Thiết lập lề trang chuẩn A4
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.different_first_page_header_footer = False

    # Bảng màu nhận diện chuyên nghiệp
    C_NAVY = RGBColor(27, 54, 93)       # #1B365D - Xanh Navy chủ đạo
    C_GOLD = RGBColor(180, 83, 9)       # #B45309 - Vàng Amber điểm nhấn
    C_SLATE = RGBColor(51, 65, 85)      # #334155 - Xám than văn bản
    C_MUTED = RGBColor(100, 116, 139)   # #64748B - Xám phụ trợ
    C_GREEN = RGBColor(22, 101, 52)     # #166534 - Xanh lục trạng thái Pass
    C_DARK = RGBColor(15, 23, 42)       # #0F172A - Đen mực chuẩn

    # Thiết lập style Normal mặc định
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(8.5)
    style_normal.font.color.rgb = C_SLATE
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_before = Pt(0)
    style_normal.paragraph_format.space_after = Pt(2)

    # Helper XML định dạng bảng và ô
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        for existing in tcPr.findall(qn('w:shd')):
            tcPr.remove(existing)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=50, bottom=50, left=70, right=70):
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

    def format_row(row, bg_color, is_header=False, font_size=8.0, bold=False, align_cols=None):
        for col_idx, cell in enumerate(row.cells):
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                if is_header:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif align_cols and col_idx in align_cols:
                    p.alignment = align_cols[col_idx]
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(font_size)
                    r.font.bold = is_header or bold
                    r.font.color.rgb = RGBColor(255, 255, 255) if is_header else C_SLATE

    def add_chapter_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    def add_section_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    def add_section_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = C_GOLD

    def add_body_p(text, bold_prefix=None, space_after=2):
        """Đoạn văn xuôi căn đều, không chứa ký tự xuống dòng thô để tránh lỗi giãn từ"""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Arial"
            r_pre.font.size = Pt(8.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = C_NAVY
        r_body = p.add_run(text)
        r_body.font.name = "Arial"
        r_body.font.size = Pt(8.5)
        r_body.font.color.rgb = C_SLATE

    def add_bullet_p(text, bold_prefix=None, bullet="• "):
        """Đoạn gạch đầu dòng căn lề trái, thụt lề, KHÔNG BAO GIỜ bị lỗi dãn chữ"""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        
        r_bullet = p.add_run(bullet)
        r_bullet.font.name = "Arial"
        r_bullet.font.size = Pt(8.5)
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = C_GOLD

        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Arial"
            r_pre.font.size = Pt(8.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = C_NAVY

        r_body = p.add_run(text)
        r_body.font.name = "Arial"
        r_body.font.size = Pt(8.5)
        r_body.font.color.rgb = C_SLATE

    def add_box(title, items, bg="F8FAFC", title_color=C_NAVY):
        """Hộp thông tin viền trang nhã, mỗi mục là 1 paragraph căn lề trái riêng biệt"""
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)

        # Viền hộp
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
                <w:left w:val="single" w:sz="18" w:space="0" w:color="1B365D"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
                <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        # Tiêu đề box
        p_t = cell.paragraphs[0]
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(3)
        p_t.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_t = p_t.add_run(title)
        r_t.font.name = "Arial"
        r_t.font.size = Pt(9.0)
        r_t.font.bold = True
        r_t.font.color.rgb = title_color

        # Nội dung từng dòng
        for it in items:
            p_i = cell.add_paragraph()
            p_i.paragraph_format.space_before = Pt(0)
            p_i.paragraph_format.space_after = Pt(2)
            p_i.paragraph_format.line_spacing = 1.15
            p_i.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r_i = p_i.add_run(it)
            r_i.font.name = "Arial"
            r_i.font.size = Pt(8.0)
            r_i.font.color.rgb = C_DARK

    def add_code_box(title, code_lines):
        """Khung hiển thị sơ đồ cây chức năng và ERD bằng font Monospace (Consolas) không bị dãn chữ"""
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=60, bottom=60, left=90, right=90)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
                <w:left w:val="single" w:sz="16" w:space="0" w:color="B45309"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
                <w:right w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p_t = cell.paragraphs[0]
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(2)
        p_t.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_t = p_t.add_run(f"📌 {title}")
        r_t.font.name = "Arial"
        r_t.font.size = Pt(8.5)
        r_t.font.bold = True
        r_t.font.color.rgb = C_NAVY

        for line in code_lines:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0.5)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(line)
            r.font.name = "Consolas"
            r.font.size = Pt(7.5)
            r.font.color.rgb = C_DARK

    # =========================================================
    # HEADER TRANG BÁO CÁO
    # =========================================================
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_top.paragraph_format.space_after = Pt(4)
    r_uni = p_top.add_run("TRƯỜNG ĐẠI HỌC KIẾN TRÚC ĐÀ NẴNG • KHOA CÔNG NGHỆ THÔNG TIN\n")
    r_uni.font.name = "Arial"; r_uni.font.size = Pt(8); r_uni.font.bold = True; r_uni.font.color.rgb = C_MUTED
    r_sub = p_top.add_run("Học phần: Phân Tích Hệ Thống Thông Tin & Lập Trình Mạng • Đề tài: ChronoVault WMS")
    r_sub.font.name = "Arial"; r_sub.font.size = Pt(8); r_sub.font.color.rgb = C_MUTED

    add_chapter_title("BÁO CÁO PHÂN TÍCH HỆ THỐNG THÔNG TIN — PHẦN CÔNG VIỆC CỦA TÔ ĐỨC THẢO\n(PHÂN HỆ 3: QUẢN LÝ ĐƠN VỊ TIẾP NHẬN & TÁC NGHIỆP ĐIỀU PHỐI XUẤT KHO)")

    add_box(
        "TÔN CHỈ THIẾT KẾ ĐỀ TÀI: KHO CHỨA ĐỒNG HỒ THUẦN TÚY (CHỈ CÓ NHẬP VÀ XUẤT, KHÔNG MUA HAY BÁN)",
        [
            "• Đề tài ChronoVault WMS thuần túy là Hệ thống Quản trị Kho Tổng Lưu Trữ & Điều Phối (Central Storage & Logistics Hub).",
            "• TUYỆT ĐỐI KHÔNG MUA BÁN: Kho không bán lẻ, không bán sỉ, không có quầy thu ngân POS, không chào giá, không tiếp thị hay chốt sale thương mại.",
            "• HAI NHIỆM VỤ CỐT LÕI DUY NHẤT:",
            "    1. NHẬP HÀNG VÀO (Inbound Receiving): Tiếp nhận đồng hồ từ nhà sản xuất/đơn vị cung ứng đưa vào lưu trữ, kiểm định và nạp Serial.",
            "    2. XUẤT HÀNG RA (Outbound Dispatching): Tiếp nhận Lệnh điều phối xuất kho cho các chi nhánh/showroom tiếp nhận trưng bày, xuất bảo hành hãng, xuất tiêu hủy phế phẩm.",
            "• BẢN CHẤT CÁC CHỈ SỐ GIÁ TRỊ: Đơn giá và giá trị lô hàng thuần túy là 'Giá trị định giá tài sản lưu kho theo bảo hiểm hàng xa xỉ' (Asset Valuation) và 'Hạn mức bảo lãnh trách nhiệm lưu giữ tài sản' (Asset Custody Limit) nhằm chống thất thoát tài sản của tổng kho, hoàn toàn không phải là doanh thu bán hàng.",
            "• Phân hệ 3 (Tô Đức Thảo) là 'Trung tâm Điều phối & Tác nghiệp Xuất kho': Tiếp nhận Lệnh điều phối xuất kho (Outbound Dispatch Orders), thẩm định hạn mức bảo lãnh tài sản, khóa giữ chỗ tồn kho (Reservation Engine), soạn hàng (Picking), quét đối soát 100% Serial bằng Camera (Verification), đóng kiện niêm phong (Packing), lập Biên bản bàn giao xuất kho vật lý (Dispatch), xuất bảo hành hãng, xuất tiêu hủy và tiếp nhận hàng hoàn trả."
        ],
        bg="EFF6FF", title_color=C_NAVY
    )

    add_box(
        "THÔNG TIN SINH VIÊN VÀ ĐẶC TẢ VAI TRÒ",
        [
            "• Sinh viên thực hiện: TÔ ĐỨC THẢO (Thành viên 3 - TV3)",
            "• Giảng viên hướng dẫn: TS. Đặng Hùng Vĩ",
            "• Tác nhân nghiệp vụ: OPERATIONS_STAFF (Nhân viên Điều phối & Tác nghiệp Xuất kho)",
            "• Phân hệ chuyên trách: MOD-03 - Quản lý Đơn vị Tiếp nhận & Điều phối Xuất kho đa năng",
            "• Nhóm thực hiện: 5 AE Siêu Nhân (Bình - Leader TV1, Quân TV2, Thảo TV3, Tâm TV4, Tú TV5)",
            "• Nhánh Git phân công: feature/tv3-outbound-dealer • Package: com.example.chronovaultwms.outbound",
            "• Tài khoản Demo: @quan_thao_ops (Mật khẩu: 123)"
        ]
    )

    # ---------------------------------------------------------
    # 1. TỔNG QUAN ĐỀ TÀI & PHÂN HỆ PHỤ TRÁCH
    # ---------------------------------------------------------
    add_section_h1("1. TỔNG QUAN ĐỀ TÀI & PHÂN HỆ PHỤ TRÁCH (GÓC NHÌN TV3: TÔ ĐỨC THẢO)")
    
    add_body_p(
        "Hệ Thống Quản Lý Kho Chứa Đồng Hồ Cao Cấp (ChronoVault WMS)",
        "1.1. Tên đề tài chung của nhóm: "
    )

    add_body_p(
        "Phân hệ 3: Quản Lý Đơn Vị Tiếp Nhận & Tác Nghiệp Điều Phối Xuất Kho (Outbound Fulfillment Hub)",
        "1.2. Phân hệ chuyên trách của Thành viên 3: "
    )
    
    add_body_p("Dưới góc nhìn nghiệp vụ Kho chứa và Điều phối Lưu chuyển Tài sản, đề tài gồm 3 thành phần cấu thành:", "1.3. Phân tích 3 thành phần cấu thành phạm vi nghiệp vụ: ")
    add_bullet_p("Quản trị Kho lưu trữ & Điều phối xuất hàng đa luồng (Warehouse Storage & Outbound Dispatching).", "Loại hình / Hành động: ", bullet="- ")
    add_bullet_p("Thẩm định hạn mức bảo lãnh trách nhiệm tài sản (Asset Custody Limit), Khóa giữ chỗ tồn kho chống xuất âm (Inventory Reservation Engine), Quét Camera đối soát 100% Serial lúc đóng kiện xuất kho (Picking & Dispatch Scan), Xuất bảo hành/tiêu hủy, và Quản lý đối soát bàn giao với các đơn vị tiếp nhận.", "Chức năng chính: ", bullet="- ")
    add_bullet_p("Kho tổng lưu trữ và bảo quản các dòng đồng hồ xa xỉ giá trị cao (Rolex, Omega, Patek Philippe, Audemars Piguet...).", "Đối tượng / Lĩnh vực: ", bullet="- ")

    add_section_h2("1.4. Bảng 1.1: So sánh Cơ chế Vận hành Kho của ChronoVault WMS với thị trường:")

    tbl_comp = doc.add_table(rows=1, cols=5)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_c = tbl_comp.rows[0]
    h_c.cells[0].text = "Tiêu chí so sánh"
    h_c.cells[1].text = "Phần mềm bán lẻ / POS"
    h_c.cells[2].text = "ERP Sản xuất (SAP B1)"
    h_c.cells[3].text = "ERP Quản trị (Odoo WMS)"
    h_c.cells[4].text = "ChronoVault WMS (TV3)"
    format_row(h_c, "1B365D", is_header=True)

    comp_rows = [
        ("Bản chất hệ thống", "Bán lẻ / POS thu ngân", "Sản xuất đa quốc gia", "Quản trị tổng thể", "Kho chứa chuyên dụng: Nhập kho - Lưu kho kệ - Xuất điều phối"),
        ("Nghiệp vụ xuất kho", "Bán lẻ cho khách tại quầy", "Xuất kho nguyên vật liệu", "Xuất bán hàng chung", "Xử lý Lệnh điều phối xuất kho cho đơn vị nhận, xuất bảo hành hãng, xuất tiêu hủy"),
        ("Khóa giữ chỗ (Reservation)", "Không có (dễ xuất âm kho)", "Phân bổ MRP phức tạp", "Module Reservation", "Khóa tự động cấp SKU khi duyệt Lệnh (RESERVED), phát WebSocket tức thời"),
        ("Kiểm soát hạn mức", "Nhắc nợ tại quầy thu ngân", "Thẩm định tín dụng đa cấp", "Cảnh báo hạn mức", "Khóa chặn tự động không cho duyệt xuất nếu vượt hạn mức bảo lãnh tài sản chi nhánh"),
        ("Quét Serial xuất kho", "Nhập tay / Quét ngẫu nhiên", "Quét mã vạch tích hợp", "Quét Barcode", "Camera đối soát 100% Serial: đúng SKU, trạng thái IN_STOCK, chặn xuất nhầm hàng lỗi"),
        ("Quy đổi ĐVT xuất", "Chỉ nhân chia số lượng", "Hỗ trợ đa cấp UoM", "Hỗ trợ UoM", "Lên lệnh xuất Thùng/Chiếc, tự động quy đổi và kiểm tra điều kiện xuất tối thiểu MOQ"),
        ("Nền tảng vận hành", "Web App / POS Tablet", "Desktop Client nặng", "Web App", "Android Native (Kotlin MVVM), nhân viên kho cầm điện thoại quét trực tiếp tại kệ")
    ]
    align_center_col0 = {0: WD_ALIGN_PARAGRAPH.CENTER}
    for r_data in comp_rows:
        row = tbl_comp.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_center_col0)

    # ---------------------------------------------------------
    # 2. ĐẶC TẢ YÊU CẦU CHỨC NĂNG (PHÂN HỆ 3)
    # ---------------------------------------------------------
    add_section_h1("2. ĐẶC TẢ YÊU CẦU CHỨC NĂNG (PHÂN HỆ 3 - TÔ ĐỨC THẢO)")

    tbl_req = doc.add_table(rows=1, cols=5)
    tbl_req.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_r = tbl_req.rows[0]
    h_r.cells[0].text = "Mã YC"
    h_r.cells[1].text = "Tên yêu cầu"
    h_r.cells[2].text = "Mô tả chi tiết luồng xử lý kho"
    h_r.cells[3].text = "Ưu tiên"
    h_r.cells[4].text = "Nguồn"
    format_row(h_r, "1B365D", is_header=True)

    fr_data = [
        ("FR-06", "Quản lý Hồ sơ Đơn vị Tiếp nhận Hàng", "Khai báo và quản lý danh bạ các chi nhánh/showroom tiếp nhận hàng xuất từ kho tổng: Mã đơn vị, Tên chi nhánh, MST, Người đại diện, Địa chỉ kho nhận, Phân hạng ưu tiên điều phối (Hạng 1, Hạng 2, Hạng 3), Hệ số phân bổ tài sản.", "Cao", "Kế toán kho / Quản lý đơn vị nhận"),
        ("FR-07", "Kiểm soát Hạn mức Bảo lãnh Tài sản", "Thiết lập Hạn mức bảo lãnh trách nhiệm tài sản tối đa (Asset Custody Limit từ 1 - 3 tỷ) cho chi nhánh nhận hàng. Tự động kiểm tra: Giá trị tài sản đang giữ + Lệnh mới - Ký quỹ <= Hạn mức. Chặn quyền duyệt Lệnh xuất nếu vượt ngưỡng.", "Cao", "Kế toán kho / Quản trị hệ thống"),
        ("FR-08", "Tiếp nhận Lệnh Điều Phối & Khóa Giữ Chỗ", "Tiếp nhận Lệnh điều phối xuất Thùng hoặc Chiếc lẻ, kiểm tra định mức xuất tối thiểu MOQ (>= 5-10c), kiểm tra Tồn khả dụng (Available = Physical - Reserved). Duyệt lệnh: Chuyển RESERVED, tăng tồn giữ chỗ chống xuất âm kho.", "Cao", "NV Điều phối / Thủ kho"),
        ("FR-09", "Quét Camera Serial Đóng Kiện Thực Xuất", "Dùng Camera quét Serial laser trên từng hộp đồng hồ. Đối soát đúng SKU, trạng thái IN_STOCK, hàng mới HANG_MOI (chặn xuất nhầm hàng lỗi). Đủ 100% mới xuất kho, đổi DISPATCHED, trừ tồn vật lý.", "Cao", "NV Xuất kho / Thủ kho"),
        ("FR-10", "Quản lý Xuất Bảo Hành, Hủy & Nhận Hoàn Trả", "Lập phiếu xuất chuyển bảo hành hãng; lập phiếu xuất tiêu hủy phế phẩm vỡ/hỏng; tiếp nhận sản phẩm chi nhánh gửi hoàn trả về kho (quét Serial đối soát lịch sử xuất, phân loại Kho Mới/Lỗi). Lập Phiếu xác nhận bàn giao giải phóng hạn mức.", "Trung bình", "Kế toán kho / NV Xuất kho")
    ]
    align_fr = {0: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER}
    for r_data in fr_data:
        row = tbl_req.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_fr)

    # ---------------------------------------------------------
    # 3. PHÂN TÍCH ĐỐI TƯỢNG & NHÓM CHỨC NĂNG
    # ---------------------------------------------------------
    add_section_h1("3. PHÂN TÍCH ĐỐI TƯỢNG & NHÓM CHỨC NĂNG PHÂN HỆ 3")

    add_section_h2("3.1. Danh sách Đối tượng cốt lõi do Tô Đức Thảo thiết kế:")
    tbl_ent = doc.add_table(rows=1, cols=5)
    tbl_ent.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_e = tbl_ent.rows[0]
    h_e.cells[0].text = "Mã ĐT"
    h_e.cells[1].text = "Tên đối tượng"
    h_e.cells[2].text = "Mô tả nghiệp vụ kho"
    h_e.cells[3].text = "Thuộc tính chính"
    h_e.cells[4].text = "Quan hệ thực thể"
    format_row(h_e, "1B365D", is_header=True)

    ent_data = [
        ("ENT-06", "Dealer (Đơn vị nhận hàng)", "Quản lý đơn vị/chi nhánh nhận hàng xuất từ kho tổng, hạn mức bảo lãnh tài sản và giá trị tài sản đang lưu giữ.", "dealerId, name, tier, discountPercent, creditLimit, currentDebt, taxCode", "Tiếp nhận nhiều Lệnh xuất (1-N); Phát sinh nhiều Phiếu giải phóng bảo lãnh (1-N)"),
        ("ENT-07", "OutboundOrder (Lệnh điều phối xuất)", "Lệnh yêu cầu xuất hàng từ kho tổng, quản lý khóa giữ chỗ tồn kho và tổng giá trị tài sản điều chuyển.", "orderCode, dealerId, totalAmount, depositAmount, remainingDebt, status", "Thuộc 1 Đơn vị nhận (N-1); Chứa nhiều OrderItem (1-N); Sinh 1 Phiếu xuất (1-1)"),
        ("ENT-08", "OrderItem (Chi tiết mặt hàng xuất)", "Chi tiết SKU yêu cầu xuất, quy cách Thùng/Chiếc và số lượng quy đổi khóa giữ chỗ trên kệ.", "itemId, orderCode, productCode, unit, quantity, convertedQuantity, subtotal", "Thuộc 1 Lệnh xuất (N-1); Tham chiếu 1 Product (N-1)"),
        ("ENT-09", "OutboundDispatch (Phiếu xuất bàn giao)", "Chứng từ xuất kho kiêm biên bản bàn giao niêm phong vận chuyển có giá trị pháp lý kho vận.", "dispatchCode, orderCode, dealerId, dispatchDate, totalCostPrice, status", "Thuộc 1 Lệnh xuất (1-1); Chứa danh sách Serial xuất (1-N)"),
        ("ENT-10", "DealerReceipt (Phiếu giải phóng bảo lãnh)", "Chứng từ xác nhận chi nhánh đã nhận bàn giao an toàn hoặc nộp ký quỹ nhằm giải phóng hạn mức bảo lãnh.", "receiptId, dealerId, amount, paymentMethod, referenceDoc, date", "Thuộc 1 Đơn vị nhận (N-1); Giảm trừ giá trị tài sản đang giữ"),
        ("ENT-11", "CustomerReturn (Phiếu nhận hoàn trả)", "Tiếp nhận sản phẩm hoàn trả về kho tổng, quét đối soát Serial nguồn gốc xuất và giải phóng trách nhiệm.", "returnId, dealerId, serialNumber, returnReason, targetWarehouse, refundAmount", "Thuộc 1 Đơn vị nhận (N-1); Liên kết 1 mã Serial (N-1)")
    ]
    align_ent = {0: WD_ALIGN_PARAGRAPH.CENTER}
    for r_data in ent_data:
        row = tbl_ent.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_ent)

    add_section_h2("3.2. Vị trí Phân hệ 3 trong Hệ thống ChronoVault WMS (5 Phân hệ):")
    add_bullet_p("Quản lý bảo mật, phân quyền RBAC 5 Roles, danh mục thông số kỹ thuật đồng hồ xa xỉ, thiết lập ĐVT 2 cấp và Room Core.", "MOD-01 (Phan Bá Hải Bình): ")
    add_bullet_p("Tiếp nhận hàng Inbound từ đơn vị sản xuất, quy đổi Thùng -> Chiếc, nạp dải Serial và phân bổ giá vốn đích danh.", "MOD-02 (Nguyễn Đắc Quân): ")
    add_bullet_p("Tiếp nhận Lệnh điều phối xuất kho, kiểm soát hạn mức bảo lãnh tài sản, khóa giữ chỗ tồn kho (Reservation), quét Camera Serial xuất kho 2 bước, xuất bảo hành hãng/tiêu hủy và giải phóng hạn mức bảo lãnh.", "MOD-03 (Tô Đức Thảo - Tác giả): ")
    add_bullet_p("Quản trị tồn kho đa vị trí kệ Bin K1/K2, quản lý 3 kho chất lượng (Mới/Trưng bày/Lỗi), kiểm kê thực tế và Sổ Thẻ kho.", "MOD-04 (Võ Công Tâm): ")
    add_bullet_p("Thống kê KPI kho vận, giá trị luân chuyển hàng xuất nhập và phân tích dòng tiền luân chuyển kho.", "MOD-05 (Trần Công Tú): ")

    # ---------------------------------------------------------
    # 4. PHÂN TÍCH CHỨC NĂNG ĐẾN TẬN CÙNG
    # ---------------------------------------------------------
    add_section_h1("4. PHÂN TÍCH CHỨC NĂNG ĐẾN TẬN CÙNG (PHÂN HỆ 3)")

    add_section_h2("4.1. Cấu trúc phân rã chức năng (Functional Decomposition Tree)")
    tree_lines = [
        "MOD-03: Quản Lý Đơn Vị Tiếp Nhận & Tác Nghiệp Điều Phối Xuất Kho (Tô Đức Thảo)",
        "├── 4.1: Quản lý đơn vị/chi nhánh tiếp nhận hàng xuất kho",
        "│    ├── 4.1.1: Quản lý hồ sơ đơn vị nhận hàng (MST, tên đơn vị, người đại diện, địa chỉ kho nhận)",
        "│    ├── 4.1.2: Cấu hình hạn mức bảo lãnh tài sản xuất kho & Phân hạng ưu tiên điều phối",
        "│    └── 4.1.3: Lập chứng từ xác nhận bàn giao hoàn tất & Giải phóng hạn mức bảo lãnh lưu kho",
        "├── 4.2: Tiếp nhận & Tác nghiệp Lệnh điều phối xuất kho (Outbound Dispatch Fulfillment)",
        "│    ├── 4.2.1: Khởi tạo Lệnh yêu cầu xuất kho (Chọn đơn vị nhận, Thùng/Chiếc, kiểm tra MOQ, kiểm tra tồn)",
        "│    ├── 4.2.2: Thẩm định điều kiện xuất & Khóa giữ chỗ kệ hàng (Check hạn mức bảo lãnh, khóa RESERVED)",
        "│    └── 4.2.3: Soạn hàng, Quét Camera Serial đóng kiện & Thực xuất kho (Picking list, Camera Serial, DISPATCHED)",
        "├── 4.3: Tác nghiệp xuất kho phi thương mại (Xuất bảo hành hãng, Xuất thanh lý, Xuất tiêu hủy phế phẩm)",
        "└── 4.4: Tiếp nhận hàng hoàn trả về kho từ chi nhánh (Quét Serial kiểm tra xuất xứ, phân loại Kho Mới/Lỗi)"
    ]
    add_code_box("CÂY PHÂN RÃ CHỨC NĂNG 4 CẤP (QUẢN TRỊ KHO VẬN XUẤT HÀNG)", tree_lines)

    add_section_h2("4.2. Bảng Mô tả Module IPO: MOD-03-01 (Tiếp nhận Lệnh Điều Phối Xuất & Khóa Giữ Chỗ)")
    tbl_ipo1 = doc.add_table(rows=1, cols=2)
    tbl_ipo1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ipo1.rows[0].cells[0].text = "Hạng mục"; tbl_ipo1.rows[0].cells[1].text = "Nội dung chi tiết"
    format_row(tbl_ipo1.rows[0], "1B365D", is_header=True)

    ipo1_rows = [
        ("Input", "Mã đơn vị tiếp nhận hàng, Mã SKU yêu cầu xuất, ĐVT ('Thùng' hoặc 'Chiếc lẻ'), Số lượng xuất, Tiền ký quỹ bảo lãnh trách nhiệm (nếu có). Nguồn: Form dialog_create_outbound_order.xml."),
        ("Process", "1. Quy đổi số lượng chiếc: convertedQty = isBox ? qty * conversionRate : qty.\n2. Kiểm tra định mức xuất tối thiểu MOQ >= moq; Kiểm tra Tồn khả dụng (Available = Physical - Reserved).\n3. Tính giá trị định giá tài sản điều chuyển theo bảng kê bảo hiểm lưu kho.\n4. Thẩm định hạn mức bảo lãnh tài sản: Trách nhiệm dự kiến = Trách nhiệm cũ + (Tổng giá trị - Ký quỹ). Nếu vượt Credit Limit -> Khóa nút Duyệt, báo đỏ vượt hạn mức bảo lãnh tài sản của chi nhánh.\n5. Nếu hợp lệ: Lưu Lệnh xuất RESERVED, tăng reservedQuantity trong CSDL, phát WebSocket EVENT_STOCK_RESERVED sang máy Thủ kho TV4."),
        ("Output", "Bản ghi Lệnh điều phối xuất RESERVED trong outbound_orders; Tồn giữ chỗ tăng; Tồn khả dụng giảm (chống xuất âm kho); Ghi Nhật ký kiểm toán Audit Log."),
        ("Actor & Quyền", "Nhân viên điều phối xuất kho (lên lệnh nháp), Kế toán kho (thẩm định bảo lãnh & ký duyệt giữ chỗ), Chủ kho (duyệt ngoại lệ)."),
        ("Ràng buộc", "Tuyệt đối không duyệt lệnh vượt quá Tồn khả dụng; Không cho duyệt vượt hạn mức bảo lãnh tài sản nếu chưa có phê duyệt ngoại lệ.")
    ]
    for k, v in ipo1_rows:
        r = tbl_ipo1.add_row()
        r.cells[0].text = k; r.cells[1].text = v
        format_row(r, "FFFFFF", font_size=7.5, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER})

    add_section_h2("4.3. Bảng Mô tả Module IPO: MOD-03-02 (Soạn Hàng & Quét Serial Thực Xuất Kho)")
    tbl_ipo2 = doc.add_table(rows=1, cols=2)
    tbl_ipo2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ipo2.rows[0].cells[0].text = "Hạng mục"; tbl_ipo2.rows[0].cells[1].text = "Nội dung chi tiết"
    format_row(tbl_ipo2.rows[0], "1B365D", is_header=True)

    ipo2_rows = [
        ("Input", "Mã Lệnh điều phối xuất RESERVED, Danh sách mã Serial quét từ hiện vật trên kệ kho.\n• Smart Picking List: Hệ thống trích xuất kèm Tọa độ ngăn kệ 5 cấp (currentLocation: Kệ-Dãy-Tầng-Ngăn hoặc Két sắt) và Giá vốn đích danh (unitCost) của từng Serial theo lô xuất chỉ định (FIFO).\n• Nguồn: Camera Barcode Scanner (ML Kit)."),
        ("Process", "1. Hệ thống tự động sinh Smart Picking List: Liệt kê đích danh Serial cần xuất kèm vị trí ngăn kệ (currentLocation) và giá vốn đích danh (unitCost).\n2. Thủ kho căn cứ lộ trình trên Picking List đi đến đúng tọa độ ngăn kệ (VD: Kệ K1-A02-B03 hoặc Két VIP-02) rút khay lấy đồng hồ về bàn đóng gói.\n3. Quét Camera từng mã Serial: Truy vấn kiểm tra trong bảng serials.\n4. Kiểm tra đối khớp chéo thời gian thực:\n   - Đúng productCode của Lệnh xuất.\n   - Đúng Serial được chỉ định trong Picking List (nếu lấy nhầm Serial khác lô/sai giá vốn -> Rung cảnh báo, phát âm thanh lỗi và chặn nạp).\n   - Trạng thái bắt buộc IN_STOCK và chất lượng hàng mới HANG_MOI (chặn DEFECTIVE, DISPLAY).\n5. Kiểm tra chống quét trùng lặp mã Serial trong cùng kiện hàng đóng xuất.\n6. Quét đủ 100%: Mở nút 'Xác nhận xuất kho'.\n7. Kích hoạt Room Database Transaction: Serial đổi sang DISPATCHED, trừ tồn vật lý, giải phóng giữ chỗ, ghi nhận bàn giao tài sản."),
        ("Output", "Lệnh xuất chuyển COMPLETED; In Biên bản bàn giao kiêm Phiếu xuất kho khổ A4 có bảng kê Serial và vị trí ngăn kệ; Phát thông điệp Socket EVENT_DISPATCH_COMPLETED sang TV4 và TV5."),
        ("Actor & Quyền", "Nhân viên xuất kho (quét Serial đóng kiện), Thủ kho (ký xác nhận bàn giao niêm phong vật lý)."),
        ("Ràng buộc", "Bắt buộc quét đúng 100% mã Serial trong Picking List; Nghiêm cấm xuất hàng lỗi kỹ thuật hoặc sai lô giá vốn.")
    ]
    for k, v in ipo2_rows:
        r = tbl_ipo2.add_row()
        r.cells[0].text = k; r.cells[1].text = v
        format_row(r, "FFFFFF", font_size=7.5, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER})

    add_section_h2("4.4. Bảng Mô tả Module IPO: MOD-03-03 (Tác Nghiệp Xuất Kho Phi Thương Mại: Bảo Hành & Hủy)")
    tbl_ipo3 = doc.add_table(rows=1, cols=2)
    tbl_ipo3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ipo3.rows[0].cells[0].text = "Hạng mục"; tbl_ipo3.rows[0].cells[1].text = "Nội dung chi tiết"
    format_row(tbl_ipo3.rows[0], "1B365D", is_header=True)

    ipo3_rows = [
        ("Input", "Danh sách Serial lỗi (DEFECTIVE) hoặc hàng mẫu (DISPLAY), Mục đích ('BAO_HANH_HANG', 'TIEU_HUY'), Biên bản thẩm định kỹ thuật."),
        ("Process", "1. Chọn mục đích xuất: Bảo hành chính hãng hoặc Tiêu hủy phế phẩm.\n2. Chọn Serial từ Kho Lỗi/Kho Trưng Bày.\n3. Duyệt cấp quản lý: Tiêu hủy tài sản bắt buộc có chữ ký phê duyệt từ Chủ kho (STORE_OWNER).\n4. Cập nhật trạng thái Serial sang BAO_HANH hoặc DA_TIEU_HUY; trừ tồn vật lý tại TV4; ghi Sổ Thẻ kho (-)."),
        ("Output", "Phiếu xuất khác (XK-xxxx) COMPLETED; Giảm tồn kho lỗi TV4; Ghi Audit Log; Cập nhật Báo cáo cơ cấu xuất kho."),
        ("Actor & Quyền", "Nhân viên xuất kho (lập phiếu), Thủ kho (bàn giao vật lý), Chủ kho (phê duyệt tiêu hủy tài sản)."),
        ("Ràng buộc", "Chỉ xuất Serial nằm trong Kho Lỗi hoặc Kho Trưng Bày; Nghiêm cấm tiêu hủy khi chưa có biên bản kỹ thuật.")
    ]
    for k, v in ipo3_rows:
        r = tbl_ipo3.add_row()
        r.cells[0].text = k; r.cells[1].text = v
        format_row(r, "FFFFFF", font_size=7.5, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER})

    add_section_h2("4.5. Bảng Mô tả Module IPO: MOD-03-04 (Tiếp Nhận Hoàn Trả Về Kho & Đối Soát Serial)")
    tbl_ipo4 = doc.add_table(rows=1, cols=2)
    tbl_ipo4.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ipo4.rows[0].cells[0].text = "Hạng mục"; tbl_ipo4.rows[0].cells[1].text = "Nội dung chi tiết"
    format_row(tbl_ipo4.rows[0], "1B365D", is_header=True)

    ipo4_rows = [
        ("Input", "Mã đơn vị hoàn trả, Danh sách Serial gửi trả, Lý do hoàn trả, Đánh giá chất lượng thực tế."),
        ("Process", "1. Quét mã Serial gửi trả: Đối soát trong CSDL kiểm tra trạng thái DISPATCHED và đã xuất đúng cho đơn vị này trong lịch sử xuất kho.\n2. Phân loại chất lượng: Nguyên seal -> Nhập Kho Mới; Trầy xước/lỗi -> Nhập Kho Lỗi C-01.\n3. Duyệt tiếp nhận: Đổi Serial sang TRONG_KHO; tăng tồn kho TV4; giảm giá trị tài sản đang giữ của đơn vị; khôi phục hạn mức bảo lãnh."),
        ("Output", "Phiếu nhận hoàn trả (TS-xxxx) APPROVED; Tăng tồn kho TV4; Giảm trách nhiệm tài sản; Ghi dòng Thẻ kho (+)."),
        ("Actor & Quyền", "Nhân viên xuất kho (quét Serial), Thủ kho (phân loại kho nhập), Kế toán kho (cấn trừ trách nhiệm tài sản)."),
        ("Ràng buộc", "Serial gửi trả bắt buộc phải có lịch sử đã xuất kho đúng cho đơn vị đó (chống nhận hàng giả).")
    ]
    for k, v in ipo4_rows:
        r = tbl_ipo4.add_row()
        r.cells[0].text = k; r.cells[1].text = v
        format_row(r, "FFFFFF", font_size=7.5, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER})

    # ---------------------------------------------------------
    # 5. LUỒNG DỮ LIỆU LIÊN QUAN ĐẾN ĐỐI TƯỢNG & CHỨC NĂNG
    # ---------------------------------------------------------
    add_section_h1("5. LUỒNG DỮ LIỆU LIÊN QUAN ĐẾN ĐỐI TƯỢNG & CHỨC NĂNG")

    add_section_h2("5.1. Ma trận CRUD (Phân hệ 3 - Điều phối & Xuất kho):")
    tbl_crud = doc.add_table(rows=1, cols=6)
    tbl_crud.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_cr = tbl_crud.rows[0]
    h_cr.cells[0].text = "Đối tượng \\ Thao tác"
    h_cr.cells[1].text = "Tạo (C)"
    h_cr.cells[2].text = "Đọc (R)"
    h_cr.cells[3].text = "Cập nhật (U)"
    h_cr.cells[4].text = "Xóa (D)"
    h_cr.cells[5].text = "Ghi chú ràng buộc"
    format_row(h_cr, "1B365D", is_header=True)

    crud_data = [
        ("Dealer (Đơn vị tiếp nhận)", "Kế toán, Admin", "Tất cả Actor", "Kế toán, Chủ", "Khóa LOCKED", "Không xóa cứng để bảo toàn lịch sử bàn giao tài sản"),
        ("OutboundOrder (Lệnh điều phối)", "NV Điều phối, Kế toán", "Tất cả Actor", "Kế toán (chưa xuất)", "Hủy CANCELLED", "Hủy lệnh tự động giải phóng tồn giữ chỗ trên kệ"),
        ("OutboundDispatch (Phiếu xuất)", "NV Xuất kho, Thủ kho", "Tất cả Actor", "Thủ kho (đang đóng)", "Cấm xóa", "Biên bản bàn giao có giá trị pháp lý kho vận"),
        ("SerialEntity (Mã Serial)", "PH2 (Nhập kho)", "Tất cả Actor", "NV Xuất (-> DISPATCHED)", "Cấm xóa", "Truy vết trọn đời vòng đời đồng hồ"),
        ("DealerReceipt (Phiếu giải phóng)", "Kế toán", "Tất cả Actor", "Kế toán", "Cấm xóa", "Chứng từ xác nhận hoàn tất giao nhận tài sản")
    ]
    align_crud = {1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER}
    for r_data in crud_data:
        row = tbl_crud.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_crud)

    add_section_h2("5.2. Sơ đồ Tuần tự Nghiệp vụ Xuất kho (Sequence Diagram):")
    seq_steps = [
        "1. Nhân viên Điều phối (TV3) lập Lệnh điều phối xuất kho -> Chọn đơn vị nhận, SKU, ĐVT Thùng/Chiếc, Số lượng.",
        "2. Hệ thống kiểm tra định mức xuất MOQ & Tồn kho khả dụng (Available = Physical - Reserved) từ TV4.",
        "3. Hệ thống thẩm định Hạn mức bảo lãnh: Trách nhiệm cũ + Lệnh mới - Ký quỹ <= Hạn mức cho phép.",
        "4. Kế toán kho ký duyệt Lệnh xuất -> Lưu CSDL trạng thái RESERVED, tăng tồn giữ chỗ reservedQuantity.",
        "5. Phát thông điệp mạng WebSocket EVENT_STOCK_RESERVED sang máy trạm Thủ kho (TV4).",
        "6. Thủ kho in Picking List theo vị trí ngăn kệ Bin, đến đúng vị trí lấy đồng hồ về bàn đóng gói.",
        "7. Nhân viên dùng Camera quét từng mã Serial -> Đối soát chéo: đúng SKU, trạng thái HANG_MOI, không quét trùng.",
        "8. Quét đủ 100% -> Thủ kho bấm 'Xác nhận xuất kho' -> Kích hoạt Database Transaction: Đổi Serial sang DISPATCHED, trừ tồn vật lý, giải phóng tồn giữ chỗ, ghi nhận bàn giao cho chi nhánh.",
        "9. Phát thông điệp WebSocket EVENT_DISPATCH_COMPLETED sang TV4 (cập nhật tồn) và TV5 (Kế toán quản trị).",
        "10. In Phiếu xuất kho kiêm Biên bản bàn giao hàng hóa khổ A4 đính kèm bảng kê 100% Serial định danh."
    ]
    add_box("QUY TRÌNH TUẦN TỰ ĐIỀU PHỐI VÀ XUẤT KHO 2 BƯỚC", seq_steps, bg="F0FDF4", title_color=C_GREEN)

    add_section_h2("5.3. Mô tả các Luồng dữ liệu chính & Khía cạnh Lập Trình Mạng (Network):")
    add_bullet_p("Đơn vị tiếp nhận -> NV Điều phối -> dialog_create_outbound_order -> DealerDao.getDealerById() -> Kiểm tra hạn mức bảo lãnh -> Ghi vào outbound_orders.", "DF-04 (Khởi tạo Lệnh điều phối xuất & Thẩm định bảo lãnh): ")
    add_bullet_p("Kế toán duyệt lệnh -> Chuyển RESERVED -> Tăng reservedQuantity trong Room DB -> Phát WebSocket EVENT_STOCK_RESERVED sang TV4 (Thủ kho).", "DF-05 (Khóa Giữ Chỗ Tồn Kho & Broadcast Socket): ")
    add_bullet_p("NV Xuất kho quét Camera -> SerialDao.getSerialByNumber() -> Đối soát hợp lệ -> Chuyển DISPATCHED -> Trừ tồn vật lý trong ProductDao -> Cập nhật trách nhiệm trong DealerDao -> Phát Socket EVENT_DISPATCH_COMPLETED sang TV4 và TV5.", "DF-06 (Quét Camera Serial Đóng Kiện & Hoàn Tất Xuất): ")
    add_bullet_p("Chi nhánh gửi biên bản xác nhận nhận hàng an toàn -> Kế toán lập Phiếu giải phóng -> Lưu DealerReceiptEntity -> Giảm currentDebt -> Tự động mở rộng hạn mức khả dụng để kho tiếp tục điều phối xuất hàng.", "DF-07 (Lập Phiếu Giải Phóng Bảo Lãnh & Mở Rộng Hạn Mức): ")
    add_bullet_p("REST API Client (POST /api/v1/outbound/orders, POST /api/v1/outbound/dispatch, POST /api/v1/dealers/receipts) truyền tải dữ liệu chuẩn JSON Payload qua mạng LAN nội bộ kho, xác thực an toàn bằng JWT Bearer Token.", "Giao thức mạng áp dụng: ")

    # ---------------------------------------------------------
    # 6. THIẾT KẾ CƠ SỞ DỮ LIỆU CỐT LÕI
    # ---------------------------------------------------------
    add_section_h1("6. THIẾT KẾ CƠ SỞ DỮ LIỆU CỐT LÕI (ROOM DATABASE v5 & PHYSICAL SCHEMA)")

    align_db = {0: WD_ALIGN_PARAGRAPH.LEFT, 1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER}

    add_section_h2("6.1. Bảng 1: 'dealers' (Đơn vị tiếp nhận & Hạn mức bảo lãnh tài sản):")
    tbl_d1 = doc.add_table(rows=1, cols=6)
    tbl_d1.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_d1 = tbl_d1.rows[0]
    h_d1.cells[0].text = "Tên cột"; h_d1.cells[1].text = "Kiểu dữ liệu"; h_d1.cells[2].text = "Null"; h_d1.cells[3].text = "Default"; h_d1.cells[4].text = "Mô tả nghiệp vụ kho"; h_d1.cells[5].text = "Ràng buộc"
    format_row(h_d1, "1B365D", is_header=True)

    d1_rows = [
        ("dealerId", "VARCHAR(50)", "No", "Không", "Mã định danh đơn vị tiếp nhận (VD: DL-GALLE)", "PRIMARY KEY"),
        ("name", "VARCHAR(255)", "No", "Không", "Tên chi nhánh / Kho tiếp nhận hàng xuất", "NOT NULL"),
        ("tier", "VARCHAR(20)", "No", "'BRONZE'", "Phân hạng ưu tiên điều phối (VIP, SILVER, BRONZE)", "CHECK in ('VIP', 'SILVER', 'BRONZE')"),
        ("discountPercent", "DOUBLE", "No", "0.20", "Hệ số phân bổ ưu tiên điều chuyển tài sản", "0.0 <= discountPercent <= 0.50"),
        ("creditLimit", "DOUBLE", "No", "500000000.0", "Hạn mức bảo lãnh trách nhiệm tài sản tối đa (VNĐ)", "creditLimit >= 0"),
        ("currentDebt", "DOUBLE", "No", "0.0", "Giá trị tài sản đang lưu giữ chưa hoàn tất bàn giao", "currentDebt >= 0"),
        ("taxCode", "VARCHAR(20)", "No", "Không", "Mã số doanh nghiệp / Mã chi nhánh", "UNIQUE, NOT NULL"),
        ("status", "VARCHAR(20)", "No", "'ACTIVE'", "Trạng thái tiếp nhận điều phối của đơn vị", "CHECK in ('ACTIVE', 'LOCKED')")
    ]
    for r_data in d1_rows:
        row = tbl_d1.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_db)

    add_section_h2("6.2. Bảng 2: 'outbound_orders' (Lệnh điều phối xuất kho & Khóa giữ chỗ):")
    tbl_d2 = doc.add_table(rows=1, cols=6)
    tbl_d2.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_d2 = tbl_d2.rows[0]
    h_d2.cells[0].text = "Tên cột"; h_d2.cells[1].text = "Kiểu dữ liệu"; h_d2.cells[2].text = "Null"; h_d2.cells[3].text = "Default"; h_d2.cells[4].text = "Mô tả nghiệp vụ kho"; h_d2.cells[5].text = "Ràng buộc"
    format_row(h_d2, "1B365D", is_header=True)

    d2_rows = [
        ("orderCode", "VARCHAR(50)", "No", "Không", "Mã Lệnh điều phối xuất kho (VD: DS-2026-001)", "PRIMARY KEY"),
        ("dealerId", "VARCHAR(50)", "No", "Không", "Mã đơn vị tiếp nhận hàng xuất", "FOREIGN KEY -> dealers(dealerId)"),
        ("productCode", "VARCHAR(50)", "No", "Không", "Mã SKU sản phẩm đồng hồ yêu cầu xuất", "FOREIGN KEY -> products(productCode)"),
        ("unit", "VARCHAR(20)", "No", "'PIECE'", "Đơn vị tính lúc yêu cầu xuất", "CHECK in ('PIECE', 'BOX')"),
        ("quantity", "INT", "No", "1", "Số lượng yêu cầu theo ĐVT", "quantity > 0"),
        ("convertedQuantity", "INT", "No", "1", "Số lượng chiếc quy đổi khóa giữ chỗ trên kệ", "convertedQuantity >= moq"),
        ("totalAmount", "DOUBLE", "No", "0.0", "Tổng giá trị định giá tài sản lô hàng xuất (VNĐ)", "totalAmount >= 0"),
        ("depositAmount", "DOUBLE", "No", "0.0", "Giá trị ký quỹ bảo lãnh lưu chuyển (VNĐ)", "depositAmount >= 0"),
        ("remainingDebt", "DOUBLE", "No", "0.0", "Giá trị trách nhiệm bảo lãnh tài sản phát sinh", "remainingDebt >= 0"),
        ("status", "VARCHAR(20)", "No", "'RESERVED'", "Trạng thái lệnh xuất kho", "CHECK in ('PENDING', 'RESERVED', 'COMPLETED')")
    ]
    for r_data in d2_rows:
        row = tbl_d2.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_db)

    add_section_h2("6.3. Bảng 3: 'outbound_dispatches' (Phiếu xuất kho kiêm Biên bản bàn giao):")
    tbl_d3 = doc.add_table(rows=1, cols=6)
    tbl_d3.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_d3 = tbl_d3.rows[0]
    h_d3.cells[0].text = "Tên cột"; h_d3.cells[1].text = "Kiểu dữ liệu"; h_d3.cells[2].text = "Null"; h_d3.cells[3].text = "Default"; h_d3.cells[4].text = "Mô tả nghiệp vụ kho"; h_d3.cells[5].text = "Ràng buộc"
    format_row(h_d3, "1B365D", is_header=True)

    d3_rows = [
        ("dispatchCode", "VARCHAR(50)", "No", "Không", "Mã phiếu xuất kho bàn giao (VD: PX-2026-001)", "PRIMARY KEY"),
        ("orderCode", "VARCHAR(50)", "Yes", "NULL", "Mã Lệnh điều phối xuất liên kết", "FOREIGN KEY -> outbound_orders"),
        ("dealerId", "VARCHAR(50)", "Yes", "NULL", "Mã đơn vị tiếp nhận hàng", "FOREIGN KEY -> dealers"),
        ("dispatchType", "VARCHAR(30)", "No", "'XUAT_DOI_TAC'", "Mục đích xuất (Tiếp nhận / Bảo hành / Hủy)", "CHECK in ('XUAT_DOI_TAC', 'BAO_HANH', 'TIEU_HUY')"),
        ("totalCostPrice", "DOUBLE", "No", "0.0", "Tổng giá vốn đích danh các Serial xuất (VNĐ)", "totalCostPrice >= 0"),
        ("status", "VARCHAR(20)", "No", "'COMPLETED'", "Trạng thái phiếu xuất kho bàn giao", "CHECK in ('PACKING', 'COMPLETED')")
    ]
    for r_data in d3_rows:
        row = tbl_d3.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_db)

    add_section_h2("6.4. Bảng 4: 'dispatch_serials' (Bảng kê chi tiết Serial đã quét xuất):")
    tbl_d4 = doc.add_table(rows=1, cols=6)
    tbl_d4.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_d4 = tbl_d4.rows[0]
    h_d4.cells[0].text = "Tên cột"; h_d4.cells[1].text = "Kiểu dữ liệu"; h_d4.cells[2].text = "Null"; h_d4.cells[3].text = "Default"; h_d4.cells[4].text = "Mô tả nghiệp vụ kho"; h_d4.cells[5].text = "Ràng buộc"
    format_row(h_d4, "1B365D", is_header=True)

    d4_rows = [
        ("id", "INT", "No", "Tự tăng", "Mã định danh bản ghi chi tiết xuất", "PRIMARY KEY AUTOINCREMENT"),
        ("dispatchCode", "VARCHAR(50)", "No", "Không", "Mã phiếu xuất kho bàn giao", "FOREIGN KEY -> outbound_dispatches"),
        ("serialNumber", "VARCHAR(100)", "No", "Không", "Mã Serial định danh chiếc đồng hồ được xuất", "FOREIGN KEY -> serials"),
        ("unitCostPrice", "DOUBLE", "No", "0.0", "Giá vốn đích danh tại thời điểm xuất kho", "unitCostPrice >= 0"),
        ("dispatchedPrice", "DOUBLE", "No", "0.0", "Giá trị định giá bảo hiểm của chiếc đồng hồ", "dispatchedPrice >= 0")
    ]
    for r_data in d4_rows:
        row = tbl_d4.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_db)

    add_section_h2("6.5. Bảng 5: 'dealer_receipts' (Phiếu xác nhận bàn giao & Giải phóng bảo lãnh):")
    tbl_d5 = doc.add_table(rows=1, cols=6)
    tbl_d5.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_d5 = tbl_d5.rows[0]
    h_d5.cells[0].text = "Tên cột"; h_d5.cells[1].text = "Kiểu dữ liệu"; h_d5.cells[2].text = "Null"; h_d5.cells[3].text = "Default"; h_d5.cells[4].text = "Mô tả nghiệp vụ kho"; h_d5.cells[5].text = "Ràng buộc"
    format_row(h_d5, "1B365D", is_header=True)

    d5_rows = [
        ("receiptId", "VARCHAR(50)", "No", "Không", "Mã chứng từ giải phóng bảo lãnh (VD: PT-2026-001)", "PRIMARY KEY"),
        ("dealerId", "VARCHAR(50)", "No", "Không", "Mã đơn vị tiếp nhận hoàn tất đối soát", "FOREIGN KEY -> dealers(dealerId)"),
        ("amount", "DOUBLE", "No", "0.0", "Giá trị tài sản đã bàn giao an toàn được giải phóng", "amount > 0"),
        ("paymentMethod", "VARCHAR(30)", "No", "'CHUYEN_KHOAN'", "Phương thức xác thực (Biên bản bàn giao / UNC)", "CHECK in ('CHUYEN_KHOAN', 'TIEN_MAT')"),
        ("referenceDoc", "VARCHAR(100)", "No", "Không", "Số chứng từ tham chiếu (Biên bản bàn giao / Mã UNC)", "NOT NULL"),
        ("date", "VARCHAR(50)", "No", "Không", "Ngày giờ xác nhận hoàn tất thủ tục bàn giao", "NOT NULL")
    ]
    for r_data in d5_rows:
        row = tbl_d5.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_db)

    add_section_h2("6.6. Sơ đồ Mối quan hệ Cơ sở dữ liệu Cốt lõi (ERD Relationships):")
    erd_lines = [
        "[dealers]            1 ──── N  [outbound_orders]   (Một đơn vị nhận tiếp nhận nhiều lệnh xuất)",
        "[dealers]            1 ──── N  [dealer_receipts]   (Một đơn vị có nhiều chứng từ giải phóng bảo lãnh)",
        "[outbound_orders]    1 ──── 1  [outbound_dispatches] (Một lệnh xuất sinh 1 biên bản bàn giao)",
        "[outbound_dispatches]1 ──── N  [dispatch_serials]  (Một phiếu xuất chứa nhiều Serial quét thực tế)",
        "[dispatch_serials]   N ──── 1  [serials]           (Mỗi chi tiết xuất liên kết đúng 1 mã Serial)",
        "[products]           1 ──── N  [outbound_orders]   (Một mẫu đồng hồ được yêu cầu trong nhiều lệnh xuất)",
        "[users]              1 ──── N  [outbound_orders]   (Một nhân viên tạo và xử lý nhiều lệnh xuất kho)"
    ]
    add_code_box("QUAN HỆ BẢNG CƠ SỞ DỮ LIỆU PHÂN HỆ 3", erd_lines)

    # ---------------------------------------------------------
    # 7. KẾ HOẠCH & TIẾN ĐỘ CÁ NHÂN
    # ---------------------------------------------------------
    add_section_h1("7. KẾ HOẠCH & TIẾN ĐỘ CÁ NHÂN CỦA TÔ ĐỨC THẢO (TV3)")

    add_section_h2("7.1. Phân công 5 vai trò thành viên nhóm 5 AE Siêu Nhân:")
    add_bullet_p("Quản trị hệ thống, kiến trúc MVVM Core, Room DB v5, RBAC 5 Roles, Master Data Luxury Horology.", "Phan Bá Hải Bình (TV1 - Trưởng nhóm): ")
    add_bullet_p("Tiếp nhận đồng hồ Inbound từ đơn vị sản xuất, quy đổi Thùng -> Chiếc, nạp dải Serial và phân bổ giá vốn đích danh.", "Nguyễn Đắc Quân (TV2): ")
    add_bullet_p("Quản lý Đơn vị tiếp nhận, kiểm soát hạn mức bảo lãnh tài sản, cơ chế khóa giữ chỗ kệ (Reservation), xuất kho 2 bước quét Camera Serial và giải phóng hạn mức bảo lãnh.", "Tô Đức Thảo (TV3 - Tác giả): ")
    add_bullet_p("Thủ kho điều hành quản lý tồn kho đa đơn vị, 3 kho chất lượng (Mới/Trưng bày/Lỗi), sơ đồ kệ Bin K1/K2, kiểm kê và Sổ Thẻ kho.", "Võ Công Tâm (TV4): ")
    add_bullet_p("Kế toán kho phụ trách Executive Dashboard KPI thời gian thực, MPAndroidChart giá trị xuất nhập 6 tháng, 9 báo cáo chuyên sâu và dòng tiền luân chuyển kho.", "Trần Công Tú (TV5): ")

    add_section_h2("7.2. Kế hoạch 4 giai đoạn hoàn thành đồ án:")
    add_bullet_p("Khảo sát bài toán điều phối kho chứa đồng hồ cao cấp, tiếp nhận kiến trúc Core MVVM và Room DB từ Trưởng nhóm Phan Bá Hải Bình.", "Giai đoạn 1 (1.5 tuần): ", bullet="- ")
    add_bullet_p("Phát triển độc lập phân hệ Điều phối Xuất kho & Đơn vị tiếp nhận trên nhánh Git feature/tv3-outbound-dealer.", "Giai đoạn 2 (2.5 tuần): ", bullet="- ")
    add_bullet_p("Ghép nối code (Merge PR), kiểm thử chéo luồng dữ liệu liên phân hệ với TV4 (Tồn kho) và TV5 (Kế toán).", "Giai đoạn 3 (1.0 tuần): ", bullet="- ")
    add_bullet_p("Hoàn thiện báo cáo chuyên đề cá nhân nộp Trưởng nhóm và chuẩn bị kịch bản Vấn đáp bảo vệ đồ án.", "Giai đoạn 4 (1.0 tuần): ", bullet="- ")

    add_section_h2("7.3. Bảng theo dõi tiến độ cá nhân của Tô Đức Thảo:")
    tbl_prog = doc.add_table(rows=1, cols=4)
    tbl_prog.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_p = tbl_prog.rows[0]
    h_p.cells[0].text = "Khoảng thời gian"
    h_p.cells[1].text = "Nội dung công việc thực hiện"
    h_p.cells[2].text = "Kết quả bàn giao"
    h_p.cells[3].text = "Tiến độ"
    format_row(h_p, "1B365D", is_header=True)

    prog_data = [
        ("01/10 - 08/10/2026", "Khảo sát bài toán điều phối kho chứa đồng hồ xa xỉ, phân tích rủi ro xuất âm kho và vượt hạn mức bảo lãnh tài sản.", "Tài liệu phân tích Outbound Logistics", "100% Hoàn thành"),
        ("09/10 - 18/10/2026", "Thiết kế CSDL Room DB: DealerEntity, OutboundOrderEntity, DealerReceiptEntity và các DAO.", "Merge vào ChronoVaultDatabase v5", "100% Hoàn thành"),
        ("19/10 - 28/10/2026", "Lập trình Android UI: fragment_outbound_order, dialog_create_order, dialog_dispatch_order.", "Hoàn thành UI, ViewBinding & Adapters", "100% Hoàn thành"),
        ("29/10 - 05/11/2026", "Lập trình Logic: Thuật toán Reservation Engine, Hạn mức bảo lãnh tài sản, quét Camera đối soát Serial đóng kiện.", "Hoàn thiện OutboundOrderFragment.kt", "100% Hoàn thành"),
        ("06/11 - 10/11/2026", "Viết bộ Test Cases Galle Watch chuẩn, soạn thảo Báo cáo cá nhân Word và Markdown, chuẩn bị vấn đáp bảo vệ.", "Hoàn tất BaoCao_TV3_ToDucThao.docx", "100% Hoàn thành")
    ]
    align_prog = {0: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER}
    for r_data in prog_data:
        row = tbl_prog.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_prog)

    # ---------------------------------------------------------
    # PHỤ LỤC A: BẢNG KỊCH BẢN KIỂM THỬ (TEST CASES)
    # ---------------------------------------------------------
    add_section_h1("PHỤ LỤC A: BẢNG KỊCH BẢN KIỂM THỬ (TEST CASES) & DỮ LIỆU MẪU CHUẨN")
    add_bullet_p("Chi nhánh Galle Watch Việt Nam (Mã: DL-GALLE, Hạng: VIP, Hạn mức bảo lãnh: 3.000.000.000 VNĐ, Trách nhiệm tài sản đang giữ: 1.800.000.000 VNĐ).", "Đơn vị tiếp nhận thử nghiệm: ")
    add_bullet_p("Rolex Submariner Date 41mm (Mã: RLX-126610LN, Định giá tài sản bảo hiểm: 350.000.000 VNĐ/chiếc, Tồn vật lý trên kệ: 14 chiếc).", "Sản phẩm thử nghiệm: ")

    tbl_tc = doc.add_table(rows=1, cols=5)
    tbl_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_tc = tbl_tc.rows[0]
    h_tc.cells[0].text = "Mã TC"; h_tc.cells[1].text = "Tên Kịch Bản"; h_tc.cells[2].text = "Dữ Liệu Vào (Input)"; h_tc.cells[3].text = "Kết Quả Mong Đợi / Thực Tế"; h_tc.cells[4].text = "Trạng Thái"
    format_row(h_tc, "1B365D", is_header=True)

    tc_data = [
        ("TC-01", "Kiểm thử tạo Lệnh xuất vượt Hạn mức bảo lãnh tài sản", 
         "Chọn Galle Watch (Trách nhiệm hiện tại 1.8 tỷ, Hạn mức 3.0 tỷ). Yêu cầu xuất điều phối 5 chiếc Rolex Submariner (Định giá tài sản 350tr/c). Tổng giá trị lô hàng xuất: 1.75 tỷ. Hệ số điều chuyển: định giá bảo lãnh 1.3125 tỷ. Tiền ký quỹ: 0đ. Trách nhiệm dự kiến: 1.8 tỷ + 1.3125 tỷ = 3.112.500.000 VNĐ.",
         "Hệ thống phát hiện 3.112.500.000 > 3.000.000.000 VNĐ. Khóa nút Duyệt lệnh xuất, hiển thị cảnh báo đỏ vượt hạn mức bảo lãnh tài sản chi nhánh 112.5 triệu VNĐ.", 
         "ĐẠT (PASS)"),
        ("TC-02", "Tạo Lệnh xuất hợp lệ & Khóa Giữ chỗ trên kệ (Reservation)", 
         "Chọn Galle Watch. Yêu cầu xuất điều phối 2 chiếc Rolex Submariner (Định giá 350tr/c). Tổng giá trị: 700tr. Giá trị bảo lãnh: 525tr. Ký quỹ bảo lãnh: 150tr. Trách nhiệm mới: 375tr. Dư bảo lãnh dự kiến: 1.8 tỷ + 375tr = 2.175.000.000 VNĐ (<= 3.0 tỷ).",
         "Duyệt Lệnh xuất thành công mã DS-2026-001 (RESERVED). Tồn giữ chỗ tăng thêm 2. Tồn khả dụng giảm từ 14 xuống 12 chiếc. Phát WebSocket EVENT_STOCK_RESERVED sang TV4.", 
         "ĐẠT (PASS)"),
        ("TC-03", "Chặn quét trùng lặp mã Serial lúc đóng kiện xuất kho", 
         "Tại lệnh DS-2026-001, dùng Camera quét Serial RLX-SUB-2026-001 lần thứ 1 (hợp lệ). Cố tình quét tiếp mã RLX-SUB-2026-001 lần thứ 2 vào cùng kiện hàng đóng xuất.",
         "Ứng dụng rung cảnh báo, phát âm thanh lỗi và hiển thị thông báo: 'Mã Serial RLX-SUB-2026-001 đã được quét rồi!'. Không cho phép nạp trùng lặp mã Serial.", 
         "ĐẠT (PASS)"),
        ("TC-04", "Chặn Serial sai SKU hoặc Hàng lỗi kỹ thuật", 
         "Tại lệnh DS-2026-001 (Rolex), cố tình quét mã Serial của đồng hồ Omega (OMG-SPEED-2026-001) hoặc quét mã Serial có trạng thái DEFECTIVE (kho lỗi).",
         "Ứng dụng từ chối nhận diện, báo lỗi: 'Serial không khớp với mã SKU của Lệnh xuất hoặc đang ở trạng thái lỗi kỹ thuật cách ly'. Chặn hoàn toàn việc xuất nhầm hàng.", 
         "ĐẠT (PASS)"),
        ("TC-05", "Xác nhận đối soát bàn giao & Giải phóng Hạn mức bảo lãnh", 
         "Chi nhánh Galle Watch gửi Biên bản xác nhận nhận hàng an toàn kèm ký quỹ 200.000.000 VNĐ (Mã chứng từ: UNC-VCB-88391). Trách nhiệm tài sản ban đầu: 1.800.000.000 VNĐ.",
         "Tạo chứng từ PT-2026-001. Giá trị tài sản đang giữ của Galle Watch giảm từ 1.8 tỷ xuống còn 1.6 tỷ VNĐ. Hạn mức bảo lãnh xuất hàng khả dụng tăng thêm 200 triệu để tiếp tục điều phối.", 
         "ĐẠT (PASS)"),
        ("TC-06", "Chặn quét nhầm Serial khác lô nhập / sai giá vốn / sai vị trí kệ",
         "Lệnh DS-2026-001 chỉ định xuất chiếc Rolex Lô 1 (Serial: RLX-SUB-2026-001, Giá vốn 285tr tại Kệ K1-A02-B03). Nhân viên đến nhầm Két VIP-02 lấy chiếc Rolex Lô 2 (Serial: RLX-SUB-2026-002, Giá vốn 295tr) và dùng Camera quét vào kiện đóng xuất.",
         "Ứng dụng rung cảnh báo đỏ, phát âm thanh lỗi và hiển thị: 'Serial RLX-SUB-2026-002 thuộc Lô 2 (Giá vốn 295tr tại Két VIP-02), không khớp với danh sách Lô cần xuất trong Picking List!'. Chặn hoàn toàn việc xuất sai lô và sai giá vốn.",
         "ĐẠT (PASS)")
    ]
    align_tc = {0: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER}
    for r_data in tc_data:
        row = tbl_tc.add_row()
        for idx, text in enumerate(r_data):
            row.cells[idx].text = text
        format_row(row, "FFFFFF", font_size=7.5, align_cols=align_tc)
        row.cells[4].paragraphs[0].runs[0].font.bold = True
        row.cells[4].paragraphs[0].runs[0].font.color.rgb = C_GREEN

    # ---------------------------------------------------------
    # PHỤ LỤC B: BỘ CÂU HỎI VẤN ĐÁP BẢO VỆ
    # ---------------------------------------------------------
    add_section_h1("PHỤ LỤC B: BỘ CÂU HỎI VẤN ĐÁP BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG")

    qa_list = [
        ("Câu hỏi 1: Đề tài này là Hệ Thống Quản Lý Kho (WMS), vậy phân hệ của em đóng vai trò gì và tại sao khẳng định kho không có mua bán?",
         [
             "Trả lời:",
             "Thưa thầy/cô, hệ thống ChronoVault WMS của nhóm em thuần túy là Kho Tổng Lưu Trữ & Điều Phối (Warehouse Storage Hub), hoàn toàn không có hoạt động mua bán, không có quầy thu ngân POS và không có nhân viên kinh doanh bán hàng.",
             "Nhiệm vụ của kho chỉ gồm hai đầu mối khép kín: Nhập hàng vào (Inbound) và Xuất hàng ra (Outbound).",
             "Phân hệ của em phụ trách đầu ra: Trung tâm Điều phối & Tác nghiệp Xuất kho (Outbound Fulfillment). Khi các chi nhánh, showroom hoặc trung tâm bảo hành gửi Yêu cầu xuất hàng, nhiệm vụ của em là:",
             "1. Thẩm định Hạn mức bảo lãnh trách nhiệm tài sản của đơn vị nhận để tránh thất thoát tài sản tổng kho.",
             "2. Khóa giữ chỗ tồn kho (Inventory Reservation Engine) ngay trên kệ để ngăn chặn triệt để tình trạng xuất âm kho.",
             "3. Soạn hàng và dùng Camera quét đối soát 100% Serial để đảm bảo xuất đúng mẫu mã, đúng chất lượng hàng mới nguyên seal, chặn hàng lỗi.",
             "4. Đóng kiện niêm phong và in Phiếu xuất kho kiêm Biên bản bàn giao hàng hóa A4.",
             "Toàn bộ là tác nghiệp kho vận kỹ thuật phục vụ lưu thông và bảo quản tài sản, tuyệt đối không phải là nghiệp vụ bán hàng."
         ]),

        ("Câu hỏi 2: Nếu kho không mua bán, tại sao trong CSDL lại có các trường giá trị (totalAmount), hạn mức (creditLimit) và phiếu thu (dealer_receipts)?",
         [
             "Trả lời:",
             "Thưa thầy/cô, đây là đặc thù bắt buộc của ngành Quản lý Kho Đồng Hồ Xa Xỉ (Luxury Horology Warehouse):",
             "1. Mỗi chiếc đồng hồ Rolex, Patek Philippe có giá trị từ vài trăm triệu đến hàng tỷ đồng. Do đó, các trường unitPrice hay totalAmount trong hệ thống thuần túy là 'Giá trị định giá tài sản lưu kho theo bảo hiểm' (Asset Valuation) để xác định giá trị bảo hiểm hàng hóa khi lưu kho và vận chuyển, cũng như quy trách nhiệm bồi thường nếu làm mất mát hoặc trầy xước.",
             "2. Trường creditLimit và currentDebt là 'Hạn mức bảo lãnh trách nhiệm giữ tài sản' (Asset Custody Limit): Một chi nhánh đang giữ 1.8 tỷ đồng giá trị hàng hóa chưa đối soát hoàn tất bàn giao thì không được phép tiếp nhận thêm quá hạn mức bảo lãnh 3.0 tỷ, nhằm kiểm soát rủi ro tài sản cho Tổng kho.",
             "3. Bảng dealer_receipts là 'Biên bản xác nhận hoàn tất giao nhận & Giải phóng hạn mức bảo lãnh' (Asset Delivery Clearance Voucher): Khi chi nhánh nhận hàng an toàn vào tủ két, chứng từ này giải phóng số dư trách nhiệm tài sản để mở rộng hạn mức cho các đợt điều phối tiếp theo. Hoàn toàn không phải là tiền bán hàng hay doanh thu."
         ]),

        ("Câu hỏi 3: Cơ chế Giữ chỗ tồn kho (Inventory Reservation Engine) bảo vệ kho khỏi tình trạng Xuất âm kho như thế nào?",
         [
             "Trả lời:",
             "Thưa thầy/cô, trong một kho chứa lớn, có nhiều nhân viên điều phối cùng làm việc đồng thời. Nếu kho chỉ còn 3 chiếc Rolex, khi 2 nhân viên cùng nhận 2 Lệnh xuất kho (mỗi lệnh 3 chiếc), nếu không có cơ chế giữ chỗ, cả 2 đều nhìn thấy tồn vật lý là 3 chiếc nên đều duyệt lệnh. Kết quả là xảy ra 'Xuất âm kho' — kho không có đủ hàng thực tế trên kệ để đóng kiện xuất giao.",
             "Với thuật toán Reservation của em, ngay khi Lệnh 1 được duyệt, Room DB lập tức tăng reservedQuantity = 3, làm cho Tồn khả dụng (Available = Physical - Reserved) tụt ngay về 0.",
             "Lệnh 2 khi kiểm tra tồn khả dụng sẽ bị hệ thống chặn lại ngay lập tức, triệt tiêu hoàn toàn rủi ro tranh chấp hàng xuất."
         ]),

        ("Câu hỏi 4: Làm sao đảm bảo nhân viên đóng gói không xuất nhầm chiếc đồng hồ đang bị lỗi kỹ thuật hoặc hàng trưng bày khỏi kho?",
         [
             "Trả lời:",
             "Thưa thầy/cô, trong quá trình quét xuất kho bằng Camera, ứng dụng của em thực hiện truy vấn thời gian thực vào bảng serials trong Room Database.",
             "Tại đây, mỗi mã Serial đều gắn liền với 2 trường dữ liệu bắt buộc: productCode (phải khớp với Lệnh xuất) và quality/status.",
             "Nếu chiếc đồng hồ đang có trạng thái là DEFECTIVE (hàng trầy xước, hấp hơi ở kho lỗi C-01) hoặc DISPLAY (hàng mẫu mở hộp trưng bày), ứng dụng sẽ lập tức rung cảnh báo, phát âm thanh lỗi, viền đỏ màn hình và chặn hoàn toàn nút 'Xác nhận xuất kho', đảm bảo 100% sản phẩm rời khỏi kho là hàng mới nguyên seal."
         ]),

        ("Câu hỏi 5: Phân hệ của em đóng góp gì cho khía cạnh Lập Trình Mạng (Network Communication) của toàn đồ án?",
         [
             "Trả lời:",
             "Thưa thầy/cô, phân hệ của em là trung tâm trao đổi thông điệp mạng thời gian thực:",
             "1. Khi em duyệt Lệnh điều phối xuất kho và khóa giữ chỗ, ứng dụng phát thông điệp WebSocket EVENT_STOCK_RESERVED giúp màn hình của Thủ kho (TV4) lập tức cập nhật giảm tồn khả dụng mà không cần tải lại.",
             "2. Khi em quét xuất kho hoàn tất, thông điệp EVENT_DISPATCH_COMPLETED được truyền sang phân hệ TV4 (để trừ tồn kho vật lý) và phân hệ Kế toán TV5 (để ghi nhận biến động giá trị tài sản lưu kho).",
             "3. Khi em lập Phiếu giải phóng bảo lãnh bàn giao, dữ liệu được đồng bộ trực tiếp sang Báo cáo luân chuyển của Kế toán.",
             "Toàn bộ các gói tin đều có định dạng chuẩn JSON và xác thực bảo mật JWT Bearer Token."
         ]),

        ("Câu hỏi 6: Nếu muốn xuất kho một lô đồng hồ mà giá vốn mỗi chiếc khác nhau, làm sao phân hệ của em biết vị trí của từng chiếc ở đâu để lấy đúng và tránh bị nhầm lẫn hoặc xuất sai lô hàng?",
         [
             "Trả lời:",
             "Thưa thầy/cô, hệ thống giải quyết bài toán này qua 3 chốt chặn kỹ thuật chặt chẽ:",
             "1. Quản trị tọa độ vị trí 5 cấp (currentLocation): Mỗi chiếc đồng hồ khi nhập kho đều được phân hệ TV4 gán một tọa độ lưu trữ cụ thể trong bảng serials (Khu vực -> Dãy kệ -> Tầng -> Ngăn Bin hoặc Két sắt an toàn).",
             "2. Sinh Phiếu soạn hàng thông minh (Smart Picking List): Khi Lệnh xuất được duyệt giữ chỗ, phân hệ của em tự động sinh Picking List chỉ định đích danh mã Serial cần xuất theo thứ tự FIFO (hoặc theo lô chỉ định) kèm theo chính xác tọa độ ngăn kệ và giá vốn đích danh của từng chiếc, giúp nhân viên đi thẳng đến đúng ngăn kệ rút hàng mà không cần tìm kiếm.",
             "3. Camera quét đối soát 100% tại bàn đóng gói (Chốt chặn chống sai sót): Khi mang đồng hồ về bàn đóng gói, nhân viên bắt buộc phải quét mã Serial bằng Camera điện thoại. Dù hộp bên ngoài giống hệt nhau, nhưng nếu nhân viên lấy nhầm chiếc của lô khác (khác giá vốn) hoặc nhầm hàng trưng bày/lỗi, ứng dụng sẽ rung cảnh báo, phát âm thanh lỗi và khóa chặn nút xuất kho ngay lập tức, đảm bảo 100% xuất đúng chiếc, đúng giá vốn và đúng vị trí."
         ])
    ]

    for q, a_items in qa_list:
        add_box(q, a_items, bg="F8FAFC", title_color=C_NAVY)

    # Chữ ký người lập báo cáo - khoảng cách vừa vặn, chuẩn học thuật
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(14)
    p_sign.paragraph_format.space_after = Pt(2)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_s1 = p_sign.add_run("Đà Nẵng, ngày 10 tháng 11 năm 2026\n")
    r_s1.font.name = "Arial"; r_s1.font.size = Pt(9); r_s1.font.italic = True
    r_s2 = p_sign.add_run("SINH VIÊN THỰC HIỆN BÁO CÁO\n\n")
    r_s2.font.name = "Arial"; r_s2.font.size = Pt(9.5); r_s2.font.bold = True; r_s2.font.color.rgb = C_NAVY
    r_s3 = p_sign.add_run("TÔ ĐỨC THẢO")
    r_s3.font.name = "Arial"; r_s3.font.size = Pt(10.5); r_s3.font.bold = True

    output_path = r"c:\LTM\LapTrinhMang_5AESiuNhan\Document\BaoCao_TV3_ToDucThao_DieuPhoi_XuatKho.docx"
    doc.save(output_path)
    print(f"Báo cáo Word đã được cập nhật thành công tại:\n  - {output_path}")

if __name__ == "__main__":
    build_thao_report()
