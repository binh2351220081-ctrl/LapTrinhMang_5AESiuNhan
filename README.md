# Đề tài: Lập Trình Mạng - Nhóm 5 AE Siu Nhân
### Hệ Thống Quản Lý Kho Hàng Hóa Cửa Hàng Đồng Hồ (ChronoVault B2B Wholesale WMS)

---

## 📌 Thành viên nhóm
1. **Phan Bá Hải Bình** (Nhóm trưởng) - *Phụ trách TV1: Quản lý Hàng hóa & Quản trị Hệ thống*
2. **Nguyễn Đắc Quân** - *Phụ trách TV2: Đối tác Nhà cung cấp & Quản lý Nhập kho*
3. **Tô Đức Thảo** - *Phụ trách TV3: Khách sỉ & Bán sỉ - Phân phối xuất hàng*
4. **Võ Công Tâm** - *Phụ trách TV4: Quản lý Tồn kho, Vị trí kệ & Kiểm kê*
5. **Trần Công Tú** - *Phụ trách TV5: Báo cáo thống kê & Dashboard điều hành*

---

## 📖 Giới thiệu đề tài
Hệ thống phần mềm quản lý kho chuyên biệt cho mô hình **B2B Wholesale Distribution** (Phân phối bán sỉ cho đại lý và chuỗi cửa hàng đồng hồ cao cấp).

### Các nguyên lý quản trị cốt lõi:
- **Quản lý định danh Serial/IMEI 100%:** Truy vết xuyên suốt vòng đời từng chiếc đồng hồ từ khi nhập kho đến khi bán cho đại lý và bảo hành.
- **Quy cách đóng gói đa cấp:** Nhập/xuất theo **Thùng / Kiện** và tự động quy đổi ra **Chiếc lẻ**; kiểm soát số lượng đặt tối thiểu (**MOQ**).
- **Giá vốn đích danh (Specific Identification):** Cộng dồn chi phí vận chuyển quốc tế, thuế hải quan và bảo hiểm vào từng mã Serial.
- **Quản lý công nợ khép kín:** Kiểm soát hạn mức tín dụng (**Credit Limit**) đại lý, đối soát công nợ 2 chiều qua Phiếu Thu / Phiếu Chi.

---

## 📁 Tài liệu đính kèm
Các tệp tài liệu và báo cáo chính thức của đề tài được lưu trữ trực tiếp trong thư mục dự án:

- **Kế hoạch toàn diện & Bộ Prompt chuẩn mực 5 thành viên (MỚI):**
  - 📄 [KE_HOACH_CHI_TIET_VA_BO_PROMPT_TOAN_DIEN_5_THANH_VIEN.docx](KE_HOACH_CHI_TIET_VA_BO_PROMPT_TOAN_DIEN_5_THANH_VIEN.docx) *(Bản đặc tả chi tiết 5 giai đoạn: PTTK, Web Client, Lập trình Mạng/API/Socket, App Android Studio và Kiểm thử tích hợp)*
- **Báo cáo phân tích thiết kế hệ thống:**
  - 📄 [BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.docx](BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.docx) (Bản Word nộp bài)
  - 📝 [BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.md](BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.md) (Bản Markdown kỹ thuật)
- **Bảng phân tích các phân hệ & chức năng con:**
  - 📄 [BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.docx](BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.docx)
  - 📝 [BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.md](BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.md)
- **Bảng phân hệ & từ điển dữ liệu (Excel 5 Sheet chuẩn):**
  - 📊 [Bang_Phan_He_Quan_Ly_Kho_Dong_Ho.xlsx](Bang_Phan_He_Quan_Ly_Kho_Dong_Ho.xlsx) *(Gồm: Phân hệ tổng quan, Phân rã 45 chức năng con, Từ điển 81 trường dữ liệu, Ma trận 5 Actor và 18 Quy tắc nghiệp vụ)*
- **Bảng xác định chức năng con:**
  - 📄 [Bang_Xac_Dinh_Chuc_Nang_Con_He_Thong_Quan_Ly_Kho_Dong_Ho_Docx (1).docx](Bang_Xac_Dinh_Chuc_Nang_Con_He_Thong_Quan_Ly_Kho_Dong_Ho_Docx%20(1).docx)
  - 📝 [Bang_Xac_Dinh_Chuc_Nang_Con_He_Thong_Quan_Ly_Kho_Dong_Ho_Docx (1).md](Bang_Xac_Dinh_Chuc_Nang_Con_He_Thong_Quan_Ly_Kho_Dong_Ho_Docx%20(1).md)
- **Bản đặc tả nhiệm vụ công việc:**
  - 📄 [DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.docx](DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.docx)
  - 📝 [DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.md](DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.md)
- **Tổng quan đề tài:**
  - 📝 [TONG_QUAN_DE_TAI.md](TONG_QUAN_DE_TAI.md)

