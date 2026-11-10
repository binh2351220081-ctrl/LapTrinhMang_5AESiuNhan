# -*- coding: utf-8 -*-
"""
Script to systematically eliminate the phrase 'bán sỉ' and replace it with
professional WMS & Outbound Fulfillment / B2B Distribution terminology
across all Markdown documents, guideline files, and Word generator scripts.
"""

import os
import re

# Directory paths
BASE_DIR = r"D:\cntt\pbhb"
DOC_DIR = os.path.join(BASE_DIR, "Document")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")

# Target Markdown and text files
MD_FILES = [
    os.path.join(DOC_DIR, "BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.md"),
    os.path.join(DOC_DIR, "BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.md"),
    os.path.join(DOC_DIR, "DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.md"),
    os.path.join(DOC_DIR, "TONG_QUAN_DE_TAI.md"),
    os.path.join(DOC_DIR, "BO_PROMPT_CHI_TIET_5_THANH_VIEN.md"),
    os.path.join(DOC_DIR, "BAO_CAO_PHAN_CONG_VIEC_PHAN_BA_HAI_BINH.md"),
    os.path.join(DOC_DIR, "HUONG_DAN_LAM_BAO_CAO_WORD_CHO_TUNG_THANH_VIEN.md"),
    os.path.join(DOC_DIR, "README.md"),
    os.path.join(BASE_DIR, "README.md"),
    os.path.join(DOC_DIR, "phantichLTM.txt"),
    os.path.join(BASE_DIR, "source", "index.html"),
    os.path.join(BASE_DIR, "source", "tv1_he_thong.html"),
    os.path.join(BASE_DIR, "source", "tv3_xuat_kho.html"),
    os.path.join(BASE_DIR, "js", "data.js"),
    os.path.join(BASE_DIR, "js", "tv1_products.js"),
    os.path.join(BASE_DIR, "js", "tv1_system.js"),
    os.path.join(BASE_DIR, "js", "tv3_outbound.js"),
    os.path.join(BASE_DIR, "js", "tv5_reports.js"),
]

# Target Python scripts
PY_FILES = [
    os.path.join(TOOLS_DIR, "generate_subsystems_docx.py"),
    os.path.join(TOOLS_DIR, "build_full_report_docx.py"),
    os.path.join(TOOLS_DIR, "build_actor_job_specs_docx.py"),
    os.path.join(TOOLS_DIR, "build_full_project_guide_docx.py"),
    os.path.join(TOOLS_DIR, "create_excel_wms.py"),
    os.path.join(TOOLS_DIR, "generate_report_binh_docx.py"),
    os.path.join(TOOLS_DIR, "generate_android_prompts_docx.py"),
    os.path.join(TOOLS_DIR, "generate_word_guideline_docx.py"),
]

