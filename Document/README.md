# Đề tài: Lập Trình Mạng - Nhóm 5 AE Siêu Nhân
### Hệ Thống Quản Lý Kho Hàng Hóa Cửa Hàng Đồng Hồ (ChronoVault B2B Wholesale WMS)

---

## 📌 1. Thành viên nhóm & Phân công 5 Tác Nhân Nghiệp Vụ (5 Actors & Subsystems)

1. **Phan Bá Hải Bình** (Nhóm trưởng) — **🛡️ Quản Trị Hệ Thống (`SYSTEM_ADMIN`)**
   - **Phân hệ phụ trách (TV1):** Quản lý Danh mục Hàng hóa, Cấu hình Ma trận RBAC, Truy vết Vòng đời Serial & Nhật ký Audit Log.
   - **Tài khoản Demo:** `@binh_admin` (Mật khẩu: `admin123`) • **Nhánh Git:** `feature/product`

2. **Nguyễn Đắc Quân** & **Tô Đức Thảo** — **📦 Nhân Viên Nhập - Xuất Kho (`OPERATIONS_STAFF`)**
   - **Phân hệ phụ trách (TV2 & TV3):** 
     - *TV2 (Quân):* Đối tác Nhà cung cấp & Quản lý Nhập kho (Nhánh `feature/inbound`).
     - *TV3 (Thảo):* Khách sỉ & Phân phối xuất hàng B2B (Nhánh `feature/outbound`).
     - *Nghiệp vụ tiền tuyến:* Cầm máy quét Barcode Serial nạp kho, soạn hàng, đóng kiện xuất bến.
   - **Tài khoản Demo:** `@quan_thao_ops` (Mật khẩu: `123`)

3. **Võ Công Tâm** — **🏢 Thủ Kho Điều Hành (`WAREHOUSE_MANAGER`)**
   - **Phân hệ phụ trách (TV4):** Quản lý Tồn kho, Sơ đồ ngăn kệ Bin/Rack, Ký xác nhận giao nhận vật lý, Chủ trì kiểm kê & Cân bằng kho.
   - **Tài khoản Demo:** `@tam_manager` (Mật khẩu: `123`) • **Nhánh Git:** `feature/inventory`

4. **Trần Công Tú** — **💰 Kế Toán Kho & Công Nợ (`ACCOUNTANT`)**
   - **Phân hệ phụ trách (TV5):** Báo cáo thống kê & Dashboard, Phân bổ giá vốn đích danh từng Serial, Quản lý công nợ đại lý 2 chiều, Lập phiếu thu/chi.
   - **Tài khoản Demo:** `@tu_accountant` (Mật khẩu: `123`) • **Nhánh Git:** `feature/dashboard`

5. **Ban Điều Hành Tối Cao** — **👑 Chủ Cửa Hàng (`STORE_OWNER`)**
   - **Vai trò điều hành tối cao:** Giám sát Dashboard KPI doanh thu, dòng tiền; Phê duyệt các ngoại lệ vượt trần (đại lý nợ quá hạn mức tín dụng, chi phí phát sinh lớn, cân bằng kiểm kê giá trị cao).
   - **Tài khoản Demo:** `@owner_boss` (Mật khẩu: `admin123`)

---

## 🎯 2. Nguyên tắc Bất Kiêm Nhiệm Vụ (Segregation of Duties - SoD)

Hệ thống áp dụng triệt để nguyên tắc **Kiểm soát bốn mắt (Four-Eyes Principle)** và **Bất kiêm nhiệm vụ** theo tài liệu đặc tả [`DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.md`](DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.md):

