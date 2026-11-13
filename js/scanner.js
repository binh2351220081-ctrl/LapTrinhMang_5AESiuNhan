/**
 * CHRONO VAULT B2B - CAMERA SCANNER MODULE
 * Tích hợp ZXing Barcode/QR Code Library & Web BarcodeDetector API
 * Hỗ trợ quét mã vạch EAN-13, Code 128, QR Code, Serial Number
 */

let activeCameraStream = null;
let activeFacingMode = 'environment';
let isFlashActive = false;
let barcodeDetectionTimer = null;
let nativeDetector = null;
let zxingCodeReader = null;
let isScannerBusy = false;

// Initialize Barcode Detectors
function initBarcodeEngines() {
  if ('BarcodeDetector' in window && !nativeDetector) {
    try {
      nativeDetector = new BarcodeDetector({
        formats: ['code_128', 'code_39', 'ean_13', 'ean_8', 'qr_code', 'upc_a', 'data_matrix']
      });
    } catch (e) {
      console.warn('BarcodeDetector error:', e);
    }
  }

  if (window.ZXing && window.ZXing.BrowserMultiFormatReader && !zxingCodeReader) {
    try {
      zxingCodeReader = new window.ZXing.BrowserMultiFormatReader();
    } catch (e) {
      console.warn('ZXing init error:', e);
    }
  }
}

// Open Scanner Modal and Start Live Camera
async function openScannerModal(targetAction = 'LOOKUP') {
  const modal = document.getElementById('scannerModal');
  if (!modal) return;
  modal.dataset.action = targetAction;
  modal.classList.add('active');

  initBarcodeEngines();
  if (typeof playBeep === 'function') playBeep(1400, 'square', 0.08);
  if (typeof flashDynamicIsland === 'function') flashDynamicIsland('Đang kết nối Camera...');
  
  await startCameraStream();
}

// Start User Media Video Stream
async function startCameraStream() {
  const video = document.getElementById('scannerVideo');
  const overlay = document.getElementById('scannerStatusOverlay');
  const statusText = document.getElementById('cameraStatusText');
  const spinner = document.getElementById('cameraSpinner');
  const grantBtn = document.getElementById('btnGrantCam');

  if (!video) return;

  if (overlay) {
    overlay.style.display = 'flex';
    if (spinner) spinner.style.display = 'block';
    if (statusText) statusText.textContent = 'Đang khởi động Camera...';
    if (grantBtn) grantBtn.style.display = 'none';
  }

  stopCameraStream();

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    if (statusText) {
      statusText.innerHTML = `Trình duyệt không hỗ trợ trực tiếp Camera trong ngữ cảnh này.<br><small style="color:var(--text-muted);">Hãy chạy qua http://localhost hoặc dùng chức năng nhập mã bên dưới.</small>`;
    }
    if (spinner) spinner.style.display = 'none';
    return;
  }

  try {
    const constraints = {
      video: {
        facingMode: { ideal: activeFacingMode },
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    };

    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    activeCameraStream = stream;
    video.srcObject = stream;
    
    video.onloadedmetadata = () => {
      video.play().then(() => {
        if (overlay) overlay.style.display = 'none';
        if (typeof flashDynamicIsland === 'function') flashDynamicIsland('Camera đã sẵn sàng quét');
        startContinuousBarcodeDetection();
      }).catch(err => {
        console.warn('Video play error:', err);
      });
    };
  } catch (err) {
    console.error('Camera access error:', err);
    if (spinner) spinner.style.display = 'none';
    if (statusText) {
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        statusText.innerHTML = `Quyền truy cập Camera bị từ chối.<br><small style="color:var(--text-muted);">Vui lòng cấp quyền Camera trên thanh trình duyệt.</small>`;
        if (grantBtn) grantBtn.style.display = 'inline-block';
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        statusText.innerHTML = `Không tìm thấy thiết bị Camera trên máy này.<br><small style="color:var(--text-muted);">Bạn vẫn có thể nhập mã hoặc nhấp các mã mẫu bên dưới.</small>`;
      } else {
        statusText.innerHTML = `Lỗi Camera: ${err.message || 'Không thể kết nối'}`;
      }
    }
  }
}

// Stop Video Stream & Cleanup
function stopCameraStream() {
  if (barcodeDetectionTimer) {
    clearInterval(barcodeDetectionTimer);
    barcodeDetectionTimer = null;
  }
  if (zxingCodeReader) {
    try { zxingCodeReader.reset(); } catch (e) {}
  }
  if (activeCameraStream) {
    activeCameraStream.getTracks().forEach(track => {
      track.stop();
    });
    activeCameraStream = null;
  }
  const video = document.getElementById('scannerVideo');
  if (video) {
    video.srcObject = null;
  }
  isFlashActive = false;
  const reticle = document.getElementById('scannerReticle');
  if (reticle) reticle.classList.remove('detected');
}

