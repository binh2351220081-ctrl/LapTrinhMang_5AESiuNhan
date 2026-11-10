/**
 * CHRONO VAULT B2B - MASTER DATA & STORAGE ENGINE
 * Dữ liệu chuẩn hóa theo Bảng Đặc tả Chức năng Hệ thống Quản lý Kho Đồng Hồ
 * Phân hệ 1 đến Phân hệ 5 (TV1 - TV5)
 */

const STORAGE_KEYS = {
  WATCHES: 'chrono_watches_v2',
  SERIALS: 'chrono_serials_v2',
  SUPPLIERS: 'chrono_suppliers_v2',
  DEALERS: 'chrono_dealers_v2',
  RECEIPTS: 'chrono_receipts_v2',
  ORDERS: 'chrono_orders_v2',
  SHELVES: 'chrono_shelves_v2',
  AUDIT_LOGS: 'chrono_logs_v2',
  FINANCE: 'chrono_finance_v2',
  ACCOUNTS: 'chrono_accounts_v2',
  ROLES: 'chrono_roles_v2',
  SUPPLIER_PAYMENTS: 'chrono_supplier_payments_v2',
  SUPPLIER_RETURNS: 'chrono_supplier_returns_v2',
  DEALER_RECEIPTS: 'chrono_dealer_receipts_v2',
  CUSTOMER_RETURNS: 'chrono_customer_returns_v2',
  OTHER_DISPATCHES: 'chrono_other_dispatches_v2',
  STOCK_AUDITS: 'chrono_stock_audits_v2',
  STOCK_CARDS: 'chrono_stock_cards_v2'
};

// ==========================================
// SEED DATA 1: DANH MỤC ĐỒNG HỒ (TV1)
// ==========================================
const INITIAL_WATCHES = [
  {
    id: 'W001',
    sku: 'RLX-SUB-126610LN',
    barcode: '7613297241012',
    name: 'Rolex Submariner Date 41mm',
    brand: 'Rolex',
    category: 'Lặn biển & Sang trọng',
    movement: 'Cơ Automatic (Calibre 3235)',
    glass: 'Sapphire nguyên khối chống lóa',
    strap: 'Thép không gỉ Oystersteel 904L',
    dialSize: '41mm',
    waterResist: '30 ATM (300m)',
    warranty: '5 năm chính hãng',
    hasSerial: true,
    baseUnit: 'Chiếc',
    wholesaleUnit: 'Thùng',
    conversionRate: 10, // 1 Thùng = 10 Chiếc
    costPriceMethod: 'Đích danh theo Serial',
    baseCost: 265000000,
    wholesalePriceVip: 295000000,
    wholesalePriceSilver: 310000000,
    wholesalePriceBronze: 325000000,
    moq: 2,
    minStock: 5,
    maxStock: 30,
    image: 'rolex-sub',
    shelfId: 'A-01',
    status: 'ACTIVE'
  },
  {
    id: 'W002',
    sku: 'OMG-SEA-220104121',
    barcode: '7612586241884',
    name: 'Omega Seamaster Aqua Terra 150M',
    brand: 'Omega',
    category: 'Thể thao sang trọng',
    movement: 'Cơ Co-Axial Master Chronometer 8900',
    glass: 'Sapphire vòm kép chống phản chiếu',
    strap: 'Dây thép không gỉ 316L',
    dialSize: '41mm',
    waterResist: '15 ATM (150m)',
    warranty: '5 năm toàn cầu',
    hasSerial: true,
    baseUnit: 'Chiếc',
    wholesaleUnit: 'Thùng',
    conversionRate: 10,
    costPriceMethod: 'Đích danh theo Serial',
    baseCost: 135000000,
    wholesalePriceVip: 155000000,
    wholesalePriceSilver: 165000000,
    wholesalePriceBronze: 172000000,
    moq: 2,
    minStock: 4,
    maxStock: 25,
    image: 'omega-sea',
    shelfId: 'A-02',
    status: 'ACTIVE'
  },
  {
    id: 'W003',
    sku: 'TIS-PRX-T137407',
    barcode: '7611608298711',
    name: 'Tissot PRX Powermatic 80 Blue',
    brand: 'Tissot',
    category: 'Classic Vintage',
    movement: 'Cơ Automatic trữ cót 80 giờ',
    glass: 'Sapphire phủ chống lóa',
    strap: 'Thép phay xước cao cấp 316L',
    dialSize: '40mm',
    waterResist: '10 ATM (100m)',
    warranty: '2 năm quốc tế',
    hasSerial: true,
    baseUnit: 'Chiếc',
    wholesaleUnit: 'Kiện',
    conversionRate: 20, // 1 Kiện = 20 Chiếc
    costPriceMethod: 'Đích danh theo Serial',
    baseCost: 13800000,
    wholesalePriceVip: 16200000,
    wholesalePriceSilver: 17500000,
    wholesalePriceBronze: 18400000,
    moq: 5,
    minStock: 15,
    maxStock: 100,
    image: 'tissot-prx',
    shelfId: 'B-01',
    status: 'ACTIVE'
  },
  {
    id: 'W004',
    sku: 'SEI-PRO-SPB143J1',
    barcode: '4954628236104',
    name: 'Seiko Prospex 1965 Diver Re-interpretation',
    brand: 'Seiko',
    category: 'Thợ lặn chuyên nghiệp',
    movement: 'Cơ 6R35 trữ cót 70 giờ',
    glass: 'Sapphire cong chống trầy siêu cứng',
    strap: 'Thép không gỉ phủ lớp chống trầy Diashield',
    dialSize: '40.5mm',
    waterResist: '20 ATM (200m)',
    warranty: '3 năm chính hãng',
    hasSerial: true,
    baseUnit: 'Chiếc',
    wholesaleUnit: 'Kiện',
    conversionRate: 15,
    costPriceMethod: 'Đích danh theo Serial',
    baseCost: 21500000,
    wholesalePriceVip: 25800000,
    wholesalePriceSilver: 27500000,
    wholesalePriceBronze: 28900000,
    moq: 3,
    minStock: 8,
    maxStock: 60,
    image: 'seiko-pro',
    shelfId: 'B-01',
    status: 'ACTIVE'
  },
  {
    id: 'W005',
    sku: 'CAS-GSH-MTGB2000',
    barcode: '4549526288124',
    name: 'Casio G-Shock MT-G Carbon Core Guard',
    brand: 'Casio',
    category: 'Chống sốc cao cấp',
    movement: 'Tough Solar kết nối Bluetooth / Radio Wave',
    glass: 'Sapphire phủ chống lóa không trầy',
    strap: 'Dây kim loại kết hợp nhựa Resin gia cường',
    dialSize: '51mm',
    waterResist: '20 ATM (200m)',
    warranty: '5 năm toàn diện',
    hasSerial: true,
    baseUnit: 'Chiếc',
    wholesaleUnit: 'Thùng',
    conversionRate: 10,
    costPriceMethod: 'Đích danh theo Serial',
    baseCost: 19500000,
    wholesalePriceVip: 23200000,
    wholesalePriceSilver: 24800000,
    wholesalePriceBronze: 26000000,
    moq: 4,
    minStock: 6,
    maxStock: 50,
    image: 'casio-mtg',
    shelfId: 'B-02',
    status: 'ACTIVE'
  },
  {
    id: 'W006',
    sku: 'CTZ-PRO-BN0150',
    barcode: '4974374249120',
    name: 'Citizen Promaster Eco-Drive Diver',
    brand: 'Citizen',
    category: 'Lặn thể thao',
    movement: 'Eco-Drive E168 (Năng lượng ánh sáng)',
    glass: 'Kính khoáng cường lực Mineral',
    strap: 'Dây cao su Polyurethane đen',
    dialSize: '44mm',
    waterResist: '20 ATM (200m ISO)',
    warranty: '3 năm quốc tế',
    hasSerial: true,
    baseUnit: 'Chiếc',
    wholesaleUnit: 'Kiện',
    conversionRate: 20,
    costPriceMethod: 'Đích danh theo Serial',
    baseCost: 5600000,
    wholesalePriceVip: 6800000,
    wholesalePriceSilver: 7400000,
    wholesalePriceBronze: 7900000,
    moq: 5,
    minStock: 10,
    maxStock: 80,
    image: 'citizen-pro',
    shelfId: 'B-02',
    status: 'ACTIVE'
  }
];

