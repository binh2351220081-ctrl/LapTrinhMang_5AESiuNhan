# HƯỚNG DẪN VIẾT BÁO CÁO WORD & CHUẨN BỊ VẤN ĐÁP CHO TỪNG THÀNH VIÊN
> **Dự án:** ChronoVault WMS - Hệ thống Quản lý Kho & Phân phối Đồng hồ Cao cấp B2B  
> **Nhóm thực hiện:** 5 AE Siêu Nhân | **Môn học:** Lập Trình Mạng | **Đại học Kiến trúc Đà Nẵng (DAU)**  
> **Nhóm trưởng phụ trách tổng hợp:** Phan Bá Hải Bình

---

## 📌 QUY ĐỊNH CHUNG DÀNH CHO CẢ 4 THÀNH VIÊN (QUÂN, THẢO, TÂM, TÚ)

1. **Hình thức nộp cho Nhóm trưởng (Bình):**
   - Mỗi bạn soạn **01 file Word riêng** (dung lượng khoảng **4 – 7 trang A4**, font Arial hoặc Times New Roman 12pt, cách dòng 1.15).
   - Đặt tên file theo đúng cú pháp: `BaoCao_[MaTV]_[HoTen]_[TenPhanHe].docx`  
     *Ví dụ: `BaoCao_TV2_NguyenDacQuan_NhapKho_NCC.docx`*
   - Gửi file Word hoàn chỉnh kèm thư mục ảnh chụp màn hình (ảnh rõ nét) cho Nhóm trưởng trước ngày nộp bài chính thức ít nhất **3 ngày** để Bình ráp thành cuốn Báo cáo Đồ án hoàn chỉnh nộp Khoa.

2. **Cấu trúc bắt buộc của mỗi file Word cá nhân (gồm đúng 5 phần):**
   - **Phần 1:** Giới thiệu phạm vi nghiệp vụ và danh sách chức năng phân hệ mình phụ trách.
   - **Phần 2:** Chụp ảnh màn hình giao diện thực tế (Screenshots) và chú thích chi tiết từng nút bấm, trường dữ liệu.
   - **Phần 3:** Sơ đồ Ca sử dụng (Use Case Diagram) & Sơ đồ Tuần tự (Sequence Diagram) mô tả luồng dữ liệu.
   - **Phần 4:** Bảng Kịch bản Kiểm thử (Test Cases) kèm dữ liệu mẫu thực tế.
   - **Phần 5:** Bộ câu hỏi Vấn đáp trọng tâm của Giảng viên & Gợi ý câu trả lời.

---

# PHẦN 1: HƯỚNG DẪN DÀNH CHO THÀNH VIÊN 2 (NGUYỄN ĐẮC QUÂN)
> **Phân hệ phụ trách:** Quản lý Đối tác Nhà Cung Cấp, Nhập Kho Quy đổi ĐVT, Quét Serial & Giá vốn Đích danh  
> **Package phụ trách:** `com.example.chronovaultwms.inbound` | **Nhánh Git:** `feature/tv2-inbound-supplier`

### 1. Khung nội dung Word bạn cần viết:
- **Tiêu đề chương trong Word:** `CHƯƠNG: PHÂN HỆ QUẢN LÝ NHÀ CUNG CẤP & NHẬP KHO ĐỒNG HỒ ĐÍCH DANH (TV2: NGUYỄN ĐẮC QUÂN)`
- **Nội dung 1 - Hồ sơ Nhà Cung Cấp & Công nợ:**
  - Mô tả cách quản lý danh bạ NCC chính hãng (Rolex Geneva SA, Swatch Group Vietnam, Richemont International...).
  - Giải thích cơ chế tự động ghi tăng nợ khi phiếu nhập được duyệt; ghi giảm nợ khi lập Phiếu Chi thanh toán qua ngân hàng/tiền mặt.
- **Nội dung 2 - Quy trình Nhập kho quy đổi ĐVT & Quét Camera Serial:**
  - Giải thích bài toán: Đồng hồ nhập về theo "Thùng" (Carton) hoặc "Hộp", nhưng bán ra và bảo hành theo từng "Chiếc" (Piece) định danh.
  - Nêu thuật toán tự động nhân tỷ lệ quy đổi (`conversionRate`): Ví dụ nhập 2 Thùng -> Bắt buộc hệ thống mở Camera quét nạp đúng 20 mã Serial.
  - Trình bày công nghệ quét Camera Barcode (Google ML Kit / ZXing) và cơ chế chặn trùng mã Serial trong Room DB.
