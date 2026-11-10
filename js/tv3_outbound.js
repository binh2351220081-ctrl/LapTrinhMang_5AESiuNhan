/**
 * CHRONO VAULT B2B - PHÂN HỆ 3 (THÀNH VIÊN 3)
 * Khách Hàng Sỉ B2B, Lên Đơn Sỉ, Xuất Kho Quét Serial, Phiếu Thu Sỉ & Đổi Trả Sỉ
 */

// Render Outbound Tab
function renderOutboundTab() {
  const ordersContainer = document.getElementById('outboundOrdersList');
  const dealersContainer = document.getElementById('dealersOverviewList');

  const orders = ChronoDB.getOrders();
  const dealers = ChronoDB.getDealers();

  // 1. Orders List
  if (ordersContainer) {
    if (orders.length === 0) {
      ordersContainer.innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-muted); font-size:12px;">Chưa có lệnh xuất kho đại lý nào</div>`;
    } else {
      let html = `<div class="orders-list">`;
      orders.forEach(order => {
        let statusBadge = '<span class="badge-status status-warning">🔒 Đã Cọc & Giữ Chỗ (Reserved)</span>';
        if (order.status === 'COMPLETED') {
          statusBadge = '<span class="badge-status status-completed">✓ Đã Xuất Bàn Giao (Dispatched)</span>';
        } else if (order.status === 'CANCELLED') {
          statusBadge = '<span class="badge-status status-danger">Đã Hủy</span>';
        }

        const totalPieces = order.items.reduce((s, it) => s + (it.convertedQty || it.quantity), 0);

        html += `
          <div class="order-card">
            <div class="order-card-header">
              <div class="order-code-badge">
                <span class="code">${order.code}</span>
                <span class="date">${order.date}</span>
              </div>
              ${statusBadge}
            </div>

            <div class="order-card-body">
              <div class="order-dealer">🏪 <b>${order.dealerName}</b></div>
              <div class="order-summary-line">
                <span>Quy mô: <b>${totalPieces} chiếc</b> (${order.items.map(it => it.name).join(', ')})</span>
              </div>
              <div class="order-amount-line">
                <span>Tổng giá trị đơn:</span>
                <span class="amount-val">${formatVND(order.totalAmount)}</span>
              </div>
              <div class="order-debt-detail">
                <span>Đã cọc: <b style="color:var(--success);">${formatShortVND(order.depositAmount || 0)}</b></span>
                <span>Công nợ đại lý còn lại: <b style="color:var(--danger);">${formatShortVND(order.remainingDebt || 0)}</b></span>
              </div>
            </div>

            <div class="order-card-actions">
              <button class="btn-action-small" onclick="viewOrderDetail('${order.code}')">
                🔍 Xem Chi Tiết
              </button>
              ${order.status === 'RESERVED' ? `
                <button class="btn-action-small primary" onclick="confirmDispatchOrder('${order.code}')">
                  🚀 Quét Xuất Kho
                </button>
              ` : `
                <button class="btn-action-small" onclick="printDispatchA4('${order.code}')">
                  🖨️ In Phiếu Xuất A4
                </button>
              `}
            </div>
          </div>
        `;
      });
      html += `</div>`;
      ordersContainer.innerHTML = html;
    }
  }

  // 2. Dealers List
  if (dealersContainer) {
    let dHtml = `<div class="dealers-grid">`;
    dealers.forEach(dealer => {
      const tierBadge = dealer.tier === 'VIP' 
        ? `<span class="badge-status status-vip">👑 HẠNG VIP (-${Math.round(dealer.discountRate * 100)}%)</span>`
        : `<span class="badge-status status-completed">HẠNG ${dealer.tier} (-${Math.round(dealer.discountRate * 100)}%)</span>`;

      dHtml += `
        <div class="dealer-card">
          <div class="dealer-card-header">
            <div>
              <h4 class="dealer-shop">${dealer.shopName}</h4>
              <div class="dealer-meta">Đại diện: ${dealer.representative || ''} • MST: ${dealer.taxCode || ''} • ${dealer.phone}</div>
              <div class="dealer-address">📍 ${dealer.address}</div>
            </div>
            ${tierBadge}
          </div>

          <div class="dealer-credit-bar">
            <div class="credit-row">
              <span>Hạn mức tín dụng tối đa:</span>
              <b>${formatShortVND(dealer.creditLimit)}</b>
            </div>
            <div class="credit-row">
              <span>Dư nợ hiện tại:</span>
              <b style="color:var(--danger);">${formatShortVND(dealer.currentDebt)}</b>
            </div>
            <div class="credit-row">
              <span>Hạn mức còn lại khả dụng:</span>
              <b style="color:var(--success);">${formatShortVND(dealer.availableCredit)}</b>
            </div>
          </div>

          <div class="dealer-card-actions">
            <button class="btn-action-small primary" onclick="openDealerReceiptModal('${dealer.id}')">
              💰 Thu Thu Nợ Đại Lý
            </button>
            <button class="btn-action-small" onclick="openCustomerReturnModal('${dealer.id}')">
              🔄 Tiếp Nhận Đổi Trả
            </button>
          </div>
        </div>
      `;
    });
    dHtml += `</div>`;
    dealersContainer.innerHTML = dHtml;
  }
}