// ==========================================
// SEED DATA 2: SERIAL NUMBER & VÒNG ĐỜI (TV1 & TV4)
// ==========================================
const INITIAL_SERIALS = [
  {
    serialNumber: 'RLX-SUB-2026-9901',
    sku: 'RLX-SUB-126610LN',
    watchName: 'Rolex Submariner Date 41mm',
    costPrice: 265000000,
    status: 'IN_STOCK', // IN_STOCK, RESERVED, SOLD, DEFECT, RETURNED_SUPPLIER, WARRANTY
    qualityType: 'NEW', // NEW (Kho Mới), DISPLAY (Trưng Bày), DEFECT (Hàng Lỗi)
    shelfLocation: 'A-01-T2-N03',
    supplierId: 'NCC01',
    receiptCode: 'PN-2026-001',
    receivedDate: '2026-08-15',
    dealerId: null,
    orderCode: null,
    soldDate: null,
    warrantyExpire: '2031-08-15',
    timeline: [
      { date: '2026-08-15 09:30', title: 'Nhập kho thành công', desc: 'Từ NCC: Rolex Authorized Asia theo PN-2026-001. Giá vốn: 265.000.000đ' },
      { date: '2026-08-15 11:00', title: 'Định vị vị trí kệ', desc: 'Chuyển vào Kho Hàng Mới: Vị trí Kệ A-01-T2-N03' },
      { date: '2026-09-01 14:20', title: 'Kiểm kê định kỳ tháng 9', desc: 'Khớp 100% số liệu thực tế tại kệ' }
    ]
  },
  {
    serialNumber: 'RLX-SUB-2026-9902',
    sku: 'RLX-SUB-126610LN',
    watchName: 'Rolex Submariner Date 41mm',
    costPrice: 265500000,
    status: 'RESERVED',
    qualityType: 'NEW',
    shelfLocation: 'A-01-T2-N04',
    supplierId: 'NCC01',
    receiptCode: 'PN-2026-001',
    receivedDate: '2026-08-15',
    dealerId: 'DL01',
    orderCode: 'DS-2026-104',
    soldDate: null,
    warrantyExpire: '2031-08-15',
    timeline: [
      { date: '2026-08-15 09:30', title: 'Nhập kho thành công', desc: 'Từ NCC: Rolex Authorized Asia theo PN-2026-001' },
      { date: '2026-08-15 11:00', title: 'Định vị vị trí kệ', desc: 'Vị trí Kệ A-01-T2-N04' },
      { date: '2026-09-28 10:15', title: 'Khóa giữ chỗ (Reserved)', desc: 'Đơn sỉ DS-2026-104 của Đại lý Hoàng Kim Watch VIP (Đã cọc 30%)' }
    ]
  },
  {
    serialNumber: 'RLX-SUB-2026-9888',
    sku: 'RLX-SUB-126610LN',
    watchName: 'Rolex Submariner Date 41mm',
    costPrice: 264000000,
    status: 'SOLD',
    qualityType: 'NEW',
    shelfLocation: 'Đã xuất kho',
    supplierId: 'NCC01',
    receiptCode: 'PN-2026-001',
    receivedDate: '2026-08-15',
    dealerId: 'DL01',
    orderCode: 'DS-2026-098',
    soldDate: '2026-09-10',
    warrantyExpire: '2031-09-10',
    timeline: [
      { date: '2026-08-15 09:30', title: 'Nhập kho thành công', desc: 'Nhập từ Rolex Authorized Asia' },
      { date: '2026-09-08 14:00', title: 'Lên đơn sỉ DS-2026-098', desc: 'Đại lý Đồng Hồ Hoàng Kim đặt sỉ' },
      { date: '2026-09-10 16:30', title: 'Quét xuất kho & Bàn giao', desc: 'Xuất giao đại lý theo PX-2026-088. Kích hoạt bảo hành điện tử 5 năm' }
    ]
  },
  {
    serialNumber: 'OMG-SEA-2026-4401',
    sku: 'OMG-SEA-220104121',
    watchName: 'Omega Seamaster Aqua Terra 150M',
    costPrice: 135000000,
    status: 'IN_STOCK',
    qualityType: 'NEW',
    shelfLocation: 'A-02-T1-N01',
    supplierId: 'NCC02',
    receiptCode: 'PN-2026-002',
    receivedDate: '2026-08-20',
    dealerId: null,
    orderCode: null,
    soldDate: null,
    warrantyExpire: '2031-08-20',
    timeline: [
      { date: '2026-08-20 10:15', title: 'Nhập kho thành công', desc: 'Từ NCC: Swatch Group Vietnam theo PN-2026-002' },
      { date: '2026-08-20 11:30', title: 'Lưu kho thành công', desc: 'Định vị Kệ A-02-T1-N01' }
    ]
  },
  {
    serialNumber: 'OMG-SEA-2026-4402',
    sku: 'OMG-SEA-220104121',
    watchName: 'Omega Seamaster Aqua Terra 150M',
    costPrice: 135000000,
    status: 'IN_STOCK',
    qualityType: 'DISPLAY',
    shelfLocation: 'A-02-T3-DEMO',
    supplierId: 'NCC02',
    receiptCode: 'PN-2026-002',
    receivedDate: '2026-08-20',
    dealerId: null,
    orderCode: null,
    soldDate: null,
    warrantyExpire: '2031-08-20',
    timeline: [
      { date: '2026-08-20 10:15', title: 'Nhập kho thành công', desc: 'Nhập khẩu từ Swatch Group' },
      { date: '2026-08-25 09:00', title: 'Chuyển Kho Trưng Bày', desc: 'Chuyển mẫu đồng hồ sang Showroom B2B giới thiệu khách sỉ' }
    ]
  },
  {
    serialNumber: 'TIS-PRX-2026-1101',
    sku: 'TIS-PRX-T137407',
    watchName: 'Tissot PRX Powermatic 80 Blue',
    costPrice: 13800000,
    status: 'IN_STOCK',
    qualityType: 'NEW',
    shelfLocation: 'B-01-T1-N02',
    supplierId: 'NCC02',
    receiptCode: 'PN-2026-002',
    receivedDate: '2026-08-20',
    dealerId: null,
    orderCode: null,
    soldDate: null,
    warrantyExpire: '2028-08-20',
    timeline: [
      { date: '2026-08-20 10:15', title: 'Nhập kho theo Kiện sỉ', desc: 'Quy đổi 1 Kiện = 20 Chiếc theo PN-2026-002' }
    ]
  },
  {
    serialNumber: 'TIS-PRX-2026-1102',
    sku: 'TIS-PRX-T137407',
    watchName: 'Tissot PRX Powermatic 80 Blue',
    costPrice: 13800000,
    status: 'DEFECT',
    qualityType: 'DEFECT',
    shelfLocation: 'C-01-KHO-LOI',
    supplierId: 'NCC02',
    receiptCode: 'PN-2026-002',
    receivedDate: '2026-08-20',
    dealerId: 'DL02',
    orderCode: 'DS-2026-095',
    soldDate: null,
    warrantyExpire: '2028-08-20',
    timeline: [
      { date: '2026-08-20 10:15', title: 'Nhập kho nguyên kiện', desc: 'Nhập từ Swatch Group' },
      { date: '2026-09-02 11:00', title: 'Xuất sỉ Hải Triều', desc: 'Theo đơn DS-2026-095' },
      { date: '2026-09-12 15:30', title: 'Tiếp nhận đổi trả sỉ', desc: 'Đại lý Hải Triều trả lại do hấp hơi nước mặt kính' },
      { date: '2026-09-12 16:00', title: 'Cách ly Kho Hàng Lỗi', desc: 'Lưu tại Kệ C-01 chờ lập Phiếu xuất trả NCC hoàn tiền' }
    ]
  },
  {
    serialNumber: 'SEI-PRO-2026-7701',
    sku: 'SEI-PRO-SPB143J1',
    watchName: 'Seiko Prospex 1965 Diver Re-interpretation',
    costPrice: 21500000,
    status: 'IN_STOCK',
    qualityType: 'NEW',
    shelfLocation: 'B-01-T2-N05',
    supplierId: 'NCC03',
    receiptCode: 'PN-2026-003',
    receivedDate: '2026-09-01',
    dealerId: null,
    orderCode: null,
    soldDate: null,
    warrantyExpire: '2029-09-01',
    timeline: [
      { date: '2026-09-01 08:45', title: 'Nhập kho', desc: 'Nhập từ Seiko Epson Vietnam theo PN-2026-003' }
    ]
  },
  {
    serialNumber: 'CAS-GSH-2026-3301',
    sku: 'CAS-GSH-MTGB2000',
    watchName: 'Casio G-Shock MT-G Carbon Core Guard',
    costPrice: 19500000,
    status: 'IN_STOCK',
    qualityType: 'NEW',
    shelfLocation: 'B-02-T1-N01',
    supplierId: 'NCC03',
    receiptCode: 'PN-2026-003',
    receivedDate: '2026-09-01',
    dealerId: null,
    orderCode: null,
    soldDate: null,
    warrantyExpire: '2031-09-01',
    timeline: [
      { date: '2026-09-01 08:45', title: 'Nhập kho', desc: 'Nhập từ Seiko & Casio Distributor' }
    ]
  },
  {
    serialNumber: 'CTZ-PRO-2026-5501',
    sku: 'CTZ-PRO-BN0150',
    watchName: 'Citizen Promaster Eco-Drive Diver',
    costPrice: 5600000,
    status: 'IN_STOCK',
    qualityType: 'NEW',
    shelfLocation: 'B-02-T2-N04',
    supplierId: 'NCC03',
    receiptCode: 'PN-2026-003',
    receivedDate: '2026-09-01',
    dealerId: null,
    orderCode: null,
    soldDate: null,
    warrantyExpire: '2029-09-01',
    timeline: [
      { date: '2026-09-01 08:45', title: 'Nhập kho', desc: 'Nhập khẩu từ Citizen Partner' }
    ]
  }
];

