/**
 * CHRONO VAULT B2B - PHÂN HỆ 5 (THÀNH VIÊN 5)
 * Dashboard Điều Hành, KPI Cards, Biểu Đồ Canvas, Sổ Công Nợ 2 Chiều & Báo Cáo Dòng Tiền
 */

// Render Main Dashboard (KPIs, Charts, Recent Activity)
function renderDashboard() {
  const watches = ChronoDB.getWatches();
  const serials = ChronoDB.getSerials();
  const orders = ChronoDB.getOrders();
  const receipts = ChronoDB.getReceipts();
  const logs = ChronoDB.getLogs();

  // 1. Calculate KPI Values
  // Tổng giá trị tồn kho đích danh: Cộng dồn giá vốn đích danh của từng Serial IN_STOCK / RESERVED
  const totalValuation = serials
    .filter(s => s.status === 'IN_STOCK' || s.status === 'RESERVED')
    .reduce((sum, s) => sum + (s.costPrice || 0), 0);

  // Tổng doanh thu sỉ B2B từ các đơn hàng
  const totalRevenue = orders
    .filter(o => o.status !== 'CANCELLED')
    .reduce((sum, o) => sum + (o.totalAmount || 0), 0);

  const completedOrdersCount = orders.length;
  const inStockPiecesCount = serials.filter(s => s.status === 'IN_STOCK').length;

  // Cập nhật DOM KPI Cards
  const valElem = document.getElementById('kpiTotalValuation');
  const revElem = document.getElementById('kpiRevenue');
  const ordElem = document.getElementById('kpiOrdersCount');
  const stkElem = document.getElementById('kpiInStockCount');

  if (valElem) valElem.textContent = formatVND(totalValuation);
  if (revElem) revElem.textContent = formatVND(totalRevenue);
  if (ordElem) ordElem.textContent = completedOrdersCount;
  if (stkElem) stkElem.textContent = inStockPiecesCount;

  // 2. Render Revenue Canvas Chart
  renderRevenueChart();

  // 3. Render Dashboard Recent Activities Log
  const logContainer = document.getElementById('dashboardActivityLogs');
  if (logContainer) {
    const recentLogs = logs.slice(0, 5);
    logContainer.innerHTML = recentLogs.map(log => `
      <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-content">
          <div class="timeline-time">${log.time}</div>
          <div class="timeline-user">👤 ${log.user}</div>
          <div class="timeline-action">
            <span class="log-badge-action">${log.action}</span>: ${log.target}
          </div>
        </div>
      </div>
    `).join('');
  }
}

// Render Revenue Canvas Chart (6 Months Trend)
function renderRevenueChart() {
  const canvas = document.getElementById('revenueCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const width = rect.width || 340;
  const height = rect.height || 180;

  canvas.width = width * dpr;
  canvas.height = height * dpr;
  ctx.scale(dpr, dpr);

  // Dữ liệu doanh thu 6 tháng gần nhất (tính bằng triệu đồng)
  const months = ['T05', 'T06', 'T07', 'T08', 'T09', 'T10'];
  const values = [1250, 1580, 1890, 2450, 2980, 3450]; // Triệu VND

  const maxVal = Math.max(...values) * 1.15;
  const paddingLeft = 45;
  const paddingRight = 15;
  const paddingTop = 25;
  const paddingBottom = 30;

  const chartWidth = width - paddingLeft - paddingRight;
  const chartHeight = height - paddingTop - paddingBottom;

  ctx.clearRect(0, 0, width, height);

  // 1. Grid Lines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.lineWidth = 1;
  const gridRows = 4;
  for (let i = 0; i <= gridRows; i++) {
    const y = paddingTop + (chartHeight / gridRows) * i;
    ctx.beginPath();
    ctx.moveTo(paddingLeft, y);
    ctx.lineTo(width - paddingRight, y);
    ctx.stroke();

    const labelVal = Math.round(maxVal - (maxVal / gridRows) * i);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.font = '10px Inter, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(labelVal + 'tr', paddingLeft - 6, y + 3);
  }

  // 2. Points coordinates
  const points = values.map((val, idx) => {
    const x = paddingLeft + (chartWidth / (values.length - 1)) * idx;
    const y = paddingTop + chartHeight - (val / maxVal) * chartHeight;
    return { x, y, val };
  });

  // 3. Fill Gradient under Line
  const gradient = ctx.createLinearGradient(0, paddingTop, 0, height - paddingBottom);
  gradient.addColorStop(0, 'rgba(212, 175, 55, 0.35)');
  gradient.addColorStop(1, 'rgba(212, 175, 55, 0.0)');

  ctx.beginPath();
  ctx.moveTo(points[0].x, points[0].y);
  for (let i = 1; i < points.length; i++) {
    const xc = (points[i - 1].x + points[i].x) / 2;
    const yc = (points[i - 1].y + points[i].y) / 2;
    ctx.quadraticCurveTo(points[i - 1].x, points[i - 1].y, xc, yc);
  }
  ctx.lineTo(points[points.length - 1].x, points[points.length - 1].y);
  ctx.lineTo(points[points.length - 1].x, height - paddingBottom);
  ctx.lineTo(points[0].x, height - paddingBottom);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();

  // 4. Draw Smooth Gold Line
  ctx.beginPath();
  ctx.moveTo(points[0].x, points[0].y);
  for (let i = 1; i < points.length; i++) {
    const xc = (points[i - 1].x + points[i].x) / 2;
    const yc = (points[i - 1].y + points[i].y) / 2;
    ctx.quadraticCurveTo(points[i - 1].x, points[i - 1].y, xc, yc);
  }
  ctx.lineTo(points[points.length - 1].x, points[points.length - 1].y);
  ctx.strokeStyle = '#D4AF37';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // 5. Dots & Month Labels
  points.forEach((p, idx) => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#0F1117';
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#D4AF37';
    ctx.stroke();

    ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.font = '10px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(months[idx], p.x, height - paddingBottom + 16);
  });
}

