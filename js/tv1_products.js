/**
 * CHRONO VAULT B2B - PHÂN HỆ 1.1 (THÀNH VIÊN 1)
 * Quản lý Hàng hóa, Thương hiệu, Thông số kỹ thuật & Vòng đời Serial
 */

// Filter state
let currentBrandFilter = 'ALL';
let currentSearchQuery = '';

// Render Products List
function renderProductsList(brand = null, search = null) {
  if (brand !== null) currentBrandFilter = brand;
  if (search !== null) currentSearchQuery = search.toLowerCase().trim();

  const container = document.getElementById('productsListContainer');
  if (!container) return;

  const watches = ChronoDB.getWatches();
  const serials = ChronoDB.getSerials();

  const filtered = watches.filter(w => {
    const matchBrand = (currentBrandFilter === 'ALL' || w.brand.toLowerCase() === currentBrandFilter.toLowerCase());
    const matchSearch = (!currentSearchQuery || 
      w.name.toLowerCase().includes(currentSearchQuery) || 
      w.sku.toLowerCase().includes(currentSearchQuery) ||
      w.barcode.includes(currentSearchQuery) ||
      w.brand.toLowerCase().includes(currentSearchQuery)
    );
    return matchBrand && matchSearch;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:32px 16px; color:var(--text-muted); background:var(--bg-card); border-radius:12px; border:1px dashed var(--border-subtle);">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:8px; opacity:0.6;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <div style="font-weight:600; font-size:14px;">Không tìm thấy đồng hồ phù hợp</div>
        <div style="font-size:12px; margin-top:4px;">Thử thay đổi từ khóa hoặc bộ lọc thương hiệu</div>
      </div>
    `;
    return;
  }

  let html = `<div class="products-grid-list">`;
  filtered.forEach(watch => {
    // Đếm tồn kho thực tế và khả dụng theo Serial
    const watchSerials = serials.filter(s => s.sku === watch.sku || s.watchId === watch.id);
    const inStockCount = watchSerials.filter(s => s.status === 'IN_STOCK').length;
    const reservedCount = watchSerials.filter(s => s.status === 'RESERVED').length;
    
    // Quy đổi đa đơn vị: vd 2 Thùng + 4 Chiếc
    const boxes = Math.floor(inStockCount / watch.conversionRate);
    const remainderPieces = inStockCount % watch.conversionRate;
    const unitText = boxes > 0 
      ? `<b>${boxes}</b> ${watch.wholesaleUnit} + <b>${remainderPieces}</b> ${watch.baseUnit}`
      : `<b>${inStockCount}</b> ${watch.baseUnit}`;

    // Cảnh báo tồn kho Min/Max
    let stockBadge = `<span class="badge-status status-completed">Khả dụng: ${inStockCount} ${watch.baseUnit}</span>`;
    if (inStockCount === 0) {
      stockBadge = `<span class="badge-status status-danger">HẾT HÀNG</span>`;
    } else if (inStockCount <= watch.minStock) {
      stockBadge = `<span class="badge-status status-warning">SẮP HẾT (≤ ${watch.minStock})</span>`;
    }

    html += `
      <div class="watch-product-card" id="card-${watch.id}">
        <div class="watch-card-top">
          <div class="watch-brand-pill">${watch.brand}</div>
          ${stockBadge}
        </div>
        
        <div class="watch-card-body">
          <div class="watch-visual-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <circle cx="12" cy="12" r="7"/>
              <polyline points="12 9 12 12 13.5 13.5"/>
              <path d="M16.51 17.35l-.85 3.83a2 2 0 0 1-2 1.82H10.34a2 2 0 0 1-2-1.82l-.85-3.83"/>
              <path d="M7.49 6.65l.85-3.83a2 2 0 0 1 2-1.82h3.32a2 2 0 0 1 2 1.82l.85 3.83"/>
            </svg>
          </div>
          <div class="watch-info-wrap">
            <h4 class="watch-title" onclick="openWatchDetailModal('${watch.id}')">${watch.name}</h4>
            <div class="watch-sku-barcode">
              <span>SKU: <b>${watch.sku}</b></span> • <span>EAN: <b>${watch.barcode}</b></span>
            </div>
            <div class="watch-spec-summary">
              <span>⚙️ ${watch.movement}</span>
              <span>🛡️ ${watch.glass}</span>
              <span>💧 ${watch.waterResist}</span>
            </div>
          </div>
        </div>

        <div class="watch-pricing-matrix">
          <div class="price-col">
            <span class="price-lbl">Giá Vốn Đích Danh:</span>
            <span class="price-val cost">${formatVND(watch.baseCost)}</span>
          </div>
          <div class="price-col">
            <span class="price-lbl">Giá Sỉ VIP (MOQ ${watch.moq}):</span>
            <span class="price-val wholesale">${formatVND(watch.wholesalePriceVip)}</span>
          </div>
        </div>

        <div class="watch-stock-conversion">
          <div class="conversion-text">
            📦 Quy cách sỉ: 1 ${watch.wholesaleUnit} = ${watch.conversionRate} ${watch.baseUnit} | Tồn: ${unitText} (Giữ chỗ: ${reservedCount})
          </div>
        </div>

        <div class="watch-card-actions">
          <button class="btn-action-small" onclick="openWatchDetailModal('${watch.id}')">
            🔍 Xem Chi Tiết
          </button>
          <button class="btn-action-small" onclick="openEditWatchModal('${watch.id}')">
            ✏️ Sửa
          </button>
          <button class="btn-action-small primary" onclick="openCreateOrderWithWatch('${watch.id}')">
            + Lên Đơn Sỉ
          </button>
        </div>
      </div>
    `;
  });
  html += `</div>`;
  container.innerHTML = html;
}

// Set Brand Filter Pill
function setBrandFilter(brand, btn) {
  document.querySelectorAll('.filter-tags-scroll .tag-pill').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderProductsList(brand, null);
}

// Open Watch Detail Modal
function openWatchDetailModal(watchId) {
  const watch = ChronoDB.getWatchById(watchId);
  if (!watch) return;

  const serials = ChronoDB.getSerials().filter(s => s.sku === watch.sku || s.watchId === watch.id);
  const inStockSerials = serials.filter(s => s.status === 'IN_STOCK');
  const reservedSerials = serials.filter(s => s.status === 'RESERVED');
  const soldSerials = serials.filter(s => s.status === 'SOLD');
  const defectSerials = serials.filter(s => s.status === 'DEFECT');

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `
    <span style="color:var(--gold-primary);">[${watch.brand}]</span> ${watch.name}
  `;

  bodyElem.innerHTML = `
    <div class="modal-detail-wrap">
      <!-- Highlight Meta -->
      <div class="detail-kpi-bar">
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Mã SKU Quản Trị</span>
          <span class="kpi-mini-val">${watch.sku}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Mã Vạch Toàn Cầu</span>
          <span class="kpi-mini-val">${watch.barcode}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Tồn Kho Vật Lý</span>
          <span class="kpi-mini-val" style="color:var(--gold-light);">${inStockSerials.length} ${watch.baseUnit}</span>
        </div>
      </div>

      <!-- Technical Specifications Table (TV1.1) -->
      <div class="section-subtitle">⚙️ BẢNG THÔNG SỐ KỸ THUẬT CHÍNH HÃNG</div>
      <table class="data-table-spec">
        <tr><td>Bộ máy chuyển động (Movement):</td><td><b>${watch.movement}</b></td></tr>
        <tr><td>Mặt kính bảo vệ (Glass):</td><td><b>${watch.glass}</b></td></tr>
        <tr><td>Chất liệu vỏ & dây đeo:</td><td><b>${watch.strap}</b></td></tr>
        <tr><td>Đường kính mặt số (Dial Size):</td><td><b>${watch.dialSize}</b></td></tr>
        <tr><td>Độ chịu nước (Water Resistance):</td><td><b>${watch.waterResist}</b></td></tr>
        <tr><td>Thời hạn bảo hành điện tử:</td><td><b>${watch.warranty}</b></td></tr>
        <tr><td>Cơ chế định danh vật lý:</td><td><b style="color:var(--success);">Quản lý 100% theo Serial / IMEI</b></td></tr>
      </table>

      <!-- Packaging and B2B Pricing Matrix -->
      <div class="section-subtitle" style="margin-top:16px;">💼 CHÍNH SÁCH XUẤT KHO ĐẠI LÝ & QUY CÁCH ĐÓNG GÓI</div>
      <table class="data-table-spec">
        <tr><td>Quy đổi ĐVT đóng gói:</td><td>1 ${watch.wholesaleUnit} = <b>${watch.conversionRate} ${watch.baseUnit}</b></td></tr>
        <tr><td>Số lượng đặt tối thiểu (MOQ):</td><td><b>${watch.moq} ${watch.baseUnit}</b></td></tr>
        <tr><td>Phương pháp tính giá vốn:</td><td><b style="color:var(--gold-light);">${watch.costPriceMethod}</b></td></tr>
        <tr><td>Giá vốn bình quân tham chiếu:</td><td><b>${formatVND(watch.baseCost)}</b></td></tr>
        <tr><td>Giá phân phối đại lý Đại lý Hạng VIP:</td><td><b style="color:var(--success);">${formatVND(watch.wholesalePriceVip)}</b></td></tr>
        <tr><td>Giá phân phối đại lý Đại lý Hạng Bạc:</td><td><b>${formatVND(watch.wholesalePriceSilver)}</b></td></tr>
        <tr><td>Giá phân phối đại lý Đại lý Hạng Đồng:</td><td><b>${formatVND(watch.wholesalePriceBronze)}</b></td></tr>
        <tr><td>Định mức tồn an toàn (Min - Max):</td><td><b>${watch.minStock} - ${watch.maxStock} ${watch.baseUnit}</b></td></tr>
      </table>

      <!-- Serials Breakdown -->
      <div class="section-subtitle" style="margin-top:16px;">
        🏷️ DANH SÁCH SERIAL ĐANG TRONG KHO (${inStockSerials.length} chiếc)
      </div>
      <div class="serials-tag-cloud">
        ${inStockSerials.map(s => `
          <div class="serial-chip" onclick="lookupSerial('${s.serialNumber}')">
            <span>${s.serialNumber}</span>
            <small>${s.shelfLocation || 'Chưa xếp kệ'}</small>
          </div>
        `).join('') || '<div style="color:var(--text-muted); font-size:12px;">Không có mã Serial nào trong kho</div>'}
      </div>

      <div style="display:flex; gap:10px; margin-top:20px;">
        <button class="btn-primary-action" onclick="closeModal('generalDetailModal'); openCreateOrderWithWatch('${watch.id}')">
          + Lên Đơn Sỉ Mẫu Này
        </button>
        <button class="btn-secondary-action" onclick="closeModal('generalDetailModal'); openEditWatchModal('${watch.id}')">
          ✏️ Chỉnh Sửa Sản Phẩm
        </button>
      </div>
    </div>
  `;

  document.getElementById('generalDetailModal').classList.add('active');
}

// Open Modal Add Watch (TV1.1)
function openAddWatchModal() {
  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `➕ Thêm Mới Đồng Hồ Phân Phối B2B`;
  bodyElem.innerHTML = `
    <form id="addWatchForm" onsubmit="event.preventDefault(); submitSaveWatch(null);">
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Thương Hiệu</label>
          <select class="form-select" id="formBrand" required>
            <option value="Rolex">Rolex</option>
            <option value="Omega">Omega</option>
            <option value="Tissot">Tissot</option>
            <option value="Seiko">Seiko</option>
            <option value="Casio">Casio</option>
            <option value="Citizen">Citizen</option>
            <option value="Longines">Longines</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Phân Loại / Danh Mục</label>
          <input type="text" id="formCategory" class="form-input" placeholder="VD: Thể thao sang trọng" required value="Đồng hồ cao cấp">
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Tên Thương Mại Đầy Đủ</label>
        <input type="text" id="formName" class="form-input" placeholder="VD: Rolex GMT-Master II Batman" required>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Mã SKU Nội Bộ</label>
          <input type="text" id="formSku" class="form-input" placeholder="VD: RLX-GMT-126710BLNR" required style="font-family:monospace;">
        </div>
        <div class="form-group">
          <label class="form-label">Mã Vạch Toàn Cầu (EAN-13)</label>
          <input type="text" id="formBarcode" class="form-input" placeholder="VD: 7613297299011" required style="font-family:monospace;">
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Bộ Máy (Movement)</label>
          <input type="text" id="formMovement" class="form-input" value="Cơ Automatic Calibre Thụy Sỹ">
        </div>
        <div class="form-group">
          <label class="form-label">Mặt Kính</label>
          <input type="text" id="formGlass" class="form-input" value="Sapphire nguyên khối chống trầy">
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Chất Liệu Dây Vỏ</label>
          <input type="text" id="formStrap" class="form-input" value="Thép không gỉ 316L / 904L">
        </div>
        <div class="form-group">
          <label class="form-label">Size Mặt & Chịu Nước</label>
          <input type="text" id="formDialSize" class="form-input" value="40mm - 10 ATM (100m)">
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">ĐVT Xuất Kho Đại Lý</label>
          <select class="form-select" id="formWholesaleUnit">
            <option value="Thùng">Thùng</option>
            <option value="Kiện">Kiện</option>
            <option value="Lô">Lô</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Tỷ Lệ Quy Đổi (1 Sỉ = ? Chiếc)</label>
          <input type="number" id="formConversionRate" class="form-input" value="10" min="1" required>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Giá Vốn Dự Kiến (VNĐ)</label>
          <input type="number" id="formBaseCost" class="form-input" value="50000000" step="500000" required>
        </div>
        <div class="form-group">
          <label class="form-label">Giá Sỉ Đại Lý VIP (VNĐ)</label>
          <input type="number" id="formPriceVip" class="form-input" value="62000000" step="500000" required>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Số Lượng Đặt Tối Thiểu (MOQ)</label>
          <input type="number" id="formMoq" class="form-input" value="2" min="1" required>
        </div>
        <div class="form-group">
          <label class="form-label">Tồn Min - Tồn Max An Toàn</label>
          <div style="display:flex; gap:6px;">
            <input type="number" id="formMinStock" class="form-input" value="3" placeholder="Min" title="Tồn Min">
            <input type="number" id="formMaxStock" class="form-input" value="30" placeholder="Max" title="Tồn Max">
          </div>
        </div>
      </div>

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button type="submit" class="btn-primary-action">✓ Lưu Mới Sản Phẩm</button>
        <button type="button" class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Hủy</button>
      </div>
    </form>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Open Modal Edit Watch (TV1.1)
function openEditWatchModal(watchId) {
  const watch = ChronoDB.getWatchById(watchId);
  if (!watch) return;

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `✏️ Cập Nhật Đồng Hồ: ${watch.sku}`;
  bodyElem.innerHTML = `
    <form id="editWatchForm" onsubmit="event.preventDefault(); submitSaveWatch('${watch.id}');">
      <div class="form-group">
        <label class="form-label">Tên Đồng Hồ</label>
        <input type="text" id="formName" class="form-input" value="${watch.name}" required>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Hãng Sản Xuất</label>
          <input type="text" id="formBrand" class="form-input" value="${watch.brand}" required>
        </div>
        <div class="form-group">
          <label class="form-label">Mã SKU</label>
          <input type="text" id="formSku" class="form-input" value="${watch.sku}" readonly style="background:rgba(255,255,255,0.05); font-family:monospace;">
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">ĐVT Xuất Kho Đại Lý</label>
          <input type="text" id="formWholesaleUnit" class="form-input" value="${watch.wholesaleUnit}">
        </div>
        <div class="form-group">
          <label class="form-label">Hệ Số Quy Đổi Sỉ -> Chiếc</label>
          <input type="number" id="formConversionRate" class="form-input" value="${watch.conversionRate}" min="1" required>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Giá Vốn Dự Kiến (VNĐ)</label>
          <input type="number" id="formBaseCost" class="form-input" value="${watch.baseCost}" required>
        </div>
        <div class="form-group">
          <label class="form-label">Giá Sỉ VIP (VNĐ)</label>
          <input type="number" id="formPriceVip" class="form-input" value="${watch.wholesalePriceVip}" required>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Giá Sỉ Hạng Bạc (VNĐ)</label>
          <input type="number" id="formPriceSilver" class="form-input" value="${watch.wholesalePriceSilver}">
        </div>
        <div class="form-group">
          <label class="form-label">Giá Sỉ Hạng Đồng (VNĐ)</label>
          <input type="number" id="formPriceBronze" class="form-input" value="${watch.wholesalePriceBronze}">
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Số Lượng Đặt Tối Thiểu (MOQ)</label>
          <input type="number" id="formMoq" class="form-input" value="${watch.moq}" min="1">
        </div>
        <div class="form-group">
          <label class="form-label">Định Mức Tồn (Min - Max)</label>
          <div style="display:flex; gap:6px;">
            <input type="number" id="formMinStock" class="form-input" value="${watch.minStock}">
            <input type="number" id="formMaxStock" class="form-input" value="${watch.maxStock}">
          </div>
        </div>
      </div>

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button type="submit" class="btn-primary-action">✓ Cập Nhật Thay Đổi</button>
        <button type="button" class="btn-danger-action" onclick="confirmDeleteWatch('${watch.id}')">🗑️ Ngừng Kinh Doanh / Xóa</button>
      </div>
    </form>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Submit Save Watch (Create or Update)
function submitSaveWatch(existingId) {
  const name = document.getElementById('formName').value.trim();
  const brand = document.getElementById('formBrand').value.trim();
  const sku = document.getElementById('formSku').value.trim().toUpperCase();
  const conversionRate = Number(document.getElementById('formConversionRate').value) || 10;
  const wholesaleUnit = document.getElementById('formWholesaleUnit').value.trim() || 'Thùng';
  const baseCost = Number(document.getElementById('formBaseCost').value) || 0;
  const priceVip = Number(document.getElementById('formPriceVip').value) || 0;
  const moq = Number(document.getElementById('formMoq').value) || 1;
  const minStock = Number(document.getElementById('formMinStock').value) || 5;
  const maxStock = Number(document.getElementById('formMaxStock').value) || 50;

  if (existingId) {
    const watch = ChronoDB.getWatchById(existingId);
    if (!watch) return;
    watch.name = name;
    watch.brand = brand;
    watch.conversionRate = conversionRate;
    watch.wholesaleUnit = wholesaleUnit;
    watch.baseCost = baseCost;
    watch.wholesalePriceVip = priceVip;
    watch.wholesalePriceSilver = Number(document.getElementById('formPriceSilver')?.value) || Math.round(priceVip * 1.05);
    watch.wholesalePriceBronze = Number(document.getElementById('formPriceBronze')?.value) || Math.round(priceVip * 1.1);
    watch.moq = moq;
    watch.minStock = minStock;
    watch.maxStock = maxStock;
    ChronoDB.saveWatch(watch);
    ChronoDB.logAction('Thành viên 1', 'CẬP_NHẬT_SP', `Chỉnh sửa thông số đồng hồ: ${watch.sku} - ${watch.name}`);
    showToast(`Đã cập nhật thông tin đồng hồ ${watch.sku}`, 'success');
  } else {
    const barcode = document.getElementById('formBarcode').value.trim() || Date.now().toString().slice(-13);
    const category = document.getElementById('formCategory')?.value || 'Đồng hồ cao cấp';
    const movement = document.getElementById('formMovement')?.value || 'Cơ Automatic';
    const glass = document.getElementById('formGlass')?.value || 'Sapphire';
    const strap = document.getElementById('formStrap')?.value || 'Thép không gỉ';
    const dialSize = document.getElementById('formDialSize')?.value || '41mm';

    const newId = 'W' + (ChronoDB.getWatches().length + 1).toString().padStart(3, '0');
    const newWatch = {
      id: newId,
      sku,
      barcode,
      name,
      brand,
      category,
      movement,
      glass,
      strap,
      dialSize,
      waterResist: '10 ATM (100m)',
      warranty: '3 năm chính hãng',
      hasSerial: true,
      baseUnit: 'Chiếc',
      wholesaleUnit,
      conversionRate,
      costPriceMethod: 'Đích danh theo Serial',
      baseCost,
      wholesalePriceVip: priceVip,
      wholesalePriceSilver: Math.round(priceVip * 1.05),
      wholesalePriceBronze: Math.round(priceVip * 1.1),
      moq,
      minStock,
      maxStock,
      shelfId: 'B-01',
      status: 'ACTIVE'
    };
    ChronoDB.saveWatch(newWatch);
    ChronoDB.logAction('Thành viên 1', 'THÊM_MỚI_SP', `Khai báo mẫu đồng hồ mới: ${sku} (${brand})`);
    showToast(`Đã thêm mới thành công đồng hồ ${sku}!`, 'success');
  }

  closeModal('generalDetailModal');
  renderProductsList();
  if (typeof renderWarehouseTab === 'function') renderWarehouseTab();
}

// Delete Watch
function confirmDeleteWatch(watchId) {
  const watch = ChronoDB.getWatchById(watchId);
  if (!watch) return;
  if (confirm(`Bạn có chắc muốn xóa hoặc ngừng kinh doanh mẫu đồng hồ [${watch.sku}] ${watch.name}?`)) {
    ChronoDB.deleteWatch(watchId);
    ChronoDB.logAction('Thành viên 1', 'XÓA_SẢN_PHẨM', `Ngừng kinh doanh mẫu: ${watch.sku}`);
    showToast(`Đã xóa sản phẩm ${watch.sku}`, 'info');
    closeModal('generalDetailModal');
    renderProductsList();
  }
}

// Export Products to CSV / Excel (TV1.1)
function exportProductsToCSV() {
  const watches = ChronoDB.getWatches();
  let csv = "ID,SKU,Barcode,Thương Hiệu,Tên Đồng Hồ,Loại Máy,ĐVT Cơ Bản,ĐVT Sỉ,Quy Đổi,Giá Vốn,Giá Sỉ VIP,MOQ,Min Tồn,Max Tồn\n";
  watches.forEach(w => {
    csv += `"${w.id}","${w.sku}","${w.barcode}","${w.brand}","${w.name}","${w.movement}","${w.baseUnit}","${w.wholesaleUnit}",${w.conversionRate},${w.baseCost},${w.wholesalePriceVip},${w.moq},${w.minStock},${w.maxStock}\n`;
  });
  
  const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Danh_Muc_Dong_Ho_ChronoVault_${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  showToast('Đã xuất danh mục sản phẩm ra file CSV thành công!', 'success');
}

// Lookup Serial Number Lifecycle Timeline (TV1.1 & TV4)
function lookupSerial(serialCode = null) {
  const inputCode = serialCode || document.getElementById('serialSearchInput')?.value?.trim();
  if (!inputCode) {
    if (typeof showToast === 'function') showToast('Vui lòng nhập hoặc quét mã Serial', 'warning');
    return;
  }

  const resultContainer = document.getElementById('serialLookupResult');
  const serial = ChronoDB.getSerial(inputCode);

  if (!serial) {
    if (typeof showToast === 'function') showToast(`Không tìm thấy mã Serial: ${inputCode}`, 'warning');
    if (resultContainer) {
      resultContainer.style.display = 'block';
      resultContainer.innerHTML = `
        <div class="serial-not-found">
          ⚠️ Không tìm thấy mã Serial <b>${inputCode}</b> trong toàn bộ cơ sở dữ liệu kho.
        </div>
      `;
    }
    return;
  }

  if (resultContainer) {
    let statusLabel = '<span class="badge-status status-completed">Trong Kho</span>';
    if (serial.status === 'RESERVED') statusLabel = '<span class="badge-status status-warning">Đã Khóa Giữ Chỗ</span>';
    else if (serial.status === 'SOLD') statusLabel = '<span class="badge-status status-sold">Đã Xuất Xuất Kho Đại Lý</span>';
    else if (serial.status === 'DEFECT') statusLabel = '<span class="badge-status status-danger">Kho Hàng Lỗi</span>';
    else if (serial.status === 'RETURNED_SUPPLIER') statusLabel = '<span class="badge-status status-danger">Đã Xuất Trả NCC</span>';

    let qualityBadge = '<span class="badge-status status-completed">Hàng Mới Seal</span>';
    if (serial.qualityType === 'DISPLAY') qualityBadge = '<span class="badge-status status-warning">Hàng Trưng Bày</span>';
    else if (serial.qualityType === 'DEFECT') qualityBadge = '<span class="badge-status status-danger">Hàng Lỗi Kỹ Thuật</span>';

    resultContainer.style.display = 'block';
    resultContainer.innerHTML = `
      <div class="serial-result-card">
        <div class="result-header">
          <div>
            <div style="font-size:11px; color:var(--text-muted);">MÃ SERIAL ĐÍCH DANH</div>
            <div class="result-serial-code">${serial.serialNumber}</div>
          </div>
          <div style="text-align:right;">
            ${statusLabel}
            <div style="margin-top:4px;">${qualityBadge}</div>
          </div>
        </div>

        <div class="result-meta-grid">
          <div><span>Sản phẩm:</span> <b>${serial.watchName}</b></div>
          <div><span>Mã SKU:</span> <b>${serial.sku}</b></div>
          <div><span>Giá vốn đích danh:</span> <b style="color:var(--gold-light);">${formatVND(serial.costPrice)}</b></div>
          <div><span>Vị trí kệ:</span> <b>${serial.shelfLocation || 'N/A'}</b></div>
          <div><span>Ngày nhập kho:</span> <b>${serial.receivedDate || 'N/A'}</b></div>
          <div><span>Hạn bảo hành:</span> <b>${serial.warrantyExpire || 'N/A'}</b></div>
        </div>

        <div class="timeline-title">📜 VÒNG ĐỜI & LỊCH SỬ TRUY VẾT SERIAL</div>
        <div class="timeline-stepper">
          ${(serial.timeline || []).map((t, idx) => `
            <div class="timeline-step-item">
              <div class="step-dot"></div>
              <div class="step-content">
                <div class="step-time">${t.date}</div>
                <div class="step-heading">${t.title}</div>
                <div class="step-desc">${t.desc}</div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  if (typeof playBeep === 'function') playBeep(1600, 'sine', 0.1);
  if (typeof flashDynamicIsland === 'function') flashDynamicIsland(`Khớp Serial: ${serial.serialNumber}`);
}