// View Order Detail Modal
function viewOrderDetail(orderCode) {
  const order = ChronoDB.getOrders().find(o => o.code === orderCode);
  if (!order) return;

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `📋 Chi Tiết Đơn Sỉ: ${order.code}`;
  bodyElem.innerHTML = `
    <div class="modal-detail-wrap">
      <div class="detail-kpi-bar">
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Đại Lý Đối Tác</span>
          <span class="kpi-mini-val" style="font-size:12px;">${order.dealerName}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Ngày Lên Đơn</span>
          <span class="kpi-mini-val">${order.date}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Tổng Đơn Hàng</span>
          <span class="kpi-mini-val" style="color:var(--gold-light);">${formatVND(order.totalAmount)}</span>
        </div>
      </div>

      <div class="section-subtitle" style="margin-top:14px;">📦 CHI TIẾT SẢN PHẨM & GIÁ SỈ ĐÃ ÁP DỤNG</div>
      <table class="data-table-spec">
        <thead>
          <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
            <th>Sản Phẩm</th>
            <th>SL</th>
            <th>Giá Sỉ Niêm Yết</th>
            <th>CK %</th>
            <th>Thành Tiền</th>
          </tr>
        </thead>
        <tbody>
          ${order.items.map(it => `
            <tr>
              <td><b>${it.name}</b><br><small style="color:var(--text-muted);">${it.sku}</small></td>
              <td><b>${it.convertedQty || it.quantity} ${it.unit || 'Chiếc'}</b></td>
              <td>${formatVND(it.unitPrice)}</td>
              <td><b style="color:var(--gold-light);">${it.discountPercent}%</b></td>
              <td><b>${formatVND(it.subtotal)}</b></td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div class="section-subtitle" style="margin-top:16px;">
        🏷️ DANH SÁCH SERIAL ${order.status === 'COMPLETED' ? 'ĐÃ XUẤT BÀN GIAO' : 'ĐANG KHÓA GIỮ CHỖ (RESERVED)'}
      </div>
      <div class="serials-tag-cloud">
        ${order.items.flatMap(it => (it.dispatchedSerials || it.reservedSerials || [])).map(s => `
          <div class="serial-chip" onclick="lookupSerial('${s}')">
            <span>${s}</span>
          </div>
        `).join('') || '<div style="color:var(--text-muted); font-size:12px;">Chưa gán mã Serial</div>'}
      </div>

      <div style="margin-top:20px; display:flex; gap:10px;">
        ${order.status === 'RESERVED' ? `
          <button class="btn-primary-action" onclick="closeModal('generalDetailModal'); confirmDispatchOrder('${order.code}')">
            🚀 Tiến Hành Quét Xuất Kho
          </button>
        ` : `
          <button class="btn-primary-action" onclick="printDispatchA4('${order.code}')">
            🖨️ In Biên Bản Bàn Giao A4
          </button>
        `}
        <button class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Đóng</button>
      </div>
    </div>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Open Create Order Modal (3.2)
function openCreateOrderModal() {
  const modal = document.getElementById('createOrderModal');
  if (!modal) return;

  const dealerSelect = document.getElementById('orderDealerSelect');
  const watchSelect = document.getElementById('orderWatchSelect');
  if (!dealerSelect || !watchSelect) return;

  const dealers = ChronoDB.getDealers();
  const watches = ChronoDB.getWatches();

  dealerSelect.innerHTML = dealers.map(d => `<option value="${d.id}">${d.shopName} (${d.tier} - CK ${Math.round(d.discountRate * 100)}%)</option>`).join('');
  watchSelect.innerHTML = watches.map(w => `<option value="${w.id}">${w.brand} - ${w.name} (${w.sku})</option>`).join('');

  updateOrderCalculationPreview();
  modal.classList.add('active');
}

// Open Create Order with preselected watch
function openCreateOrderWithWatch(watchId) {
  openCreateOrderModal();
  const watchSelect = document.getElementById('orderWatchSelect');
  if (watchSelect) {
    watchSelect.value = watchId;
    updateOrderCalculationPreview();
  }
}

// Update Order Calculation Preview
function updateOrderCalculationPreview() {
  const dealerSelect = document.getElementById('orderDealerSelect');
  const watchSelect = document.getElementById('orderWatchSelect');
  const unitSelect = document.getElementById('orderUnitSelect');
  const qtyInput = document.getElementById('orderQtyInput');
  const depositInput = document.getElementById('orderDepositInput');
  const previewDiv = document.getElementById('orderCalculationPreview');

  if (!dealerSelect || !watchSelect || !unitSelect || !qtyInput || !previewDiv) return;

  const dealer = ChronoDB.getDealerById(dealerSelect.value);
  const watch = ChronoDB.getWatchById(watchSelect.value);
  if (!dealer || !watch) return;

  const unit = unitSelect.value;
  const qty = Math.max(1, parseInt(qtyInput.value) || 1);
  const totalPieces = (unit === 'BOX') ? (qty * watch.conversionRate) : qty;

  // Lấy giá phân phối đại lý theo cấp đại lý
  let baseWholesalePrice = watch.wholesalePriceVip;
  if (dealer.tier === 'SILVER') baseWholesalePrice = watch.wholesalePriceSilver;
  else if (dealer.tier === 'BRONZE') baseWholesalePrice = watch.wholesalePriceBronze;

  const discountPercent = Math.round(dealer.discountRate * 100);
  const finalUnitPrice = Math.round(baseWholesalePrice * (1 - dealer.discountRate));
  const subtotal = totalPieces * finalUnitPrice;

  // Kiểm tra tồn khả dụng
  const serials = ChronoDB.getSerials().filter(s => (s.sku === watch.sku || s.watchId === watch.id) && s.status === 'IN_STOCK');
  const isStockOk = serials.length >= totalPieces;

  // Tự động set cọc tối thiểu 30%
  const minDeposit = Math.round(subtotal * 0.3);
  if (depositInput && (!depositInput.value || depositInput.dataset.manual !== 'true')) {
    depositInput.value = minDeposit;
  }

  let html = `
    <div style="background:rgba(212,175,55,0.06); border:1px solid var(--border-gold); border-radius:8px; padding:10px; font-size:12px;">
      <div>Quy đổi đặt hàng: <b>${qty} ${unit === 'BOX' ? watch.wholesaleUnit : watch.baseUnit}</b> = <b style="color:var(--success); font-size:13px;">${totalPieces} Chiếc</b> (MOQ yêu cầu: ${watch.moq} Chiếc)</div>
      <div style="margin-top:4px;">Giá phân phối đại lý niêm yết: ${formatVND(baseWholesalePrice)} • Chiết khấu ${dealer.tier}: <b style="color:var(--gold-light);">${discountPercent}%</b></div>
      <div style="margin-top:4px;">Đơn giá sau CK: <b>${formatVND(finalUnitPrice)}/chiếc</b></div>
      <div style="margin-top:6px; font-size:13px; font-weight:700;">Tổng thanh toán đơn: <span style="color:var(--gold-primary);">${formatVND(subtotal)}</span></div>
      <div style="margin-top:6px; display:flex; justify-content:space-between;">
        <span>Kho khả dụng: <b style="${isStockOk ? 'color:var(--success)' : 'color:var(--danger)'};">${serials.length} chiếc</b></span>
        <span>Hạn mức đại lý: <b>${formatShortVND(dealer.availableCredit)}</b></span>
      </div>
    </div>
  `;
  previewDiv.innerHTML = html;
}

// Submit Create Wholesale Order (3.2)
function submitCreateOrder() {
  const dealerSelect = document.getElementById('orderDealerSelect');
  const watchSelect = document.getElementById('orderWatchSelect');
  const unitSelect = document.getElementById('orderUnitSelect');
  const qtyInput = document.getElementById('orderQtyInput');
  const depositInput = document.getElementById('orderDepositInput');

  const dealer = ChronoDB.getDealerById(dealerSelect.value);
  const watch = ChronoDB.getWatchById(watchSelect.value);
  if (!dealer || !watch) return;

  const unit = unitSelect.value;
  const qty = Math.max(1, parseInt(qtyInput.value) || 1);
  const totalPieces = (unit === 'BOX') ? (qty * watch.conversionRate) : qty;

  // 1. Kiểm tra MOQ
  if (totalPieces < watch.moq) {
    showToast(`Lệnh xuất đại lý không đạt số lượng tối thiểu MOQ (${watch.moq} Chiếc)!`, 'warning');
    return;
  }

  // 2. Kiểm tra Tồn Khả Dụng
  const availableSerials = ChronoDB.getSerials().filter(s => (s.sku === watch.sku || s.watchId === watch.id) && s.status === 'IN_STOCK');
  if (availableSerials.length < totalPieces) {
    showToast(`Kho chỉ còn ${availableSerials.length} chiếc khả dụng, không đủ xuất ${totalPieces} chiếc!`, 'danger');
    return;
  }

  // Tính tiền
  let baseWholesalePrice = watch.wholesalePriceVip;
  if (dealer.tier === 'SILVER') baseWholesalePrice = watch.wholesalePriceSilver;
  else if (dealer.tier === 'BRONZE') baseWholesalePrice = watch.wholesalePriceBronze;

  const discountPercent = Math.round(dealer.discountRate * 100);
  const finalUnitPrice = Math.round(baseWholesalePrice * (1 - dealer.discountRate));
  const subtotal = totalPieces * finalUnitPrice;
  const depositAmount = Number(depositInput.value) || 0;
  const remainingDebt = Math.max(0, subtotal - depositAmount);

  // 3. Kiểm tra hạn mức nợ
  if (remainingDebt > dealer.availableCredit) {
    showToast(`Đại lý vượt quá hạn mức tín dụng công nợ (Tối đa khả dụng: ${formatShortVND(dealer.availableCredit)})!`, 'warning');
    return;
  }

  // Khóa giữ chỗ (Reserved) mã Serial
  const reservedSerialsToAssign = availableSerials.slice(0, totalPieces);
  const orderCode = 'DS-2026-' + (ChronoDB.getOrders().length + 1).toString().padStart(3, '0');
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);

  reservedSerialsToAssign.forEach(s => {
    s.status = 'RESERVED';
    s.dealerId = dealer.id;
    s.orderCode = orderCode;
    (s.timeline = s.timeline || []).push({
      date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`,
      title: 'Khóa giữ chỗ (Reserved)',
      desc: `Lệnh xuất đại lý ${orderCode} cho ${dealer.shopName}. Đã cọc ${formatShortVND(depositAmount)}`
    });
    ChronoDB.saveSerial(s);
  });

  // Tạo Order
  const newOrder = {
    code: orderCode,
    dealerId: dealer.id,
    dealerName: `${dealer.shopName} (${dealer.tier})`,
    date: dateStr,
    status: 'RESERVED',
    items: [
      {
        watchId: watch.id,
        sku: watch.sku,
        name: watch.name,
        unit: (unit === 'BOX') ? watch.wholesaleUnit : watch.baseUnit,
        quantity: qty,
        convertedQty: totalPieces,
        unitPrice: baseWholesalePrice,
        discountPercent: discountPercent,
        finalUnitPrice: finalUnitPrice,
        subtotal: subtotal,
        reservedSerials: reservedSerialsToAssign.map(s => s.serialNumber)
      }
    ],
    totalAmount: subtotal,
    depositAmount: depositAmount,
    remainingDebt: remainingDebt,
    shippingFee: 0,
    note: `Lệnh xuất đại lý đại lý ${dealer.tier}. Đã cọc ${formatShortVND(depositAmount)}, khóa giữ chỗ ${totalPieces} chiếc.`
  };
  ChronoDB.addOrder(newOrder);

  // Nếu có thu cọc -> Tạo Phiếu Thu sỉ tương ứng
  if (depositAmount > 0) {
    ChronoDB.addDealerReceipt({
      id: 'PT-2026-' + (ChronoDB.getDealerReceipts().length + 1).toString().padStart(3, '0'),
      dealerId: dealer.id,
      dealerName: dealer.shopName,
      date: dateStr,
      amount: depositAmount,
      paymentMethod: 'CHUYEN_KHOAN',
      referenceDoc: `Tiền cọc đơn xuất kho ${orderCode}`,
      createdBy: 'Kế toán (Phạm Thị Lan)',
      note: `Đặt cọc bảo đảm lệnh xuất đại lý ${orderCode}`
    });
  }

  // Audit Log
  ChronoDB.logAction('Thành viên 3', 'TẠO_ĐƠN_SỈ', `Lên lệnh xuất đại lý ${orderCode} cho ${dealer.shopName} (${totalPieces} chiếc, Cọc: ${formatShortVND(depositAmount)})`);

  closeModal('createOrderModal');
  showToast(`Đã tạo lệnh xuất đại lý ${orderCode} & Khóa giữ chỗ ${totalPieces} chiếc thành công!`, 'success');
  renderOutboundTab();
  if (typeof renderProductsList === 'function') renderProductsList();
  if (typeof renderWarehouseTab === 'function') renderWarehouseTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Confirm Dispatch Order (Quét Xuất Kho Thực Tế - 3.2)
function confirmDispatchOrder(orderCode) {
  const order = ChronoDB.getOrders().find(o => o.code === orderCode);
  if (!order || order.status !== 'RESERVED') return;

  if (!confirm(`Xác nhận quét mã Serial đóng gói và xuất kho giao cho đại lý ${order.dealerName}?`)) return;

  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);
  const dealer = ChronoDB.getDealerById(order.dealerId);

  // Chuyển serial sang SOLD
  const serialCodes = [];
  order.items.forEach(it => {
    (it.reservedSerials || []).forEach(sCode => {
      serialCodes.push(sCode);
      const s = ChronoDB.getSerial(sCode);
      if (s) {
        s.status = 'SOLD';
        s.shelfLocation = 'Đã xuất kho giao đại lý';
        s.soldDate = dateStr;
        (s.timeline = s.timeline || []).push({
          date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`,
          title: 'Xuất kho giao đại lý',
          desc: `Xuất giao theo lệnh xuất đại lý ${order.code}. Kích hoạt bảo hành điện tử chính hãng.`
        });
        ChronoDB.saveSerial(s);
      }
    });
    it.dispatchedSerials = it.reservedSerials;
    delete it.reservedSerials;
  });

  // Cập nhật Order
  order.status = 'COMPLETED';
  ChronoDB.setOrders(ChronoDB.getOrders());

  // Cập nhật nợ đại lý
  if (dealer && order.remainingDebt > 0) {
    dealer.currentDebt = (dealer.currentDebt || 0) + order.remainingDebt;
    dealer.availableCredit = Math.max(0, dealer.creditLimit - dealer.currentDebt);
    ChronoDB.saveDealer(dealer);
  }

  // Ghi Thẻ kho
  order.items.forEach(it => {
    ChronoDB.addStockCard({
      id: 'TK-' + Date.now().toString().slice(-4),
      date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`,
      watchId: it.watchId,
      sku: it.sku,
      watchName: it.name,
      refType: 'XUẤT_SỈ',
      refCode: order.code,
      changeQty: -(it.convertedQty || it.quantity),
      balanceAfter: 0,
      serialNumber: (it.dispatchedSerials || []).join(', '),
      user: 'Thủ kho (Lê Tuấn)',
      note: `Xuất kho đại lý đơn ${order.code} cho ${order.dealerName}`
    });
  });

  // Audit Log
  ChronoDB.logAction('Thành viên 3', 'XUẤT_KHO_SỈ', `Xuất kho thành công đơn ${order.code} (${serialCodes.length} chiếc)`);

  showToast(`Xuất kho thành công đơn ${order.code}! Đã trừ tồn kho thực tế và kích hoạt bảo hành.`, 'success');
  renderOutboundTab();
  if (typeof renderWarehouseTab === 'function') renderWarehouseTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Open Dealer Receipt Modal (Phiếu Thu Nợ Đại Lý - 3.1)
function openDealerReceiptModal(dealerId) {
  const dealer = ChronoDB.getDealerById(dealerId);
  if (!dealer) return;

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `💰 Lập Phiếu Thu Nợ Đại Lý: ${dealer.shopName}`;
  bodyElem.innerHTML = `
    <form id="dealerReceiptForm" onsubmit="event.preventDefault(); submitDealerReceipt('${dealer.id}');">
      <div class="form-group">
        <label class="form-label">Đại Lý Khách Sỉ</label>
        <input type="text" class="form-input" value="${dealer.shopName} (${dealer.tier})" readonly>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Dư Nợ Sỉ Hiện Tại</label>
          <input type="text" class="form-input" value="${formatVND(dealer.currentDebt)}" readonly style="color:var(--danger); font-weight:700;">
        </div>
        <div class="form-group">
          <label class="form-label">Hạn Mức Khả Dụng</label>
          <input type="text" class="form-input" value="${formatVND(dealer.availableCredit)}" readonly style="color:var(--success); font-weight:700;">
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Số Tiền Thu (VNĐ)</label>
          <input type="number" id="receiptAmountInput" class="form-input" value="${Math.min(100000000, dealer.currentDebt || 50000000)}" min="1000000" step="1000000" required>
        </div>
        <div class="form-group">
          <label class="form-label">Hình Thức Thu</label>
          <select class="form-select" id="receiptMethodSelect">
            <option value="CHUYEN_KHOAN">Chuyển khoản tài khoản công ty</option>
            <option value="TIEN_MAT">Tiền mặt tại kho / văn phòng</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Nội Dung Thu / Chứng Từ Gốc</label>
        <input type="text" id="receiptRefDocInput" class="form-input" value="Thu hồi công nợ đại lý theo kỳ hợp đồng" required>
      </div>

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button type="submit" class="btn-primary-action">✓ Xác Nhận Lập Phiếu Thu</button>
        <button type="button" class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Hủy</button>
      </div>
    </form>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Submit Dealer Receipt
function submitDealerReceipt(dealerId) {
  const dealer = ChronoDB.getDealerById(dealerId);
  if (!dealer) return;

  const amount = Number(document.getElementById('receiptAmountInput').value) || 0;
  const method = document.getElementById('receiptMethodSelect').value;
  const refDoc = document.getElementById('receiptRefDocInput').value.trim();

  if (amount <= 0) {
    showToast('Số tiền thu phải lớn hơn 0!', 'warning');
    return;
  }

  const receiptCode = 'PT-2026-' + (ChronoDB.getDealerReceipts().length + 1).toString().padStart(3, '0');
  const newReceipt = {
    id: receiptCode,
    dealerId: dealer.id,
    dealerName: dealer.shopName,
    date: new Date().toISOString().slice(0, 10),
    amount: amount,
    paymentMethod: method,
    referenceDoc: refDoc,
    createdBy: 'Kế toán (Phạm Thị Lan)',
    note: refDoc
  };

  ChronoDB.addDealerReceipt(newReceipt);
  closeModal('generalDetailModal');
  showToast(`Đã lập thành công phiếu thu ${receiptCode} thu ${formatShortVND(amount)} từ ${dealer.shopName}!`, 'success');
  renderOutboundTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Open Customer Return Modal (Tiếp Nhận Đổi Trả Sỉ - 3.1)
function openCustomerReturnModal(dealerId) {
  const dealer = ChronoDB.getDealerById(dealerId);
  if (!dealer) return;

  // Lấy các serial đã bán cho đại lý này
  const soldSerials = ChronoDB.getSerials().filter(s => s.status === 'SOLD' && (s.dealerId === dealer.id || !s.dealerId));

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `🔄 Tiếp Nhận Đổi Trả Sỉ Từ: ${dealer.shopName}`;
  bodyElem.innerHTML = `
    <form id="customerReturnForm" onsubmit="event.preventDefault(); submitCustomerReturn('${dealer.id}');">
      <div class="form-group">
        <label class="form-label">Chọn Mã Serial Đồng Hồ Trả Lại (Đối soát nguồn gốc bán)</label>
        <select class="form-select" id="custReturnSerialSelect" required>
          ${soldSerials.length > 0 ? soldSerials.map(s => `
            <option value="${s.serialNumber}">${s.serialNumber} - ${s.watchName}</option>
          `).join('') : '<option value="">Chưa có Serial nào đã xuất bán cho đại lý này</option>'}
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Phân Loại Trạng Thái Khi Nhập Kho Trả Về</label>
        <select class="form-select" id="custReturnTypeSelect">
          <option value="DEFECT_WAREHOUSE">Chuyển Kho Hàng Lỗi (Hỏng máy, trầy xước, lỗi NSX chờ trả NCC)</option>
          <option value="RESTOCK_NEW">Nhập lại Kho Hàng Mới (Đổi mẫu kinh doanh, nguyên seal)</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Số Tiền Cấn Trừ Công Nợ Hoặc Hoàn Tiền (VNĐ)</label>
        <input type="number" id="custReturnRefundInput" class="form-input" value="16200000" step="500000" required>
      </div>

      <div class="form-group">
        <label class="form-label">Lý Do Đổi Trả</label>
        <textarea id="custReturnReasonInput" class="form-textarea" rows="2">Đồng hồ có dấu hiệu hơi nước trong kính khi đại lý kiểm tra giao khách</textarea>
      </div>

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button type="submit" class="btn-primary-action" ${soldSerials.length === 0 ? 'disabled' : ''}>✓ Xác Nhận Tiếp Nhận Đổi Trả</button>
        <button type="button" class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Hủy</button>
      </div>
    </form>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Submit Customer Return
function submitCustomerReturn(dealerId) {
  const dealer = ChronoDB.getDealerById(dealerId);
  const serialSelect = document.getElementById('custReturnSerialSelect');
  const typeSelect = document.getElementById('custReturnTypeSelect');
  const refundInput = document.getElementById('custReturnRefundInput');
  const reasonInput = document.getElementById('custReturnReasonInput');

  if (!dealer || !serialSelect || !serialSelect.value) {
    showToast('Vui lòng chọn mã Serial cần tiếp nhận đổi trả!', 'warning');
    return;
  }

  const serialCode = serialSelect.value;
  const returnType = typeSelect.value;
  const refundAmount = Number(refundInput.value) || 0;
  const reason = reasonInput.value.trim();

  const serialObj = ChronoDB.getSerial(serialCode);
  if (!serialObj) return;

  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);

  // Cập nhật Serial
  if (returnType === 'DEFECT_WAREHOUSE') {
    serialObj.status = 'DEFECT';
    serialObj.qualityType = 'DEFECT';
    serialObj.shelfLocation = 'C-01-KHO-LOI';
  } else {
    serialObj.status = 'IN_STOCK';
    serialObj.qualityType = 'NEW';
    serialObj.shelfLocation = 'A-01-T1-N01';
  }

  (serialObj.timeline = serialObj.timeline || []).push({
    date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`,
    title: 'Tiếp nhận trả hàng đại lý',
    desc: `Đại lý ${dealer.shopName} trả lại. Phân loại: ${returnType}. Cấn trừ nợ: ${formatVND(refundAmount)}`
  });
  ChronoDB.saveSerial(serialObj);

  // Giảm trừ nợ đại lý
  dealer.currentDebt = Math.max(0, (dealer.currentDebt || 0) - refundAmount);
  dealer.availableCredit = Math.min(dealer.creditLimit, dealer.creditLimit - dealer.currentDebt);
  ChronoDB.saveDealer(dealer);

  // Lưu Phiếu nhận đổi trả
  const returnCode = 'TS-2026-' + (ChronoDB.getCustomerReturns().length + 1).toString().padStart(3, '0');
  ChronoDB.addCustomerReturn({
    id: returnCode,
    dealerId: dealer.id,
    dealerName: dealer.shopName,
    date: dateStr,
    serial: serialCode,
    watchId: serialObj.sku,
    watchName: serialObj.watchName,
    returnType: returnType,
    refundAmount: refundAmount,
    reason: reason,
    status: 'COMPLETED',
    createdBy: 'Nhân viên nhập/xuất kho (Nguyễn Phương)'
  });

  // Ghi Thẻ kho
  ChronoDB.addStockCard({
    id: 'TK-' + Date.now().toString().slice(-4),
    date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`,
    watchId: serialObj.sku,
    sku: serialObj.sku,
    watchName: serialObj.watchName,
    refType: 'ĐỔI_TRẢ_SỈ',
    refCode: returnCode,
    changeQty: 1,
    balanceAfter: 1,
    serialNumber: serialCode,
    user: 'Thủ kho (Lê Tuấn)',
    note: `Nhận trả hàng đại lý từ ${dealer.shopName} -> ${returnType === 'DEFECT_WAREHOUSE' ? 'Kho Lỗi C-01' : 'Kho Mới'}`
  });

  // Audit Log
  ChronoDB.logAction('Thành viên 3', 'TIẾP_NHẬN_ĐỔI_TRẢ', `Đổi trả Serial ${serialCode} từ ${dealer.shopName} (Cấn trừ: ${formatShortVND(refundAmount)})`);

  closeModal('generalDetailModal');
  showToast(`Đã tiếp nhận đổi trả thành công mã ${serialCode}! Cấn trừ nợ ${formatShortVND(refundAmount)}`, 'success');
  renderOutboundTab();
  if (typeof renderWarehouseTab === 'function') renderWarehouseTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Print Dispatch Voucher A4 (3.2)
function printDispatchA4(orderCode) {
  const order = ChronoDB.getOrders().find(o => o.code === orderCode);
  if (!order) return;

  const printWindow = window.open('', '_blank');
  if (!printWindow) {
    showToast('Trình duyệt đã chặn cửa sổ in (Pop-up). Vui lòng cho phép mở cửa sổ.', 'warning');
    return;
  }

  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Biên Bản Giao Hàng & Phiếu Xuất Kho - ${order.code}</title>
      <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; padding: 30px; color: #111; line-height: 1.5; }
        .header { display: flex; justify-content: space-between; border-bottom: 2px solid #333; padding-bottom: 15px; }
        .company-name { font-size: 20px; font-weight: bold; text-transform: uppercase; }
        .title { text-align: center; margin: 25px 0 10px; font-size: 22px; font-weight: bold; text-transform: uppercase; }
        .meta-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #333; padding: 8px 10px; text-align: left; font-size: 12px; }
        th { background: #f0f0f0; }
        .signatures { display: flex; justify-content: space-between; margin-top: 50px; text-align: center; font-size: 13px; }
        .sig-block { width: 22%; }
        .sig-space { height: 70px; }
        .serials-box { background: #fafafa; border: 1px dashed #666; padding: 8px; font-family: monospace; font-size: 11px; margin-top: 10px; }
      </style>
    </head>
    <body>
      <div class="header">
        <div>
          <div class="company-name">CHRONO VAULT B2B WMS</div>
          <div>Tổng Đại Lý Phân Phối Đồng Hồ Đeo Tay</div>
          <div>Kho Tổng Xuất Hàng: Q. Tân Bình, TP.HCM</div>
        </div>
        <div style="text-align:right;">
          <div>Mẫu số: <b>02-VT/B2B</b></div>
          <div>Số đơn: <b>${order.code}</b></div>
          <div>Ngày: <b>${order.date}</b></div>
        </div>
      </div>

      <div class="title">BIÊN BẢN GIAO NHẬN KIÊM PHIẾU XUẤT KHO XUẤT KHO ĐẠI LÝ B2B</div>

      <div class="meta-row">
        <div>Đại lý nhận hàng: <b>${order.dealerName}</b></div>
        <div>Mã lệnh xuất đại lý: <b>${order.code}</b></div>
      </div>
      <div class="meta-row">
        <div>Trạng thái: <b>ĐÃ XUẤT KHO VẬT LÝ</b></div>
        <div>Đã đặt cọc: <b>${formatVND(order.depositAmount || 0)}</b></div>
      </div>

      <table>
        <thead>
          <tr>
            <th>STT</th>
            <th>Mã SKU</th>
            <th>Tên Đồng Hồ</th>
            <th>Số Lượng</th>
            <th>Đơn Giá Sỉ</th>
            <th>Chiết Khấu</th>
            <th>Thành Tiền</th>
          </tr>
        </thead>
        <tbody>
          ${order.items.map((it, idx) => `
            <tr>
              <td style="text-align:center;">${idx + 1}</td>
              <td><b>${it.sku}</b></td>
              <td>${it.name}</td>
              <td style="text-align:center; font-weight:bold;">${it.convertedQty || it.quantity}</td>
              <td>${formatVND(it.unitPrice)}</td>
              <td style="text-align:center;">${it.discountPercent}%</td>
              <td><b>${formatVND(it.subtotal)}</b></td>
            </tr>
          `).join('')}
          <tr>
            <td colspan="6" style="text-align:right; font-weight:bold;">TỔNG GIÁ TRỊ ĐƠN HÀNG:</td>
            <td style="font-weight:bold; font-size:13px;">${formatVND(order.totalAmount)}</td>
          </tr>
          <tr>
            <td colspan="6" style="text-align:right;">Số tiền đã thanh toán / cọc:</td>
            <td>${formatVND(order.depositAmount || 0)}</td>
          </tr>
          <tr>
            <td colspan="6" style="text-align:right; font-weight:bold; color:#b91c1c;">CÔNG NỢ SỈ GHI NHẬN:</td>
            <td style="font-weight:bold; color:#b91c1c;">${formatVND(order.remainingDebt || 0)}</td>
          </tr>
        </tbody>
      </table>

      <div class="serials-box">
        <b>BẢNG DANH SÁCH SERIAL ĐÍCH DANH BÀN GIAO & KÍCH HOẠT BẢO HÀNH:</b><br>
        ${order.items.map(it => `
          <div><b>${it.name}:</b> ${(it.dispatchedSerials || it.reservedSerials || []).join(', ')}</div>
        `).join('')}
      </div>

      <div class="signatures">
        <div class="sig-block">
          <b>Người Lập Đơn</b>
          <div class="sig-space"></div>
          <div>Nguyễn Phương</div>
        </div>
        <div class="sig-block">
          <b>Thủ Kho Xuất</b>
          <div class="sig-space"></div>
          <div>Lê Tuấn</div>
        </div>
        <div class="sig-block">
          <b>Đại Diện Giao Vận</b>
          <div class="sig-space"></div>
          <div>Chuyển Phát Hỏa Tốc</div>
        </div>
        <div class="sig-block">
          <b>Đại Diện Đại Lý Nhận</b>
          <div class="sig-space"></div>
          <div>${order.dealerName.slice(0, 20)}</div>
        </div>
      </div>

      <script>window.onload = function() { window.print(); };</script>
    </body>
    </html>
  `);
  printWindow.document.close();
}