| Tác Nhân (Actor) | Tên Vai Trò Hệ Thống | Phạm Vi Quyền Hạn Thực Tế (RBAC) | Ranh Giới Thẩm Quyền (Không Được Làm) |
| :--- | :--- | :--- | :--- |
| **1. Quản trị hệ thống** 🛡️ | `SYSTEM_ADMIN` | Cấu hình tham số, cấp tài khoản, thiết lập ma trận RBAC, giám sát Audit Log. | Không thao tác hoặc phê duyệt các chứng từ nhập/xuất kho, phiếu thu/chi hay công nợ. |
| **2. Chủ cửa hàng** 👑 | `STORE_OWNER` | Giám sát KPI doanh thu, dòng tiền; phê duyệt ngoại lệ công nợ vượt hạn mức, chi phí lớn. | Không can thiệp cấu hình kỹ thuật, không làm các thao tác nhập xuất thường nhật. |
| **3. Thủ kho điều hành** 🏢 | `WAREHOUSE_MANAGER` | Quản lý sơ đồ kệ Bin/Rack, xác nhận giao nhận vật lý, chủ trì kiểm kê & cân bằng kho. | Không lập chứng từ thu/chi tiền, không can thiệp giá bán & hạn mức nợ sỉ. |
| **4. NV Nhập - Xuất kho** 📦 | `OPERATIONS_STAFF` | Tác nghiệp quét Barcode Serial nạp kho, soạn hàng, đóng kiện xuất bán sỉ B2B. | Không duyệt thu/chi tiền, không tự duyệt đơn bán sỉ vượt hạn mức nợ. |
| **5. Kế toán kho** 💰 | `ACCOUNTANT` | Phân bổ giá vốn đích danh, kiểm soát công nợ 2 chiều, lập phiếu thu/chi tiền. | Không ký nhận bàn giao vật lý thay Thủ kho, không tự duyệt chi vượt ngưỡng. |

---

## 📖 3. Giới thiệu đề tài & 4 Nguyên lý quản trị cốt lõi

Hệ thống phần mềm quản lý kho chuyên biệt cho mô hình **B2B Wholesale Distribution** (Phân phối bán sỉ cho các chuỗi đại lý cửa hàng đồng hồ xa xỉ cao cấp như Rolex, Omega, Patek Philippe, Audemars Piguet...).

1. **Quản lý định danh Serial/IMEI 100%:** Mỗi chiếc đồng hồ sở hữu duy nhất một mã Serial độc bản. Truy vết xuyên suốt vòng đời 6 bước: *Nhập mới $\rightarrow$ Lưu kho Kệ Bin $\rightarrow$ Khóa giữ chỗ đơn sỉ $\rightarrow$ Đóng gói xuất kho $\rightarrow$ Bàn giao đại lý $\rightarrow$ Bảo hành / Đổi trả*.
2. **Quy cách đóng gói đa cấp:** Nhập/xuất theo **Thùng / Kiện** và tự động quy đổi ra **Chiếc lẻ**; kiểm soát số lượng đặt tối thiểu (**MOQ**).
3. **Giá vốn đích danh (Specific Identification):** Cộng dồn chi phí vận chuyển quốc tế, thuế hải quan, bảo hiểm trực tiếp vào từng mã Serial cụ thể.
4. **Quản lý công nợ khép kín:** Kiểm soát hạn mức tín dụng (**Credit Limit**) đại lý, đối soát công nợ 2 chiều qua Phiếu Thu / Phiếu Chi.

---

## 💾 4. Kiến trúc Cơ sở Dữ liệu (Database Architecture)

* **Công nghệ:** Google Android Jetpack **Room Database** v4 chạy trên nền tảng **SQLite** nhúng.
* **Cơ chế:** ORM tiêu chuẩn của Google, xử lý đọc/ghi bất đồng bộ bằng Kotlin Coroutines (`Dispatchers.IO`) đảm bảo UI mượt mà 60fps.
* **Vị trí mã nguồn:** Thư mục [`../android/app/src/main/java/com/example/chronovaultwms/core/database/`](../android/app/src/main/java/com/example/chronovaultwms/core/database/)
  - `ChronoVaultDatabase.kt`: Quản trị Singleton CSDL, `version = 4`, tự động migration.
  - `ProductEntity.kt`: Bảng `products` lưu 12 trường dữ liệu luxury horology.
  - `SerialEntity.kt`: Bảng `serials` quản lý Serial đích danh, giá vốn, vị trí kệ Bin (`K1-A01`).
  - `UserEntity.kt`: Bảng `users` lưu danh sách người dùng và vai trò RBAC.
  - `AuditLogEntity.kt`: Bảng `audit_logs` lưu nhật ký kiểm toán hệ thống bất biến.
  - `DatabaseSeeder.kt`: Nạp sẵn 10 mẫu đồng hồ xa xỉ, 10 mã Serial, 5 tài khoản tương ứng 5 tác nhân và nhật ký mẫu.
