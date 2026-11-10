# BÁO CÁO PHÂN TÍCH HỆ THỐNG THÔNG TIN — PHẦN CÔNG VIỆC CỦA PHAN BÁ HẢI BÌNH
> **Học phần:** Phân Tích Hệ Thống Thông Tin | **Khoa:** Công Nghệ Thông Tin — Đại học Kiến trúc Đà Nẵng (DAU)  
> **Giảng viên hướng dẫn:** TS. Đặng Hùng Vĩ  
> **Đề tài:** Hệ Thống Quản Lý Kho & Phân Phối Bán Sỉ Đồng Hồ Cao Cấp B2B (ChronoVault WMS)  
> **Sinh viên thực hiện:** Phan Bá Hải Bình (Nhóm trưởng / System Architect / Phụ trách Phân hệ 1)  
> **Nhóm:** 5 AE Siêu Nhân (Bình, Quân, Thảo, Tâm, Tú)

---

## 1. ĐẶT TÊN ĐỀ TÀI & PHÂN TÍCH BÀI TOÁN

### 1.1. Tên đề tài đề xuất
**Hệ Thống Quản Lý Kho & Phân Phối Bán Sỉ Đồng Hồ Cao Cấp B2B (ChronoVault WMS)**

### 1.2. Phân tích 3 thành phần cấu thành tên đề tài:
- **Loại hình / Hành động:** Hệ thống Quản trị Kho vận đa cấp & Điều phối Chuỗi cung ứng sỉ B2B (Warehouse Management System - WMS).
- **Chức năng chính:** Quản lý định danh Serial Number 100%, Tự động quy đổi Đơn vị tính (ĐVT) đa cấp (Thùng - Chiếc lẻ), Kiểm soát hạn mức công nợ & khóa giữ chỗ, Hạch toán giá vốn đích danh (Specific Identification Costing).
- **Đối tượng / Lĩnh vực:** Ngành phân phối đồng hồ cao cấp xa xỉ (Luxury Horology Wholesale Distribution).

### 1.3. Bảng 1.1: So sánh ChronoVault WMS với các giải pháp trên thị trường:
| Tiêu chí so sánh | Phần mềm bán lẻ phổ thông (KiotViet, Sapo) | ERP Quốc tế cao cấp (SAP B1, Oracle NetSuite) | ERP Mã nguồn mở (Odoo WMS) | **Hệ thống ChronoVault WMS (Đề tài)** |
|:---|:---|:---|:---|:---|
| **Mô hình mục tiêu** | Bán lẻ B2C / Tạp hóa / POS | Doanh nghiệp sản xuất đa quốc gia | Quản trị doanh nghiệp tổng thể | **Bán sỉ B2B phân phối độc quyền Đồng hồ Xa xỉ** |
| **Quản lý Serial/IMEI** | Tùy chọn (chủ yếu quản lý số lượng tổng) | Hỗ trợ đầy đủ nhưng cấu hình cực kỳ phức tạp | Cần cài thêm module trả phí | **Bắt buộc 100% định danh từng chiếc, chống trùng tuyệt đối** |
| **Quy đổi ĐVT đa cấp** | Chỉ nhân chia số lượng giản đơn | Hỗ trợ đa cấp UoM | Hỗ trợ UoM | **Nhập Thùng tự động ép quét đủ N mã Serial lẻ bằng Camera** |
| **Phương pháp Giá vốn** | Bình quân gia quyền / FIFO giản đơn | Bình quân / FIFO / Đích danh | Bình quân gia quyền | **Giá vốn Đích danh cộng dồn chi phí vận chuyển & thuế vào từng Serial** |
| **Nền tảng vận hành** | Web / POS máy tính bảng | Desktop Client nặng nề | Web App | **Android Studio Native (Kotlin MVVM), quét mã vạch bằng Camera điện thoại** |
| **Chi phí đầu tư** | Vài trăm ngàn/tháng (thiếu nghiệp vụ sỉ) | Hàng chục ngàn USD phí bản quyền | Tốn chi phí tùy biến lớn | **Tối ưu chi phí, triển khai gọn nhẹ trên thiết bị di động nội bộ** |