- **Nội dung 3 - Phương pháp Giá vốn Đích danh (Specific Identification Costing):**
  - Trình bày sự khác biệt giữa giá vốn đích danh với bình quân gia quyền.
  - Nêu rõ công thức phân bổ chi phí phát sinh thực tế (phí vận chuyển quốc tế, thuế quan, bảo hiểm) vào từng chiếc:
    $$\text{Giá vốn đích danh Serial} = \text{Đơn giá mua HĐ} + \frac{\text{Tổng chi phí phân bổ}}{\text{Tổng số chiếc}}$$
- **Nội dung 4 - Xuất trả hàng lỗi cho NCC (Supplier Return):**
  - Trình bày cách chọn Serial từ kho hàng lỗi (`HANG_LOI`), xuất trả hãng và cấn trừ công nợ phải trả.

### 2. Sơ đồ cần vẽ và chèn vào Word:
- **Sơ đồ Use Case:** Các ca sử dụng: *Quản lý NCC, Lập Phiếu nhập kho, Quét Serial Camera, Khai báo phân bổ chi phí, Lập Phiếu Chi nợ NCC, Xuất trả hàng lỗi*.
- **Sơ đồ Tuần tự (Sequence Diagram):** Luồng xử lý khi bấm nút "Lưu Phiếu Nhập": *App -> Camera quét mã -> InboundViewModel -> SerialDao (Check trùng) -> Tính giá vốn -> Lưu Room DB -> Cập nhật nợ NCC*.

### 3. Bảng Dữ liệu Mẫu (Test Data) cần đưa vào báo cáo:
- **Nhà cung cấp:** Rolex Geneva SA (Mã: `NCC-RLX-01`, MST: `CHE-101.324.567`, Số nợ: `0 VNĐ`).
- **Lô nhập kho:** SKU `RLX-SUB-01` (Rolex Submariner Date).
  - Số lượng: 2 Thùng (Quy đổi: 20 chiếc).
  - Đơn giá mua: 200,000,000 VNĐ/chiếc (Tổng: 4,000,000,000 VNĐ).
  - Chi phí logistics + bảo hiểm: 40,000,000 VNĐ (Phân bổ: 2,000,000 VNĐ/chiếc).
  - Giá vốn đích danh mỗi Serial nhập kho: 202,000,000 VNĐ/chiếc.
  - Dải Serial quét: `RLX24001` đến `RLX24020`.

### 4. Câu hỏi Vấn đáp Giảng viên hay hỏi & Cách trả lời:
- **Câu 1:** *"Tại sao đồng hồ cao cấp bắt buộc phải quản lý theo từng Serial mà không nhập theo số lượng tổng?"*  
  👉 **Trả lời:** *"Thưa thầy/cô, đồng hồ xa xỉ là tài sản có giá trị rất cao. Mỗi chiếc có một mã Serial duy nhất do hãng khắc laser để kiểm tra nguồn gốc, phân loại bảo hành toàn cầu và chống hàng giả. Bắt buộc phải quản lý đích danh 100% để đảm bảo tính pháp lý và giá vốn chính xác."*
- **Câu 2:** *"Nếu em quét trùng 1 mã Serial đã có trong kho thì hệ thống xử lý ra sao?"*  
  👉 **Trả lời:** *"Trong Room Database, trường `serialNumber` là khóa chính (Primary Key). Khi Camera nhận diện mã, ViewModel gọi hàm `serialDao.isSerialExists(serialNumber)`. Nếu mã đã tồn tại, ứng dụng sẽ phát âm thanh cảnh báo lỗi, viền đỏ ô quét và chặn hoàn toàn không cho thêm vào phiếu nhập."*

---

