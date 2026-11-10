/**
 * CHRONO VAULT B2B - PHÂN HỆ 4 (THÀNH VIÊN 4)
 * Tồn Kho Đa Trạng Thái, Vị Trí Kệ Vật Lý, Kiểm Kê Cân Bằng & Thẻ Kho (Stock Card)
 */

let currentWarehouseQualityFilter = 'ALL'; // ALL, NEW, DISPLAY, DEFECT

// Render Warehouse Tab
function renderWarehouseTab(filter = null) {
  if (filter !== null) currentWarehouseQualityFilter = filter;

  const shelvesContainer = document.getElementById('shelvesVisualGrid');
  const multiUnitContainer = document.getElementById('multiUnitStockSummary');

  const watches = ChronoDB.getWatches();
  const serials = ChronoDB.getSerials();
  const shelves = ChronoDB.getShelves();

  // 1. Cập nhật số đếm trên 3 nút trạng thái
  const countNew = serials.filter(s => s.status === 'IN_STOCK' && s.qualityType === 'NEW').length;
  const countDisplay = serials.filter(s => s.status === 'IN_STOCK' && s.qualityType === 'DISPLAY').length;
  const countDefect = serials.filter(s => s.status === 'DEFECT' || s.qualityType === 'DEFECT').length;

  const elNew = document.getElementById('whCountNew');
  const elDisplay = document.getElementById('whCountDisplay');
  const elDefect = document.getElementById('whCountDefect');
  if (elNew) elNew.textContent = countNew;
  if (elDisplay) elDisplay.textContent = countDisplay;
  if (elDefect) elDefect.textContent = countDefect;

  // 2. Render Physical Shelves Visual Grid
  if (shelvesContainer) {
    let sHtml = `<div class="shelves-grid">`;
    shelves.forEach(shelf => {
      // Đếm số lượng serial đang nằm tại kệ này
      const shelfSerials = serials.filter(s => (s.shelfLocation || '').startsWith(shelf.id) && s.status !== 'SOLD' && s.status !== 'RETURNED_SUPPLIER');
      const count = shelfSerials.length;
      const percent = Math.min(100, Math.round((count / shelf.capacity) * 100));

      let progressColor = 'var(--gold-primary)';
      if (percent >= 90) progressColor = 'var(--danger)';
      else if (percent >= 60) progressColor = 'var(--gold-light)';
      else progressColor = 'var(--success)';

      sHtml += `
        <div class="shelf-box-card" onclick="viewShelfDetail('${shelf.id}')">
          <div class="shelf-box-header">
            <span class="shelf-code">${shelf.id}</span>
            <span class="shelf-zone">${shelf.category}</span>
          </div>
          <div class="shelf-name">${shelf.name}</div>
          <div class="shelf-capacity-row">
            <span>Sức chứa: <b>${count} / ${shelf.capacity} chiếc</b></span>
            <span style="color:${progressColor}; font-weight:bold;">${percent}%</span>
          </div>
          <div class="shelf-progress-track">
            <div class="shelf-progress-fill" style="width:${percent}%; background:${progressColor};"></div>
          </div>
        </div>
      `;
    });
    sHtml += `</div>`;
    shelvesContainer.innerHTML = sHtml;
  }

  // 3. Render Multi-Unit Stock Summary (Thùng + Chiếc lẻ)
  if (multiUnitContainer) {
    let mHtml = `<div class="multi-unit-table-wrap">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div style="font-size:12px; color:var(--text-secondary);">
          Đang xem: <b style="color:var(--gold-light);">${currentWarehouseQualityFilter === 'ALL' ? 'Toàn bộ kho' : (currentWarehouseQualityFilter === 'NEW' ? 'Kho Hàng Mới' : (currentWarehouseQualityFilter === 'DISPLAY' ? 'Kho Trưng Bày' : 'Kho Hàng Lỗi'))}</b>
        </div>
        <button class="btn-toggle-view" style="font-size:11px;" onclick="openStockCardModal(null)">
          📜 Xem Thẻ Kho
        </button>
      </div>
      <table class="data-table-spec">
        <thead>
          <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
            <th>Sản Phẩm</th>
            <th>Tồn Đa Đơn Vị (Thùng + Chiếc)</th>
            <th>Giữ Chỗ</th>
            <th>Khả Dụng</th>
            <th>Giá Trị Đích Danh</th>
          </tr>
        </thead>
        <tbody>
    `;

    let totalWarehouseValuation = 0;

    watches.forEach(watch => {
      let watchSerials = serials.filter(s => s.sku === watch.sku || s.watchId === watch.id);

      // Lọc theo trạng thái chất lượng nếu có
      if (currentWarehouseQualityFilter === 'NEW') {
        watchSerials = watchSerials.filter(s => s.qualityType === 'NEW' && s.status !== 'DEFECT');
      } else if (currentWarehouseQualityFilter === 'DISPLAY') {
        watchSerials = watchSerials.filter(s => s.qualityType === 'DISPLAY');
      } else if (currentWarehouseQualityFilter === 'DEFECT') {
        watchSerials = watchSerials.filter(s => s.qualityType === 'DEFECT' || s.status === 'DEFECT');
      }

      const inStock = watchSerials.filter(s => s.status === 'IN_STOCK').length;
      const reserved = watchSerials.filter(s => s.status === 'RESERVED').length;
      const available = inStock;

      // Cộng dồn giá vốn đích danh của từng serial thực tế trong kho
      const valuation = watchSerials.filter(s => s.status === 'IN_STOCK' || s.status === 'RESERVED')
        .reduce((sum, s) => sum + (s.costPrice || watch.baseCost), 0);
      totalWarehouseValuation += valuation;

      const boxes = Math.floor(inStock / watch.conversionRate);
      const remainder = inStock % watch.conversionRate;
      const unitText = boxes > 0 
        ? `<b>${boxes}</b> ${watch.wholesaleUnit} + <b>${remainder}</b> ${watch.baseUnit}`
        : `<b>${inStock}</b> ${watch.baseUnit}`;

      mHtml += `
        <tr>
          <td>
            <b>${watch.name}</b><br>
            <small style="color:var(--text-muted); font-family:monospace;">${watch.sku}</small>
          </td>
          <td>
            <span style="color:var(--gold-light); font-size:12px;">${unitText}</span><br>
            <small style="color:var(--text-muted);">Tổng: ${inStock} ${watch.baseUnit}</small>
          </td>
          <td style="text-align:center;"><b style="color:var(--warning);">${reserved}</b></td>
          <td style="text-align:center;"><b style="color:var(--success); font-size:13px;">${available}</b></td>
          <td style="text-align:right;"><b style="color:var(--gold-primary);">${formatVND(valuation)}</b></td>
        </tr>
      `;
    });

    mHtml += `
        <tr style="background:rgba(212,175,55,0.08); font-weight:bold;">
          <td colspan="4" style="text-align:right;">TỔNG GIÁ TRỊ TỒN KHO ĐÍCH DANH TOÀN HỆ THỐNG:</td>
          <td style="text-align:right; font-size:13px; color:var(--gold-primary);">${formatVND(totalWarehouseValuation)}</td>
        </tr>
      </tbody>
      </table>
    </div>`;

    multiUnitContainer.innerHTML = mHtml;
  }
}