// ==========================================
// SEED DATA 3: NHÀ CUNG CẤP & CÔNG NỢ NCC (TV2)
// ==========================================
const INITIAL_SUPPLIERS = [
  {
    id: 'NCC01',
    name: 'Rolex Authorized Distribution Asia Pte. Ltd',
    taxCode: '0312456789',
    phone: '+84 28 3822 9999',
    representative: 'Mr. Jean-Marc Dubois',
    address: 'Tầng 18, Tòa nhà Bitexco, Q.1, TP.HCM',
    bankAccount: '0071001234567',
    bankName: 'Vietcombank CN Bến Thành',
    debtBalance: 1250000000, // Nợ phải trả NCC
    status: 'ACTIVE'
  },
  {
    id: 'NCC02',
    name: 'Swatch Group Distribution Vietnam Co., Ltd',
    taxCode: '0309887711',
    phone: '+84 28 3910 8888',
    representative: 'Bà Trần Thu Hà',
    address: 'Vincom Center Đồng Khởi, 72 Lê Thánh Tôn, Q.1, TP.HCM',
    bankAccount: '119000889977',
    bankName: 'Vietinbank CN TP.HCM',
    debtBalance: 480000000,
    status: 'ACTIVE'
  },
  {
    id: 'NCC03',
    name: 'Seiko Epson Corporation Vietnam',
    taxCode: '0108992233',
    phone: '+84 24 3772 5555',
    representative: 'Mr. Kenjiro Tanaka',
    address: 'Tòa nhà Keangnam Landmark 72, Nam Từ Liêm, Hà Nội',
    bankAccount: '0451000998877',
    bankName: 'VCB Thăng Long',
    debtBalance: 165000000,
    status: 'ACTIVE'
  }
];

// Phiếu Chi Thanh Toán Nợ NCC (TV2.1)
const INITIAL_SUPPLIER_PAYMENTS = [
  {
    id: 'PC-2026-001',
    supplierId: 'NCC01',
    supplierName: 'Rolex Authorized Distribution Asia',
    date: '2026-08-25',
    amount: 1700000000,
    paymentMethod: 'CHUYEN_KHOAN',
    bankAccount: '0071001234567 - Vietcombank CN Bến Thành',
    referenceDoc: 'Thanh toán đợt 1 PN-2026-001',
    createdBy: 'Kế toán (Phạm Thị Lan)',
    note: 'Ủy nhiệm chi ngân hàng số UNC-88412'
  },
  {
    id: 'PC-2026-002',
    supplierId: 'NCC02',
    supplierName: 'Swatch Group Distribution Vietnam',
    date: '2026-08-30',
    amount: 1320800000,
    paymentMethod: 'CHUYEN_KHOAN',
    bankAccount: '119000889977 - Vietinbank CN TP.HCM',
    referenceDoc: 'Thanh toán đợt 1 PN-2026-002',
    createdBy: 'Kế toán (Phạm Thị Lan)',
    note: 'Chuyển khoản thanh toán lô Tissot & Omega'
  }
];

// Phiếu Xuất Trả Hàng Lỗi Cho NCC (TV2.1)
const INITIAL_SUPPLIER_RETURNS = [
  {
    id: 'XT-2026-001',
    supplierId: 'NCC02',
    supplierName: 'Swatch Group Distribution Vietnam',
    date: '2026-09-15',
    watchId: 'W003',
    watchName: 'Tissot PRX Powermatic 80 Blue',
    serials: ['TIS-PRX-2026-0999'],
    quantity: 1,
    refundValue: 13800000,
    reason: 'Lỗi hấp hơi mặt kính từ nhà sản xuất',
    status: 'APPROVED',
    createdBy: 'Thủ kho (Lê Tuấn)'
  }
];

