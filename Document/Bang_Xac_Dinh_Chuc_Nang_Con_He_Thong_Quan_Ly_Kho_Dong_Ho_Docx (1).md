# ĐẶC TẢ YÊU CẦU CHỨC NĂNG HỆ THỐNG QUẢN LÝ KHO HÀNG HÓA CỬA HÀNG ĐỒNG HỒ
Tài liệu đặc tả chi tiết kiến trúc chức năng con, cấu trúc menu, thiết kế giao diện dự kiến và luồng dữ liệu phục vụ công tác thiết kế CSDL (Database Schema) và phát triển phần mềm quản lý kho đồng hồ chuyên nghiệp.
Lưu ý phạm vi nghiệp vụ cốt lõi: Hệ thống là mô hình B2B Wholesale Distribution thuần túy (phân phối bán sỉ cho đại lý, không phục vụ lẻ B2C/POS). Mô hình hoạt động dựa trên 4 cơ chế quản trị bắt buộc: (1) Quản lý định danh Serial/IMEI đích danh 100% sản phẩm đồng hồ từ nhập đến xuất; (2) Quản lý Đơn vị tính đa cấp & Quy cách đóng gói sỉ (Thùng/Kiện/Lô quy đổi chính xác ra Chiếc lẻ); (3) Cơ chế tính Giá vốn Đích danh theo từng mã Serial Number lúc nhập kho (kết hợp Bình quân gia quyền cho phụ kiện); (4) Chu trình Quản lý Công nợ khép kín tích hợp Phiếu Thu - Phiếu Chi thanh toán nợ thực tế.

### Tác nhân nghiệp vụ và vai trò người dùng
Hệ thống chuẩn hóa 5 tác nhân (actor) nội bộ: **Quản trị hệ thống, Chủ cửa hàng, Thủ kho (quản lý điều hành), Nhân viên nhập - xuất kho, Kế toán**. Nhà cung cấp và đại lý B2B là đối tác giao dịch bên ngoài, không phải tài khoản nhân viên.

- **Quản trị hệ thống:** Quản lý tài khoản, vai trò, cấu hình hệ thống và nhật ký Audit Log; không mặc định can thiệp hoặc duyệt nghiệp vụ nhập/xuất hoặc thu/chi.
- **Chủ cửa hàng:** Theo dõi Dashboard/báo cáo điều hành và duyệt ngoại lệ vượt ngưỡng về chi phí, tín dụng hoặc chênh lệch kiểm kê; không trực tiếp quản trị tài khoản hoặc xử lý giao dịch kho thường ngày.
- **Thủ kho (quản lý điều hành):** Chịu trách nhiệm quản lý điều hành toàn diện hoạt động kho, bảo quản an toàn hàng hóa, định vị kệ hàng, kiểm đếm và xác nhận giao nhận vật lý; kiểm kê và cân bằng kho trong thẩm quyền.
- **Nhân viên nhập - xuất kho:** Lập phiếu nhập từ PO, quét nạp Serial, lập đơn bán sỉ nháp, soạn/đóng gói đơn và xử lý xuất kho, bảo hành, đổi trả theo quy trình.
- **Kế toán:** Phân bổ chi phí, theo dõi công nợ NCC/đại lý, lập phiếu thu/chi, đối soát chứng từ và lập báo cáo tài chính.
## Tổng Quan Phân Công Trách Nhiệm
| STT | Thành viên phụ trách | Nhóm chức năng chính | Phạm vi nghiệp vụ |
| --- | --- | --- | --- |
| 1 | Thành viên 1 | Quản lý Hàng hóa & Hệ thống | Danh mục đồng hồ, Thương hiệu, Serial/IMEI, Tài khoản, Phân quyền & Audit Log |
| 2 | Thành viên 2 | Đối tác NCC & Quản lý Nhập hàng | Nhà cung cấp, Xuất trả hàng lỗi, Phiếu nhập kho, Quản lý chi phí nhập |
| 3 | Thành viên 3 | Khách hàng Sỉ & Bán sỉ - Xuất hàng | Đại lý sỉ, Nhận đổi trả sỉ, Đơn bán sỉ, Xuất kho bảo hành/hủy |
| 4 | Thành viên 4 | Tồn kho, Vị trí & Kiểm kê | Theo dõi tồn kho đa trạng thái, Định vị kệ hàng, Kiểm kê & Thẻ kho |
| 5 | Thành viên 5 | Báo cáo & Dashboard Điều hành | Chỉ số KPI, Biểu đồ doanh thu/chi phí, Báo cáo chuyên sâu đa phân hệ |



