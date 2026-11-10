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

## 🚀 Hướng dẫn làm việc nhóm

### 1. Quy định phân nhánh Git (Branching Policy)
- Mỗi thành viên tạo nhánh riêng khi phát triển:
  ```bash
  git checkout -b feature/ten-thanh-vien-chuc-nang
  ```
  *Ví dụ:* `feature/binh-quan-ly-hang-hoa`, `feature/quan-nhap-kho-serial`
- **Tuyệt đối KHÔNG push trực tiếp lên nhánh `main`.**

### 2. Quy chuẩn Commit Message
Đặt tên commit rõ ràng, có tiền tố hành động:
- `feat: thêm chức năng quét barcode camera cho phiếu nhập`
- `fix: sửa lỗi tính giá vốn đích danh khi phân bổ chi phí`
- `docs: cập nhật bảng phân tích phân hệ và README`
- `style: điều chỉnh giao diện dark mode horology`

### 3. Quy trình Review & Merge
1. Hoàn thành chức năng $\rightarrow$ Push nhánh của mình lên remote repository:
   ```bash
   git push origin feature/ten-thanh-vien-chuc-nang
   ```
2. Tạo **Pull Request (PR)** trên GitHub/GitLab vào nhánh `main`.
3. Ghi rõ mô tả các việc đã làm và ảnh chụp màn hình kiểm thử.
4. Nhóm trưởng (**Phan Bá Hải Bình**) sẽ review code, kiểm tra xung đột và thực hiện merge vào nhánh `main`.

---
*Nhóm 5 AE Siu Nhân • Đồ án môn học Lập Trình Mạng*