---

## 2. ĐẶC TẢ YÊU CẦU CHỨC NĂNG (PHÂN HỆ 1 - PHAN BÁ HẢI BÌNH)

| Mã YC | Tên yêu cầu | Mô tả chi tiết | Ưu tiên | Nguồn |
|:---:|:---|:---|:---:|:---|
| **FR-01** | Đăng nhập & Xác thực bảo mật | Xác thực danh tính người dùng bằng Email/Username và mật khẩu mã hóa (BCrypt/SHA-256). Cấp quyền phiên làm việc lưu trong `SessionManager`. Tự động đăng xuất khi hết hạn. | **Cao** | System Admin / Store Owner |
| **FR-02** | Kiểm soát Phân quyền RBAC | Kiểm soát truy cập dựa trên 5 vai trò hệ thống: `SYSTEM_ADMIN` (Quản trị hệ thống), `STORE_OWNER` (Chủ cửa hàng), `WAREHOUSE_MANAGER` (Thủ kho), `OPERATIONS_STAFF` (Nhân viên nhập - xuất kho), `ACCOUNTANT` (Kế toán kho). Ngăn chặn người dùng trái phép can thiệp chức năng ngoài quyền hạn. | **Cao** | System Admin |
| **FR-03** | Quản lý Danh mục Đồng hồ Cao cấp | Khai báo và quản lý hồ sơ Master Data từng mẫu đồng hồ xa xỉ: Mã SKU duy nhất, Tên mẫu, Hãng (Rolex, Omega, Patek...), Bộ sưu tập, Loại máy (Automatic, Quartz, Solar), Chất liệu vỏ (Vàng 18K, Thép, Titanium), Mặt kính Sapphire, Độ chống nước, Upload ảnh sản phẩm. | **Cao** | Store Owner / System Admin |
| **FR-04** | Quản lý ĐVT Đa cấp & Tỷ lệ Quy đổi | Thiết lập cấu trúc Đơn vị tính 2 cấp bắt buộc: ĐVT Cơ sở ("Chiếc") và ĐVT Đóng gói ("Thùng" hoặc "Hộp"). Lưu trữ tỷ lệ quy đổi `conversionRate` (1 Thùng = N Chiếc) làm căn cứ tự động cho phân hệ Nhập kho (TV2) và Xuất kho (TV3). | **Cao** | Warehouse Manager |
| **FR-05** | Định mức Tồn kho & Cảnh báo an toàn | Thiết lập mức tồn kho tối thiểu (`minStockAlert`) và tối đa (`maxStockAlert`) cho từng mẫu đồng hồ. Hiển thị cảnh báo trực quan màu vàng/đỏ khi tồn khả dụng chạm ngưỡng an toàn. | **Trung bình** | Store Owner / Quản lý kho |
| *FR-06 → FR-20* | *[Các phân hệ của TV2, TV3, TV4, TV5]* | *Bao gồm các yêu cầu chức năng về Nhập kho NCC (TV2 Quân), Phân phối Bán sỉ & Khóa giữ chỗ (TV3 Thảo), Ma trận Kệ Bin & Kiểm kê (TV4 Tâm), Executive Dashboard & 9 Báo cáo (TV5 Tú).* | *Cao* | *Nhóm 5 AE Siêu Nhân* |

---

## 3. PHÂN TÍCH ĐỐI TƯỢNG & NHÓM CHỨC NĂNG