// Filter Warehouse Status Tab Buttons
function setWarehouseQualityTab(qualityType, element) {
  document.querySelectorAll('.warehouse-status-tabs .wh-status-tab-btn').forEach(b => b.classList.remove('active'));
  if (element) element.classList.add('active');
  renderWarehouseTab(qualityType);
}

// View Physical Shelf Detail Modal
function viewShelfDetail(shelfCode) {
  const shelf = ChronoDB.getShelves().find(s => s.id === shelfCode);
  if (!shelf) return;

  const serials = ChronoDB.getSerials().filter(s => (s.shelfLocation || '').startsWith(shelf.id) && s.status !== 'SOLD' && s.status !== 'RETURNED_SUPPLIER');

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `📍 Sơ Đồ Chi Tiết: ${shelf.name}`;
  bodyElem.innerHTML = `
    <div class="modal-detail-wrap">
      <div class="detail-kpi-bar">
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Mã Kệ</span>
          <span class="kpi-mini-val">${shelf.id}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Khu Vực Phân Lô</span>
          <span class="kpi-mini-val" style="font-size:12px;">${shelf.zone}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Đang Chứa</span>
          <span class="kpi-mini-val" style="color:var(--gold-light);">${serials.length} / ${shelf.capacity} chiếc</span>
        </div>
      </div>

      <div class="section-subtitle" style="margin-top:14px;">🏷️ DANH SÁCH SERIAL ĐANG LƯU TẠI KỆ NÀY (${serials.length} chiếc)</div>
      
      ${serials.length === 0 ? `
        <div style="text-align:center; padding:20px; color:var(--text-muted); font-size:12px;">Kệ hiện đang trống</div>
      ` : `
        <div class="serials-tag-cloud">
          ${serials.map(s => `
            <div class="serial-chip" onclick="lookupSerial('${s.serialNumber}')">
              <span>${s.serialNumber}</span>
              <small>${s.watchName} (${s.qualityType})</small>
            </div>
          `).join('')}
        </div>
      `}

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button class="btn-primary-action" onclick="closeModal('generalDetailModal'); openStockCountModalWithShelf('${shelf.id}')">
          📝 Kiểm Kê Kệ Này
        </button>
        <button class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Đóng</button>
      </div>
    </div>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Open Stock Count Modal (4.2)
function openStockCountModal() {
  const modal = document.getElementById('stockCountModal');
  if (!modal) return;
  modal.classList.add('active');
}

function openStockCountModalWithShelf(shelfCode) {
  openStockCountModal();
  const select = document.getElementById('auditShelfSelect');
  if (select) {
    select.value = shelfCode;
  }
}

// Process Stock Audit & Reconcile Discrepancy (Kiểm kê & Cân bằng kho - 4.2)
function processStockAudit() {
  const shelfSelect = document.getElementById('auditShelfSelect');
  const scannedQtyInput = document.getElementById('auditScannedQty');
  if (!shelfSelect || !scannedQtyInput) return;

  const shelfId = shelfSelect.value;
  const actualCount = parseInt(scannedQtyInput.value) || 0;

  // Lấy số lượng thực tế trên sổ sách của kệ
  const shelfSerials = ChronoDB.getSerials().filter(s => (s.shelfLocation || '').startsWith(shelfId) && s.status !== 'SOLD' && s.status !== 'RETURNED_SUPPLIER');
  const bookCount = shelfSerials.length;
  const diffCount = actualCount - bookCount;

  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);
  const auditCode = 'KK-2026-' + (ChronoDB.getStockAudits().length + 1).toString().padStart(3, '0');

  let resultStatus = 'KHỚP_100%';
  let msg = `Kiểm kê hoàn tất! Kệ ${shelfId} khớp 100% (Sổ sách: ${bookCount}, Thực tế: ${actualCount}).`;

  if (diffCount !== 0) {
    resultStatus = diffCount > 0 ? `THỪA_${diffCount}` : `THIẾU_${Math.abs(diffCount)}`;
    msg = `Phát hiện chênh lệch: ${diffCount > 0 ? 'Thừa +' : 'Thiếu '}${diffCount} chiếc! Đã lập phiếu cân bằng kho ${auditCode}.`;
  }

  // Ghi nhận Phiếu kiểm kê
  ChronoDB.addStockAudit({
    id: auditCode,
    auditDate: dateStr,
    shelfId: shelfId,
    shelfName: `Kệ ${shelfId}`,
    bookCount: bookCount,
    actualCount: actualCount,
    diffCount: diffCount,
    status: resultStatus,
    auditor: 'Thủ kho (Lê Tuấn)',
    note: msg
  });

  // Ghi Thẻ kho
  ChronoDB.addStockCard({
    id: 'TK-' + Date.now().toString().slice(-4),
    date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`,
    watchId: shelfId,
    sku: shelfId,
    watchName: `Kiểm kê Kệ ${shelfId}`,
    refType: 'KIỂM_KÊ',
    refCode: auditCode,
    changeQty: diffCount,
    balanceAfter: actualCount,
    serialNumber: `Kệ ${shelfId}`,
    user: 'Thủ kho (Lê Tuấn)',
    note: msg
  });

  // Ghi Audit Log
  ChronoDB.logAction('Thành viên 4', 'KIỂM_KÊ_KHO', `Kiểm kê Kệ ${shelfId}: Sổ sách ${bookCount} / Thực tế ${actualCount} (${resultStatus})`);

  closeModal('stockCountModal');
  showToast(msg, diffCount === 0 ? 'success' : 'warning');
  renderWarehouseTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Open Stock Card Modal (Thẻ kho - 4.2)