# PHẦN 2: HƯỚNG DẪN DÀNH CHO THÀNH VIÊN 3 (TÔ ĐỨC THẢO)
> **Phân hệ phụ trách:** Đối Tác Đại Lý & Quản Lý Xuất Kho, Kiểm soát Hạn mức Tín dụng, Lệnh Xuất Kho, Cơ chế Giữ chỗ & Quét Serial Xuất kho  
> **Package phụ trách:** `com.example.chronovaultwms.outbound` | **Nhánh Git:** `feature/tv3-outbound-dealer`

### 1. Khung nội dung Word bạn cần viết:
- **Tiêu đề chương trong Word:** `CHƯƠNG: PHÂN HỆ ĐỐI TÁC ĐẠI LÝ & QUẢN LÝ XUẤT KHO (TV3: TÔ ĐỨC THẢO)`
- **Nội dung 1 - Quản lý Đại lý Tiếp Nhận B2B & Hạn mức Tín dụng (Credit Limit):**
  - Mô tả danh mục đại lý tiếp nhận (Hải Triều, Galle Watch, Boss Luxury...), phân hạng (VIP Kim Cương, Vàng, Bạc, Đồng), tỷ lệ chiết khấu thương mại (15% – 30%).
  - Giải thích giải thuật khóa tự động (Credit Limit Enforcement): Khi tạo lệnh xuất hàng mới, nếu $(\text{Dư nợ hiện tại} + \text{Giá trị lô hàng xuất}) > \text{Hạn mức nợ}$ thì hệ thống chặn không cho lưu đơn, hiện cảnh báo đỏ.
  - Mô tả chức năng Lập Phiếu Thu đối soát công nợ đại lý để giảm dư nợ.
- **Nội dung 2 - Quy trình Tạo Lệnh Xuất Hàng Đại Lý & Cơ chế Khóa Giữ Chỗ (Inventory Reservation):**
  - Giải thích bài toán: Tránh tình trạng tranh chấp tồn kho giữa các nhân viên điều phối xuất hàng.
  - Công thức: $\text{Tồn khả dụng} = \text{Tổng tồn vật lý} - \text{Tồn đang giữ chỗ}$.
  - Khi đơn hàng ở trạng thái tiếp nhận (Pending), hệ thống tự động tăng `reservedQuantity` để các lệnh xuất sau không thể lấy trùng.
- **Nội dung 3 - Quy trình Xuất kho 2 bước (Picking & Dispatch):**
  - Bước 1 (Picking List): Gợi ý danh sách Serial cụ thể trong kho theo vị trí ngăn kệ.
  - Bước 2 (Quét Camera Serial Dispatch): Nhân viên xuất kho cầm điện thoại quét từng mã Serial trên hộp trước khi đóng thùng bàn giao vận chuyển. Kiểm tra chéo thời gian thực (không cho quét hàng trưng bày hoặc hàng lỗi).
- **Nội dung 4 - Cập nhật Công nợ & In Phiếu Xuất kho B2B:**
  - Chuyển trạng thái Serial sang `DA_BAN`, ghi giảm tồn vật lý, giải phóng tồn giữ chỗ, ghi tăng công nợ phải thu của đại lý và sinh dòng Sổ Thẻ kho (-).

### 2. Sơ đồ cần vẽ và chèn vào Word:
- **Sơ đồ Use Case:** *Quản lý hồ sơ đại lý, Kiểm tra hạn mức tín dụng, Tạo lệnh xuất kho B2B, Khóa giữ chỗ tồn kho, Quét Serial xuất kho, Lập Phiếu Thu nợ đại lý*.
- **Sơ đồ Tuần tự (Sequence Diagram):** Luồng Tạo lệnh xuất và Xuất bến: *Tạo lệnh xuất -> Check Hạn mức tín dụng -> Tăng tồn giữ chỗ -> Quét Serial -> Check trạng thái Serial -> Chuyển DA_BAN -> Tăng nợ đại lý*.