### 3.1. Danh sách Đối tượng (Entities cốt lõi do Bình thiết kế)
| Mã ĐT | Tên đối tượng | Mô tả | Thuộc tính chính | Quan hệ với đối tượng khác |
|:---:|:---|:---|:---|:---|
| **ENT-01** | **User (Người dùng)** | Quản lý thông tin tài khoản nhân viên và lãnh đạo trong hệ thống WMS. | `id`, `username`, `password_hash`, `full_name`, `email`, `role`, `is_active`, `created_at` | Thuộc 1 Role (1-1); Tạo nhiều Giao dịch (1-N) |
| **ENT-02** | **Role (Vai trò)** | Quản lý 5 nhóm quyền hạn truy cập nghiệp vụ trong hệ thống. | `role_code`, `role_name`, `description`, `permissions_json` | Gán cho nhiều User (1-N) |
| **ENT-03** | **Product (Mẫu đồng hồ)** | Lưu trữ Master Data mẫu đồng hồ cao cấp chuẩn Luxury Horology. | `sku`, `name`, `brand`, `collection`, `movement_type`, `case_material`, `wholesale_price`, `conversion_rate`, `min_stock`, `max_stock` | Chứa nhiều Serial định danh (1-N); Thuộc 1 Brand (N-1) |
| **ENT-04** | **Brand (Thương hiệu)** | Danh bạ các hãng đồng hồ xa xỉ chính hãng (Thụy Sỹ, Nhật, Đức). | `brand_id`, `brand_name`, `origin_country`, `website` | Chứa nhiều Product (1-N) |
| **ENT-05** | **UnitOfMeasure (ĐVT)** | Định nghĩa quy cách đóng gói đa cấp (Chiếc, Thùng, Hộp). | `uom_id`, `uom_name`, `uom_type`, `conversion_factor` | Áp dụng cho nhiều Product (1-N) |

### 3.2. Bảng 5 Phân hệ của Hệ thống:
- **MOD-01: Quản trị Hệ thống & Danh mục Luxury Horology (Phan Bá Hải Bình phụ trách):** Quản lý bảo mật, xác thực người dùng, phân quyền RBAC 5 Roles, danh mục thông số đồng hồ xa xỉ, thiết lập ĐVT 2 cấp và cấu trúc CSDL Room Core.
- **MOD-02: Quản lý Đối tác NCC & Nhập kho Quy đổi ĐVT (Nguyễn Đắc Quân phụ trách)**
- **MOD-03: Quản lý Đại lý B2B & Phân phối Xuất kho (Tô Đức Thảo phụ trách)**
- **MOD-04: Quản trị Tồn kho Nội bộ & Kiểm kê Kệ hàng (Võ Công Tâm phụ trách)**
- **MOD-05: Executive Dashboard & Hệ thống 9 Báo cáo (Trần Công Tú phụ trách)**

---

## 4. PHÂN TÍCH CHỨC NĂNG ĐẾN TẬN CÙNG (PHÂN HỆ 1)

### 4.1. Cấu trúc phân rã chức năng (Functional Decomposition Tree)
```text
MOD-01: Phân hệ Quản trị Hệ thống & Danh mục Luxury Horology (Phan Bá Hải Bình)
├── F1.1: Quản trị Xác thực & Kiểm soát Phân quyền Người dùng (RBAC)
│    ├── F1.1.1: Đăng nhập bảo mật & Khởi tạo phiên làm việc (SessionManager)
│    ├── F1.1.2: Phân quyền theo 5 vai trò hệ thống (SYSTEM_ADMIN, STORE_OWNER, WAREHOUSE_MANAGER, OPERATIONS_STAFF, ACCOUNTANT)
│    └── F1.1.3: Quản lý danh sách tài khoản & Khóa/Mở khóa nhân viên vi phạm
└── F1.2: Quản lý Danh mục Đồng hồ Cao cấp (Luxury Horology Master Data)
     ├── F1.2.1: Quản lý Thông số Kỹ thuật Chuyên ngành (SKU, Brand, Bộ máy, Kính Sapphire, Vỏ, Kháng nước)
     ├── F1.2.2: Thiết lập Đơn vị tính Đa cấp (Thùng - Chiếc) & Tỷ lệ Quy đổi conversionRate
     └── F1.2.3: Thiết lập Ngưỡng cảnh báo Tồn kho An toàn (Min / Max Stock Alert)
```

