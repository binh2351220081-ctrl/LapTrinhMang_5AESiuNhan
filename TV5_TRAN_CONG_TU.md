# Phân hệ TV5 — Trần Công Tú

Phân hệ `dashboard/` đã được tích hợp vào mã nguồn `main` của nhóm và tuân thủ quy ước đặt tên `fragment_dashboard_*`, `item_dashboard_*`.

## Chức năng hoàn thành

- Dashboard KPI: giá trị tồn theo giá vốn đích danh, doanh thu sỉ, số đơn sỉ, tồn khả dụng, tỷ lệ đổi trả.
- Biểu đồ doanh thu 6 tháng và cơ cấu chi phí bằng View Android thuần, không phụ thuộc thư viện biểu đồ ngoài.
- Top sản phẩm và nhật ký hoạt động liên phân hệ.
- 9 báo cáo: nhập hàng, xuất sỉ, cơ cấu xuất; chất lượng/đổi trả theo hãng và dòng máy; dead stock trên 90/180 ngày; lợi nhuận gộp B2B; công nợ đại lý/NCC đủ dư đầu kỳ, phát sinh Nợ/Có và dư cuối kỳ; dòng tiền; audit log.
- Lọc khoảng ngày, xuất CSV vào Downloads trên Android 10+ (thư mục ứng dụng trên Android 8–9), in A4 qua Android Print Manager.
- Nút `Danh mục TV1` để kiểm tra luồng tích hợp với phân hệ sản phẩm.

## Đồng bộ dữ liệu

`RoomDashboardRepository` chỉ đọc `ProductDao`, `SerialDao`, `AuditLogDao` và gọi bộ seed dùng chung khi cơ sở dữ liệu trống. TV5 không thay đổi Entity, DAO hoặc schema của các thành viên khác. Khi TV2–TV4 bổ sung bảng riêng, chỉ cần thay projection đọc trong repository; giao diện và báo cáo không phải sửa.

## Chạy dự án

1. Mở thư mục `android/` bằng Android Studio.
2. Chờ Gradle Sync hoàn tất.
3. Chạy cấu hình `app` trên thiết bị Android API 26 trở lên.

Tài khoản demo theo tài liệu nhóm: `tu_accountant` / `123` — vai trò `ACCOUNTANT`.

## Kiểm thử đã chạy

- `:app:assembleDebug`
- `:app:testDebugUnitTest`
- `:app:lintDebug`
- Smoke test trên máy ảo Pixel 7: khởi động Dashboard và đọc dữ liệu Room thành công.
