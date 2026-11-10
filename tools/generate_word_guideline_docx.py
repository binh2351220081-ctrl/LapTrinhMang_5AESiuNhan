# -*- coding: utf-8 -*-
"""
Script to generate: Document/HUONG_DAN_LAM_BAO_CAO_WORD_CHO_TUNG_THANH_VIEN.docx
Bản Hướng Dẫn Chi Tiết Viết Báo Cáo Word & Chuẩn Bị Vấn Đáp Cho Từng Thành Viên
Đề tài: Hệ Thống Quản Lý Kho Đồng Hồ ChronoVault B2B Wholesale WMS
Nhóm: 5AE Siêu Nhân (Phan Bá Hải Bình, Nguyễn Đắc Quân, Tô Đức Thảo, Võ Công Tâm, Trần Công Tú)
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

def build_word_guideline_document():
    doc = Document()
    
    # Page setup (A4 Portrait)
    section = doc.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    
    # Header & Footer
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "CHRONOVAULT B2B WMS • HƯỚNG DẪN VIẾT BÁO CÁO WORD & VẤN ĐÁP 5 THÀNH VIÊN"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.style.font.name = "Arial"
    hp.style.font.size = Pt(8)
    hp.style.font.color.rgb = RGBColor(148, 163, 184)
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Tài Liệu Hướng Dẫn Thành Viên • Nhóm 5AE Siêu Nhân • Môn Lập Trình Mạng (DAU)"
    fp.style.font.name = "Arial"
    fp.style.font.size = Pt(8)
    fp.style.font.color.rgb = RGBColor(148, 163, 184)
    
    # Colors
    C_NAVY = RGBColor(27, 54, 93)      # #1B365D
    C_GOLD = RGBColor(197, 155, 39)    # #C59B27
    C_SLATE = RGBColor(51, 65, 85)     # #334155
    C_GRAY = RGBColor(100, 116, 139)   # #64748B
    
    def set_cell_background(cell, hex_color):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)
        
    def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
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
        
    def add_callout(doc, text_lines, title=None, border_color="1B365D", bg_color="F8FAFC"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.77)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
                <w:top w:val="none"/>
                <w:right w:val="none"/>
                <w:bottom w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        if title:
            r_title = p.add_run(f"📌 {title}\n")
            r_title.font.name = "Arial"
            r_title.font.size = Pt(10)
            r_title.font.bold = True
            r_title.font.color.rgb = C_NAVY
            
        for idx, line in enumerate(text_lines):
            p_line = cell.add_paragraph() if (idx > 0 or title) else p
            p_line.paragraph_format.space_before = Pt(0)
            p_line.paragraph_format.space_after = Pt(2)
            p_line.paragraph_format.line_spacing = 1.15
            r = p_line.add_run(line)
            r.font.name = "Arial"
            r.font.size = Pt(9.5)
            r.font.color.rgb = C_SLATE
            if line.startswith("•") or line.startswith("👉") or line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5."):
                r.font.bold = True
                
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # HEADER / BANNER
    # =========================================================================
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(0)
    p_top.paragraph_format.space_after = Pt(2)
    r_top = p_top.add_run("TRƯỜNG ĐẠI HỌC KIẾN TRÚC ĐÀ NẴNG (DAU) • KHOA CÔNG NGHỆ THÔNG TIN\nBỘ MÔN: LẬP TRÌNH MẠNG")
    r_top.font.name = "Arial"; r_top.font.size = Pt(9.5); r_top.font.bold = True; r_top.font.color.rgb = C_GRAY

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("HƯỚNG DẪN CHI TIẾT VIẾT BÁO CÁO WORD & VẤN ĐÁP\nDÀNH CHO 5 THÀNH VIÊN NHÓM '5 AE SIÊU NHÂN'")
    r_title.font.name = "Arial"; r_title.font.size = Pt(15); r_title.font.bold = True; r_title.font.color.rgb = C_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Dự Án: ChronoVault WMS — Hệ Thống Quản Lý Kho & Phân Phối Đồng Hồ Cao Cấp B2B\nNhóm Trưởng Phụ Trách: Phan Bá Hải Bình")
    r_sub.font.name = "Arial"; r_sub.font.size = Pt(10.5); r_sub.font.italic = True; r_sub.font.color.rgb = C_GOLD

    # =========================================================================
    # PHẦN QUY ĐỊNH CHUNG
    # =========================================================================
    h1 = doc.add_heading("I. QUY ĐỊNH CHUNG & HÌNH THỨC NỘP BÀI CHO NHÓM TRƯỞNG", level=1)
    for r in h1.runs:
        r.font.name = "Arial"; r.font.size = Pt(12.5); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "1. Hình thức nộp: Mỗi bạn tự viết 01 file Word riêng (từ 4 đến 7 trang A4) mô tả toàn bộ phân hệ mình phụ trách.",
            "2. Đặt tên file Word: BaoCao_[MaTV]_[HoTen]_[TenPhanHe].docx (Ví dụ: BaoCao_TV2_NguyenDacQuan_NhapKho_NCC.docx).",
            "3. Thời hạn nộp: Gửi file Word và thư mục ảnh chụp màn hình (rõ nét) cho Nhóm trưởng trước ngày nộp bài 3 ngày.",
            "4. Cấu trúc bắt buộc của file Word cá nhân (gồm 5 mục chuẩn):",
            "   • Mục 1: Danh sách các chức năng & phạm vi bài toán phân hệ.",
            "   • Mục 2: Chụp ảnh màn hình giao diện thực tế (Screenshots) và chú thích chi tiết từng nút bấm, ô nhập liệu.",
            "   • Mục 3: Vẽ Sơ đồ Ca sử dụng (Use Case) & Sơ đồ Tuần tự (Sequence Diagram) mô tả luồng nghiệp vụ.",
            "   • Mục 4: Bảng Kịch bản Kiểm thử (Test Cases) có dữ liệu mẫu thực tế.",
            "   • Mục 5: Bộ câu hỏi Vấn đáp trọng tâm của Giảng viên & Gợi ý câu trả lời tự tin."
        ],
        title="QUY CHUẨN NỘP BÀI CỦA THÀNH VIÊN",
        border_color="1B365D",
        bg_color="F8FAFC"
    )

    # Table of 5 members
    tbl = doc.add_table(rows=6, cols=5)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Mã TV", "Họ Và Tên", "Phân Hệ Nghiệp Vụ", "Package Phụ Trách", "Nhánh Git Riêng"]
    col_widths = [Inches(0.8), Inches(1.5), Inches(1.8), Inches(1.6), Inches(1.0)]
    
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=60, right=60)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Arial"; r.font.size = Pt(9); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

    data = [
        ("TV1", "Phan Bá Hải Bình\n(Nhóm trưởng)", "Core Arch, RBAC 5 Roles, Danh mục Luxury & ĐVT", "com.example.chronovaultwms.core\ncom.example.chronovaultwms.product", "main\nfeature/product"),
        ("TV2", "Nguyễn Đắc Quân", "Nhà Cung Cấp, Nhập Kho ĐVT, Quét Serial & Giá Vốn Đích Danh", "com.example.chronovaultwms.inbound", "feature/tv2-inbound-supplier"),
        ("TV3", "Tô Đức Thảo", "Đối Tác Đại Lý & Quản Lý Xuất Kho, Khóa Giữ Chỗ, Quét Serial", "com.example.chronovaultwms.outbound", "feature/tv3-outbound-dealer"),
        ("TV4", "Võ Công Tâm", "Tồn Kho 3 Chất Lượng, Ma Trận Kệ Bin, Kiểm Kê & Sổ Thẻ Kho", "com.example.chronovaultwms.inventory", "feature/tv4-inventory-audit"),
        ("TV5", "Trần Công Tú", "Dashboard KPI, MPAndroidChart Doanh Số 6 Tháng & 9 Báo Cáo", "com.example.chronovaultwms.dashboard", "feature/tv5-dashboard-reports")
    ]

    for row_idx, item in enumerate(data):
        row_cells = tbl.rows[row_idx + 1].cells
        bg_col = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
        for col_idx, text in enumerate(item):
            row_cells[col_idx].text = text
            row_cells[col_idx].width = col_widths[col_idx]
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=60, bottom=60, left=60, right=60)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.color.rgb = C_SLATE
                if col_idx in [0, 1]:
                    r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # HƯỚNG DẪN TV2: NGUYỄN ĐẮC QUÂN
    # =========================================================================
    h2 = doc.add_heading("II. HƯỚNG DẪN VIẾT BÁO CÁO CHO THÀNH VIÊN 2 (NGUYỄN ĐẮC QUÂN)", level=1)
    for r in h2.runs:
        r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "• Phân hệ: Đối tác Nhà Cung Cấp, Nhập Kho Quy đổi ĐVT, Quét Serial & Giá vốn Đích danh.",
            "• Tiêu đề chương trong Word: CHƯƠNG: PHÂN HỆ QUẢN LÝ NHÀ CUNG CẤP & NHẬP KHO ĐỒNG HỒ ĐÍCH DANH",
            "",
            "1. Nội dung 1 - Hồ sơ Nhà Cung Cấp & Công nợ: Danh bạ NCC chính hãng (Rolex Geneva SA, Swatch Group, Richemont...), cơ chế tự động ghi tăng nợ khi duyệt nhập kho; ghi giảm nợ khi lập Phiếu Chi thanh toán.",
            "2. Nội dung 2 - Nhập kho quy đổi ĐVT & Quét Camera Serial: Giải thích cơ chế nhập theo 'Thùng' quy đổi ra 'Chiếc' lẻ theo conversionRate; tích hợp Camera quét mã Serial và cơ chế chặn trùng lặp mã tuyệt đối trong Room DB.",
            "3. Nội dung 3 - Phương pháp Giá vốn Đích danh (Specific Identification): Phân bổ chi phí vận chuyển quốc tế, thuế quan, bảo hiểm vào từng chiếc: Giá vốn đích danh = Đơn giá mua + (Tổng chi phí phân bổ / Tổng số chiếc).",
            "4. Nội dung 4 - Xuất trả hàng lỗi cho NCC: Chọn Serial từ kho hàng lỗi (HANG_LOI), xuất trả hãng và cấn trừ công nợ.",
            "",
            "👉 Câu hỏi vấn đáp hay gặp:",
            "   - Giảng viên hỏi: 'Tại sao phải quản lý đích danh từng Serial mà không nhập theo số lượng tổng?'",
            "     Trả lời: 'Đồng hồ cao cấp là tài sản xa xỉ, mỗi chiếc có 1 số Serial duy nhất của hãng để bảo hành toàn cầu và chống hàng giả, bắt buộc quản lý đích danh 100%.'",
            "   - Giảng viên hỏi: 'Hệ thống chống trùng mã Serial như thế nào?'",
            "     Trả lời: 'Trường serialNumber là Primary Key trong bảng serials của Room DB. Khi quét Camera, hệ thống check tồn tại qua DAO, nếu đã có sẽ rung cảnh báo lỗi và chặn không cho thêm.'"
        ],
        title="NHIỆM VỤ WORD & VẤN ĐÁP CỦA NGUYỄN ĐẮC QUÂN (TV2)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    # =========================================================================
    # HƯỚNG DẪN TV3: TÔ ĐỨC THẢO
    # =========================================================================
    h3 = doc.add_heading("III. HƯỚNG DẪN VIẾT BÁO CÁO CHO THÀNH VIÊN 3 (TÔ ĐỨC THẢO)", level=1)
    for r in h3.runs:
        r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "• Phân hệ: Đối Tác Đại Lý & Quản Lý Xuất Kho (Hạn Mức Tín Dụng, Khóa Giữ Chỗ & Quét Serial).",
            "• Tiêu đề chương trong Word: CHƯƠNG: PHÂN HỆ ĐỐI TÁC ĐẠI LÝ & QUẢN LÝ XUẤT KHO",
            "",
            "1. Nội dung 1 - Quản lý Đại lý B2B & Hạn mức Tín dụng: Hồ sơ đại lý (Hải Triều, Galle Watch...), phân hạng VIP/Vàng/Bạc/Đồng, chiết khấu 15%-30%; thuật toán khóa đơn tự động nếu (Dư nợ hiện tại + Giá trị lô hàng xuất) > Hạn mức nợ.",
            "2. Nội dung 2 - Lệnh xuất kho & Cơ chế Khóa Giữ Chỗ (Reservation): Tồn khả dụng = Tồn vật lý - Tồn giữ chỗ. Lệnh xuất ở trạng thái tiếp nhận sẽ tăng reservedQuantity để các đơn sau không lấy trùng.",
            "3. Nội dung 3 - Xuất kho 2 bước (Picking & Dispatch): Gợi ý Serial theo vị trí kệ, quét Camera Serial trước khi đóng thùng (chặn hàng lỗi/trưng bày), xác nhận xuất kho hoàn tất.",
            "4. Nội dung 4 - Cập nhật Công nợ & In Phiếu Xuất: Chuyển Serial sang DA_BAN, trừ tồn vật lý, giải phóng giữ chỗ, tăng nợ đại lý, in phiếu xuất B2B kèm danh sách Serial bảo hành.",
            "",
            "👉 Câu hỏi vấn đáp hay gặp:",
            "   - Giảng viên hỏi: 'Cơ chế giữ chỗ tồn kho (Reservation) giải quyết vấn đề gì?'",
            "     Trả lời: 'Nếu không có giữ chỗ, khi kho còn 3 chiếc mà 2 nhân viên cùng tạo đơn 3 chiếc sẽ bị bán âm kho. Reservation khóa số lượng ngay khi tiếp nhận đơn để đơn sau thấy tồn khả dụng bằng 0.'",
            "   - Giảng viên hỏi: 'Nếu đại lý bị vượt hạn mức nợ thì làm sao để tạo được đơn?'",
            "     Trả lời: 'Bắt buộc phải lập Phiếu Thu tiền nợ cũ để giảm số dư nợ hoặc xin phê duyệt ngoại lệ từ Chủ cửa hàng.'"
        ],
        title="NHIỆM VỤ WORD & VẤN ĐÁP CỦA TÔ ĐỨC THẢO (TV3)",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # =========================================================================
    # HƯỚNG DẪN TV4: VÕ CÔNG TÂM
    # =========================================================================
    h4 = doc.add_heading("IV. HƯỚNG DẪN VIẾT BÁO CÁO CHO THÀNH VIÊN 4 (VÕ CÔNG TÂM)", level=1)
    for r in h4.runs:
        r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "• Phân hệ: Quản trị Tồn Kho Nội Bộ, Phân loại 3 Chất Lượng, Ma Trận Kệ Bin & Kiểm Kê Thực Tế.",
            "• Tiêu đề chương trong Word: CHƯƠNG: PHÂN HỆ QUẢN LÝ TỒN KHO NỘI BỘ, SƠ ĐỒ KỆ & KIỂM KÊ",
            "",
            "1. Nội dung 1 - Tồn kho 3 Cấp Chất Lượng: Phân tách Hàng Mới (HANG_MOI), Trưng bày Boutique (TRUNG_BAY), Hàng Lỗi kỹ thuật (HANG_LOI); chức năng chuyển đổi trạng thái kèm lý do kỹ thuật.",
            "2. Nội dung 2 - Sơ đồ Ma Trận Ngăn Kệ (Bin Location Matrix): Trực quan hóa mặt bằng tủ chống trộm: Kệ K1 (Sport), Kệ K2 (Classic), các ô Bin K1-A01, K1-A02... đổi màu Trống (Xanh)/Chứa (Vàng)/Đầy (Đỏ); điều chuyển kệ bằng quét mã vạch.",
            "3. Nội dung 3 - Quy trình Kiểm kê Kho & Đối soát Tự động: Quét Camera Serial thực tế trên kệ; thuật toán tự động phân loại Khớp đúng / Thừa kho (Surplus) / Thiếu kho (Deficit); lập biên bản chênh lệch có chữ ký.",
            "4. Nội dung 4 - Sổ Thẻ kho Điện tử (Stock Card): Tra cứu toàn bộ lịch sử biến động (+/-) của từng SKU hoặc từng Serial duy nhất từ lúc nhập đến lúc xuất.",
            "",
            "👉 Câu hỏi vấn đáp hay gặp:",
            "   - Giảng viên hỏi: 'Khi kiểm kê phát hiện thiếu đồng hồ thì hệ thống xử lý thế nào?'",
            "     Trả lời: 'Hệ thống đưa Serial đó vào danh sách Thiếu kho, yêu cầu lập Biên bản xử lý chênh lệch kiểm kê, giải trình nguyên nhân và phải có phê duyệt của Quản lý kho mới điều chỉnh tồn và ghi Audit Log.'",
            "   - Giảng viên hỏi: 'Sổ Thẻ kho điện tử khác gì với bảng danh sách tồn kho?'",
            "     Trả lời: 'Bảng tồn kho chỉ cho biết số lượng hiện có. Sổ Thẻ kho là sổ nhật ký kế toán ghi lại từng lần biến động (+/-) theo thời gian kèm chứng từ gốc, đảm bảo truy vết 100% đường đi của từng chiếc.'"
        ],
        title="NHIỆM VỤ WORD & VẤN ĐÁP CỦA VÕ CÔNG TÂM (TV4)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    # =========================================================================
    # HƯỚNG DẪN TV5: TRẦN CÔNG TÚ
    # =========================================================================
    h5 = doc.add_heading("V. HƯỚNG DẪN VIẾT BÁO CÁO CHO THÀNH VIÊN 5 (TRẦN CÔNG TÚ)", level=1)
    for r in h5.runs:
        r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "• Phân hệ: Executive Dashboard KPI Thời Gian Thực, MPAndroidChart Doanh Số & 9 Báo Cáo Chuyên Sâu.",
            "• Tiêu đề chương trong Word: CHƯƠNG: PHÂN HỆ DASHBOARD ĐIỀU HÀNH & HỆ THỐNG 9 BÁO CÁO KHO CHUYÊN SÂU",
            "",
            "1. Nội dung 1 - Executive Dashboard: 5 thẻ KPI thời gian thực: Tổng giá trị tài sản tồn kho (theo giá vốn đích danh), Doanh số phân phối sỉ, Số đơn sỉ mới, Tồn khả dụng, Tỷ lệ đổi trả (>2% cảnh báo đỏ); dòng Audit Stream.",
            "2. Nội dung 2 - MPAndroidChart Trực Quan: Biểu đồ BarChart/LineChart doanh thu 6 tháng, PieChart cơ cấu chi phí logistics, Bảng xếp hạng Top 10 đồng hồ bán chạy nhất.",
            "3. Nội dung 3 - Hệ thống 9 Báo Cáo Chuyên Sâu: Báo cáo nhập hàng & chi phí, Báo cáo phân phối sỉ theo đại lý, Báo cáo cơ cấu xuất hàng, Báo cáo đổi trả theo dòng máy, Báo cáo hàng chậm luân chuyển (>90 ngày), Báo cáo tài chính lợi nhuận gộp, Sổ đối soát công nợ 2 chiều, Báo cáo Dòng tiền thuần Cashflow, Báo cáo Audit Log.",
            "4. Nội dung 4 - Xuất CSV & In ấn A4: Xuất file CSV vào thư mục Downloads, xem trước và in báo cáo chuẩn A4 bằng PrintManager.",
            "",
            "👉 Câu hỏi vấn đáp hay gặp:",
            "   - Giảng viên hỏi: 'Chỉ số Tổng tài sản tồn kho được tính như thế nào?'",
            "     Trả lời: 'Hệ thống SUM trực tiếp giá vốn đích danh (unitCost) của tất cả Serial đang có trạng thái TRONG_KHO, đảm bảo chính xác 100% không bị sai lệch do tính bình quân.'",
            "   - Giảng viên hỏi: 'Báo cáo Dòng tiền Cashflow khác gì với Báo cáo Doanh thu?'",
            "     Trả lời: 'Doanh thu ghi nhận khi xuất hóa đơn bán (dù đại lý chưa thanh toán). Còn Cashflow là tiền thực thu trừ tiền thực chi, giúp lãnh đạo biết chính xác lượng tiền mặt thực tế đang có.'"
        ],
        title="NHIỆM VỤ WORD & VẤN ĐÁP CỦA TRẦN CÔNG TÚ (TV5)",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # =========================================================================
    # HƯỚNG DẪN TV1 (BÌNH)
    # =========================================================================
    h6 = doc.add_heading("VI. HƯỚNG DẪN TỔNG HỢP CHO NHÓM TRƯỞNG (PHAN BÁ HẢI BÌNH)", level=1)
    for r in h6.runs:
        r.font.name = "Arial"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "1. Dựng file Khung sườn Báo cáo tổng thể (Master Document):",
            "   • Trang bìa chuẩn ĐH Kiến trúc Đà Nẵng (DAU), Khoa CNTT, Giảng viên hướng dẫn, danh sách 5 thành viên.",
            "   • Lời cảm ơn, Mục lục tự động, Danh mục Bảng biểu, Danh mục Hình ảnh.",
            "   • Chương 1: Giới thiệu bài toán B2B Luxury Horology, Kiến trúc MVVM, Room DB v4, SessionManager & RBAC 5 Roles (Bình viết).",
            "   • Chương 2, 3, 4, 5: Copy & paste nguyên vẹn các chương do Quân, Thảo, Tâm, Tú nộp về.",
            "   • Chương 6: Đánh giá kết quả thực nghiệm, Quy chuẩn Git Workflow và Kết luận.",
            "",
            "2. Quy trình kiểm tra & duyệt bài trước khi in:",
            "   • Kiểm tra ảnh chụp màn hình của 4 bạn (không để mờ hoặc vỡ nét).",
            "   • Kiểm tra đồng bộ tên package (com.example.chronovaultwms.*) và các mã Role (SYSTEM_ADMIN, STORE_OWNER, v.v.).",
            "   • Xuất file PDF hoàn chỉnh và in thành 1 cuốn báo cáo đóng bìa kính nộp Giảng viên."
        ],
        title="QUY TRÌNH RÁP BÁO CÁO CỦA NHÓM TRƯỞNG",
        border_color="1B365D",
        bg_color="F8FAFC"
    )

    # Save to disk
    output_filename = "Document/HUONG_DAN_LAM_BAO_CAO_WORD_CHO_TUNG_THANH_VIEN.docx"
    output_path = os.path.join(r"D:\cntt\pbhb", output_filename)
    doc.save(output_path)
    print(f"SUCCESS: Created document at {output_path}")

if __name__ == "__main__":
    build_word_guideline_document()