### 4.2. Bảng Mô tả Module IPO: MOD-01-02 (Khai báo Sản phẩm & Tỷ lệ Quy đổi ĐVT)
| Hạng mục | Nội dung chi tiết |
|:---|:---|
| **Input** | • Dữ liệu đầu vào: Mã SKU, Tên mẫu mã, Hãng, Bộ sưu tập, Loại máy, Chất liệu vỏ, Đường kính (mm), Kháng nước (ATM), Đơn giá sỉ, ĐVT Cơ sở ('Chiếc'), ĐVT Đóng gói ('Thùng'), Hệ số quy đổi (`conversionRate`), Ngưỡng tồn Min/Max, Ảnh mẫu.<br>• Nguồn dữ liệu: Form nhập `AddEditProductActivity`.<br>• Điều kiện tiên quyết: Đăng nhập với quyền `SYSTEM_ADMIN` hoặc `STORE_OWNER`. |
| **Process** | 1. Kiểm tra tính hợp lệ dữ liệu (SKU không trống, không ký tự đặc biệt, Giá sỉ > 0, Tỷ lệ quy đổi >= 1).<br>2. Kiểm tra tính duy nhất của Mã SKU trong Room Database (chặn trùng hoàn toàn).<br>3. Tải ảnh mẫu đồng hồ, nén và lưu trữ cục bộ.<br>4. Tạo `ProductEntity` và gọi hàm DAO `insertProduct()`.<br>5. Ghi nhật ký kiểm toán hệ thống (Audit Log). |
| **Output** | • Bản ghi mẫu đồng hồ mới được lưu thành công vào bảng `products` của Room Database.<br>• Hiển thị SnackBar thông báo thành công.<br>• Danh mục `ProductListFragment` tự động cập nhật qua Flow / LiveData. |
| **Actor** | Chủ cửa hàng (`STORE_OWNER`) và Quản trị viên (`SYSTEM_ADMIN`). |
| **Quyền hạn** | Toàn quyền thêm/sửa đối với Admin và Chủ cửa hàng (các vai trò khác chỉ có quyền Xem). |
| **Luồng dữ liệu liên quan** | Ghi vào bảng `products`, ghi vào bảng `system_audit_logs`, cập nhật StateFlow `ProductViewModel`. |
| **Ràng buộc** | Mã SKU bắt buộc viết hoa; Khi đã có phiếu nhập/xuất thì không được sửa tỷ lệ quy đổi ĐVT. |

---

## 5. LUỒNG DỮ LIỆU LIÊN QUAN ĐẾN ĐỐI TƯỢNG & CHỨC NĂNG

### 5.1. Ma trận CRUD (Đối tượng cốt lõi)
| Đối tượng \ Chức năng | Tạo (C) | Đọc (R) | Cập nhật (U) | Xóa (D) | Ghi chú |
|:---|:---:|:---:|:---:|:---:|:---|
| **User (Tài khoản)** | Admin | Admin, Owner, Cá nhân | Admin (đổi role/khóa), Cá nhân (đổi pass) | Admin (Khóa tài khoản / Soft Delete) | Không xóa cứng để bảo toàn lịch sử giao dịch |
| **Role (Vai trò RBAC)** | Hệ thống | Tất cả các Actor | Admin (cập nhật mô tả) | Cấm xóa | 5 vai trò cố định |
| **Product (Mẫu đồng hồ)** | Admin, Owner | Tất cả các Actor | Admin, Owner, Quản lý kho | Admin, Owner (Ẩn kinh doanh) | Chỉ ngừng kinh doanh khi đã có giao dịch |
| **Brand (Thương hiệu)** | Admin, Owner | Tất cả các Actor | Admin, Owner | Admin (khi chưa có sản phẩm) | Rolex, Patek, Omega, Cartier, Hublot... |
| **UnitOfMeasure (ĐVT)** | Admin, Quản lý kho | Tất cả các Actor | Admin, Quản lý kho | Cấm xóa khi đã có SKU liên kết | 1 Thùng = N Chiếc |

### 5.2. Mô tả Luồng dữ liệu chính:
- **DF-01 (Xác thực Đăng nhập & Cấp quyền phiên):** `Người dùng` $\rightarrow$ `LoginActivity` $\rightarrow$ `SessionManager` (Lưu thông tin vai trò `UserRole`).
- **DF-02 (Khai báo Mẫu đồng hồ & Cấu hình ĐVT):** `Chủ cửa hàng` $\rightarrow$ `AddEditProductActivity` $\rightarrow$ `ProductDao` $\rightarrow$ Ghi vào bảng `products`.
- **DF-03 (Cập nhật Phân quyền Nhân viên):** `Admin` $\rightarrow$ `UserManagementFragment` $\rightarrow$ Cập nhật cột `role` trong bảng `users`.