# Replacement rules ordered strictly from longest/most specific to shortest/general
REPLACEMENTS = [
    # 1. Project Title & Headers
    ("HỆ THỐNG QUẢN LÝ KHO & PHÂN PHỐI BÁN SỈ ĐỒNG HỒ CAO CẤP B2B (CHRONOVAULT WMS)", "HỆ THỐNG QUẢN LÝ KHO & PHÂN PHỐI ĐỒNG HỒ CAO CẤP B2B (CHRONOVAULT WMS)"),
    ("Hệ Thống Quản Lý Kho & Phân Phối Bán Sỉ Đồng Hồ Cao Cấp B2B (ChronoVault WMS)", "Hệ Thống Quản Lý Kho & Phân Phối Đồng Hồ Cao Cấp B2B (ChronoVault WMS)"),
    ("Hệ Thống Quản Lý Kho & Phân Phối Bán Sỉ Đồng Hồ Cao Cấp B2B", "Hệ Thống Quản Lý Kho & Phân Phối Đồng Hồ Cao Cấp B2B"),
    ("Hệ thống Quản lý Kho & Phân phối Bán sỉ Đồng Hồ Cao Cấp B2B", "Hệ thống Quản lý Kho & Phân phối Đồng Hồ Cao Cấp B2B"),
    ("Hệ thống Quản lý Kho & Phân Phối Bán Sỉ Đồng Hồ Cao Cấp B2B", "Hệ thống Quản lý Kho & Phân Phối Đồng Hồ Cao Cấp B2B"),
    ("Hệ Thống Quản Lý Kho & Phân Phối Bán Sỉ Đồng Hồ Cao Cấp", "Hệ Thống Quản Lý Kho & Phân Phối Đồng Hồ Cao Cấp"),
    ("Hệ thống Quản lý Kho & Phân phối Bán sỉ", "Hệ thống Quản lý Kho & Phân phối B2B"),
    ("QUẢN LÝ KHO HÀNG HÓA CỬA HÀNG ĐỒNG HỒ (BÁN SỈ B2B)", "QUẢN LÝ KHO HÀNG HÓA CỬA HÀNG ĐỒNG HỒ (PHÂN PHỐI ĐẠI LÝ B2B)"),

    # 2. Subsystem 3 Title & Headings
    ("PH3: Khách Sỉ & Bán Sỉ - Xuất Hàng", "PH3: Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Khách Sỉ & Bán Sỉ - Xuất Hàng", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Khách sỉ & Bán sỉ - Xuất Hàng", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("BÁN SỈ & PHÂN PHỐI ĐẠI LÝ - XUẤT HÀNG", "ĐỐI TÁC ĐẠI LÝ & QUẢN LÝ XUẤT KHO"),
    ("Bán sỉ & Phân phối đại lý - Xuất hàng", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Bán Sỉ & Phân Phối Đại Lý - Xuất Hàng", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("BÁN SỈ & XUẤT HÀNG ĐA NĂNG (ĐƠN SỈ, XUẤT SỈ, BẢO HÀNH/HỦY)", "QUẢN LÝ XUẤT KHO ĐẠI LÝ & ĐIỀU CHUYỂN"),
    ("BÁN SỈ & XUẤT HÀNG ĐA NĂNG", "QUẢN LÝ XUẤT KHO ĐẠI LÝ & ĐIỀU CHUYỂN"),
    ("Bán Sỉ & Xuất Hàng Đa Năng", "Quản Lý Xuất Kho Đại Lý & Điều Chuyển"),
    ("Bán sỉ & Xuất hàng đa năng", "Quản lý xuất kho đại lý & điều chuyển"),
    ("Khách sỉ, Bán sỉ & Xuất kho", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Khách Sỉ, Bán Sỉ & Xuất Kho", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Bán sỉ B2B & Xuất kho", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Bán sỉ & Xuất kho", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Bán Sỉ & Xuất Kho", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Bán Sỉ & Xuất Hàng", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Bán sỉ & Xuất hàng", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Bán sỉ và Xuất hàng", "Đối Tác Đại Lý và Quản Lý Xuất Kho"),
    ("bán sỉ và xuất kho", "xuất kho đại lý"),
    ("bán sỉ và xuất hàng", "quản lý xuất kho đại lý"),
    ("Khách sỉ và Bán sỉ", "Đối tác Đại lý"),
    ("Khách Sỉ và Bán Sỉ", "Đối Tác Đại Lý"),
    ("khách sỉ và bán sỉ", "đối tác đại lý"),
    ("KHÁCH SỈ & BÁN SỈ - XUẤT HÀNG", "ĐỐI TÁC ĐẠI LÝ & QUẢN LÝ XUẤT KHO"),
    ("KHÁCH SỈ & BÁN SỈ", "ĐỐI TÁC ĐẠI LÝ"),
    ("KHÁCH HÀNG SỈ, BÁN SỈ & XUẤT KHO", "ĐỐI TÁC ĐẠI LÝ & QUẢN LÝ XUẤT KHO"),

    # 3. Model & Business Terms
    ("Phân phối Bán sỉ B2B Wholesale Distribution", "Phân phối Đại lý B2B (B2B Wholesale Distribution)"),
    ("Phân phối Bán sỉ B2B", "Phân phối Đại lý B2B"),
    ("phân phối bán sỉ B2B", "phân phối đại lý B2B"),
    ("Phân phối Bán sỉ", "Phân phối Đại lý"),
    ("phân phối bán sỉ", "phân phối đại lý"),
    ("Bán sỉ B2B", "Phân phối Đại lý B2B"),
    ("bán sỉ B2B", "phân phối đại lý B2B"),

    # 4. Reports & Statistics
    ("Báo cáo Phân phối Bán sỉ", "Báo cáo Xuất kho Phân phối Đại lý"),
    ("báo cáo phân phối bán sỉ", "báo cáo xuất kho phân phối đại lý"),
    ("Báo cáo bán sỉ", "Báo cáo xuất kho đại lý"),
    ("báo cáo bán sỉ", "báo cáo xuất kho đại lý"),
    ("Báo cáo cơ cấu xuất bán sỉ", "Báo cáo cơ cấu xuất kho đại lý"),
    ("báo cáo cơ cấu xuất bán sỉ", "báo cáo cơ cấu xuất kho đại lý"),
    ("tỷ trọng xuất bán sỉ", "tỷ trọng xuất kho đại lý"),
    ("Tỷ trọng xuất bán sỉ", "Tỷ trọng xuất kho đại lý"),
    ("Doanh thu bán sỉ", "Doanh số xuất kho đại lý"),
    ("doanh thu bán sỉ", "doanh số xuất kho đại lý"),

    # 5. Orders & Processing
    ("tiếp nhận & xử lý đơn bán sỉ", "tiếp nhận & xử lý lệnh xuất kho đại lý"),
    ("Tiếp nhận & Xử lý đơn bán sỉ", "Tiếp nhận & Xử lý lệnh xuất kho đại lý"),
    ("Khởi tạo đơn bán sỉ", "Khởi tạo lệnh xuất kho đại lý"),
    ("khởi tạo đơn bán sỉ", "khởi tạo lệnh xuất kho đại lý"),
    ("Lập đơn bán sỉ nháp", "Lập lệnh xuất kho đại lý nháp"),
    ("lập đơn bán sỉ nháp", "lập lệnh xuất kho đại lý nháp"),
    ("Lập đơn bán sỉ", "Lập lệnh xuất kho đại lý"),
    ("lập đơn bán sỉ", "lập lệnh xuất kho đại lý"),
    ("Lên đơn bán sỉ", "Lập lệnh xuất kho đại lý"),
    ("lên đơn bán sỉ", "lập lệnh xuất kho đại lý"),
    ("tạo đơn bán sỉ", "tạo lệnh xuất kho đại lý"),
    ("Tạo đơn bán sỉ", "Tạo lệnh xuất kho đại lý"),
    ("đơn bán sỉ nháp", "lệnh xuất kho đại lý nháp"),
    ("Đơn bán sỉ nháp", "Lệnh xuất kho đại lý nháp"),
    ("đơn bán sỉ mới", "lệnh xuất kho đại lý mới"),
    ("Đơn bán sỉ mới", "Lệnh xuất kho đại lý mới"),
    ("đơn bán sỉ đã duyệt", "lệnh xuất kho đại lý đã duyệt"),
    ("Đơn bán sỉ đã duyệt", "Lệnh xuất kho đại lý đã duyệt"),
    ("đơn đặt hàng bán sỉ", "đơn đặt hàng xuất kho đại lý"),
    ("Đơn đặt hàng bán sỉ", "Đơn đặt hàng xuất kho đại lý"),
    ("đơn bán sỉ", "lệnh xuất kho đại lý"),
    ("Đơn bán sỉ", "Lệnh xuất kho đại lý"),
    ("ĐƠN BÁN SỈ", "LỆNH XUẤT KHO ĐẠI LÝ"),
    ("đơn đặt sỉ", "đơn đặt hàng đại lý"),
    ("Đơn đặt sỉ", "Đơn đặt hàng đại lý"),
    ("đặt hàng sỉ", "đặt hàng đại lý"),
    ("Đặt hàng sỉ", "Đặt hàng đại lý"),
    ("đặt sỉ", "đặt hàng đại lý"),
    ("Đặt sỉ", "Đặt hàng đại lý"),

    # 6. Physical Outbound & Packing
    ("thực xuất kho bán sỉ", "thực xuất kho phân phối đại lý"),
    ("Thực xuất kho bán sỉ", "Thực xuất kho phân phối đại lý"),
    ("Thực xuất bán sỉ", "Thực xuất kho đại lý"),
    ("thực xuất bán sỉ", "thực xuất kho đại lý"),
    ("xuất bán sỉ", "xuất kho đại lý"),
    ("Xuất bán sỉ", "Xuất kho đại lý"),
    ("XUẤT BÁN SỈ", "XUẤT KHO ĐẠI LÝ"),
    ("đóng kiện xuất sỉ", "đóng kiện xuất kho đại lý"),
    ("Đóng kiện xuất sỉ", "Đóng kiện xuất kho đại lý"),
    ("đóng gói xuất sỉ", "đóng gói xuất kho đại lý"),
    ("Đóng gói xuất sỉ", "Đóng gói xuất kho đại lý"),
    ("quét xuất sỉ", "quét xuất kho đại lý"),
    ("Quét xuất sỉ", "Quét xuất kho đại lý"),
    ("quét Serial đóng kiện xuất sỉ", "quét Serial đóng kiện xuất kho đại lý"),
    ("xuất sỉ", "xuất kho đại lý"),
    ("Xuất sỉ", "Xuất kho đại lý"),
    ("XUẤT SỈ", "XUẤT KHO ĐẠI LÝ"),

    # 7. Returns & Customer Service
    ("tiếp nhận đổi trả sỉ", "tiếp nhận trả hàng đại lý"),
    ("Tiếp nhận đổi trả sỉ", "Tiếp nhận trả hàng đại lý"),
    ("đổi trả sỉ", "nhận trả hàng đại lý"),
    ("Đổi trả sỉ", "Nhận trả hàng đại lý"),
    ("ĐỔI TRẢ SỈ", "NHẬN TRẢ HÀNG ĐẠI LÝ"),

    # 8. Money, Debt, Credit
    ("phiếu thu tiền sỉ", "phiếu thu nợ đại lý"),
    ("Phiếu Thu tiền sỉ", "Phiếu Thu nợ đại lý"),
    ("Phiếu thu tiền sỉ", "Phiếu thu nợ đại lý"),
    ("thu tiền bán sỉ", "thu hồi công nợ đại lý"),
    ("Thu tiền bán sỉ", "Thu hồi công nợ đại lý"),
    ("thu tiền sỉ", "thu hồi công nợ đại lý"),
    ("Thu tiền sỉ", "Thu hồi công nợ đại lý"),
    ("tiền cọc sỉ", "tiền bảo chứng xuất kho đại lý"),
    ("Tiền cọc sỉ", "Tiền bảo chứng xuất kho đại lý"),
    ("tiền cọc đơn sỉ", "tiền cọc đơn xuất kho"),
    ("Tiền cọc đơn sỉ", "Tiền cọc đơn xuất kho"),
    ("tiền nợ sỉ", "công nợ đại lý"),
    ("áp giá sỉ tự động", "áp giá phân phối đại lý tự động"),
    ("áp giá sỉ", "áp giá đại lý"),
    ("Áp giá sỉ", "Áp giá đại lý"),

    # 9. Prices & Packaging Units
    ("đơn giá bán sỉ niêm yết", "đơn giá phân phối đại lý niêm yết"),
    ("Đơn giá bán sỉ niêm yết", "Đơn giá phân phối đại lý niêm yết"),
    ("giá bán sỉ niêm yết", "giá phân phối đại lý niêm yết"),
    ("Giá bán sỉ niêm yết", "Giá phân phối đại lý niêm yết"),
    ("giá bán sỉ", "giá phân phối đại lý"),
    ("Giá bán sỉ", "Giá phân phối đại lý"),
    ("GIÁ BÁN SỈ", "GIÁ PHÂN PHỐI ĐẠI LÝ"),
    ("giá sỉ", "giá phân phối đại lý"),
    ("Giá sỉ", "Giá phân phối đại lý"),
    ("công nợ sỉ", "công nợ đại lý"),
    ("Công nợ sỉ", "Công nợ đại lý"),
    ("sản lượng sỉ", "sản lượng xuất kho"),
    ("Sản lượng sỉ", "Sản lượng xuất kho"),
    ("đại lý sỉ B2B", "đại lý B2B"),
    ("Đại lý sỉ B2B", "Đại lý B2B"),
    ("Đại Lý Sỉ B2B", "Đại Lý B2B"),
    ("Đại Lý & Xuất Sỉ", "Đối Tác Đại Lý & Quản Lý Xuất Kho"),
    ("Đại lý & xuất sỉ", "Đối tác đại lý & xuất kho"),
    ("đại lý sỉ", "đại lý B2B"),
    ("Đại lý sỉ", "Đại lý B2B"),
    ("ĐẠI LÝ SỈ", "ĐẠI LÝ B2B"),
    ("khách hàng sỉ", "đối tác đại lý"),
    ("Khách hàng sỉ", "Đối tác đại lý"),
    ("khách sỉ", "đối tác đại lý"),
    ("Khách sỉ", "Đối tác đại lý"),
    ("KHÁCH SỈ", "ĐỐI TÁC ĐẠI LÝ"),
    ("đơn hàng sỉ", "đơn hàng xuất đại lý"),
    ("Đơn hàng sỉ", "Đơn hàng xuất đại lý"),
    ("Đơn Hàng Sỉ", "Đơn Hàng Xuất Đại Lý"),
    ("đơn sỉ", "lệnh xuất đại lý"),
    ("Đơn sỉ", "Lệnh xuất đại lý"),
    ("ĐƠN SỈ", "LỆNH XUẤT ĐẠI LÝ"),
    ("đổi trả hàng sỉ", "tiếp nhận trả hàng đại lý"),
    ("Đổi trả hàng sỉ", "Tiếp nhận trả hàng đại lý"),
    ("hàng sỉ", "hàng đại lý"),
    ("Hàng sỉ", "Hàng đại lý"),
    ("tín dụng sỉ", "tín dụng đại lý"),
    ("Tín dụng sỉ", "Tín dụng đại lý"),
    ("Tín Dụng Sỉ", "Tín Dụng Đại Lý"),
    ("Phiếu Thu Tiền Sỉ", "Phiếu Thu Nợ Đại Lý"),
    ("tiền sỉ", "thu nợ đại lý"),
    ("Tiền sỉ", "Thu nợ đại lý"),
    ("Tiền Sỉ", "Thu Nợ Đại Lý"),
    ("thanh toán sỉ", "thanh toán công nợ"),
    ("Thanh toán sỉ", "Thanh toán công nợ"),
    ("thu hồi nợ mua sỉ", "thu hồi công nợ đại lý"),
    ("mua sỉ", "nhập hàng đại lý"),
    ("Mua sỉ", "Nhập hàng đại lý"),
    ("phân phối sỉ", "phân phối đại lý"),
    ("Phân phối sỉ", "Phân phối đại lý"),
    ("Doanh thu phân phối sỉ", "Doanh thu xuất kho đại lý"),
    ("doanh thu phân phối sỉ", "doanh số xuất kho đại lý"),
    ("doanh thu sỉ", "doanh số xuất kho đại lý"),
    ("Doanh thu sỉ", "Doanh số xuất kho đại lý"),
    ("doanh số sỉ", "doanh số xuất kho đại lý"),
    ("Doanh số sỉ", "Doanh số xuất kho đại lý"),
    ("đóng gói sỉ", "đóng gói xuất kho"),
    ("Đóng gói sỉ", "Đóng gói xuất kho"),
    ("xuất sỉ", "xuất kho đại lý"),
    ("Xuất sỉ", "Xuất kho đại lý"),
    ("XUẤT SỈ", "XUẤT KHO ĐẠI LÝ"),
    ("nợ sỉ", "nợ đại lý"),
    ("Nợ sỉ", "Nợ đại lý"),
    ("ĐVT bán sỉ", "ĐVT đóng gói xuất kho"),
    ("ĐVT sỉ", "ĐVT đóng gói"),
    ("đơn vị tính bán sỉ", "đơn vị tính đóng gói xuất kho"),
    ("Đơn vị tính bán sỉ", "Đơn vị tính đóng gói xuất kho"),
    ("đóng gói bán sỉ", "đóng gói xuất kho"),
    ("Đóng gói bán sỉ", "Đóng gói xuất kho"),
    ("Quy cách đóng gói bán sỉ", "Quy cách đóng gói xuất kho đại lý"),
    ("Quy cách đóng gói sỉ", "Quy cách đóng gói xuất kho đại lý"),
    ("quy cách đóng gói sỉ", "quy cách đóng gói xuất kho đại lý"),

    # 10. General fallbacks
    ("bán sỉ", "xuất kho đại lý"),
    ("Bán sỉ", "Xuất kho đại lý"),
    ("Bán Sỉ", "Xuất Kho Đại Lý"),
    ("BÁN SỈ", "XUẤT KHO ĐẠI LÝ"),
]

def clean_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 0
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    replacement_count = 0

    for old, new in REPLACEMENTS:
        if old in content:
            cnt = content.count(old)
            content = content.replace(old, new)
            replacement_count += cnt

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath} ({replacement_count} replacements)")
    else:
        print(f"No changes needed for {filepath}")

    return replacement_count

def main():
    print("=" * 60)
    print("STARTING COMPREHENSIVE REPLACEMENT OF 'BÁN SỈ'...")
    print("=" * 60)

    total_replacements = 0

    print("\n--- Processing Markdown Files ---")
    for f in MD_FILES:
        total_replacements += clean_file(f)

    print("\n--- Processing Python Script Files ---")
    for f in PY_FILES:
        total_replacements += clean_file(f)

    print("\n" + "=" * 60)
    print(f"TOTAL REPLACEMENTS ACROSS ALL FILES: {total_replacements}")
    print("=" * 60)

if __name__ == "__main__":
    main()
