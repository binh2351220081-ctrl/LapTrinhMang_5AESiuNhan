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
        set_cell_background(cell, "F8FAFC") # Soft clean light slate
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
                <w:right w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        # Header title
        p_head = cell.paragraphs[0]
        p_head.paragraph_format.space_before = Pt(0)
        p_head.paragraph_format.space_after = Pt(6)
        r_t = p_head.add_run(f"📋 BẢN PROMPT COPY-PASTE (DÙNG CHO AI / ANDROID STUDIO COPILOT):\n{prompt_title}")
        r_t.font.name = "Arial"
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(27, 54, 93) # Navy
        
        # Body text - Split line by line so Word NEVER truncates or clips Vietnamese accents
        for line in prompt_text.strip().splitlines():
            p_line = cell.add_paragraph()
            p_line.paragraph_format.space_before = Pt(0)
            p_line.paragraph_format.space_after = Pt(2)
            p_line.paragraph_format.line_spacing = 1.15
            r = p_line.add_run(line if line.strip() else " ")
            r.font.name = "Consolas"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
            
        doc.add_paragraph().paragraph_format.space_after = Pt(10)

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
        ("TV1: Phan Bá Hải Bình\n(Nhóm trưởng)", "Core Framework, Auth & Quản lý Hàng hóa Master", "com.example.chronovaultwms.core\ncom.example.chronovaultwms.product", "Khởi tạo Architecture MVVM, Room DB, Navigation, Master Đồng hồ, ĐVT Thùng/Chiếc, MOQ, Tra cứu Serial Timeline, Audit Log."),
        ("TV2: Nguyễn Đắc Quân", "Đối tác Nhà Cung Cấp & Quản lý Nhập Kho", "com.example.chronovaultwms.inbound", "Hồ sơ NCC, Phiếu nhập kho, Tích hợp Camera Barcode/ZXing nạp Serial, Quy đổi ĐVT, Tính Giá vốn đích danh, Phiếu Chi nợ NCC."),
        ("TV3: Tô Đức Thảo", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "com.example.chronovaultwms.outbound", "Hồ sơ đại lý tiếp nhận B2B, Hạn mức tín dụng, Lệnh xuất kho, Duyệt khóa giữ chỗ (Reserved), Quét Serial đóng kiện xuất bến, Phiếu Thu nợ đại lý."),
        ("TV4: Võ Công Tâm", "Tồn Kho, Vị Trí Kệ Vật Lý & Kiểm Kê", "com.example.chronovaultwms.inventory", "Tồn kho đa đơn vị, 3 kho chất lượng (Mới/Trưng bày/Lỗi), Sơ đồ kệ Bin [Khu-Dãy-Tầng-Ngăn], Quét kiểm kê Camera, Phiếu cân bằng kho, Sổ Thẻ kho."),
        ("TV5: Trần Công Tú", "Dashboard Điều Hành & Báo Cáo Thống Kê", "com.example.chronovaultwms.dashboard", "Executive Dashboard KPI, Vẽ biểu đồ MPAndroidChart doanh số/chi phí 6 tháng, Top sản phẩm bán chạy, 9 Báo cáo chuyên sâu, Sổ nợ 2 chiều, Dòng tiền.")
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
    val orderCode: String? = null,        // FK -> orders.code (Mã lệnh xuất kho đại lý)
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
   - Package gốc: com.example.chronovaultwms
   - Cấu trúc thư mục chuẩn:
     + core/ (database, model, auth, utils)
     + product/ (ui, viewmodel, adapter)
   - Thiết lập Room Database (ChronoVaultDatabase, version = 4) chứa các bảng cốt lõi: products, serials, users, audit_logs.
   - Định nghĩa toàn bộ Enums chuẩn: UserRole (SYSTEM_ADMIN, STORE_OWNER, WAREHOUSE_MANAGER, OPERATIONS_STAFF, ACCOUNTANT), MovementType, SerialLifecycleStatus, QualityStatus.
   - Cung cấp sẵn cơ chế Seed Data (DatabaseSeeder): nạp 10 mẫu đồng hồ cao cấp (Rolex, Omega, Patek Philippe...), 10 mã Serial thực tế và 5 tài khoản mẫu cho 5 tác nhân.

