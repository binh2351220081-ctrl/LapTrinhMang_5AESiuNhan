# -*- coding: utf-8 -*-
"""
Script tạo file Word (.docx) Báo Cáo Phân Tích & Thiết Kế Hệ Thống Quản Lý Kho Đồng Hồ B2B
Dự án: ChronoVault B2B Wholesale Horology WMS
Nguồn đặc tả: phantichLTM.txt
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def generate_report():
    doc = Document()

    # -------------------------------------------------------------
    # 1. CẤU HÌNH TRANG VÀ LỀ KHỔ GIẤY A4
    # -------------------------------------------------------------
    section = doc.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Inches(8.27)   # A4 Width
    section.page_height = Inches(11.69) # A4 Height
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # Header & Footer
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "CHRONOVAULT B2B WMS • BÁO CÁO PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.style.font.name = "Arial"
    hp.style.font.size = Pt(8)
    hp.style.font.color.rgb = RGBColor(148, 163, 184)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Hệ Thống Quản Lý Kho Đồng Hồ B2B • Tài Liệu Đặc Tả Nghiệp Vụ & CSDL Chuẩn Hóa"
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    fp.style.font.name = "Arial"
    fp.style.font.size = Pt(8)
    fp.style.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH ĐỊNH DẠNG XML BẢNG & Ô
    # -------------------------------------------------------------
    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/></w:tblBorders>')
        tblPr.append(borders)

    def make_row_header(row):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    def make_row_cant_split(row):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    def set_cell_width(cell, width_dxa):
        tcPr = cell._tc.get_or_add_tcPr()
        tcW = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{width_dxa}" w:type="dxa"/>')
        tcPr.append(tcW)

    def add_callout(text, bold_prefix="", border_color="1B365D", bg_color="F1F5F9"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_width(cell, 9600)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=140)
        set_cell_background(cell, bg_color)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        if bold_prefix:
            r_bold = p.add_run(bold_prefix + " ")
            r_bold.font.name = "Arial"
            r_bold.font.size = Pt(9.5)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(27, 54, 93)
        r_txt = p.add_run(text)
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 2. TRANG BÌA BÁO CÁO CHUẨN
    # -------------------------------------------------------------
    cover_p = doc.add_paragraph()
    cover_p.paragraph_format.space_before = Pt(36)
    cover_p.paragraph_format.space_after = Pt(6)
    cover_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    r_inst = cover_p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO • KHOA CÔNG NGHỆ THÔNG TIN\n")
    r_inst.font.name = "Arial"; r_inst.font.size = Pt(11); r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(71, 85, 105)

    r_main_title = cover_p.add_run("BÁO CÁO PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG\nQUẢN LÝ KHO HÀNG HÓA CỬA HÀNG ĐỒNG HỒ\n")
    r_main_title.font.name = "Arial"; r_main_title.font.size = Pt(19); r_main_title.font.bold = True
    r_main_title.font.color.rgb = RGBColor(27, 54, 93) # Navy

    r_sub = cover_p.add_run("MÔ HÌNH PHÂN PHỐI BÁN SỈ B2B (WHOLESALE DISTRIBUTION)\n")
    r_sub.font.name = "Arial"; r_sub.font.size = Pt(12); r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(197, 155, 39) # Warm Gold

    desc_p = doc.add_paragraph()
    desc_p.paragraph_format.space_before = Pt(10)
    desc_p.paragraph_format.space_after = Pt(20)
    desc_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_desc = desc_p.add_run("Tài liệu đặc tả toàn diện: Cây phân rã WBS 5 thành viên, Thiết lập ban đầu, Danh mục I/O, Yêu cầu phi chức năng, Ma trận phân quyền RBAC, 4 Use Case cốt lõi, Cơ sở dữ liệu 23 bảng 3NF và Quy tắc toàn vẹn giao dịch.")
    r_desc.font.name = "Arial"; r_desc.font.size = Pt(9.5); r_desc.font.italic = True
    r_desc.font.color.rgb = RGBColor(100, 116, 139)

    # Bảng tóm tắt thông tin đề tài
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(info_table, color="CBD5E1", sz="4")
    
    meta_info = [
        ("Tên dự án:", "Hệ thống Quản lý Kho Hàng Hóa Cửa Hàng Đồng Hồ (ChronoVault B2B WMS)"),
        ("Phạm vi nghiệp vụ:", "Phân phối bán sỉ B2B Wholesale (Quản lý Serial đích danh, Giá vốn thực tế, Hạn mức tín dụng)"),
        ("Quy mô phân hệ:", "06 Phân hệ chức năng • Phân công độc lập và tích hợp cho nhóm 05 thành viên"),
        ("Mô hình dữ liệu:", "23 Bảng cơ sở dữ liệu quan hệ vật lý đạt chuẩn hóa 3NF"),
        ("Tài liệu tham chiếu:", "phantichLTM.txt (Đặc tả phân tích và thiết kế hệ thống chi tiết)"),
        ("Ngày lập / Phiên bản:", "Tháng 10/2026 • Phiên bản 2.0 Enterprise Release")
    ]
    col_widths_meta = [2400, 7200]
    for row_idx, (k, v) in enumerate(meta_info):
        row = info_table.rows[row_idx]
        make_row_cant_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        set_cell_width(c0, col_widths_meta[0])
        set_cell_width(c1, col_widths_meta[1])
        set_cell_margins(c0, top=70, bottom=70, left=120, right=120)
        set_cell_margins(c1, top=70, bottom=70, left=120, right=120)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        
        p0 = c0.paragraphs[0]; r0 = p0.add_run(k)
        r0.font.name = "Arial"; r0.font.size = Pt(9); r0.font.bold = True
        r0.font.color.rgb = RGBColor(30, 41, 59)
        
        p1 = c1.paragraphs[0]; r1 = p1.add_run(v)
        r1.font.name = "Arial"; r1.font.size = Pt(9)
        r1.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. PHẦN I: TỔNG QUAN ĐỀ TÀI & 4 NGUYÊN LÝ CỐT LÕI
    # -------------------------------------------------------------
    h1 = doc.add_heading("I. TỔNG QUAN KIẾN TRÚC & 4 NGUYÊN LÝ CỐT LÕI", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(8)
    for r in h1.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(6)
    r = p_intro.add_run("Hệ thống ChronoVault B2B được nghiên cứu và xây dựng nhằm giải quyết bài toán quản trị vận hành kho hàng hóa đồng hồ phân phối sỉ quy mô lớn. Không phục vụ mô hình bán lẻ nhỏ giọt (B2C), toàn bộ quy trình thiết kế bám sát ")
    r.font.name = "Arial"; r.font.size = Pt(10)
    r_b = p_intro.add_run("4 nguyên lý quản trị bắt buộc:")
    r_b.font.name = "Arial"; r_b.font.size = Pt(10); r_b.font.bold = True

    core_pillars = [
        ("1. Quản lý định danh Serial / Số máy đích danh 100%: ", "Mọi chiếc đồng hồ trong kho đều mang một mã Serial duy nhất do nhà sản xuất khắc chìm. Hệ thống truy vết vòng đời trọn vẹn: Lô hàng nhập NCC -> Vị trí ngăn kệ vật lý -> Đơn hàng sỉ B2B -> Khóa giữ chỗ -> Quét xuất đại lý -> Lịch sử tiếp nhận bảo hành, đổi trả."),
        ("2. Quản lý ĐVT đa cấp & Quy cách đóng gói sỉ: ", "Hỗ trợ lập chứng từ linh hoạt theo Thùng / Kiện / Hộp / Lô và tự động quy đổi ra Chiếc lẻ theo hệ số chuẩn (Ví dụ: 1 Thùng = 20 Chiếc). Kiểm soát nghiêm ngặt số lượng đặt hàng sỉ tối thiểu (MOQ) theo từng mẫu mã."),
        ("3. Cơ chế tính Giá vốn Đích danh (Specific Identification): ", "Không áp dụng phương pháp bình quân giản đơn cho tài sản giá trị cao. Mỗi mã Serial mang một giá vốn đích danh riêng biệt, được cộng dồn chi phí vận chuyển quốc tế, thuế quan và phí bảo hiểm phân bổ, đảm bảo tính toán lợi nhuận gộp chính xác 100%."),
        ("4. Chu trình Quản lý Công nợ B2B khép kín: ", "Tích hợp Phiếu Chi thanh toán tiền hàng NCC và Phiếu Thu tiền hàng/tiền cọc đại lý. Tự động kiểm tra hạn mức công nợ tối đa (Credit Limit) và kỳ hạn nợ (Net 15, Net 30), ngăn chặn duyệt đơn xuất khi đại lý có nợ quá hạn.")
    ]
    for b_title, b_desc in core_pillars:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15
        bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(b_title)
        r1.font.name = "Arial"; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = bp.add_run(b_desc)
        r2.font.name = "Arial"; r2.font.size = Pt(9.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.paragraph_format = None
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 3.2 Tác nhân nghiệp vụ và vai trò người dùng trong hệ thống
    h1_2 = doc.add_heading("Tác nhân nghiệp vụ và vai trò người dùng trong hệ thống", level=2)
    h1_2.paragraph_format.space_before = Pt(10)
    h1_2.paragraph_format.space_after = Pt(4)
    for r in h1_2.runs:
        r.font.name = "Arial"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    p_actors = doc.add_paragraph()
    p_actors.paragraph_format.line_spacing = 1.15
    p_actors.paragraph_format.space_after = Pt(6)
    r_act = p_actors.add_run("Hệ thống ChronoVault B2B WMS chuẩn hóa 5 tác nhân (actor) nội bộ, phân định ranh giới trách nhiệm và thẩm quyền độc lập nhằm kiểm soát chặt chẽ quy trình vận hành kho phân phối:")
    r_act.font.name = "Arial"; r_act.font.size = Pt(9.5)

    tbl_actors = doc.add_table(rows=6, cols=3)
    tbl_actors.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_actors, color="CBD5E1", sz="4")
    actor_headers = ["Tác Nhân (Actor)", "Trách Nhiệm Chính Trong Hệ Thống", "Giới Hạn Phân Quyền & Kiểm Soát Chéo"]
    actor_widths = [2400, 4200, 3000]

    r_ahdr = tbl_actors.rows[0]
    make_row_header(r_ahdr)
    for i, title in enumerate(actor_headers):
        c = r_ahdr.cells[i]
        set_cell_width(c, actor_widths[i])
        set_cell_margins(c, top=80, bottom=80, left=90, right=90)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.font.name = "Arial"; run.font.size = Pt(8.5); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    actors_info = [
        ("Quản trị hệ thống", "Quản trị tài khoản người dùng, ma trận phân quyền RBAC, cấu hình tham số hệ thống, giám sát nhật ký truy vết Audit Log, sao lưu và bảo mật dữ liệu.", "Không mặc định can thiệp hoặc tự duyệt các chứng từ nghiệp vụ nhập/xuất, thu/chi hay công nợ."),
        ("Chủ cửa hàng", "Giám sát toàn diện hoạt động vận hành qua Dashboard KPI thời gian thực; phê duyệt các ngoại lệ nghiệp vụ vượt ngưỡng (chi phí lô hàng lớn, vượt hạn mức tín dụng đại lý, cân bằng sai lệch kiểm kê giá trị cao).", "Không trực tiếp cấu hình kỹ thuật tài khoản/phân quyền và không xử lý các thao tác nhập xuất, kiểm đếm vật lý thường ngày."),
        ("Thủ kho (quản lý điều hành)", "Quản lý điều hành toàn diện kho hàng; quản trị sơ đồ vị trí kệ (Bin Location); tổ chức điều phối xuất/nhập; bảo quản an toàn hàng hóa; xác nhận giao nhận vật lý; chủ trì kiểm kê và duyệt cân bằng chênh lệch kho trong hạn mức.", "Không lập chứng từ thu chi tài chính, không can thiệp chính sách giá/hạn mức tín dụng và không tự duyệt sai lệch kiểm kê vượt ngưỡng thẩm quyền."),
        ("Nhân viên nhập - xuất kho", "Trực tiếp tác nghiệp hiện trường: lập phiếu nhập kho từ đơn PO, quét nạp dải Serial; lập đơn bán sỉ nháp, soạn hàng từ kệ, quét Serial đóng kiện xuất kho; tiếp nhận xử lý đổi trả và bảo hành.", "Không có quyền phê duyệt thu/chi tài chính, không tự duyệt đơn vượt hạn mức nợ và không tự ý điều chỉnh tồn kho."),
        ("Kế toán", "Kiểm soát dòng tiền và số liệu tài chính; phân bổ chi phí phụ trợ vào giá vốn đích danh của từng Serial; thẩm định hạn mức tín dụng; lập phiếu thu (cọc/tiền hàng), phiếu chi (NCC); đối soát chứng từ và Sổ Thẻ kho.", "Không thay thế Thủ kho (quản lý điều hành) trong việc xác nhận giao nhận vật lý; mọi ngoại lệ tài chính vượt ngưỡng bắt buộc phải trình Chủ cửa hàng phê duyệt.")
    ]

    for row_idx, rvals in enumerate(actors_info, start=1):
        row = tbl_actors.rows[row_idx]
        make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]
            set_cell_width(c, actor_widths[col_idx])
            set_cell_margins(c, top=65, bottom=65, left=90, right=90)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r_val = p.add_run(val)
                r_val.font.name = "Arial"; r_val.font.size = Pt(8.5); r_val.font.bold = True
                r_val.font.color.rgb = RGBColor(27, 54, 93)
            else:
                r_val = p.add_run(val)
                r_val.font.name = "Arial"; r_val.font.size = Pt(8.5)
                r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 4. PHẦN II: CÂY PHÂN RÃ CHỨC NĂNG & PHÂN CÔNG 5 THÀNH VIÊN
    # -------------------------------------------------------------
    h2 = doc.add_heading("II. PHÂN CÔNG TRÁCH NHIỆM 5 THÀNH VIÊN & CÂY PHÂN RÃ WBS", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(8)
    for r in h2.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    # Bảng phân công 5 thành viên
    tbl_tv = doc.add_table(rows=7, cols=4)
    tbl_tv.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_tv, color="CBD5E1", sz="4")

    tv_headers = ["Phân hệ", "Tên Phân Hệ Chức Năng", "Thành Viên Phụ Trách", "Nhiệm Vụ Nghiệp Vụ Cốt Lõi"]
    tv_widths = [1100, 2400, 1800, 4300]
    
    r_hdr = tbl_tv.rows[0]
    make_row_header(r_hdr)
    for i, title in enumerate(tv_headers):
        c = r_hdr.cells[i]
        set_cell_width(c, tv_widths[i])
        set_cell_margins(c, top=90, bottom=90, left=100, right=100)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.font.name = "Arial"; run.font.size = Pt(8.5); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    tv_data = [
        ("Module 1", "Quản lý Hàng hóa, Serial & ĐVT", "Thành viên 1", "Master thương hiệu, động cơ, mặt kính, dây đeo; cấu hình ĐVT quy đổi; MOQ; bảng giá sỉ; tra cứu vòng đời Serial."),
        ("Module 2", "Quản trị Hệ thống & Phân quyền", "Thành viên 1", "Quản lý tài khoản và ma trận RBAC cho 5 vai trò: Quản trị hệ thống, Chủ cửa hàng, Thủ kho (quản lý điều hành), Nhân viên nhập - xuất kho và Kế toán; thu hồi Token, Audit Log."),
        ("Module 3", "Đối tác NCC, Nhập kho & Chi phí", "Thành viên 2", "Hồ sơ NCC, đơn PO, lập phiếu nhập kho, quy đổi ĐVT, nạp Serial (quét/Excel), phân bổ chi phí lô vào giá vốn, trả hàng lỗi NCC, phiếu chi."),
        ("Module 4", "Khách sỉ, Bán sỉ & Xuất kho", "Thành viên 3", "Hồ sơ đại lý, phân hạng VIP/Bạc/Đồng, hạn mức nợ, đơn sỉ, thẩm định nợ, duyệt khóa giữ chỗ (Reserved), quét Serial xuất kho, phiếu thu."),
        ("Module 5", "Tồn kho, Vị trí Kệ & Kiểm kê", "Thành viên 4", "Giám sát tồn kho 3 trạng thái (Mới/Trưng bày/Lỗi), sơ đồ vị trí kệ (Bin), điều chuyển nội bộ, cảnh báo Min/Max, kiểm kê đối soát, Sổ Thẻ kho."),
        ("Module 6", "Báo cáo, Dòng tiền & Dashboard", "Thành viên 5", "KPI Cards thời gian thực, biểu đồ doanh thu/chi phí, sổ chi tiết công nợ 2 chiều, báo cáo dòng tiền thực, phân tích Dead Stock, lợi nhuận gộp B2B.")
    ]
    for row_idx, row_vals in enumerate(tv_data, start=1):
        row = tbl_tv.rows[row_idx]
        make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_vals):
            c = row.cells[col_idx]
            set_cell_width(c, tv_widths[col_idx])
            set_cell_margins(c, top=70, bottom=70, left=100, right=100)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 2):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val)
            r_val.font.name = "Arial"; r_val.font.size = Pt(8.5)
            if col_idx in (0, 2):
                r_val.font.bold = True
                r_val.font.color.rgb = RGBColor(27, 54, 93)
            elif col_idx == 1:
                r_val.font.bold = True
                r_val.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 5. PHẦN III: THIẾT LẬP BAN ĐẦU & CHÍNH SÁCH B2B
    # -------------------------------------------------------------
    h3 = doc.add_heading("III. THIẾT LẬP THAM SỐ BAN ĐẦU & CHÍNH SÁCH THƯƠNG MẠI B2B", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(8)
    for r in h3.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    p_set = doc.add_paragraph()
    p_set.paragraph_format.line_spacing = 1.15
    p_set.paragraph_format.space_after = Pt(4)
    r = p_set.add_run("Các tham số khởi tạo cấu hình hệ thống bao gồm:")
    r.font.name = "Arial"; r.font.size = Pt(10)

    settings_list = [
        ("Múi giờ & Đồng bộ hệ thống: ", "Thiết lập múi giờ UTC+7 (Asia/Ho_Chi_Minh), tự động đồng bộ thời gian máy chủ phục vụ ghi nhận thời điểm biến động xuất nhập và Audit Log."),
        ("Quy cách ĐVT cơ sở và ĐVT sỉ: ", "Đơn vị tính cơ sở là Chiếc / Cái. Đơn vị tính bán sỉ gồm Hộp (5 chiếc), Thùng carton (20 chiếc), Kiện (50 chiếc), Lô (100 chiếc) với hệ số quy đổi linh hoạt theo từng SKU."),
        ("Danh mục phân loại kỹ thuật: ", "Động cơ: Pin (Quartz), Cơ tự động (Automatic), Năng lượng ánh sáng (Solar/Eco-Drive). Kính: Sapphire chống trầy, Khoáng cường lực (Mineral), Hardlex. Dây: Thép 316L, Da thật, Cao su, NATO."),
        ("Cấu trúc địa chỉ ngăn kệ vật lý: ", "Phân khu (Khu A, Khu B, Khu Hàng Lỗi) -> Dãy kệ (01 - 10) -> Tầng kệ (1 - 4) -> Ngăn/Hộc chứa (Bin)."),
        ("Phương pháp tính giá vốn: ", "Áp dụng phương pháp Đích danh theo Serial Number (Specific Identification Method) cho 100% đồng hồ có quản lý Serial.")
    ]
    for stitle, sdesc in settings_list:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15; p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(stitle); r1.font.name = "Arial"; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = p.add_run(sdesc); r2.font.name = "Arial"; r2.font.size = Pt(9.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Bảng phân hạng đại lý B2B
    h3_sub = doc.add_heading("Bảng 2: Chính sách Thương Mại & Hạn Mức Tín Dụng Phân Cấp Đại Lý Sỉ", level=2)
    h3_sub.paragraph_format.space_before = Pt(8); h3_sub.paragraph_format.space_after = Pt(4)
    for r in h3_sub.runs:
        r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(30, 41, 59)

    tbl_b2b = doc.add_table(rows=4, cols=5)
    tbl_b2b.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b2b, color="CBD5E1", sz="4")

    b2b_headers = ["Hạng Đại Lý", "Tỷ Lệ Chiết Khấu Sỉ", "Hạn Mức Công Nợ Tối Đa", "Thời Hạn Nợ (Terms)", "Điều Kiện Áp Dụng"]
    b2b_widths = [1600, 1800, 2200, 1800, 2200]
    
    r_hdr = tbl_b2b.rows[0]
    make_row_header(r_hdr)
    for i, title in enumerate(b2b_headers):
        c = r_hdr.cells[i]
        set_cell_width(c, b2b_widths[i])
        set_cell_margins(c, top=80, bottom=80, left=90, right=90)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.font.name = "Arial"; run.font.size = Pt(8.5); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    b2b_data = [
        ("Hạng VIP", "30.00%", "1.000.000.000 VNĐ", "Net 30 (30 ngày)", "Doanh số sỉ >= 2 tỷ VNĐ/quý"),
        ("Hạng Bạc (Cấp 1)", "25.00%", "500.000.000 VNĐ", "Net 15 (15 ngày)", "Doanh số sỉ >= 500 triệu VNĐ/quý"),
        ("Hạng Đồng (Cấp 2)", "20.00%", "100.000.000 VNĐ", "Thanh toán ngay", "Đại lý mới tham gia mạng lưới")
    ]
    for row_idx, rvals in enumerate(b2b_data, start=1):
        row = tbl_b2b.rows[row_idx]
        make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]
            set_cell_width(c, b2b_widths[col_idx])
            set_cell_margins(c, top=65, bottom=65, left=90, right=90)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 1, 2, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val)
            r_val.font.name = "Arial"; r_val.font.size = Pt(8.5)
            if col_idx == 0:
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            elif col_idx in (1, 2):
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(197, 155, 39)
            else:
                r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_callout(
        "Quy tắc chặn tín dụng tự động: Nếu đại lý có bất kỳ hóa đơn nào quá thời hạn quy định (Net 15 / Net 30) hoặc số dư nợ mới vượt quá hạn mức công nợ tối đa, hệ thống sẽ tự động khóa nút duyệt đơn sỉ, bắt buộc đại lý thanh toán nợ cũ hoặc nộp tiền đặt cọc.",
        bold_prefix="QUY TẮC RỦI RO CÔNG NỢ B2B:"
    )

    # -------------------------------------------------------------
    # 6. PHẦN IV: MA TRẬN PHÂN QUYỀN TRUY CẬP (RBAC MATRIX)
    # -------------------------------------------------------------
    h4 = doc.add_heading("IV. MA TRẬN PHÂN QUYỀN VAI TRÒ NGƯỜI DÙNG (RBAC MATRIX)", level=1)
    h4.paragraph_format.space_before = Pt(14); h4.paragraph_format.space_after = Pt(8)
    for r in h4.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    tbl_rbac = doc.add_table(rows=15, cols=6)
    tbl_rbac.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_rbac, color="CBD5E1", sz="4")

    rbac_headers = ["Nghiệp Vụ Chức Năng", "Quản Trị Hệ Thống", "Chủ Cửa Hàng", "Thủ Kho (Quản Lý Điều Hành)", "Nhân Viên Nhập - Xuất Kho", "Kế Toán"]
    rbac_widths = [2600, 1400, 1500, 1600, 1600, 1300]

    r_hdr = tbl_rbac.rows[0]
    make_row_header(r_hdr)
    for i, title in enumerate(rbac_headers):
        c = r_hdr.cells[i]
        set_cell_width(c, rbac_widths[i])
        set_cell_margins(c, top=80, bottom=80, left=90, right=90)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.font.name = "Arial"; run.font.size = Pt(8.5); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    rbac_data = [
        ("Danh mục Master SKU, Thương hiệu, ĐVT", "Quản lý cấu hình", "Xem", "Chỉ xem", "Chỉ xem", "Chỉ xem"),
        ("Cấu hình Bảng giá sỉ & Giá vốn đích danh", "Không mặc định", "Xem", "Không có quyền", "Chỉ xem giá áp dụng", "Phân bổ / đối soát"),
        ("Quản trị Tài khoản, Role & Audit Log", "Toàn quyền", "Xem log hoạt động", "Không có quyền", "Không có quyền", "Xem log tài chính"),
        ("Hồ sơ Nhà cung cấp & Đơn đặt mua PO", "Cấu hình hệ thống", "Xem / duyệt ngoại lệ", "Xác nhận giao nhận", "Lập đề nghị / PO", "Thẩm định chứng từ"),
        ("Khởi tạo phiếu nhập & Quét/Nạp Serial", "Không thao tác thường ngày", "Giám sát", "Xác nhận nhận hàng", "Lập phiếu & quét Serial", "Kiểm tra số liệu"),
        ("Phân bổ chi phí lô hàng & Duyệt nhập kho", "Không mặc định", "Duyệt ngoại lệ vượt ngưỡng", "Xác nhận vật lý", "Không duyệt chi phí", "Phân bổ / đối soát"),
        ("Phiếu Chi thanh toán nợ Nhà cung cấp", "Không mặc định", "Duyệt vượt ngưỡng", "Không có quyền", "Không có quyền", "Lập phiếu / đối soát"),
        ("Hồ sơ Đại lý, Cấp bậc & Hạn mức nợ", "Không quản trị thương mại", "Duyệt hạn mức / ngoại lệ", "Không xem công nợ", "Cập nhật hồ sơ giao dịch", "Thẩm định hạn mức"),
        ("Khởi tạo Đơn bán sỉ & Duyệt giữ chỗ", "Không thao tác thường ngày", "Duyệt ngoại lệ tín dụng", "Xác nhận khả năng giao", "Lập đơn nháp / đề nghị giữ chỗ", "Thẩm định công nợ"),
        ("Quét Serial đóng kiện & Thực xuất kho sỉ", "Không thao tác thường ngày", "Giám sát", "Xác nhận xuất vật lý", "Soạn hàng / quét Serial", "Đối soát hóa đơn"),
        ("Phiếu Thu tiền bán sỉ & Thu nợ đại lý", "Không mặc định", "Xem báo cáo", "Không có quyền", "Không có quyền", "Lập phiếu thu / đối soát"),
        ("Sơ đồ Kệ & Điều chuyển nội bộ kho", "Không thao tác thường ngày", "Xem", "Quản lý vị trí / điều chuyển", "Đề nghị điều chuyển", "Xem vị trí"),
        ("Kiểm kê kho & Duyệt cân bằng thừa/thiếu", "Quản lý cấu hình", "Duyệt vượt ngưỡng", "Kiểm đếm / cân bằng trong ngưỡng", "Hỗ trợ quét / đếm", "Đối soát chứng từ"),
        ("Dashboard KPI, Báo cáo Lợi nhuận & Dòng tiền", "Xem log hệ thống", "Toàn quyền xem / xuất", "Xem tồn kho", "Xem tiến độ giao dịch", "Báo cáo tài chính")
    ]
    for row_idx, rvals in enumerate(rbac_data, start=1):
        row = tbl_rbac.rows[row_idx]
        make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]
            set_cell_width(c, rbac_widths[col_idx])
            set_cell_margins(c, top=65, bottom=65, left=90, right=90)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val)
            r_val.font.name = "Arial"; r_val.font.size = Pt(8.5)
            if "Toàn quyền" in val or "Duyệt" in val:
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            elif "Không có quyền" in val or "Không xem" in val:
                r_val.font.color.rgb = RGBColor(148, 163, 184)
            else:
                r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. PHẦN V: ĐẶC TẢ CÁC USE CASE NGHIỆP VỤ TRỌNG TÂM
    # -------------------------------------------------------------
    h5 = doc.add_heading("V. ĐẶC TẢ CÁC USE CASE NGHIỆP VỤ TRỌNG TÂM (CORE USE CASES)", level=1)
    h5.paragraph_format.space_before = Pt(14); h5.paragraph_format.space_after = Pt(8)
    for r in h5.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    use_cases = [
        {
            "code": "UC-01",
            "name": "Lập & Phê Duyệt Phiếu Nhập Kho Kèm Nạp Dải Serial & Phân Bổ Chi Phí",
            "actors": "Nhân viên nhập - xuất kho (Lập phiếu & Nạp Serial), Thủ kho (quản lý điều hành) (Xác nhận nhận hàng), Kế toán (Phân bổ / đối soát), Chủ cửa hàng (Duyệt ngoại lệ chi phí)",
            "pre": "Nhà cung cấp đã kích hoạt; Đơn đặt mua (PO) đã được phê duyệt; Mã SKU đã có trong Master Data.",
            "steps": [
                "1. Nhân viên nhập - xuất kho mở đơn PO, hệ thống tự động tải danh sách SKU, số lượng đặt và quy cách đóng gói (Thùng/Hộp).",
                "2. Nhân viên nhập - xuất kho nhập số lượng thùng thực nhận; hệ thống tự động nhân hệ số quy đổi ra tổng số chiếc lẻ (N chiếc).",
                "3. Nhân viên nhập - xuất kho nạp dải mã Serial bằng máy quét barcode hoặc import file Excel từ nhà sản xuất.",
                "4. Hệ thống kiểm tra đối soát 2 chiều: (a) Số lượng mã Serial quét = Tổng số chiếc sau quy đổi; (b) Toàn bộ mã Serial chưa từng tồn tại trong hệ thống (kiểm tra tính duy nhất).",
                "5. Nhân viên nhập - xuất kho lưu phiếu ở trạng thái 'Lưu nháp' (LUU_NHAP); Thủ kho (quản lý điều hành) xác nhận số lượng thực nhận và vị trí ngăn kệ.",
                "6. Kế toán tiếp nhận phiếu nháp, nhập chi phí phát sinh thực tế: cước vận chuyển, phí bốc dỡ, thuế hải quan.",
                "7. Hệ thống tự động tính chi phí phân bổ bình quân và cộng trực tiếp vào giá vốn đích danh của từng Serial: Giá vốn Serial = Đơn giá mua + (Tổng chi phí phân bổ / Tổng số chiếc lẻ).",
                "8. Kế toán hoàn tất đối soát; Thủ kho (quản lý điều hành) xác nhận nhập vật lý. Khoản chi hoặc chênh lệch vượt ngưỡng phải được Chủ cửa hàng duyệt trước khi ghi nhận; hệ thống lưu Serial, tăng tồn và ghi Sổ Thẻ kho."
            ],
            "exceptions": "Lệch số lượng Serial hoặc trùng lặp mã Serial -> Hệ thống cảnh báo đỏ và khóa nút phê duyệt cho đến khi được chỉnh sửa đúng."
        },
        {
            "code": "UC-02",
            "name": "Tạo Đơn Bán Sỉ & Duyệt Khóa Giữ Chỗ Tồn Kho (Reserved Allocation)",
            "actors": "Nhân viên nhập - xuất kho (Lập đơn nháp và xử lý xuất), Kế toán (Thẩm định công nợ / tiền cọc), Chủ cửa hàng (Duyệt ngoại lệ tín dụng), Thủ kho (quản lý điều hành) (Xác nhận giao nhận)",
            "pre": "Đại lý B2B có tài khoản kích hoạt; Sản phẩm đồng hồ có tồn kho khả dụng > 0.",
            "steps": [
                "1. Nhân viên nhập - xuất kho chọn đại lý đặt hàng và lập đơn bán sỉ nháp theo Thùng hoặc Chiếc lẻ.",
                "2. Hệ thống kiểm tra điều kiện sỉ: Số lượng đặt >= MOQ quy định (5 - 10 chiếc/mẫu); Số lượng đặt <= Tồn kho khả dụng (Tồn khả dụng = Tồn thực tế - Tồn đang giữ chỗ).",
                "3. Hệ thống tự động áp dụng giá sỉ và tỷ lệ chiết khấu theo cấp đại lý (VIP 30%, Bạc 25%, Đồng 20%) để tính Tổng giá trị đơn hàng.",
                "4. Hệ thống thẩm định hạn mức tín dụng: Dư nợ hiện tại + Giá trị đơn mới - Tiền cọc <= Hạn mức nợ cho phép, đồng thời kiểm tra đại lý không có hóa đơn quá hạn Net 15 / Net 30.",
                "5. Kế toán xác nhận hạn mức còn khả dụng; đơn được trình duyệt theo quy trình. Nếu vượt hạn mức, chỉ Chủ cửa hàng mới được duyệt ngoại lệ có ghi lý do. Sau khi duyệt, hệ thống tăng so_luong_giu_cho và giảm so_luong_kha_dung tại bảng tong_hop_ton_kho."
            ],
            "exceptions": "Không đủ tồn khả dụng hoặc vượt hạn mức nợ -> Hệ thống từ chối duyệt tự động, yêu cầu đại lý thanh toán nợ cũ hoặc nộp cọc bổ sung."
        },
        {
            "code": "UC-03",
            "name": "Quét Serial Đóng Kiện & Thực Xuất Kho Bán Sỉ",
            "actors": "Nhân viên nhập - xuất kho (Soạn hàng, quét Serial và lập phiếu xuất), Thủ kho (quản lý điều hành) (Xác nhận giao nhận vật lý)",
            "pre": "Đơn bán sỉ đã ở trạng thái DA_DUYET (đã giữ chỗ tồn kho thành công).",
            "steps": [
                "1. Nhân viên nhập - xuất kho mở đơn bán sỉ đã duyệt, tạo Phiếu xuất kho đóng hàng (phieu_xuat_kho).",
                "2. Nhân viên nhập - xuất kho đến vị trí ngăn kệ, quét từng mã Serial để đóng vào kiện hàng.",
                "3. Hệ thống đối soát thời gian thực: Serial quét vào phải thuộc đúng mã SKU trên đơn; Serial phải đang ở trạng thái HANG_MOI và TRONG_KHO; không bị quét trùng trong cùng kiện.",
                "4. Khi số lượng Serial quét đủ 100% số lượng theo đơn, hệ thống bật sáng nút 'Xác nhận xuất kho'.",
                "5. Thủ kho (quản lý điều hành) xác nhận giao nhận vật lý; hệ thống giảm tồn thực tế và giải phóng số lượng giữ chỗ; cập nhật Serial sang DA_BAN, ghi Thẻ kho (-) và in Phiếu xuất kho kiêm Biên bản bàn giao B2B khổ A4."
            ],
            "exceptions": "Quét sai SKU hoặc Serial đang ở Kho hàng lỗi -> Hệ thống phát âm thanh cảnh báo lỗi và từ chối ghi nhận mã đó."
        },
        {
            "code": "UC-04",
            "name": "Kiểm Kê Kho & Cân Bằng Sai Lệch Tồn Kho Theo Serial",
            "actors": "Thủ kho (quản lý điều hành) (Tổ chức và quét kiểm đếm), Nhân viên nhập - xuất kho (Hỗ trợ quét), Kế toán (Đối soát), Chủ cửa hàng (Duyệt chênh lệch vượt ngưỡng)",
            "pre": "Đợt kiểm kê được khởi tạo trên hệ thống (phieu_kiem_ke).",
            "steps": [
                "1. Thủ kho (quản lý điều hành) lập đợt kiểm kê, chọn phạm vi kiểm kê (Toàn bộ kho hoặc theo dãy kệ).",
                "2. Hệ thống tạm thời đóng băng hoạt động xuất/nhập tại khu vực kiểm kê đã chọn.",
                "3. Thủ kho (quản lý điều hành) cùng nhân viên đến từng ngăn kệ, dùng máy quét quét toàn bộ mã Serial thực tế hiện diện.",
                "4. Hệ thống tự động so khớp danh sách quét thực tế với số liệu trên hệ thống: phân loại Khớp đúng, Serial Thừa (thực tế có nhưng CSDL không ghi nhận tại kệ này), Serial Thiếu (CSDL báo có nhưng thực tế không tìm thấy).",
                "5. Xuất 'Biên bản đối soát kiểm kê' phân tích từng mã Serial sai lệch; Thủ kho (quản lý điều hành) và Kế toán xác minh nguyên nhân, ghi lý do điều chỉnh.",
                "6. Thủ kho (quản lý điều hành) cân bằng chênh lệch trong ngưỡng được giao; trường hợp vượt ngưỡng phải được Chủ cửa hàng phê duyệt trước khi cập nhật Serial, tồn kho và Sổ Thẻ kho."
            ],
            "exceptions": "Chênh lệch giá trị tài sản vượt ngưỡng quy định -> Yêu cầu Chủ cửa hàng phê duyệt trước khi cân bằng."
        }
    ]

    for uc in use_cases:
        h_uc = doc.add_heading(f"{uc['code']}: {uc['name']}", level=2)
        h_uc.paragraph_format.space_before = Pt(10); h_uc.paragraph_format.space_after = Pt(4)
        for r in h_uc.runs:
            r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

        tbl_uc = doc.add_table(rows=4, cols=2)
        tbl_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl_uc, color="CBD5E1", sz="4")
        set_cell_width(tbl_uc.rows[0].cells[0], 2200); set_cell_width(tbl_uc.rows[0].cells[1], 7400)
        
        meta_uc = [
            ("Tác nhân thực hiện:", uc["actors"]),
            ("Tiền điều kiện:", uc["pre"]),
            ("Luồng xử lý chính:", "\n".join(uc["steps"])),
            ("Xử lý ngoại lệ:", uc["exceptions"])
        ]
        for idx, (lbl, content) in enumerate(meta_uc):
            row = tbl_uc.rows[idx]
            make_row_cant_split(row)
            c0, c1 = row.cells[0], row.cells[1]
            set_cell_width(c0, 2200); set_cell_width(c1, 7400)
            set_cell_margins(c0, top=65, bottom=65, left=90, right=90)
            set_cell_margins(c1, top=65, bottom=65, left=90, right=90)
            set_cell_background(c0, "F8FAFC"); set_cell_background(c1, "FFFFFF")
            
            p0 = c0.paragraphs[0]; r0 = p0.add_run(lbl)
            r0.font.name = "Arial"; r0.font.size = Pt(8.5); r0.font.bold = True; r0.font.color.rgb = RGBColor(30, 41, 59)
            
            p1 = c1.paragraphs[0]; r1 = p1.add_run(content)
            r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.color.rgb = RGBColor(15, 23, 42)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. PHẦN VI: THIẾT KẾ CƠ SỞ DỮ LIỆU QUAN HỆ VẬT LÝ (23 BẢNG 3NF)
    # -------------------------------------------------------------
    h6 = doc.add_heading("VI. THIẾT KẾ CƠ SỞ DỮ LIỆU QUAN HỆ VẬT LÝ (23 BẢNG CHUẨN HÓA 3NF)", level=1)
    h6.paragraph_format.space_before = Pt(14); h6.paragraph_format.space_after = Pt(8)
    for r in h6.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    p_db = doc.add_paragraph()
    p_db.paragraph_format.line_spacing = 1.15; p_db.paragraph_format.space_after = Pt(6)
    r = p_db.add_run("Mô hình CSDL được thiết kế đạt chuẩn hóa 3NF, đáp ứng đầy đủ tính toàn vẹn tham chiếu (Referential Integrity), hỗ trợ lưu vết lịch sử giao dịch và phương pháp tính giá vốn đích danh:")
    r.font.name = "Arial"; r.font.size = Pt(10)

    tbl_db = doc.add_table(rows=24, cols=5)
    tbl_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_db, color="CBD5E1", sz="4")

    db_headers = ["STT", "Tên Bảng CSDL", "Khóa Chính (PK)", "Khóa Ngoại (FK) & Ràng Buộc", "Ý Nghĩa Nghiệp Vụ Quản Lý"]
    db_widths = [600, 2200, 1800, 2400, 2600]

    r_hdr = tbl_db.rows[0]
    make_row_header(r_hdr)
    for i, title in enumerate(db_headers):
        c = r_hdr.cells[i]
        set_cell_width(c, db_widths[i])
        set_cell_margins(c, top=80, bottom=80, left=90, right=90)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.font.name = "Arial"; run.font.size = Pt(8.5); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    tables_catalog = [
        ("1", "vai_tro", "ma_vai_tro", "QUAN_TRI_HE_THONG, CHU_CUA_HANG, THU_KHO, NHAN_VIEN_NHAP_XUAT, KE_TOAN", "Quản lý 5 vai trò chức năng trong hệ thống"),
        ("2", "nguoi_dung", "ma_nguoi_dung", "FK ma_vai_tro, UNIQUE ten_dang_nhap, email", "Tài khoản nhân viên, mật khẩu băm Bcrypt/Argon2"),
        ("3", "thuong_hieu", "ma_thuong_hieu", "Tên hãng, xuất xứ, cờ đang phân phối", "Danh mục hãng đồng hồ: Rolex, Seiko, Casio..."),
        ("4", "san_pham", "ma_san_pham", "FK ma_thuong_hieu, UNIQUE ma_vach", "Hồ sơ kỹ thuật Master SKU, động cơ, kính, dây"),
        ("5", "quy_doi_don_vi", "ma_quy_doi", "FK ma_san_pham (1 Thùng = N Chiếc)", "Cấu hình hệ số đóng gói quy đổi bán sỉ ra chiếc lẻ"),
        ("6", "vi_tri_ngan_ke", "ma_ngan_ke", "Phân khu, Dãy, Tầng, Hộc (Bin)", "Sơ đồ địa chỉ vật lý lưu trữ trong kho"),
        ("7", "tong_hop_ton_kho", "ma_tong_hop", "FK ma_san_pham, UNIQUE(SP, TrangThai)", "Quản lý tồn kho 3 trạng thái: Mới, Trưng bày, Lỗi"),
        ("8", "nha_cung_cap", "ma_nha_cung_cap", "UNIQUE ma_so_thue, du_no_hien_tai", "Hồ sơ NCC đồng hồ và theo dõi công nợ phải trả"),
        ("9", "dai_ly_b2b", "ma_dai_ly", "Cấp bậc VIP/Bạc/Đồng, han_muc_cong_no", "Hồ sơ đối tác sỉ, chính sách chiết khấu, hạn nợ"),
        ("10", "don_dat_hang_mua", "ma_don_mua_po", "FK ma_nha_cung_cap, FK ma_nguoi_tao", "Đơn đặt mua hàng từ nhà sản xuất (PO)"),
        ("11", "chi_tiet_don_mua", "ma_chi_tiet_don_mua", "FK ma_don_mua_po, FK ma_san_pham", "Chi tiết SKU và số lượng quy đổi đặt mua"),
        ("12", "phieu_nhap_kho", "ma_phieu_nhap", "FK ma_don_mua_po, FK ma_nha_cung_cap", "Chứng từ nghiệm thu nhập kho hàng hóa chính hãng"),
        ("13", "chi_tiet_phieu_nhap", "ma_chi_tiet_nhap", "FK ma_phieu_nhap, FK ma_san_pham", "Chi tiết số lượng và phân bổ chi phí lô vào từng chiếc"),
        ("14", "serial_san_pham", "so_serial", "FK san_pham, FK phieu_nhap, FK ngan_ke", "Bảng lõi: Định danh từng Serial, giá vốn đích danh"),
        ("15", "don_ban_si", "ma_don_ban_si", "FK ma_dai_ly, chiết khấu, tiền cọc", "Đơn bán sỉ, thẩm định công nợ và duyệt giữ chỗ"),
        ("16", "chi_tiet_don_ban_si", "ma_chi_tiet_don_si", "FK ma_don_ban_si, FK ma_san_pham", "Chi tiết SKU và số lượng chiếc khóa giữ chỗ"),
        ("17", "phieu_xuat_kho", "ma_phieu_xuat", "FK ma_don_ban_si, FK ma_dai_ly", "Phiếu xuất kho kiêm biên bản giao nhận sỉ B2B A4"),
        ("18", "chi_tiet_serial_xuat", "ma_chi_tiet_serial_xuat", "FK phieu_xuat, FK so_serial", "Danh sách Serial thực tế quét đóng kiện xuất bán"),
        ("19", "phieu_thu_tien", "ma_phieu_thu", "FK ma_dai_ly, FK don_ban_si (nếu cọc)", "Chứng từ thu tiền thanh toán nợ / cọc sỉ"),
        ("20", "phieu_chi_tien", "ma_phieu_chi", "FK ma_nha_cung_cap, FK phieu_nhap", "Chứng từ chi tiền trả nợ NCC và chi phí vận hành kho"),
        ("21", "phieu_kiem_ke", "ma_phieu_kiem_ke", "Phạm vi: Toàn kho, Kệ, Hãng", "Lệnh khởi tạo và quản lý đợt kiểm kê thực tế"),
        ("22", "chi_tiet_kiem_ke_serial", "ma_chi_tiet_kiem_ke", "FK phieu_kiem_ke, FK so_serial", "Đối soát Serial thực tế quét được vs dữ liệu CSDL"),
        ("23", "so_the_kho", "ma_the_kho", "FK san_pham, FK so_serial, ma_chung_tu", "Sổ Thẻ kho điện tử bất biến ghi mọi biến động +/-")
    ]

    for row_idx, rvals in enumerate(tables_catalog, start=1):
        row = tbl_db.rows[row_idx]
        make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]
            set_cell_width(c, db_widths[col_idx])
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 2):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val)
            r_val.font.name = "Arial"; r_val.font.size = Pt(8.5)
            if col_idx == 0:
                r_val.font.color.rgb = RGBColor(100, 116, 139)
            elif col_idx == 1:
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            elif col_idx == 2:
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(197, 155, 39)
            else:
                r_val.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. PHẦN VII: TOÀN VẸN GIAO DỊCH, CONCURRENCY & CÔNG THỨC TÀI CHÍNH
    # -------------------------------------------------------------
    h7 = doc.add_heading("VII. QUY TRÌNH TOÀN VẸN GIAO DỊCH & LOGIC ĐỒNG THỜI", level=1)
    h7.paragraph_format.space_before = Pt(14); h7.paragraph_format.space_after = Pt(8)
    for r in h7.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    # Vòng đời Serial
    h7_1 = doc.add_heading("1. Biểu đồ Chuyển dịch Vòng đời Serial (State Machine Logic)", level=2)
    h7_1.paragraph_format.space_before = Pt(8); h7_1.paragraph_format.space_after = Pt(4)
    for r in h7_1.runs:
        r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(30, 41, 59)

    sm_text = (
        "Luồng chuẩn xuất bán: Nhập kho (PN) -> TRONG_KHO (HANG_MOI) -> Khóa giữ chỗ (Duyệt đơn sỉ) -> Quét xuất kho (PX) -> DA_BAN.\n\n"
        "Luồng điều chuyển nội bộ: TRONG_KHO (HANG_MOI) -> TRONG_KHO (HANG_TRUNG_BAY) -> Xuất bán thanh lý (DA_BAN).\n\n"
        "Luồng xử lý lỗi kỹ thuật: TRONG_KHO (HANG_MOI / HANG_TRUNG_BAY) hoặc Đại lý bảo hành trả về -> TRONG_KHO (HANG_LOI) -> Xuất trả NCC (DA_TRA_NCC) hoặc Xuất tiêu hủy (DA_TIEU_HUY)."
    )
    add_callout(sm_text, bold_prefix="CÁC BƯỚC CHUYỂN DỊCH TRẠNG THÁI SERIAL:")

    # Khóa bi quan Concurrency
    h7_2 = doc.add_heading("2. Cơ Chế Khóa Bi Quan (Pessimistic Row-Level Locking) Chống Bán Trùng", level=2)
    h7_2.paragraph_format.space_before = Pt(10); h7_2.paragraph_format.space_after = Pt(4)
    for r in h7_2.runs:
        r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(30, 41, 59)

    lock_p = doc.add_paragraph()
    lock_p.paragraph_format.line_spacing = 1.15; lock_p.paragraph_format.space_after = Pt(4)
    r = lock_p.add_run("Để giải quyết bài toán nhiều nhân viên nhập - xuất kho cùng tác nghiệp và thủ kho (quản lý điều hành) cùng đối soát cho các mẫu đồng hồ hot số lượng có hạn, hệ thống kích hoạt khóa hàng ở mức cơ sở dữ liệu:")
    r.font.name = "Arial"; r.font.size = Pt(9.5)

    sql_steps = [
        ("Tại bước Duyệt đơn bán sỉ: ", "SELECT so_luong_kha_dung FROM tong_hop_ton_kho WHERE ma_san_pham = @sku AND trang_thai_chat_luong = 'HANG_MOI' FOR UPDATE;\nNếu khả dụng >= số lượng đặt, tăng ngay số lượng giữ chỗ và giảm tồn khả dụng trong cùng 1 Transaction."),
        ("Tại bước Quét Serial xuất kho: ", "SELECT so_serial, trang_thai_vong_doi FROM serial_san_pham WHERE so_serial = @serial FOR UPDATE;\nNếu trạng thái != 'TRONG_KHO', lập tức Rollback giao dịch và báo lỗi, triệt tiêu nguy cơ xuất âm kho hoặc bán trùng 1 chiếc đồng hồ cho 2 đơn khác nhau.")
    ]
    for stitle, scontent in sql_steps:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15; p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(stitle); r1.font.name = "Arial"; r1.font.size = Pt(9); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = p.add_run(scontent); r2.font.name = "Consolas"; r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Công thức tài chính
    h7_3 = doc.add_heading("3. Công Thức Tính Lợi Nhuận Gộp Đích Danh Trên Từng Giao Dịch B2B", level=2)
    h7_3.paragraph_format.space_before = Pt(10); h7_3.paragraph_format.space_after = Pt(4)
    for r in h7_3.runs:
        r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(30, 41, 59)

    fin_text = (
        "• Doanh thu thuần đơn sỉ = ∑ [Đơn giá sỉ niêm yết × (1 - Tỷ lệ chiết khấu đại lý)]\n"
        "• Tổng giá vốn hàng bán (COGS) = ∑ [Giá vốn đích danh(Serial_i)]\n"
        "• Lợi nhuận gộp B2B = Doanh thu thuần - Tổng COGS - Chi phí vận chuyển kho chịu\n\n"
        "Mô hình đảm bảo tính minh bạch tài chính tuyệt đối, bóc tách chính xác tỷ suất lợi nhuận trên từng chiếc đồng hồ và từng đại lý phân phối trong hệ thống."
    )
    add_callout(fin_text, bold_prefix="CÔNG THỨC TÀI CHÍNH:", border_color="C59B27", bg_color="FFFBEB")

    # -------------------------------------------------------------
    # 10. PHẦN VIII: YÊU CẦU PHI CHỨC NĂNG & KẾT LUẬN
    # -------------------------------------------------------------
    h8 = doc.add_heading("VIII. YÊU CẦU PHI CHỨC NĂNG & TIÊU CHUẨN KỸ THUẬT", level=1)
    h8.paragraph_format.space_before = Pt(14); h8.paragraph_format.space_after = Pt(8)
    for r in h8.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    nfr_items = [
        ("Hiệu năng xử lý dải Serial: ", "Hệ thống nạp, kiểm tra tính duy nhất và đối soát dải từ 500 đến 1.000 mã Serial từ file Excel nhà sản xuất hoặc súng quét barcode trong thời gian dưới 2.0 giây."),
        ("Tính bất biến dữ liệu (Immutability): ", "Dữ liệu Sổ Thẻ kho (so_the_kho) và Nhật ký kiểm toán (Audit Log) tuyệt đối không được phép chỉnh sửa hoặc xóa vật lý; mọi phát sinh thừa thiếu đều phải thông qua chứng từ điều chỉnh đối ứng."),
        ("Bảo mật xác thực & Token: ", "Mật khẩu người dùng được băm một chiều an toàn bằng thuật toán Bcrypt / Argon2. Quản lý phiên làm việc bằng cơ chế JWT Token hỗ trợ thu hồi từ xa ngay lập tức."),
        ("Tương thích thiết bị ngoại vi: ", "Giao diện bắt tự động sự kiện từ máy quét mã vạch Barcode/QR 1D/2D ở chế độ HID Keyboard Emulation. Các mẫu chứng từ in ấn phiếu nhập, xuất, biên bản bàn giao B2B được chuẩn hóa định dạng khổ giấy A4.")
    ]
    for ntitle, ndesc in nfr_items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15; p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(ntitle); r1.font.name = "Arial"; r1.font.size = Pt(9.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = p.add_run(ndesc); r2.font.name = "Arial"; r2.font.size = Pt(9.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

    # Khung chữ ký nghiệm thu
    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sig_table, color="FFFFFF", sz="0")
    sig_widths = [3200, 3200, 3200]
    
    r0 = sig_table.rows[0]
    titles_sig = ["GIẢNG VIÊN HƯỚNG DẪN", "TRƯỞNG NHÓM PHÁT TRIỂN", "ĐẠI DIỆN HỘI ĐỒNG THẨM ĐỊNH"]
    for i in range(3):
        c = r0.cells[i]
        set_cell_width(c, sig_widths[i])
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(titles_sig[i])
        run.font.name = "Arial"; run.font.size = Pt(9); run.font.bold = True; run.font.color.rgb = RGBColor(30, 41, 59)
        
    r1 = sig_table.rows[1]
    for i in range(3):
        c = r1.cells[i]
        set_cell_width(c, sig_widths[i])
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(45)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("(Ký và ghi rõ họ tên)")
        run.font.name = "Arial"; run.font.size = Pt(8.5); run.font.italic = True; run.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # LƯU FILE DOCUMENT .DOCX
    # -------------------------------------------------------------
    output_filename = "BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.docx"
    output_path = os.path.join(os.getcwd(), output_filename)
    doc.save(output_path)
    print(f"SUCCESS: Document created at {output_path}")

if __name__ == "__main__":
    generate_report()