// ==========================================
// SEED DATA 4: ĐẠI LÝ B2B & CÔNG NỢ SỈ (TV3)
// ==========================================
const INITIAL_DEALERS = [
  {
    id: 'DL01',
    shopName: 'Đại Lý Đồng Hồ Hoàng Kim',
    companyName: 'Công ty Cổ phần Thương mại Hoàng Kim Luxury',
    representative: 'Ông Nguyễn Hoàng Kim',
    taxCode: '0315998811',
    phone: '0908 123 456',
    address: '158 Lê Lợi, Phường Bến Thành, Quận 1, TP.HCM',
    tier: 'VIP', // VIP: 15% discount, Silver: 10%, Bronze: 5%
    discountRate: 0.15,
    creditLimit: 2000000000, // Hạn mức tín dụng 2 tỷ
    currentDebt: 650000000, // Dư nợ hiện tại
    availableCredit: 1350000000,
    status: 'ACTIVE'
  },
  {
    id: 'DL02',
    shopName: 'Hệ Thống Showroom Hải Triều',
    companyName: 'Công ty TNHH Hải Triều Watch & Jewelry',
    representative: 'Bà Đặng Thị Thanh Thảo',
    taxCode: '0304991122',
    phone: '0912 888 999',
    address: '160 Âu Cơ, Phường 9, Quận Tân Bình, TP.HCM',
    tier: 'SILVER',
    discountRate: 0.10,
    creditLimit: 1200000000,
    currentDebt: 420000000,
    availableCredit: 780000000,
    status: 'ACTIVE'
  },
  {
    id: 'DL03',
    shopName: 'Chuỗi Cửa Hàng WatchStore',
    companyName: 'Công ty Cổ phần Bán lẻ WatchStore Việt Nam',
    representative: 'Ông Vũ Tuấn Anh',
    taxCode: '0107883344',
    phone: '0933 667 788',
    address: '58 Trần Phú, Quận Ba Đình, Hà Nội',
    tier: 'BRONZE',
    discountRate: 0.05,
    creditLimit: 500000000,
    currentDebt: 110000000,
    availableCredit: 390000000,
    status: 'ACTIVE'
  }
];

// Phiếu Thu Tiền Bán Sỉ / Thu Hồi Nợ Đại Lý (TV3.1)
const INITIAL_DEALER_RECEIPTS = [
  {
    id: 'PT-2026-001',
    dealerId: 'DL01',
    dealerName: 'Đại Lý Đồng Hồ Hoàng Kim',
    date: '2026-09-10',
    amount: 150000000,
    paymentMethod: 'CHUYEN_KHOAN',
    referenceDoc: 'Thu tiền cọc đơn sỉ DS-2026-104',
    createdBy: 'Kế toán (Phạm Thị Lan)',
    note: 'Chuyển khoản qua VCB tài khoản công ty'
  },
  {
    id: 'PT-2026-002',
    dealerId: 'DL02',
    dealerName: 'Hệ Thống Showroom Hải Triều',
    date: '2026-09-20',
    amount: 80000000,
    paymentMethod: 'CHUYEN_KHOAN',
    referenceDoc: 'Thu hồi nợ kỳ 1 tháng 9',
    createdBy: 'Kế toán (Phạm Thị Lan)',
    note: 'Đại lý Hải Triều đối soát thanh toán'
  }
];

// Phiếu Nhận Đổi Trả Hàng Sỉ (TV3.1)
const INITIAL_CUSTOMER_RETURNS = [
  {
    id: 'TS-2026-001',
    dealerId: 'DL02',
    dealerName: 'Hệ Thống Showroom Hải Triều',
    date: '2026-09-12',
    serial: 'TIS-PRX-2026-1102',
    watchId: 'W003',
    watchName: 'Tissot PRX Powermatic 80 Blue',
    returnType: 'DEFECT_WAREHOUSE', // DEFECT_WAREHOUSE hoặc RESTOCK_NEW
    refundAmount: 16200000,
    reason: 'Đồng hồ có dấu hiệu hơi nước trong kính khi đại lý kiểm tra giao khách',
    status: 'COMPLETED',
    createdBy: 'Nhân viên nhập/xuất kho (Nguyễn Phương)'
  }
];

// Phiếu Xuất Khác: Bảo Hành / Hủy Hỏng (TV3.2)
const INITIAL_OTHER_DISPATCHES = [
  {
    id: 'XK-2026-001',
    type: 'WARRANTY', // WARRANTY (Xuất bảo hành hãng), DISPOSE (Xuất hủy hàng hỏng)
    date: '2026-09-18',
    watchId: 'W002',
    watchName: 'Omega Seamaster Aqua Terra 150M',
    serials: ['OMG-SEA-2026-4412'],
    destination: 'Trung tâm Bảo hành Quốc tế Swatch Group TP.HCM',
    reason: 'Chuyển hãng cân chỉnh độ sai số cơ học định kỳ',
    createdBy: 'Thủ kho (Lê Tuấn)'
  }
];

// ==========================================
// SEED DATA 5: PHIẾU NHẬP KHO & ĐƠN BÁN SỈ
// ==========================================
const INITIAL_RECEIPTS = [
  {
    code: 'PN-2026-001',
    supplierId: 'NCC01',
    supplierName: 'Rolex Authorized Distribution Asia',
    date: '2026-08-15',
    status: 'COMPLETED',
    items: [
      {
        watchId: 'W001',
        sku: 'RLX-SUB-126610LN',
        name: 'Rolex Submariner Date 41mm',
        unit: 'Thùng',
        quantity: 1,
        convertedQty: 10,
        unitCost: 265000000,
        subtotal: 2650000000,
        serials: ['RLX-SUB-2026-9901', 'RLX-SUB-2026-9902', 'RLX-SUB-2026-9888', 'RLX-SUB-2026-9904', 'RLX-SUB-2026-9905', 'RLX-SUB-2026-9906', 'RLX-SUB-2026-9907', 'RLX-SUB-2026-9908', 'RLX-SUB-2026-9909', 'RLX-SUB-2026-9910']
      }
    ],
    allocatedExpenses: 35000000,
    taxRate: 0.1,
    totalAmount: 2950000000,
    paidAmount: 1700000000,
    debtRemaining: 1250000000
  },
  {
    code: 'PN-2026-002',
    supplierId: 'NCC02',
    supplierName: 'Swatch Group Distribution Vietnam',
    date: '2026-08-20',
    status: 'COMPLETED',
    items: [
      {
        watchId: 'W002',
        sku: 'OMG-SEA-220104121',
        name: 'Omega Seamaster Aqua Terra 150M',
        unit: 'Thùng',
        quantity: 1,
        convertedQty: 10,
        unitCost: 135000000,
        subtotal: 1350000000,
        serials: ['OMG-SEA-2026-4401', 'OMG-SEA-2026-4402', 'OMG-SEA-2026-4403', 'OMG-SEA-2026-4404', 'OMG-SEA-2026-4405', 'OMG-SEA-2026-4406', 'OMG-SEA-2026-4407', 'OMG-SEA-2026-4408', 'OMG-SEA-2026-4409', 'OMG-SEA-2026-4410']
      },
      {
        watchId: 'W003',
        sku: 'TIS-PRX-T137407',
        name: 'Tissot PRX Powermatic 80 Blue',
        unit: 'Kiện',
        quantity: 1,
        convertedQty: 20,
        unitCost: 13800000,
        subtotal: 276000000,
        serials: ['TIS-PRX-2026-1101', 'TIS-PRX-2026-1102', 'TIS-PRX-2026-1103']
      }
    ],
    allocatedExpenses: 12000000,
    taxRate: 0.1,
    totalAmount: 1800800000,
    paidAmount: 1320800000,
    debtRemaining: 480000000
  }
];