2. PHÂN HỆ XÁC THỰC, PHÂN QUYỀN RBAC & AUDIT LOG:
   - Xây dựng hộp thoại Đăng nhập (dialog_login.xml) hỗ trợ Quick Login 1-chạm cho 5 tác nhân nghiệp vụ: binh_admin, owner_boss, tam_manager, quan_thao_ops, tu_accountant.
   - Xây dựng SessionManager lưu phiên đăng nhập và vai trò người dùng vào SharedPreferences.
   - Tạo hộp thoại Quản trị hệ thống (dialog_system_management.xml): Tab Tài khoản, Tab Ma trận phân quyền RBAC Matrix, Tab Nhật ký kiểm toán Audit Log Trail.
   - Chức năng Đổi Gmail / Sửa hồ sơ cá nhân có kiểm tra quyền hạn (Admin hoặc chính chủ).

3. QUẢN LÝ HÀNG HÓA MASTER & TRA CỨU SERIAL TIMELINE:
   - Xây dựng ProductListFragment: Hiển thị danh sách đồng hồ dạng CardView xa xỉ (Onyx Navy #1A2332, Gold #D4AF37), hiển thị SKU, Barcode, thương hiệu, giá phân phối đại lý, giá niêm yết, tồn kho; hỗ trợ tìm kiếm real-time và chip lọc hãng.
   - Form thêm mới đồng hồ (dialog_product_add.xml): đầy đủ 12 trường thông số kỹ thuật, tự động sinh mã Serial đầu tiên vào Room Database.
   - Quy cách đóng gói xuất kho: Thiết lập ĐVT cơ bản (Chiếc lẻ), ĐVT đóng gói (Thùng/Kiện), hệ số quy đổi (conversionRate = 10) và số lượng đặt tối thiểu (MOQ = 5).
   - Truy vết vòng đời Serial (dialog_product_serial_timeline.xml): Stepper 6 bước trực quan (Nhập mới -> Kệ Bin -> Giữ chỗ -> Đóng gói -> Bàn giao -> Bảo hành).

YÊU CẦU ĐẦU RA:
- Mã nguồn Kotlin sạch, chuẩn MVVM, sử dụng ViewBinding và Kotlin Coroutines (Dispatchers.IO).
- Layout XML tuân thủ tiền tố: fragment_product_..., dialog_product_..., item_product_..."""

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

    p2_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ NHẬP KHO VÀ ĐỐI TÁC NHÀ CUNG CẤP. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.inbound` BẰNG KOTLIN:

1. KẾ THỪA NỀN TẢNG CORE & CƠ SỞ DỮ LIỆU:
   - Kế thừa trực tiếp từ branch `main` của Nhóm trưởng (Phan Bá Hải Bình).
   - Sử dụng các Entity và DAO dùng chung từ `com.example.chronovaultwms.core.database.*`: ProductEntity, SerialEntity, ChronoVaultDatabase.
   - Sử dụng SessionManager để kiểm tra vai trò người dùng hiện tại (OPERATIONS_STAFF hoặc WAREHOUSE_MANAGER).

2. QUẢN LÝ HỒ SƠ NHÀ CUNG CẤP & CÔNG NỢ PHẢI TRẢ:
   - Danh bạ Nhà Cung Cấp chính hãng (SupplierListFragment): Hiển thị mã NCC, tên công ty, mã số thuế, hotline, số tài khoản ngân hàng và tổng số dư nợ phải trả.
   - Thêm/Sửa NCC: Kiểm tra tính duy nhất của mã NCC và MST.
   - Theo dõi công nợ NCC: Tự động cộng nợ khi phiếu nhập kho được duyệt; trừ nợ khi lập Phiếu Chi thanh toán.
   - Lập Phiếu Chi thanh toán nợ (PaymentVoucherDialog): Nhập số tiền chi trả, hình thức chuyển khoản/tiền mặt, mã tham chiếu ngân hàng; cập nhật giảm số dư nợ NCC.

3. LẬP PHIẾU NHẬP KHO QUY ĐỔI ĐVT & QUÉT CAMERA SERIAL (INBOUND WORKFLOW):
   - Xây dựng CreateInboundReceiptActivity / Dialog:
     + Bước 1: Chọn Nhà Cung Cấp và nhập số hóa đơn / Invoice vận chuyển.
     + Bước 2: Chọn mẫu đồng hồ (SKU) và chọn ĐVT nhập là "Thùng" hoặc "Chiếc lẻ".
     + Bước 3: Cơ chế quy đổi tự động: Khi người dùng nhập số Thùng, hệ thống lấy conversionRate từ ProductEntity để tính ra tổng số chiếc lẻ (Ví dụ: Nhập 2 Thùng, hệ số 10 -> Yêu cầu nạp đủ 20 mã Serial).
     + Bước 4: Tích hợp Camera Barcode Scanner (hoặc hỗ trợ nhập tay / dán dải mã Serial): Quét liên tục từng mã Serial in trên hộp/tem đồng hồ. Có âm thanh 'beep' xác nhận mỗi lần quét.
     + Bước 5: Kiểm tra đối soát 2 chiều nghiêm ngặt:
       * Tổng số mã Serial quét được PHẢI BẰNG CHÍNH XÁC tổng số chiếc sau quy đổi (không cho duyệt nếu thiếu/thừa).
       * Chặn hoàn toàn và báo lỗi đỏ nếu phát hiện bất kỳ mã Serial nào đã tồn tại trong bảng `serials` của Room DB (chống trùng lặp tuyệt đối).

4. PHÂN BỔ CHI PHÍ & TÍNH TOÁN GIÁ VỐN ĐÍCH DANH (SPECIFIC IDENTIFICATION COSTING):
   - Trong phiếu nhập, kế toán/nhân viên khai báo các chi phí phát sinh thực tế: cước vận chuyển quốc tế, thuế quan hải quan, bảo hiểm lô hàng.
   - Tự động phân bổ đều chi phí vào từng chiếc đồng hồ theo công thức bắt buộc:
     Giá vốn Serial = Đơn giá mua trên HĐ + (Tổng chi phí phân bổ / Tổng số chiếc)
   - Lưu trữ từng Serial vào bảng `serials` với giá vốn đích danh này, gán trạng thái `TRONG_KHO`, vị trí mặc định `K1-A01` và chất lượng `HANG_MOI`.
   - Cập nhật tăng tồn kho vật lý tại Room DB, ghi nhận tăng công nợ NCC.

5. XUẤT TRẢ HÀNG LỖI CHO NCC (SUPPLIER RETURN):
   - Cho phép chọn NCC, quét/chọn các mã Serial từ Kho Hàng Lỗi (`HANG_LOI`), ghi lý do kỹ thuật (hỏng máy, hấp hơi nước, trầy xước từ hãng).
   - Sau khi duyệt: Chuyển Serial sang trạng thái `DA_TRA_NCC`, giảm tồn kho lỗi và tự động cấn trừ số tiền tương ứng vào công nợ phải trả NCC.

YÊU CẦU ĐẦU RA:
- Mã nguồn Kotlin sạch, tuân thủ MVVM (ViewModel, Repository, Room DAO).
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_inbound_...`, `dialog_inbound_...`, `item_inbound_...`
- Tích hợp mượt mà vào luồng chung của ứng dụng."""

    add_prompt_box(doc, p2_text, "PROMPT TV2 (NGUYỄN ĐẮC QUÂN): NHÀ CUNG CẤP, NHẬP KHO QUÉT SERIAL & GIÁ VỐN ĐÍCH DANH")

    # -------------------------------------------------------------
    # PROMPT 3: TV3 - TÔ ĐỨC THẢO
    # -------------------------------------------------------------
    doc.add_heading("3. PROMPT CHO THÀNH VIÊN 3: TÔ ĐỨC THẢO (ĐỐI TÁC ĐẠI LÝ & QUẢN LÝ XUẤT KHO)", level=2)
    
    add_callout(
        doc,
        [
            "• Vai trò: Phụ trách Phân hệ 3 (Đối Tác Đại Lý & Quản Lý Xuất Kho).",
            "• Trách nhiệm: Quản lý hồ sơ đại lý tiếp nhận B2B, phân hạng và kiểm soát hạn mức tín dụng (Credit Limit), lập lệnh xuất kho theo hợp đồng đại lý, thẩm định công nợ & duyệt khóa hàng giữ chỗ (Reserved), quy trình xuất kho 2 bước (Picking & Dispatch), quét Serial đóng kiện xuất kho, thu hồi công nợ đại lý và xử lý nhập trả hàng đại lý."
        ],
        title="MỤC TIÊU PHÂN HỆ 3 (TV3 - TÔ ĐỨC THẢO)",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    p3_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ ĐỐI TÁC ĐẠI LÝ VÀ QUẢN LÝ XUẤT KHO. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.outbound` BẰNG KOTLIN:

1. KẾ THỪA NỀN TẢNG CORE & CƠ SỞ DỮ LIỆU:
   - Kế thừa trực tiếp từ branch `main` của Nhóm trưởng (Phan Bá Hải Bình).
   - Sử dụng các Entity và DAO dùng chung từ `com.example.chronovaultwms.core.database.*`:
     + ProductEntity: Lấy mã SKU, tên mẫu mã, giá phân phối đại lý niêm yết, đơn vị tính.
     + SerialEntity: Lấy danh sách Serial đang `TRONG_KHO`, cập nhật trạng thái khi giữ chỗ (`CHO_XUAT`) và khi thực xuất (`DA_BAN`).
     + ChronoVaultDatabase: Instance Room Database dùng chung.
   - Sử dụng SessionManager để kiểm tra vai trò người dùng (STORE_OWNER, ACCOUNTANT, OPERATIONS_STAFF).

2. HỒ SƠ ĐẠI LÝ TIẾP NHẬN B2B & KIỂM SOÁT HẠN MỨC TÍN DỤNG:
   - Danh bạ Đại lý B2B (DealerListFragment): Quản lý tên đại lý / chuỗi cửa hàng (Galle Watch, Hải Triều, Boss Luxury...), Mã số thuế, Hạng đại lý (VIP Kim Cương, Vàng, Bạc, Đồng), Tỷ lệ chiết khấu thương mại (Ví dụ: 15% - 30%), Hạn mức nợ tối đa (Credit Limit, ví dụ: 2 tỷ VNĐ), Số dư nợ hiện tại (Outstanding Balance).
   - Kiểm tra Hạn mức nợ tự động (Credit Limit Enforcement):
     + Khi nhân viên tạo lệnh xuất hàng mới, hệ thống tự động kiểm tra:
       Nếu (Dư nợ hiện tại + Giá trị lô hàng xuất) > Hạn mức nợ cho phép:
       -> Khóa chặn không cho Lưu đơn hàng, hiển thị Dialog cảnh báo đỏ: "Đại lý đã vượt hạn mức tín dụng! Vui lòng thu bớt tiền nợ cũ hoặc xin duyệt ngoại lệ từ Chủ cửa hàng."
   - Lập Phiếu Thu tiền nợ Đại lý (ReceiptVoucherDialog): Ghi nhận tiền thu nợ từ đại lý (tiền mặt/chuyển khoản), cập nhật giảm dư nợ ngay lập tức.

3. QUẢN LÝ LỆNH XUẤT HÀNG ĐẠI LÝ B2B & CƠ CHẾ GIỮ CHỖ (INVENTORY RESERVATION):
   - Xây dựng CreateOutboundOrderActivity:
     + Chọn Đại lý tiếp nhận -> Hệ thống tự động áp dụng mức chiết khấu theo Hạng đại lý.
     + Chọn danh sách SKU đồng hồ và số lượng xuất theo ĐVT "Thùng" hoặc "Chiếc".
     + Kiểm tra tồn kho khả dụng (Available Stock Check):
       Tồn khả dụng = Tổng tồn vật lý - Tồn đang giữ chỗ cho các đơn khác.
       Nếu số lượng đặt > Tồn khả dụng -> Báo lỗi không cho lưu.
     + Cơ chế Giữ chỗ (Reservation Engine): Khi đơn hàng ở trạng thái "Đã tiếp nhận" (Pending), hệ thống tự động tăng `reservedQuantity` của SKU để các đơn khác không thể lấy trùng.

4. QUY TRÌNH XUẤT KHO 2 BƯỚC BẮT BUỘC & QUÉT CAMERA SERIAL (PICKING & DISPATCH):
   - Bước 1 (Picking List - Tạo danh sách xuất kho): Hệ thống gợi ý danh sách Serial cụ thể trong kho theo vị trí ngăn kệ Bin thuận tiện lấy hàng nhất.
   - Bước 2 (Quét Serial Dispatch bằng Camera ML Kit / ZXing):
     + Nhân viên xuất kho cầm điện thoại quét từng mã Serial trên hộp đồng hồ trước khi đóng thùng giao cho đại lý.
     + Ứng dụng kiểm tra chéo thời gian thực (Real-time Cross-validation):
       * Báo lỗi và rung cảnh báo nếu quét nhầm mã Serial không thuộc đơn hàng.
       * Báo lỗi nếu quét mã Serial đang ở trạng thái lỗi (`HANG_LOI`) hoặc đang trưng bày (`TRUNG_BAY`).
     + Sau khi quét đủ 100% mã Serial: Mở nút "Xác nhận Xuất kho Hoàn tất".

5. HOÀN TẤT XUẤT KHO, CẬP NHẬT CÔNG NỢ & PHIẾU XUẤT KHO B2B:
   - Chuyển trạng thái các Serial đã quét sang `DA_BAN`.
   - Giảm trừ tồn kho vật lý và giải phóng số lượng giữ chỗ trong Room DB.
   - Ghi tăng công nợ phải thu của Đại lý tương ứng với giá trị sau chiết khấu của lô hàng xuất.
   - Ghi nhận giao dịch vào Sổ Thẻ kho (-).
   - In / Xem Phiếu Xuất kho kiêm Hóa đơn B2B: Hiển thị đầy đủ danh sách Serial định danh để kích hoạt bảo hành hãng.

YÊU CẦU ĐẦU RA:
- Mã nguồn Kotlin sạch, chuẩn MVVM, kết nối mượt mà với Room DB của TV1.
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_outbound_...`, `dialog_outbound_...`, `item_outbound_...`"""

    add_prompt_box(doc, p3_text, "PROMPT TV3 (TÔ ĐỨC THẢO): ĐỐI TÁC ĐẠI LÝ, KHÓA GIỮ CHỖ & QUÉT XUẤT SERIAL")

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

    p4_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ QUẢN LÝ TỒN KHO VẬT LÝ, VỊ TRÍ KỆ VÀ KIỂM KÊ. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.inventory` BẰNG KOTLIN:

1. KẾ THỪA NỀN TẢNG CORE & CƠ SỞ DỮ LIỆU:
   - Kế thừa trực tiếp từ branch `main` của Nhóm trưởng (Phan Bá Hải Bình).
   - Sử dụng các Entity và DAO dùng chung từ `com.example.chronovaultwms.core.database.*`: ProductEntity, SerialEntity, ChronoVaultDatabase.
   - Sử dụng SessionManager để kiểm tra vai trò người dùng hiện tại (WAREHOUSE_MANAGER).

2. THEO DÕI TỒN KHO ĐA ĐƠN VỊ & 3 KHO CHẤT LƯỢNG:
   - Xây dựng StockOverviewFragment:
     + Hiển thị số lượng tồn kho theo cả 2 đơn vị: Đơn vị sỉ (Thùng/Kiện) và Đơn vị lẻ (Chiếc).
     + Phân tách rõ ràng 3 chỉ số quan trọng cho từng mẫu đồng hồ:
       * Tồn thực tế (In-Stock)
       * Tồn giữ chỗ (Reserved)
       * Tồn khả dụng xuất kho đại lý (Available = Thực tế - Giữ chỗ).
     + Thiết kế 3 Tab phân loại chất lượng độc lập:
       * Kho Hàng Mới (New Stock): Đủ điều kiện xuất kho đại lý.
       * Kho Hàng Trưng Bày (Display Stock): Hàng mở mẫu cho đại lý xem.
       * Kho Hàng Lỗi (Defect Stock): Hàng phát sinh lỗi kỹ thuật chờ trả hãng.
   - Tính toán tổng giá trị tồn kho bằng cách cộng dồn 100% Giá vốn đích danh của các mã Serial đang có mặt trong kho; không dùng bình quân giản đơn.
   - Cảnh báo định mức tồn kho tự động:
     * Cảnh báo màu vàng khi tồn kho <= minStock (nhắc lập PO nhập thêm).
     * Cảnh báo màu đỏ khi tồn khả dụng = 0 (hết hàng ngừng nhận đơn).
     * Cảnh báo vượt maxStock (tránh ứ đọng vốn).

3. SƠ ĐỒ VỊ TRÍ KỆ KHO VẬT LÝ (BIN LOCATION MANAGEMENT):
   - Quản lý mã định danh vị trí kệ theo cấu trúc chuẩn: [Dãy kệ - Tầng - Ngăn] (Ví dụ: "K1-A01", "K1-A02", "K2-B01"...).
   - Trực quan hóa sơ đồ mặt bằng kệ (Grid / RecyclerView): Hiển thị sức chứa tối đa, số lượng Serial hiện lưu trên từng ngăn kệ và thanh tiến độ phần trăm lấp đầy (Capacity Progress Bar). Đổi màu đỏ khi kệ đầy 100%.
   - Chức năng điều chuyển ngăn kệ: Cho phép quét Serial và chọn vị trí kệ mới để cập nhật vị trí lưu kho của chiếc đồng hồ.

4. KIỂM KÊ KHO & TỰ ĐỘNG ĐỐI SOÁT CHÊNH LỆCH SERIAL:
   - Xây dựng StockAuditActivity:
     + Khởi tạo đợt kiểm kê theo phạm vi: Toàn kho, Theo dãy kệ, hoặc Theo thương hiệu.
     + Cơ chế tạm khóa xuất nhập: Khi đợt kiểm kê kích hoạt, hệ thống tạm khóa biến động xuất/nhập trên các ngăn kệ kiểm kê để đảm bảo tính chính xác.
     + Quét kiểm đếm thực tế bằng Camera / Nhập tay: Thủ kho quét nhanh toàn bộ mã Serial thực tế hiện diện trên kệ.
     + Đối soát tự động thời gian thực:
       * Serial Khớp đúng: Trùng khớp cả vị trí và trạng thái trong CSDL.
       * Serial Thừa: Có mặt thực tế trên kệ nhưng CSDL không ghi nhận ở kệ này.
       * Serial Thiếu: CSDL báo có nhưng thực tế quét không thấy.
     + Hiển thị bảng đối soát phân màu rõ ràng (Xanh: Khớp, Vàng: Thừa, Đỏ: Thiếu).

5. PHIẾU CÂN BẰNG KHO & SỔ THẺ KHO ĐIỆN TỬ (STOCK LEDGER):
   - Lập phiếu cân bằng kho sau kiểm kê: Điều chỉnh số liệu sổ sách khớp đúng với thực tế đếm được; ghi rõ lý do và người chịu trách nhiệm. (Chênh lệch giá trị lớn > 10 triệu bắt buộc Chủ cửa hàng duyệt).
   - Xây dựng StockCardActivity (Sổ Thẻ kho điện tử):
     + Truy vấn nhật ký biến động của từng mã SKU: Ngày phát sinh, loại chứng từ (Nhập, Xuất kho đại lý, Đổi trả, Cân bằng kiểm kê), số lượng (+/-) và danh sách mã Serial liên quan.
     + Đảm bảo tính bất biến (Immutability): Dữ liệu Thẻ kho tuyệt đối cấm sửa/xóa; nếu sai sót phải lập phiếu điều chỉnh đối ứng.

YÊU CẦU ĐẦU RA:
- Mã nguồn Kotlin sạch, chuẩn MVVM, kết nối mượt mà với Room DB của TV1.
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_inventory_...`, `dialog_inventory_...`, `item_inventory_...`"""

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

    p5_text = """BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ BÁO CÁO VÀ DASHBOARD ĐIỀU HÀNH. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.dashboard` BẰNG KOTLIN:

1. KẾ THỪA NỀN TẢNG CORE & CƠ SỞ DỮ LIỆU:
   - Kế thừa trực tiếp từ branch `main` của Nhóm trưởng (Phan Bá Hải Bình).
   - Sử dụng các Entity và DAO dùng chung từ `com.example.chronovaultwms.core.database.*`: ProductEntity, SerialEntity, ChronoVaultDatabase.
   - Sử dụng SessionManager để kiểm tra vai trò người dùng hiện tại (ACCOUNTANT hoặc STORE_OWNER).

2. EXECUTIVE DASHBOARD & THẺ CHỈ SỐ KPI THỜI GIAN THỰC:
   - Xây dựng DashboardOverviewFragment (Màn hình trung tâm điều hành):
     + Hiển thị 5 thẻ chỉ số hiệu suất trọng yếu (KPI Cards) phong cách Horology Luxury:
       * Tổng giá trị tài sản tồn kho: Tính chuẩn xác theo giá vốn đích danh của từng Serial trong kho.
       * Doanh thu phân phối đại lý: Doanh số tích lũy từ các đơn hàng xuất bán cho đại lý trong kỳ.
       * Số lượng lệnh xuất kho đại lý mới.
       * Tổng tồn kho khả dụng cung ứng.
       * Tỷ lệ tiếp nhận trả hàng đại lý (Cảnh báo đỏ nếu vượt ngưỡng an toàn > 2.0%).
     + Dòng thời gian hoạt động gần đây (Audit Activity Stream): Hiển thị danh sách các thao tác quan trọng vừa phát sinh trong kho (nhập mới, duyệt lệnh xuất đại lý, thu tiền nợ, kiểm kê kệ...).

3. BIỂU ĐỒ TRỰC QUAN DOANH SỐ & CHI PHÍ BẰNG MPANDROIDCHART:
   - Tích hợp thư viện `com.github.PhilJay:MPAndroidChart:v3.1.0`.
   - Biểu đồ BarChart / LineChart xu hướng doanh thu phân phối đại lý 6 tháng gần nhất kèm tỷ lệ tăng trưởng.
   - Biểu đồ PieChart cơ cấu chi phí phát sinh: Cước vận chuyển quốc tế, thuế hải quan, bảo hiểm lô hàng, phí lưu kho.
   - Bảng xếp hạng Top 5 / Top 10 mẫu đồng hồ bán chạy nhất kênh sỉ (xếp theo sản lượng chiếc bán ra và theo doanh thu).

4. HỆ THỐNG 9 BÁO CÁO CHUYÊN SÂU ĐA PHÂN HỆ:
   - Xây dựng ReportContainerFragment với bộ lọc thời gian (Từ ngày - Đến ngày) và hiển thị 9 báo cáo chuyên sâu:
     1. Báo cáo Nhập hàng (Inbound Report): Số lượng và giá trị nhập theo từng NCC, cơ cấu chi phí phân bổ.
     2. Báo cáo Phân phối Đại lý (Outbound Report): Doanh số theo từng đại lý, tỷ lệ hoàn tất đơn hàng.
     3. Báo cáo Cơ cấu xuất hàng: Tỷ trọng xuất kho đại lý vs Xuất gửi bảo hành hãng vs Xuất tiêu hủy hàng hỏng.
     4. Báo cáo Đổi trả & Chất lượng bộ máy: Phân tích tỷ lệ lỗi theo từng hãng và theo dòng máy (Automatic, Quartz, Solar) phục vụ đàm phán hợp đồng với NCC.
     5. Báo cáo Hàng chậm luân chuyển (Dead Stock Aging): Liệt kê các mẫu đồng hồ có thời gian lưu kho > 90 ngày hoặc > 180 ngày để đề xuất thanh lý thu hồi vốn.
     6. Báo cáo Tài chính & Lợi nhuận gộp B2B: Doanh số xuất kho đại lý trừ Giá vốn đích danh trừ Chi phí logistics = Lợi nhuận gộp thực tế.
     7. Sổ chi tiết công nợ B2B 2 chiều: Đối soát chi tiết từng đại lý và nhà cung cấp (Dư nợ đầu kỳ, Phát sinh nợ, Phát sinh có, Dư nợ cuối kỳ).
     8. Báo cáo Dòng tiền Thu / Chi thực tế (Cashflow Report): Dòng tiền thu vào (xuất kho đại lý, thu hồi nợ) trừ Dòng tiền chi ra (trả NCC, chi phí) = Dòng tiền thuần (Net Cashflow).
     9. Báo cáo Nhật ký kiểm toán Audit Log toàn hệ thống.

5. XUẤT BÁO CÁO (EXPORT CSV / PDF / IN ẤN):
   - Hỗ trợ nút "Xuất file CSV / Excel" lưu vào thư mục Downloads của điện thoại để người dùng chia sẻ qua Zalo / Email.
   - Hỗ trợ xem trước và in báo cáo định dạng chuẩn A4 qua Android PrintManager.

YÊU CẦU ĐẦU RA:
- Giao diện báo cáo trực quan, biểu đồ mượt mà, tính toán số liệu khớp đúng 100% với dữ liệu giao dịch của 4 phân hệ kia.
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_dashboard_...`, `item_dashboard_...`"""

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
            "     - TV1: git checkout -b feature/product",
            "     - TV2 (Quân): git checkout -b feature/tv2-inbound-supplier",
            "     - TV3 (Thảo): git checkout -b feature/tv3-outbound-dealer",
            "     - TV4 (Tâm): git checkout -b feature/tv4-inventory-audit",
            "     - TV5 (Tú): git checkout -b feature/tv5-dashboard-reports",
            "   • Tuyệt đối KHÔNG push trực tiếp lên nhánh `main`.",
            "",
            "2. Quy trình kiểm thử tích hợp chéo (Cross-Testing Checklist):",
            "   • Test case 1 (TV1 & TV2): TV1 tạo sản phẩm SKU 'RLX-SUB-01' (1 Thùng = 10 Chiếc). TV2 tạo phiếu nhập 2 Thùng -> Kiểm tra hệ thống yêu cầu quét đủ 20 Serial và tính giá vốn đích danh.",
            "   • Test case 2 (TV2 & TV4): TV2 duyệt phiếu nhập -> Kiểm tra TV4 thấy tồn kho tăng, các Serial xuất hiện trên kệ và có dòng phát sinh trong Sổ Thẻ kho (+).",
            "   • Test case 3 (TV3 & TV4): TV3 lập lệnh xuất kho đại lý 5 chiếc -> Kiểm tra TV4 thấy tồn giữ chỗ tăng 5, tồn khả dụng giảm 5. TV3 quét xuất kho -> Tồn thực tế giảm 5, Serial chuyển 'DA_BAN'.",
            "   • Test case 4 (TV2, TV3 & TV5): TV2 lập phiếu chi trả NCC, TV3 lập phiếu thu đại lý -> Kiểm tra TV5 thấy Dashboard cập nhật dòng tiền và Sổ chi tiết công nợ 2 chiều chính xác."
        ],
        title="QUY TRÌNH KIỂM SOÁT TÍCH HỢP & GHÉP NỐI CODE",
        border_color="C59B27",
        bg_color="FEF9C3"
    )

    # =========================================================================
    # PHẦN IV: CHECKLIST NHIỆM VỤ BẮT BUỘC NGOÀI CODE CỦA 5 THÀNH VIÊN
    # =========================================================================
    h4 = doc.add_heading("IV. BẢNG PHÂN CÔNG NHIỆM VỤ NGOÀI CODE (TEST DATA, VIẾT BÁO CÁO & DEMO VẤN ĐÁP)", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)
    for r in h4.runs:
        r.font.name = "Arial"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = C_NAVY

    add_callout(
        doc,
        [
            "Lập trình (Code) chỉ chiếm khoảng 40% - 50% khối lượng đồ án. Để cả nhóm đạt điểm tối đa khi thầy cô chấm bài, 4 thành viên bắt buộc phải hoàn thành đầy đủ 3 nhiệm vụ ngoài code dưới đây:",
            "",
            "1. Chuẩn bị Dữ liệu mẫu (Test Data) thực tế cho phân hệ của mình:",
            "   • TV2 (Quân): Chuẩn bị hồ sơ 3 Nhà cung cấp (Rolex Geneva SA, Omega Bienne...), 2 PO hóa đơn nhập khẩu và dải mã Serial mẫu.",
            "   • TV3 (Thảo): Chuẩn bị hồ sơ 5 Đại lý B2B (Hải Triều, Galle Watch, Boss Luxury...), phân hạng VIP/Bạc/Đồng, hạn mức nợ và chiết khấu.",
            "   • TV4 (Tâm): Chuẩn bị danh sách vị trí ngăn kệ Bin [K1-A01, K1-A02...], quy định kho Mới / Trưng bày / Lỗi kỹ thuật.",
            "   • TV5 (Tú): Chuẩn bị bảng số liệu doanh thu 6 tháng, bảng đối soát sổ nợ 2 chiều và công thức giá vốn đích danh.",
            "",
            "2. Viết tài liệu Báo cáo Đồ án (File Word nộp Khoa):",
            "   • Mỗi thành viên tự chụp ảnh màn hình giao diện (Screenshots) của phân hệ mình, chú thích chi tiết từng chức năng.",
            "   • Vẽ sơ đồ ca sử dụng Use Case và Sơ đồ tuần tự (Sequence Diagram) mô tả luồng nghiệp vụ của phân hệ mình phụ trách.",
            "   • Trình bày giải thích các thuật toán, cơ chế ràng buộc logic (như quy đổi ĐVT, khóa giữ chỗ, kiểm soát hạn mức nợ).",
            "",
            "3. Chuẩn bị Kịch bản Demo & Vấn đáp trực tiếp với Giảng viên:",
            "   • Thầy/cô sẽ chấm điểm trực tiếp trên máy tính/máy ảo Android: Từng bạn phải tự tay mở app và thao tác một chu trình nghiệp vụ hoàn chỉnh của mình.",
            "   • Hiểu rõ đoạn code mình viết: Khi thầy cô chỉ vào hàm hoặc bảng Room Database nào thì phải giải thích được luồng dữ liệu chạy ra sao.",
            "   • Đảm bảo lịch sử Git Commit: Tự commit từ tài khoản GitHub cá nhân để thầy cô kiểm tra lịch sử đóng góp thực tế trên Repository."
        ],
        title="CHECKLIST 3 NHIỆM VỤ QUAN TRỌNG NGOÀI CODE CỦA CÁC THÀNH VIÊN",
        border_color="1B365D",
        bg_color="F1F5F9"
    )

    # Save to disk
    output_filename = "Document/KE_HOACH_CHI_TIET_VA_BO_PROMPT_TOAN_DIEN_5_THANH_VIEN.docx"
    output_path = os.path.join(r"D:\cntt\pbhb", output_filename)
    doc.save(output_path)
    print(f"SUCCESS: Created document at {output_path}")

if __name__ == "__main__":
    build_android_prompts_document()
