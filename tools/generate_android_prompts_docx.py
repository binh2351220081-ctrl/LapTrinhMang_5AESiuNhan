# -*- coding: utf-8 -*-
"""
Script to generate: HUONG_DAN_TRIEN_KHAI_ANDROID_STUDIO_5_THANH_VIEN.docx
Bản Hướng Dẫn & Bộ Prompt Chi Tiết Triển Khai Ứng Dụng Android Studio (Kotlin MVVM)
Đề tài: Hệ Thống Quản Lý Kho Đồng Hồ ChronoVault B2B Wholesale WMS
Nhóm: 5AE Siêu Nhân (Phan Bá Hải Bình, Nguyễn Đắc Quân, Tô Đức Thảo, Võ Công Tâm, Trần Công Tú)
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_android_prompts_document():
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
    hp.text = "CHRONOVAULT B2B WMS • HƯỚNG DẪN TRIỂN KHAI ANDROID STUDIO 5 THÀNH VIÊN"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.style.font.name = "Arial"
    hp.style.font.size = Pt(8)
    hp.style.font.color.rgb = RGBColor(148, 163, 184)
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Bộ Prompt Kỹ Thuật Android Studio • Nhóm 5AE Siêu Nhân • Môn Lập Trình Mạng"
    fp.style.font.name = "Arial"
    fp.style.font.size = Pt(8)
    fp.style.font.color.rgb = RGBColor(148, 163, 184)
    
    # Colors
    C_NAVY = RGBColor(27, 54, 93)      # #1B365D
    C_GOLD = RGBColor(197, 155, 39)    # #C59B27
    C_SLATE = RGBColor(51, 65, 85)     # #334155
    C_GRAY = RGBColor(100, 116, 139)   # #64748B
    
    # Styling helpers
    def set_cell_background(cell, hex_color):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)
        
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
            r_t.font.name = "Arial"
            r_t.font.size = Pt(9.5)
            r_t.font.bold = True
            r_t.font.color.rgb = C_NAVY
            
        for idx, line in enumerate(text_lines):
            r = p.add_run(line if idx == len(text_lines)-1 else line + "\n")
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_SLATE
            
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_prompt_box(doc, prompt_text, prompt_title):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "0F172A") # Dark Navy Black
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="12" w:space="0" w:color="C59B27"/>
                <w:left w:val="single" w:sz="18" w:space="0" w:color="C59B27"/>
                <w:bottom w:val="single" w:sz="12" w:space="0" w:color="C59B27"/>
                <w:right w:val="single" w:sz="12" w:space="0" w:color="C59B27"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        r_t = p.add_run(f"📋 BẢN PROMPT COPY-PASTE (DÙNG CHO AI / ANDROID STUDIO COPILOT):\n{prompt_title}\n\n")
        r_t.font.name = "Courier New"
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(212, 175, 55) # Gold
        
        r_body = p.add_run(prompt_text)
        r_body.font.name = "Courier New"
        r_body.font.size = Pt(8)
        r_body.font.color.rgb = RGBColor(226, 232, 240) # Light Slate Text
        
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # TRANG TIÊU ĐỀ & TỔNG QUAN
    # =========================================================================
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("BỘ MÔN MẠNG MÁY TÍNH & TRUYỀN THÔNG • ĐỒ ÁN LẬP TRÌNH MẠNG\nNHÓM 5AE SIÊU NHÂN (FOURSIUNHAN)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_GOLD
    p_sub.paragraph_format.space_after = Pt(4)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BỘ PROMPT KỸ THUẬT TRIỂN KHAI DỰ ÁN\nAPP ANDROID STUDIO (KOTLIN MVVM)\n")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = C_NAVY
    
    r_title_sub = p_title.add_run("ĐỀ TÀI: HỆ THỐNG QUẢN LÝ KHO ĐỒNG HỒ CAO CẤP CHRONOVAULT B2B WHOLESALE WMS")
    r_title_sub.font.name = "Arial"
    r_title_sub.font.size = Pt(11)
    r_title_sub.font.bold = True
    r_title_sub.font.color.rgb = C_SLATE
    p_title.paragraph_format.space_after = Pt(12)

    add_callout(
        doc,
        [
            "• Mục tiêu tài liệu: Chuẩn hóa toàn bộ kiến trúc ứng dụng Android, mô hình dữ liệu Room/SQLite, giao thức truyền thông mạng và đặc tả 5 bộ Prompt chuyên biệt cho 5 thành viên.",
            "• Yêu cầu kỹ thuật cốt lõi: 100% các thành viên dùng chung chuẩn Data Contract (Models, Enums, DTOs, Repository interfaces), đảm bảo khi ghép nối code (Git Merge) không xảy ra bất kỳ xung đột dữ liệu hay sai lệch logic nghiệp vụ nào.",
            "• Đối tượng áp dụng: Phan Bá Hải Bình (Nhóm trưởng - TV1), Nguyễn Đắc Quân (TV2), Tô Đức Thảo (TV3), Võ Công Tâm (TV4), Trần Công Tú (TV5)."
        ],
        title="📌 NGUYÊN TẮC BẢO ĐẢM TÍNH NHẤT QUÁN TOÀN HỆ THỐNG",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # Bảng phân công 5 thành viên
    tbl_team = doc.add_table(rows=6, cols=4)
    tbl_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_team, color="CBD5E1", sz="4")
    
    t_headers = ["STT / Thành Viên", "Phân Hệ Android Phụ Trách", "Gói Package / Modules Phụ Trách", "Trọng Tâm Nghiệp Vụ Cần Xử Lý"]
    t_widths = [1600, 2400, 2400, 3600]
    
    hdr_row = tbl_team.rows[0]
    for i, title in enumerate(t_headers):
        c = hdr_row.cells[i]
        set_cell_width(c, t_widths[i])
        set_cell_margins(c, top=80, bottom=80, left=60, right=60)
        set_cell_background(c, "1B365D")
        p = c.paragraphs[0]
        r = p.add_run(title)
        r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
        
    team_data = [
        ("TV1: Phan Bá Hải Bình\n(Nhóm trưởng)", "Core Framework, Auth & Quản lý Hàng hóa Master", "com.chronovault.wms.core\ncom.chronovault.wms.auth\ncom.chronovault.wms.product", "Khởi tạo Architecture MVVM, Room DB, Navigation, Master Đồng hồ, ĐVT Thùng/Chiếc, MOQ, Tra cứu Serial Timeline, Audit Log."),
        ("TV2: Nguyễn Đắc Quân", "Đối tác Nhà Cung Cấp & Quản lý Nhập Kho", "com.chronovault.wms.supplier\ncom.chronovault.wms.inbound", "Hồ sơ NCC, Phiếu nhập kho, Tích hợp Camera Barcode/ZXing nạp Serial, Quy đổi ĐVT, Tính Giá vốn đích danh, Phiếu Chi nợ NCC."),
        ("TV3: Tô Đức Thảo", "Khách Sỉ & Bán Sỉ - Phân Phối Xuất Hàng", "com.chronovault.wms.dealer\ncom.chronovault.wms.outbound", "Hồ sơ đại lý B2B, Hạn mức tín dụng, Đơn bán sỉ, Duyệt khóa giữ chỗ (Reserved), Quét Serial đóng kiện xuất sỉ, Phiếu Thu sỉ, Đổi trả sỉ."),
        ("TV4: Võ Công Tâm", "Tồn Kho, Vị Trí Kệ Vật Lý & Kiểm Kê", "com.chronovault.wms.inventory\ncom.chronovault.wms.audit", "Tồn kho đa đơn vị, 3 kho chất lượng (Mới/Trưng bày/Lỗi), Sơ đồ kệ Bin [Khu-Dãy-Tầng-Ngăn], Quét kiểm kê Camera, Phiếu cân bằng kho, Sổ Thẻ kho."),
        ("TV5: Trần Công Tú", "Dashboard Điều Hành & Báo Cáo Thống Kê", "com.chronovault.wms.dashboard\ncom.chronovault.wms.reports", "Executive Dashboard KPI, Vẽ biểu đồ MPAndroidChart doanh số/chi phí 6 tháng, Top sản phẩm bán chạy, 9 Báo cáo chuyên sâu, Sổ nợ 2 chiều, Dòng tiền.")
    ]
    
    for r_i, r_vals in enumerate(team_data, start=1):
        row = tbl_team.rows[r_i]
        bg = "FFFFFF" if r_i % 2 == 1 else "F8FAFC"
        for c_i, val in enumerate(r_vals):
            cell = row.cells[c_i]
            set_cell_width(cell, t_widths[c_i])
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Arial"; r.font.size = Pt(8)
            if c_i == 0:
                r.font.bold = True
                r.font.color.rgb = C_NAVY
            elif c_i == 2:
                r.font.name = "Courier New"
                r.font.size = Pt(7.5)
                r.font.color.rgb = C_SLATE
            else:
                r.font.color.rgb = C_SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # PHẦN I: MASTER DATA CONTRACT (HỢP ĐỒNG DỮ LIỆU DÙNG CHUNG)
    # =========================================================================
    h1 = doc.add_heading("I. HỢP ĐỒNG DỮ LIỆU DÙNG CHUNG (MASTER DATA CONTRACT)", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    for r in h1.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(6)
    r_int = p_intro.add_run(
        "Để đảm bảo khi 5 thành viên lập trình độc lập trên Android Studio và merge code qua Git không xảy ra xung đột, "
        "toàn bộ các Entity, Enums, Room Database Tables và Constants bắt buộc phải tuân thủ hợp đồng mã nguồn sau đây. "
        "TV1 sẽ khởi tạo các file này vào thư mục core/data/model để các thành viên khác sử dụng:"
    )
    r_int.font.name = "Arial"; r_int.font.size = Pt(9); r_int.font.color.rgb = C_SLATE

    # Code block Master Contract
    contract_code = """// ==========================================