---

## 6. THIẾT KẾ CƠ SỞ DỮ LIỆU CỐT LÕI (ROOM DATABASE v4)

### 6.1. Danh sách bảng Core do Bình thiết kế
- `users`: Quản lý tài khoản và vai trò người dùng (Khóa chính: `id`).
- `products`: Danh mục đồng hồ xa xỉ và cấu hình quy đổi ĐVT (Khóa chính: `sku`).
- `brands`: Danh bạ thương hiệu chính hãng (Khóa chính: `brand_id`).
- `units_of_measure`: Bảng đơn vị tính và hệ số quy đổi (Khóa chính: `uom_id`).
- `system_audit_logs`: Nhật ký kiểm toán toàn hệ thống (Khóa chính: `log_id`).

### 6.2. Chi tiết thuộc tính bảng `products` (Bảng trung tâm của toàn hệ thống):
| Tên cột | Kiểu dữ liệu | Null | Default | Mô tả | Ràng buộc |
|:---|:---|:---:|:---:|:---|:---|
| `sku` | VARCHAR(50) | No | Không | Mã định danh duy nhất của mẫu đồng hồ | **PRIMARY KEY, Bắt buộc viết hoa** |
| `name` | VARCHAR(255) | No | Không | Tên thương mại đầy đủ | NOT NULL |
| `brand` | VARCHAR(100) | No | Không | Hãng sản xuất (Rolex, Patek, Omega...) | NOT NULL |
| `collection` | VARCHAR(100) | Yes | NULL | Bộ sưu tập (Submariner, Nautilus...) | Có thể để trống |
| `movement_type` | VARCHAR(50) | No | 'AUTOMATIC' | Loại bộ máy cơ học / điện tử | CHECK in ('AUTOMATIC', 'MANUAL', 'QUARTZ', 'SOLAR') |
| `case_material` | VARCHAR(100) | No | 'STAINLESS_STEEL' | Chất liệu vỏ chế tác | CHECK in ('GOLD_18K', 'STEEL', 'TITANIUM', 'PLATINUM') |
| `dial_size_mm` | DOUBLE | No | 40.0 | Đường kính mặt số (mm) | dial_size_mm > 0 |
| `wholesale_price`| DOUBLE | No | 0.0 | Đơn giá bán sỉ niêm yết (VNĐ) | wholesale_price >= 0 |
| `base_unit` | VARCHAR(20) | No | 'Chiếc' | Đơn vị tính cơ sở nhỏ nhất | Mặc định là 'Chiếc' |
| `pack_unit` | VARCHAR(20) | No | 'Thùng' | ĐVT đóng gói bán sỉ | Mặc định là 'Thùng' hoặc 'Hộp' |
| `conversion_rate`| INT | No | 1 | Hệ số quy đổi (1 Thùng = N Chiếc) | **conversion_rate >= 1** |
| `min_stock_alert`| INT | No | 5 | Ngưỡng tồn kho tối thiểu | min_stock_alert >= 0 |
| `max_stock_alert`| INT | No | 100 | Ngưỡng tồn kho tối đa | max_stock_alert >= min_stock_alert |
| `image_uri` | TEXT | Yes | NULL | Đường dẫn ảnh mẫu đồng hồ cục bộ | URI hợp lệ |
| `is_active` | BOOLEAN | No | TRUE | Trạng thái kinh doanh | TRUE: Đang bán, FALSE: Ngừng bán |

### 6.3. Sơ đồ Mối quan hệ Cơ sở dữ liệu Cốt lõi (Core ERD Relationships):
```text
• [brands] 1 ──────────── N [products] (Một hãng có nhiều mẫu đồng hồ)
• [products] 1 ────────── N [serials] (Một mẫu đồng hồ có nhiều mã Serial định danh đích danh 100%)
• [units_of_measure] 1 ── N [products] (Quy định ĐVT Thùng / Chiếc và tỷ lệ quy đổi)
• [roles] 1 ───────────── N [users] (Một vai trò RBAC gán cho nhiều tài khoản người dùng)
• [users] 1 ───────────── N [system_audit_logs] (Một người dùng ghi nhận nhiều nhật ký kiểm toán)
```