### 3. Bảng Dữ liệu Mẫu (Test Data) cần đưa vào báo cáo:
- **Đại lý:** Chuỗi Đồng hồ Galle Watch (Hạng VIP, Chiết khấu 25%, Hạn mức nợ: 3,000,000,000 VNĐ, Dư nợ hiện tại: 1,800,000,000 VNĐ).
- **Đơn hàng sỉ mẫu:** Đặt mua 5 chiếc Rolex Submariner (Giá niêm yết: 350,000,000 VNĐ/chiếc).
  - Tổng tiền trước CK: 1,750,000,000 VNĐ.
  - Chiết khấu VIP 25%: -437,500,000 VNĐ.
  - Giá trị đơn hàng sau CK: 1,312,500,000 VNĐ.
  - Kiểm tra hạn mức: $1,800,000,000 + 1,312,500,000 = 3,112,500,000 > 3,000,000,000 \rightarrow$ **Hệ thống cảnh báo đỏ vượt hạn mức nợ**.

### 4. Câu hỏi Vấn đáp Giảng viên hay hỏi & Cách trả lời:
- **Câu 1:** *"Cơ chế giữ chỗ tồn kho (Reservation) hoạt động thế nào và nếu không có nó thì gặp lỗi gì?"*  
  👉 **Trả lời:** *"Thưa thầy/cô, nếu không có cơ chế giữ chỗ, khi kho chỉ còn 3 chiếc đồng hồ mà cùng lúc 2 nhân viên tạo 2 đơn hàng 3 chiếc, cả 2 đơn đều duyệt thành công dẫn đến bán âm kho và không có hàng giao. Cơ chế Reservation khi đơn 1 được tạo sẽ lập tức tăng `reservedQuantity = 3`, khiến Tồn khả dụng về 0, đơn 2 sẽ bị từ chối ngay lập tức."*
- **Câu 2:** *"Làm sao đảm bảo thủ kho không xuất nhầm chiếc đồng hồ đang bị lỗi kỹ thuật cho đại lý?"*  
  👉 **Trả lời:** *"Trong quá trình quét xuất kho bằng Camera, ứng dụng truy vấn trường `quality` của Serial đó. Nếu `quality != 'HANG_MOI'` (ví dụ là `HANG_LOI` hoặc `TRUNG_BAY`), máy sẽ rung cảnh báo, báo lỗi đỏ và từ chối xác nhận xuất chiếc đó."*

---

# PHẦN 3: HƯỚNG DẪN DÀNH CHO THÀNH VIÊN 4 (VÕ CÔNG TÂM)
> **Phân hệ phụ trách:** Quản lý Tồn Kho Nội Bộ, Phân loại 3 Chất lượng, Sơ đồ Ngăn kệ Bin, Kiểm kê Thực tế & Sổ Thẻ kho  
> **Package phụ trách:** `com.example.chronovaultwms.inventory` | **Nhánh Git:** `feature/tv4-inventory-audit`

### 1. Khung nội dung Word bạn cần viết:
- **Tiêu đề chương trong Word:** `CHƯƠNG: PHÂN HỆ QUẢN LÝ TỒN KHO NỘI BỘ, SƠ ĐỒ KỆ & KIỂM KÊ (TV4: VÕ CÔNG TÂM)`
- **Nội dung 1 - Phân loại Tồn kho theo 3 Trạng thái Chất lượng:**
  - Trình bày sự cần thiết của việc tách biệt: Hàng Mới chuẩn hãng (`HANG_MOI`), Hàng Trưng bày Boutique (`TRUNG_BAY`), và Kho Hàng Lỗi (`HANG_LOI`).
  - Chức năng Chuyển đổi trạng thái chất lượng kèm lý do kỹ thuật (ví dụ: phát hiện xước viền bezel chuyển từ Mới sang Lỗi).
- **Nội dung 2 - Sơ đồ Ma trận Vị trí Kệ hàng (Bin Location Matrix):**
  - Mô tả cách thức phân khu tủ sắt chống trộm: Kệ K1 (Dòng Thể thao), Kệ K2 (Dòng Classic).
  - Trực quan hóa các ô Bin: K1-A01, K1-A02... bằng màu sắc (Trống: Xanh, Đang chứa: Vàng, Đầy: Đỏ).
  - Bấm vào một ô Bin xem danh sách Serial đang lưu trữ; chức năng quét mã vạch điều chuyển ô kệ.
- **Nội dung 3 - Quy trình Kiểm kê Kho thực tế & Đối soát Thừa / Thiếu:**
  - Quy trình 5 bước: Tạo đợt kiểm kê -> Khóa sổ tạm thời -> Quét camera Serial thực tế -> Thuật toán đối soát tự động (Khớp đúng / Thừa kho / Thiếu kho) -> Lập Biên bản xử lý chênh lệch có chữ ký phê duyệt.