const INITIAL_ORDERS = [
  {
    code: 'DS-2026-104',
    dealerId: 'DL01',
    dealerName: 'Đại Lý Đồng Hồ Hoàng Kim (VIP)',
    date: '2026-09-28',
    status: 'RESERVED', // DRAFT, RESERVED, COMPLETED, CANCELLED
    items: [
      {
        watchId: 'W001',
        sku: 'RLX-SUB-126610LN',
        name: 'Rolex Submariner Date 41mm',
        unit: 'Chiếc',
        quantity: 1,
        convertedQty: 1,
        unitPrice: 295000000,
        discountPercent: 15,
        finalUnitPrice: 250750000,
        subtotal: 250750000,
        reservedSerials: ['RLX-SUB-2026-9902']
      }
    ],
    totalAmount: 250750000,
    depositAmount: 100000000,
    remainingDebt: 150750000,
    shippingFee: 2500000,
    note: 'Đại lý VIP đã thanh toán cọc 100 triệu, giữ chỗ serial nguyên seal'
  },
  {
    code: 'DS-2026-098',
    dealerId: 'DL01',
    dealerName: 'Đại Lý Đồng Hồ Hoàng Kim (VIP)',
    date: '2026-09-08',
    status: 'COMPLETED',
    items: [
      {
        watchId: 'W001',
        sku: 'RLX-SUB-126610LN',
        name: 'Rolex Submariner Date 41mm',
        unit: 'Chiếc',
        quantity: 1,
        convertedQty: 1,
        unitPrice: 295000000,
        discountPercent: 15,
        finalUnitPrice: 250750000,
        subtotal: 250750000,
        dispatchedSerials: ['RLX-SUB-2026-9888']
      }
    ],
    totalAmount: 250750000,
    depositAmount: 250750000,
    remainingDebt: 0,
    shippingFee: 0,
    note: 'Đã hoàn tất thanh toán và xuất giao đại lý'
  }
];

// ==========================================
// SEED DATA 6: VỊ TRÍ KỆ & KIỂM KÊ & THẺ KHO (TV4)
// ==========================================
const INITIAL_SHELVES = [
  { id: 'A-01', name: 'Kệ A-01 (Đồng hồ Thụy Sỹ Luxury)', zone: 'Khu A - Tủ Kính Chống Ẩm', capacity: 30, currentCount: 18, category: 'Thụy Sỹ' },
  { id: 'A-02', name: 'Kệ A-02 (Omega & Longines Thể Thao)', zone: 'Khu A - Tủ Kính Chống Ẩm', capacity: 25, currentCount: 14, category: 'Thụy Sỹ' },
  { id: 'B-01', name: 'Kệ B-01 (Seiko & Tissot Phân Phối Sỉ)', zone: 'Khu B - Kệ Kiện Sỉ An Ninh', capacity: 60, currentCount: 42, category: 'Nhật Bản & Thụy Sỹ' },
  { id: 'B-02', name: 'Kệ B-02 (Casio G-Shock & Citizen)', zone: 'Khu B - Kệ Kiện Sỉ An Ninh', capacity: 80, currentCount: 56, category: 'Nhật Bản' },
  { id: 'C-01', name: 'Kệ C-01 (Kho Hàng Lỗi Chờ Trả NCC)', zone: 'Khu C - Khu Cách Ly Kỹ Thuật', capacity: 20, currentCount: 3, category: 'Hàng Lỗi' }
];

const INITIAL_STOCK_AUDITS = [
  {
    id: 'KK-2026-001',
    auditDate: '2026-09-01',
    shelfId: 'A-01',
    shelfName: 'Kệ A-01 (Đồng hồ Thụy Sỹ Luxury)',
    bookCount: 18,
    actualCount: 18,
    diffCount: 0,
    status: 'KHỚP_100%',
    auditor: 'Thủ kho (Lê Tuấn)',
    note: 'Khớp 100% số liệu vật lý với danh sách Serial trên hệ thống'
  },
  {
    id: 'KK-2026-002',
    auditDate: '2026-09-15',
    shelfId: 'B-01',
    shelfName: 'Kệ B-01 (Seiko & Tissot)',
    bookCount: 42,
    actualCount: 42,
    diffCount: 0,
    status: 'KHỚP_100%',
    auditor: 'Thủ kho (Lê Tuấn)',
    note: 'Đã kiểm đếm đầy đủ 42 chiếc nguyên kiện'
  }
];

const INITIAL_STOCK_CARDS = [
  {
    id: 'TK-001',
    date: '2026-08-15 09:30',
    watchId: 'W001',
    sku: 'RLX-SUB-126610LN',
    watchName: 'Rolex Submariner Date 41mm',
    refType: 'NHẬP_KHO',
    refCode: 'PN-2026-001',
    changeQty: 10,
    balanceAfter: 10,
    serialNumber: 'RLX-SUB-2026-9901 -> 9910',
    user: 'Thủ kho (Lê Tuấn)',
    note: 'Nhập khẩu 1 Thùng (10 Chiếc) từ Rolex Asia'
  },
  {
    id: 'TK-002',
    date: '2026-09-10 16:30',
    watchId: 'W001',
    sku: 'RLX-SUB-126610LN',
    watchName: 'Rolex Submariner Date 41mm',
    refType: 'XUẤT_SỈ',
    refCode: 'DS-2026-098',
    changeQty: -1,
    balanceAfter: 9,
    serialNumber: 'RLX-SUB-2026-9888',
    user: 'Thủ kho (Lê Tuấn)',
    note: 'Xuất giao 1 chiếc cho Đại lý Đồng Hồ Hoàng Kim'
  },
  {
    id: 'TK-003',
    date: '2026-09-12 15:30',
    watchId: 'W003',
    sku: 'TIS-PRX-T137407',
    watchName: 'Tissot PRX Powermatic 80 Blue',
    refType: 'ĐỔI_TRẢ_SỈ',
    refCode: 'TS-2026-001',
    changeQty: 1,
    balanceAfter: 15,
    serialNumber: 'TIS-PRX-2026-1102',
    user: 'Thủ kho (Lê Tuấn)',
    note: 'Nhận đổi trả lỗi hơi kính từ Hải Triều -> Nhập cách ly Kho Lỗi C-01'
  }
];