* **Vị trí file vật lý trên thiết bị/máy ảo Android:**
  ```text
  /data/data/com.example.chronovaultwms/databases/chronovault_wms.db
  ```
* **Cách xem trực tiếp dữ liệu trong Android Studio:** Mở **View $\rightarrow$ Tool Windows $\rightarrow$ App Inspection $\rightarrow$ Database Inspector** khi ứng dụng đang chạy.

---

## ✅ 5. Tiến độ hoàn thành phân hệ TV1 (Phan Bá Hải Bình)

Phân hệ TV1 đã được cài đặt và kiểm thử hoàn chỉnh 100% trên máy ảo Pixel 7 Pro (Android 14):
- [x] **Quản lý Danh mục Hàng hóa:** Danh sách 10 mẫu đồng hồ cao cấp với ảnh minh họa, nhãn thương hiệu, phân cấp đóng gói Thùng/Chiếc, giá niêm yết, giá sỉ B2B.
- [x] **Bộ lọc & Tìm kiếm Real-time:** Tìm kiếm tức thời theo SKU, Model, Thương hiệu, Bộ sưu tập; chip lọc nhanh theo Hãng.
- [x] **Thêm mới Hàng hóa & Auto Serial:** Form thêm sản phẩm với đầy đủ 12 trường dữ liệu, tự động sinh mã Serial đầu tiên và cập nhật tức thì vào Room Database.
- [x] **Truy vết Vòng đời Serial (Lifecycle Timeline):** Stepper 6 bước trực quan biểu diễn trạng thái vật lý của chiếc đồng hồ.
- [x] **Quản trị Hệ thống & Bảo mật:**
  - Nút chuyển đổi nhanh 5 Tác nhân nghiệp vụ (Quick 1-Click Login).
  - Hộp thoại Quản trị 3 Tab: Danh sách tài khoản, Ma trận phân quyền RBAC Matrix, Nhật ký kiểm toán Audit Log Trail.
  - Chức năng Đổi Gmail / Cập nhật hồ sơ trực tiếp trong ứng dụng có kiểm tra quyền hạn (Admin hoặc Chính chủ).

---

## 📁 6. Thư mục Tài liệu đính kèm (Document)

Toàn bộ hồ sơ phân tích thiết kế chính thức của đề tài được lưu trữ trong thư mục này:

- **Kế hoạch & Bộ Prompt 5 thành viên:**
  - 📄 [`KE_HOACH_CHI_TIET_VA_BO_PROMPT_TOAN_DIEN_5_THANH_VIEN.docx`](KE_HOACH_CHI_TIET_VA_BO_PROMPT_TOAN_DIEN_5_THANH_VIEN.docx)
- **Báo cáo phân tích thiết kế hệ thống:**
  - 📄 [`BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.docx`](BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.docx) (Bản Word nộp bài)
  - 📝 [`BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.md`](BAO_CAO_PHAN_TICH_THIET_KE_HE_THONG.md) (Bản Markdown kỹ thuật)
- **Bảng phân tích các phân hệ & chức năng con:**
  - 📄 [`BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.docx`](BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.docx)
  - 📝 [`BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.md`](BANG_PHAN_TICH_CAC_PHAN_HE_HE_THONG_KHO_DONG_HO.md)