## Phân Hệ 1: Thành Viên 1 - Quản Lý Hàng Hóa & Quản Trị Hệ Thống
### 1.1 Quản Lý Hàng Hóa (Đồng Hồ, Thương Hiệu, Bộ Sưu Tập)
#### Menu & Giao diện dự kiến
Menu: Quản lý hàng hóa > Danh sách, Thêm mới, Danh mục, Tra cứu Serial.
Giao diện:
Bảng danh sách đồng hồ (Datatable tích hợp bộ lọc nhanh).
Form thêm/sửa đồng hồ (Form nhập liệu đa cột + đính kèm hình ảnh).
Modal quản lý danh mục, thương hiệu, bộ sưu tập.
Màn hình tra cứu vòng đời Serial/IMEI theo mốc thời gian (Timeline View).
#### Danh sách chức năng con (Mức nguyên tử)
Xem danh sách đồng hồ: Hiển thị danh sách sản phẩm hỗ trợ phân trang, sắp xếp linh hoạt theo giá, tên sản phẩm, số lượng tồn kho.
Xem chi tiết thông số kỹ thuật: Hiển thị đầy đủ thông số đồng hồ (Loại máy: Pin/Cơ/Solar, chất liệu kính, chất liệu dây, size mặt, độ chịu nước, thời hạn bảo hành).
Thêm mới đồng hồ: Nhập các trường thông tin cơ bản bao gồm SKU, Barcode, giá vốn, giá sỉ (phân theo cấp bậc đại lý), số lượng đặt sỉ tối thiểu (MOQ - Minimum Order Quantity), hình ảnh, hạn mức min/max tồn kho, cấu hình bật/tắt cờ quản lý theo mã Serial.
Chỉnh sửa thông tin đồng hồ & Cấu hình quy đổi đóng gói sỉ: Cập nhật thuộc tính sản phẩm, cấu hình ĐVT cơ bản (Cái/Chiếc), ĐVT bán sỉ (Thùng/Kiện/Lô), Hệ số quy đổi (ví dụ: 1 Thùng = 20 Chiếc), Phương pháp tính giá vốn Đích danh theo Serial, quy định MOQ và chính sách giá sỉ theo cấp bậc đại lý.
Xóa / Ẩn sản phẩm: Ngừng kinh doanh sản phẩm hoặc xóa tạm thời khỏi danh mục hiển thị.
Quản lý Danh mục / Thương hiệu / Bộ sưu tập: Thêm, sửa, xóa các nhóm danh mục đồng hồ, hãng sản xuất và các bộ sưu tập.
Tìm kiếm & Lọc nâng cao: Tìm kiếm tức thời theo từ khóa, lọc đa tiêu chí (khoảng giá, loại máy, hãng sản xuất).
Tra cứu lịch sử vòng đời Serial (Serial Lookup): Truy vết chi tiết lịch sử mã Serial (Ngày nhập kho, NCC cung cấp, vị trí kệ lưu trữ, đại lý mua, lịch sử bảo hành).
Xuất dữ liệu: Bóc tách và xuất danh sách sản phẩm ra file Excel hoặc PDF.
#### Luồng công việc & Dữ liệu
Luồng công việc: Khai báo Danh mục/Thương hiệu -> Thiết lập ĐVT chuẩn & Quy cách đóng gói sỉ (Thùng/Kiện -> Chiếc) -> Khai báo chi tiết Đồng hồ, Thời gian bảo hành & Cấu hình Giá vốn Đích danh -> Cài đặt Giá sỉ theo cấp đại lý, MOQ & Định mức tồn Kho -> Cung cấp dữ liệu master cho Phân hệ Nhập (TV2) và Phân hệ Xuất bán sỉ (TV3).
Cấu trúc dữ liệu: SKU, Ten_SP, ID_Danhmuc, Hang_SX, Thong_so_KT, Thoi_gian_BH, Co_quan_ly_Serial, DVT_Co_ban, DVT_Si, He_so_quy_doi, Phuong_phap_gia_von, Gia_von_dich_danh, Gia_si_theo_cap, MOQ, Min_ton, Max_ton, Anh.
### 1.2 Quản Trị Hệ Thống (Tài Khoản, Phân Quyền, Nhật Ký)
#### Menu & Giao diện dự kiến
Menu: Hệ thống > Tài khoản, Phân quyền, Đổi mật khẩu, Nhật ký hệ thống.
Giao diện:
Bảng danh sách tài khoản người dùng và trạng thái.
Ma trận phân quyền chi tiết (Role - Permission Matrix).
Form đổi mật khẩu cá nhân.
Bảng truy vết Nhật ký hệ thống (Audit Log Viewer).
#### Danh sách chức năng con (Mức nguyên tử)
Xem danh sách tài khoản: Hiển thị toàn bộ tài khoản người dùng trong hệ thống kèm vai trò và trạng thái hoạt động.
Cấp mới tài khoản: Tạo tài khoản cho nhân viên mới (Email, Username, Mật khẩu mặc định).
Khóa / Kích hoạt tài khoản: Thay đổi trạng thái truy cập của tài khoản nhân viên.
Tạo và cấu hình vai trò (Role): Định nghĩa 5 vai trò nội bộ (Quản trị hệ thống, Chủ cửa hàng, Thủ kho (quản lý điều hành), Nhân viên nhập - xuất kho, Kế toán).
Gán ma trận quyền: Cấu hình chi tiết quyền hạn (Xem, Thêm, Sửa, Xóa, Duyệt phiếu, Xuất báo cáo) theo từng phân hệ.
Đổi mật khẩu cá nhân: Kiểm tra độ mạnh mật khẩu và thực hiện đổi mật khẩu cho người dùng hiện tại.
Quản lý phiên đăng nhập: Đăng xuất an toàn, thu hồi Session / JWT Token từ xa.
Ghi nhận Audit Log: Lưu trữ nhật ký chi tiết lịch sử thao tác hệ thống (Người thực hiện, hành động Tạo/Sửa/Xóa/Duyệt, thời gian, IP).
#### Luồng công việc & Dữ liệu
Luồng công việc: Admin khởi tạo User -> Gán Role & Permissions -> Hệ thống xác thực và phân quyền truy cập thông qua Middleware -> Chặn truy cập không hợp lệ & Ghi vết Audit Log.
Cấu trúc dữ liệu: User_ID, Username, Password_Hash, Role_ID, Permissions, Session_Token, Audit_Log.


