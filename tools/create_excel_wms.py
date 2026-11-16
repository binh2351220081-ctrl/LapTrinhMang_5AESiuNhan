# -*- coding: utf-8 -*-
"""
Script to generate Bang_Phan_He_Quan_Ly_Kho_Dong_Ho.xlsx
for ChronoVault B2B Wholesale Horology WMS project.
Matching and elevating the structure of Bang_Phan_He_da_chinh_sua.xlsx across 5 sheets:
1. Sheet1: Phân hệ tổng quan & Phân quyền 5 vai trò
2. Phân rã chức năng: 45 chức năng con chi tiết
3. Trường dữ liệu: Từ điển trường nhập liệu (Data Dictionary)
4. Vai trò và quyền: Ma trận trách nhiệm 5 tác nhân
5. Quy tắc nghiệp vụ: 18 quy tắc nghiệp vụ trọng yếu
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_wms_excel():
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active

    # Palette
    NAVY = "1B365D"       # Main header background
    SLATE = "334155"      # Secondary header background
    GOLD = "C59B27"       # Accent Gold
    LIGHT_BG = "F8FAFC"   # Alternating row background
    WHITE = "FFFFFF"
    BORDER_COLOR = "CBD5E1"
    GROUP_BG = "E2E8F0"
    NOTE_COLOR = "64748B"

    # Borders
    thin_border = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )

    # Helper styling function
    def style_title(ws, cell_ref, text):
        ws[cell_ref] = text
        ws[cell_ref].font = Font(name="Arial", size=14, bold=True, color="1B365D")
        ws[cell_ref].alignment = Alignment(vertical="center")

    def style_note(ws, cell_ref, text):
        ws[cell_ref] = text
        ws[cell_ref].font = Font(name="Arial", size=10, italic=True, color=NOTE_COLOR)
        ws[cell_ref].alignment = Alignment(vertical="center")

    def apply_header(ws, row_idx, headers, fill_color=NAVY):
        ws.row_dimensions[row_idx].height = 28
        for col_idx, h in enumerate(headers, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=h)
            cell.font = Font(name="Arial", size=10, bold=True, color=WHITE)
            cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = thin_border

    def auto_fit_columns(ws, min_widths=None):
        if min_widths is None:
            min_widths = {}
        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = 0
            for cell in col:
                val_str = str(cell.value or '')
                lines = val_str.split('\n')
                for l in lines:
                    if len(l) > max_len:
                        max_len = len(l)
            # reasonable cap and padding
            calculated = max(max_len + 3, min_widths.get(col[0].column, 12))
            ws.column_dimensions[col_letter].width = min(calculated, 65)

    # =========================================================================
    # SHEET 1: Sheet1 (Phân hệ tổng quan & Phân quyền 5 vai trò)
    # =========================================================================
    ws1 = wb.create_sheet(title="Sheet1")
    ws1.views.sheetView[0].showGridLines = True

    style_title(ws1, "A1", "BẢNG MA TRẬN PHÂN HỆ TỔNG QUAN & PHÂN QUYỀN VAI TRÒ (CHRONOVAULT B2B WMS)")
    style_note(ws1, "A2", "Hệ thống quản lý kho đồng hồ phân phối đại lý B2B: Định danh Serial 100%, Quy đổi ĐVT Thùng/Chiếc, Giá vốn đích danh và Quản lý công nợ.")

    s1_headers = [
        "Phân hệ", "Module / Chức năng", "Chi tiết yêu cầu & Luồng xử lý", "Dữ liệu Đầu vào (Input)", "Dữ liệu Đầu ra (Output)",
        "Quản trị hệ thống", "Chủ cửa hàng", "Thủ kho", "NV Nhập - Xuất", "Kế toán"
    ]
    apply_header(ws1, 4, s1_headers, fill_color=NAVY)

    s1_rows = [
        # PH1
        ("PH1: Hàng hóa & Hệ thống", "Đăng nhập & Xác thực", "Xác thực danh tính, kiểm tra vai trò (Role), sinh JWT session và ghi Audit Log đăng nhập.", "Tên đăng nhập / Email, mật khẩu, IP", "Phiên đăng nhập (Session token), vai trò, quyền hạn", "Toàn quyền", "Đăng nhập", "Đăng nhập", "Đăng nhập", "Đăng nhập"),
        ("PH1: Hàng hóa & Hệ thống", "Quản trị tài khoản & Ma trận quyền", "Khởi tạo tài khoản nhân viên, cấu hình 5 vai trò (RBAC), kích hoạt/khóa tài khoản, phân quyền CRUD.", "Họ tên, email, tên đăng nhập, vai trò, ma trận phân quyền", "Tài khoản kích hoạt, danh sách quyền gán", "Toàn quyền", "Xem danh sách", "Không", "Không", "Không"),
        ("PH1: Hàng hóa & Hệ thống", "Nhật ký kiểm toán (Audit Log)", "Ghi vết tự động mọi hành vi: người thực hiện, thời gian, IP, chứng từ tác động (Thêm/Sửa/Xóa/Duyệt); bất biến 100%.", "Dữ liệu thao tác người dùng, mốc thời gian, IP", "Bảng nhật ký Audit Log tra cứu lịch sử", "Toàn quyền", "Xem toàn quyền", "Không", "Không", "Xem vết tài chính"),
        ("PH1: Hàng hóa & Hệ thống", "Danh mục Đồng hồ Master & Quy cách ĐVT", "Khai báo SKU, Barcode, thông số kỹ thuật (bộ máy, kính, size), cấu hình ĐVT đóng gói/lẻ (Thùng -> Chiếc), định mức Min/Max và MOQ.", "SKU, Barcode, tên, hãng, máy, kính, ĐVT cơ bản, ĐVT đóng gói, hệ số quy đổi, MOQ, Min/Max", "Hồ sơ sản phẩm chuẩn, hệ số quy đổi đóng gói", "Cấu hình / Quản trị", "Xem danh mục", "Xem danh mục", "Xem danh mục", "Xem giá áp dụng"),
        ("PH1: Hàng hóa & Hệ thống", "Truy vết vòng đời Serial (Serial Timeline)", "Tra cứu toàn diện dòng đời của 1 chiếc đồng hồ: Ngày nhập -> NCC -> Ngăn kệ -> Lệnh xuất đại lý -> Đại lý sở hữu -> Bảo hành.", "Mã Serial / IMEI cần tra cứu", "Timeline chi tiết toàn bộ lịch sử biến động của chiếc đồng hồ", "Toàn quyền tra cứu", "Tra cứu", "Tra cứu", "Tra cứu", "Tra cứu"),
        
        # PH2
        ("PH2: NCC & Nhập kho", "Hồ sơ Nhà cung cấp & Công nợ phải trả", "Quản lý danh bạ NCC chính hãng, số tài khoản thụ hưởng ủy nhiệm chi, theo dõi công nợ mua hàng phát sinh.", "Mã NCC, tên hãng, MST, hotline, tài khoản ngân hàng", "Hồ sơ đối tác, sổ nợ phải trả NCC", "Xem cấu hình", "Xem / Giám sát", "Xem NCC", "Lập đề xuất", "Quản lý & Đối soát nợ"),
        ("PH2: NCC & Nhập kho", "Phiếu chi thanh toán nợ NCC", "Lập phiếu chi (Ủy nhiệm chi CK / Tiền mặt) thanh toán tiền hàng hoặc ứng trước cho NCC; tự động trừ nợ phải trả.", "Mã NCC, số tiền chi, hình thức, số hóa đơn/PO, chứng từ ngân hàng", "Phiếu chi hợp lệ, số dư nợ NCC giảm tương ứng", "Không", "Duyệt chi vượt ngưỡng", "Không", "Không", "Lập phiếu & Chi trả"),
        ("PH2: NCC & Nhập kho", "Lập & Phê duyệt Phiếu nhập kho", "Tạo phiếu nhập từ PO, quy đổi tự động Thùng ra Chiếc, nạp quét dải Serial, đối soát kiểm tra trùng lặp.", "PO, số thùng thực nhận, dải mã Serial quét được", "Phiếu nhập nháp, danh sách Serial đối soát khớp 100%", "Không", "Duyệt ngoại lệ giá trị lớn", "Xác nhận hàng vật lý", "Lập phiếu & Quét Serial", "Kiểm tra số liệu"),
        ("PH2: NCC & Nhập kho", "Phân bổ chi phí & Chốt Giá vốn đích danh", "Khai báo cước vận chuyển quốc tế, thuế hải quan, phí bảo hiểm; phân bổ đều vào từng chiếc hình thành Giá vốn đích danh.", "Phí vận chuyển, thuế hải quan, bảo hiểm lô hàng", "Giá vốn đích danh từng mã Serial, tăng tồn kho vật lý, tăng công nợ NCC", "Không", "Duyệt chi phí vượt ngưỡng", "Cập nhật vị trí kệ", "Không", "Phân bổ & Chốt giá vốn"),
        ("PH2: NCC & Nhập kho", "Xuất trả hàng lỗi cho NCC", "Quét Serial lỗi kỹ thuật từ Kho Hàng Lỗi xuất trả về hãng; giảm trừ trực tiếp vào công nợ phải trả NCC.", "Mã NCC, danh sách Serial lỗi, lý do hỏng máy/hấp hơi", "Phiếu xuất trả NCC, Serial chuyển trạng thái DA_TRA_NCC, giảm nợ NCC", "Không", "Phê duyệt trả hàng", "Xác nhận xuất vật lý", "Soạn hàng lỗi", "Đối soát giảm nợ"),

        # PH3
        ("PH3: Đại lý & Xuất kho đại lý", "Hồ sơ Đại lý B2B & Hạn mức tín dụng", "Quản lý danh sách đại lý xuất kho đại lý, phân hạng (VIP/Bạc/Đồng), chính sách chiết khấu, hạn mức nợ (Credit Limit), thời hạn nợ.", "Mã đại lý, tên shop/chuỗi, MST, hạng đại lý, hạn mức nợ, Net 15/30", "Hồ sơ đại lý, hạn mức tín dụng khả dụng", "Xem cấu hình", "Duyệt hạn mức tín dụng", "Không", "Cập nhật liên hệ", "Thẩm định công nợ"),
        ("PH3: Đại lý & Xuất kho đại lý", "Lệnh xuất kho đại lý & Khóa Giữ chỗ (Reserved)", "Lên lệnh xuất đại lý theo Thùng/Chiếc; kiểm tra MOQ và tồn khả dụng; áp giá đại lý theo hạng; thẩm định tín dụng; khóa giữ chỗ số lượng.", "Đại lý, SKU, số lượng thùng/chiếc đặt mua, tiền cọc", "Lệnh xuất đại lý DA_DUYET, tăng tồn giữ chỗ (Reserved), giảm tồn khả dụng", "Không", "Duyệt ngoại lệ vượt nợ", "Xác nhận hàng có sẵn", "Lập lệnh xuất kho đại lý nháp", "Thẩm định nợ & cọc"),
        ("PH3: Đại lý & Xuất kho đại lý", "Quét Serial đóng kiện & Thực xuất kho đại lý", "Thủ kho quét camera/máy quét từng Serial lấy trên kệ đóng kiện; đối soát Serial thuộc SKU và trạng thái HANG_MOI.", "Mã lệnh xuất đại lý, mã Serial quét thực tế", "Phiếu xuất B2B kèm danh sách Serial, Serial chuyển DA_BAN, trừ tồn kho, tăng nợ đại lý", "Không", "Giám sát tiến độ", "Xác nhận xuất vật lý", "Quét Serial & Đóng gói", "Ghi nhận nợ đại lý"),
        ("PH3: Đại lý & Xuất kho đại lý", "Phiếu thu hồi công nợ đại lý & Thu nợ đại lý", "Thu tiền cọc hoặc thu nợ đại lý theo hạn hợp đồng (CK/tiền mặt); tự động cấn trừ số dư nợ và khôi phục hạn mức mua.", "Mã đại lý, số tiền thu, chứng từ ngân hàng đối soát", "Phiếu thu hợp lệ, giảm nợ đại lý, khôi phục hạn mức tín dụng", "Không", "Xem báo cáo thu", "Không", "Không", "Lập phiếu & Thu tiền"),
        ("PH3: Đại lý & Xuất kho đại lý", "Nhận trả hàng đại lý & Xuất khác (Bảo hành/Hủy)", "Tiếp nhận hàng đổi trả từ đại lý, quét Serial xác minh nguồn gốc xuất bán, phân loại về Kho Mới hoặc Kho Lỗi; xuất bảo hành hãng.", "Serial đổi trả, tình trạng nguyên seal hay lỗi máy", "Phiếu nhận trả hàng đại lý, cấn trừ nợ đại lý, cập nhật tồn kho phân loại", "Không", "Duyệt đổi trả ngoại lệ", "Kiểm định & Nhập kho lại", "Tiếp nhận Serial trả", "Đối soát cấn trừ tiền"),

        # PH4
        ("PH4: Tồn kho & Kiểm kê", "Tồn kho đa đơn vị & 3 Kho chất lượng", "Theo dõi tồn kho theo Thùng và Chiếc lẻ; phân tách Tồn thực tế, Tồn giữ chỗ, Tồn khả dụng; tách bạch 3 kho: Mới, Trưng Bày, Lỗi.", "Dữ liệu xuất/nhập/điều chuyển phân loại", "Bảng tổng hợp tồn kho đa đơn vị, giá trị tồn theo giá vốn đích danh", "Không", "Xem tổng quan tài sản", "Quản lý tồn kho thực tế", "Xem tồn khả dụng", "Xem giá trị tồn kho"),
        ("PH4: Tồn kho & Kiểm kê", "Sơ đồ Kệ kho vật lý (Bin Location)", "Quản lý mã định danh vị trí [Khu - Dãy - Tầng - Ngăn]; gán sản phẩm vào kệ cố định; trực quan hóa sức chứa và tỷ lệ lấp đầy.", "Mã vị trí kệ, SKU gán, sức chứa tối đa", "Sơ đồ kệ trực quan, vị trí lấy hàng (picking) chuẩn xác", "Không", "Xem trực quan", "Quy hoạch & Quản lý kệ", "Lấy hàng theo kệ", "Không"),
        ("PH4: Tồn kho & Kiểm kê", "Kiểm kê kho & Đối soát Serial chênh lệch", "Lập đợt kiểm kê theo kệ/toàn kho; tạm khóa xuất nhập; quét thực tế toàn bộ Serial trên kệ; hệ thống đối soát Thừa/Thiếu.", "Phạm vi kiểm kê, dải Serial quét đếm thực tế", "Biên bản đối soát kiểm kê, danh sách Serial thừa/thiếu", "Không", "Duyệt chênh lệch lớn", "Chủ trì quét kiểm kê", "Hỗ trợ quét Serial", "Đối soát sổ sách"),
        ("PH4: Tồn kho & Kiểm kê", "Phiếu cân bằng kho & Sổ Thẻ kho điện tử", "Sinh phiếu cân bằng kho điều chỉnh sổ sách khớp thực tế; ghi vết bất biến vào Sổ Thẻ kho (+/-) và nhật ký kiểm toán.", "Phiếu kiểm kê đã duyệt, lý do sai lệch", "Tồn kho được cân bằng, dòng ghi Sổ Thẻ kho (so_the_kho) bất biến", "Không", "Phê duyệt cân bằng", "Xác nhận điều chỉnh vật lý", "Không", "Đối soát chứng từ"),
        ("PH4: Tồn kho & Kiểm kê", "Cảnh báo định mức tồn kho (Min / Max / Out)", "Tự động cảnh báo màu vàng khi tồn kho <= Min để lập PO nhập thêm; cảnh báo đỏ khi hết hàng (Out of Stock); cảnh báo vượt Max.", "Số lượng tồn khả dụng, ngưỡng Min/Max", "Thông báo cảnh báo trên màn hình điều hành, gợi ý số lượng đặt hàng đại lý", "Không", "Xem cảnh báo", "Theo dõi cảnh báo Min", "Xem cảnh báo hết", "Không"),

        # PH5
        ("PH5: Báo cáo & Dashboard", "Executive Dashboard & KPI Cards", "Hiển thị chỉ số thời gian thực: Tổng giá trị tồn đích danh, Doanh thu phân phối đại lý, Số lệnh xuất đại lý, Tồn khả dụng, Tỷ lệ đổi trả.", "Dữ liệu giao dịch phát sinh từ PH1 - PH4", "Thẻ KPI trực quan thời gian thực", "Xem hệ thống", "Toàn quyền điều hành", "Xem tồn & tiến độ", "Xem tiến độ đơn", "Xem số liệu tài chính"),
        ("PH5: Báo cáo & Dashboard", "Biểu đồ Canvas Doanh số & Chi phí", "Biểu diễn trực quan xu hướng doanh số 6 tháng gần nhất và cơ cấu chi phí nhập hàng (vận chuyển, hải quan, lưu kho).", "Số liệu lệnh xuất đại lý hoàn tất, chi phí phân bổ theo tháng", "Biểu đồ cột/đường trực quan trên nền HTML5 Canvas", "Không", "Phân tích chiến lược", "Không", "Không", "Phân tích tài chính"),
        ("PH5: Báo cáo & Dashboard", "Hệ thống 9 Báo cáo chuyên sâu đa phân hệ", "Xuất báo cáo chi tiết: Báo cáo Nhập hàng, Phân phối đại lý, Cơ cấu xuất, Đổi trả theo loại máy, Hàng Dead Stock, Lợi nhuận gộp B2B.", "Thời khoảng lọc (Từ ngày - Đến ngày), điều kiện phân hệ", "Báo cáo chi tiết định dạng bảng biểu, hỗ trợ xuất Excel/CSV/PDF", "Xem báo cáo hệ thống", "Toàn quyền xem & xuất", "Xem báo cáo tồn/kệ", "Xem báo cáo giao dịch", "Xem báo cáo doanh thu/vốn"),
        ("PH5: Báo cáo & Dashboard", "Sổ chi tiết công nợ B2B & Dòng tiền Cashflow", "Đối soát chi tiết nợ 2 chiều (Đại lý & NCC): Dư đầu kỳ, phát sinh nợ (+), phát sinh có (-), dư cuối kỳ; Báo cáo dòng tiền thực tế.", "Thời khoảng kế toán, mã đối tác, phiếu thu/chi phát sinh", "Sổ chi tiết công nợ 2 chiều, Báo cáo dòng tiền thuần (Net Cashflow)", "Không", "Xem & Giám sát dòng tiền", "Không", "Không", "Toàn quyền lập & đối soát")
    ]

    for r_idx, r_data in enumerate(s1_rows, start=5):
        ws1.row_dimensions[r_idx].height = 24
        bg = LIGHT_BG if r_idx % 2 == 1 else WHITE
        fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws1.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Arial", size=9)
            cell.fill = fill
            cell.border = thin_border
            if c_idx == 1:
                cell.font = Font(name="Arial", size=9, bold=True, color="1B365D")
                cell.alignment = Alignment(vertical="center")
            elif c_idx == 2:
                cell.font = Font(name="Arial", size=9, bold=True)
                cell.alignment = Alignment(vertical="center")
            elif c_idx in [6, 7, 8, 9, 10]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if val in ["Toàn quyền", "Toàn quyền điều hành", "Cấu hình / Quản trị"]:
                    cell.font = Font(name="Arial", size=8.5, bold=True, color="15803D") # green
                elif val == "Không":
                    cell.font = Font(name="Arial", size=8.5, color="94A3B8") # muted
                else:
                    cell.font = Font(name="Arial", size=8.5, color="1E293B")
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)

    auto_fit_columns(ws1, {1: 24, 2: 28, 3: 40, 4: 35, 5: 35, 6: 18, 7: 18, 8: 18, 9: 18, 10: 18})
    ws1.freeze_panes = "A5"

    # =========================================================================
    # SHEET 2: Phân rã chức năng (45 chức năng con chi tiết)
    # =========================================================================
    ws2 = wb.create_sheet(title="Phân rã chức năng")
    ws2.views.sheetView[0].showGridLines = True

    style_title(ws2, "A1", "PHÂN RÃ CHỨC NĂNG THEO TÁC NHÂN VÀ ĐỐI TƯỢNG (CHRONOVAULT HOROLOGY WMS)")
    style_note(ws2, "A2", "Mỗi dòng là một chức năng nhỏ (nguyên tử). Input chính là bắt buộc; input phụ chỉ nhập khi có hoặc khi điều kiện nghiệp vụ yêu cầu.")

    s2_headers = [
        "Mã CN", "Phân hệ", "Chức năng lớn", "Chức năng con chi tiết", "Tác nhân chính", "Tác nhân phối hợp",
        "Đối tượng dữ liệu", "Input chính (Bắt buộc)", "Input phụ (Tùy chọn)", "Dữ liệu Đầu ra (Output)", "Quy tắc nghiệp vụ & Phạm vi quyền"
    ]
    apply_header(ws2, 4, s2_headers, fill_color=NAVY)

    s2_data = [
        # PH1
        ("F1.1.1", "PH1: Hàng hóa", "Quản lý hàng hóa", "Xem danh sách đồng hồ", "Thủ kho", "NV Nhập - Xuất; Kế toán", "Đồng hồ Master", "Từ khóa tìm kiếm; Bộ lọc thương hiệu", "Khoảng giá phân phối đại lý; Loại máy; Tùy chọn sắp xếp", "Bảng danh sách mẫu đồng hồ phân trang", "Chỉ hiển thị các sản phẩm ACTIVE hoặc có cờ hiển thị."),
        ("F1.1.2", "PH1: Hàng hóa", "Quản lý hàng hóa", "Xem chi tiết thông số kỹ thuật", "NV Nhập - Xuất", "Thủ kho; Kế toán", "Đồng hồ Master", "Mã SKU hoặc ID sản phẩm", "Không", "Modal thông số 6 thuộc tính chuẩn ngành xa xỉ", "Hiển thị đầy đủ bộ máy, kính, dây, size mặt, chống nước, bảo hành."),
        ("F1.1.3", "PH1: Hàng hóa", "Quản lý hàng hóa", "Thêm mới đồng hồ Master", "Quản trị hệ thống", "Không", "Đồng hồ; Quy đổi ĐVT", "SKU; Barcode; Tên; Hãng; Giá vốn; Giá phân phối đại lý các hạng", "Hình ảnh; Kính; Dây; Chống nước; Min/Max tồn", "Bản ghi đồng hồ mới lưu vào CSDL", "SKU và Barcode duy nhất tuyệt đối. Cờ quản lý Serial bắt buộc bật."),
        ("F1.1.4", "PH1: Hàng hóa", "Quản lý hàng hóa", "Chỉnh sửa thông số & Cấu hình ĐVT", "Quản trị hệ thống", "Thủ kho", "Đồng hồ; Quy đổi ĐVT", "ID sản phẩm; Hệ số quy đổi (conversionRate); ĐVT đóng gói", "MOQ; Giá phân phối đại lý VIP/Bạc/Đồng; Ghi chú", "Thông tin đồng hồ và tỷ lệ đóng gói cập nhật", "Hệ số quy đổi là số nguyên dương >= 1 (VD: 1 Thùng = 10 Chiếc)."),
        ("F1.1.5", "PH1: Hàng hóa", "Quản lý hàng hóa", "Ngừng kinh doanh / Xóa sản phẩm", "Quản trị hệ thống", "Chủ cửa hàng", "Đồng hồ Master", "ID sản phẩm; Xác nhận thay đổi trạng thái", "Lý do ngưng kinh doanh", "Trạng thái chuyển INACTIVE / DISCONTINUED", "Không cho phép xóa nếu sản phẩm còn tồn kho hoặc có giao dịch lịch sử."),
        ("F1.1.6", "PH1: Hàng hóa", "Quản lý hàng hóa", "Quản lý Thương hiệu & Bộ sưu tập", "Quản trị hệ thống", "Không", "Thương hiệu; Bộ sưu tập", "Tên thương hiệu; Xuất xứ (Thụy Sỹ, Nhật...)", "Logo; Mô tả bộ sưu tập", "Danh mục thương hiệu cập nhật", "Không cho xóa thương hiệu đang có sản phẩm liên kết."),
        ("F1.1.7", "PH1: Hàng hóa", "Quản lý hàng hóa", "Tìm kiếm & Lọc nâng cao", "Mọi tác nhân", "Không", "Đồng hồ Master", "Từ khóa SKU / Tên / Hãng", "Khoảng giá phân phối đại lý; Loại máy; Vị trí kệ", "Danh sách sản phẩm thỏa mãn điều kiện lọc", "Tìm kiếm tức thì theo cơ chế debounce không làm đơ giao diện."),
        ("F1.1.8", "PH1: Hàng hóa", "Quản lý hàng hóa", "Truy vết vòng đời Serial (Timeline)", "Mọi tác nhân", "Không", "Serial; Lịch sử giao dịch", "Mã Serial / IMEI đích danh", "Không", "Timeline vòng đời toàn vẹn từ nhập đến xuất", "Hiển thị xuyên suốt ngày nhập, NCC, vị trí kệ, lệnh xuất đại lý, đại lý và bảo hành."),
        ("F1.1.9", "PH1: Hàng hóa", "Quản lý hàng hóa", "Xuất dữ liệu danh mục hàng", "Quản trị hệ thống", "Kế toán", "Đồng hồ Master", "Tùy chọn bộ lọc cần trích xuất", "Định dạng file (CSV / Excel)", "File danh mục đồng hồ tải về máy", "Chỉ người dùng có quyền Export mới được xuất dữ liệu."),

        ("F1.2.1", "PH1: Hệ thống", "Quản trị hệ thống", "Xem danh sách tài khoản", "Quản trị hệ thống", "Chủ cửa hàng", "Tài khoản người dùng", "Bộ lọc vai trò; Trạng thái tài khoản", "Từ khóa tìm kiếm nhân viên", "Bảng danh sách tài khoản kèm trạng thái", "Mật khẩu luôn được băm một chiều an toàn, không hiển thị plain text."),
        ("F1.2.2", "PH1: Hệ thống", "Quản trị hệ thống", "Cấp mới tài khoản nhân viên", "Quản trị hệ thống", "Không", "Tài khoản; Vai trò", "Tên đăng nhập; Email; Mật khẩu ban đầu; Vai trò", "Họ tên; Số điện thoại; Ảnh đại diện", "Tài khoản nhân viên mới được kích hoạt", "Tên đăng nhập và email duy nhất trên toàn hệ thống."),
        ("F1.2.3", "PH1: Hệ thống", "Quản trị hệ thống", "Khóa / Mở khóa tài khoản", "Quản trị hệ thống", "Chủ cửa hàng", "Tài khoản người dùng", "ID tài khoản; Trạng thái (ACTIVE/LOCKED)", "Lý do khóa tài khoản", "Tài khoản đổi trạng thái; Hủy phiên làm việc", "Không cho phép tự khóa tài khoản Admin đang đăng nhập hiện hành."),
        ("F1.2.4", "PH1: Hệ thống", "Quản trị hệ thống", "Cấu hình vai trò (Role Setup)", "Quản trị hệ thống", "Không", "Vai trò (Role)", "Mã vai trò (5 vai trò chuẩn); Tên hiển thị", "Mô tả trách nhiệm cốt lõi", "Bản ghi vai trò được lưu trong hệ thống", "Hệ thống chuẩn hóa đúng 5 vai trò theo nguyên tắc phân tách quyền."),
        ("F1.2.5", "PH1: Hệ thống", "Quản trị hệ thống", "Thiết lập ma trận phân quyền (RBAC)", "Quản trị hệ thống", "Chủ cửa hàng", "Ma trận quyền", "Mã vai trò; Danh sách mã quyền phân hệ", "Ghi chú cấu hình", "Quyền hạn các nhóm người dùng được áp dụng", "Áp dụng có hiệu lực tức thì cho các phiên làm việc tiếp theo."),
        ("F1.2.6", "PH1: Hệ thống", "Quản trị hệ thống", "Đổi mật khẩu cá nhân", "Người dùng hiện hành", "Không", "Tài khoản người dùng", "Mật khẩu hiện tại; Mật khẩu mới xác nhận", "Không", "Mật khẩu cập nhật thành công", "Mật khẩu mới tối thiểu 8 ký tự, gồm chữ hoa, chữ thường và số."),
        ("F1.2.7", "PH1: Hệ thống", "Quản trị hệ thống", "Quản lý phiên đăng nhập (Session)", "Quản trị hệ thống", "Không", "Phiên JWT", "Token phiên / User ID", "Không", "Hủy bỏ token từ xa thành công", "Tự động đăng xuất an toàn sau 60 phút không có thao tác."),
        ("F1.2.8", "PH1: Hệ thống", "Quản trị hệ thống", "Truy xuất Nhật ký hệ thống (Audit Log)", "Quản trị hệ thống", "Chủ cửa hàng; Kế toán", "Nhật ký kiểm toán", "Thời khoảng tra cứu; Tác nhân; Loại thao tác", "Từ khóa chứng từ liên quan", "Bảng nhật ký kiểm toán ghi vết đầy đủ", "Nhật ký kiểm toán có tính bất biến 100%, cấm sửa xóa vật lý."),

        # PH2
        ("F2.1.1", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Xem danh bạ Nhà cung cấp", "Kế toán", "NV Nhập - Xuất; Thủ kho", "Nhà cung cấp", "Từ khóa tìm kiếm NCC; Trạng thái hợp tác", "Bộ lọc hãng phân phối", "Bảng danh bạ NCC và tổng nợ phải trả", "Chỉ hiển thị các nhà cung cấp phân phối đồng hồ chính hãng."),
        ("F2.1.2", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Thêm mới & Cập nhật NCC", "Kế toán", "Quản trị hệ thống", "Nhà cung cấp", "Mã NCC; Tên hãng; MST; Người liên hệ; SĐT", "Email; Địa chỉ trụ sở chính", "Hồ sơ NCC được tạo/cập nhật", "Mã số thuế và mã NCC là duy nhất."),
        ("F2.1.3", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Cấu hình tài khoản ngân hàng NCC", "Kế toán", "Không", "Tài khoản ngân hàng NCC", "Mã NCC; Tên ngân hàng; Số tài khoản; Chủ TK", "Chi nhánh ngân hàng", "Thông tin ủy nhiệm chi được lưu", "Bắt buộc kiểm tra độ dài và định dạng số tài khoản ngân hàng."),
        ("F2.1.4", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Theo dõi công nợ phải trả NCC", "Kế toán", "Chủ cửa hàng", "Sổ nợ NCC", "Mã NCC cần đối soát", "Kỳ kế toán (Tháng/Quý)", "Bảng chi tiết nợ phải trả, hạn thanh toán", "Tự động cộng nợ khi duyệt nhập kho, trừ nợ khi duyệt phiếu chi."),
        ("F2.1.5", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Lập phiếu Chi thanh toán nợ NCC", "Kế toán", "Chủ cửa hàng", "Phiếu chi; Công nợ NCC", "Mã NCC; Số tiền chi; Hình thức (CK/Tiền mặt)", "Số PO liên quan; Ủy nhiệm chi đính kèm", "Phiếu chi hợp lệ; Giảm số dư nợ NCC", "Khoản chi vượt ngưỡng quy định phải có Chủ cửa hàng phê duyệt."),
        ("F2.1.6", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Lập phiếu xuất trả hàng lỗi cho NCC", "NV Nhập - Xuất", "Thủ kho", "Serial lỗi; Phiếu xuất trả", "Mã NCC; Danh sách Serial lỗi từ Kho Lỗi", "Biên bản giám định lỗi; Ảnh chụp lỗi", "Phiếu xuất trả NCC ở trạng thái nháp", "Chỉ được chọn các Serial đang có trạng thái HANG_LOI trong kho."),
        ("F2.1.7", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Phê duyệt phiếu trả hàng NCC", "Chủ cửa hàng", "Kế toán; Thủ kho", "Phiếu trả hàng; Công nợ", "Mã phiếu trả hàng; Chữ ký duyệt", "Ghi chú phê duyệt", "Phiếu trả hoàn tất; Giảm nợ NCC; Trừ Serial", "Tự động cấn trừ giá trị hàng trả vào số dư nợ phải trả NCC."),
        ("F2.1.8", "PH2: Nhập kho", "Quản lý Nhà cung cấp", "Quản lý trạng thái hợp tác NCC", "Chủ cửa hàng", "Kế toán", "Nhà cung cấp", "Mã NCC; Trạng thái (ACTIVE/SUSPENDED)", "Lý do thay đổi trạng thái", "Trạng thái NCC cập nhật", "Tạm khóa không cho tạo PO mới đối với NCC bị ngưng hợp tác."),

        ("F2.2.1", "PH2: Nhập kho", "Quản lý Nhập kho", "Khởi tạo phiếu nhập kho", "NV Nhập - Xuất", "Kế toán", "Phiếu nhập kho", "Nhà cung cấp; Số hóa đơn / Invoice hãng", "Ngày nhập dự kiến; Ghi chú vận chuyển", "Bản ghi Phiếu nhập nháp (DRAFT) được tạo", "Nhà cung cấp phải đang ở trạng thái ACTIVE."),
        ("F2.2.2", "PH2: Nhập kho", "Quản lý Nhập kho", "Thêm sản phẩm & Chọn ĐVT nhập", "NV Nhập - Xuất", "Không", "Chi tiết phiếu nhập", "Mã SKU; Đơn vị tính nhập (Thùng hoặc Chiếc)", "Đơn giá nhập theo hợp đồng", "Dòng chi tiết hàng nhập được ghi nhận", "Hệ thống tự động hiển thị hệ số quy đổi đóng gói tương ứng."),
        ("F2.2.3", "PH2: Nhập kho", "Quản lý Nhập kho", "Quy đổi số lượng tự động", "Hệ thống", "NV Nhập - Xuất", "Chi tiết phiếu nhập", "Số lượng Thùng thực nhận", "Hệ số quy đổi của SKU", "Tổng số lượng Chiếc lẻ bắt buộc nạp Serial", "Số chiếc = Số thùng x Hệ số quy đổi (VD: 3 Thùng x 10 = 30 Chiếc)."),
        ("F2.2.4", "PH2: Nhập kho", "Quản lý Nhập kho", "Nạp & Quét danh sách mã Serial", "NV Nhập - Xuất", "Thủ kho", "Serial sản phẩm", "Dải mã Serial (quét camera barcode hoặc dán list)", "Không", "Danh sách Serial nạp tạm vào phiếu nhập", "Bắt buộc số lượng Serial phải khớp đúng 100% số chiếc quy đổi."),
        ("F2.2.5", "PH2: Nhập kho", "Quản lý Nhập kho", "Đối soát kiểm tra trùng lặp Serial", "Hệ thống", "NV Nhập - Xuất", "Serial trong CSDL", "Dải Serial vừa nạp", "Không", "Thông báo hợp lệ hoặc cảnh báo đỏ mã trùng", "Chặn hoàn toàn nếu có bất kỳ mã Serial nào đã tồn tại trong CSDL."),
        ("F2.2.6", "PH2: Nhập kho", "Quản lý Nhập kho", "Phân bổ chi phí nhập hàng", "Kế toán", "Không", "Chi phí lô hàng; Giá vốn", "Chi phí vận chuyển quốc tế; Thuế hải quan; Bảo hiểm", "Phí bốc xếp phụ trợ", "Giá vốn đích danh từng chiếc đồng hồ", "Giá vốn Serial = Giá nhập HĐ + (Tổng chi phí phân bổ / Tổng số chiếc)."),
        ("F2.2.7", "PH2: Nhập kho", "Quản lý Nhập kho", "Tính toán tổng giá trị phiếu nhập", "Hệ thống", "Kế toán", "Phiếu nhập kho", "Đơn giá, số lượng, chiết khấu, thuế VAT, chi phí", "Không", "Tổng giá trị thanh toán của lô hàng", "Tính toán tự động theo công thức kế toán tài chính."),
        ("F2.2.8", "PH2: Nhập kho", "Quản lý Nhập kho", "Lưu tạm (Draft) phiếu nhập", "NV Nhập - Xuất", "Không", "Phiếu nhập kho", "Dữ liệu phiếu đang nhập dở", "Không", "Phiếu nhập lưu trạng thái DRAFT", "Cho phép mở lại để quét tiếp dải Serial khi có hàng lớn."),
        ("F2.2.9", "PH2: Nhập kho", "Quản lý Nhập kho", "Phê duyệt & Chốt nhập kho vật lý", "Thủ kho", "Kế toán; Chủ cửa hàng", "Phiếu nhập; Tồn kho; Serial; Công nợ", "Mã phiếu nhập; Xác nhận kiểm đếm đủ và đúng", "Vị trí kệ phân bổ ban đầu", "Tăng tồn kho; Kích hoạt Serial; Tăng nợ NCC", "Khoản chi vượt ngưỡng phải có Chủ cửa hàng phê duyệt."),
        ("F2.2.10", "PH2: Nhập kho", "Quản lý Nhập kho", "Hủy phiếu nhập kho nháp", "NV Nhập - Xuất", "Thủ kho", "Phiếu nhập kho", "Mã phiếu nhập nháp", "Lý do hủy phiếu", "Phiếu nhập chuyển trạng thái CANCELLED", "Chỉ được hủy khi phiếu chưa được phê duyệt chốt kho."),
        ("F2.2.11", "PH2: Nhập kho", "Quản lý Nhập kho", "In phiếu nhập kho & Xuất PDF", "NV Nhập - Xuất", "Kế toán", "Phiếu nhập kho", "Mã phiếu nhập đã duyệt", "Mẫu in khổ A4", "Bản in A4 hoặc file PDF lưu chứng từ kế toán", "Hiển thị đầy đủ bảng kê chi tiết toàn bộ các mã Serial đã nhập."),

        # PH3
        ("F3.1.1", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Xem danh sách đại lý B2B", "NV Nhập - Xuất", "Kế toán", "Đại lý B2B", "Từ khóa tìm đại lý; Phân hạng đại lý", "Bộ lọc khu vực địa lý", "Bảng danh bạ đại lý, hạn mức nợ, dư nợ", "100% đối tác là pháp nhân/cửa hàng phân phối đại lý, không có khách lẻ."),
        ("F3.1.2", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Thêm mới & Cập nhật hồ sơ đại lý", "Kế toán", "NV Nhập - Xuất", "Đại lý B2B", "Mã đại lý; Tên shop/chuỗi; MST; Người đại diện", "SĐT; Địa chỉ kho nhận hàng; Hợp đồng cam kết", "Hồ sơ đại lý hoàn chỉnh được lưu trữ", "MST và mã đại lý là duy nhất trên hệ thống."),
        ("F3.1.3", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Cấu hình chính sách thương mại", "Chủ cửa hàng", "Kế toán", "Chính sách giá; Hạn mức", "Hạng đại lý (VIP/Bạc/Đồng); Chiết khấu (%); Hạn mức nợ", "Thời hạn nợ (Net 15 / Net 30)", "Chính sách giá phân phối đại lý được kích hoạt cho đại lý", "Đại lý hạng VIP hưởng giá phân phối đại lý tốt nhất và hạn mức nợ cao nhất."),
        ("F3.1.4", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Giám sát hạn mức công nợ khả dụng", "Kế toán", "NV Nhập - Xuất", "Công nợ đại lý", "Mã đại lý cần tra cứu", "Không", "Số dư nợ hiện tại, hạn mức nợ còn lại có thể mua", "Hạn mức khả dụng = Hạn mức tín dụng - Dư nợ hiện tại."),
        ("F3.1.5", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Lập phiếu Thu hồi công nợ đại lý / Thu nợ", "Kế toán", "Chủ cửa hàng", "Phiếu thu; Công nợ", "Mã đại lý; Số tiền thu; Hình thức (CK/Tiền mặt)", "Ủy nhiệm chi ngân hàng đối soát", "Phiếu thu hợp lệ; Giảm nợ; Khôi phục hạn mức", "Tiền thu ghi giảm nợ đại lý và khôi phục hạn mức khả dụng ngay lập tức."),
        ("F3.1.6", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Tiếp nhận yêu cầu nhận trả hàng đại lý", "NV Nhập - Xuất", "Thủ kho", "Đơn nhận trả hàng đại lý; Serial", "Mã đại lý; Mã Serial sản phẩm hoàn trả", "Lý do đổi trả (đổi mẫu / lỗi kỹ thuật)", "Kết quả xác minh nguồn gốc xuất bán của Serial", "Bắt buộc Serial phải có nguồn gốc bán đúng cho chính đại lý này."),
        ("F3.1.7", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Phân loại sản phẩm đổi trả", "Thủ kho", "NV Nhập - Xuất", "Serial; Trạng thái kho", "Kết quả kiểm định chất lượng sản phẩm", "Biên bản giám định lỗi đồng hồ", "Gán vào KHO_MOI (nguyên seal) hoặc KHO_LOI", "Hàng nguyên seal đưa về Kho Mới bán tiếp; hàng lỗi đưa về Kho Lỗi chờ xử lý."),
        ("F3.1.8", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Phê duyệt phiếu nhận trả hàng đại lý", "Chủ cửa hàng", "Kế toán; Thủ kho", "Phiếu đổi trả; Công nợ", "Mã phiếu đổi trả", "Ghi chú duyệt cấn trừ tiền", "Cấn trừ nợ đại lý; Tăng tồn kho tương ứng", "Phiếu duyệt tự động giảm số dư nợ của đại lý tương ứng giá trị nhận trả."),
        ("F3.1.9", "PH3: Xuất kho đại lý", "Quản lý Đại lý B2B", "Quản lý trạng thái đại lý", "Chủ cửa hàng", "Kế toán", "Đại lý B2B", "Mã đại lý; Trạng thái (ACTIVE/LOCKED)", "Lý do khóa (nợ quá hạn, vi phạm)", "Tài khoản đại lý bị khóa mua hàng", "Đại lý nợ quá hạn bị tạm khóa tự động, không cho phép lên đơn mới."),

        ("F3.2.1", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Khởi tạo lệnh xuất kho đại lý", "NV Nhập - Xuất", "Kế toán", "Lệnh xuất kho đại lý", "Đại lý B2B được chỉ định", "Ghi chú hợp đồng; Thời hạn giao hàng", "Bản ghi lệnh xuất kho đại lý nháp (DRAFT) được tạo", "Đại lý phải ở trạng thái ACTIVE và không bị nợ quá hạn."),
        ("F3.2.2", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Chọn sản phẩm theo Thùng hoặc Chiếc", "NV Nhập - Xuất", "Không", "Chi tiết lệnh xuất đại lý", "SKU; Đơn vị tính (Thùng hoặc Chiếc); Số lượng", "Không", "Dòng sản phẩm được thêm vào lệnh xuất kho đại lý", "Bắt buộc số lượng chiếc sau quy đổi phải >= MOQ quy định."),
        ("F3.2.3", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Kiểm tra tồn kho khả dụng thời gian thực", "Hệ thống", "NV Nhập - Xuất", "Tồn kho tổng hợp", "Mã SKU; Số lượng chiếc yêu cầu", "Không", "Xác nhận đủ hàng hoặc cảnh báo thiếu hàng", "Tồn khả dụng = Tồn thực tế - Tồn đang giữ chỗ (Reserved)."),
        ("F3.2.4", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Áp giá đại lý tự động theo cấp bậc", "Hệ thống", "Kế toán", "Bảng giá phân phối đại lý; Chiết khấu", "Hạng đại lý (VIP/Bạc/Đồng); Số lượng đặt", "Không", "Đơn giá phân phối đại lý chuẩn và tỷ lệ chiết khấu hợp đồng", "Tự động áp giá đại lý theo ma trận hạng đại lý đã cấu hình trước."),
        ("F3.2.5", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Quản lý tiền cọc & Hạn thanh toán", "Kế toán", "NV Nhập - Xuất", "Lệnh xuất kho đại lý", "Số tiền cọc thỏa thuận; Thời hạn nợ (Net 15/30)", "Chứng từ ngân hàng xác nhận cọc", "Trạng thái cọc được cập nhật vào đơn", "Đơn hàng giá trị lớn bắt buộc phải thu tối thiểu 10-30% tiền cọc."),
        ("F3.2.6", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Phê duyệt lệnh xuất đại lý & Khóa Giữ chỗ", "Chủ cửa hàng", "Kế toán; Thủ kho", "Lệnh xuất đại lý; Tồn kho Reserved", "Mã lệnh xuất đại lý; Xác nhận hạn mức nợ hợp lệ", "Lý do phê duyệt ngoại lệ (nếu vượt hạn mức)", "Đơn sang DA_DUYET; Tăng tồn Giữ chỗ (Reserved)", "Khóa số lượng tồn khả dụng, ngăn không cho bán trùng lặp cho đơn khác."),
        ("F3.2.7", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Hủy lệnh xuất kho đại lý", "NV Nhập - Xuất", "Thủ kho; Kế toán", "Lệnh xuất kho đại lý; Tồn kho", "Mã lệnh xuất đại lý cần hủy", "Lý do hủy đơn", "Đơn sang CANCELLED; Giải phóng tồn giữ chỗ", "Tự động hoàn trả số lượng đang giữ chỗ lại cho tồn khả dụng."),
        ("F3.2.8", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Khởi tạo phiếu xuất kho xuất kho đại lý", "NV Nhập - Xuất", "Thủ kho", "Phiếu xuất kho", "Mã lệnh xuất kho đại lý đã được duyệt", "Thông tin đóng kiện và bàn giao", "Phiếu xuất kho xuất kho đại lý được sinh ra", "Chỉ được tạo phiếu xuất khi lệnh xuất kho đại lý ở trạng thái DA_DUYET."),
        ("F3.2.9", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Đóng gói & Quét Serial xuất kho", "Thủ kho", "NV Nhập - Xuất", "Serial; Phiếu xuất", "Mã Serial quét thực tế từ trên kệ đóng kiện", "Không", "Danh sách Serial đóng gói vào kiện hàng xuất", "Serial phải thuộc đúng SKU của đơn, trạng thái TRONG_KHO và HANG_MOI."),
        ("F3.2.10", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Xác nhận hoàn tất xuất kho", "Thủ kho", "Kế toán", "Phiếu xuất; Tồn kho; Serial; Nợ", "Mã phiếu xuất; Chữ ký xác nhận bàn giao", "Không", "Trừ tồn thực tế; Serial sang DA_BAN; Tăng nợ đại lý", "Giảm tồn thực tế, giải phóng giữ chỗ, ghi Sổ Thẻ kho (-) và tăng nợ đại lý."),
        ("F3.2.11", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Lập phiếu xuất khác (Bảo hành/Hủy)", "NV Nhập - Xuất", "Thủ kho; Chủ cửa hàng", "Phiếu xuất khác; Serial", "Loại xuất (BAO_HANH / TIEU_HUY); Danh sách Serial", "Biên bản hãng yêu cầu hoặc biên bản vỡ hỏng", "Phiếu xuất khác hoàn tất; Serial chuyển trạng thái", "Xuất tiêu hủy phải có phê duyệt chính thức của Chủ cửa hàng."),
        ("F3.2.12", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "Ghi nhận chi phí vận chuyển & Logistics", "NV Nhập - Xuất", "Kế toán", "Đơn hàng; Chi phí", "Cước vận chuyển; Chi phí đóng gói bảo hiểm; Bên chịu", "Mã đơn vị vận chuyển", "Chi phí được lưu và phân bổ vào báo cáo tài chính", "Ghi nhận rõ bên chịu chi phí (Kho tổng chịu hoặc Đại lý chịu)."),
        ("F3.2.13", "PH3: Xuất kho đại lý", "Đối Tác Đại Lý & Quản Lý Xuất Kho", "In biên bản bàn giao kiêm phiếu xuất", "NV Nhập - Xuất", "Thủ kho", "Phiếu xuất kho B2B", "Mã phiếu xuất kho hoàn tất", "Mẫu in khổ A4", "Biên bản giao nhận B2B A4 có bảng kê 100% Serial", "Bản in chính thức có giá trị pháp lý giao nhận và kích hoạt bảo hành."),

        # PH4
        ("F4.1.1", "PH4: Tồn kho", "Quản lý tồn kho", "Theo dõi tồn kho tổng hợp đa đơn vị", "Thủ kho", "NV Nhập - Xuất; Kế toán", "Tồn kho tổng hợp", "Bộ lọc sản phẩm; Trạng thái tồn", "Tùy chọn hiển thị theo Thùng hoặc Chiếc", "Bảng tồn kho đa đơn vị (Tồn thực, Giữ chỗ, Khả dụng)", "Hiển thị song song số Thùng quy đổi và tổng số Chiếc lẻ khả dụng."),
        ("F4.1.2", "PH4: Tồn kho", "Quản lý tồn kho", "Quản lý 3 trạng thái phân loại chất lượng", "Thủ kho", "NV Nhập - Xuất", "Tồn kho phân loại", "Tùy chọn tab kho (Kho Mới / Trưng Bày / Kho Lỗi)", "Không", "Danh sách hàng hóa tách bạch theo 3 kho chất lượng", "Chỉ hàng thuộc Kho Hàng Mới mới đủ điều kiện xuất kho đại lý cho đại lý."),
        ("F4.1.3", "PH4: Tồn kho", "Quản lý tồn kho", "Truy vấn danh mục Serial lưu kho", "Thủ kho", "NV Nhập - Xuất", "Serial trong kho", "Mã SKU; Vị trí kệ; Trạng thái Serial", "Khoảng ngày nhập kho", "Bảng danh mục chi tiết từng mã Serial có mặt trong kho", "Hiển thị đầy đủ vị trí ngăn kệ, ngày nhập và giá vốn đích danh."),
        ("F4.1.4", "PH4: Tồn kho", "Quản lý tồn kho", "Tính toán giá trị tồn theo Giá vốn đích danh", "Hệ thống", "Kế toán; Chủ cửa hàng", "Serial; Giá vốn", "Danh sách Serial đang có mặt trong kho", "Không", "Tổng giá trị tài sản kho theo Giá vốn đích danh", "Cộng dồn 100% giá vốn thực tế từng chiếc, không làm tròn hay bình quân sai lệch."),
        ("F4.1.5", "PH4: Tồn kho", "Quản lý tồn kho", "Cảnh báo định mức tồn kho (Min / Max)", "Hệ thống", "Thủ kho", "Tồn kho; Ngưỡng định mức", "Số lượng tồn khả dụng; Ngưỡng Min/Max đã cấu hình", "Không", "Tín hiệu cảnh báo màu vàng (<= Min) hoặc đỏ (>= Max)", "Tự động phát cảnh báo nhắc lập đơn đặt mua PO mới."),
        ("F4.1.6", "PH4: Tồn kho", "Quản lý tồn kho", "Cảnh báo hết hàng (Out-of-Stock)", "Hệ thống", "NV Nhập - Xuất; Thủ kho", "Tồn kho khả dụng", "Tồn khả dụng chạm mức 0", "Không", "Cờ đánh dấu hết hàng và tự động tạm khóa nhận lệnh xuất đại lý", "Bảo vệ kho không bị âm hoặc hứa giao hàng ngoài năng lực cung ứng."),

        ("F4.2.1", "PH4: Tồn kho", "Sơ đồ vị trí kệ", "Quản lý sơ đồ vị trí kệ kho vật lý", "Thủ kho", "Không", "Sơ đồ kệ (Bins)", "Khu vực; Mã dãy kệ; Số tầng; Số ngăn", "Sức chứa tối đa (chiếc); Chủng loại lưu trữ", "Sơ đồ mặt bằng vị trí kệ được số hóa hoàn chỉnh", "Mã vị trí chuẩn hóa dạng: [Khu A - Dãy A-01 - Tầng 2 - Ngăn Rolex]."),
        ("F4.2.2", "PH4: Tồn kho", "Sơ đồ vị trí kệ", "Phân bổ & Sắp xếp sản phẩm vào kệ", "Thủ kho", "NV Nhập - Xuất", "Vị trí kệ; Sản phẩm", "Mã SKU đồng hồ; Mã vị trí kệ chỉ định", "Ghi chú phân luồng lấy hàng", "Sản phẩm được gán cố định vào vị trí ngăn kệ", "Giúp nhân viên lấy hàng (picking) nhanh chóng khi đóng kiện lệnh xuất đại lý."),
        ("F4.2.3", "PH4: Tồn kho", "Sơ đồ vị trí kệ", "Hiển thị sức chứa & Tải trọng kệ", "Hệ thống", "Thủ kho", "Sức chứa kệ", "Số lượng Serial hiện lưu trên từng ngăn kệ", "Không", "Trực quan hóa tỷ lệ lấp đầy (%) và cảnh báo đầy kệ", "Cảnh báo màu đỏ khi ngăn kệ đạt 100% sức chứa tối đa."),

        ("F4.3.1", "PH4: Tồn kho", "Kiểm kê & Thẻ kho", "Khởi tạo đợt kiểm kê", "Thủ kho", "Chủ cửa hàng", "Phiếu kiểm kê", "Phạm vi kiểm kê (Toàn kho / Dãy kệ / Thương hiệu)", "Ngày kiểm kê; Thành phần tham gia", "Phiếu kiểm kê kích hoạt; Tạm khóa xuất nhập khu vực", "Khoanh vùng và khóa biến động để đảm bảo tính chuẩn xác khi đếm."),
        ("F4.3.2", "PH4: Tồn kho", "Kiểm kê & Thẻ kho", "Quét kiểm đếm thực tế bằng Camera", "Thủ kho", "NV Nhập - Xuất", "Serial thực tế", "Mã Serial quét bằng camera ZXing / máy quét tại kệ", "Ghi chú tình trạng đồng hồ", "Danh sách Serial đếm được nạp vào biên bản kiểm kê", "Hỗ trợ quét liên tục với tốc độ cao, có âm thanh bíp xác nhận."),
        ("F4.3.3", "PH4: Tồn kho", "Kiểm kê & Thẻ kho", "Tự động đối soát & Tính chênh lệch", "Hệ thống", "Thủ kho; Kế toán", "Số liệu sổ sách vs Thực tế", "Danh sách Serial quét đếm vs Danh sách sổ sách", "Không", "Bảng phân loại: Serial Khớp, Serial Thừa, Serial Thiếu", "Tự động tính toán số lượng chênh lệch và giá trị sai lệch tương ứng."),
        ("F4.3.4", "PH4: Tồn kho", "Kiểm kê & Thẻ kho", "Lập phiếu cân bằng kho", "Thủ kho", "Chủ cửa hàng; Kế toán", "Phiếu cân bằng kho", "Phiếu kiểm kê đã xác nhận nguyên nhân chênh lệch", "Ý kiến phê duyệt chênh lệch", "Số liệu tồn kho được điều chỉnh chuẩn xác; Ghi Thẻ kho", "Chênh lệch giá trị lớn bắt buộc phải có Chủ cửa hàng phê duyệt."),
        ("F4.3.5", "PH4: Tồn kho", "Kiểm kê & Thẻ kho", "Truy xuất Sổ Thẻ kho điện tử", "Thủ kho", "Kế toán", "Sổ Thẻ kho (so_the_kho)", "Mã SKU đồng hồ; Khoảng thời gian tra cứu", "Loại chứng từ (Nhập/Xuất/Cân bằng)", "Sổ chi tiết xuất - nhập - tồn từng biến động", "Dữ liệu Thẻ kho có tính bất biến, đảm bảo tính toàn vẹn kiểm toán."),

        # PH5
        ("F5.1.1", "PH5: Báo cáo", "Dashboard điều hành", "Thẻ chỉ số hiệu suất trọng yếu (KPI)", "Chủ cửa hàng", "Quản lý phân hệ", "Dữ liệu vận hành toàn hệ thống", "Mốc thời gian điều hành (Hôm nay / Tháng này)", "Không", "5 thẻ KPI: Giá trị tồn, Doanh thu, Lệnh xuất đại lý, Khả dụng, Đổi trả", "Cập nhật dữ liệu thời gian thực sau mỗi giao dịch hoàn tất."),
        ("F5.1.2", "PH5: Báo cáo", "Dashboard điều hành", "Biểu đồ trực quan doanh số xuất kho đại lý Canvas", "Chủ cửa hàng", "Kế toán", "Dữ liệu đơn hàng xuất kho đại lý", "Khoảng thời gian 6 tháng gần nhất", "Tùy chọn xem doanh thu hoặc sản lượng chiếc", "Biểu đồ cột/đường vẽ bằng HTML5 Canvas", "Biểu diễn trực quan tốc độ tăng trưởng doanh số kênh sỉ."),
        ("F5.1.3", "PH5: Báo cáo", "Dashboard điều hành", "Bảng xếp hạng Top sản phẩm bán chạy", "Chủ cửa hàng", "Kế toán", "Dữ liệu xuất kho đại lý", "Khoảng thời gian thống kê; Giới hạn Top (5, 10)", "Không", "Danh sách Top mẫu đồng hồ bán chạy nhất", "Xếp hạng song song theo tổng số lượng chiếc bán và theo doanh thu."),
        ("F5.1.4", "PH5: Báo cáo", "Dashboard điều hành", "Dòng thời gian hoạt động (Activity Stream)", "Chủ cửa hàng", "Quản trị hệ thống", "Audit Log giao dịch", "Số lượng sự kiện cần xem gần nhất", "Bộ lọc loại giao dịch", "Dòng thời gian các thao tác vừa phát sinh trong kho", "Giúp ban điều hành nắm bắt nhịp độ vận hành kho tức thời."),

        ("F5.2.1", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Báo cáo chuyên sâu Nhập hàng (Inbound)", "Kế toán", "Chủ cửa hàng", "Phiếu nhập kho; Chi phí", "Khoảng ngày; Nhà cung cấp", "Chi tiết chi phí vận chuyển/hải quan", "Báo cáo cơ cấu giá trị hàng nhập và chi phí phân bổ", "Giúp phân tích chi phí logistics nhập khẩu theo từng hãng sản xuất."),
        ("F5.2.2", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Báo cáo Phân phối Đại lý (Outbound)", "Kế toán", "Chủ cửa hàng", "Lệnh xuất kho đại lý; Phiếu xuất", "Khoảng ngày; Đại lý B2B", "Bộ lọc cấp bậc đại lý (VIP/Bạc/Đồng)", "Báo cáo doanh số xuất kho đại lý, tỷ lệ hoàn tất đơn hàng", "Đánh giá hiệu quả kinh doanh của từng đối tác đại lý."),
        ("F5.2.3", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Báo cáo Cơ cấu xuất hàng", "Thủ kho", "Kế toán", "Phiếu xuất kho các loại", "Khoảng ngày thống kê", "Không", "Biểu đồ tỷ trọng xuất kho đại lý vs Xuất bảo hành vs Xuất hủy", "Kiểm soát chặt chẽ tỷ lệ hàng xuất phi thương mại."),
        ("F5.2.4", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Báo cáo Đổi trả & Chất lượng bộ máy", "Thủ kho", "Chủ cửa hàng", "Phiếu đổi trả; Serial lỗi", "Khoảng ngày; Hãng đồng hồ", "Bộ lọc loại máy (Automatic / Pin Quartz / Solar)", "Tỷ lệ lỗi kỹ thuật theo từng hãng và từng bộ máy", "Cung cấp bằng chứng thực tế phục vụ đàm phán hợp đồng với NCC."),
        ("F5.2.5", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Báo cáo Tồn kho & Hàng Dead Stock", "Thủ kho", "Chủ cửa hàng", "Tồn kho; Ngày nhập Serial", "Ngưỡng ngày lưu kho (ví dụ: > 90 ngày, > 180 ngày)", "Bộ lọc thương hiệu", "Danh sách mẫu đồng hồ lưu kho lâu ngày chậm luân chuyển", "Gợi ý chiến lược khuyến mãi thanh lý sỉ thu hồi vốn."),
        ("F5.2.6", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Báo cáo Tài chính & Lợi nhuận gộp B2B", "Kế toán", "Chủ cửa hàng", "Doanh thu; Giá vốn đích danh", "Khoảng thời gian kỳ kế toán", "Bộ lọc nhóm sản phẩm", "Báo cáo Lợi nhuận gộp (Doanh thu - Giá vốn - Chi phí)", "Tính toán chính xác tuyệt đối nhờ phương pháp Giá vốn đích danh."),
        ("F5.2.7", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Sổ chi tiết công nợ B2B (Đại lý & NCC)", "Kế toán", "Chủ cửa hàng", "Công nợ 2 chiều", "Kỳ kế toán; Đối tác cụ thể hoặc tất cả", "Tùy chọn chỉ xem đối tác còn dư nợ", "Sổ chi tiết: Dư đầu kỳ, Phát sinh nợ, Phát sinh có, Dư cuối kỳ", "Chứng từ kế toán chuẩn mực phục vụ đối soát công nợ định kỳ."),
        ("F5.2.8", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Báo cáo Dòng tiền Thu / Chi (Cashflow)", "Kế toán", "Chủ cửa hàng", "Phiếu thu; Phiếu chi", "Kỳ kế toán; Hình thức thanh toán (CK / Tiền mặt)", "Không", "Báo cáo tổng tiền thu, tổng tiền chi và Dòng tiền thuần", "Kiểm soát an toàn thanh khoản tài chính của cửa hàng."),
        ("F5.2.9", "PH5: Báo cáo", "Báo cáo chuyên sâu", "Xuất báo cáo đa định dạng (Excel/PDF)", "Kế toán", "Chủ cửa hàng", "Dữ liệu báo cáo", "Báo cáo đang xem; Định dạng xuất (Excel / CSV / PDF)", "Tùy chọn in khổ A4 ngang/dọc", "Tệp tin báo cáo tải về máy hoặc lệnh in trực tiếp", "Định dạng bảng biểu chuẩn mực, có tiêu đề và ngày giờ trích xuất.")
    ]

    for r_idx, r_data in enumerate(s2_data, start=5):
        ws2.row_dimensions[r_idx].height = 24
        bg = LIGHT_BG if r_idx % 2 == 1 else WHITE
        fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Arial", size=9)
            cell.fill = fill
            cell.border = thin_border
            if c_idx == 1:
                cell.font = Font(name="Arial", size=9, bold=True, color="1B365D")
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 2:
                cell.font = Font(name="Arial", size=8.5, bold=True, color="C59B27")
                cell.alignment = Alignment(vertical="center")
            elif c_idx == 4:
                cell.font = Font(name="Arial", size=9, bold=True)
                cell.alignment = Alignment(vertical="center")
            elif c_idx in [5, 6]:
                cell.font = Font(name="Arial", size=8.5)
                cell.alignment = Alignment(vertical="center")
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)

    auto_fit_columns(ws2, {1: 10, 2: 18, 3: 24, 4: 32, 5: 18, 6: 22, 7: 20, 8: 35, 9: 30, 10: 35, 11: 45})
    ws2.freeze_panes = "A5"

    # =========================================================================
    # SHEET 3: Trường dữ liệu (Từ điển trường nhập liệu - Data Dictionary)
    # =========================================================================
    ws3 = wb.create_sheet(title="Trường dữ liệu")
    ws3.views.sheetView[0].showGridLines = True

    style_title(ws3, "A1", "TỪ ĐIỂN TRƯỜNG NHẬP LIỆU (DATA DICTIONARY - CHRONOVAULT WMS)")
    style_note(ws3, "A2", "Phân loại trường chính/phụ, kiểu nhập, điều kiện bắt buộc và tác nhân nhập liệu trong 23 bảng CSDL.")

    s3_headers = [
        "Đối tượng / Bảng CSDL", "Tên trường kỹ thuật", "Nhãn hiển thị tiếng Việt", "Nhóm trường",
        "Mức bắt buộc", "Kiểu dữ liệu & Input", "Ràng buộc / Kiểm tra hợp lệ", "Tác nhân nhập dữ liệu"
    ]
    apply_header(ws3, 4, s3_headers, fill_color=NAVY)

    s3_data = [
        # Tài khoản & Người dùng
        ("Tài khoản (users)", "user_id", "Mã người dùng", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Khóa chính; Tự sinh duy nhất", "Hệ thống"),
        ("Tài khoản (users)", "username", "Tên đăng nhập", "Chính", "Bắt buộc", "VARCHAR(50) / Text", "Duy nhất; Tối thiểu 4 ký tự; Không dấu", "Quản trị hệ thống"),
        ("Tài khoản (users)", "email", "Địa chỉ Email", "Chính", "Bắt buộc", "VARCHAR(100) / Email", "Duy nhất; Định dạng email chuẩn", "Quản trị hệ thống"),
        ("Tài khoản (users)", "password_hash", "Mật khẩu mã hóa", "Chính", "Bắt buộc", "VARCHAR(255) / Password", "Băm Bcrypt/Argon2; Không lưu plain text", "Người dùng / Quản trị"),
        ("Tài khoản (users)", "role_id", "Mã vai trò", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại thuộc bảng vai_tro", "Quản trị hệ thống"),
        ("Tài khoản (users)", "full_name", "Họ và tên nhân viên", "Phụ", "Bắt buộc", "NVARCHAR(100) / Text", "Tối đa 100 ký tự", "Quản trị hệ thống"),
        ("Tài khoản (users)", "phone_number", "Số điện thoại", "Phụ", "Tùy chọn", "VARCHAR(20) / Tel", "10 chữ số; Bắt đầu bằng 0", "Người dùng"),
        ("Tài khoản (users)", "account_status", "Trạng thái tài khoản", "Chính", "Bắt buộc", "ENUM / Select", "Thuộc tập: 'ACTIVE', 'LOCKED'", "Quản trị hệ thống"),
        
        # Hàng hóa Master
        ("Đồng hồ (products)", "product_id", "ID sản phẩm nội bộ", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Khóa chính; Tự sinh duy nhất", "Hệ thống"),
        ("Đồng hồ (products)", "sku", "Mã SKU đồng hồ", "Chính", "Bắt buộc", "VARCHAR(50) / Text", "Duy nhất trên toàn hệ thống; Không dấu", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "barcode", "Mã vạch quốc tế", "Chính", "Bắt buộc", "VARCHAR(50) / Barcode", "Duy nhất; 12-13 chữ số chuẩn EAN/UPC", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "product_name", "Tên mẫu đồng hồ", "Chính", "Bắt buộc", "NVARCHAR(255) / Text", "Không để trống; Tối đa 255 ký tự", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "brand_id", "Hãng sản xuất / Thương hiệu", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại bảng thuong_hieu", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "movement_type", "Phân loại bộ máy", "Chính", "Bắt buộc", "ENUM / Select", "'AUTOMATIC', 'QUARTZ', 'SOLAR_ECODRIVE'", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "glass_material", "Chất liệu mặt kính", "Phụ", "Bắt buộc", "NVARCHAR(50) / Select", "'Sapphire Crystal', 'Hardlex', 'Mineral'", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "strap_material", "Chất liệu dây đeo", "Phụ", "Tùy chọn", "NVARCHAR(50) / Text", "'Thép Oystersteel', 'Da cá sấu', 'Cao su'", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "dial_size", "Kích thước mặt số", "Phụ", "Bắt buộc", "DECIMAL(4,1) / Number", "Đơn vị mm (36.0 đến 45.0 mm)", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "water_resistance", "Độ chịu nước", "Phụ", "Bắt buộc", "NVARCHAR(50) / Text", "'30m / 3ATM', '50m', '100m', '300m Diver'", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "warranty_months", "Thời hạn bảo hành hãng", "Phụ", "Bắt buộc", "INT / Number", "Số nguyên dương (tháng, thường 24-60)", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "base_unit", "Đơn vị tính cơ bản", "Chính", "Bắt buộc", "VARCHAR(20) / Select", "Mặc định: 'Chiếc' hoặc 'Cái'", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "wholesale_unit", "Đơn vị tính đóng gói xuất kho", "Chính", "Bắt buộc", "VARCHAR(20) / Select", "'Thùng', 'Kiện', 'Lô'", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "conversion_rate", "Hệ số quy đổi đóng gói", "Chính", "Bắt buộc", "INT / Number", "Số nguyên dương >= 1 (1 Thùng = N Chiếc)", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "moq", "Số lượng đặt hàng đại lý tối thiểu", "Chính", "Bắt buộc", "INT / Number", "Số nguyên dương >= 1 (thường 5 - 10 chiếc)", "Quản trị hệ thống"),
        ("Đồng hồ (products)", "min_stock", "Ngưỡng tồn kho tối thiểu", "Phụ", "Bắt buộc", "INT / Number", "Số nguyên dương; Ngưỡng cảnh báo vàng", "Thủ kho / Quản trị"),
        ("Đồng hồ (products)", "max_stock", "Ngưỡng tồn kho tối đa", "Phụ", "Bắt buộc", "INT / Number", "Số nguyên dương; Ngưỡng cảnh báo đỏ", "Thủ kho / Quản trị"),
        ("Đồng hồ (products)", "wholesale_price_vip", "Giá phân phối đại lý Hạng VIP", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Số dương; Chiết khấu sâu nhất", "Chủ cửa hàng / Quản trị"),
        ("Đồng hồ (products)", "wholesale_price_silver", "Giá phân phối đại lý Hạng Bạc", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Số dương; Cao hơn hạng VIP", "Chủ cửa hàng / Quản trị"),
        ("Đồng hồ (products)", "wholesale_price_bronze", "Giá phân phối đại lý Hạng Đồng", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Số dương; Giá chuẩn cho đại lý mới", "Chủ cửa hàng / Quản trị"),
        ("Đồng hồ (products)", "has_serial", "Cờ quản lý Serial đích danh", "Chính", "Bắt buộc", "BOOLEAN / Checkbox", "Luôn TRUE đối với ngành đồng hồ", "Hệ thống / Quản trị"),

        # Serial / IMEI
        ("Serial (serials)", "serial_id", "ID bản ghi Serial", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Khóa chính tự sinh", "Hệ thống"),
        ("Serial (serials)", "serial_number", "Mã Serial / Số máy", "Chính", "Bắt buộc", "VARCHAR(100) / Barcode", "Duy nhất tuyệt đối; Chuỗi do hãng cấp", "NV Nhập - Xuất"),
        ("Serial (serials)", "product_id", "Mã sản phẩm SKU", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại thuộc bảng san_pham", "NV Nhập - Xuất"),
        ("Serial (serials)", "cost_price", "Giá vốn đích danh", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Giá nhập trên HĐ + Chi phí phân bổ", "Kế toán"),
        ("Serial (serials)", "lifecycle_status", "Trạng thái vòng đời Serial", "Chính", "Bắt buộc", "ENUM / Select", "'TRONG_KHO', 'DA_BAN', 'BAO_HANH', 'TRA_NCC'", "Hệ thống"),
        ("Serial (serials)", "quality_status", "Trạng thái chất lượng kho", "Chính", "Bắt buộc", "ENUM / Select", "'HANG_MOI', 'HANG_TRUNG_BAY', 'HANG_LOI'", "Thủ kho"),
        ("Serial (serials)", "shelf_location_id", "Mã vị trí ngăn kệ", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại thuộc bảng vi_tri_ngan_ke", "Thủ kho"),
        ("Serial (serials)", "warranty_expiry_date", "Ngày hết hạn bảo hành", "Phụ", "Tùy chọn", "DATE / Datepicker", "Tính bằng: Ngày xuất bán + Số tháng BH", "Hệ thống"),

        # Nhà cung cấp
        ("Nhà cung cấp (suppliers)", "supplier_id", "Mã Nhà cung cấp", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Duy nhất; Tiền tố NCC-xxxx", "Quản trị / Kế toán"),
        ("Nhà cung cấp (suppliers)", "supplier_name", "Tên Nhà cung cấp", "Chính", "Bắt buộc", "NVARCHAR(255) / Text", "Tên doanh nghiệp chính thức", "Kế toán"),
        ("Nhà cung cấp (suppliers)", "tax_code", "Mã số thuế NCC", "Chính", "Bắt buộc", "VARCHAR(20) / Text", "10 hoặc 13 chữ số; Duy nhất", "Kế toán"),
        ("Nhà cung cấp (suppliers)", "bank_account", "Số tài khoản ngân hàng", "Chính", "Bắt buộc", "VARCHAR(50) / Text", "Số tài khoản thụ hưởng của NCC", "Kế toán"),
        ("Nhà cung cấp (suppliers)", "bank_name", "Tên ngân hàng thụ hưởng", "Chính", "Bắt buộc", "NVARCHAR(100) / Text", "Tên ngân hàng thương mại", "Kế toán"),
        ("Nhà cung cấp (suppliers)", "total_debt_balance", "Số dư nợ phải trả NCC", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Tự động cộng/trừ qua chứng từ", "Hệ thống"),

        # Đại lý B2B
        ("Đại lý (dealers)", "dealer_id", "Mã Đại lý B2B", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Duy nhất; Tiền tố DL-xxxx", "Quản trị / Kế toán"),
        ("Đại lý (dealers)", "dealer_name", "Tên Đại lý / Chuỗi cửa hàng", "Chính", "Bắt buộc", "NVARCHAR(255) / Text", "Tên thương mại đại lý", "NV Nhập - Xuất"),
        ("Đại lý (dealers)", "dealer_tier", "Phân hạng đại lý", "Chính", "Bắt buộc", "ENUM / Select", "'VIP', 'BAC', 'DONG'", "Chủ cửa hàng"),
        ("Đại lý (dealers)", "credit_limit", "Hạn mức tín dụng nợ", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Hạn mức nợ tối đa được phép nhập hàng đại lý", "Chủ cửa hàng"),
        ("Đại lý (dealers)", "payment_term", "Thời hạn nợ hợp đồng", "Chính", "Bắt buộc", "ENUM / Select", "'THANH_TOAN_NGAY', 'NET_15', 'NET_30'", "Chủ cửa hàng"),
        ("Đại lý (dealers)", "discount_rate", "Tỷ lệ chiết khấu hợp đồng", "Phụ", "Bắt buộc", "DECIMAL(5,2) / Phầm trăm", "Từ 0.00% đến 35.00%", "Chủ cửa hàng"),
        ("Đại lý (dealers)", "current_debt", "Số dư nợ hiện tại", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Dư nợ mua hàng chưa thanh toán", "Hệ thống"),

        # Phiếu nhập kho
        ("Phiếu nhập (receipts)", "receipt_id", "Mã Phiếu nhập kho", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Duy nhất; Tiền tố PN-xxxx", "Hệ thống"),
        ("Phiếu nhập (receipts)", "po_code", "Mã Đơn đặt mua (PO)", "Chính", "Bắt buộc", "VARCHAR(50) / Text", "Khóa ngoại đơn mua hàng PO", "NV Nhập - Xuất"),
        ("Phiếu nhập (receipts)", "supplier_id", "Mã Nhà cung cấp", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại thuộc bảng nha_cung_cap", "NV Nhập - Xuất"),
        ("Phiếu nhập (receipts)", "inbound_date", "Ngày giờ nhập kho", "Chính", "Bắt buộc", "DATETIME / Timestamp", "Mốc thời gian ghi nhận nhập kho", "Hệ thống / NV"),
        ("Phiếu nhập (receipts)", "allocated_extra_costs", "Tổng chi phí phân bổ", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Vận chuyển + Hải quan + Bảo hiểm", "Kế toán"),
        ("Phiếu nhập (receipts)", "total_receipt_amount", "Tổng giá trị phiếu nhập", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Tiền hàng + Chi phí phát sinh", "Hệ thống"),
        ("Phiếu nhập (receipts)", "receipt_status", "Trạng thái phiếu nhập", "Chính", "Bắt buộc", "ENUM / Select", "'DRAFT', 'APPROVED', 'CANCELLED'", "Thủ kho / Kế toán"),

        # Lệnh xuất kho đại lý
        ("Lệnh xuất kho đại lý (orders)", "order_code", "Mã Lệnh xuất kho đại lý", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Duy nhất; Tiền tố DS-xxxx", "Hệ thống"),
        ("Lệnh xuất kho đại lý (orders)", "dealer_id", "Mã Đại lý đặt hàng", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại thuộc bảng dai_ly_b2b", "NV Nhập - Xuất"),
        ("Lệnh xuất kho đại lý (orders)", "order_date", "Ngày lập lệnh xuất đại lý", "Chính", "Bắt buộc", "DATETIME / Timestamp", "Thời điểm phát sinh đơn", "Hệ thống"),
        ("Lệnh xuất kho đại lý (orders)", "deposit_amount", "Số tiền đặt cọc", "Phụ", "Tùy chọn", "DECIMAL(18,2) / Tiền tệ", "Tiền cọc theo thỏa thuận hợp đồng", "Kế toán"),
        ("Lệnh xuất kho đại lý (orders)", "shipping_fee", "Cước vận chuyển bảo đảm", "Phụ", "Tùy chọn", "DECIMAL(18,2) / Tiền tệ", "Phí logistics đóng gói chống sốc", "NV Nhập - Xuất"),
        ("Lệnh xuất kho đại lý (orders)", "order_status", "Trạng thái lệnh xuất kho đại lý", "Chính", "Bắt buộc", "ENUM / Select", "'DRAFT', 'APPROVED', 'PACKING', 'COMPLETED', 'CANCELLED'", "Hệ thống / Chủ shop"),

        # Phiếu kiểm kê & Sổ thẻ kho
        ("Kiểm kê (stock_audits)", "audit_code", "Mã Phiếu kiểm kê", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Duy nhất; Tiền tố KK-xxxx", "Hệ thống"),
        ("Kiểm kê (stock_audits)", "shelf_id", "Mã ngăn kệ kiểm kê", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại thuộc bảng vi_tri_ngan_ke", "Thủ kho"),
        ("Kiểm kê (stock_audits)", "book_qty", "Số lượng trên sổ sách", "Chính", "Bắt buộc", "INT / Number", "Số lượng hệ thống đang ghi nhận", "Hệ thống"),
        ("Kiểm kê (stock_audits)", "actual_qty", "Số lượng đếm thực tế", "Chính", "Bắt buộc", "INT / Number", "Số lượng quét Serial thực tế", "Thủ kho"),
        ("Kiểm kê (stock_audits)", "diff_qty", "Số lượng chênh lệch", "Chính", "Bắt buộc", "INT / Number", "Thực tế trừ Sổ sách (Thừa/Thiếu)", "Hệ thống"),
        ("Sổ Thẻ kho (stock_cards)", "card_id", "Mã dòng thẻ kho", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Khóa chính tự sinh", "Hệ thống"),
        ("Sổ Thẻ kho (stock_cards)", "ref_doc_code", "Mã chứng từ đối ứng", "Chính", "Bắt buộc", "VARCHAR(50) / Text", "Mã PN, PX, KK, DC phát sinh", "Hệ thống"),
        ("Sổ Thẻ kho (stock_cards)", "change_qty", "Số lượng biến động", "Chính", "Bắt buộc", "INT / Number", "Số nguyên (+ khi nhập, - khi xuất)", "Hệ thống"),
        ("Sổ Thẻ kho (stock_cards)", "balance_after", "Tồn kho sau biến động", "Chính", "Bắt buộc", "INT / Number", "Số lượng tồn cập nhật tức thời", "Hệ thống"),

        # Thu / Chi
        ("Chứng từ Thu/Chi", "voucher_code", "Mã Phiếu thu / Phiếu chi", "Chính", "Bắt buộc", "VARCHAR(50) / ID", "Duy nhất; Tiền tố PT-xxxx hoặc PC-xxxx", "Hệ thống"),
        ("Chứng từ Thu/Chi", "partner_id", "Mã Đối tác nộp / nhận", "Chính", "Bắt buộc", "VARCHAR(50) / Select", "Khóa ngoại NCC hoặc Đại lý", "Kế toán"),
        ("Chứng từ Thu/Chi", "amount", "Số tiền giao dịch", "Chính", "Bắt buộc", "DECIMAL(18,2) / Tiền tệ", "Số dương > 0", "Kế toán"),
        ("Chứng từ Thu/Chi", "payment_method", "Hình thức thanh toán", "Chính", "Bắt buộc", "ENUM / Select", "'CHUYEN_KHOAN', 'TIEN_MAT'", "Kế toán"),
        ("Chứng từ Thu/Chi", "bank_reference", "Mã tham chiếu ngân hàng", "Phụ", "Tùy chọn", "VARCHAR(100) / Text", "Mã giao dịch ngân hàng / Ủy nhiệm chi", "Kế toán")
    ]

    for r_idx, r_data in enumerate(s3_data, start=5):
        ws3.row_dimensions[r_idx].height = 22
        bg = LIGHT_BG if r_idx % 2 == 1 else WHITE
        fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws3.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Arial", size=9)
            cell.fill = fill
            cell.border = thin_border
            if c_idx == 1:
                cell.font = Font(name="Arial", size=9, bold=True, color="1B365D")
                cell.alignment = Alignment(vertical="center")
            elif c_idx == 2:
                cell.font = Font(name="Courier New", size=9, bold=True, color="0F172A")
                cell.alignment = Alignment(vertical="center")
            elif c_idx in [4, 5]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if val == "Bắt buộc":
                    cell.font = Font(name="Arial", size=8.5, bold=True, color="DC2626") # red
                else:
                    cell.font = Font(name="Arial", size=8.5, color="64748B")
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)

    auto_fit_columns(ws3, {1: 26, 2: 24, 3: 26, 4: 15, 5: 16, 6: 25, 7: 38, 8: 22})
    ws3.freeze_panes = "A5"

    # =========================================================================
    # SHEET 4: Vai trò và quyền (Ma trận trách nhiệm 5 tác nhân)
    # =========================================================================
    ws4 = wb.create_sheet(title="Vai trò và quyền")
    ws4.views.sheetView[0].showGridLines = True

    style_title(ws4, "A1", "MA TRẬN TRÁCH NHIỆM & RANH GIỚI THẨM QUYỀN 5 TÁC NHÂN (RBAC MATRIX)")
    style_note(ws4, "A2", "Tách quyền quản trị hệ thống, giám sát điều hành, kiểm soát vật lý, tác nghiệp kho và kiểm soát tài chính.")

    s4_headers = [
        "Tác nhân (Actor)", "Mục tiêu vai trò", "Chức năng được thực hiện",
        "Đối tượng phụ trách", "Quyền quyết định & Phê duyệt", "Ranh giới thẩm quyền (Không được làm)"
    ]
    apply_header(ws4, 4, s4_headers, fill_color=NAVY)

    s4_data = [
        (
            "1. Quản trị hệ thống (System Admin)",
            "Bảo đảm an ninh hệ thống, tính sẵn sàng và toàn vẹn dữ liệu phần mềm.",
            "Quản lý tài khoản người dùng; Cấu hình ma trận phân quyền RBAC; Khóa/mở tài khoản; Giám sát nhật ký Audit Log; Thu hồi Token JWT; Cấu hình tham số hệ thống.",
            "Tài khoản người dùng; Nhóm quyền; Cấu hình hệ thống; Nhật ký kiểm toán Audit Log.",
            "Quyết định cấp mới, thu hồi hoặc điều chỉnh quyền truy cập của người dùng trên toàn hệ thống.",
            "Không can thiệp hoặc thay thế Chủ cửa hàng phê duyệt các ngoại lệ nghiệp vụ; Không xử lý tác nghiệp phiếu nhập/xuất hoặc chứng từ thu/chi thường nhật."
        ),
        (
            "2. Chủ cửa hàng (Store Owner / Executive)",
            "Giám sát điều hành toàn diện, kiểm soát hiệu quả tài chính và phê duyệt ngoại lệ nghiệp vụ.",
            "Theo dõi Executive Dashboard và hệ thống 9 báo cáo chuyên sâu; Phê duyệt chi phí nhập hàng vượt ngưỡng; Duyệt lệnh xuất đại lý vượt hạn mức tín dụng; Phê duyệt cân bằng kiểm kê giá trị cao.",
            "Chỉ số KPI; Dòng tiền thu/chi; Công nợ 2 chiều; Tồn kho tài sản; Các ngoại lệ vượt hạn mức.",
            "Quyền quyết định tối cao đối với các giao dịch vượt ngưỡng thẩm quyền của nhân viên cấp dưới.",
            "Không trực tiếp can thiệp cấu hình tài khoản kỹ thuật của hệ thống; Không trực tiếp xử lý các thao tác nhập xuất, kiểm đếm vật lý thường ngày."
        ),
        (
            "3. Thủ kho (Warehouse Head / Quản lý điều hành)",
            "Chịu trách nhiệm toàn diện về quản lý điều hành hoạt động kho và bảo quản an toàn tài sản vật lý.",
            "Quản lý sơ đồ ngăn kệ (Bins); Xác nhận giao nhận vật lý cho phiếu nhập/xuất; Chủ trì kiểm kê định kỳ; Quét đối soát Serial; Cân bằng chênh lệch kho trong thẩm quyền.",
            "Hàng hóa vật lý; Dãy kệ lưu trữ; Mã Serial trong kho; Tình trạng chất lượng 3 kho (Mới/Trưng bày/Lỗi); Biên bản kiểm kê.",
            "Quyết định vị trí lưu kho, kế hoạch lấy hàng (picking), xác nhận xuất kho vật lý và cân bằng chênh lệch trong hạn mức cho phép.",
            "Không lập chứng từ tài chính (phiếu thu/chi); Không cấu hình giá bán/hạn mức tín dụng đại lý; Không tự duyệt chênh lệch kiểm kê vượt ngưỡng quy định."
        ),
        (
            "4. Nhân viên nhập - xuất kho (Operations Staff)",
            "Thực thi tác nghiệp nhập, xuất, đóng gói, kiểm đếm và bảo hành theo đúng quy trình chuẩn.",
            "Lập phiếu nhập kho; Tiếp nhận và quét dải Serial; Lập lệnh xuất kho đại lý nháp; Lấy hàng theo kệ; Quét Serial đóng kiện xuất kho đại lý; Tiếp nhận trả hàng đại lý; Hỗ trợ quét kiểm kê.",
            "Phiếu nhập kho nháp; Lệnh xuất kho đại lý nháp; Kiện hàng đóng gói xuất kho đại lý; Dải Serial quét camera.",
            "Quyết định ghi nhận thông tin chứng từ nháp, từ chối nạp Serial nếu phát hiện trầy xước/lỗi vật lý.",
            "Không duyệt các khoản thu/chi tài chính; Không tự phê duyệt hạn mức tín dụng công nợ đại lý; Không tự ý cân bằng kho khi có chênh lệch kiểm kê."
        ),
        (
            "5. Kế toán (Financial Accountant - Vốn, Kho & Công nợ)",
            "Kiểm soát chi phí nhập hàng, hạch toán công nợ 2 chiều và quản lý dòng tiền B2B an toàn.",
            "Khai báo và phân bổ chi phí lô hàng hình thành Giá vốn đích danh; Thẩm định hạn mức nợ đại lý; Lập Phiếu Thu nợ đại lý; Lập Phiếu Chi NCC; Đối soát sổ nợ 2 chiều; Lập báo cáo tài chính.",
            "Công nợ NCC; Công nợ đại lý; Giá vốn đích danh từng Serial; Phiếu Thu / Phiếu Chi; Sổ chi tiết công nợ; Báo cáo dòng tiền.",
            "Quyết định đủ điều kiện tài chính để duyệt lệnh xuất đại lý; Xác nhận tính hợp lệ của chứng từ thanh toán ngân hàng.",
            "Không thay thế xác nhận giao nhận vật lý của Thủ kho; Các khoản chi và hạn mức vượt ngưỡng bắt buộc phải trình Chủ cửa hàng phê duyệt."
        )
    ]

    for r_idx, r_data in enumerate(s4_data, start=5):
        ws4.row_dimensions[r_idx].height = 45
        bg = LIGHT_BG if r_idx % 2 == 1 else WHITE
        fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Arial", size=9)
            cell.fill = fill
            cell.border = thin_border
            if c_idx == 1:
                cell.font = Font(name="Arial", size=9.5, bold=True, color="1B365D")
                cell.alignment = Alignment(vertical="center")
            elif c_idx == 6:
                cell.font = Font(name="Arial", size=8.5, color="DC2626") # red alert
                cell.alignment = Alignment(vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)

    auto_fit_columns(ws4, {1: 28, 2: 32, 3: 45, 4: 28, 5: 32, 6: 38})
    ws4.freeze_panes = "A5"

    # =========================================================================
    # SHEET 5: Quy tắc nghiệp vụ (18 quy tắc nghiệp vụ trọng yếu)
    # =========================================================================
    ws5 = wb.create_sheet(title="Quy tắc nghiệp vụ")
    ws5.views.sheetView[0].showGridLines = True

    style_title(ws5, "A1", "QUY TẮC NGHIỆP VỤ TRỌNG YẾU (BUSINESS RULES - CHRONOVAULT WMS)")
    style_note(ws5, "A2", "Làm rõ nguyên tắc Serial 100%, quy đổi Thùng/Chiếc, giá vốn đích danh, hạn mức tín dụng và khóa giữ chỗ tồn kho.")

    s5_headers = [
        "Mã quy tắc", "Tên quy tắc nghiệp vụ", "Điều kiện / Sự kiện kích hoạt",
        "Xử lý của hệ thống", "Tác nhân chịu trách nhiệm", "Kết quả / Ràng buộc bắt buộc"
    ]
    apply_header(ws5, 4, s5_headers, fill_color=NAVY)

    s5_data = [
        (
            "RB-01",
            "Định danh Serial/IMEI 100% duy nhất",
            "Khi khởi tạo danh mục đồng hồ và nạp Serial vào kho.",
            "Tự động kiểm tra tính duy nhất trên toàn bộ CSDL; kích hoạt bắt buộc cờ quản lý Serial.",
            "Quản trị hệ thống; NV Nhập - Xuất",
            "Mỗi chiếc đồng hồ là một thực thể độc lập duy nhất; cấm lưu hành đồng hồ không có mã Serial."
        ),
        (
            "RB-02",
            "Quy đổi ĐVT đóng gói xuất kho bắt buộc",
            "Khi khai báo sản phẩm hoặc tạo phiếu nhập/xuất theo Thùng/Kiện.",
            "Tự động nhân hệ số quy đổi: Số chiếc = Số thùng x conversionRate.",
            "Quản trị hệ thống; Kế toán",
            "Hệ số quy đổi là số nguyên dương >= 1. Kiểm soát số lượng chiếc thực tế cần kiểm đếm."
        ),
        (
            "RB-03",
            "Khớp đúng 100% số lượng Serial khi nhập",
            "Khi nạp dải Serial trên Phiếu nhập kho.",
            "Đối soát 2 chiều: Số mã Serial quét được phải bằng chính xác tổng số chiếc quy đổi.",
            "NV Nhập - Xuất; Thủ kho",
            "Chặn không cho phê duyệt nhập kho nếu thiếu hoặc thừa dù chỉ 01 mã Serial."
        ),
        (
            "RB-04",
            "Tính Giá vốn đích danh phân bổ chi phí",
            "Khi kế toán khai báo chi phí lô hàng (vận chuyển, hải quan, bảo hiểm).",
            "Giá vốn Serial = Giá mua HĐ + (Tổng chi phí phân bổ / Tổng số chiếc).",
            "Kế toán",
            "Mỗi chiếc đồng hồ lưu trữ giá vốn đích danh riêng biệt; không dùng giá bình quân giản đơn."
        ),
        (
            "RB-05",
            "Kiểm tra số lượng đặt hàng đại lý tối thiểu (MOQ)",
            "Khi nhân viên lập lệnh xuất kho đại lý cho đại lý.",
            "Kiểm tra: Số lượng chiếc đặt của từng SKU >= MOQ đã cấu hình cho mẫu đó.",
            "NV Nhập - Xuất",
            "Cảnh báo và chặn lưu đơn nếu không đạt MOQ (thường từ 5 – 10 chiếc/mẫu)."
        ),
        (
            "RB-06",
            "Kiểm soát Tồn kho khả dụng thời gian thực",
            "Khi kiểm tra khả năng đáp ứng lệnh xuất kho đại lý.",
            "Tồn khả dụng = Tồn thực tế - Tồn đang giữ chỗ (Reserved).",
            "Hệ thống; Thủ kho",
            "Chỉ cho phép lên đơn trong phạm vi Tồn khả dụng; triệt tiêu hoàn toàn nguy cơ xuất âm kho."
        ),
        (
            "RB-07",
            "Áp giá đại lý tự động theo cấp bậc đại lý",
            "Khi chọn đại lý đối tác trên lệnh xuất kho đại lý.",
            "Tự động tra cứu hạng đại lý (VIP/Bạc/Đồng) và áp đơn giá phân phối đại lý + chiết khấu tương ứng.",
            "Hệ thống; Kế toán",
            "Đại lý VIP hưởng mức giá tốt nhất; nhân viên không được tự ý sửa giá bán sai chính sách."
        ),
        (
            "RB-08",
            "Thẩm định Hạn mức tín dụng công nợ (Credit Limit)",
            "Trước khi phê duyệt lệnh xuất kho đại lý.",
            "Kiểm tra: Dư nợ hiện tại + Giá trị đơn mới - Tiền cọc <= Hạn mức tín dụng đại lý.",
            "Kế toán; Chủ cửa hàng",
            "Vượt hạn mức phải được Chủ cửa hàng phê duyệt ngoại lệ ghi rõ lý do trước khi xuất hàng."
        ),
        (
            "RB-09",
            "Khóa hàng Giữ chỗ (Reserved Allocation)",
            "Khi lệnh xuất kho đại lý được phê duyệt thành công.",
            "Chuyển trạng thái số lượng hàng sang Giữ chỗ (Reserved); trừ trực tiếp vào Tồn khả dụng.",
            "Hệ thống; Thủ kho",
            "Đảm bảo hàng đã hứa bán cho đại lý này không bị bán trùng lặp cho đại lý khác."
        ),
        (
            "RB-10",
            "Giải phóng hàng Giữ chỗ khi hủy lệnh xuất đại lý",
            "Khi lệnh xuất kho đại lý bị hủy bỏ do đại lý không hoàn tất cọc hoặc vi phạm.",
            "Tự động giải phóng số lượng giữ chỗ; cộng hoàn trả lại cho Tồn khả dụng.",
            "Hệ thống; NV Nhập - Xuất",
            "Trả lại trạng thái sẵn sàng xuất kho đại lý cho các đơn hàng tiếp theo ngay lập tức."
        ),
        (
            "RB-11",
            "Quét Serial thực tế đối soát khi xuất kho",
            "Khi thủ kho soạn hàng đóng kiện theo phiếu xuất.",
            "Quét kiểm tra từng Serial: Phải thuộc SKU của đơn, trạng thái TRONG_KHO và HANG_MOI.",
            "Thủ kho; NV Nhập - Xuất",
            "Không cho phép đóng gói Serial không đúng quy cách hoặc đang thuộc kho lỗi."
        ),
        (
            "RB-12",
            "Chuyển trạng thái Serial ĐÃ BÁN & Gán bảo hành",
            "Khi hoàn tất xác nhận bàn giao xuất kho xuất kho đại lý.",
            "Cập nhật Serial sang DA_BAN; gán mã đại lý sở hữu; tính ngày hết hạn bảo hành.",
            "Hệ thống; Thủ kho",
            "Kích hoạt thời hạn bảo hành chính thức; trừ tồn thực tế; giải phóng tồn giữ chỗ."
        ),
        (
            "RB-13",
            "Tạm khóa xuất nhập khu vực khi kiểm kê",
            "Khi kích hoạt đợt kiểm kê theo ngăn kệ / toàn kho.",
            "Khóa tạm thời các thao tác tạo phiếu nhập/xuất tác động lên các ngăn kệ đang kiểm đếm.",
            "Thủ kho; Hệ thống",
            "Ngăn chặn biến động dữ liệu tức thời gây sai lệch số liệu đối soát kiểm kê."
        ),
        (
            "RB-14",
            "Phân loại chênh lệch kiểm kê (Khớp / Thừa / Thiếu)",
            "Sau khi hoàn tất quét Serial thực tế tại kệ.",
            "Đối soát tự động với sổ sách: Tách danh sách Serial Khớp đúng, Serial Thừa và Serial Thiếu.",
            "Hệ thống; Thủ kho",
            "Xác định chính xác vị trí và nguyên nhân thất thoát hoặc để nhầm ngăn kệ."
        ),
        (
            "RB-15",
            "Phân cấp thẩm quyền Phê duyệt Cân bằng kho",
            "Khi có chênh lệch thừa/thiếu giữa thực tế và sổ sách.",
            "Chênh lệch trong hạn mức: Thủ kho duyệt; Chênh lệch vượt hạn mức: Chủ cửa hàng duyệt.",
            "Thủ kho; Chủ cửa hàng",
            "Kiểm soát chặt chẽ thất thoát tài sản có giá trị cao; ghi vết lý do vào Audit Log."
        ),
        (
            "RB-16",
            "Tính bất biến của Sổ Thẻ kho & Audit Log",
            "Mọi giao dịch làm tăng/giảm số lượng tồn kho.",
            "Ghi phát sinh dòng mới vào bảng so_the_kho (+/-) kèm mã Serial; cấm UPDATE hoặc DELETE.",
            "Hệ thống",
            "Đảm bảo toàn vẹn dữ liệu kế toán kho; nếu sai sót phải lập phiếu điều chỉnh đối ứng."
        ),
        (
            "RB-17",
            "Chu trình khép kín Công nợ qua Thu / Chi",
            "Khi giao nhận hàng hoàn tất hoặc phát sinh thanh toán.",
            "Nhập kho -> Tăng nợ NCC; Phiếu Chi -> Trừ nợ NCC; Xuất kho đại lý -> Tăng nợ đại lý; Phiếu Thu -> Trừ nợ đại lý.",
            "Kế toán; Hệ thống",
            "Dòng tiền và công nợ luôn đồng bộ tuyệt đối với luồng di chuyển vật lý của hàng hóa."
        ),
        (
            "RB-18",
            "Phân loại chất lượng 3 kho độc lập",
            "Khi nhập hàng, đổi trả hoặc phát sinh hỏng hóc kỹ thuật.",
            "Tách biệt hàng thành 3 trạng thái: Kho Hàng Mới, Kho Hàng Trưng Bày và Kho Hàng Lỗi.",
            "Thủ kho",
            "Nghiêm cấm xuất kho đại lý hàng trưng bày hoặc hàng lỗi cho đại lý nếu không có phê duyệt thanh lý."
        )
    ]

    for r_idx, r_data in enumerate(s5_data, start=5):
        ws5.row_dimensions[r_idx].height = 36
        bg = LIGHT_BG if r_idx % 2 == 1 else WHITE
        fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws5.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Arial", size=9)
            cell.fill = fill
            cell.border = thin_border
            if c_idx == 1:
                cell.font = Font(name="Arial", size=9.5, bold=True, color="1B365D")
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 2:
                cell.font = Font(name="Arial", size=9, bold=True, color="0F172A")
                cell.alignment = Alignment(vertical="center")
            elif c_idx == 6:
                cell.font = Font(name="Arial", size=8.5, color="B45309") # amber / alert
                cell.alignment = Alignment(vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)

    auto_fit_columns(ws5, {1: 12, 2: 32, 3: 35, 4: 45, 5: 25, 6: 45})
    ws5.freeze_panes = "A5"

    # Remove the default sheet that openpyxl created
    if default_sheet.title in wb.sheetnames:
        wb.remove(default_sheet)

    # Save to disk
    output_filename = "Bang_Phan_He_Quan_Ly_Kho_Dong_Ho.xlsx"
    output_path = os.path.join(r"D:\cntt\pbhb", output_filename)
    wb.save(output_path)
    print(f"SUCCESS: Successfully generated {output_path} with 5 sheets!")

if __name__ == "__main__":
    build_wms_excel()