- **Nội dung 4 - Sổ Thẻ kho Điện tử (Stock Card Ledger):**
  - Tra cứu lịch sử luân chuyển của bất kỳ mẫu SKU hoặc 1 mã Serial duy nhất từ lúc nhập đến lúc xuất; ghi nhận đầy đủ Ngày giờ, Chứng từ, Biến động (+/-), Tồn cuối kỳ, Nhân viên thực hiện.

### 2. Sơ đồ cần vẽ và chèn vào Word:
- **Sơ đồ Use Case:** *Xem tồn kho 3 chất lượng, Chuyển trạng thái chất lượng, Quản lý sơ đồ kệ Bin, Điều chuyển ngăn kệ, Tạo đợt kiểm kê, Quét Serial kiểm kê, Xử lý chênh lệch, Tra cứu Sổ thẻ kho*.
- **Sơ đồ Tuần tự (Sequence Diagram):** Luồng Kiểm kê đối soát: *Tạo đợt kiểm kê -> Quét danh sách Serial thực tế -> Đối chiếu danh sách Serial sổ sách trong Room DB -> Phân loại Khớp/Thừa/Thiếu -> Cập nhật biên bản*.

### 3. Bảng Dữ liệu Mẫu (Test Data) cần đưa vào báo cáo:
- **Sơ đồ kệ:** Kệ K1-A01 (chứa 5 chiếc Rolex), K1-A02 (chứa 3 chiếc Omega), K2-B01 (Kho hàng lỗi kỹ thuật - chứa 2 chiếc).
- **Biên bản kiểm kê mẫu:** Đợt kiểm kê Kệ K1-A01:
  - Sổ sách ghi nhận: 5 mã Serial (`RLX01` đến `RLX05`).
  - Thực tế quét được: 5 mã (`RLX01`, `RLX02`, `RLX03`, `RLX04`, `RLX99`).
  - Kết quả đối soát tự động: Khớp: 4 chiếc (`RLX01`-`04`); Thiếu: 1 chiếc (`RLX05`); Thừa: 1 chiếc (`RLX99` - nằm nhầm kệ từ K1-A02 sang).

### 4. Câu hỏi Vấn đáp Giảng viên hay hỏi & Cách trả lời:
- **Câu 1:** *"Khi kiểm kê phát hiện thiếu 1 chiếc đồng hồ thì hệ thống xử lý ra sao?"*  
  👉 **Trả lời:** *"Hệ thống đưa Serial đó vào danh sách 'Thiếu kho' (Deficit). Để đảm bảo tính minh bạch kế toán, hệ thống không tự ý xóa mà yêu cầu lập 'Biên bản xử lý chênh lệch kiểm kê', nhập nguyên nhân giải trình và bắt buộc có xác nhận của Quản lý kho trước khi cập nhật điều chỉnh tồn kho và ghi Audit Log."*
- **Câu 2:** *"Sổ Thẻ kho điện tử khác gì với bảng danh sách tồn kho thông thường?"*  
  👉 **Trả lời:** *"Bảng tồn kho chỉ cho biết hiện tại trong kho có bao nhiêu chiếc. Còn Sổ Thẻ kho là sổ nhật ký kế toán ghi lại từng dòng biến động (+/-) theo trục thời gian kèm mã chứng từ gốc (Phiếu nhập, Phiếu xuất, Phiếu kiểm kê), đảm bảo truy vết được 100% đường đi của từng chiếc đồng hồ."*

---

# PHẦN 4: HƯỚNG DẪN DÀNH CHO THÀNH VIÊN 5 (TRẦN CÔNG TÚ)
> **Phân hệ phụ trách:** Executive Dashboard KPI thời gian thực, MPAndroidChart Doanh số 6 tháng, 9 Báo cáo Chuyên sâu & Dòng tiền  
> **Package phụ trách:** `com.example.chronovaultwms.dashboard` | **Nhánh Git:** `feature/tv5-dashboard-reports`