// ==========================================
// SEED DATA 7: TÀI KHOẢN & PHÂN QUYỀN (TV1.2)
// ==========================================
const INITIAL_ACCOUNTS = [
  {
    id: 'USR01',
    username: 'admin',
    fullName: 'Trần Bảo',
    email: 'bao.tran@chronovault.com',
    role: 'ADMIN',
    roleName: 'Quản Trị Hệ Thống',
    status: 'ACTIVE',
    phone: '0988 123 456',
    avatar: 'TB',
    lastLogin: 'Hôm nay 08:30'
  },
  {
    id: 'USR02',
    username: 'thukho_tuan',
    fullName: 'Lê Tuấn',
    email: 'tuan.le@chronovault.com',
    role: 'KHO',
    roleName: 'Thủ Kho',
    status: 'ACTIVE',
    phone: '0977 234 567',
    avatar: 'LT',
    lastLogin: 'Hôm nay 07:45'
  },
  {
    id: 'USR03',
    username: 'nhanvien_kho',
    fullName: 'Nguyễn Phương',
    email: 'phuong.nguyen@chronovault.com',
    role: 'NHANVIEN_KHO',
    roleName: 'Nhân Viên Nhập/Xuất Kho',
    status: 'ACTIVE',
    phone: '0966 345 678',
    avatar: 'NP',
    lastLogin: 'Hôm qua 17:20'
  },
  {
    id: 'USR04',
    username: 'ketoan_lan',
    fullName: 'Phạm Thị Lan',
    email: 'lan.pham@chronovault.com',
    role: 'KETOAN',
    roleName: 'Kế Toán',
    status: 'ACTIVE',
    phone: '0955 456 789',
    avatar: 'PL',
    lastLogin: 'Hôm qua 16:50'
  },
  {
    id: 'USR05',
    username: 'chucuahang',
    fullName: 'Nguyễn Minh Châu',
    email: 'chau.nguyen@chronovault.com',
    role: 'OWNER',
    roleName: 'Chủ Cửa Hàng',
    status: 'ACTIVE',
    phone: '0944 567 890',
    avatar: 'NC',
    lastLogin: 'Hôm nay 08:00'
  }
];

const INITIAL_ROLES = [
  {
    roleId: 'ADMIN',
    roleName: 'Quản Trị Hệ Thống (Admin)',
    desc: 'Quản trị tài khoản, vai trò, cấu hình hệ thống và nhật ký; không mặc định xử lý nghiệp vụ kho hoặc tài chính',
    permissions: {
      products: { view: true, add: true, edit: true, delete: true },
      inbound: { view: true, create: false, approve: false, pay: false },
      outbound: { view: true, create: false, approve: false, collect: false },
      warehouse: { view: true, audit: false, balance: false },
      reports: { view: true, export: true },
      system: { manageUsers: true, manageRoles: true, viewLogs: true }
    }
  },
  {
    roleId: 'KHO',
    roleName: 'Thủ Kho',
    desc: 'Chịu trách nhiệm bảo quản, vị trí kệ, kiểm đếm và xác nhận giao nhận vật lý; kiểm kê trong thẩm quyền',
    permissions: {
      products: { view: true, add: false, edit: false, delete: false },
      inbound: { view: true, create: false, approve: true, pay: false },
      outbound: { view: true, create: false, approve: true, collect: false },
      warehouse: { view: true, audit: true, balance: true },
      reports: { view: true, export: false, inventoryOnly: true },
      system: { manageUsers: false, manageRoles: false, viewLogs: true }
    }
  },
  {
    roleId: 'NHANVIEN_KHO',
    roleName: 'Nhân Viên Nhập/Xuất Kho',
    desc: 'Lập phiếu nhập, quét Serial, lập đơn bán sỉ nháp, soạn/đóng gói đơn và xử lý xuất kho theo quy trình',
    permissions: {
      products: { view: true, add: false, edit: false, delete: false },
      inbound: { view: true, create: true, approve: false, pay: false },
      outbound: { view: true, create: true, approve: false, collect: false },
      warehouse: { view: true, audit: false, balance: false },
      reports: { view: true, export: false },
      system: { manageUsers: false, manageRoles: false, viewLogs: false }
    }
  },
  {
    roleId: 'KETOAN',
    roleName: 'Kế Toán',
    desc: 'Theo dõi công nợ 2 chiều NCC & Đại lý, lập Phiếu Thu/Chi, đối soát dòng tiền',
    permissions: {
      products: { view: true, add: false, edit: false, delete: false },
      inbound: { view: true, create: false, approve: false, pay: true },
      outbound: { view: true, create: false, approve: false, collect: true },
      warehouse: { view: true, audit: true, balance: false },
      reports: { view: true, export: true },
      system: { manageUsers: false, manageRoles: false, viewLogs: true }
    }
  },
  {
    roleId: 'OWNER',
    roleName: 'Chủ Cửa Hàng (Owner)',
    desc: 'Theo dõi Dashboard/báo cáo và phê duyệt ngoại lệ vượt ngưỡng về chi phí, tín dụng, kiểm kê',
    permissions: {
      products: { view: true, add: false, edit: false, delete: false },
      inbound: { view: true, create: false, approve: false, pay: false },
      outbound: { view: true, create: false, approve: false, collect: false },
      warehouse: { view: true, audit: false, balance: false },
      reports: { view: true, export: true },
      system: { manageUsers: false, manageRoles: false, viewLogs: true },
      exceptions: { approve: true }
    }
  }
];

// ==========================================
// SEED DATA 8: NHẬT KÝ AUDIT LOG (TV1.2 & TV5)
// ==========================================
const INITIAL_AUDIT_LOGS = [
  { time: 'Hôm nay 10:15', user: 'Nhân viên nhập/xuất kho (Nguyễn Phương)', action: 'TẠO_ĐƠN_SỈ', target: 'Đơn sỉ DS-2026-104 cho Đại lý Hoàng Kim (Khóa giữ chỗ)' },
  { time: 'Hôm nay 09:20', user: 'Kế toán (Phạm Thị Lan)', action: 'THU_TIỀN_SỈ', target: 'Lập phiếu thu PT-2026-001 thu 150.000.000đ từ Hoàng Kim Watch' },
  { time: 'Hôm nay 08:30', user: 'Thủ kho (Lê Tuấn)', action: 'KIỂM_KÊ_KHO', target: 'Hoàn tất kiểm kê Kệ A-01 (18/18 chiếc khớp 100%)' },
  { time: 'Hôm qua 16:30', user: 'Thủ kho (Lê Tuấn)', action: 'NHẬP_TRẢ_HÀNG', target: 'Tiếp nhận Tissot PRX lỗi hơi kính từ Hải Triều -> Kho Lỗi C-01' },
  { time: 'Hôm qua 14:10', user: 'Kế toán (Phạm Thị Lan)', action: 'CHI_TRẢ_NCC', target: 'Lập phiếu chi PC-2026-002 thanh toán 1.320.800.000đ cho Swatch Group' }
];

// ==========================================
// STORAGE ENGINE CHRONODB HOÀN CHỈNH
// ==========================================
class ChronoDB {
  static get(key, defaultValue) {
    try {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : defaultValue;
    } catch (e) {
      console.error('Error reading localStorage for key', key, e);
      return defaultValue;
    }
  }