## Phân Hệ 2: Thành Viên 2 - Đối Tác Nhà Cung Cấp & Quản Lý Nhập Hàng
### 2.1 Đối Tác Nhà Cung Cấp & Xuất Trả Hàng Lỗi
#### Menu & Giao diện dự kiến
Menu: Đối tác > Nhà cung cấp (Danh sách, Thêm/Sửa, Công nợ, Trả hàng NCC).
Giao diện:
Danh sách thông tin Nhà cung cấp.
Form hồ sơ pháp lý & Cấu hình tài khoản ngân hàng NCC.
Bảng đối soát công nợ phải trả NCC.
Màn hình lập phiếu xuất trả hàng lỗi cho NCC.
#### Danh sách chức năng con (Mức nguyên tử)
Xem danh sách NCC: Tra cứu danh sách NCC, tìm kiếm nhanh theo Tên, Mã số thuế, Số điện thoại.
Quản lý thông tin NCC: Thêm mới và cập nhật thông tin pháp lý, địa chỉ, người đại diện liên hệ.
Cấu hình tài khoản thanh toán: Lưu trữ thông tin tài khoản ngân hàng phục vụ giao dịch chuyển khoản.
Theo dõi công nợ NCC: Quản lý tổng số dư công nợ phải trả và tra cứu lịch sử các đợt giao dịch.
Lập phiếu xuất trả hàng lỗi: Chọn NCC, quét/nhập mã Serial bị lỗi từ kho, ghi nhận chi tiết lý do (lỗi máy, hấp hơi kính, trầy xước vỏ).
Duyệt phiếu trả hàng NCC: Tự động giảm trừ số dư công nợ phải trả NCC và gửi yêu cầu cho Phân hệ Kho (TV4) xuất trừ tồn kho lỗi.
Lập phiếu Chi thanh toán công nợ NCC: Tạo phiếu chi tiền (Ủy nhiệm chi / Chuyển khoản ngân hàng) để thanh toán cho NCC, ghi nhận chi phí/tiền ứng trước, tự động giảm trừ số dư công nợ phải trả NCC.
Quản lý trạng thái hợp tác: Tạm dừng hoặc kích hoạt lại trạng thái giao dịch với Nhà cung cấp.
#### Luồng công việc & Dữ liệu
Luồng công việc: Khởi tạo NCC -> Liên kết NCC vào Phiếu nhập kho -> Duyệt nhập kho ghi nhận Công nợ -> Thực hiện Lập Phiếu Chi thanh toán bớt/dứt điểm công nợ -> Khi phát sinh hàng lỗi NSX -> Lập Phiếu xuất trả NCC -> Giảm trừ nợ & Trừ tồn kho lỗi tương ứng (TV4).
Cấu trúc dữ liệu: Ma_NCC, Ten_NCC, MST, SDT, Dia_chi, STK_Ngan_hang, So_du_no, Phieu_chi_NCC (Ma_phieu_chi, Ma_NCC, Ngay_chi, So_tien, Hinh_thuc_TT, Chung_tu_goc), Phieu_tra_NCC (Ma_phieu, Ma_SP, Danh_sach_Serial_tra, Ly_do, Gia_tri_hoan).
### 2.2 Quản Lý Nhập Hàng & Chi Phí Nhập Kho
#### Menu & Giao diện dự kiến
Menu: Nhập hàng > Tạo phiếu, Danh sách phiếu, Chi phí phát sinh, Phiếu chi thanh toán NCC.
Giao diện:
Màn hình lập phiếu nhập (Tích hợp quét Barcode, nạp danh sách Serial).
Bảng quản lý danh sách phiếu nhập kho (Bộ lọc trạng thái, ngày tháng).
Màn hình xem chi tiết Phiếu nhập & In phiếu A4 / Xuất PDF.
#### Danh sách chức năng con (Mức nguyên tử)
Khởi tạo phiếu nhập: Chọn Nhà cung cấp từ danh bạ hệ thống.
Thêm sản phẩm nhập: Chọn mã đồng hồ bằng cách quét Barcode/SKU hoặc tìm kiếm danh mục.
Nhập số lượng theo ĐVT sỉ & Đơn giá: Khai báo số lượng nhập theo ĐVT sỉ (Thùng/Kiện) hoặc Chiếc lẻ, hệ thống tự động tính tổng số lượng quy đổi ra Chiếc và tính đơn giá vốn nhập kho tương ứng.
Nạp & Quét danh sách Serial theo quy đổi: Quét trực tiếp hoặc nạp file Excel danh sách Serial từ NSX với tổng số lượng mã Serial bắt buộc phải khớp đúng 100% với tổng số lượng Chiếc lẻ sau quy đổi.
Kiểm tra trùng lặp Serial: Tự động đối soát và cảnh báo nếu mã Serial đã tồn tại trên hệ thống.
Tính toán giá trị phiếu: Tự động tính Thành tiền, thuế VAT và phần trăm chiết khấu.
Lưu tạm phiếu nhập: Lưu trữ thông tin ở trạng thái "Nháp" để tiếp tục cập nhật.
Phê duyệt hoàn tất nhập kho: Chốt phiếu nhập, phát sự kiện cộng tồn kho vật lý và lưu danh sách Serial mới vào Phân hệ Kho (TV4).
Hủy phiếu nhập: Cho phép hủy phiếu khi đang ở trạng thái "Nháp".
In ấn & Xuất file: Hỗ trợ in phiếu nhập kho physical A4 hoặc xuất định dạng PDF.
Phân bổ chi phí phát sinh: Ghi nhận và phân bổ chi phí vận chuyển, hải quan, bảo hiểm lô hàng vào trực tiếp giá vốn sản phẩm.
#### Luồng công việc & Dữ liệu
Luồng công việc: Lập Phiếu nhập kho -> Chọn ĐVT sỉ (Thùng/Lô) hoặc Chiếc -> Nhập giá vốn -> Quét dải Serial (kiểm tra đủ số lượng quy đổi) -> Duyệt phiếu nhập -> Tăng tồn kho & Lưu kho Serial kèm Giá vốn Đích danh (TV4) -> Ghi nhận Công nợ/Lập Phiếu Chi NCC & Chuyển dữ liệu Báo cáo (TV5).
Cấu trúc dữ liệu: Ma_PN, Ngay_nhap, Ma_NCC, Chi_tiet_PN (Ma_SP, DVT_Nhap, SL_Nhap, SL_Quy_doi_Chiec, Don_gia_nhap, Danh_sach_Serial), Tong_tien, Chi_phi_phat_sinh.