### 1. Khung nội dung Word bạn cần viết:
- **Tiêu đề chương trong Word:** `CHƯƠNG: PHÂN HỆ DASHBOARD ĐIỀU HÀNH & HỆ THỐNG 9 BÁO CÁO KHO CHUYÊN SÂU (TV5: TRẦN CÔNG TÚ)`
- **Nội dung 1 - Executive Dashboard & 5 Thẻ Chỉ số KPI:**
  - Trình bày 5 chỉ số trọng yếu:
    1. Tổng giá trị tài sản tồn kho: Tính chuẩn xác bằng tổng giá vốn đích danh của tất cả Serial đang trong kho.
    2. Doanh thu phân phối bán sỉ trong kỳ.
    3. Số lượng đơn bán sỉ mới.
    4. Tổng tồn kho khả dụng cung ứng.
    5. Tỷ lệ đổi trả hàng sỉ (Cảnh báo đỏ nếu $> 2.0\%$).
  - Dòng thời gian hoạt động gần đây (Audit Activity Stream).
- **Nội dung 2 - Trực quan hóa Biểu đồ bằng MPAndroidChart:**
  - Biểu đồ BarChart / LineChart: Doanh thu phân phối sỉ 6 tháng gần nhất và tốc độ tăng trưởng.
  - Biểu đồ PieChart: Cơ cấu chi phí logistics (vận chuyển, thuế, bảo hiểm, lưu kho).
  - Bảng xếp hạng Top 5 / Top 10 mẫu đồng hồ bán chạy nhất kênh sỉ.
- **Nội dung 3 - Hệ thống 9 Báo cáo Chuyên sâu Đa phân hệ:**
  - Trình bày mục đích và bảng dữ liệu của 9 báo cáo:
    1. Báo cáo Nhập hàng theo NCC & chi phí phân bổ.
    2. Báo cáo Phân phối Bán sỉ theo từng đại lý.
    3. Báo cáo Cơ cấu xuất hàng (Bán sỉ vs Bảo hành vs Tiêu hủy).
    4. Báo cáo Tỷ lệ đổi trả theo dòng máy (Automatic, Quartz, Solar).
    5. Báo cáo Hàng chậm luân chuyển (Dead Stock Aging $> 90$ ngày, $> 180$ ngày).
    6. Báo cáo Tài chính & Lợi nhuận gộp B2B (Doanh thu trừ Giá vốn đích danh).
    7. Sổ chi tiết công nợ B2B 2 chiều (Đối soát NCC và Đại lý).
    8. Báo cáo Dòng tiền Thu/Chi thực tế (Cashflow Report).
    9. Báo cáo Nhật ký kiểm toán Audit Log toàn hệ thống.
- **Nội dung 4 - Xuất dữ liệu CSV & In ấn A4:**
  - Nút xuất file CSV lưu thư mục Downloads; xem trước và in báo cáo định dạng A4 bằng `PrintManager`.

### 2. Sơ đồ cần vẽ và chèn vào Word:
- **Sơ đồ Use Case:** *Xem Dashboard KPI, Xem biểu đồ MPAndroidChart, Lọc báo cáo theo ngày, Xem Sổ công nợ 2 chiều, Xem báo cáo Dòng tiền, Xuất file CSV, In báo cáo A4*.
- **Sơ đồ Luồng Dữ liệu (Data Aggregation Flow):** Dữ liệu thô từ Room DB (`serials`, `products`, `orders`, `transactions`) -> `DashboardRepository` thực hiện truy vấn tổng hợp (GROUP BY, SUM, COUNT) -> Truyền qua LiveData/Flow -> Render lên giao diện MPAndroidChart.

### 3. Bảng Dữ liệu Mẫu (Test Data) cần đưa vào báo cáo:
- **Doanh số 6 tháng:** Tháng 5: 1.2 tỷ, Tháng 6: 1.8 tỷ, Tháng 7: 2.1 tỷ, Tháng 8: 1.9 tỷ, Tháng 9: 2.5 tỷ, Tháng 10: 3.2 tỷ VNĐ.
- **Sổ đối soát công nợ 2 chiều mẫu:**
  - Chiều Phải Trả NCC: Rolex Geneva SA (Nợ đầu kỳ: 0, Tăng do nhập: 4 tỷ, Đã trả: 2 tỷ, Còn nợ: 2 tỷ).
  - Chiều Phải Thu Đại Lý: Galle Watch (Nợ đầu kỳ: 500tr, Tăng do mua: 1.3 tỷ, Đã thu: 800tr, Còn nợ: 1 tỷ).
