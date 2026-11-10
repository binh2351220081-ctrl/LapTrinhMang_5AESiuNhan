# BỘ PROMPT CHI TIẾT DÀNH CHO 5 THÀNH VIÊN - DỰ ÁN CHRONOVAULT WMS
> **Hệ thống Quản lý Kho & Phân phối Đồng hồ Cao cấp B2B (Luxury Horology Warehouse Management System)**  
> **Nhóm thực hiện:** 5 AE Siêu Nhân | **Môn học:** Lập Trình Mạng | **Trường:** Đại học Kiến trúc Đà Nẵng (DAU)  
> **Package gốc thống nhất:** `com.example.chronovaultwms`  
> **Database:** Room Database v4 (`com.example.chronovaultwms.core.database.*`)  
> **Architecture:** MVVM (Model - View - ViewModel) + Repository Pattern + Kotlin Coroutines & Flow

---

## MỤC LỤC
1. [Quy chuẩn kỹ thuật chung & Bảng phân công 5 Phân hệ](#1-quy-chuẩn-kỹ-thuật-chung)
2. [Prompt Thành viên 1 (Phan Bá Hải Bình - Nhóm trưởng)](#prompt-thành-viên-1-phan-bá-hải-bình)
3. [Prompt Thành viên 2 (Nguyễn Đắc Quân)](#prompt-thành-viên-2-nguyễn-đắc-quân)
4. [Prompt Thành viên 3 (Tô Đức Thảo)](#prompt-thành-viên-3-tô-đức-thảo)
5. [Prompt Thành viên 4 (Võ Công Tâm)](#prompt-thành-viên-4-võ-công-tâm)
6. [Prompt Thành viên 5 (Trần Công Tú)](#prompt-thành-viên-5-trần-công-tú)
7. [Quy chuẩn Git Workflow & Kịch bản Kiểm thử chéo (Cross-Testing)](#7-quy-chuẩn-git-workflow--kiểm-thử-chéo)

---

## 1. QUY CHUẨN KỸ THUẬT CHUNG

| STT | Thành viên | Vai trò & Nghiệp vụ | Package con | Nhánh Git | Tiền tố XML |
|:---:|:---|:---|:---|:---|:---|
| **TV1** | **Phan Bá Hải Bình** (Leader) | Quản trị Hệ thống, RBAC 5 Roles, Danh mục Sản phẩm Đồng hồ Luxury & ĐVT Thùng/Chiếc | `com.example.chronovaultwms.core` & `product` | `main` / `feature/product` | `fragment_product_...` |
| **TV2** | **Nguyễn Đắc Quân** | Nhà Cung Cấp, Công nợ Phải trả, Nhập kho Quy đổi ĐVT, Quét Serial & Giá vốn Đích danh | `com.example.chronovaultwms.inbound` | `feature/tv2-inbound-supplier` | `fragment_inbound_...` |
| **TV3** | **Tô Đức Thảo** | Đối Tác Đại Lý & Quản Lý Xuất Kho, Kiểm soát Hạn mức Tín dụng, Khóa Giữ chỗ & Quét Serial | `com.example.chronovaultwms.outbound` | `feature/tv3-outbound-dealer` | `fragment_outbound_...` |
| **TV4** | **Võ Công Tâm** | Tồn kho 3 Cấp Chất lượng, Sơ đồ Ngăn kệ K1/K2, Phiếu Kiểm kê Thừa/Thiếu & Sổ Thẻ kho | `com.example.chronovaultwms.inventory` | `feature/tv4-inventory-audit` | `fragment_inventory_...` |
| **TV5** | **Trần Công Tú** | Executive Dashboard KPI thời gian thực, MPAndroidChart Doanh số 6 tháng, 9 Báo cáo Chuyên sâu & Dòng tiền | `com.example.chronovaultwms.dashboard` | `feature/tv5-dashboard-reports` | `fragment_dashboard_...` |

### Bảng 5 Vai trò Tài khoản (UserRole Enum)
```kotlin
enum class UserRole {
    SYSTEM_ADMIN,       // Quản trị viên hệ thống (TV1)
    STORE_OWNER,        // Chủ cửa hàng / Giám đốc điều hành
    WAREHOUSE_MANAGER,  // Quản lý kho tổng
    OPERATIONS_STAFF,   // Nhân viên vận hành kho
    ACCOUNTANT          // Kế toán kho & công nợ
}
```

---

## PROMPT THÀNH VIÊN 1: PHAN BÁ HẢI BÌNH
*Copy toàn bộ phần code dưới đây và dán vào AI (ChatGPT / Claude / DeepSeek / Gemini):*

```text
BẠN LÀ CHUYÊN GIA PHÁT TRIỂN ANDROID SENIOR KIÊM KIẾN TRÚC SƯ HỆ THỐNG (SOFTWARE ARCHITECT). HÃY PHÁT TRIỂN MODULE QUẢN TRỊ DANH MỤC SẢN PHẨM ĐỒNG HỒ CAO CẤP VÀ XÁC THỰC NGƯỜI DÙNG PHÂN QUYỀN (RBAC) BẰNG KOTLIN:

1. KẾ THỪA NỀN TẢNG CORE & CƠ SỞ DỮ LIỆU:
   - Module nằm trong package: `com.example.chronovaultwms.product` và `com.example.chronovaultwms.core`
   - Kế thừa trực tiếp cấu trúc Room Database v4 từ `com.example.chronovaultwms.core.database.*`:
     + ChronoVaultDatabase: Quản lý entities UserEntity, ProductEntity, SerialEntity, TransactionEntity...
     + SessionManager: Lưu trữ phiên đăng nhập, JWT/Token và thông tin vai trò hiện tại (UserRole).
   - Danh sách 5 vai trò (UserRole Enum) chuẩn:
     SYSTEM_ADMIN, STORE_OWNER, WAREHOUSE_MANAGER, OPERATIONS_STAFF, ACCOUNTANT.

2. QUẢN LÝ DANH MỤC ĐỒNG HỒ CAO CẤP (LUXURY HOROLOGY MASTER DATA):
   - Xây dựng ProductListFragment và ProductDetailFragment:
     + Hiển thị danh mục đồng hồ cao cấp sang trọng với bố cục CardView / RecyclerView: Ảnh đồng hồ, Mã SKU, Tên mẫu mã, Thương hiệu (Rolex, Patek Philippe, Audemars Piguet, Omega, Cartier, Hublot...), Bộ sưu tập, Loại máy (Automatic, Quartz, Manual, Spring Drive), Chất liệu vỏ (Vàng 18K, Thép Oystersteel, Titanium, Bạch kim, Ceramic), Đường kính mặt (36mm, 40mm, 41mm...), Mặt kính Sapphire chống trầy, Kháng nước.
     + Quản lý cấu trúc Đơn vị tính (ĐVT) 2 cấp độ bắt buộc: ĐVT Cơ sở ("Chiếc") và ĐVT Đóng gói ("Thùng" / "Hộp"). Lưu tỷ lệ quy đổi `conversionRate` (Ví dụ: 1 Thùng = 10 Chiếc).
     + Thiết lập Cảnh báo mức tồn kho an toàn: `minStockAlert` và `maxStockAlert`. Khi tồn kho khả dụng dưới ngưỡng min, hiển thị cảnh báo màu vàng/đỏ.
     + Hỗ trợ tìm kiếm nhanh theo SKU/Tên, bộ lọc đa tiêu chí (Hãng sản xuất, Khoảng giá niêm yết, Loại máy).
     + Thêm mới / Cập nhật sản phẩm (AddEditProductActivity): Validate dữ liệu nghiêm ngặt, upload ảnh mẫu đồng hồ.

3. XÁC THỰC NGƯỜI DÙNG & KIỂM SOÁT PHÂN QUYỀN (RBAC):
   - Màn hình Đăng nhập (LoginActivity): Nhập Email/Username và Mật khẩu (băm mật khẩu BCrypt / SHA-256 trước khi xác thực).
   - Quản lý Tài khoản & Phân quyền (UserManagementFragment): Dành riêng cho vai trò `SYSTEM_ADMIN` và `STORE_OWNER`:
     + Xem danh sách nhân viên nội bộ, trạng thái kích hoạt (Active / Suspended).
     + Phân quyền tài khoản theo đúng 5 nhóm vai trò `UserRole`.
     + Đổi mật khẩu, khóa tài khoản vi phạm chính sách bảo mật.

YÊU CẦU ĐẦU RA:
- Mã nguồn Kotlin sạch, tuân thủ MVVM (ProductViewModel, ProductRepository, ProductDao).
- Sử dụng Kotlin Coroutines & Flow để xử lý bất đồng bộ.
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_product_...`, `activity_product_...`, `item_product_...`
- Thiết kế giao diện sang trọng chuẩn Luxury Horology: Tông màu Navy Onyx (#1A2332), Trắng viền Gold kim loại (#D4AF37).
```

---

## PROMPT THÀNH VIÊN 2: NGUYỄN ĐẮC QUÂN
*Copy toàn bộ phần code dưới đây và dán vào AI (ChatGPT / Claude / DeepSeek / Gemini):*

```text
BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ NHẬP KHO VÀ NHÀ CUNG CẤP. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.inbound` BẰNG KOTLIN:

1. KẾ THỪA NỀN TẢNG CORE & CƠ SỞ DỮ LIỆU:
   - Kế thừa trực tiếp từ branch `main` của Nhóm trưởng (Phan Bá Hải Bình).
   - Sử dụng các Entity và DAO dùng chung từ `com.example.chronovaultwms.core.database.*`:
     + ProductEntity: Lấy thông tin mã SKU, tên mẫu đồng hồ, đơn vị tính, tỷ lệ quy đổi `conversionRate`.
     + SerialEntity: Bảng quản lý từng chiếc đồng hồ định danh với các trường: `serialNumber` (Khóa chính), `sku`, `status` ("TRONG_KHO", "CHO_XUAT", "DA_BAN", "DA_TRA_NCC", "BAO_HANH"), `quality` ("HANG_MOI", "TRUNG_BAY", "HANG_LOI"), `unitCost` (giá vốn đích danh), `locationBin` (vị trí ngăn kệ).
     + ChronoVaultDatabase: Instance Room Database dùng chung toàn ứng dụng.
   - Sử dụng SessionManager để kiểm tra vai trò người dùng hiện tại (chỉ WAREHOUSE_MANAGER, OPERATIONS_STAFF, ACCOUNTANT được phép thao tác).

2. QUẢN LÝ HỒ SƠ NHÀ CUNG CẤP & CÔNG NỢ PHẢI TRẢ:
   - Danh bạ Nhà Cung Cấp chính hãng (SupplierListFragment): Hiển thị mã NCC, tên công ty đại diện (Ví dụ: Rolex Geneva SA, Swatch Group Vietnam, Richemont...), mã số thuế, hotline, số tài khoản ngân hàng và tổng số dư nợ phải trả.
   - Thêm/Sửa NCC: Kiểm tra tính duy nhất của mã NCC và MST.
   - Theo dõi công nợ NCC: Tự động cộng nợ khi phiếu nhập kho được duyệt; trừ nợ khi lập Phiếu Chi thanh toán.
   - Lập Phiếu Chi thanh toán nợ (PaymentVoucherDialog): Nhập số tiền chi trả, hình thức chuyển khoản/tiền mặt, mã tham chiếu ngân hàng; cập nhật giảm số dư nợ NCC.

3. LẬP PHIẾU NHẬP KHO QUY ĐỔI ĐVT & QUÉT CAMERA SERIAL (INBOUND WORKFLOW):
   - Xây dựng CreateInboundReceiptActivity:
     + Bước 1: Chọn Nhà Cung Cấp và nhập số hóa đơn / Invoice vận chuyển.
     + Bước 2: Chọn mẫu đồng hồ (SKU) và chọn ĐVT nhập là "Thùng" hoặc "Chiếc".
     + Bước 3: Cơ chế quy đổi tự động: Khi người dùng nhập số Thùng, hệ thống lấy `conversionRate` từ ProductEntity để tính ra tổng số chiếc lẻ (Ví dụ: Nhập 3 Thùng -> Yêu cầu nạp đủ 30 mã Serial).
     + Bước 4: Tích hợp Camera Barcode Scanner (Sử dụng Google ML Kit Barcode Scanning hoặc ZXing Embedded): Quét liên tục từng mã Serial in trên hộp/tem đồng hồ. Có âm thanh 'beep' xác nhận mỗi lần quét thành công.
     + Bước 5: Validate dữ liệu:
       * Tổng số mã Serial đã quét phải khớp chính xác 100% với số chiếc quy đổi (không cho duyệt nếu thiếu/thừa).
       * Chặn hoàn toàn và báo lỗi đỏ nếu phát hiện bất kỳ mã Serial nào đã tồn tại trong bảng `serials` của Room DB (chống trùng lặp tuyệt đối).

4. PHÂN BỔ CHI PHÍ & TÍNH TOÁN GIÁ VỐN ĐÍCH DANH (SPECIFIC IDENTIFICATION COSTING):
   - Trong phiếu nhập, kế toán khai báo các chi phí phát sinh thực tế: cước vận chuyển quốc tế, thuế quan hải quan, bảo hiểm lô hàng.
   - Tự động phân bổ đều chi phí vào từng chiếc đồng hồ theo công thức bắt buộc:
     Giá vốn Serial = Đơn giá mua trên HĐ + (Tổng chi phí phân bổ / Tổng số chiếc)
   - Lưu trữ từng Serial vào bảng `serials` với giá vốn đích danh này, gán trạng thái `TRONG_KHO` và chất lượng `HANG_MOI`.
   - Cập nhật tăng tồn kho vật lý tại Room DB, ghi nhận tăng công nợ NCC và sinh bản ghi Sổ Thẻ kho (+) tương ứng.

5. XUẤT TRẢ HÀNG LỖI CHO NCC (SUPPLIER RETURN):
   - Cho phép chọn NCC, quét/chọn các mã Serial từ Kho Hàng Lỗi (`HANG_LOI`), ghi lý do kỹ thuật (hỏng máy, hấp hơi nước, trầy xước từ hãng).
   - Sau khi duyệt: Chuyển Serial sang trạng thái `DA_TRA_NCC`, giảm tồn kho lỗi và tự động cấn trừ số tiền tương ứng vào công nợ phải trả NCC.

YÊU CẦU ĐẦU RA:
- Kết nối chính xác với Room DB của TV1, không tự ý thay đổi cấu trúc bảng Core.
- Mã nguồn Kotlin sạch, tuân thủ MVVM (ViewModel, Repository, Room DAO).
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_inbound_...`, `dialog_inbound_...`, `item_inbound_...`
- Tích hợp mượt mà vào luồng chung của ứng dụng.
```

---

## PROMPT THÀNH VIÊN 3: TÔ ĐỨC THẢO
*Copy toàn bộ phần code dưới đây và dán vào AI (ChatGPT / Claude / DeepSeek / Gemini):*

```text
BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ ĐỐI TÁC ĐẠI LÝ VÀ QUẢN LÝ XUẤT KHO. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.outbound` BẰNG KOTLIN:

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
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_outbound_...`, `dialog_outbound_...`, `item_outbound_...`
```

---

## PROMPT THÀNH VIÊN 4: VÕ CÔNG TÂM

```text
BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ QUẢN LÝ KHO NỘI BỘ, VỊ TRÍ VÀ KIỂM KÊ. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.inventory` BẰNG KOTLIN:

1. KẾ THỪA NỀN TẢNG CORE & CƠ SỞ DỮ LIỆU:
   - Kế thừa trực tiếp từ branch `main` của Nhóm trưởng (Phan Bá Hải Bình).
   - Sử dụng các Entity và DAO dùng chung từ `com.example.chronovaultwms.core.database.*`:
     + ProductEntity, SerialEntity, ChronoVaultDatabase.
   - Sử dụng SessionManager để kiểm tra vai trò người dùng (WAREHOUSE_MANAGER, OPERATIONS_STAFF).

2. PHÂN LOẠI TỒN KHO 3 TRẠNG THÁI CHẤT LƯỢNG (INVENTORY SEGREGATION):
   - Màn hình InventoryStatusFragment: Hiển thị chi tiết tồn kho từng SKU chia thành 3 nhóm trạng thái chất lượng riêng biệt:
     1. Hàng Mới Chuẩn Hãng (`HANG_MOI`): Sẵn sàng cung ứng xuất kho đại lý.
     2. Hàng Trưng Bày Boutique (`TRUNG_BAY`): Đồng hồ để tại tủ kính cho khách VIP xem mẫu, không được tự động xuất kho đại lý.
     3. Kho Hàng Lỗi / Chờ Xử Lý (`HANG_LOI`): Đồng hồ trầy xước, chạy sai giờ, hấp hơi nước chờ gửi trả hãng hoặc gửi đi bảo hành nước ngoài.
   - Chức năng Chuyển đổi trạng thái chất lượng (ChangeQualityDialog): Cho phép chọn mã Serial, chuyển trạng thái kèm nhập lý do kỹ thuật (Ví dụ: Chuyển từ HÀNG MỚI sang HÀNG LỖI vì xước vành bezel).

3. SƠ ĐỒ KỆ HÀNG TRỰC QUAN (BIN LOCATION MATRIX):
   - Xây dựng LocationMatrixFragment:
     + Trực quan hóa mặt bằng kho đồng hồ: Hệ thống tủ sắt chống trộm 2 khu vực: Kệ K1 (Dòng Thể thao Rolex, AP) và Kệ K2 (Dòng Dress Watch Patek, Cartier).
     + Mỗi kệ chia thành các ngăn Bin chuẩn: K1-A01, K1-A02, K1-B01...
     + Hiển thị trạng thái ô kệ bằng màu sắc trực quan:
       * Ô màu xanh lá: Kệ còn trống chỗ.
       * Ô màu vàng: Kệ đang chứa hàng (hiển thị số lượng chiếc và SKU đang lưu giữ).
       * Ô màu đỏ: Kệ đã đầy định mức an toàn.
     + Khi bấm vào một ô Bin: Hiển thị danh sách chính xác các mã Serial đang nằm trên ngăn kệ đó.
   - Chức năng Điều chuyển vị trí ngăn kệ (RelocateBinDialog): Quét mã Serial và quét mã Barcode dán trên ngăn kệ mới để cập nhật `locationBin` trong cơ sở dữ liệu.

4. QUY TRÌNH KIỂM KÊ KHO THỰC TẾ & XỬ LÝ LỆCH KHO (STOCK AUDIT WORKFLOW):
   - Xây dựng StockAuditActivity:
     + Bước 1: Tạo đợt kiểm kê (Theo kệ Bin hoặc theo Danh mục Thương hiệu).
     + Bước 2: Hệ thống khóa sổ tạm thời danh mục kiểm kê.
     + Bước 3: Nhân viên dùng Camera điện thoại quét liên tục toàn bộ mã Serial thực tế có trên kệ.
     + Bước 4: Tự động đối soát thời gian thực:
       * Danh sách Khớp đúng: Serial có trong sổ sách và đã quét thấy.
       * Danh sách Thừa kho (Surplus): Quét thấy Serial nhưng trên hệ thống không ghi nhận ở vị trí này.
       * Danh sách Thiếu kho (Deficit): Sổ sách có nhưng quét không thấy (nghi ngờ thất thoát).
     + Bước 5: Lập Biên bản xử lý chênh lệch kiểm kê (AuditAdjustmentDialog): Nhập nguyên nhân, bắt buộc có chữ ký xác nhận của Quản lý kho; tự động điều chỉnh số liệu tồn kho và ghi nhật ký kiểm toán Audit Log.

5. SỔ THẺ KHO ĐIỆN TỬ (STOCK CARD LEDGER):
   - Màn hình StockCardFragment: Tra cứu lịch sử biến động tồn kho của bất kỳ mẫu SKU hoặc tra cứu hành trình luân chuyển của 1 mã Serial duy nhất (từ lúc nhập kho -> đổi kệ -> xuất kho đại lý -> hoặc trả hàng). Hiển thị rõ: Ngày giờ, Loại nghiệp vụ (Nhập/Xuất/Kiểm kê), Mã chứng từ, Số lượng biến động (+/-), Tồn cuối kỳ, Nhân viên thực hiện.

YÊU CẦU ĐẦU RA:
- Mã nguồn Kotlin sạch, chuẩn MVVM, kết nối mượt mà với Room DB của TV1.
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_inventory_...`, `dialog_inventory_...`, `item_inventory_...`
```

---

## PROMPT THÀNH VIÊN 5: TRẦN CÔNG TÚ
*Copy toàn bộ phần code dưới đây và dán vào AI (ChatGPT / Claude / DeepSeek / Gemini):*

```text
BẠN LÀ LẬP TRÌNH VIÊN ANDROID CHUYÊN TRÁCH PHÂN HỆ BÁO CÁO VÀ DASHBOARD ĐIỀU HÀNH. HÃY PHÁT TRIỂN MODULE TRONG PACKAGE `com.example.chronovaultwms.dashboard` BẰNG KOTLIN:

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
- Đặt tên file giao diện XML bắt buộc dùng tiền tố: `fragment_dashboard_...`, `item_dashboard_...`
```

---

## 7. QUY CHUẨN GIT WORKFLOW & KIỂM THỬ CHÉO

### A. Phân nhánh Git
1. **TV1 (Bình):** Giữ nhánh `main`, tích hợp và review code của 4 thành viên.
2. **TV2 (Quân):** Nhánh `feature/tv2-inbound-supplier`
3. **TV3 (Thảo):** Nhánh `feature/tv3-outbound-dealer`
4. **TV4 (Tâm):** Nhánh `feature/tv4-inventory-audit`
5. **TV5 (Tú):** Nhánh `feature/tv5-dashboard-reports`

### B. Kịch bản Kiểm thử Tích hợp Liên phân hệ (Cross-Testing Checklist)
- **Test Case 1 (TV1 & TV2):** TV1 tạo sản phẩm SKU `RLX-SUB-01` (1 Thùng = 10 Chiếc). TV2 tạo phiếu nhập 2 Thùng -> Kiểm tra hệ thống yêu cầu quét đủ 20 Serial và tính giá vốn đích danh.
- **Test Case 2 (TV2 & TV4):** TV2 duyệt phiếu nhập -> Kiểm tra TV4 thấy tồn kho tăng, các Serial xuất hiện trên kệ và có dòng phát sinh trong Sổ Thẻ kho (+).
- **Test Case 3 (TV3 & TV4):** TV3 lập lệnh xuất kho đại lý 5 chiếc -> Kiểm tra TV4 thấy tồn giữ chỗ tăng 5, tồn khả dụng giảm 5. TV3 quét xuất kho -> Tồn thực tế giảm 5, Serial chuyển `DA_BAN`.
- **Test Case 4 (TV2, TV3 & TV5):** TV2 lập phiếu chi trả NCC, TV3 lập phiếu thu đại lý -> Kiểm tra TV5 thấy Dashboard cập nhật dòng tiền và Sổ chi tiết công nợ 2 chiều chính xác.

