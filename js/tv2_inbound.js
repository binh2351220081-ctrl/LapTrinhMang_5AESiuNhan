/**
 * CHRONO VAULT B2B - PHÂN HỆ 2 (THÀNH VIÊN 2)
 * Quản lý Nhà Cung Cấp, Phiếu Nhập Kho, Chi Phí Nhập, Phiếu Chi NCC & Trả Hàng Lỗi NCC
 */

// Render Inbound Tab
function renderInboundTab() {
  const receiptsContainer = document.getElementById('inboundReceiptsList');
  const suppliersContainer = document.getElementById('suppliersDebtOverview');

  const receipts = ChronoDB.getReceipts();
  const suppliers = ChronoDB.getSuppliers();

  // 1. Render Inbound Receipts List
  if (receiptsContainer) {
    if (receipts.length === 0) {
      receiptsContainer.innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-muted); font-size:12px;">Chưa có phiếu nhập kho nào</div>`;
    } else {
      let html = `<div class="receipts-list">`;
      receipts.forEach(rcpt => {
        const totalItemsCount = rcpt.items.reduce((sum, it) => sum + (it.convertedQty || it.quantity), 0);
        html += `
          <div class="receipt-card">
            <div class="receipt-card-header">
              <div class="receipt-code-badge">
                <span class="code">${rcpt.code}</span>
                <span class="date">${rcpt.date}</span>
              </div>
              <span class="badge-status status-completed">✓ Đã Nhập Kho</span>
            </div>

            <div class="receipt-card-body">
              <div class="receipt-supplier">🏢 <b>${rcpt.supplierName}</b></div>
              <div class="receipt-summary-line">
                <span>Quy mô: <b>${totalItemsCount} chiếc</b> (${rcpt.items.length} mẫu mã)</span>
                <span>Chi phí phân bổ: <b>${formatShortVND(rcpt.allocatedExpenses || 0)}</b></span>
              </div>
              <div class="receipt-amount-line">
                <span>Tổng giá trị nhập:</span>
                <span class="amount-val">${formatVND(rcpt.totalAmount)}</span>
              </div>
            </div>

            <div class="receipt-card-actions">
              <button class="btn-action-small" onclick="viewReceiptDetail('${rcpt.code}')">
                🔍 Xem Chi Tiết & Serial
              </button>
              <button class="btn-action-small" onclick="printReceiptA4('${rcpt.code}')">
                🖨️ In Phiếu A4
              </button>
            </div>
          </div>
        `;
      });
      html += `</div>`;
      receiptsContainer.innerHTML = html;
    }
  }

  // 2. Render Suppliers & Debt Balance Overview
  if (suppliersContainer) {
    let sHtml = `<div class="suppliers-debt-grid">`;
    suppliers.forEach(supp => {
      sHtml += `
        <div class="supplier-card">
          <div class="supplier-card-header">
            <div>
              <h4 class="supp-name">${supp.name}</h4>
              <div class="supp-meta">MST: ${supp.taxCode} • SĐT: ${supp.phone}</div>
              <div class="supp-bank">💳 ${supp.bankAccount || ''} - ${supp.bankName || ''}</div>
            </div>
            <span class="badge-status ${supp.status === 'ACTIVE' ? 'status-completed' : 'status-danger'}">${supp.status === 'ACTIVE' ? 'Hợp Tác' : 'Tạm Dừng'}</span>
          </div>

          <div class="supplier-debt-box">
            <div class="debt-label">Dư nợ phải trả NCC:</div>
            <div class="debt-value">${formatVND(supp.debtBalance)}</div>
          </div>

          <div class="supplier-card-actions">
            <button class="btn-action-small primary" onclick="openSupplierPaymentModal('${supp.id}')">
              💵 Lập Phiếu Chi NCC
            </button>
            <button class="btn-action-small" onclick="openSupplierReturnModal('${supp.id}')">
              ↩️ Trả Hàng Lỗi NCC
            </button>
          </div>
        </div>
      `;
    });
    sHtml += `</div>`;
    suppliersContainer.innerHTML = sHtml;
  }
}