// 1. CÁC ENUM CHUẨN HOÁ DÙNG CHUNG TOÀN HỆ THỐNG
// ==========================================
enum class UserRole(val roleName: String) {
    SYSTEM_ADMIN("Quản trị hệ thống"),
    STORE_OWNER("Chủ cửa hàng"),
    WAREHOUSE_MANAGER("Thủ kho (quản lý điều hành)"),
    OPERATIONS_STAFF("Nhân viên nhập - xuất kho"),
    ACCOUNTANT("Kế toán kho")
}
enum class MovementType { AUTOMATIC, QUARTZ, SOLAR_ECODRIVE }
enum class SerialLifecycleStatus { TRONG_KHO, DA_BAN, BAO_HANH, DA_TRA_NCC, DA_TIEU_HUY }
enum class QualityStatus { HANG_MOI, HANG_TRUNG_BAY, HANG_LOI }
enum class DealerTier { VIP, BAC, DONG }
enum class PaymentTerm { THANH_TOAN_NGAY, NET_15, NET_30 }
enum class OrderStatus { DRAFT, APPROVED, PACKING, COMPLETED, CANCELLED }
enum class InboundStatus { DRAFT, APPROVED, CANCELLED }
enum class PaymentMethod { CHUYEN_KHOAN, TIEN_MAT }
enum class StockAuditScope { TOAN_KHO, DAY_KE, THUONG_HIEU }
enum class StockLedgerRefType { NHAP, XUAT_SI, DOI_TRA_SI, TRA_NCC, XUAT_BAO_HANH, XUAT_HUY, CAN_BANG_KIEM_KE }

