/**
 * CHRONO VAULT B2B - PHÂN HỆ 1.2 (THÀNH VIÊN 1)
 * Quản trị Hệ thống, Tài khoản người dùng, Ma trận Phân quyền & Nhật ký Audit Log
 */

// Open System Admin Modal (Tài khoản & Phân quyền)
function openSystemAdminModal() {
  const titleElem = document.getElementById('generalModalTitle');
  const bodyElem = document.getElementById('generalModalBody');
  if (!titleElem || !bodyElem) return;

  const accounts = ChronoDB.getAccounts();
  const roles = ChronoDB.getRoles();

  titleElem.innerHTML = `🛡️ Quản Trị Hệ Thống & Phân Quyền Nhân Sự`;
  bodyElem.innerHTML = `
    <div class="system-admin-wrap">
      <!-- Tabs navigation inside modal -->
      <div class="sub-tab-bar">
        <button class="sub-tab-btn active" id="tabBtnAccounts" onclick="switchSystemSubTab('accounts')">👥 Danh Sách Tài Khoản (${accounts.length})</button>
        <button class="sub-tab-btn" id="tabBtnRoles" onclick="switchSystemSubTab('roles')">🔐 Ma Trận Phân Quyền</button>
        <button class="sub-tab-btn" id="tabBtnAudit" onclick="switchSystemSubTab('audit')">📜 Nhật Ký Audit Log</button>
      </div>

      <!-- Section 1: Accounts List -->
      <div class="sub-tab-content active" id="systemTabAccounts">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <span style="font-size:12px; color:var(--text-secondary);">Nhân sự vận hành 5 phân hệ kho B2B:</span>
          <button class="btn-primary-action" style="width:auto; padding:5px 12px; font-size:11px;" onclick="openAddAccountModal()">+ Cấp Mới Tài Khoản</button>
        </div>

        <div class="accounts-cards-list">
          ${accounts.map(acc => `
            <div class="account-item-card">
              <div class="acc-avatar">${acc.avatar || 'US'}</div>
              <div class="acc-meta">
                <div class="acc-name">${acc.fullName} <span class="acc-username">(@${acc.username})</span></div>
                <div class="acc-role">${acc.roleName} • ${acc.email}</div>
                <div class="acc-login">Lần đăng nhập cuối: ${acc.lastLogin || 'Chưa ghi nhận'}</div>
              </div>
              <div class="acc-actions">
                <span class="badge-status ${acc.status === 'ACTIVE' ? 'status-completed' : 'status-danger'}">
                  ${acc.status === 'ACTIVE' ? 'Hoạt Động' : 'Đã Khóa'}
                </span>
                <button class="btn-action-small" onclick="toggleAccountStatus('${acc.id}')" style="margin-top:6px;">
                  ${acc.status === 'ACTIVE' ? '🔒 Khóa' : '🔓 Mở Khóa'}
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Section 2: Roles Matrix -->
      <div class="sub-tab-content" id="systemTabRoles" style="display:none;">
        <div style="font-size:12px; color:var(--text-secondary); margin-bottom:12px;">
          Ma trận phân quyền chi tiết (Role - Permission Matrix) theo tài liệu thiết kế CSDL:
        </div>
        
        <div class="role-matrix-table-wrap">
          <table class="role-matrix-table">
            <thead>
              <tr>
                <th>Nhóm Vai Trò (Role)</th>
                <th>Phân Hệ 1 (Hàng Hóa)</th>
                <th>Phân Hệ 2 (Nhập NCC)</th>
                <th>Phân Hệ 3 (Xuất Kho Đại Lý)</th>
                <th>Phân Hệ 4 (Kho Kệ)</th>
                <th>Phân Hệ 5 (Báo Cáo)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><b>🛡️ Quản trị hệ thống</b><br><small>Quản lý tài khoản, vai trò & nhật ký</small></td>
                <td><span class="perm-tag write">Quản lý danh mục hệ thống</span></td>
                <td><span class="perm-tag read">Xem, không xử lý phiếu</span></td>
                <td><span class="perm-tag read">Xem, không xử lý đơn</span></td>
                <td><span class="perm-tag read">Xem nhật ký</span></td>
                <td><span class="perm-tag read">Xem báo cáo</span></td>
              </tr>
              <tr>
                <td><b>📦 Thủ Kho</b><br><small>Quản lý vật lý</small></td>
                <td><span class="perm-tag read">Chỉ xem</span></td>
                <td><span class="perm-tag write">Xác nhận nhận hàng</span></td>
                <td><span class="perm-tag write">Xác nhận xuất vật lý</span></td>
                <td><span class="perm-tag full">Kệ, kiểm kê, cân bằng trong ngưỡng</span></td>
                <td><span class="perm-tag read">Báo cáo tồn kho</span></td>
              </tr>
              <tr>
                <td><b>📥📤 Nhân viên nhập/xuất kho</b><br><small>Tác nghiệp giao dịch</small></td>
                <td><span class="perm-tag read">Tra cứu sản phẩm</span></td>
                <td><span class="perm-tag full">Lập phiếu, quét Serial</span></td>
                <td><span class="perm-tag full">Lập đơn nháp, soạn và xuất</span></td>
                <td><span class="perm-tag read">Tra cứu, đề nghị điều chuyển</span></td>
                <td><span class="perm-tag read">Báo cáo nghiệp vụ</span></td>
              </tr>
              <tr>
                <td><b>📊 Kế Toán</b><br><small>Công nợ & Dòng tiền</small></td>
                <td><span class="perm-tag read">Chỉ xem</span></td>
                <td><span class="perm-tag write">Phân bổ chi phí, đối soát</span></td>
                <td><span class="perm-tag write">Kiểm tra công nợ</span></td>
                <td><span class="perm-tag read">Đối soát thẻ kho</span></td>
                <td><span class="perm-tag full">Thu chi, công nợ, tài chính</span></td>
              </tr>
              <tr>
                <td><b>👑 Chủ cửa hàng</b><br><small>Điều hành & duyệt ngoại lệ</small></td>
                <td><span class="perm-tag read">Xem</span></td>
                <td><span class="perm-tag write">Duyệt chi vượt ngưỡng</span></td>
                <td><span class="perm-tag write">Duyệt ngoại lệ tín dụng</span></td>
                <td><span class="perm-tag write">Duyệt cân bằng vượt ngưỡng</span></td>
                <td><span class="perm-tag full">Dashboard, báo cáo, xuất</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Section 3: Audit Log Trail -->
      <div class="sub-tab-content" id="systemTabAudit" style="display:none;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <span style="font-size:12px; color:var(--text-secondary);">Nhật ký truy vết thao tác thời gian thực:</span>
          <select class="wh-select" style="font-size:11px; padding:3px 8px;" onchange="filterAuditLogsInModal(this.value)">
            <option value="ALL">Tất cả hành động</option>
            <option value="TẠO_ĐƠN_SỈ">Lệnh xuất kho đại lý</option>
            <option value="THU_TIỀN_SỈ">Thu hồi công nợ đại lý</option>
            <option value="CHI_TRẢ_NCC">Chi trả NCC</option>
            <option value="KIỂM_KÊ_KHO">Kiểm kê kệ</option>
            <option value="NHẬP_TRẢ_HÀNG">Đổi trả hàng</option>
          </select>
        </div>
        <div class="timeline-flow" id="modalAuditLogsContainer"></div>
      </div>

    </div>
  `;

  renderAuditLogsInModal('ALL');
  document.getElementById('generalDetailModal').classList.add('active');
}

// Switch Sub Tabs inside System Admin
function switchSystemSubTab(tabName) {
  document.querySelectorAll('.sub-tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.sub-tab-content').forEach(c => {
    c.classList.remove('active');
    c.style.display = 'none';
  });

  if (tabName === 'accounts') {
    document.getElementById('tabBtnAccounts').classList.add('active');
    document.getElementById('systemTabAccounts').style.display = 'block';
  } else if (tabName === 'roles') {
    document.getElementById('tabBtnRoles').classList.add('active');
    document.getElementById('systemTabRoles').style.display = 'block';
  } else if (tabName === 'audit') {
    document.getElementById('tabBtnAudit').classList.add('active');
    document.getElementById('systemTabAudit').style.display = 'block';
    renderAuditLogsInModal('ALL');
  }
}

// Open Add Account Modal
function openAddAccountModal() {
  const username = prompt("Nhập Tên đăng nhập (Username) cho nhân viên mới:");
  if (!username) return;
  const fullName = prompt("Nhập Họ và tên nhân viên:");
  if (!fullName) return;
  const role = prompt("Chọn Vai trò (ADMIN / KHO / NHANVIEN_KHO / KETOAN / OWNER):", "NHANVIEN_KHO");
  if (!role) return;

  const roleUpper = role.trim().toUpperCase();
  const roleMap = {
    'ADMIN': 'Quản Trị Viên (Admin)',
    'KHO': 'Thủ Kho',
    'NHANVIEN_KHO': 'Nhân Viên Nhập/Xuất Kho',
    'KETOAN': 'Kế Toán',
    'OWNER': 'Chủ Cửa Hàng'
  };
  if (!roleMap[roleUpper]) {
    showToast('Vai trò không hợp lệ. Hãy chọn một trong 5 vai trò đã khai báo.', 'error');
    return;
  }

  const newAcc = {
    id: 'USR' + (ChronoDB.getAccounts().length + 1).toString().padStart(2, '0'),
    username: username.trim().toLowerCase(),
    fullName: fullName.trim(),
    email: `${username.trim().toLowerCase()}@chronovault.com`,
    role: roleUpper,
    roleName: roleMap[roleUpper] || 'Nhân Viên',
    status: 'ACTIVE',
    avatar: fullName.trim().slice(0, 2).toUpperCase(),
    lastLogin: 'Vừa tạo'
  };

  ChronoDB.saveAccount(newAcc);
  ChronoDB.logAction('Admin (Trần Bảo)', 'CẤP_TÀI_KHOẢN', `Cấp tài khoản mới: @${newAcc.username} (${newAcc.roleName})`);
  showToast(`Đã cấp mới tài khoản cho ${newAcc.fullName}!`, 'success');
  openSystemAdminModal();
}

// Toggle Account Status (Lock / Unlock)
function toggleAccountStatus(accId) {
  const accounts = ChronoDB.getAccounts();
  const acc = accounts.find(a => a.id === accId);
  if (!acc) return;

  acc.status = (acc.status === 'ACTIVE') ? 'LOCKED' : 'ACTIVE';
  ChronoDB.setAccounts(accounts);
  ChronoDB.logAction('Admin (Trần Bảo)', 'KHÓA_MỞ_USER', `Thay đổi trạng thái tài khoản @${acc.username}: ${acc.status}`);
  showToast(`Tài khoản @${acc.username} hiện ở trạng thái: ${acc.status === 'ACTIVE' ? 'Đang hoạt động' : 'Đã khóa'}`, 'info');
  openSystemAdminModal();
}

// Render Audit Logs In Modal
function renderAuditLogsInModal(filterAction = 'ALL') {
  const container = document.getElementById('modalAuditLogsContainer');
  if (!container) return;

  const logs = ChronoDB.getLogs();
  const filtered = (filterAction === 'ALL') ? logs : logs.filter(l => l.action === filterAction);

  if (filtered.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:16px; color:var(--text-muted); font-size:12px;">Không có nhật ký nào cho hành động này</div>`;
    return;
  }

  container.innerHTML = filtered.map(log => `
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

function filterAuditLogsInModal(val) {
  renderAuditLogsInModal(val);
}