// Open Sổ Chi Tiết Công Nợ 2 Chiều (5.2)
function openDebtLedgerModal() {
  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  const dealers = ChronoDB.getDealers();
  const suppliers = ChronoDB.getSuppliers();

  titleElem.innerHTML = `📊 Sổ Chi Tiết Công Nợ B2B (Đại Lý & Nhà Cung Cấp)`;
  bodyElem.innerHTML = `
    <div class="modal-detail-wrap">
      <!-- Section 1: Công nợ Phải Thu Đại Lý B2B -->
      <div class="section-subtitle">🏪 1. SỔ CÔNG NỢ PHẢI THU ĐẠI LÝ BÁN SỈ B2B</div>
      <table class="data-table-spec">
        <thead>
          <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
            <th>Đại Lý</th>
            <th>Hạng</th>
            <th>Hạn Mức Tín Dụng</th>
            <th>Dư Nợ Hiện Tại</th>
            <th>Khả Dụng</th>
          </tr>
        </thead>
        <tbody>
          ${dealers.map(d => `
            <tr>
              <td><b>${d.shopName}</b><br><small style="color:var(--text-muted);">${d.taxCode || ''}</small></td>
              <td><span class="badge-status ${d.tier === 'VIP' ? 'status-vip' : 'status-completed'}">${d.tier}</span></td>
              <td>${formatVND(d.creditLimit)}</td>
              <td><b style="color:var(--danger);">${formatVND(d.currentDebt)}</b></td>
              <td><b style="color:var(--success);">${formatVND(d.availableCredit)}</b></td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <!-- Section 2: Công nợ Phải Trả Nhà Cung Cấp -->
      <div class="section-subtitle" style="margin-top:20px;">🏢 2. SỔ CÔNG NỢ PHẢI TRẢ NHÀ CUNG CẤP (SUPPLIERS)</div>
      <table class="data-table-spec">
        <thead>
          <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
            <th>Nhà Cung Cấp</th>
            <th>Mã Số Thuế</th>
            <th>Tài Khoản Ngân Hàng</th>
            <th>Dư Nợ Phải Trả NCC</th>
          </tr>
        </thead>
        <tbody>
          ${suppliers.map(s => `
            <tr>
              <td><b>${s.name}</b></td>
              <td>${s.taxCode}</td>
              <td><small>${s.bankAccount || ''} - ${s.bankName || ''}</small></td>
              <td><b style="color:var(--danger); font-size:13px;">${formatVND(s.debtBalance)}</b></td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div style="margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
        <button class="btn-toggle-view" onclick="exportDebtLedgerToCSV()">📥 Xuất File Sổ Công Nợ Excel</button>
        <button class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Đóng</button>
      </div>
    </div>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Open Báo Cáo Dòng Tiền Thu / Chi Thực Tế (5.2)
function openCashflowReportModal() {
  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  const receipts = ChronoDB.getDealerReceipts();
  const payments = ChronoDB.getSupplierPayments();

  const totalInflow = receipts.reduce((sum, r) => sum + (r.amount || 0), 0);
  const totalOutflow = payments.reduce((sum, p) => sum + (p.amount || 0), 0);
  const netCashflow = totalInflow - totalOutflow;

  titleElem.innerHTML = `💵 Báo Cáo Dòng Tiền Thu / Chi Thực Tế`;
  bodyElem.innerHTML = `
    <div class="modal-detail-wrap">
      <div class="detail-kpi-bar">
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Tổng Thu Thực Tế (Inflow)</span>
          <span class="kpi-mini-val" style="color:var(--success);">${formatShortVND(totalInflow)}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Tổng Chi Thực Tế (Outflow)</span>
          <span class="kpi-mini-val" style="color:var(--danger);">${formatShortVND(totalOutflow)}</span>
        </div>
        <div class="kpi-mini">
          <span class="kpi-mini-lbl">Dòng Tiền Ròng (Net)</span>
          <span class="kpi-mini-val" style="color:${netCashflow >= 0 ? 'var(--gold-light)' : 'var(--danger)'};">${formatShortVND(netCashflow)}</span>
        </div>
      </div>

      <!-- Inflow Transactions -->
      <div class="section-subtitle" style="margin-top:16px;">📈 CÁC KHOẢN THU BÁN SỈ THỰC TẾ (${receipts.length} phiếu thu)</div>
      <table class="data-table-spec">
        <thead>
          <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
            <th>Mã Phiếu</th>
            <th>Ngày Thu</th>
            <th>Đại Lý Nộp Tiền</th>
            <th>Hình Thức</th>
            <th>Số Tiền Thu</th>
          </tr>
        </thead>
        <tbody>
          ${receipts.map(r => `
            <tr>
              <td><b>${r.id}</b></td>
              <td>${r.date}</td>
              <td>${r.dealerName}</td>
              <td><small>${r.paymentMethod}</small></td>
              <td><b style="color:var(--success);">${formatVND(r.amount)}</b></td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <!-- Outflow Transactions -->
      <div class="section-subtitle" style="margin-top:20px;">📉 CÁC KHOẢN CHI TRẢ TIỀN HÀNG NCC (${payments.length} phiếu chi)</div>
      <table class="data-table-spec">
        <thead>
          <tr style="background:rgba(255,255,255,0.05); font-size:11px;">
            <th>Mã Phiếu</th>
            <th>Ngày Chi</th>
            <th>Nhà Cung Cấp Thụ Hưởng</th>
            <th>Hình Thức</th>
            <th>Số Tiền Chi</th>
          </tr>
        </thead>
        <tbody>
          ${payments.map(p => `
            <tr>
              <td><b>${p.id}</b></td>
              <td>${p.date}</td>
              <td>${p.supplierName}</td>
              <td><small>${p.paymentMethod}</small></td>
              <td><b style="color:var(--danger);">${formatVND(p.amount)}</b></td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div style="margin-top:20px; display:flex; justify-content:flex-end;">
        <button class="btn-secondary-action" onclick="closeModal('generalDetailModal')">Đóng</button>
      </div>
    </div>
  `;
  document.getElementById('generalDetailModal').classList.add('active');
}

// Export Debt Ledger to CSV / Excel
function exportDebtLedgerToCSV() {
  const dealers = ChronoDB.getDealers();
  const suppliers = ChronoDB.getSuppliers();

  let csv = "PHAN_HE,DOI_TAC,MA_SO_THUE,HANG,HAN_MUC_TIN_DUNG,DU_NO_HIEN_TAI,HAN_MUC_KHA_DUNG\n";
  dealers.forEach(d => {
    csv += `"DAI_LY_SI","${d.shopName}","${d.taxCode || ''}","${d.tier}",${d.creditLimit},${d.currentDebt},${d.availableCredit}\n`;
  });
  suppliers.forEach(s => {
    csv += `"NHA_CUNG_CAP","${s.name}","${s.taxCode}","NCC",0,${s.debtBalance},0\n`;
  });

  const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `So_Cong_No_B2B_ChronoVault_${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  showToast('Đã xuất Sổ Chi Tiết Công Nợ thành công!', 'success');
}