// View Receipt Detail Modal
function viewReceiptDetail(receiptCode) {
  const rcpt = ChronoDB.getReceipts().find(r => r.code === receiptCode);
  if (!rcpt) return;

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `📄 Phiếu Nhập Kho: ${rcpt.code}`;
  bodyElem.innerHTML = `
    <div class="modal-detail-wrap">
      <div class="detail-kpi-bar">
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Nhà Cung Cấp</span>
          <span class="kpi-mini-val" style="font-size:12px;">${rcpt.supplierName}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Ngày Lập Phiếu</span>
          <span class="kpi-mini-val">${rcpt.date}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Tổng Giá Trị</span>
          <span class="kpi-mini-val" style="color:var(--gold-light);">${formatVND(rcpt.totalAmount)}</span>
        </div>
      </div>

      <div class="section-subtitle" style="margin-top:14px;">📦 CHI TIẾT SẢN PHẨM & QUY ĐỔI ĐƠN VỊ TÍNH</div>
      <table class="data-table-spec">
        <thead>
          <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
            <th>Sản Phẩm</th>
            <th>ĐVT Nhập</th>
            <th>SL Quy Đổi</th>
            <th>Đơn Giá Vốn</th>
            <th>Thành Tiền</th>
          </tr>
        </thead>
        <tbody>
          ${rcpt.items.map(it => `
            <tr>
              <td><b>${it.name}</b><br><small style="color:var(--text-muted);">${it.sku}</small></td>
              <td>${it.quantity} ${it.unit}</td>
              <td><b style="color:var(--success);">${it.convertedQty} Chiếc</b></td>
              <td>${formatVND(it.unitCost)}</td>
              <td><b>${formatVND(it.subtotal)}</b></td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div style="background:rgba(212,175,55,0.06); border:1px solid var(--border-gold); border-radius:8px; padding:10px; margin-top:12px; font-size:12px;">
        🚢 Chi phí vận chuyển & hải quan phân bổ: <b>${formatVND(rcpt.allocatedExpenses || 0)}</b> (đã tính vào giá vốn đích danh).
      </div>

      <div class="section-subtitle" style="margin-top:16px;">🏷️ DANH SÁCH MÃ SERIAL ĐÍCH DANH NHẬP KHO</div>
      ${rcpt.items.map(it => `
        <div style="margin-bottom:10px;">
          <div style="font-size:11.5px; font-weight:700; color:var(--text-primary); margin-bottom:4px;">${it.name}:</div>
          <div class="serials-tag-cloud">
            ${(it.serials || []).map(s => `
              <div class="serial-chip" onclick="lookupSerial('${s}')">
                <span>${s}</span>
              </div>
            `).join('')}
          </div>
        </div>
      `).join('')}

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button class="btn-primary-action" onclick="printReceiptA4('${rcpt.code}')">
          🖨️ In Phiếu Nhập Kho A4
        </button>
        <button class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Đóng</button>
      </div>
    </div>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Open Create Inbound Modal (2.2)
function openCreateInboundModal() {
  const modal = document.getElementById('createInboundModal');
  if (!modal) return;

  const suppSelect = document.getElementById('inboundSupplierSelect');
  const watchSelect = document.getElementById('inboundWatchSelect');
  if (!suppSelect || !watchSelect) return;

  const suppliers = ChronoDB.getSuppliers();
  const watches = ChronoDB.getWatches();

  suppSelect.innerHTML = suppliers.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
  watchSelect.innerHTML = watches.map(w => `<option value="${w.id}">${w.brand} - ${w.name} (${w.sku})</option>`).join('');

  updateInboundConversionPreview();
  modal.classList.add('active');
}

// Update Inbound Conversion Preview
function updateInboundConversionPreview() {
  const watchSelect = document.getElementById('inboundWatchSelect');
  const unitSelect = document.getElementById('inboundUnitSelect');
  const qtyInput = document.getElementById('inboundQtyInput');
  const previewDiv = document.getElementById('inboundConversionPreview');
  const serialTextarea = document.getElementById('inboundSerialTextarea');

  if (!watchSelect || !unitSelect || !qtyInput || !previewDiv) return;

  const watch = ChronoDB.getWatchById(watchSelect.value);
  if (!watch) return;

  const unit = unitSelect.value;
  const qty = Math.max(1, parseInt(qtyInput.value) || 1);

  let totalPieces = qty;
  let text = '';

  if (unit === 'BOX') {
    totalPieces = qty * watch.conversionRate;
    text = `Quy đổi sỉ: <b>${qty} ${watch.wholesaleUnit}</b> × ${watch.conversionRate} = <b style="color:var(--success); font-size:13px;">${totalPieces} Chiếc lẻ</b>`;
  } else {
    text = `Nhập trực tiếp theo chiếc lẻ: <b style="color:var(--success); font-size:13px;">${qty} Chiếc</b>`;
  }

  const estVal = totalPieces * watch.baseCost;
  text += `<br>Ước tính giá trị hàng nhập: <b>${formatVND(estVal)}</b>`;
  previewDiv.innerHTML = text;

  // Auto-generate sample serial sequence if empty or flagged
  if (serialTextarea && serialTextarea.dataset.autoGen !== 'false') {
    const prefix = watch.sku.split('-')[0] + '-' + watch.sku.split('-')[1];
    const year = new Date().getFullYear();
    const startNum = 1000 + Math.floor(Math.random() * 8000);
    const generatedSerials = [];
    for (let i = 0; i < totalPieces; i++) {
      generatedSerials.push(`${prefix}-${year}-${startNum + i}`);
    }
    serialTextarea.value = generatedSerials.join('\n');
  }
}

// Submit Create Inbound Receipt (2.2)
function submitCreateInbound() {
  const suppSelect = document.getElementById('inboundSupplierSelect');
  const watchSelect = document.getElementById('inboundWatchSelect');
  const unitSelect = document.getElementById('inboundUnitSelect');
  const qtyInput = document.getElementById('inboundQtyInput');
  const serialTextarea = document.getElementById('inboundSerialTextarea');
  const allocatedCostInput = document.getElementById('inboundAllocatedCost');

  const supplier = ChronoDB.getSupplierById(suppSelect.value);
  const watch = ChronoDB.getWatchById(watchSelect.value);
  if (!supplier || !watch) return;

  const unit = unitSelect.value;
  const qty = Math.max(1, parseInt(qtyInput.value) || 1);
  const totalPieces = (unit === 'BOX') ? (qty * watch.conversionRate) : qty;
  const allocatedExpense = Number(allocatedCostInput?.value) || 0;

  // Parse Serials
  const rawSerials = (serialTextarea.value || '').split('\n').map(s => s.trim().toUpperCase()).filter(s => s.length > 0);
  
  if (rawSerials.length !== totalPieces) {
    showToast(`Số lượng Serial (${rawSerials.length}) không khớp chính xác 100% với số lượng quy đổi (${totalPieces} Chiếc)!`, 'warning');
    return;
  }

  // Check Duplicate Serials across system
  const existingSerials = ChronoDB.getSerials();
  for (const s of rawSerials) {
    if (existingSerials.some(es => es.serialNumber === s)) {
      showToast(`Mã Serial bị trùng lặp trên hệ thống: ${s}!`, 'danger');
      return;
    }
  }

  // Cost calculation
  const expensePerPiece = Math.round(allocatedExpense / totalPieces);
  const finalPieceCost = watch.baseCost + expensePerPiece;
  const subtotal = totalPieces * watch.baseCost;
  const totalAmount = subtotal + allocatedExpense;

  const receiptCode = 'PN-2026-' + (ChronoDB.getReceipts().length + 1).toString().padStart(3, '0');
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10);

  // 1. Create Receipt
  const newReceipt = {
    code: receiptCode,
    supplierId: supplier.id,
    supplierName: supplier.name,
    date: dateStr,
    status: 'COMPLETED',
    items: [
      {
        watchId: watch.id,
        sku: watch.sku,
        name: watch.name,
        unit: (unit === 'BOX') ? watch.wholesaleUnit : watch.baseUnit,
        quantity: qty,
        convertedQty: totalPieces,
        unitCost: finalPieceCost,
        subtotal: subtotal,
        serials: rawSerials
      }
    ],
    allocatedExpenses: allocatedExpense,
    totalAmount: totalAmount,
    paidAmount: 0,
    debtRemaining: totalAmount
  };
  ChronoDB.addReceipt(newReceipt);

  // 2. Add Serials into DB
  const shelf = ChronoDB.getShelves()[0] || { id: 'A-01' };
  rawSerials.forEach(sCode => {
    ChronoDB.saveSerial({
      serialNumber: sCode,
      sku: watch.sku,
      watchName: watch.name,
      costPrice: finalPieceCost,
      status: 'IN_STOCK',
      qualityType: 'NEW',
      shelfLocation: `${shelf.id}-T1-N01`,
      supplierId: supplier.id,
      receiptCode: receiptCode,
      receivedDate: dateStr,
      warrantyExpire: (now.getFullYear() + 3) + '-' + dateStr.slice(5),
      timeline: [
        { date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`, title: 'Nhập kho thành công', desc: `Từ NCC: ${supplier.name} theo ${receiptCode}. Giá vốn: ${formatVND(finalPieceCost)}` }
      ]
    });
  });

  // 3. Update Supplier Debt Balance
  supplier.debtBalance = (supplier.debtBalance || 0) + totalAmount;
  ChronoDB.saveSupplier(supplier);

  // 4. Create Stock Card Entry
  ChronoDB.addStockCard({
    id: 'TK-' + Date.now().toString().slice(-4),
    date: `${dateStr} ${now.getHours()}:${now.getMinutes()}`,
    watchId: watch.id,
    sku: watch.sku,
    watchName: watch.name,
    refType: 'NHẬP_KHO',
    refCode: receiptCode,
    changeQty: totalPieces,
    balanceAfter: totalPieces,
    serialNumber: `${rawSerials[0]} -> ${rawSerials[rawSerials.length - 1]}`,
    user: 'Thủ kho (Lê Tuấn)',
    note: `Nhập ${totalPieces} chiếc từ ${supplier.name} (Chi phí phân bổ: ${formatShortVND(allocatedExpense)})`
  });

  // 5. Audit Log
  ChronoDB.logAction('Thành viên 2', 'NHẬP_KHO', `Lập & Duyệt phiếu nhập ${receiptCode} cho ${supplier.name} (+${totalPieces} chiếc)`);

  closeModal('createInboundModal');
  showToast(`Nhập kho thành công ${totalPieces} chiếc vào hệ thống theo ${receiptCode}!`, 'success');
  renderInboundTab();
  if (typeof renderProductsList === 'function') renderProductsList();
  if (typeof renderWarehouseTab === 'function') renderWarehouseTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Open Supplier Payment Modal (Phiếu Chi NCC - 2.1)
function openSupplierPaymentModal(supplierId) {
  const supplier = ChronoDB.getSupplierById(supplierId);
  if (!supplier) return;

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `💵 Lập Phiếu Chi Thanh Toán NCC: ${supplier.name}`;
  bodyElem.innerHTML = `
    <form id="supplierPaymentForm" onsubmit="event.preventDefault(); submitSupplierPayment('${supplier.id}');">
      <div class="form-group">
        <label class="form-label">Nhà Cung Cấp Đối Tác</label>
        <input type="text" class="form-input" value="${supplier.name}" readonly style="background:rgba(255,255,255,0.05);">
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Dư Nợ Hiện Tại Phải Trả</label>
          <input type="text" class="form-input" value="${formatVND(supplier.debtBalance)}" readonly style="color:var(--danger); font-weight:700;">
        </div>
        <div class="form-group">
          <label class="form-label">Tài Khoản Thụ Hưởng Của NCC</label>
          <input type="text" class="form-input" value="${supplier.bankAccount || ''} - ${supplier.bankName || ''}" readonly>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Số Tiền Thanh Toán (VNĐ)</label>
          <input type="number" id="payAmountInput" class="form-input" value="${Math.min(500000000, supplier.debtBalance)}" max="${supplier.debtBalance}" min="1000000" step="1000000" required>
        </div>
        <div class="form-group">
          <label class="form-label">Hình Thức Thanh Toán</label>
          <select class="form-select" id="payMethodSelect">
            <option value="CHUYEN_KHOAN">Ủy nhiệm chi / Chuyển khoản ngân hàng</option>
            <option value="TIEN_MAT">Tiền mặt quỹ công ty</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Số Chứng Từ Gốc / Tham Chiếu</label>
        <input type="text" id="payRefDocInput" class="form-input" value="UNC-${Date.now().toString().slice(-6)}" required>
      </div>

      <div class="form-group">
        <label class="form-label">Ghi Chú Nghiệp Vụ</label>
        <textarea id="payNoteInput" class="form-textarea" rows="2">Thanh toán công nợ tiền hàng đợt mới</textarea>
      </div>

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button type="submit" class="btn-primary-action">✓ Xác Nhận Lập Phiếu Chi</button>
        <button type="button" class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Hủy</button>
      </div>
    </form>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Submit Supplier Payment
function submitSupplierPayment(supplierId) {
  const supplier = ChronoDB.getSupplierById(supplierId);
  if (!supplier) return;

  const amount = Number(document.getElementById('payAmountInput').value) || 0;
  const method = document.getElementById('payMethodSelect').value;
  const refDoc = document.getElementById('payRefDocInput').value.trim();
  const note = document.getElementById('payNoteInput').value.trim();

  if (amount <= 0) {
    showToast('Số tiền thanh toán phải lớn hơn 0!', 'warning');
    return;
  }

  const payCode = 'PC-2026-' + (ChronoDB.getSupplierPayments().length + 1).toString().padStart(3, '0');
  const newPayment = {
    id: payCode,
    supplierId: supplier.id,
    supplierName: supplier.name,
    date: new Date().toISOString().slice(0, 10),
    amount: amount,
    paymentMethod: method,
    referenceDoc: refDoc,
    createdBy: 'Kế toán (Phạm Thị Lan)',
    note: note
  };

  ChronoDB.addSupplierPayment(newPayment);
  closeModal('generalDetailModal');
  showToast(`Đã lập thành công phiếu chi ${payCode} thanh toán ${formatShortVND(amount)} cho NCC!`, 'success');
  renderInboundTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Open Supplier Defect Return Modal (Xuất Trả Hàng Lỗi NCC - 2.1)
function openSupplierReturnModal(supplierId) {
  const supplier = ChronoDB.getSupplierById(supplierId);
  if (!supplier) return;

  // Lấy các serial lỗi trong kho
  const serials = ChronoDB.getSerials().filter(s => s.status === 'DEFECT' || s.qualityType === 'DEFECT');

  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  titleElem.innerHTML = `↩️ Phiếu Xuất Trả Hàng Lỗi Cho NCC: ${supplier.name}`;
  bodyElem.innerHTML = `
    <form id="supplierReturnForm" onsubmit="event.preventDefault(); submitSupplierReturn('${supplier.id}');">
      <div class="form-group">
        <label class="form-label">Chọn Mã Serial Hàng Lỗi Cần Trả (Kho Hàng Lỗi)</label>
        <select class="form-select" id="returnSerialSelect" required>
          ${serials.length > 0 ? serials.map(s => `
            <option value="${s.serialNumber}">${s.serialNumber} - ${s.watchName} (Giá vốn: ${formatVND(s.costPrice)})</option>
          `).join('') : '<option value="">Không có Serial nào trong Kho Hàng Lỗi</option>'}
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Lý Do Xuất Trả Nhà Sản Xuất</label>
        <select class="form-select" id="returnReasonSelect">
          <option value="Hấp hơi nước mặt kính từ NSX">Hấp hơi nước mặt kính từ NSX</option>
          <option value="Lỗi bộ máy cơ sai số vượt tiêu chuẩn">Lỗi bộ máy cơ sai số vượt tiêu chuẩn</option>
          <option value="Trầy xước vỏ bezel khi khui kiện seal">Trầy xước vỏ bezel khi khui kiện seal</option>
          <option value="Lỗi kim cọc số phát quang LumiNova">Lỗi kim cọc số phát quang LumiNova</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Số Tiền Hoàn Trả Giảm Trừ Công Nợ NCC (VNĐ)</label>
        <input type="number" id="returnRefundInput" class="form-input" value="13800000" step="500000" required>
      </div>

      <div style="background:rgba(239,68,68,0.08); border:1px solid var(--danger); border-radius:8px; padding:10px; font-size:12px; margin-bottom:12px;">
        ⚠️ Khi duyệt phiếu xuất trả: Mã Serial sẽ được chuyển trạng thái sang "ĐÃ XUẤT TRẢ NCC", tự động trừ tồn Kho Hàng Lỗi và cấn trừ trực tiếp vào số dư công nợ phải trả NCC.
      </div>

      <div style="margin-top:20px; display:flex; gap:10px;">
        <button type="submit" class="btn-primary-action" ${serials.length === 0 ? 'disabled' : ''}>✓ Phê Duyệt Xuất Trả NCC</button>
        <button type="button" class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Hủy</button>
      </div>
    </form>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Submit Supplier Defect Return
function submitSupplierReturn(supplierId) {
  const supplier = ChronoDB.getSupplierById(supplierId);
  const serialSelect = document.getElementById('returnSerialSelect');
  const reasonSelect = document.getElementById('returnReasonSelect');
  const refundInput = document.getElementById('returnRefundInput');

  if (!supplier || !serialSelect || !serialSelect.value) {
    showToast('Vui lòng chọn mã Serial lỗi cần xuất trả!', 'warning');
    return;
  }

  const serialCode = serialSelect.value;
  const reason = reasonSelect.value;
  const refundValue = Number(refundInput.value) || 0;

  const serialObj = ChronoDB.getSerial(serialCode);
  if (!serialObj) return;

  // Cập nhật trạng thái Serial
  serialObj.status = 'RETURNED_SUPPLIER';
  serialObj.shelfLocation = 'Đã xuất trả NCC';
  (serialObj.timeline = serialObj.timeline || []).push({
    date: new Date().toISOString().slice(0, 16).replace('T', ' '),
    title: 'Xuất trả NCC hoàn tiền',
    desc: `Trả cho NCC ${supplier.name}. Lý do: ${reason}. Cấn trừ nợ: ${formatVND(refundValue)}`
  });
  ChronoDB.saveSerial(serialObj);

  // Tạo phiếu trả hàng NCC
  const returnCode = 'XT-2026-' + (ChronoDB.getSupplierReturns().length + 1).toString().padStart(3, '0');
  ChronoDB.addSupplierReturn({
    id: returnCode,
    supplierId: supplier.id,
    supplierName: supplier.name,
    date: new Date().toISOString().slice(0, 10),
    watchId: serialObj.sku,
    watchName: serialObj.watchName,
    serials: [serialCode],
    quantity: 1,
    refundValue: refundValue,
    reason: reason,
    status: 'APPROVED',
    createdBy: 'Thủ kho (Lê Tuấn)'
  });

  // Ghi Thẻ kho
  ChronoDB.addStockCard({
    id: 'TK-' + Date.now().toString().slice(-4),
    date: new Date().toISOString().slice(0, 16).replace('T', ' '),
    watchId: serialObj.sku,
    sku: serialObj.sku,
    watchName: serialObj.watchName,
    refType: 'TRẢ_NCC',
    refCode: returnCode,
    changeQty: -1,
    balanceAfter: 0,
    serialNumber: serialCode,
    user: 'Thủ kho (Lê Tuấn)',
    note: `Xuất trả hàng lỗi cho ${supplier.name} (-${formatShortVND(refundValue)})`
  });

  closeModal('generalDetailModal');
  showToast(`Đã xuất trả thành công Serial ${serialCode} cho NCC theo ${returnCode}!`, 'success');
  renderInboundTab();
  if (typeof renderWarehouseTab === 'function') renderWarehouseTab();
  if (typeof renderDashboard === 'function') renderDashboard();
}

// Print Inbound Receipt A4 (2.2)
function printReceiptA4(receiptCode) {
  const rcpt = ChronoDB.getReceipts().find(r => r.code === receiptCode);
  if (!rcpt) return;

  const printWindow = window.open('', '_blank');
  if (!printWindow) {
    showToast('Trình duyệt đã chặn cửa sổ in (Pop-up). Vui lòng cho phép mở cửa sổ.', 'warning');
    return;
  }

  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Phiếu Nhập Kho - ${rcpt.code}</title>
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
          <div>Kho Tổng Phân Phối Đồng Hồ Chính Hãng</div>
          <div>Địa chỉ: Tòa nhà Horology Center, Q. Tân Bình, TP.HCM</div>
        </div>
        <div style="text-align:right;">
          <div>Mẫu số: <b>01-VT/B2B</b></div>
          <div>Số phiếu: <b>${rcpt.code}</b></div>
          <div>Ngày: <b>${rcpt.date}</b></div>
        </div>
      </div>

      <div class="title">PHIẾU NHẬP KHO KIÊM BIÊN BẢN KIỂM NGHIỆM ĐỒNG HỒ</div>

      <div class="meta-row">
        <div>Nhà cung cấp: <b>${rcpt.supplierName}</b></div>
        <div>Mã phiếu: <b>${rcpt.code}</b></div>
      </div>
      <div class="meta-row">
        <div>Địa điểm nhập: <b>Kho Tổng Tân Bình - TP.HCM</b></div>
        <div>Chi phí phân bổ: <b>${formatVND(rcpt.allocatedExpenses || 0)}</b></div>
      </div>

      <table>
        <thead>
          <tr>
            <th>STT</th>
            <th>Mã SKU</th>
            <th>Tên Đồng Hồ</th>
            <th>ĐVT Nhập</th>
            <th>SL Quy Đổi (Chiếc)</th>
            <th>Đơn Giá Vốn</th>
            <th>Thành Tiền</th>
          </tr>
        </thead>
        <tbody>
          ${rcpt.items.map((it, idx) => `
            <tr>
              <td style="text-align:center;">${idx + 1}</td>
              <td><b>${it.sku}</b></td>
              <td>${it.name}</td>
              <td>${it.quantity} ${it.unit}</td>
              <td style="text-align:center; font-weight:bold;">${it.convertedQty}</td>
              <td>${formatVND(it.unitCost)}</td>
              <td><b>${formatVND(it.subtotal)}</b></td>
            </tr>
          `).join('')}
          <tr>
            <td colspan="6" style="text-align:right; font-weight:bold;">TỔNG CỘNG GIÁ TRỊ NHẬP:</td>
            <td style="font-weight:bold; font-size:13px;">${formatVND(rcpt.totalAmount)}</td>
          </tr>
        </tbody>
      </table>

      <div class="serials-box">
        <b>BẢNG MÃ SERIAL NUMBER ĐÍCH DANH THEO TỪNG CHIẾC:</b><br>
        ${rcpt.items.map(it => `
          <div><b>${it.name}:</b> ${(it.serials || []).join(', ')}</div>
        `).join('')}
      </div>

      <div class="signatures">
        <div class="sig-block">
          <b>Người Lập Phiếu</b>
          <div class="sig-space"></div>
          <div>Nguyễn Văn Lập</div>
        </div>
        <div class="sig-block">
          <b>Đại Diện NCC</b>
          <div class="sig-space"></div>
          <div>${rcpt.supplierName.slice(0, 20)}</div>
        </div>
        <div class="sig-block">
          <b>Thủ Kho</b>
          <div class="sig-space"></div>
          <div>Lê Tuấn</div>
        </div>
        <div class="sig-block">
          <b>Kế Toán Trưởng</b>
          <div class="sig-space"></div>
          <div>Phạm Thị Lan</div>
        </div>
      </div>

      <script>window.onload = function() { window.print(); };</script>
    </body>
    </html>
  `);
  printWindow.document.close();
}