- **Báo cáo Dòng tiền mẫu:** Tổng thu thực tế (1.5 tỷ) - Tổng chi thực tế (2.2 tỷ) = Dòng tiền thuần âm (-700 triệu VNĐ) -> Phản ánh giai đoạn nhập nhiều hàng chuẩn bị mùa lễ.

### 4. Câu hỏi Vấn đáp Giảng viên hay hỏi & Cách trả lời:
- **Câu 1:** *"Tại sao em không dùng phương pháp bình quân gia quyền mà lại tính Tổng tài sản kho theo Giá vốn đích danh?"*  
  👉 **Trả lời:** *"Thưa thầy/cô, trong ngành đồng hồ xa xỉ, cùng một dòng Rolex Submariner nhưng mỗi lô hàng nhập vào thời điểm khác nhau có giá ngoại tệ, cước vận chuyển và thuế suất khác nhau. Nếu dùng giá bình quân sẽ làm sai lệch giá trị tài sản hàng tỷ đồng và tính sai lợi nhuận gộp từng thương vụ. Do đó hệ thống SUM trực tiếp giá vốn thực tế của từng mã Serial lưu kho."*
- **Câu 2:** *"Báo cáo Dòng tiền (Cashflow) có gì khác so với Báo cáo Doanh thu?"*  
  👉 **Trả lời:** *"Báo cáo Doanh thu ghi nhận ngay khi xuất hóa đơn bán sỉ, dù đại lý mua nợ chưa trả tiền. Còn Báo cáo Cashflow chỉ ghi nhận tiền thực tế ra/vào tài khoản qua Phiếu Thu và Phiếu Chi, giúp Ban Giám đốc biết chính xác doanh nghiệp còn bao nhiêu tiền mặt để chi trả cho các nhà cung cấp."*

---

# PHẦN 5: CHECKLIST DÀNH CHO NHÓM TRƯỞNG (PHAN BÁ HẢI BÌNH)
> **Trách nhiệm:** Dựng khung Word tổng, tích hợp bài của 4 thành viên và chuẩn bị nộp bài.

1. **Khung sườn Báo cáo Đồ án tổng thể (Master Document Structure):**
   - Trang Bìa (Trường ĐH Kiến trúc Đà Nẵng, Khoa CNTT, Tên đề tài, Giảng viên hướng dẫn, Danh sách 5 thành viên).
   - Lời cảm ơn & Mục lục tự động, Danh mục Bảng biểu, Danh mục Hình ảnh.
   - **Chương 1:** Tổng quan bài toán B2B Luxury Horology, Kiến trúc Core MVVM, Room Database v4 & Phân quyền RBAC 5 Roles (Do Bình viết).
   - **Chương 2:** Phân hệ Nhà cung cấp & Nhập kho (Ghép bài của TV2 - Quân).
   - **Chương 3:** Phân hệ Đối tác Đại lý & Quản lý Xuất kho (Ghép bài của TV3 - Thảo).
   - **Chương 4:** Phân hệ Quản lý Tồn kho & Kiểm kê (Ghép bài của TV4 - Tâm).
   - **Chương 5:** Phân hệ Executive Dashboard & Báo cáo Chuyên sâu (Ghép bài của TV5 - Tú).
   - **Chương 6:** Đánh giá kết quả thực nghiệm, Quy chuẩn Git Workflow & Hướng phát triển tương lai.
2. **Quy trình duyệt bài:**
   - Kiểm tra ảnh chụp màn hình của từng bạn (không để ảnh vỡ hạt hoặc mờ).
   - Kiểm tra mã package (`com.example.chronovaultwms.*`) và vai trò xem có đúng chuẩn không.
   - Thống nhất định dạng: Tiêu đề Heading 1 màu Xanh Navy `#1B365D`, bảng biểu viền gọn gàng, đánh số thứ tự hình vẽ (Hình 2.1, Hình 3.1...).