- **Bảng phân hệ & từ điển dữ liệu (Excel 5 Sheet chuẩn):**
  - 📊 [`Bang_Phan_He_Quan_Ly_Kho_Dong_Ho.xlsx`](Bang_Phan_He_Quan_Ly_Kho_Dong_Ho.xlsx) *(45 chức năng con, 81 trường dữ liệu, 5 Actor, 18 Quy tắc)*
- **Bản đặc tả nhiệm vụ 5 tác nhân nghiệp vụ:**
  - 📄 [`DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.docx`](DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.docx)
  - 📝 [`DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.md`](DAC_TA_NHIEM_VU_CONG_VIEC_5_ACTOR.md)
- **Tổng quan đề tài:**
  - 📝 [`TONG_QUAN_DE_TAI.md`](TONG_QUAN_DE_TAI.md)

---

## 🚀 7. Quy chuẩn Code Android Studio & Hướng dẫn làm việc nhóm

### 1. Cấu trúc thư mục Code Android (`android/app/src/main/java/com/example/chronovaultwms/`)
Mỗi thành viên chỉ viết code trong đúng thư mục phân hệ của mình:
- `core/`: **Dùng chung** (Chứa `ChronoVaultDatabase`, Entity, DAO, `RetrofitClient`, `SessionManager`, `SystemEnums`).
- `product/`: **TV1 (Phan Bá Hải Bình)** - Quản lý Danh mục Hàng hóa & Quản trị Hệ thống.
- `inbound/`: **TV2 (Nguyễn Đắc Quân)** - Quản lý Đối tác NCC & Nhập kho.
- `outbound/`: **TV3 (Tô Đức Thảo)** - Quản lý Đại lý sỉ & Xuất hàng B2B.
- `inventory/`: **TV4 (Võ Công Tâm)** - Quản lý Vị trí kệ Bin/Rack & Kiểm kê kho.
- `dashboard/`: **TV5 (Trần Công Tú)** - Báo cáo thống kê, Biểu đồ & Dashboard.

---

### 2. Quy chuẩn vị trí & Đặt tên file giao diện XML (`android/app/src/main/res/layout/`)
Để **tuyệt đối không bị xung đột (conflict) tên file giữa 5 thành viên**, bắt buộc dùng tiền tố theo phân hệ:
- **TV1:** Bắt đầu bằng `fragment_product_...` hoặc `item_product_...`, `dialog_product_...`, `dialog_user_...`, `dialog_system_...`
- **TV2:** Bắt đầu bằng `fragment_inbound_...` hoặc `item_inbound_...`, `dialog_inbound_...`
- **TV3:** Bắt đầu bằng `fragment_outbound_...` hoặc `item_outbound_...`, `dialog_outbound_...`
- **TV4:** Bắt đầu bằng `fragment_inventory_...` hoặc `item_inventory_...`, `dialog_inventory_...`
- **TV5:** Bắt đầu bằng `fragment_dashboard_...` hoặc `item_dashboard_...`

---

### 3. Quy trình làm việc trên Git (Branching Workflow)
1. **Kéo code mới nhất từ nhánh `main` về máy:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Tạo nhánh riêng theo đúng tên phân hệ trước khi code:**
   ```bash
   git checkout -b feature/ten-thanh-vien-chuc-nang
   ```
   *Ví dụ:* `feature/tv2-inbound`, `feature/tv3-outbound`, `feature/tv4-inventory`, `feature/tv5-dashboard`.
3. **Tuyệt đối KHÔNG commit và push trực tiếp lên nhánh `main`.**
4. Sau khi hoàn thành chức năng trên nhánh riêng:
   ```bash
   git add .
   git commit -m "feat: mo ta chuc nang da lam"
   git push origin feature/ten-nhanh-cua-ban
   ```
5. Lên GitHub tạo **Pull Request (PR)** để Nhóm trưởng (**Phan Bá Hải Bình**) review và merge vào nhánh `main`.

---

*Nhóm 5 AE Siêu Nhân • Đồ án môn học Lập Trình Mạng • Đại học Kiến trúc Đà Nẵng (DAU)*