---

## 7. CHIA & QUẢN LÝ CÔNG VIỆC THEO NHÓM (VAI TRÒ LEADER)

### 7.1. Phân công 5 vai trò thành viên
1. **Phan Bá Hải Bình (TV1):** Trưởng nhóm / Quản trị hệ thống (`SYSTEM_ADMIN`) — Điều phối toàn bộ dự án, kiến trúc MVVM Core, Room DB v4, phân quyền RBAC 5 Roles, Phân hệ Quản trị Danh mục Luxury Horology, tổng hợp báo cáo.
2. **Nguyễn Đắc Quân (TV2):** Nhân viên Nhập kho (`OPERATIONS_STAFF`) — Lập trình phân hệ Nhà cung cấp, công nợ phải trả, phiếu nhập kho quy đổi ĐVT, tích hợp Camera quét mã Serial và tính giá vốn đích danh.
3. **Tô Đức Thảo (TV3):** Nhân viên Xuất kho (`OPERATIONS_STAFF`) — Lập trình phân hệ Đại lý B2B, hạn mức nợ, khóa giữ chỗ tồn kho (Reservation), xuất kho 2 bước và in hóa đơn B2B.
4. **Võ Công Tâm (TV4):** Thủ kho (`WAREHOUSE_MANAGER`) — Lập trình phân hệ Phân loại tồn kho 3 chất lượng, ma trận kệ tủ chống trộm K1/K2, kiểm kê đối soát tự động và Sổ Thẻ kho điện tử.
5. **Trần Công Tú (TV5):** Kế toán kho (`ACCOUNTANT`) — Lập trình Executive Dashboard KPI thời gian thực, MPAndroidChart doanh thu 6 tháng, hệ thống 9 báo cáo chuyên sâu và báo cáo dòng tiền thuần Cashflow.

### 7.2. Kế hoạch 4 giai đoạn hoàn thành đồ án
- **Giai đoạn 1 (1.5 tuần):** Khảo sát nghiệp vụ, thiết kế Core MVVM, Room DB v4, phân quyền RBAC (Bình chủ trì).
- **Giai đoạn 2 (2.5 tuần):** Phát triển độc lập các phân hệ con trên nhánh Git riêng (Quân, Thảo, Tâm, Tú).
- **Giai đoạn 3 (1.0 tuần):** Ghép nối code (Merge), Kiểm thử chéo liên phân hệ (Cross-testing).
- **Giai đoạn 4 (1.0 tuần):** Hoàn thiện cuốn Báo cáo đồ án tổng thể nộp Khoa & Chuẩn bị kịch bản Vấn đáp.

### 7.3. Bảng theo dõi tiến độ cá nhân của Phan Bá Hải Bình
- `01/10 - 05/10/2026`: Khảo sát bài toán quản lý kho đồng hồ xa xỉ, xác định 4 cơ chế quản trị bắt buộc $\rightarrow$ **100% Hoàn thành**.
- `06/10 - 15/10/2026`: Thiết kế kiến trúc Android MVVM, khởi tạo Room Database v4 và SessionManager $\rightarrow$ **100% Hoàn thành**.
- `16/10 - 25/10/2026`: Lập trình hoàn chỉnh Phân hệ 1 (ProductList, ProductDetail, AddEditProduct, Login, RBAC 5 Roles) $\rightarrow$ **100% Hoàn thành**.
- `26/10 - 05/11/2026`: Soạn thảo Bộ Prompt 5 thành viên, quy chuẩn phân nhánh Git & Hướng dẫn viết Word $\rightarrow$ **100% Hoàn thành**.
- `06/11 - 10/11/2026`: Điền hoàn chỉnh dữ liệu phần việc Trưởng nhóm & Phân hệ 1 vào file Mẫu báo cáo Khoa CNTT $\rightarrow$ **100% Hoàn thành**.