function openStockCardModal(watchId = null) {
  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  const stockCards = ChronoDB.getStockCards();

  titleElem.innerHTML = `📜 Thẻ Kho & Lịch Sử Biến Động Nhập - Xuất - Tồn`;
  bodyElem.innerHTML = `
    <div class="modal-detail-wrap">
      <div style="font-size:12px; color:var(--text-secondary); margin-bottom:12px;">
        Nhật ký biến động xuất nhập tồn đích danh từng giao dịch vật lý:
      </div>

      <div class="stock-cards-table-wrap">
        <table class="data-table-spec">
          <thead>
            <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
              <th>Thời Gian</th>
              <th>Loại Nghiệp Vụ</th>
              <th>Số Chứng Từ</th>
              <th>Sản Phẩm & Serial</th>
              <th>Biến Động (SL)</th>
              <th>Người Thực Hiện</th>
            </tr>
          </thead>
          <tbody>
            ${stockCards.map(tc => {
              let badgeType = '<span class="badge-status status-completed">Nhập Kho</span>';
              if (tc.refType === 'XUẤT_SỈ') badgeType = '<span class="badge-status status-danger">Xuất Sỉ</span>';
              else if (tc.refType === 'ĐỔI_TRẢ_SỈ') badgeType = '<span class="badge-status status-warning">Đổi Trả</span>';
              else if (tc.refType === 'TRẢ_NCC') badgeType = '<span class="badge-status status-danger">Trả NCC</span>';
              else if (tc.refType === 'KIỂM_KÊ') badgeType = '<span class="badge-status status-vip">Kiểm Kê</span>';

              const qtyDisplay = tc.changeQty > 0 ? `+${tc.changeQty}` : tc.changeQty;
              const colorDisplay = tc.changeQty > 0 ? 'var(--success)' : 'var(--danger)';

              return `
                <tr>
                  <td><small>${tc.date}</small></td>
                  <td>${badgeType}</td>
                  <td><b>${tc.refCode}</b></td>
                  <td>
                    <b>${tc.watchName}</b><br>
                    <small style="color:var(--text-muted); font-family:monospace;">${tc.serialNumber}</small>
                  </td>
                  <td style="text-align:center;"><b style="color:${colorDisplay}; font-size:13px;">${qtyDisplay}</b></td>
                  <td><small>${tc.user}</small></td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      </div>

      <div style="margin-top:20px; display:flex; justify-content:flex-end;">
        <button class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Đóng</button>
      </div>
    </div>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}