// ==========================================
// 2. CÁC DATA CLASS / ROOM ENTITIES CỐT LÕI
// ==========================================
@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey val id: String, // SKU duy nhất (ví dụ: "RLX-SUB-01")
    val barcode: String,        // Mã vạch quốc tế
    val name: String,           // Tên mẫu đồng hồ
    val brand: String,          // Hãng sản xuất (Rolex, Omega, Tissot...)
    val movement: MovementType, // Phân loại bộ máy
    val dialSize: Double,       // Kích thước mặt số mm (36.0, 40.0...)
    val glass: String,          // Kính Sapphire chống lóa / Hardlex
    val strap: String,          // Dây Oystersteel / Da cá sấu
    val waterResist: String,    // Độ chịu nước (30m, 100m, 300m)
    val warrantyMonths: Int,    // Bảo hành hãng (tháng)
    val baseUnit: String = "Chiếc",
    val wholesaleUnit: String = "Thùng",
    val conversionRate: Int = 10,  // 1 Thùng = 10 Chiếc
    val moq: Int = 5,              // Số lượng đặt tối thiểu sỉ
    val minStock: Int = 10,        // Cảnh báo vàng sắp hết
    val maxStock: Int = 100,       // Cảnh báo đỏ vượt tồn
    val wholesalePriceVip: Double,
    val wholesalePriceSilver: Double,
    val wholesalePriceBronze: Double,
    val baseCost: Double,
    val shelfLocationId: String,   // Mã vị trí kệ gán cố định
    val hasSerial: Boolean = true,
    val isActive: Boolean = true
)

@Entity(tableName = "serials")
data class SerialEntity(
    @PrimaryKey val serialNumber: String, // Mã Serial đích danh do hãng cấp
    val productId: String,                // FK -> products.id (SKU)
    val costPrice: Double,                // Giá vốn đích danh (đã cộng chi phí phân bổ)
    val lifecycleStatus: SerialLifecycleStatus = SerialLifecycleStatus.TRONG_KHO,
    val qualityStatus: QualityStatus = QualityStatus.HANG_MOI,
    val shelfLocationId: String,          // FK -> shelves.id (Vị trí ngăn kệ hiện tại)
    val supplierId: String,               // FK -> suppliers.id
    val receiptCode: String,              // FK -> receipts.code (Mã phiếu nhập sinh ra)
    val dealerId: String? = null,         // FK -> dealers.id (Đại lý sở hữu sau khi bán)
    val orderCode: String? = null,        // FK -> orders.code (Mã đơn bán sỉ)
    val warrantyExpireDate: Long? = null  // Timestamp hết hạn bảo hành
)