## Phân Hệ 3: Thành Viên 3 - Bán Sỉ & Phân Phối Đại Lý - Xuất Hàng
### 3.1 Quản Lý Đại Lý Khách Sỉ & Tiếp Nhận Đổi Trả Sỉ
#### Menu & Giao diện dự kiến
Menu: Đối tác > Khách sỉ; Đổi trả hàng sỉ > Tạo phiếu nhận, Danh sách đổi trả; Tài chính sỉ > Lập phiếu thu tiền sỉ.
Giao diện:
Danh mục danh sách Đại lý / Cửa hàng bán sỉ.
Form hồ sơ đại lý & Cấu hình hạn mức tín dụng, chiết khấu.
Bảng đối soát hạn mức công nợ khách sỉ.
Màn hình tiếp nhận & Phân loại hàng sỉ trả lại.
#### Danh sách chức năng con (Mức nguyên tử)
Xem danh sách đại lý: Quản lý danh sách khách sỉ (100% là pháp nhân, cửa hàng, đại lý đối tác B2B) tích hợp phân hạng tự động (VIP, Bạc, Đồng).
Quản lý hồ sơ đại lý: Thêm mới, cập nhật thông tin Pháp nhân/Tên shop, Mã số thuế, Người đại diện, Hợp đồng phân phối B2B, Số điện thoại và Địa chỉ kho/cửa hàng nhận hàng sỉ.
Cấu hình chính sách thương mại: Cài đặt tỷ lệ chiết khấu riêng và hạn mức nợ tối đa cho từng đại lý.
Theo dõi hạn mức nợ: Cập nhật hạn mức nợ sỉ còn lại khả dụng theo hợp đồng cam kết và tra cứu lịch sử mua sỉ.
Lập phiếu nhận hàng sỉ trả lại: Quét kiểm tra mã Serial để xác minh nguồn gốc xuất bán từ hệ thống cho đại lý tương ứng.
Phân loại hàng đổi trả: Phân loại sản phẩm trả về: "Nhập lại kho hàng mới" (Đổi mẫu kinh doanh) hoặc "Chuyển kho lỗi" (Hỏng máy, trầy xước chờ bảo hành).
Duyệt phiếu đổi trả: Tự động cấn trừ công nợ đại lý và gửi thông báo cho Phân hệ Kho (TV4) cập nhật lại trạng thái tồn kho.
Quản lý trạng thái đại lý: Tạm khóa hoặc ngưng hợp tác với đại lý vi phạm chính sách.
Lập phiếu Thu tiền bán sỉ / Thu hồi công nợ đại lý: Tạo phiếu thu tiền (Chuyển khoản / Tiền mặt), ghi nhận tiền cọc hoặc thanh toán công nợ của đại lý, tự động giảm số dư nợ và khôi phục hạn mức công nợ khả dụng cho đại lý.
#### Luồng công việc & Dữ liệu
Luồng công việc: Khai báo Đại lý -> Cài đặt Chiết khấu & Hạn mức nợ -> Nhận thanh toán/Tiền cọc (Lập Phiếu Thu sỉ) -> Tiếp nhận yêu cầu đổi trả -> Quét Serial đối soát nguồn gốc -> Lập phiếu nhận trả -> Cấn trừ công nợ đại lý & Cập nhật tồn kho (TV4).
Cấu trúc dữ liệu: Ma_Dai_ly, Ten_Shop, Chu_shop, SDT, Dia_chi, Hang_dai_ly, Chiet_khau, Han_muc_no, Phieu_thu_si (Ma_phieu_thu, Ma_Dai_ly, Ma_Don_si, So_tien_thu, Hinh_thuc_TT, Ngay_thu), Phieu_tra_si (Ma_phieu, Ma_Dai_ly, Serial_tra, Ly_do, Phan_loai_kho).
### 3.2 Bán Sỉ & Xuất Hàng Đa Năng (Đơn Sỉ, Xuất Sỉ, Xuất Bảo Hành/Hủy)
#### Menu & Giao diện dự kiến
Menu: Bán sỉ / Xuất hàng > Tạo đơn sỉ, Quản lý đơn, Phiếu xuất sỉ, Xuất khác (Bảo hành/Hủy).
Giao diện:
Form tạo đơn sỉ (Tính chiết khấu tự động theo hạng đại lý).
Bảng quản lý đơn hàng sỉ đa trạng thái (Chờ duyệt, Giữ chỗ, Đã xuất, Hủy).
Màn hình đóng gói & Quét xuất Serial thực tế.
Form lập phiếu xuất khác (Xuất bảo hành hãng, Xuất hủy hàng hỏng).
Màn hình In biên bản giao hàng kiêm phiếu xuất kho.
#### Danh sách chức năng con (Mức nguyên tử)
Khởi tạo đơn bán sỉ: Chọn đại lý mua hàng từ danh mục.
Chọn sản phẩm sỉ theo Thùng/Lô hoặc Cái lẻ: Cho phép lên đơn đặt mua sỉ theo Thùng/Kiện hoặc Cái lẻ, hệ thống tự động quy đổi ra Chiếc lẻ và kiểm tra đáp ứng ngưỡng MOQ đã cài đặt.
Kiểm tra tồn kho khả dụng: Tự động tra cứu tồn kho thực tế khả dụng từ Phân hệ Kho (TV4).
Áp giá sỉ & Chiết khấu đại lý: Tự động áp dụng giá bán sỉ chuẩn theo cấp bậc đại lý và tính % chiết khấu thương mại theo hợp đồng B2B.
Thiết lập tiền đặt cọc, hạn thanh toán & Hợp đồng: Nhập số tiền đặt cọc/thanh toán trước (nếu có), thiết lập hạn thanh toán công nợ sỉ và lưu đơn bán sỉ.
Duyệt đơn bán sỉ & Kiểm tra cọc/công nợ: Kiểm tra điều kiện hoàn tất thanh toán cọc và hạn mức nợ còn lại của đại lý trước khi chuyển số lượng sản phẩm sang trạng thái "Giữ chỗ" (Reserved).
Hủy đơn bán sỉ: Giải phóng số lượng sản phẩm "Giữ chỗ" trả lại cho tồn kho khả dụng.
Tạo phiếu xuất kho sỉ: Khởi tạo phiếu xuất kho dựa trên đơn bán sỉ đã duyệt.
Quét Serial xuất kho theo lô/kiện: Quét thực tế từng mã Serial trong lô/kiện hàng đóng gói để xuất giao cho đại lý đối tác.
Xác nhận xuất kho: Trừ tồn kho vật lý và chuyển trạng thái các mã Serial sang "Đã bán" trên Phân hệ Kho (TV4).
Lập phiếu xuất khác: Xuất đồng hồ chuyển đi Trung tâm bảo hành hãng hoặc Xuất hủy hàng vỡ/hỏng không thể phục hồi.
Ghi nhận chi phí giao hàng: Nhập chi phí đóng gói, vận chuyển và đánh dấu bên chịu chi phí.
In chứng từ giao hàng B2B: In phiếu xuất kho kiêm biên bản bàn giao đính kèm danh sách chi tiết các mã Serial xuất và điều khoản hợp đồng giao hàng sỉ.
#### Luồng công việc & Dữ liệu
Luồng công việc: Tạo Đơn sỉ (Nhập số tiền cọc) -> Kiểm tra MOQ & Kho khả dụng (TV4) -> Thu tiền cọc (Lập Phiếu thu) -> Duyệt đơn (Khóa giữ chỗ) -> Quét đóng gói Serial -> Xác nhận xuất kho (Gửi TV4 trừ tồn) -> Ghi nhận công nợ xuất bán & Chuyển số liệu cho Báo cáo (TV5).
Cấu trúc dữ liệu: Ma_Don_si, Ma_Dai_ly, So_tien_coc, Chi_tiet_don (Ma_SP, DVT_Dat, SL_Dat, SL_Quy_doi_Chiec, Gia_si), Danh_sach_Serial_xuat, Ma_Phieu_xuat, Ly_do_xuat (Ban_si/Bao_hanh/Huy), Phi_giao_hang.