// Switch Camera Facing (Back / Front)
async function switchCameraFacing() {
  activeFacingMode = (activeFacingMode === 'environment') ? 'user' : 'environment';
  if (typeof showToast === 'function') showToast(`Đang chuyển sang Camera: ${activeFacingMode === 'environment' ? 'Sau' : 'Trước'}`, 'info');
  await startCameraStream();
}

// Toggle Flash / Torch if supported
async function toggleCameraFlash() {
  if (!activeCameraStream) return;
  const videoTrack = activeCameraStream.getVideoTracks()[0];
  if (!videoTrack) return;

  const capabilities = videoTrack.getCapabilities ? videoTrack.getCapabilities() : {};
  if (!capabilities.torch) {
    if (typeof showToast === 'function') showToast('Thiết bị hoặc camera này không hỗ trợ đèn Flash', 'warning');
    return;
  }

  isFlashActive = !isFlashActive;
  try {
    await videoTrack.applyConstraints({
      advanced: [{ torch: isFlashActive }]
    });
    if (typeof showToast === 'function') showToast(`Đèn Flash: ${isFlashActive ? 'BẬT' : 'TẮT'}`, 'info');
    const flashBtn = document.getElementById('btnToggleFlash');
    if (flashBtn) {
      flashBtn.style.color = isFlashActive ? 'var(--gold-light)' : '';
      flashBtn.style.borderColor = isFlashActive ? 'var(--gold-primary)' : '';
    }
  } catch (e) {
    console.warn('Flash error:', e);
  }
}

// Continuous Frame Barcode Detection
function startContinuousBarcodeDetection() {
  if (barcodeDetectionTimer) clearInterval(barcodeDetectionTimer);
  const video = document.getElementById('scannerVideo');
  if (!video) return;

  if (zxingCodeReader && !nativeDetector) {
    try {
      zxingCodeReader.decodeFromVideoElement(video, (result, err) => {
        if (result && result.getText()) {
          onBarcodeDetected(result.getText());
        }
      });
      return;
    } catch (e) {
      console.warn('ZXing live stream failed, falling back to interval:', e);
    }
  }

  barcodeDetectionTimer = setInterval(async () => {
    if (isScannerBusy || video.readyState < 2) return;

    if (nativeDetector) {
      try {
        isScannerBusy = true;
        const barcodes = await nativeDetector.detect(video);
        if (barcodes && barcodes.length > 0) {
          const code = barcodes[0].rawValue;
          if (code) {
            onBarcodeDetected(code);
          }
        }
      } catch (e) {
        // frame decode skip
      } finally {
        isScannerBusy = false;
      }
    }
  }, 250);
}

// Handle Barcode Detection Success
function onBarcodeDetected(detectedCode) {
  if (!detectedCode) return;
  detectedCode = detectedCode.trim().toUpperCase();

  const reticle = document.getElementById('scannerReticle');
  if (reticle) {
    reticle.classList.add('detected');
    setTimeout(() => reticle.classList.remove('detected'), 600);
  }

  if (typeof playBeep === 'function') playBeep(1800, 'triangle', 0.15);
  if (navigator.vibrate) {
    try { navigator.vibrate([100, 50, 100]); } catch (e) {}
  }

  const modal = document.getElementById('scannerModal');
  const action = modal ? modal.dataset.action : 'LOOKUP';

  if (action === 'INBOUND') {
    const textarea = document.getElementById('inboundSerialTextarea');
    if (textarea) {
      const currentVal = textarea.value.trim();
      const existing = currentVal ? currentVal.split('\n').map(s => s.trim()) : [];
      if (!existing.includes(detectedCode)) {
        existing.push(detectedCode);
        textarea.value = existing.join('\n');
        if (typeof showToast === 'function') showToast(`Đã thêm Serial vào phiếu: ${detectedCode}`, 'success');
      } else {
        if (typeof showToast === 'function') showToast(`Serial này đã có trong danh sách: ${detectedCode}`, 'warning');
      }
      closeScannerModal();
      return;
    }
  }

  if (typeof showToast === 'function') showToast(`Đã quét nhận diện: ${detectedCode}`, 'success');
  closeScannerModal();

  if (typeof lookupSerial === 'function') {
    if (typeof switchTab === 'function') switchTab('products');
    lookupSerial(detectedCode);
  }
}

// Close Scanner Modal
function closeScannerModal() {
  const modal = document.getElementById('scannerModal');
  if (modal) modal.classList.remove('active');
  stopCameraStream();
}