@Entity(tableName = "stock_cards")
data class StockCardEntity(
    @PrimaryKey(autoGenerate = true) val cardId: Long = 0,
    val timestamp: Long,                  // Mốc thời gian biến động
    val productId: String,                // SKU đồng hồ
    val refType: StockLedgerRefType,      // Loại giao dịch
    val refCode: String,                  // Mã chứng từ (PN-xxxx, DS-xxxx, KK-xxxx...)
    val changeQty: Int,                   // Biến động (+ khi nhập/trả, - khi xuất)
    val balanceAfter: Int,                // Tồn kho thực tế sau biến động
    val serialNumber: String,             // Mã Serial đích danh biến động
    val actor: String,                    // Người thực hiện giao dịch
    val note: String? = null              // Ghi chú chi tiết
)"""

    add_prompt_box(doc, contract_code, "DATA CONTRACT CHUNG: KOTLIN ROOM ENTITIES & ENUMS (CORE ARCHITECTURE)")

    # =========================================================================
    # PHẦN II: BỘ PROMPT CHI TIẾT CHO 5 THÀNH VIÊN
    # =========================================================================
    h2 = doc.add_heading("II. BỘ PROMPT CHI TIẾT CHO TỪNG THÀNH VIÊN TRIỂN KHAI", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    for r in h2.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    # -------------------------------------------------------------
    # PROMPT 1: TV1 - PHAN BÁ HẢI BÌNH (NHÓM TRƯỞNG)
    # -------------------------------------------------------------
    doc.add_heading("1. PROMPT CHO THÀNH VIÊN 1: PHAN BÁ HẢI BÌNH (NHÓM TRƯỞNG & CORE + HÀNG HÓA)", level=2)
    
    add_callout(
        doc,
        [
            "• Vai trò: Nhóm trưởng kiến trúc & Trưởng phân hệ 1.",
            "• Trách nhiệm: Thiết lập dự án Android Studio mẫu chuẩn (Clean MVVM), tích hợp Room Database, Navigation Component, xác thực đăng nhập, phân quyền RBAC ma trận 5 vai trò, Audit Log và quản trị danh mục Đồng hồ Master, cấu hình ĐVT quy đổi, MOQ, tra cứu vòng đời Serial (Serial Timeline)."
        ],
        title="MỤC TIÊU PHÂN HỆ 1 (TV1 - PHAN BÁ HẢI BÌNH)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    p1_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CAO CẤP VÀ NHÓM TRƯỞNG DỰ ÁN. HÃY THỰC HIỆN CÁC NHIỆM VỤ DƯỚI ĐÂY BẰNG KOTLIN VÀ ANDROID STUDIO THEO KIẾN TRÚC MVVM:

1. KHỞI TẠO DỰ ÁN VÀ KIẾN TRÚC CHUNG (CORE ARCHITECTURE):
   - Package gốc: com.chronovault.wms
   - Cấu trúc thư mục chuẩn:
     + core/ (data, database, di, network, utils, base)
     + auth/ (login, session, rbac, auditlog)
     + product/ (ui, viewmodel, repository, adapter)
   - Thiết lập Room Database (ChronoVaultDatabase) chứa đủ các bảng: products, serials, suppliers, dealers, orders, receipts, shelves, stock_audits, stock_cards, vouchers, audit_logs.
   - Định nghĩa toàn bộ Enums và Data Contract dùng chung như trong tài liệu Master Data Contract.
   - Cung cấp sẵn cơ chế Seed Data (khởi tạo dữ liệu mẫu 10 sản phẩm đồng hồ cao cấp: Rolex Submariner, Omega Speedmaster, Tissot Le Locle, Seiko Prospex... kèm các mã Serial mẫu để các thành viên khác có dữ liệu test ngay lập tức).

2. PHÂN HỆ XÁC THỰC, PHÂN QUYỀN RBAC & AUDIT LOG:
   - Xây dựng màn hình Đăng nhập (LoginActivity) xác thực tài khoản và gán đúng 1 trong 5 vai trò (QUAN_TRI_HE_THONG, CHU_CUA_HANG, THU_KHO, NHAN_VIEN_NHAP_XUAT, KE_TOAN).
   - Xây dựng SessionManager (sử dụng EncryptedSharedPreferences) để lưu phiên đăng nhập và token an toàn.
   - Tạo ma trận phân quyền (RolePermissionManager): Kiểm tra quyền trước khi người dùng truy cập vào các chức năng (Thêm, Sửa, Xóa, Duyệt chi, Duyệt xuất kho).
   - Xây dựng tính năng Audit Log (AuditLogManager): Mỗi thao tác thêm/sửa/xóa/duyệt đều tự động ghi 1 dòng log bất biến gồm: timestamp, username, role, action, targetEntity, ip/deviceInfo.

3. QUẢN LÝ HÀNG HÓA MASTER & TRA CỨU SERIAL TIMELINE:
   - Xây dựng ProductListFragment / Activity: Hiển thị danh sách đồng hồ dạng RecyclerView CardView cao cấp (nền đen Onyx #0B0F17, viền vàng Gold #D4AF37), hiển thị hình ảnh, SKU, Barcode, thương hiệu, giá sỉ, tồn kho thực tế; hỗ trợ phân trang và tìm kiếm theo cơ chế Debounce.
   - Xây dựng AddEditProductDialog / Activity: Form khai báo đầy đủ 6 thông số kỹ thuật ngành xa xỉ (loại máy, chất liệu kính, dây đeo, size mặt số, độ chịu nước, thời hạn bảo hành).
   - Cấu hình đóng gói sỉ: Thiết lập ĐVT cơ bản (Chiếc), ĐVT sỉ (Thùng), hệ số quy đổi (conversionRate, VD: 1 Thùng = 10 Chiếc), cấu hình ngưỡng Min/Max tồn kho và số lượng đặt hàng tối thiểu (MOQ >= 5 chiếc).
   - Xây dựng SerialTimelineActivity (Tra cứu vòng đời Serial): Người dùng nhập hoặc quét 1 mã Serial bất kỳ -> Hệ thống hiển thị trực quan toàn bộ dòng thời gian: Ngày nhập kho -> NCC cung cấp -> Vị trí kệ lưu trữ -> Đơn bán sỉ xuất kho -> Đại lý sở hữu -> Ngày hết hạn bảo hành.

YÊU CẦU ĐẦU RA:
- Mã nguồn Kotlin sạch, tuân thủ MVVM (ViewModel, StateFlow/LiveData, Repository, Room DAO).
- Đóng gói đầy đủ layout XML giao diện Horology Luxury Dark Mode."""

    add_prompt_box(doc, p1_text, "PROMPT TV1 (PHAN BÁ HẢI BÌNH): CORE SETUP, AUTH, RBAC & MASTER HÀNG HÓA")

    # -------------------------------------------------------------
    # PROMPT 2: TV2 - NGUYỄN ĐẮC QUÂN
    # -------------------------------------------------------------
    doc.add_heading("2. PROMPT CHO THÀNH VIÊN 2: NGUYỄN ĐẮC QUÂN (NCC & QUẢN LÝ NHẬP KHO)", level=2)
    
    add_callout(
        doc,
        [
            "• Vai trò: Phụ trách Phân hệ 2.",
            "• Trách nhiệm: Quản lý hồ sơ Nhà Cung Cấp, theo dõi nợ phải trả, tích hợp Camera quét mã vạch ZXing/ML Kit nạp Serial, tự động quy đổi Thùng ra Chiếc, tính Giá vốn đích danh phân bổ chi phí, lập phiếu Chi nợ NCC và xuất trả hàng lỗi NCC."
        ],
        title="MỤC TIÊU PHÂN HỆ 2 (TV2 - NGUYỄN ĐẮC QUÂN)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    p2_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ NHẬP KHO VÀ ĐỐI TÁC NHÀ CUNG CẤP. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.chronovault.wms.supplier` VÀ `com.chronovault.wms.inbound` BẰNG KOTLIN:

1. QUẢN LÝ HỒ SƠ NHÀ CUNG CẤP & CÔNG NỢ PHẢI TRẢ:
   - Danh bạ Nhà Cung Cấp chính hãng (SupplierListFragment): Hiển thị mã NCC, tên công ty, mã số thuế, hotline, số tài khoản ngân hàng và tổng số dư nợ phải trả.
   - Thêm/Sửa NCC: Kiểm tra tính duy nhất của mã NCC và MST.
   - Theo dõi công nợ NCC: Tự động cộng nợ khi phiếu nhập kho được duyệt; trừ nợ khi lập Phiếu Chi thanh toán.
   - Lập Phiếu Chi thanh toán nợ (PaymentVoucherDialog): Nhập số tiền chi trả, hình thức chuyển khoản/tiền mặt, mã tham chiếu ngân hàng; cập nhật giảm số dư nợ NCC.

2. LẬP PHIẾU NHẬP KHO QUY ĐỔI ĐVT & QUÉT CAMERA SERIAL (INBOUND WORKFLOW):
   - Xây dựng CreateInboundReceiptActivity:
     + Bước 1: Chọn Nhà Cung Cấp và nhập số hóa đơn / Invoice vận chuyển.
     + Bước 2: Chọn mẫu đồng hồ (SKU) và chọn ĐVT nhập là "Thùng" hoặc "Chiếc".
     + Bước 3: Cơ chế quy đổi tự động: Khi người dùng nhập số Thùng, hệ thống lấy conversionRate từ ProductEntity để tính ra tổng số chiếc lẻ (Ví dụ: Nhập 3 Thùng -> Yêu cầu nạp đủ 30 mã Serial).
     + Bước 4: Tích hợp Camera Barcode Scanner (Sử dụng Google ML Kit Barcode Scanning hoặc ZXing Embedded): Quét liên tục từng mã Serial in trên hộp/tem đồng hồ. Có âm thanh 'beep' xác nhận mỗi lần quét thành công.
     + Bước 5: Kiểm tra đối soát 2 chiều nghiêm ngặt:
       * Tổng số mã Serial quét được PHẢI BẰNG CHÍNH XÁC tổng số chiếc sau quy đổi (không cho duyệt nếu thiếu/thừa).
       * Chặn hoàn toàn và báo lỗi đỏ nếu phát hiện bất kỳ mã Serial nào đã tồn tại trong bảng `serials` của Room DB (chống trùng lặp tuyệt đối).

3. PHÂN BỔ CHI PHÍ & TÍNH TOÁN GIÁ VỐN ĐÍCH DANH (SPECIFIC IDENTIFICATION COSTING):
   - Trong phiếu nhập, kế toán khai báo các chi phí phát sinh thực tế: cước vận chuyển quốc tế, thuế quan hải quan, bảo hiểm lô hàng.
   - Tự động phân bổ đều chi phí vào từng chiếc đồng hồ theo công thức bắt buộc:
     Giá vốn Serial = Đơn giá mua trên HĐ + (Tổng chi phí phân bổ / Tổng số chiếc)
   - Lưu trữ từng Serial vào bảng `serials` với giá vốn đích danh này, gán trạng thái `TRONG_KHO` và chất lượng `HANG_MOI`.
   - Cập nhật tăng tồn kho vật lý tại Room DB, ghi nhận tăng công nợ NCC và sinh bản ghi Sổ Thẻ kho (+) tương ứng.

4. XUẤT TRẢ HÀNG LỖI CHO NCC (SUPPLIER RETURN):
   - Cho phép chọn NCC, quét/chọn các mã Serial từ Kho Hàng Lỗi (`HANG_LOI`), ghi lý do kỹ thuật (hỏng máy, hấp hơi nước, trầy xước từ hãng).
   - Sau khi duyệt: Chuyển Serial sang trạng thái `DA_TRA_NCC`, giảm tồn kho lỗi và tự động cấn trừ số tiền tương ứng vào công nợ phải trả NCC.

YÊU CẦU ĐẦU RA:
- Kết nối chính xác với Room Database do TV1 thiết kế.
- Luồng quét camera mượt mà, hỗ trợ cả dán danh sách Serial bằng tay nếu camera không tiện."""

    add_prompt_box(doc, p2_text, "PROMPT TV2 (NGUYỄN ĐẮC QUÂN): NHÀ CUNG CẤP, NHẬP KHO QUÉT SERIAL & GIÁ VỐN ĐÍCH DANH")

    # -------------------------------------------------------------
    # PROMPT 3: TV3 - TÔ ĐỨC THẢO
    # -------------------------------------------------------------
    doc.add_heading("3. PROMPT CHO THÀNH VIÊN 3: TÔ ĐỨC THẢO (KHÁCH SỈ & BÁN SỈ - XUẤT HÀNG)", level=2)
    
    add_callout(
        doc,
        [
            "• Vai trò: Phụ trách Phân hệ 3.",
            "• Trách nhiệm: Quản lý hồ sơ đại lý sỉ B2B, phân hạng và kiểm soát hạn mức tín dụng (Credit Limit), lên đơn bán sỉ, áp giá sỉ tự động, thẩm định nợ & duyệt khóa hàng giữ chỗ (Reserved), quét Serial đóng kiện xuất sỉ, thu tiền cọc/nợ và tiếp nhận đổi trả sỉ."
        ],
        title="MỤC TIÊU PHÂN HỆ 3 (TV3 - TÔ ĐỨC THẢO)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    p3_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ ĐẠI LÝ B2B VÀ BÁN SỈ XUẤT KHO. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.chronovault.wms.dealer` VÀ `com.chronovault.wms.outbound` BẰNG KOTLIN:

1. QUẢN LÝ ĐẠI LÝ B2B & HẠN MỨC CÔNG NỢ TÍN DỤNG (CREDIT LIMIT):
   - Danh sách đại lý sỉ (DealerListFragment): Quản lý 100% đối tác là cửa hàng/chuỗi bán lẻ; phân loại 3 cấp bậc (VIP, BAC, DONG); hiển thị hạn mức tín dụng (Credit Limit) và số dư nợ hiện tại.
   - Thêm/Sửa hồ sơ đại lý: Cấu hình tỷ lệ chiết khấu hợp đồng và thời hạn nợ (Net 15 / Net 30).
   - Lập Phiếu Thu tiền sỉ (DealerReceiptDialog): Thu tiền cọc đơn hàng hoặc thu nợ đại lý; cập nhật giảm số dư nợ và tự động khôi phục hạn mức mua hàng khả dụng.

2. LÊN ĐƠN BÁN SỈ & DUYỆT KHÓA GIỮ CHỖ TỒN KHO (RESERVED ALLOCATION):
   - Xây dựng CreateWholesaleOrderActivity:
     + Chọn đại lý B2B -> Hệ thống tự động nhận diện cấp bậc (VIP/Bạc/Đồng).
     + Thêm sản phẩm theo Thùng hoặc Chiếc lẻ.
     + Ràng buộc bắt buộc 1: Kiểm tra MOQ (Số lượng đặt phải >= MOQ quy định cho từng mẫu).
     + Ràng buộc bắt buộc 2: Tự động áp giá sỉ theo cấp bậc đại lý (VIP được giá tốt nhất) và tính chiết khấu thương mại.
     + Ràng buộc bắt buộc 3: Kiểm tra tồn kho khả dụng (Available = Thực tế - Đang giữ chỗ Reserved). Chặn lên đơn nếu vượt tồn khả dụng.
     + Ràng buộc bắt buộc 4: Thẩm định hạn mức nợ tín dụng:
       Dư nợ hiện tại + Giá trị đơn mới - Tiền cọc <= Hạn mức tín dụng của đại lý.
       Nếu vượt hạn mức, hệ thống yêu cầu cờ duyệt ngoại lệ từ Chủ cửa hàng.
     + Sau khi duyệt đơn: Chuyển đơn sang trạng thái `APPROVED`, đồng thời KHÓA SỐ LƯỢNG HÀNG GIỮ CHỖ (Tăng `reservedQty`, giảm `availableQty`) để ngăn không cho đơn khác bán trùng lặp.
     + Nếu đơn hàng bị hủy: Tự động giải phóng số lượng giữ chỗ, trả lại cho tồn khả dụng ngay lập tức.

3. QUÉT SERIAL ĐÓNG KIỆN & THỰC XUẤT KHO BÁN SỈ (OUTBOUND DISPATCH):
   - Xây dựng DispatchOrderActivity (Quét Serial đóng gói giao hàng):
     + Dựa trên đơn bán sỉ đã duyệt, thủ kho lấy hàng trên kệ và dùng camera quét mã Serial từng chiếc đóng vào kiện.
     + Đối soát thời gian thực:
       * Mã Serial quét vào PHẢI thuộc đúng mã SKU yêu cầu trên đơn.
       * Serial phải đang có trạng thái `TRONG_KHO` và chất lượng `HANG_MOI`.
       * Không bị quét trùng trong cùng kiện hàng.
     + Khi quét đủ 100% số lượng: Bấm "Xác nhận xuất kho" -> Hệ thống thực hiện đồng thời:
       * Giảm tồn thực tế và giải phóng tồn giữ chỗ.
       * Cập nhật Serial sang trạng thái `DA_BAN`, gán mã đại lý sở hữu và tính ngày hết hạn bảo hành.
       * Tăng số dư nợ của đại lý (trừ đi tiền cọc đã nộp) và ghi Sổ Thẻ kho (-).
       * Sinh Biên bản bàn giao hàng hóa kiêm phiếu xuất kho B2B hiển thị danh sách 100% mã Serial đã xuất.

4. TIẾP NHẬN ĐỔI TRẢ SỈ & XUẤT KHÁC (BẢO HÀNH/HỦY):
   - Tiếp nhận đổi trả: Quét mã Serial đại lý trả về để kiểm tra nguồn gốc bán ra từ hệ thống.
   - Phân loại chất lượng: Đưa về `HANG_MOI` (nguyên seal đổi mẫu) hoặc đưa về `HANG_LOI` (hỏng kỹ thuật); tự động cấn trừ tiền vào nợ đại lý.
   - Phiếu xuất khác: Cho phép lập phiếu xuất gửi về Trung tâm bảo hành của hãng hoặc xuất tiêu hủy hàng vỡ nát.

YÊU CẦU ĐẦU RA:
- Đảm bảo logic tính toán tài chính và tồn kho liên kết chuẩn xác với Room DB của TV1."""

    add_prompt_box(doc, p3_text, "PROMPT TV3 (TÔ ĐỨC THẢO): ĐẠI LÝ B2B, BÁN SỈ, KHÓA GIỮ CHỖ & QUÉT XUẤT SERIAL")

    # -------------------------------------------------------------
    # PROMPT 4: TV4 - VÕ CÔNG TÂM
    # -------------------------------------------------------------
    doc.add_heading("4. PROMPT CHO THÀNH VIÊN 4: VÕ CÔNG TÂM (TỒN KHO, VỊ TRÍ KỆ & KIỂM KÊ)", level=2)
    
    add_callout(
        doc,
        [
            "• Vai trò: Phụ trách Phân hệ 4.",
            "• Trách nhiệm: Giám sát tồn kho đa đơn vị (Thùng + Chiếc) và 3 kho chất lượng (Mới/Trưng bày/Lỗi), quản lý sơ đồ ngăn kệ vật lý [Khu-Dãy-Tầng-Ngăn], tổ chức kiểm kê quét Serial bằng Camera, đối soát chênh lệch Thừa/Thiếu, lập phiếu cân bằng kho và quản lý Sổ Thẻ kho bất biến."
        ],
        title="MỤC TIÊU PHÂN HỆ 4 (TV4 - VÕ CÔNG TÂM)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    p4_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ QUẢN LÝ TỒN KHO VẬT LÝ, VỊ TRÍ KỆ VÀ KIỂM KÊ. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.chronovault.wms.inventory` VÀ `com.chronovault.wms.audit` BẰNG KOTLIN:

1. THEO DÕI TỒN KHO ĐA ĐƠN VỊ & 3 KHO CHẤT LƯỢNG:
   - Xây dựng StockOverviewFragment:
     + Hiển thị số lượng tồn kho theo cả 2 đơn vị: Đơn vị sỉ (Thùng/Kiện) và Đơn vị lẻ (Chiếc).
     + Phân tách rõ ràng 3 chỉ số quan trọng cho từng mẫu đồng hồ:
       * Tồn thực tế (In-Stock)
       * Tồn giữ chỗ (Reserved)
       * Tồn khả dụng bán sỉ (Available = Thực tế - Giữ chỗ).
     + Thiết kế 3 Tab phân loại chất lượng độc lập:
       * Kho Hàng Mới (New Stock): Đủ điều kiện xuất sỉ.
       * Kho Hàng Trưng Bày (Display Stock): Hàng mở mẫu cho đại lý xem.
       * Kho Hàng Lỗi (Defect Stock): Hàng phát sinh lỗi kỹ thuật chờ trả hãng.
   - Tính toán tổng giá trị tồn kho bằng cách cộng dồn 100% Giá vốn đích danh của các mã Serial đang có mặt trong kho; không dùng bình quân giản đơn.
   - Cảnh báo định mức tồn kho tự động:
     * Cảnh báo màu vàng khi tồn kho <= minStock (nhắc lập PO nhập thêm).
     * Cảnh báo màu đỏ khi tồn khả dụng = 0 (hết hàng ngừng nhận đơn).
     * Cảnh báo vượt maxStock (tránh ứ đọng vốn).

2. SƠ ĐỒ VỊ TRÍ KỆ KHO VẬT LÝ (BIN LOCATION MANAGEMENT):
   - Quản lý mã định danh vị trí kệ theo cấu trúc chuẩn: [Khu vực - Dãy kệ - Tầng kệ - Ngăn chứa] (Ví dụ: "Khu A - Dãy A-01 - Tầng 2 - Ngăn Rolex").
   - Trực quan hóa sơ đồ mặt bằng kệ (Grid / RecyclerView): Hiển thị sức chứa tối đa, số lượng Serial hiện lưu trên từng ngăn kệ và thanh tiến độ phần trăm lấp đầy (Capacity Progress Bar). Đổi màu đỏ khi kệ đầy 100%.
   - Chức năng điều chuyển ngăn kệ: Cho phép quét Serial và chọn vị trí kệ mới để cập nhật vị trí lưu kho của chiếc đồng hồ.

3. KIỂM KÊ KHO & TỰ ĐỘNG ĐỐI SOÁT CHÊNH LỆCH SERIAL:
   - Xây dựng StockAuditActivity:
     + Khởi tạo đợt kiểm kê theo phạm vi: Toàn kho, Theo dãy kệ, hoặc Theo thương hiệu.
     + Cơ chế tạm khóa xuất nhập: Khi đợt kiểm kê kích hoạt, hệ thống tạm khóa biến động xuất/nhập trên các ngăn kệ kiểm kê để đảm bảo tính chính xác.
     + Quét kiểm đếm thực tế bằng Camera: Thủ kho dùng camera quét nhanh toàn bộ mã Serial thực tế hiện diện trên kệ.
     + Đối soát tự động thời gian thực:
       * Serial Khớp đúng: Trùng khớp cả vị trí và trạng thái trong CSDL.
       * Serial Thừa: Có mặt thực tế trên kệ nhưng CSDL không ghi nhận ở kệ này.
       * Serial Thiếu: CSDL báo có nhưng thực tế quét không thấy.
     + Hiển thị bảng đối soát phân màu rõ ràng (Xanh: Khớp, Vàng: Thừa, Đỏ: Thiếu).

4. PHIẾU CÂN BẰNG KHO & SỔ THẺ KHO ĐIỆN TỬ (STOCK LEDGER):
   - Lập phiếu cân bằng kho sau kiểm kê: Điều chỉnh số liệu sổ sách khớp đúng với thực tế đếm được; ghi rõ lý do và người chịu trách nhiệm. (Chênh lệch giá trị lớn > 10 triệu bắt buộc Chủ cửa hàng duyệt).
   - Xây dựng StockCardActivity (Sổ Thẻ kho điện tử):
     + Truy vấn nhật ký biến động của từng mã SKU: Ngày phát sinh, loại chứng từ (Nhập, Xuất sỉ, Đổi trả, Cân bằng kiểm kê), số lượng (+/-) và danh sách mã Serial liên quan.
     + Đảm bảo tính bất biến (Immutability): Dữ liệu Thẻ kho tuyệt đối cấm sửa/xóa; nếu sai sót phải lập phiếu điều chỉnh đối ứng.

YÊU CẦU ĐẦU RA:
- Giao diện trực quan, thao tác nhanh, hỗ trợ thủ kho làm việc linh hoạt trong môi trường kho thực tế."""

    add_prompt_box(doc, p4_text, "PROMPT TV4 (VÕ CÔNG TÂM): TỒN KHO 3 CHẤT LƯỢNG, SƠ ĐỒ KỆ BIN, KIỂM KÊ & SỔ THẺ KHO")

    # -------------------------------------------------------------
    # PROMPT 5: TV5 - TRẦN CÔNG TÚ
    # -------------------------------------------------------------
    doc.add_heading("5. PROMPT CHO THÀNH VIÊN 5: TRẦN CÔNG TÚ (DASHBOARD & HỆ THỐNG BÁO CÁO)", level=2)
    
    add_callout(
        doc,
        [
            "• Vai trò: Phụ trách Phân hệ 5.",
            "• Trách nhiệm: Xây dựng Executive Dashboard điều hành thời gian thực, tích hợp thư viện MPAndroidChart vẽ biểu đồ doanh số/chi phí 6 tháng, bảng xếp hạng Top sản phẩm bán chạy, hệ thống 9 báo cáo chuyên sâu đa phân hệ, sổ chi tiết công nợ 2 chiều và báo cáo dòng tiền thuần Cashflow."
        ],
        title="MỤC TIÊU PHÂN HỆ 5 (TV5 - TRẦN CÔNG TÚ)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    p5_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ BÁO CÁO VÀ DASHBOARD ĐIỀU HÀNH. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.chronovault.wms.dashboard` VÀ `com.chronovault.wms.reports` BẰNG KOTLIN:

1. EXECUTIVE DASHBOARD & THẺ CHỈ SỐ KPI THỜI GIAN THỰC:
   - Xây dựng DashboardFragment (Màn hình trung tâm điều hành):
     + Hiển thị 5 thẻ chỉ số hiệu suất trọng yếu (KPI Cards) phong cách Horology Luxury:
       * Tổng giá trị tài sản tồn kho: Tính chuẩn xác theo giá vốn đích danh của từng Serial trong kho.
       * Doanh thu phân phối sỉ: Doanh số tích lũy từ các đơn hàng xuất bán cho đại lý trong kỳ.
       * Số lượng đơn bán sỉ mới.
       * Tổng tồn kho khả dụng cung ứng.
       * Tỷ lệ đổi trả hàng sỉ (Cảnh báo đỏ nếu vượt ngưỡng an toàn > 2.0%).
     + Dòng thời gian hoạt động gần đây (Audit Activity Stream): Hiển thị danh sách các thao tác quan trọng vừa phát sinh trong kho (nhập mới, duyệt đơn sỉ, thu tiền nợ, kiểm kê kệ...).

2. BIỂU ĐỒ TRỰC QUAN DOANH SỐ & CHI PHÍ BẰNG MPANDROIDCHART:
   - Tích hợp thư viện `com.github.PhilJay:MPAndroidChart:v3.1.0`.
   - Biểu đồ BarChart / LineChart xu hướng doanh thu phân phối sỉ 6 tháng gần nhất kèm tỷ lệ tăng trưởng.
   - Biểu đồ PieChart cơ cấu chi phí phát sinh: Cước vận chuyển quốc tế, thuế hải quan, bảo hiểm lô hàng, phí lưu kho.
   - Bảng xếp hạng Top 5 / Top 10 mẫu đồng hồ bán chạy nhất kênh sỉ (xếp theo sản lượng chiếc bán ra và theo doanh thu).

3. HỆ THỐNG 9 BÁO CÁO CHUYÊN SÂU ĐA PHÂN HỆ:
   - Xây dựng ReportContainerFragment với bộ lọc thời gian (Từ ngày - Đến ngày) và xuất 9 báo cáo chuyên sâu:
     1. Báo cáo Nhập hàng (Inbound Report): Số lượng và giá trị nhập theo từng NCC, cơ cấu chi phí phân bổ.
     2. Báo cáo Phân phối Bán sỉ (Outbound Report): Doanh số theo từng đại lý, tỷ lệ hoàn tất đơn hàng.
     3. Báo cáo Cơ cấu xuất hàng: Tỷ trọng xuất bán sỉ vs Xuất gửi bảo hành hãng vs Xuất tiêu hủy hàng hỏng.
     4. Báo cáo Đổi trả & Chất lượng bộ máy: Phân tích tỷ lệ lỗi theo từng hãng và theo dòng máy (Automatic, Quartz, Solar) phục vụ đàm phán hợp đồng với NCC.
     5. Báo cáo Hàng chậm luân chuyển (Dead Stock Aging): Liệt kê các mẫu đồng hồ có thời gian lưu kho > 90 ngày hoặc > 180 ngày để đề xuất thanh lý thu hồi vốn.
     6. Báo cáo Tài chính & Lợi nhuận gộp B2B: Doanh thu bán sỉ trừ Giá vốn đích danh trừ Chi phí logistics = Lợi nhuận gộp thực tế.
     7. Sổ chi tiết công nợ B2B 2 chiều: Đối soát chi tiết từng đại lý và nhà cung cấp (Dư nợ đầu kỳ, Phát sinh nợ, Phát sinh có, Dư nợ cuối kỳ).
     8. Báo cáo Dòng tiền Thu / Chi thực tế (Cashflow Report): Dòng tiền thu vào (bán sỉ, thu hồi nợ) trừ Dòng tiền chi ra (trả NCC, chi phí) = Dòng tiền thuần (Net Cashflow).
     9. Báo cáo Nhật ký kiểm toán Audit Log toàn hệ thống.

4. XUẤT BÁO CÁO (EXPORT CSV / PDF / IN ẤN):
   - Hỗ trợ nút "Xuất file CSV / Excel" lưu vào thư mục Downloads của điện thoại để người dùng gửi qua Zalo / Email.
   - Hỗ trợ xem trước và in báo cáo định dạng chuẩn A4 qua Android PrintManager.

YÊU CẦU ĐẦU RA:
- Giao diện báo cáo trực quan, biểu đồ mượt mà, tính toán số liệu khớp đúng 100% với dữ liệu giao dịch của 4 phân hệ kia."""

    add_prompt_box(doc, p5_text, "PROMPT TV5 (TRẦN CÔNG TÚ): DASHBOARD KPI, BIỂU ĐỒ MPANDROIDCHART & 9 BÁO CÁO CHUYÊN SÂU")

    # =========================================================================
    # PHẦN III: HƯỚNG DẪN TÍCH HỢP GIT VÀ QUY TRÌNH PHỐI HỢP
    # =========================================================================
    h3 = doc.add_heading("III. QUY CHUẨN GIT WORKFLOW & KIỂM THỬ TÍCH HỢP LIÊN PHÂN HỆ", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)
    for r in h3.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "1. Quy tắc phân nhánh Git bắt buộc:",
            "   • TV1 (Bình): Tạo repo gốc trên GitHub `LapTrinhMang_5AESiuNhan`, commit phần Core Architecture + Master Data Contract lên nhánh `main` trước.",
            "   • Các thành viên clone repo về máy và tạo nhánh riêng:",
            "     - TV1: git checkout -b feature/tv1-core-product",
            "     - TV2 (Quân): git checkout -b feature/tv2-inbound-supplier",
            "     - TV3 (Thảo): git checkout -b feature/tv3-outbound-dealer",
            "     - TV4 (Tâm): git checkout -b feature/tv4-inventory-audit",
            "     - TV5 (Tú): git checkout -b feature/tv5-dashboard-reports",
            "   • Tuyệt đối KHÔNG push trực tiếp lên nhánh `main`.",
            "",
            "2. Quy trình kiểm thử tích hợp chéo (Cross-Testing Checklist):",
            "   • Test case 1 (TV1 & TV2): TV1 tạo sản phẩm SKU 'RLX-SUB-01' (1 Thùng = 10 Chiếc). TV2 tạo phiếu nhập 2 Thùng -> Kiểm tra hệ thống yêu cầu quét đủ 20 Serial và tính giá vốn đích danh.",
            "   • Test case 2 (TV2 & TV4): TV2 duyệt phiếu nhập -> Kiểm tra TV4 thấy tồn kho tăng, các Serial xuất hiện trên kệ và có dòng phát sinh trong Sổ Thẻ kho (+).",
            "   • Test case 3 (TV3 & TV4): TV3 lên đơn bán sỉ 5 chiếc -> Kiểm tra TV4 thấy tồn giữ chỗ tăng 5, tồn khả dụng giảm 5. TV3 quét xuất kho -> Tồn thực tế giảm 5, Serial chuyển 'DA_BAN'.",
            "   • Test case 4 (TV2, TV3 & TV5): TV2 lập phiếu chi trả NCC, TV3 lập phiếu thu đại lý -> Kiểm tra TV5 thấy Dashboard cập nhật dòng tiền và Sổ chi tiết công nợ 2 chiều chính xác."
        ],
        title="QUY TRÌNH KIỂM SOÁT TÍCH HỢP & GHÉP NỐI CODE",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # Save to disk
    output_filename = "HUONG_DAN_TRIEN_KHAI_ANDROID_STUDIO_5_THANH_VIEN.docx"
    output_path = os.path.join(r"D:\cntt\pbhb", output_filename)
    doc.save(output_path)
    print(f"SUCCESS: Created document at {output_path}")

if __name__ == "__main__":
    build_android_prompts_document()