## Phân Hệ 4: Thành Viên 4 - Tồn Kho, Vị Trí Kệ & Kiểm Kê
### Menu & Giao diện dự kiến
Menu: Tồn kho > Tình trạng tồn, Quản lý Serial tồn, Vị trí kho, Cảnh báo, Kiểm kê, Thẻ kho.
Giao diện:
Bảng theo dõi tồn kho đa đơn vị (Hiển thị song song số lượng quy đổi Thùng/Kiện và tổng Chiếc lẻ khả dụng) theo vị trí kệ và phân loại chất lượng.
Màn hình truy vấn danh sách mã Serial đang lưu kho.
Màn hình cảnh báo ngưỡng tồn kho (Min/Max Alert).
Màn hình kiểm kê kho (So sánh Số liệu thực tế vs Hệ thống).
Màn hình Thẻ kho (Lịch sử biến động xuất nhập tồn).
### Danh sách chức năng con (Mức nguyên tử)
Theo dõi tồn kho tổng hợp đa đơn vị: Hiển thị chi tiết Số lượng tồn thực tế hiển thị đa đơn vị (ví dụ: 10 Thùng + 5 Chiếc lẻ), Số lượng giữ chỗ (Reserved) và Số lượng khả dụng có thể bán.
Quản lý phân loại kho: Phân chia và quản lý tồn kho theo trạng thái chất lượng: Kho Hàng Mới, Kho Hàng Trưng Bày, Kho Hàng Lỗi chờ xử lý.
Quản lý danh mục Serial tồn: Tra cứu, lọc danh sách chi tiết từng mã Serial đang nằm tại các vị trí trong kho.
Quy đổi giá trị tồn kho theo Giá vốn Đích danh: Tự động tính toán tổng giá trị hàng tồn kho hiện tại bằng cách cộng dồn Giá vốn Đích danh của từng mã Serial cụ thể đang lưu kho.
Quản lý sơ đồ vị trí kho: Định vị sơ đồ lưu trữ vật lý (Mã Dãy, Số Kệ, Tầng, Ngăn chứa hộp đồng hồ).
Cảnh báo hàng sắp hết cho kênh sỉ: Tự động trích xuất danh sách sản phẩm có tồn kho khả dụng &lt;= Min tồn kho sỉ và lập đề xuất nhập bổ sung phục vụ các đơn sỉ lớn.
Cảnh báo hàng hết: Tự động nhận diện sản phẩm có tồn kho bằng 0 và bật cờ tạm ngưng nhận đơn sỉ.
Khởi tạo đợt kiểm kê: Lập phiếu kiểm kê kho định kỳ hoặc đột xuất theo danh mục sản phẩm/vị trí.
Nhập số liệu kiểm đếm: Quét mã Barcode hoặc quét trực tiếp từng mã Serial thực tế tại kệ để kiểm đếm.
Tự động đối soát chênh lệch: So sánh số liệu kiểm đếm thực tế với số liệu hệ thống để tính số lượng thừa/thiếu.
Lập phiếu cân bằng kho: Cập nhật điều chỉnh số liệu tồn kho chuẩn sau khi kiểm kê được duyệt.
Truy xuất Thẻ kho: Nhật ký ghi vết toàn bộ lịch sử biến động Nhập (+), Xuất (-), Trả hàng (+/-), Cân bằng (+/-) kèm mã Serial chi tiết.
Cung cấp API / Cảnh báo: Cung cấp Widget dữ liệu cảnh báo tồn kho real-time hiển thị trên Trung tâm điều hành (TV5).
### Luồng công việc & Dữ liệu
Luồng công việc: Tiếp nhận sự kiện biến động từ Phân hệ Nhập TV2 (+) và Phân hệ Xuất TV3 (-) -> Cập nhật trạng thái và vị trí mã Serial -> Quét kiểm kê thực tế -> Lập phiếu cân bằng lệch kho -> Đẩy số liệu tồn kho và giá trị tài sản kho sang Phân hệ Báo cáo (TV5).
Cấu trúc dữ liệu: Ma_SP, Ma_Serial, Trang_thai_hang (Moi/Trung_bay/Loi), Vi_tri_ke, SL_Thuc_te, SL_Giu_cho, SL_Kha_dung, Phieu_kiem_ke (Ma_phieu, SL_Dem, SL_Lech), The_kho (Ngay, Loai_phieu, Serial_lien_quan, SL).


