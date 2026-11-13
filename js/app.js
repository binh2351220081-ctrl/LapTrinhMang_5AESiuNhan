/**
 * CHRONO VAULT B2B - MAIN CONTROLLER & APPLICATION ROUTER
 * Kết nối 5 phân hệ TV1, TV2, TV3, TV4, TV5 và quản lý sự kiện toàn cục
 */

// App State
const AppState = {
  currentTab: 'dashboard',
  selectedWarehouse: 'Kho Tổng Tân Bình - TP.HCM',
  audioCtx: null
};

// Sound feedback using Web Audio API
function playBeep(freq = 1200, type = 'sine', duration = 0.08) {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AppState.audioCtx) {
      AppState.audioCtx = new AudioContext();
    }
    const ctx = AppState.audioCtx;
    if (ctx.state === 'suspended') {
      ctx.resume();
    }
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + duration);
  } catch (e) {
    // Audio blocked by browser policy
  }
}

// Toast Notifications
function showToast(msg, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast-msg toast-${type}`;
  
  let iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>`;
  if (type === 'success') {
    iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`;
  } else if (type === 'warning') {
    iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
  } else if (type === 'danger') {
    iconSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`;
  }
  
  toast.innerHTML = `${iconSvg} <span>${msg}</span>`;
  container.appendChild(toast);
  playBeep(type === 'success' ? 1400 : (type === 'danger' ? 700 : 900), 'sine', 0.1);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// Dynamic Island Alert simulation
function flashDynamicIsland(text) {
  const island = document.getElementById('dynamicIsland');
  const statusSpan = document.getElementById('islandStatus');
  if (!island || !statusSpan) return;
  statusSpan.textContent = text;
  island.classList.add('expanded');
  setTimeout(() => {
    island.classList.remove('expanded');
  }, 2800);
}

// Update Native Status Clock
function startClock() {
  const timeElem = document.getElementById('phoneClock');
  if (!timeElem) return;
  const update = () => {
    const now = new Date();
    const h = now.getHours().toString().padStart(2, '0');
    const m = now.getMinutes().toString().padStart(2, '0');
    timeElem.textContent = `${h}:${m}`;
  };
  update();
  setInterval(update, 1000);
}

// Navigation Tab Switching
function switchTab(tabId) {
  AppState.currentTab = tabId;
  document.querySelectorAll('.tab-view').forEach(view => view.classList.remove('active'));
  document.querySelectorAll('.nav-item-btn').forEach(btn => btn.classList.remove('active'));

  const targetView = document.getElementById(`tab-${tabId}`);
  if (targetView) targetView.classList.add('active');

  const targetBtn = document.querySelector(`.nav-item-btn[data-tab="${tabId}"]`);
  if (targetBtn) targetBtn.classList.add('active');

  const scrollContainer = document.getElementById('phoneContent');
  if (scrollContainer) scrollContainer.scrollTop = 0;

  // Render view data according to tab
  if (tabId === 'dashboard' && typeof renderDashboard === 'function') {
    renderDashboard();
  } else if (tabId === 'products' && typeof renderProductsList === 'function') {
    renderProductsList();
  } else if (tabId === 'inbound' && typeof renderInboundTab === 'function') {
    renderInboundTab();
  } else if (tabId === 'outbound' && typeof renderOutboundTab === 'function') {
    renderOutboundTab();
  } else if (tabId === 'warehouse' && typeof renderWarehouseTab === 'function') {
    renderWarehouseTab();
  }

  playBeep(1100, 'sine', 0.04);
}

// Toggle Side Drawer
function toggleDrawer() {
  const drawer = document.getElementById('sideDrawer');
  const backdrop = document.getElementById('drawerBackdrop');
  if (!drawer || !backdrop) return;
  const isOpen = drawer.classList.contains('active');
  if (isOpen) {
    drawer.classList.remove('active');
    backdrop.classList.remove('active');
  } else {
    drawer.classList.add('active');
    backdrop.classList.add('active');
  }
}

// Close Modal helper
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

// Toggle Desktop Fullscreen / Mobile simulator mode
function toggleViewportMode() {
  const wrapper = document.getElementById('phoneWrapper');
  const btnText = document.getElementById('btnToggleViewText');
  if (!wrapper) return;

  const isFull = wrapper.classList.toggle('full-screen-mode');
  if (btnText) {
    btnText.textContent = isFull ? 'Chuyển Khung Mobile' : 'Toàn màn hình Tablet/PC';
  }
  showToast(isFull ? 'Đã chuyển sang chế độ Toàn Màn Hình' : 'Đã chuyển sang Khung Mobile App', 'info');
  if (typeof renderRevenueChart === 'function') {
    setTimeout(renderRevenueChart, 250);
  }
}

// Global Search in products tab
function initSearchListeners() {
  const searchInput = document.getElementById('productsSearchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      if (typeof renderProductsList === 'function') {
        renderProductsList(null, e.target.value);
      }
    });
  }
}

// App Initialization
window.addEventListener('DOMContentLoaded', () => {
  ChronoDB.init();
  startClock();
  initSearchListeners();

  // Initial render of active tab
  if (typeof renderDashboard === 'function') renderDashboard();
  if (typeof renderProductsList === 'function') renderProductsList();
  if (typeof renderInboundTab === 'function') renderInboundTab();
  if (typeof renderOutboundTab === 'function') renderOutboundTab();
  if (typeof renderWarehouseTab === 'function') renderWarehouseTab();

  flashDynamicIsland('ChronoVault WMS Sẵn Sàng');
});