---

## 🌐 Giao diện & Mã nguồn hệ thống
- **Cổng trung tâm tích hợp 5 phân hệ:** [index.html](index.html) *(Chế độ Mobile App Simulator & Toàn màn hình)*
- **Trang chức năng độc lập của từng thành viên:**
  - **Phan Bá Hải Bình (TV1):** [tv1_hang_hoa.html](tv1_hang_hoa.html) (Hàng hóa & Serial) & [tv1_he_thong.html](tv1_he_thong.html) (Tài khoản & Audit Log)
  - **Nguyễn Đắc Quân (TV2):** [tv2_nhap_kho.html](tv2_nhap_kho.html) (NCC & Nhập kho)
  - **Tô Đức Thảo (TV3):** [tv3_xuat_kho.html](tv3_xuat_kho.html) (Đại lý sỉ & Xuất kho)
  - **Võ Công Tâm (TV4):** [tv4_ton_kho.html](tv4_ton_kho.html) (Tồn kho, Vị trí kệ & Kiểm kê)
  - **Trần Công Tú (TV5):** [tv5_bao_cao.html](tv5_bao_cao.html) (Dashboard & Báo cáo)

---

## 🚀 Hướng dẫn làm việc nhóm & Quy chuẩn Code Android Studio

### 1. Cấu trúc thư mục Code Android (`android/app/src/main/java/com/example/chronovaultwms/`)
Mỗi thành viên chỉ viết code trong đúng thư mục phân hệ của mình:
- `core/`: **Dùng chung** (Chứa `ChronoVaultDatabase`, DAO, `RetrofitClient`, `ApiService`, `SessionManager`, `SystemEnums`).
- `product/`: **TV1** - Quản lý Danh mục Đồng hồ & Serial Number (`ProductListFragment.kt`...).
- `inbound/`: **TV2** - Quản lý Nhà cung cấp & Nhập kho (`InboundReceiptFragment.kt`...).
- `outbound/`: **TV3** - Quản lý Đại lý sỉ & Xuất kho (`OutboundOrderFragment.kt`...).
- `inventory/`: **TV4** - Quản lý Vị trí kệ Bin/Rack & Kiểm kê (`WarehouseMapFragment.kt`...).
- `dashboard/`: **TV5** - Báo cáo thống kê, Biểu đồ & Dashboard (`DashboardOverviewFragment.kt`...).

---

### 2. Quy chuẩn vị trí & Đặt tên file giao diện XML (`android/app/src/main/res/`)
Toàn bộ file giao diện XML nằm trong thư mục `res/layout/`. Để **không bao giờ bị trùng tên file giữa 5 người**, bắt buộc tuân thủ quy tắc tiền tố:
- **TV1:** Bắt đầu bằng `fragment_product_...` hoặc `item_product_...` *(VD: `fragment_product_list.xml`, `item_serial_card.xml`)*
- **TV2:** Bắt đầu bằng `fragment_inbound_...` hoặc `item_inbound_...` *(VD: `fragment_inbound_receipt.xml`, `item_po_order.xml`)*
- **TV3:** Bắt đầu bằng `fragment_outbound_...` hoặc `item_outbound_...` *(VD: `fragment_outbound_order.xml`, `item_so_order.xml`)*
- **TV4:** Bắt đầu bằng `fragment_inventory_...` hoặc `item_inventory_...` *(VD: `fragment_inventory_map.xml`, `item_bin_rack.xml`)*
- **TV5:** Bắt đầu bằng `fragment_dashboard_...` *(VD: `fragment_dashboard_overview.xml`, `fragment_inventory_alert.xml`)*

---

### 3. Quy trình làm việc trên Git (Branching Workflow)
1. **Kéo code mới nhất từ nhánh `main` về máy:**
   ```bash
   git pull origin main
   ```
2. **Tạo nhánh riêng của mình trước khi code:**
   ```bash
   git checkout -b feature/ten-thanh-vien-chuc-nang
   ```''
   *Ví dụ:* `feature/tv1-product`, `feature/tv2-inbound`, `feature/tv3-outbound`, `feature/tv4-inventory`, `feature/tv5-dashboard`.
3. **Tuyệt đối KHÔNG commit và push trực tiếp lên nhánh `main`.**
4. Sau khi hoàn thành chức năng trên nhánh riêng:
   ```bash
   git add .
   git commit -m "feat: mo ta chuc nang da lam"
   git push origin feature/ten-nhanh-cua-ban
   ```
5. Lên GitHub tạo **Pull Request (PR)** để Nhóm trưởng (**Phan Bá Hải Bình**) duyệt và merge vào nhánh `main`.

---

---
*Nhóm 5 AE Siu Nhân • Đồ án môn học Lập Trình Mạng*
