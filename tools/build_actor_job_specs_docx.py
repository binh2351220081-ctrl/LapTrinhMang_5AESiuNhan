# -*- coding: utf-8 -*-
"""
Script to generate: DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.docx
Bảng Đặc Tả Chi Tiết Nhiệm Vụ & Công Việc Cần Làm Của 5 Tác Nhân (Actor)
Trong Đề Tài: Hệ Thống Quản Lý Kho Đồng Hồ ChronoVault B2B Wholesale WMS
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcMar'):
            tcPr.remove(child)
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_cell_width(cell, width_dxa):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcW'):
            tcPr.remove(child)
    tcW = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{width_dxa}" w:type="dxa"/>')
    tcPr.append(tcW)

def set_table_borders(table, color="CBD5E1", sz="4"):
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def add_callout(doc, text, bold_prefix="", fill_hex="F8FAFC", border_color="1B365D"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cell_width(tbl.rows[0].cells[0], 9600)
    set_cell_margins(tbl.rows[0].cells[0], top=100, bottom=100, left=150, right=150)
    set_cell_background(tbl.rows[0].cells[0], fill_hex)
    
    cell = tbl.rows[0].cells[0]
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(0)
    if bold_prefix:
        r_bold = p.add_run(bold_prefix + " ")
        r_bold.font.name = "Arial"; r_bold.font.size = Pt(9); r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(27, 54, 93)
    r_txt = p.add_run(text)
    r_txt.font.name = "Arial"; r_txt.font.size = Pt(8.5); r_txt.font.italic = True
    r_txt.font.color.rgb = RGBColor(51, 65, 85)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_actor_document():
    doc = docx.Document()

    # 1. Page Margins (A4)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "CHRONOVAULT B2B WMS • BẢNG ĐẶC TẢ CÔNG VIỆC CHI TIẾT CỦA 5 TÁC NHÂN (ACTORS)"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.style.font.name = "Arial"; hp.style.font.size = Pt(8)
        hp.style.font.color.rgb = RGBColor(148, 163, 184)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Tài Liệu Đặc Tả Nghiệp Vụ & Phân Công Trách Nhiệm • Hệ Thống Quản Lý Kho B2B"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.style.font.name = "Arial"; fp.style.font.size = Pt(8)
        fp.style.font.color.rgb = RGBColor(148, 163, 184)

    # 2. Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(24)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_title.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO • KHOA CÔNG NGHỆ THÔNG TIN\n")
    r_uni.font.name = "Arial"; r_uni.font.size = Pt(10); r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(71, 85, 105)

    r_main = p_title.add_run("BẢNG ĐẶC TẢ CHI TIẾT CÔNG VIỆC CỦA TỪNG TÁC NHÂN (ACTOR)\n")
    r_main.font.name = "Arial"; r_main.font.size = Pt(17); r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(27, 54, 93)

    r_sub = p_title.add_run("HỆ THỐNG QUẢN LÝ KHO HÀNG HÓA CỬA HÀNG ĐỒNG HỒ (CHRONOVAULT B2B WMS)\n")
    r_sub.font.name = "Arial"; r_sub.font.size = Pt(11); r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(197, 155, 39)

    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_before = Pt(6)
    p_desc.paragraph_format.space_after = Pt(16)
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_desc.add_run("Tài liệu chuẩn hóa nhiệm vụ, quy trình tác nghiệp thường nhật, dữ liệu I/O, cơ chế kiểm soát chéo và ma trận trách nhiệm RACI cho 05 tác nhân nội bộ: Quản trị hệ thống, Chủ cửa hàng, Thủ kho (quản lý điều hành), Nhân viên nhập - xuất kho, Kế toán.")
    r_d.font.name = "Arial"; r_d.font.size = Pt(9); r_d.font.italic = True
    r_d.font.color.rgb = RGBColor(100, 116, 139)

    # Info summary table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="CBD5E1", sz="4")
    meta_data = [
        ("Tên dự án:", "Hệ thống Quản lý Kho Hàng Hóa Cửa Hàng Đồng Hồ (ChronoVault B2B WMS)"),
        ("Mô hình hoạt động:", "Phân phối phân phối đại lý B2B Wholesale (Định danh Serial 100%, Giá vốn đích danh, Hạn mức tín dụng)"),
        ("Nhóm tác nhân chuẩn hóa:", "05 Tác nhân nội bộ (Admin, Chủ cửa hàng, Thủ kho điều hành, NV nhập - xuất kho, Kế toán)"),
        ("Mục tiêu tài liệu:", "Quy định rõ ràng 'Ai làm việc gì, ở màn hình nào, dữ liệu đầu vào/ra là gì và bị ràng buộc bởi quyền hạn nào'"),
        ("Phiên bản / Ngày ban hành:", "Phiên bản 2.1 Enterprise Release • Tháng 11/2026")
    ]
    for r_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[r_idx]
        make_row_cant_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        set_cell_width(c0, 2400); set_cell_width(c1, 7200)
        set_cell_margins(c0, top=65, bottom=65, left=100, right=100)
        set_cell_margins(c1, top=65, bottom=65, left=100, right=100)
        set_cell_background(c0, "F8FAFC"); set_cell_background(c1, "FFFFFF")
        p0 = c0.paragraphs[0]; r0 = p0.add_run(k); r0.font.name = "Arial"; r0.font.size = Pt(8.5); r0.font.bold = True; r0.font.color.rgb = RGBColor(27, 54, 93)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(v); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()

    # =============================================================
    # PHẦN I: NGUYÊN TẮC PHÂN ĐỊNH TRÁCH NHIỆM & KIỂM SOÁT CHÉO
    # =============================================================
    h1 = doc.add_heading("I. TỔNG QUAN VỀ NGUYÊN TẮC PHÂN ĐỊNH TRÁCH NHIỆM (SEGREGATION OF DUTIES)", level=1)
    h1.paragraph_format.space_before = Pt(12); h1.paragraph_format.space_after = Pt(6)
    for r in h1.runs:
        r.font.name = "Arial"; r.font.size = Pt(12.5); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    p_p1 = doc.add_paragraph()
    p_p1.paragraph_format.line_spacing = 1.15; p_p1.paragraph_format.space_after = Pt(6)
    r = p_p1.add_run("Trong mô hình tổng kho phân phối đồng hồ cao cấp (B2B Wholesale), mỗi sản phẩm có giá trị tài sản rất lớn (từ hàng chục đến hàng trăm triệu đồng/chiếc) và mang một mã Serial độc bản. Do đó, hệ thống ChronoVault áp dụng triệt để ")
    r.font.name = "Arial"; r.font.size = Pt(9.5)
    r_b = p_p1.add_run("Nguyên tắc Kiểm soát Bốn Mắt (Four-Eyes Principle) và Bất kiêm nhiệm vụ (Segregation of Duties - SoD):")
    r_b.font.name = "Arial"; r_b.font.size = Pt(9.5); r_b.font.bold = True

    sod_points = [
        ("Tách biệt giữa Quản trị kỹ thuật và Tác nghiệp kinh doanh: ", "Quản trị hệ thống chỉ cấp phát tài khoản và cấu hình hệ thống, tuyệt đối không được tự ý lập phiếu nhập xuất hay can thiệp số liệu thu chi."),
        ("Tách biệt giữa Tác nghiệp kho và Xác nhận giao nhận vật lý: ", "Nhân viên nhập - xuất kho lập phiếu và cầm súng quét Serial, nhưng việc xác nhận niêm phong kiện hàng và ký bàn giao vật lý bắt buộc thuộc thẩm quyền của Thủ kho (quản lý điều hành)."),
        ("Tách biệt giữa Giao nhận vật lý và Hạch toán tài chính: ", "Thủ kho kiểm soát chiếc đồng hồ thực tế trên ngăn kệ, trong khi Kế toán kiểm soát dòng tiền, công nợ và chi phí phân bổ vào giá vốn. Kế toán không thể tự ký thay Thủ kho và ngược lại."),
        ("Tách biệt giữa Vận hành thường nhật và Phê duyệt ngoại lệ: ", "Chủ cửa hàng không tham gia thao tác giao dịch hàng ngày nhưng giữ quyền kiểm soát cao nhất để phê duyệt các tình huống vượt ngưỡng định mức (chi phí phụ trội, đại lý vượt hạn mức nợ, chênh lệch kiểm kê lớn).")
    ]
    for b_title, b_desc in sod_points:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15; bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(b_title); r1.font.name = "Arial"; r1.font.size = Pt(9); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = bp.add_run(b_desc); r2.font.name = "Arial"; r2.font.size = Pt(9); r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Overview Table of 5 Actors
    h1_sub = doc.add_heading("Bảng Tổng Hợp Vai Trò & Ranh Giới Thẩm Quyền 5 Tác Nhân", level=2)
    h1_sub.paragraph_format.space_before = Pt(8); h1_sub.paragraph_format.space_after = Pt(4)
    for r in h1_sub.runs:
        r.font.name = "Arial"; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    tbl_actors_ov = doc.add_table(rows=6, cols=3)
    tbl_actors_ov.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_actors_ov, color="CBD5E1", sz="4")
    a_headers = ["Tác Nhân (Actor)", "Phạm Vi Trách Nhiệm Cốt Lõi", "Ranh Giới Thẩm Quyền (Không Được Làm)"]
    a_widths = [2300, 4300, 3000]

    r_hdr = tbl_actors_ov.rows[0]; make_row_header(r_hdr)
    for i, t in enumerate(a_headers):
        c = r_hdr.cells[i]; set_cell_width(c, a_widths[i])
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(t); run.font.name = "Arial"; run.font.size = Pt(8.5); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    actors_ov_data = [
        ("1. Quản trị hệ thống", "Quản lý tài khoản người dùng, phân quyền vai trò RBAC, cấu hình tham số hệ thống, giám sát nhật ký Audit Log, thu hồi Token và bảo mật dữ liệu.", "Không thao tác hoặc phê duyệt các chứng từ nhập/xuất kho, phiếu thu/chi hay công nợ thương mại."),
        ("2. Chủ cửa hàng", "Giám sát Dashboard KPI điều hành (doanh thu, dòng tiền, nợ 2 chiều); phê duyệt ngoại lệ chi phí lớn, vượt hạn mức nợ đại lý và cân bằng kiểm kê giá trị cao.", "Không can thiệp cấu hình tài khoản kỹ thuật và không làm các thao tác nhập xuất, kiểm đếm kho thường nhật."),
        ("3. Thủ kho (quản lý điều hành)", "Điều hành toàn diện hoạt động kho; quản lý sơ đồ ngăn kệ (Bin); kiểm soát bảo quản an toàn; xác nhận giao nhận vật lý; chủ trì kiểm kê và cân bằng trong hạn mức.", "Không lập chứng từ thu/chi tiền, không can thiệp giá bán/hạn mức nợ đại lý và không tự duyệt sai lệch kiểm kê vượt ngưỡng."),
        ("4. Nhân viên nhập - xuất kho", "Tác nghiệp kho trực tiếp: lập phiếu nhập từ PO, quét nạp Serial; lập lệnh xuất đại lý nháp, soạn hàng, quét Serial đóng kiện xuất kho; tiếp nhận xử lý đổi trả và bảo hành.", "Không duyệt thu/chi, không tự duyệt đơn vượt hạn mức nợ của khách và không tự ý điều chỉnh tồn kho."),
        ("5. Kế toán", "Kiểm soát số liệu tài chính; phân bổ chi phí phụ trợ vào giá vốn đích danh của từng Serial; quản lý công nợ 2 chiều; lập phiếu thu/chi; đối soát Sổ Thẻ kho.", "Không thay thế Thủ kho xác nhận giao nhận vật lý; không tự duyệt các khoản nợ hoặc chi phí phát sinh vượt ngưỡng.")
    ]
    for row_idx, rvals in enumerate(actors_ov_data, start=1):
        row = tbl_actors_ov.rows[row_idx]; make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]; set_cell_width(c, a_widths[col_idx])
            set_cell_margins(c, top=65, bottom=65, left=80, right=80)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8.5); r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            else:
                r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8.5); r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # PHẦN II: CHI TIẾT CÔNG VIỆC CẦN LÀM CỦA TỪNG ACTOR
    # =============================================================
    h2 = doc.add_heading("II. ĐẶC TẢ CHI TIẾT CÁC CÔNG VIỆC CẦN LÀM CỦA TỪNG ACTOR", level=1)
    h2.paragraph_format.space_before = Pt(12); h2.paragraph_format.space_after = Pt(8)
    for r in h2.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    # -------------------------------------------------------------
    # ACTOR 1: QUẢN TRỊ HỆ THỐNG
    # -------------------------------------------------------------
    doc.add_heading("1. TÁC NHÂN: QUẢN TRỊ HỆ THỐNG (SYSTEM ADMINISTRATOR)", level=2)
    add_callout(
        doc,
        "Đảm bảo hệ thống vận hành liên tục, bảo mật tuyệt đối dữ liệu người dùng, quản lý vòng đời tài khoản và kiểm soát chặt chẽ phân quyền truy cập thông qua cơ chế phân quyền dựa trên vai trò (RBAC) và nhật ký kiểm toán bất biến (Audit Log).",
        bold_prefix="MỤC TIÊU VAI TRÒ:"
    )

    p_admin_intro = doc.add_paragraph()
    p_admin_intro.paragraph_format.line_spacing = 1.15; p_admin_intro.paragraph_format.space_after = Pt(4)
    r = p_admin_intro.add_run("Danh mục các công việc và nhiệm vụ chi tiết của Quản trị hệ thống:")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True

    admin_tasks = [
        ("Công việc 1.1: Khởi tạo và Quản lý Vòng đời Tài khoản Nhân viên: ", "Tiếp nhận thông tin nhân sự mới từ ban quản lý; tạo tài khoản người dùng mới (Username, Email, Họ tên, Số điện thoại); thiết lập mật khẩu ban đầu và yêu cầu đổi mật khẩu ở lần đăng nhập đầu tiên. Kích hoạt trạng thái ACTIVE hoặc khóa tài khoản (LOCK/INACTIVE) khi nhân viên nghỉ việc hoặc có cảnh báo vi phạm bảo mật."),
        ("Công việc 1.2: Cấu hình Vai trò & Thiết lập Ma trận Phân quyền (RBAC Matrix): ", "Khai báo và duy trì 5 vai trò người dùng chuẩn mực trong hệ thống. Gán các quyền thao tác mức nguyên tử (Xem [V], Tạo mới [C], Chỉnh sửa [E], Xóa [D], Duyệt [A], Tài chính [F], Kiểm kê [K]) cho từng phân hệ, ngăn chặn việc leo thang đặc quyền (Privilege Escalation)."),
        ("Công việc 1.3: Thu hồi Phiên Làm Việc Từ Xa (Session & Token Revocation): ", "Giám sát danh sách các phiên đăng nhập đang hoạt động; thực hiện thu hồi Token xác thực (JWT Revocation / Blacklist) tức thời đối với các phiên làm việc bất thường, thiết bị thất lạc hoặc khi tài khoản bị khóa."),
        ("Công việc 1.4: Giám sát Nhật ký Kiểm toán Hệ thống (Audit Trail Viewer): ", "Theo dõi toàn bộ nhật ký ghi vết của hệ thống: thời gian, người thực hiện, địa chỉ IP, hành động (Tạo, Sửa, Xóa, Duyệt, Xuất file) và đối tượng tác động. Định kỳ sao lưu dữ liệu Audit Log sang kho lưu trữ lạnh (Cold Storage) để phục vụ thanh tra compliance."),
        ("Công việc 1.5: Khai báo Danh mục Master Data & Cấu hình Tham số Toàn cục: ", "Khai báo danh mục thương hiệu đồng hồ (Rolex, Omega, Tissot, Seiko, Casio...), bộ sưu tập, chất liệu vỏ/kính, kiểu động cơ; cấu hình ĐVT cơ bản (Chiếc lẻ), ĐVT đóng gói xuất kho (Thùng/Kiện) và hệ số quy đổi đóng gói (ví dụ: 1 Thùng = 10 Chiếc). Thiết lập cờ bắt buộc quản lý mã Serial."),
        ("Công việc 1.6: Quản trị Cơ sở Dữ liệu & Sao lưu Định kỳ (Database Backup & Maintenance): ", "Thiết lập lịch sao lưu tự động cho 23 bảng cơ sở dữ liệu quan hệ (Hàng ngày / Hàng tuần); kiểm tra tính toàn vẹn của các bảng chỉ mục (Index) trên các trường tra cứu tần suất cao như `so_serial`, `ma_san_pham`, `ma_dai_ly`.")
    ]
    for t_title, t_desc in admin_tasks:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15; bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(t_title); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = bp.add_run(t_desc); r2.font.name = "Arial"; r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    # Admin Task Summary Table
    tbl_adm = doc.add_table(rows=7, cols=5)
    tbl_adm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_adm, color="CBD5E1", sz="4")
    th_widths = [1600, 1400, 2600, 2000, 2000]
    th_headers = ["Đầu Việc Cần Làm", "Tần Suất", "Dữ Liệu Đầu Vào (Input)", "Dữ Liệu Đầu Ra (Output)", "Quy Tắc Ràng Buộc"]
    
    r_hdr = tbl_adm.rows[0]; make_row_header(r_hdr)
    for i, title in enumerate(th_headers):
        c = r_hdr.cells[i]; set_cell_width(c, th_widths[i])
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title); run.font.name = "Arial"; run.font.size = Pt(8); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    adm_table_data = [
        ("Quản lý tài khoản User", "Khi có biến động nhân sự", "Họ tên, email, SĐT, vai trò chỉ định", "User ID, mật khẩu băm Bcrypt, cờ Active", "Email và Username duy nhất 100%"),
        ("Thiết lập RBAC Matrix", "Định kỳ / khi đổi quy trình", "Danh mục Role, danh mục Module", "Bản đồ quyền truy cập (Permissions JSON)", "Không cấp quyền duyệt tài chính cho Admin"),
        ("Thu hồi Token phiên", "Khi có sự cố rủi ro", "User ID, Device ID nghi vấn", "Token Blacklist, Buộc đăng xuất", "Ngắt kết nối ngay lập tức (<1s)"),
        ("Giám sát Audit Trail", "Hàng ngày", "Khoảng thời gian, Action, IP lọc", "Báo cáo lịch sử biến động, cảnh báo xâm nhập", "Dữ liệu log bất biến, không thể sửa/xóa"),
        ("Master Data & Quy đổi ĐVT", "Khi có sản phẩm / hãng mới", "SKU, Barcode, Hãng, ĐVT, Hệ số", "Hồ sơ sản phẩm chuẩn, Bảng quy đổi ĐVT", "Hệ số quy đổi là số nguyên dương >= 1"),
        ("Sao lưu & Bảo trì CSDL", "Hàng ngày (tự động 00:00)", "Snapshot 23 bảng vật lý", "File nén Dump SQL (.sql/.dump) mã hóa", "Lưu trữ tối thiểu 30 bản sao lưu gần nhất")
    ]
    for row_idx, rvals in enumerate(adm_table_data, start=1):
        row = tbl_adm.rows[row_idx]; make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]; set_cell_width(c, th_widths[col_idx])
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 1): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8)
            if col_idx == 0: r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            else: r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACTOR 2: CHỦ CỬA HÀNG (STORE OWNER)
    # -------------------------------------------------------------
    doc.add_heading("2. TÁC NHÂN: CHỦ CỬA HÀNG (STORE OWNER / BAN ĐIỀU HÀNH)", level=2)
    add_callout(
        doc,
        "Giám sát bức tranh toàn cảnh về sức khỏe tài chính và vận hành kho thông qua Dashboard KPI thời gian thực; đóng vai trò 'chốt chặn cuối cùng' phê duyệt các ngoại lệ nghiệp vụ có giá trị rủi ro cao vượt ngưỡng thẩm quyền thông thường.",
        bold_prefix="MỤC TIÊU VAI TRÒ:"
    )

    p_owner_intro = doc.add_paragraph()
    p_owner_intro.paragraph_format.line_spacing = 1.15; p_owner_intro.paragraph_format.space_after = Pt(4)
    r = p_owner_intro.add_run("Danh mục các công việc và nhiệm vụ chi tiết của Chủ cửa hàng:")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True

    owner_tasks = [
        ("Công việc 2.1: Giám sát Chỉ số Điều hành Thời Gian Thực (Executive Dashboard): ", "Theo dõi trực quan 5 thẻ chỉ số cốt lõi: Tổng giá trị tồn kho đích danh, Doanh số xuất kho đại lý trong kỳ, Tỷ lệ nợ đại lý quá hạn, Tồn kho khả dụng và Tỷ lệ tiếp nhận trả hàng đại lý. Đọc biểu đồ trực quan dòng tiền và xu hướng nhập/xuất để điều tiết chiến lược kinh doanh."),
        ("Công việc 2.2: Phê duyệt Ngoại lệ Hạn mức Tín dụng & Đơn Xuất Kho Đại Lý (Credit Override Approval): ", "Khi hệ thống tự động khóa nút duyệt lệnh xuất kho đại lý do Đại lý vượt hạn mức nợ (Credit Limit) hoặc có hóa đơn quá hạn (Net 15/Net 30), Chủ cửa hàng là người duy nhất có thẩm quyền xem xét uy tín đại lý, kiểm tra lý do và ký phê duyệt ngoại lệ (Override Approval) kèm ghi chú trách nhiệm."),
        ("Công việc 2.3: Phê duyệt Chi Phí Nhập Kho Phụ Trội Vượt Ngưỡng: ", "Xem xét và phê duyệt các khoản chi phụ trợ (cước bay quốc tế, phí hải quan, lưu kho bến bãi) có giá trị phát sinh vượt quá định mức ngân sách (ví dụ: vượt quá 10% giá trị hợp đồng mua), đảm bảo giá vốn hàng bán không bị đội lên bất hợp lý."),
        ("Công việc 2.4: Phê duyệt Xử lý Chênh lệch Kiểm kê Giá trị Cao (Inventory Discrepancy Approval): ", "Tiếp nhận 'Biên bản đối soát kiểm kê' từ Thủ kho và Kế toán khi phát hiện sai lệch số lượng hoặc mất mát mã Serial có giá trị vượt hạn mức phân quyền của Thủ kho (ví dụ: chênh lệch > 20 triệu VNĐ hoặc mất đồng hồ xa xỉ). Phê duyệt quyết định cân bằng kho và chỉ đạo truy cứu trách nhiệm."),
        ("Công việc 2.5: Phê duyệt Xuất trả Hàng lỗi Giá trị lớn & Xuất Tiêu hủy: ", "Phê duyệt các phiếu xuất trả lô đồng hồ lỗi cho Nhà cung cấp chính hãng và phê duyệt biên bản xuất tiêu hủy (Discard Stock) đối với các sản phẩm hỏng hóc nghiêm trọng không thể phục hồi."),
        ("Công việc 2.6: Phân tích Báo cáo Chiến lược Doanh nghiệp: ", "Định kỳ kết xuất và phân tích 3 báo cáo tài chính quản trị chuyên sâu: (1) Báo cáo Lợi nhuận gộp B2B đích danh theo từng đại lý và mẫu đồng hồ; (2) Báo cáo Hàng chậm luân chuyển (Dead Stock > 90 ngày) để chỉ đạo xả hàng thanh lý; (3) Báo cáo Sổ chi tiết công nợ 2 chiều và Dòng tiền thuần (Cashflow).")
    ]
    for t_title, t_desc in owner_tasks:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15; bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(t_title); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = bp.add_run(t_desc); r2.font.name = "Arial"; r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    # Owner Task Summary Table
    tbl_own = doc.add_table(rows=7, cols=5)
    tbl_own.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_own, color="CBD5E1", sz="4")
    
    r_hdr = tbl_own.rows[0]; make_row_header(r_hdr)
    for i, title in enumerate(th_headers):
        c = r_hdr.cells[i]; set_cell_width(c, th_widths[i])
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title); run.font.name = "Arial"; run.font.size = Pt(8); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    own_table_data = [
        ("Giám sát Dashboard KPI", "Hàng ngày / Thời gian thực", "Dữ liệu tổng hợp từ 4 phân hệ", "Quyết định điều hành tồn kho & tín dụng", "Số liệu cập nhật thời gian thực"),
        ("Duyệt ngoại lệ tín dụng đại lý", "Khi phát sinh đơn vượt nợ", "Đơn hàng xuất đại lý, Lịch sử nợ đại lý", "Lệnh duyệt ngoại lệ (Status: DA_DUYET)", "Bắt buộc ghi nhận lý do vào Audit Log"),
        ("Duyệt chi phí phụ trội lô", "Khi có lô hàng nhập phát sinh lớn", "Phiếu nhập nháp, chứng từ cước/thuế", "Lệnh duyệt hạch toán chi phí", "Khoản chi phụ trợ > 10% giá trị hợp đồng"),
        ("Duyệt chênh lệch kiểm kê", "Sau mỗi đợt kiểm kê lớn", "Biên bản đối soát kiểm kê Serial", "Lệnh cân bằng kho (Adjust Stock)", "Áp dụng khi sai lệch vượt ngưỡng thẩm quyền"),
        ("Duyệt trả hàng NCC / Hủy", "Khi phát sinh hàng lỗi máy/vỡ", "Biên bản giám định lỗi kỹ thuật", "Phiếu xuất trả NCC / Lệnh tiêu hủy", "Có chữ ký xác nhận của kỹ thuật & thủ kho"),
        ("Phân tích báo cáo Dead Stock", "Định kỳ hàng tháng / quý", "Báo cáo tuổi kho Aging Inventory", "Kế hoạch khuyến mãi / Giảm giá phân phối đại lý", "Nhận diện mẫu đồng hồ tồn kho > 90 ngày")
    ]
    for row_idx, rvals in enumerate(own_table_data, start=1):
        row = tbl_own.rows[row_idx]; make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]; set_cell_width(c, th_widths[col_idx])
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 1): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8)
            if col_idx == 0: r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            else: r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACTOR 3: THỦ KHO (QUẢN LÝ ĐIỀU HÀNH)
    # -------------------------------------------------------------
    doc.add_heading("3. TÁC NHÂN: THỦ KHO (QUẢN LÝ ĐIỀU HÀNH)", level=2)
    add_callout(
        doc,
        "Chịu trách nhiệm toàn diện về công tác quản lý điều hành kho bãi, bảo quản an toàn tài sản hàng hóa, tổ chức sơ đồ vị trí kệ (Bin Location), xác nhận giao nhận vật lý và chủ trì công tác kiểm kê đối soát Serial.",
        bold_prefix="MỤC TIÊU VAI TRÒ:"
    )

    p_wh_intro = doc.add_paragraph()
    p_wh_intro.paragraph_format.line_spacing = 1.15; p_wh_intro.paragraph_format.space_after = Pt(4)
    r = p_wh_intro.add_run("Danh mục các công việc và nhiệm vụ chi tiết của Thủ kho (quản lý điều hành):")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True

    wh_tasks = [
        ("Công việc 3.1: Quản trị Sơ đồ Vị trí Ngăn Kệ Vật lý (Warehouse Bin Management): ", "Thiết lập và quản lý danh mục địa chỉ kệ lưu trữ trong kho theo cấu trúc phân cấp chuẩn: Phân Khu (Zone) - Dãy (Aisle) - Kệ (Rack) - Tầng (Shelf) - Ngăn/Hộc (Bin). Cấu hình sức chứa tối đa và theo dõi trực quan tỷ lệ lấp đầy của từng ngăn kệ."),
        ("Công việc 3.2: Điều hành Phân loại 3 Kho Chất Lượng (Quality Stock Segregation): ", "Tổ chức và giám sát nghiêm ngặt việc phân luồng hàng hóa theo 3 trạng thái chất lượng: (1) Kho Hàng Mới (nguyên seal, đủ tiêu chuẩn xuất kho đại lý); (2) Kho Trưng Bày (hàng mẫu cho khách xem); (3) Kho Hàng Lỗi (cách ly riêng biệt tại khu vực C-01 để chờ xuất trả NCC hoặc bảo hành)."),
        ("Công việc 3.3: Xác nhận Nghiệm thu & Nhập Kho Vật lý (Physical Inbound Confirmation): ", "Tiếp nhận xe vận chuyển từ NCC, kiểm tra niêm phong kẹp chì của thùng kiện; đối chiếu số lượng thùng thực nhận với vận đơn; ký xác nhận bàn giao nhận hàng và chỉ định ngăn kệ lưu trữ cho nhân viên xếp dỡ."),
        ("Công việc 3.4: Kiểm tra & Xác nhận Xuất Kho Vật lý (Physical Outbound Confirmation): ", "Trước khi bàn giao hàng cho đơn vị vận chuyển hoặc đại lý đến nhận, Thủ kho trực tiếp kiểm tra kiện hàng đã đóng gói, đối chiếu danh sách mã Serial dán trên kiện với Phiếu xuất kho B2B trên hệ thống; xác nhận hoàn tất xuất kho vật lý."),
        ("Công việc 3.5: Quản lý & Phê duyệt Điều chuyển Nội bộ Kho (Bin-to-Bin Transfer): ", "Khởi tạo hoặc phê duyệt các lệnh điều chuyển sản phẩm giữa các ngăn kệ để tối ưu hóa không gian lưu trữ, hoặc điều chuyển giữa Kho Trưng Bày và Kho Hàng Mới sau khi phục hồi tình trạng đóng gói."),
        ("Công việc 3.6: Chủ trì Tổ chức Kiểm kê & Cân bằng Sai lệch trong Thẩm quyền: ", "Lập kế hoạch và kích hoạt lệnh kiểm kê định kỳ (tháng/quý) hoặc đột xuất theo từng dãy kệ; phân công nhân viên quét Serial; hệ thống tự động so khớp để xuất biên bản đối soát. Thủ kho xem xét nguyên nhân sai lệch và thực hiện cân bằng kho trong ngưỡng thẩm quyền cho phép (sai lệch giá trị thấp)."),
        ("Công việc 3.7: Giám sát Sổ Thẻ Kho & Cảnh báo Tồn Định Mức (Stock Card & Min/Max Alerts): ", "Theo dõi dòng biến động nhập - xuất trên Sổ Thẻ kho điện tử (`so_the_kho`); kiểm tra các mẫu đồng hồ chạm ngưỡng tồn kho an toàn (Min Stock) để đề xuất lên kế hoạch đặt mua thêm hàng từ hãng.")
    ]
    for t_title, t_desc in wh_tasks:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15; bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(t_title); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = bp.add_run(t_desc); r2.font.name = "Arial"; r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    # Warehouse Manager Table
    tbl_wh = doc.add_table(rows=8, cols=5)
    tbl_wh.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_wh, color="CBD5E1", sz="4")
    
    r_hdr = tbl_wh.rows[0]; make_row_header(r_hdr)
    for i, title in enumerate(th_headers):
        c = r_hdr.cells[i]; set_cell_width(c, th_widths[i])
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title); run.font.name = "Arial"; run.font.size = Pt(8); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    wh_table_data = [
        ("Quản lý sơ đồ ngăn kệ (Bin)", "Định kỳ / khi bố trí lại kho", "Khu, Dãy, Kệ, Tầng, Hộc, Sức chứa", "Sơ đồ mặt bằng kệ, Tỷ lệ lấp đầy (%)", "Mỗi kệ gắn mã định danh vật lý duy nhất"),
        ("Phân luồng 3 kho chất lượng", "Liên tục", "Serial, Trạng thái (New/Display/Defect)", "Phân bổ Serial vào đúng khu vực kho", "Chỉ xuất kho đại lý đồng hồ thuộc Kho Hàng Mới"),
        ("Xác nhận nhập kho vật lý", "Khi có lô hàng NCC giao đến", "Thùng kiện thực tế, Phiếu nhập nháp", "Biên bản bàn giao ký nhận, Vị trí lưu kệ", "Kiểm tra kỹ niêm phong thùng kiện của hãng"),
        ("Xác nhận xuất kho vật lý", "Khi kiện hàng đóng gói xong", "Kiện hàng, Danh sách Serial quét", "Phiếu xuất kho B2B có chữ ký xác nhận", "Chỉ xác nhận khi đối chiếu khớp 100% Serial"),
        ("Điều chuyển ngăn kệ nội bộ", "Khi cần sắp xếp / gom hàng", "Serial cần chuyển, Ngăn nguồn, Ngăn đích", "Phiếu điều chuyển, Cập nhật vị trí Serial", "Ngăn đích phải còn sức chứa khả dụng"),
        ("Chủ trì đợt kiểm kê kho", "Định kỳ tháng/quý hoặc đột xuất", "Phạm vi kiểm kê (Toàn kho/Dãy kệ/Hãng)", "Biên bản đối soát kiểm kê Serial chi tiết", "Đóng băng giao dịch tại khu vực kiểm kê"),
        ("Cân bằng kiểm kê trong hạn", "Sau khi hoàn tất đối soát", "Danh sách Serial thừa/thiếu, Lý do", "Lệnh cân bằng kho, Ghi Sổ Thẻ kho", "Vượt ngưỡng thẩm quyền phải trình Chủ duyệt")
    ]
    for row_idx, rvals in enumerate(wh_table_data, start=1):
        row = tbl_wh.rows[row_idx]; make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]; set_cell_width(c, th_widths[col_idx])
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 1): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8)
            if col_idx == 0: r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            else: r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACTOR 4: NHÂN VIÊN NHẬP - XUẤT KHO
    # -------------------------------------------------------------
    doc.add_heading("4. TÁC NHÂN: NHÂN VIÊN NHẬP - XUẤT KHO (OPERATIONS STAFF)", level=2)
    add_callout(
        doc,
        "Lực lượng tác nghiệp tiền tuyến tại kho hàng; trực tiếp sử dụng thiết bị quét mã vạch (Barcode/QR HID) để nhập liệu, nạp đối soát dải Serial, soạn hàng theo đơn, đóng gói xuất kho đại lý và xử lý các luồng hàng đổi trả, bảo hành.",
        bold_prefix="MỤC TIÊU VAI TRÒ:"
    )

    p_op_intro = doc.add_paragraph()
    p_op_intro.paragraph_format.line_spacing = 1.15; p_op_intro.paragraph_format.space_after = Pt(4)
    r = p_op_intro.add_run("Danh mục các công việc và nhiệm vụ chi tiết của Nhân viên nhập - xuất kho:")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True

    op_tasks = [
        ("Công việc 4.1: Khởi tạo Phiếu Nhập Kho & Quy đổi ĐVT Thùng ra Chiếc: ", "Tiếp nhận đơn mua hàng (PO) đã duyệt; tạo phiếu nhập kho mới; chọn ĐVT nhập là Thùng/Kiện; nhập số lượng thùng thực nhận; hệ thống tự động nhân hệ số quy đổi để ra tổng số lượng chiếc lẻ cần nạp Serial."),
        ("Công việc 4.2: Nạp & Quét Đối soát Dải Serial Lúc Nhập Kho: ", "Sử dụng súng quét mã vạch hoặc camera Barcode scanner để quét mã Serial từng chiếc đồng hồ khi khui thùng, hoặc import file Excel chứa dải Serial do nhà sản xuất phát hành. Hệ thống kiểm tra đối soát 2 chiều: (1) Số Serial nạp vào = Tổng số chiếc sau quy đổi; (2) Toàn bộ Serial chưa từng tồn tại trên hệ thống."),
        ("Công việc 4.3: Lưu Phiếu Nhập Nháp & Chuyển Trình Duyệt: ", "Lưu trữ phiếu nhập ở trạng thái bản nháp (DRAFT) sau khi hoàn tất nạp Serial; bàn giao thông tin cho Kế toán để nhập chi phí phân bổ và thông báo cho Thủ kho xác nhận vật lý."),
        ("Công việc 4.4: Lập Đơn Xuất Kho Đại Lý Nháp Theo Đặt Hàng Của Đại Lý: ", "Tiếp nhận đơn đặt hàng từ đại lý B2B; kiểm tra số lượng đặt theo từng mẫu mã đảm bảo >= MOQ quy định; kiểm tra số lượng tồn kho khả dụng; áp dụng bảng giá phân phối đại lý theo cấp đại lý (VIP/Bạc/Đồng); lập lệnh xuất kho đại lý nháp và chuyển sang Kế toán thẩm định công nợ."),
        ("Công việc 4.5: Soạn Hàng Từ Ngăn Kệ Theo Lệnh Giữ Chỗ (Reserved): ", "Khi lệnh xuất kho đại lý đã được duyệt và khóa hàng giữ chỗ trên hệ thống, nhân viên in phiếu soạn hàng (Pick List), đến đúng các vị trí ngăn kệ (Bin) được chỉ định để lấy đồng hồ ra bàn đóng gói."),
        ("Công việc 4.6: Quét Serial Đóng Kiện & Thực Xuất Kho Phân Phối Đại Lý: ", "Dùng máy quét quét từng mã Serial đích danh trên sản phẩm trước khi đóng vào kiện hàng. Hệ thống kiểm tra thời gian thực: mã Serial phải đúng SKU, phải đang ở trạng thái 'HANG_MOI' và 'TRONG_KHO', không bị quét trùng. Khi quét đủ 100%, chuyển kiện hàng cho Thủ kho xác nhận bàn giao."),
        ("Công việc 4.7: Tiếp nhận Hàng Đại Lý Hoàn Trả & Xuất Kho Bảo Hành / Tiêu Hủy: ", "Tiếp nhận sản phẩm đổi trả từ đại lý; quét kiểm tra Serial để xác định nguồn gốc bán ra; phân loại sơ bộ (hàng nguyên seal đưa về Kho Mới, hàng lỗi đưa về Kho Lỗi C-01). Thực hiện đóng gói xuất kho đồng hồ lỗi đi gửi bảo hành chính hãng theo lệnh xuất kho khác.")
    ]
    for t_title, t_desc in op_tasks:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15; bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(t_title); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = bp.add_run(t_desc); r2.font.name = "Arial"; r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    # Operations Staff Table
    tbl_op = doc.add_table(rows=8, cols=5)
    tbl_op.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_op, color="CBD5E1", sz="4")
    
    r_hdr = tbl_op.rows[0]; make_row_header(r_hdr)
    for i, title in enumerate(th_headers):
        c = r_hdr.cells[i]; set_cell_width(c, th_widths[i])
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title); run.font.name = "Arial"; run.font.size = Pt(8); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    op_table_data = [
        ("Khởi tạo phiếu nhập kho", "Khi có đợt hàng về", "Đơn mua PO, Số lượng thùng kiện", "Phiếu nhập nháp, Số chiếc quy đổi", "Áp dụng đúng hệ số quy đổi chuẩn"),
        ("Nạp & Quét Serial nhập", "Sau khi khui thùng kiện", "Mã Serial quét bằng súng / File Excel", "Danh sách Serial nạp vào chi tiết phiếu", "Khớp 100% số chiếc, không trùng lặp"),
        ("Lập lệnh xuất kho đại lý nháp", "Khi đại lý gửi yêu cầu đặt", "Mã đại lý, SKU, Số lượng thùng/chiếc", "Lệnh xuất kho đại lý nháp (DRAFT Order)", "Số lượng >= MOQ, Số lượng <= Khả dụng"),
        ("Soạn hàng tại ngăn kệ", "Sau khi lệnh xuất đại lý được duyệt", "Lệnh soạn hàng Pick List, Vị trí Bin", "Lô đồng hồ đưa về bàn đóng gói", "Lấy đúng vị trí kệ được hệ thống chỉ định"),
        ("Quét Serial đóng kiện xuất", "Tại bàn đóng gói", "Mã Serial trên từng chiếc đồng hồ", "Kiện hàng dán tem, Phiếu xuất kho B2B", "Serial phải thuộc HANG_MOI & TRONG_KHO"),
        ("Tiếp nhận hàng nhận trả hàng đại lý", "Khi đại lý gửi trả hàng", "Mã đại lý, Mã Serial sản phẩm trả", "Phiếu nhận đổi trả, Đánh giá phân loại", "Serial phải tồn tại lịch sử xuất bán cho đại lý"),
        ("Đóng gói xuất bảo hành/hủy", "Theo lệnh xử lý hàng lỗi", "Lệnh xuất bảo hành/tiêu hủy từ quản lý", "Kiện hàng bảo hành gửi hãng", "Chỉ xuất các Serial nằm trong Kho Hàng Lỗi")
    ]
    for row_idx, rvals in enumerate(op_table_data, start=1):
        row = tbl_op.rows[row_idx]; make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]; set_cell_width(c, th_widths[col_idx])
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 1): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8)
            if col_idx == 0: r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            else: r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACTOR 5: KẾ TOÁN (ACCOUNTANT)
    # -------------------------------------------------------------
    doc.add_heading("5. TÁC NHÂN: KẾ TOÁN (ACCOUNTANT - VỐN, KHO & CÔNG NỢ)", level=2)
    add_callout(
        doc,
        "Đảm bảo tính chính xác tuyệt đối của số liệu tài chính; chịu trách nhiệm tính toán và phân bổ chi phí giá vốn đích danh vào từng mã Serial, kiểm soát chu trình công nợ hai chiều (NCC và Đại lý), lập các chứng từ thu chi và đối soát Sổ Thẻ kho.",
        bold_prefix="MỤC TIÊU VAI TRÒ:"
    )

    p_acc_intro = doc.add_paragraph()
    p_acc_intro.paragraph_format.line_spacing = 1.15; p_acc_intro.paragraph_format.space_after = Pt(4)
    r = p_acc_intro.add_run("Danh mục các công việc và nhiệm vụ chi tiết của Kế toán:")
    r.font.name = "Arial"; r.font.size = Pt(9.5); r.font.bold = True

    acc_tasks = [
        ("Công việc 5.1: Phân bổ Chi phí Lô Hàng & Thiết lập Giá vốn Đích danh: ", "Tiếp nhận phiếu nhập kho nháp từ nhân viên; thu thập hóa đơn chi phí phát sinh thực tế (cước vận chuyển quốc tế, thuế nhập khẩu hải quan, phí bảo hiểm hàng xa xỉ); nhập vào hệ thống để tự động phân bổ bình quân vào từng chiếc: Giá vốn Serial = Giá mua hóa đơn + (Tổng chi phí phân bổ / Tổng số chiếc). Gán giá vốn đích danh này vào từng mã Serial lưu kho."),
        ("Công việc 5.2: Theo dõi Công nợ NCC & Lập Phiếu Chi Thanh Toán: ", "Theo dõi số dư nợ phải trả Nhà cung cấp theo từng lô hàng nhập; đối soát hóa đơn; lập Phiếu Chi tiền (ủy nhiệm chi ngân hàng / tiền mặt) để thanh toán cho NCC theo kỳ hạn thanh toán cam kết; cập nhật giảm dư nợ NCC."),
        ("Công việc 5.3: Thẩm định Hạn mức Tín dụng (Credit Limit) Đơn Xuất Kho Đại Lý: ", "Khi nhân viên lập lệnh xuất kho đại lý nháp, Kế toán kiểm tra điều kiện tín dụng của đại lý: Dư nợ hiện tại + Giá trị đơn mới - Tiền cọc <= Hạn mức nợ cho phép, đồng thời kiểm tra đại lý không có hóa đơn quá hạn (Net 15 / Net 30). Nếu hợp lệ, ký xác nhận để hệ thống khóa giữ chỗ tồn kho; nếu vượt ngưỡng, chuyển hồ sơ trình Chủ cửa hàng duyệt."),
        ("Công việc 5.4: Lập Phiếu Thu Tiền Xuất Kho Đại Lý & Thu Hồi Nợ Đại Lý: ", "Tiếp nhận chứng từ nộp tiền cọc đơn xuất kho hoặc chứng từ thanh toán tiền hàng của đại lý qua ngân hàng; lập Phiếu Thu tiền trên hệ thống; giảm số dư nợ của đại lý và tự động khôi phục hạn mức tín dụng khả dụng của đại lý."),
        ("Công việc 5.5: Đối soát Sổ Thẻ Kho Điện tử & Chứng từ Giao Dịch: ", "Định kỳ hàng tuần đối chiếu giữa số lượng và giá trị trên Sổ Thẻ kho điện tử (`so_the_kho`), Phiếu nhập kho (PN), Phiếu xuất kho (PX) và Phiếu cân bằng kiểm kê (KK); phát hiện và xử lý kịp thời các sai lệch số liệu."),
        ("Công việc 5.6: Kết xuất Báo cáo Tài chính Kho & Dòng Tiền Thuần: ", "Lập và kết xuất định kỳ các báo cáo chuyên sâu: Báo cáo Doanh thu - Giá vốn (COGS) - Lợi nhuận gộp B2B; Sổ chi tiết công nợ 2 chiều; Báo cáo dòng tiền thu chi thực tế (Cashflow Report); xuất dữ liệu ra định dạng Excel/PDF phục vụ thanh kiểm tra thuế.")
    ]
    for t_title, t_desc in acc_tasks:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15; bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(t_title); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = bp.add_run(t_desc); r2.font.name = "Arial"; r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    # Accountant Table
    tbl_acc = doc.add_table(rows=7, cols=5)
    tbl_acc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_acc, color="CBD5E1", sz="4")
    
    r_hdr = tbl_acc.rows[0]; make_row_header(r_hdr)
    for i, title in enumerate(th_headers):
        c = r_hdr.cells[i]; set_cell_width(c, th_widths[i])
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title); run.font.name = "Arial"; run.font.size = Pt(8); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    acc_table_data = [
        ("Phân bổ chi phí lô nhập", "Theo từng phiếu nhập kho", "Chi phí vận chuyển, thuế hải quan, bảo hiểm", "Giá vốn Đích danh của từng mã Serial", "Giá vốn = Giá mua + Chi phí phân bổ/chiếc"),
        ("Lập Phiếu Chi trả nợ NCC", "Theo kỳ hạn thanh toán", "Mã NCC, Hóa đơn NCC, Số tiền chi", "Phiếu chi (PC-xxxx), Giảm dư nợ NCC", "Số tiền chi không vượt quá dư nợ thực tế"),
        ("Thẩm định tín dụng lệnh xuất đại lý", "Khi nhân viên lên đơn nháp", "Đơn hàng xuất đại lý, Dư nợ & Hạn mức nợ đại lý", "Xác nhận hạn mức khả dụng / Trình duyệt", "Không cho nợ nếu có hóa đơn quá hạn"),
        ("Lập Phiếu Thu nợ đại lý / cọc", "Khi phát sinh thanh toán", "Mã đại lý, Giấy báo Có ngân hàng", "Phiếu thu (PT-xxxx), Tăng hạn mức khả dụng", "Khớp đúng số tiền và nội dung chuyển khoản"),
        ("Đối soát Sổ Thẻ kho", "Hàng tuần / Cuối tháng", "Sổ Thẻ kho, Chứng từ PN, PX, KK", "Biên bản đối soát cân đối kho tài chính", "Khớp số lượng và giá trị 100%"),
        ("Báo cáo Tài chính & Dòng tiền", "Định kỳ tháng/quý/năm", "Toàn bộ giao dịch PN, PX, PT, PC", "Báo cáo Lợi nhuận gộp B2B, Sổ công nợ", "Xuất file chuẩn khổ A4 / Excel / PDF")
    ]
    for row_idx, rvals in enumerate(acc_table_data, start=1):
        row = tbl_acc.rows[row_idx]; make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]; set_cell_width(c, th_widths[col_idx])
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx in (0, 1): p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8)
            if col_idx == 0: r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            else: r_val.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # PHẦN III: QUY TRÌNH PHỐI HỢP LIÊN TÁC NHÂN (COLLABORATION WORKFLOWS)
    # =============================================================
    h3 = doc.add_heading("III. QUY TRÌNH PHỐI HỢP TÁC NGHIỆP LIÊN TÁC NHÂN TRỌNG TÂM", level=1)
    h3.paragraph_format.space_before = Pt(12); h3.paragraph_format.space_after = Pt(8)
    for r in h3.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    flows = [
        {
            "name": "1. Luồng Nhập Kho Chính Hãng & Ghi Nhận Giá Vốn Đích Danh",
            "steps": [
                ("Bước 1 (Nhân viên nhập - xuất kho): ", "Mở đơn mua PO đã duyệt, kiểm tra quy cách đóng gói (Thùng/Kiện), nhập số thùng thực nhận để hệ thống nhân hệ số quy đổi ra số chiếc lẻ."),
                ("Bước 2 (Nhân viên nhập - xuất kho): ", "Dùng máy quét Barcode quét dải Serial từng chiếc đồng hồ khi khui thùng hoặc nạp dải Serial từ file Excel của hãng. Hệ thống kiểm tra đối soát số lượng và tính duy nhất của Serial. Lưu phiếu ở trạng thái DRAFT."),
                ("Bước 3 (Thủ kho điều hành): ", "Kiểm tra tình trạng vật lý kiện hàng, chỉ định vị trí ngăn kệ lưu trữ (Bin), xác nhận số lượng thực tế nhận vào kho."),
                ("Bước 4 (Kế toán): ", "Tiếp nhận phiếu nháp, nhập chi phí phụ trợ (vận chuyển, hải quan, bảo hiểm); hệ thống tự động tính Giá vốn Đích danh cho từng Serial. Kế toán đối soát và ký duyệt chứng từ tài chính."),
                ("Bước 5 (Chủ cửa hàng): ", "Nếu chi phí phụ trợ hoặc chênh lệch vượt định mức quy định, Chủ cửa hàng ký duyệt ngoại lệ trước khi chốt nhập kho."),
                ("Bước 6 (Hệ thống): ", "Kích hoạt trạng thái APPROVED cho phiếu nhập; lưu trữ từng Serial với trạng thái 'TRONG_KHO' / 'HANG_MOI'; tăng tồn kho thực tế; tăng công nợ NCC và ghi Sổ Thẻ kho (+).")
            ]
        },
        {
            "name": "2. Luồng Xuất Kho Đại Lý & Duyệt Khóa Giữ Chỗ Tồn Kho (Reserved Allocation)",
            "steps": [
                ("Bước 1 (Nhân viên nhập - xuất kho): ", "Tiếp nhận yêu cầu từ đại lý B2B, lập lệnh xuất kho đại lý nháp theo Thùng hoặc Chiếc lẻ; hệ thống tự động kiểm tra điều kiện sỉ: Số lượng đặt >= MOQ, Số lượng đặt <= Tồn khả dụng."),
                ("Bước 2 (Kế toán): ", "Thẩm định hạn mức tín dụng và thời hạn nợ của đại lý. Nếu đại lý còn hạn mức và không có nợ quá hạn, Kế toán ký duyệt chấp thuận đơn."),
                ("Bước 3 (Chủ cửa hàng): ", "Trường hợp đại lý vượt hạn mức tín dụng, đơn được chuyển lên Chủ cửa hàng. Chỉ Chủ cửa hàng mới có thẩm quyền duyệt ngoại lệ tín dụng có ghi nhận lý do."),
                ("Bước 4 (Hệ thống): ", "Chuyển trạng thái đơn sang DA_DUYET; tự động tăng so_luong_giu_cho và giảm so_luong_kha_dung tại bảng tổng hợp tồn kho, triệt tiêu nguy cơ bán trùng hàng.")
            ]
        },
        {
            "name": "3. Luồng Quét Serial Đóng Kiện & Thực Xuất Kho Xuất Kho Đại Lý",
            "steps": [
                ("Bước 1 (Nhân viên nhập - xuất kho): ", "Mở lệnh xuất kho đại lý đã duyệt giữ chỗ, tạo Phiếu xuất kho đóng hàng, in lệnh soạn hàng Pick List."),
                ("Bước 2 (Nhân viên nhập - xuất kho): ", "Đến đúng ngăn kệ (Bin), lấy đồng hồ và dùng súng quét từng mã Serial vào kiện hàng. Hệ thống kiểm soát tính hợp lệ: đúng SKU, thuộc HANG_MOI, đang TRONG_KHO và không bị quét trùng."),
                ("Bước 3 (Thủ kho điều hành): ", "Đối chiếu số lượng và danh sách Serial dán trên kiện hàng thực tế so với phiếu xuất điện tử; xác nhận xuất kho vật lý."),
                ("Bước 4 (Hệ thống): ", "Trừ tồn kho thực tế, giải phóng tồn giữ chỗ; chuyển trạng thái Serial sang 'DA_BAN'; tăng công nợ đại lý; ghi Sổ Thẻ kho (-) và in Phiếu xuất kho kiêm Biên bản bàn giao A4.")
            ]
        },
        {
            "name": "4. Luồng Kiểm Kê Kho & Cân Bằng Sai Lệch Theo Serial",
            "steps": [
                ("Bước 1 (Thủ kho điều hành): ", "Lập đợt kiểm kê trên hệ thống, chọn phạm vi kiểm kê (toàn kho hoặc theo kệ); hệ thống tạm thời đóng băng giao dịch tại khu vực đó."),
                ("Bước 2 (Thủ kho & Nhân viên): ", "Đến từng ngăn kệ, dùng máy quét quét toàn bộ mã Serial thực tế hiện diện."),
                ("Bước 3 (Hệ thống): ", "Tự động so khớp dữ liệu quét với CSDL, phân loại rõ ràng: Serial Khớp đúng, Serial Thừa và Serial Thiếu."),
                ("Bước 4 (Kế toán & Thủ kho): ", "Cùng xác minh nguyên nhân sai lệch và lập Biên bản đối soát kiểm kê."),
                ("Bước 5 (Phê duyệt cân bằng): ", "Nếu sai lệch nhỏ trong hạn mức, Thủ kho phê duyệt cân bằng kho; nếu sai lệch tài sản lớn vượt ngưỡng, Chủ cửa hàng xem xét phê duyệt lệnh cân bằng; hệ thống tự động cập nhật lại vị trí/trạng thái Serial và ghi phát sinh Sổ Thẻ kho.")
            ]
        }
    ]

    for flow in flows:
        hf = doc.add_heading(flow["name"], level=2)
        hf.paragraph_format.space_before = Pt(8); hf.paragraph_format.space_after = Pt(3)
        for r in hf.runs:
            r.font.name = "Arial"; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

        for s_title, s_desc in flow["steps"]:
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.line_spacing = 1.15; p.paragraph_format.space_after = Pt(2.5)
            r1 = p.add_run(s_title); r1.font.name = "Arial"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = RGBColor(27, 54, 93)
            r2 = p.add_run(s_desc); r2.font.name = "Arial"; r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =============================================================
    # PHẦN IV: MA TRẬN TRÁCH NHIỆM RACI CHO 5 TÁC NHÂN
    # =============================================================
    h4 = doc.add_heading("IV. MA TRẬN PHÂN ĐỊNH TRÁCH NHIỆM RACI (RACI MATRIX)", level=1)
    h4.paragraph_format.space_before = Pt(12); h4.paragraph_format.space_after = Pt(6)
    for r in h4.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(27, 54, 93)

    p_raci_desc = doc.add_paragraph()
    p_raci_desc.paragraph_format.line_spacing = 1.15; p_raci_desc.paragraph_format.space_after = Pt(6)
    r = p_raci_desc.add_run("Ký hiệu chuẩn RACI: ")
    r.font.name = "Arial"; r.font.size = Pt(9); r.font.bold = True
    r_sub = p_raci_desc.add_run("[R] Responsible: Người trực tiếp thực hiện • [A] Accountable: Người chịu trách nhiệm phê duyệt cuối cùng • [C] Consulted: Người được tham vấn / đối soát • [I] Informed: Người nhận thông tin / theo dõi.")
    r_sub.font.name = "Arial"; r_sub.font.size = Pt(8.5); r_sub.font.color.rgb = RGBColor(71, 85, 105)

    raci_data = [
        ("Khai báo Danh mục Master SKU, Thương hiệu, ĐVT", "R / A", "I", "I", "I", "C"),
        ("Quản trị Tài khoản người dùng & Phân quyền RBAC", "R / A", "I", "I", "I", "I"),
        ("Giám sát Nhật ký Audit Log & Thu hồi Token", "R / A", "I", "I", "I", "I"),
        ("Khởi tạo Phiếu nhập kho & Nạp Serial (quét/Excel)", "I", "I", "C", "R", "C"),
        ("Phân bổ chi phí lô hàng vào Giá vốn đích danh", "I", "C", "I", "I", "R / A"),
        ("Xác nhận nghiệm thu & nhập kho vật lý", "I", "I", "R / A", "C", "I"),
        ("Phê duyệt chi phí nhập phát sinh vượt định mức", "I", "A", "I", "I", "R"),
        ("Lập Phiếu Chi thanh toán công nợ Nhà cung cấp", "I", "A (vượt)", "I", "I", "R / A"),
        ("Tiếp nhận đặt hàng & Lập Lệnh xuất kho đại lý nháp", "I", "I", "I", "R", "C"),
        ("Thẩm định hạn mức tín dụng & Duyệt giữ chỗ", "I", "A (vượt)", "C", "I", "R / A"),
        ("Soạn hàng tại kệ & Quét Serial đóng kiện xuất kho đại lý", "I", "I", "C", "R", "I"),
        ("Xác nhận bàn giao & xuất kho vật lý B2B", "I", "I", "R / A", "C", "I"),
        ("Lập Phiếu Thu hồi công nợ đại lý & Thu nợ đại lý", "I", "I", "I", "I", "R / A"),
        ("Bố trí ngăn kệ & Điều chuyển kho nội bộ", "I", "I", "R / A", "C", "I"),
        ("Kiểm kê thực tế & Đối soát sai lệch Serial", "I", "A (vượt)", "R / A (trong)", "R", "C"),
        ("Theo dõi Dashboard KPI & Báo cáo Tài chính dòng tiền", "I (Log)", "R / A (All)", "I (Kho)", "I (Tiến độ)", "R / A (TC)")
    ]

    raci_table = doc.add_table(rows=len(raci_data) + 1, cols=6)
    raci_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(raci_table, color="CBD5E1", sz="4")
    raci_widths = [3000, 1400, 1400, 1400, 1400, 1400]
    raci_headers = ["Nhóm Đầu Việc Nghiệp Vụ", "Quản Trị Hệ Thống", "Chủ Cửa Hàng", "Thủ Kho Điều Hành", "NV Nhập - Xuất Kho", "Kế Toán"]

    r_hdr = raci_table.rows[0]; make_row_header(r_hdr)
    for i, title in enumerate(raci_headers):
        c = r_hdr.cells[i]; set_cell_width(c, raci_widths[i])
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title); run.font.name = "Arial"; run.font.size = Pt(8); run.font.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, rvals in enumerate(raci_data, start=1):
        row = raci_table.rows[row_idx]; make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(rvals):
            c = row.cells[col_idx]; set_cell_width(c, raci_widths[col_idx])
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            if col_idx > 0: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_val = p.add_run(val); r_val.font.name = "Arial"; r_val.font.size = Pt(8)
            if col_idx == 0:
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            elif "A" in val:
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(197, 155, 39)
            elif "R" in val:
                r_val.font.bold = True; r_val.font.color.rgb = RGBColor(27, 54, 93)
            else:
                r_val.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Output file
    output_filename = "DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.docx"
    output_path = os.path.join(r"D:\cntt\pbhb", output_filename)
    doc.save(output_path)
    print(f"SUCCESS: Created document at {output_path}")

if __name__ == "__main__":
    build_actor_document()