  static set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.error('Error saving to localStorage for key', key, e);
    }
  }

  static init() {
    if (!localStorage.getItem(STORAGE_KEYS.WATCHES)) this.set(STORAGE_KEYS.WATCHES, INITIAL_WATCHES);
    if (!localStorage.getItem(STORAGE_KEYS.SERIALS)) this.set(STORAGE_KEYS.SERIALS, INITIAL_SERIALS);
    if (!localStorage.getItem(STORAGE_KEYS.SUPPLIERS)) this.set(STORAGE_KEYS.SUPPLIERS, INITIAL_SUPPLIERS);
    if (!localStorage.getItem(STORAGE_KEYS.DEALERS)) this.set(STORAGE_KEYS.DEALERS, INITIAL_DEALERS);
    if (!localStorage.getItem(STORAGE_KEYS.RECEIPTS)) this.set(STORAGE_KEYS.RECEIPTS, INITIAL_RECEIPTS);
    if (!localStorage.getItem(STORAGE_KEYS.ORDERS)) this.set(STORAGE_KEYS.ORDERS, INITIAL_ORDERS);
    if (!localStorage.getItem(STORAGE_KEYS.SHELVES)) this.set(STORAGE_KEYS.SHELVES, INITIAL_SHELVES);
    if (!localStorage.getItem(STORAGE_KEYS.AUDIT_LOGS)) this.set(STORAGE_KEYS.AUDIT_LOGS, INITIAL_AUDIT_LOGS);
    if (!localStorage.getItem(STORAGE_KEYS.ACCOUNTS)) this.set(STORAGE_KEYS.ACCOUNTS, INITIAL_ACCOUNTS);
    else {
      const accounts = this.get(STORAGE_KEYS.ACCOUNTS, INITIAL_ACCOUNTS);
      let accountsChanged = false;
      const roleNames = {
        ADMIN: 'Quản Trị Hệ Thống',
        KHO: 'Thủ Kho',
        NHANVIEN_KHO: 'Nhân Viên Nhập/Xuất Kho',
        KETOAN: 'Kế Toán',
        OWNER: 'Chủ Cửa Hàng'
      };
      accounts.forEach(account => {
        if (account.role === 'SALES') {
          account.role = 'NHANVIEN_KHO';
          accountsChanged = true;
        }
        if (roleNames[account.role] && account.roleName !== roleNames[account.role]) {
          account.roleName = roleNames[account.role];
          accountsChanged = true;
        }
      });
      if (!accounts.some(account => account.role === 'OWNER')) {
        accounts.push(INITIAL_ACCOUNTS.find(account => account.role === 'OWNER'));
        accountsChanged = true;
      }
      if (accountsChanged) this.set(STORAGE_KEYS.ACCOUNTS, accounts);
    }
    if (!localStorage.getItem(STORAGE_KEYS.ROLES)) this.set(STORAGE_KEYS.ROLES, INITIAL_ROLES);
    else {
      const roles = this.get(STORAGE_KEYS.ROLES, INITIAL_ROLES);
      const migratedRoles = [];
      roles.forEach(role => {
        const roleId = role.roleId === 'SALES' ? 'NHANVIEN_KHO' : role.roleId;
        if (migratedRoles.some(existing => existing.roleId === roleId)) return;
        const currentRole = INITIAL_ROLES.find(item => item.roleId === roleId);
        migratedRoles.push(currentRole ? { ...role, ...currentRole } : role);
      });
      INITIAL_ROLES.forEach(defaultRole => {
        if (!migratedRoles.some(role => role.roleId === defaultRole.roleId)) migratedRoles.push(defaultRole);
      });
      this.set(STORAGE_KEYS.ROLES, migratedRoles);
    }
    if (!localStorage.getItem(STORAGE_KEYS.SUPPLIER_PAYMENTS)) this.set(STORAGE_KEYS.SUPPLIER_PAYMENTS, INITIAL_SUPPLIER_PAYMENTS);
    if (!localStorage.getItem(STORAGE_KEYS.SUPPLIER_RETURNS)) this.set(STORAGE_KEYS.SUPPLIER_RETURNS, INITIAL_SUPPLIER_RETURNS);
    if (!localStorage.getItem(STORAGE_KEYS.DEALER_RECEIPTS)) this.set(STORAGE_KEYS.DEALER_RECEIPTS, INITIAL_DEALER_RECEIPTS);
    if (!localStorage.getItem(STORAGE_KEYS.CUSTOMER_RETURNS)) this.set(STORAGE_KEYS.CUSTOMER_RETURNS, INITIAL_CUSTOMER_RETURNS);
    if (!localStorage.getItem(STORAGE_KEYS.OTHER_DISPATCHES)) this.set(STORAGE_KEYS.OTHER_DISPATCHES, INITIAL_OTHER_DISPATCHES);
    if (!localStorage.getItem(STORAGE_KEYS.STOCK_AUDITS)) this.set(STORAGE_KEYS.STOCK_AUDITS, INITIAL_STOCK_AUDITS);
    if (!localStorage.getItem(STORAGE_KEYS.STOCK_CARDS)) this.set(STORAGE_KEYS.STOCK_CARDS, INITIAL_STOCK_CARDS);
  }

  // --- Products (TV1) ---
  static getWatches() { return this.get(STORAGE_KEYS.WATCHES, INITIAL_WATCHES); }
  static setWatches(watches) { this.set(STORAGE_KEYS.WATCHES, watches); }
  static getWatchById(id) { return this.getWatches().find(w => w.id === id); }
  static saveWatch(watch) {
    const list = this.getWatches();
    const idx = list.findIndex(w => w.id === watch.id || w.sku === watch.sku);
    if (idx >= 0) {
      list[idx] = { ...list[idx], ...watch };
    } else {
      list.unshift(watch);
    }
    this.setWatches(list);
  }
  static deleteWatch(watchId) {
    const list = this.getWatches().filter(w => w.id !== watchId);
    this.setWatches(list);
  }

  // --- Serials (TV1 & TV4) ---
  static getSerials() { return this.get(STORAGE_KEYS.SERIALS, INITIAL_SERIALS); }
  static setSerials(serials) { this.set(STORAGE_KEYS.SERIALS, serials); }
  static getSerial(serialNumber) {
    return this.getSerials().find(s => s.serialNumber.toLowerCase() === (serialNumber || '').trim().toLowerCase());
  }
  static saveSerial(serialObj) {
    const list = this.getSerials();
    const idx = list.findIndex(s => s.serialNumber === serialObj.serialNumber);
    if (idx >= 0) {
      list[idx] = { ...list[idx], ...serialObj };
    } else {
      list.push(serialObj);
    }
    this.setSerials(list);
  }

  // --- Suppliers (TV2) ---
  static getSuppliers() { return this.get(STORAGE_KEYS.SUPPLIERS, INITIAL_SUPPLIERS); }
  static setSuppliers(suppliers) { this.set(STORAGE_KEYS.SUPPLIERS, suppliers); }
  static getSupplierById(id) { return this.getSuppliers().find(s => s.id === id); }
  static saveSupplier(supp) {
    const list = this.getSuppliers();
    const idx = list.findIndex(s => s.id === supp.id);
    if (idx >= 0) list[idx] = { ...list[idx], ...supp };
    else list.push(supp);
    this.setSuppliers(list);
  }

  // --- Supplier Payments (TV2) ---
  static getSupplierPayments() { return this.get(STORAGE_KEYS.SUPPLIER_PAYMENTS, INITIAL_SUPPLIER_PAYMENTS); }
  static addSupplierPayment(pay) {
    const list = this.getSupplierPayments();
    list.unshift(pay);
    this.set(STORAGE_KEYS.SUPPLIER_PAYMENTS, list);
    // Cập nhật giảm trừ nợ NCC
    const suppliers = this.getSuppliers();
    const supp = suppliers.find(s => s.id === pay.supplierId);
    if (supp) {
      supp.debtBalance = Math.max(0, (supp.debtBalance || 0) - Number(pay.amount));
      this.setSuppliers(suppliers);
    }
    this.logAction(pay.createdBy || 'Kế toán', 'CHI_TRẢ_NCC', `Lập phiếu chi ${pay.id} cho ${pay.supplierName}: ${formatShortVND(pay.amount)}`);
  }

  // --- Supplier Defect Returns (TV2) ---
  static getSupplierReturns() { return this.get(STORAGE_KEYS.SUPPLIER_RETURNS, INITIAL_SUPPLIER_RETURNS); }
  static addSupplierReturn(ret) {
    const list = this.getSupplierReturns();
    list.unshift(ret);
    this.set(STORAGE_KEYS.SUPPLIER_RETURNS, list);
    // Giảm trừ nợ NCC
    const suppliers = this.getSuppliers();
    const supp = suppliers.find(s => s.id === ret.supplierId);
    if (supp) {
      supp.debtBalance = Math.max(0, (supp.debtBalance || 0) - Number(ret.refundValue));
      this.setSuppliers(suppliers);
    }
    this.logAction(ret.createdBy || 'Thủ kho', 'TRẢ_HÀNG_NCC', `Phiếu xuất trả lỗi ${ret.id} cho ${ret.supplierName} (-${formatShortVND(ret.refundValue)})`);
  }

  // --- Receipts (TV2) ---
  static getReceipts() { return this.get(STORAGE_KEYS.RECEIPTS, INITIAL_RECEIPTS); }
  static setReceipts(receipts) { this.set(STORAGE_KEYS.RECEIPTS, receipts); }
  static addReceipt(rec) {
    const list = this.getReceipts();
    list.unshift(rec);
    this.setReceipts(list);
  }

  // --- Dealers (TV3) ---
  static getDealers() { return this.get(STORAGE_KEYS.DEALERS, INITIAL_DEALERS); }
  static setDealers(dealers) { this.set(STORAGE_KEYS.DEALERS, dealers); }
  static getDealerById(id) { return this.getDealers().find(d => d.id === id); }
  static saveDealer(dealer) {
    const list = this.getDealers();
    const idx = list.findIndex(d => d.id === dealer.id);
    if (idx >= 0) list[idx] = { ...list[idx], ...dealer };
    else list.push(dealer);
    this.setDealers(list);
  }

  // --- Wholesale Orders (TV3) ---
  static getOrders() { return this.get(STORAGE_KEYS.ORDERS, INITIAL_ORDERS); }
  static setOrders(orders) { this.set(STORAGE_KEYS.ORDERS, orders); }
  static addOrder(order) {
    const list = this.getOrders();
    list.unshift(order);
    this.setOrders(list);
  }

  // --- Dealer Receipts (Thu tiền sỉ TV3) ---
  static getDealerReceipts() { return this.get(STORAGE_KEYS.DEALER_RECEIPTS, INITIAL_DEALER_RECEIPTS); }
  static addDealerReceipt(rcpt) {
    const list = this.getDealerReceipts();
    list.unshift(rcpt);
    this.set(STORAGE_KEYS.DEALER_RECEIPTS, list);
    // Giảm nợ đại lý & khôi phục hạn mức
    const dealers = this.getDealers();
    const dealer = dealers.find(d => d.id === rcpt.dealerId);
    if (dealer) {
      dealer.currentDebt = Math.max(0, (dealer.currentDebt || 0) - Number(rcpt.amount));
      dealer.availableCredit = Math.min(dealer.creditLimit, (dealer.creditLimit - dealer.currentDebt));
      this.setDealers(dealers);
    }
    this.logAction(rcpt.createdBy || 'Kế toán', 'THU_TIỀN_SỈ', `Lập phiếu thu ${rcpt.id} từ ${rcpt.dealerName}: ${formatShortVND(rcpt.amount)}`);
  }

  // --- Customer Returns (Đổi trả sỉ TV3) ---
  static getCustomerReturns() { return this.get(STORAGE_KEYS.CUSTOMER_RETURNS, INITIAL_CUSTOMER_RETURNS); }
  static addCustomerReturn(ret) {
    const list = this.getCustomerReturns();
    list.unshift(ret);
    this.set(STORAGE_KEYS.CUSTOMER_RETURNS, list);
  }

  // --- Other Dispatches (Xuất bảo hành / Hủy TV3) ---
  static getOtherDispatches() { return this.get(STORAGE_KEYS.OTHER_DISPATCHES, INITIAL_OTHER_DISPATCHES); }
  static addOtherDispatch(disp) {
    const list = this.getOtherDispatches();
    list.unshift(disp);
    this.set(STORAGE_KEYS.OTHER_DISPATCHES, list);
  }

  // --- Warehouse Shelves & Stock (TV4) ---
  static getShelves() { return this.get(STORAGE_KEYS.SHELVES, INITIAL_SHELVES); }
  static setShelves(shelves) { this.set(STORAGE_KEYS.SHELVES, shelves); }
  static getStockAudits() { return this.get(STORAGE_KEYS.STOCK_AUDITS, INITIAL_STOCK_AUDITS); }
  static addStockAudit(audit) {
    const list = this.getStockAudits();
    list.unshift(audit);
    this.set(STORAGE_KEYS.STOCK_AUDITS, list);
  }
  static getStockCards() { return this.get(STORAGE_KEYS.STOCK_CARDS, INITIAL_STOCK_CARDS); }
  static addStockCard(card) {
    const list = this.getStockCards();
    list.unshift(card);
    this.set(STORAGE_KEYS.STOCK_CARDS, list);
  }

  // --- System Accounts & Roles (TV1.2) ---
  static getAccounts() { return this.get(STORAGE_KEYS.ACCOUNTS, INITIAL_ACCOUNTS); }
  static setAccounts(accs) { this.set(STORAGE_KEYS.ACCOUNTS, accs); }
  static saveAccount(acc) {
    const list = this.getAccounts();
    const idx = list.findIndex(a => a.id === acc.id || a.username === acc.username);
    if (idx >= 0) list[idx] = { ...list[idx], ...acc };
    else list.push(acc);
    this.setAccounts(list);
  }
  static getRoles() { return this.get(STORAGE_KEYS.ROLES, INITIAL_ROLES); }
  static setRoles(roles) { this.set(STORAGE_KEYS.ROLES, roles); }

  // --- Logs & Audit Trail ---
  static getLogs() { return this.get(STORAGE_KEYS.AUDIT_LOGS, INITIAL_AUDIT_LOGS); }
  static logAction(user, action, target) {
    const logs = this.getLogs();
    const now = new Date();
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')} Hôm nay`;
    logs.unshift({ time: timeStr, user, action, target });
    this.set(STORAGE_KEYS.AUDIT_LOGS, logs.slice(0, 100));
  }
}

// ==========================================
// UTILITY FORMATTERS
// ==========================================
function formatVND(amount) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount || 0);
}

function formatShortVND(amount) {
  const num = Number(amount) || 0;
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(2).replace(/\.00$/, '') + ' tỷ';
  }
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace(/\.0$/, '') + ' triệu';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(0) + ' k';
  }
  return num.toString();
}

// Khởi tạo Database ngay khi file nạp
ChronoDB.init();