## Phân Hệ 5: Thành Viên 5 - Báo Cáo & Dashboard Điều Hành
### Menu & Giao diện dự kiến
Menu: Trang chủ (Dashboard, Hoạt động gần đây); Báo cáo > Nhập, Bán sỉ, Xuất, Tồn kho, Đổi trả & Bảo hành, Công nợ & Dòng tiền (Sổ chi tiết công nợ Đại lý/NCC, Báo cáo Thu/Chi).
Giao diện:
Trung tâm điều hành Dashboard (Thẻ KPI Cards, Biểu đồ trực quan Doanh thu/Chi phí).
Widget Hoạt động gần đây (Timeline Log thời gian thực).
Màn hình cấu hình bộ lọc nâng cao và truy xuất báo cáo tổng hợp.
### Danh sách chức năng con (Mức nguyên tử)
Actor chính: Chủ cửa hàng, Quản trị hệ thống, Thủ kho, Nhân viên nhập - xuất kho và Kế toán; quyền xem và xuất báo cáo được giới hạn theo phạm vi công việc của từng vai trò.
Thẻ chỉ số điều hành B2B (KPI Cards): Hiển thị cho Chủ cửa hàng và các cấp quản lý những chỉ số quan trọng real-time: Doanh thu bán sỉ đại lý, Tổng chi phí phân phối, Tổng giá trị tồn kho sỉ, Số đơn hàng sỉ mới, Tỷ lệ đổi trả sỉ từ đại lý.
Biểu đồ phân tích xu hướng phân phối sỉ: Biểu diễn trực quan cho Chủ cửa hàng biểu đồ cột/đường về diễn biến doanh thu bán sỉ theo thời gian và biểu đồ tròn về cơ cấu chi phí vận hành kho sỉ.
Bảng xếp hạng Top sản phẩm bán sỉ: Thống kê danh sách Top mẫu đồng hồ các đại lý nhập nhiều nhất hệ thống (theo số lượng bán sỉ và theo tổng doanh thu phân phối).
Widget Hoạt động gần đây: Giám sát dòng vết thao tác (Audit log) của toàn bộ nhân viên hệ thống theo thời gian thực.
Báo cáo chuyên sâu Nhập hàng: Tổng hợp giá trị nhập kho, số lượng sản phẩm nhập phân theo từng Nhà cung cấp.
Báo cáo chuyên sâu Phân phối Bán sỉ: Phân tích doanh số bán sỉ theo từng Đại lý/Cửa hàng đối tác, hạn mức công nợ sỉ quá hạn và tỷ lệ hủy đơn bán sỉ.
Báo cáo chuyên sâu Xuất hàng: Phân tích cơ cấu xuất kho theo các mục đích (Xuất bán sỉ, Xuất gửi bảo hành hãng, Xuất hủy hàng hỏng).
Báo cáo Đổi trả & Chất lượng: Thống kê tỷ lệ sản phẩm lỗi theo từng Nhà cung cấp và theo từng dòng máy đồng hồ (Pin/Cơ/Solar).
Báo cáo Tồn kho & Luân chuyển: Phân tích tốc độ luân chuyển hàng tồn kho, danh sách hàng tồn lâu ngày (Dead Stock), giá trị tồn kho theo phân loại chất lượng.
Báo cáo Tài chính - Lợi nhuận Bán sỉ: Tổng hợp Doanh thu sỉ, Chi phí phân bổ (vận chuyển, hải quan, đóng gói lô hàng sỉ) và Lợi nhuận gộp từ kênh phân phối B2B.
Báo cáo Sổ chi tiết Công nợ sỉ & NCC: Thống kê chi tiết biến động công nợ theo từng Đại lý sỉ và Nhà cung cấp (Dư nợ đầu kỳ, Phát sinh Nợ xuất/nhập hàng, Phát sinh Có từ Phiếu thu/chi tiền, Dư nợ cuối kỳ).
Báo cáo Dòng tiền Thu/Chi thực tế: Tổng hợp toàn bộ dòng tiền thu thực tế từ bán sỉ/đặt cọc và dòng tiền chi thực tế trả NCC/chi phí vận hành theo mốc thời gian.
Xuất báo cáo đa định dạng: Hỗ trợ Chủ cửa hàng và người dùng được phân quyền trích xuất các mẫu báo cáo ra định dạng file Excel hoặc PDF.
### Luồng công việc & Dữ liệu
Luồng công việc: Thu thập dữ liệu thời gian thực từ TV1 (Sản phẩm), TV2 (Nhập kho, Chi phí, Trả NCC), TV3 (Bán sỉ, Đổi trả sỉ, Xuất khác), TV4 (Tồn kho, Serial, Giá trị kho) -> Tổng hợp dữ liệu, tính toán các chỉ số KPI -> Vẽ biểu đồ & Xuất các chứng từ báo cáo.
Cấu trúc dữ liệu: Khoang_thoi_gian, Doanh_thu_tong, Chi_phi_tong, Loi_nhuan_gop, So_chi_tiet_cong_no_Dai_ly, So_chi_tiet_cong_no_NCC, Bao_cao_dong_tien_Thu_Chi, Top_ban_chay, Gia_tri_ton_kho_dich_danh.
