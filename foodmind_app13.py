import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FoodMind AI - Tracking",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stAppViewContainer"] { background: #333; } /* Nền tối để tôn lên điện thoại */
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: transparent;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  font-family: 'Be Vietnam Pro', sans-serif;
  padding: 24px 0 40px;
}

/* Khung điện thoại chuẩn iPhone */
.phone-frame {
  width: 390px;
  min-height: 844px;
  max-height: 844px;
  /* Giả lập nền bản đồ (Map Grid) */
  background-color: #e5e2d8;
  background-image: 
    linear-gradient(rgba(0,0,0,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.04) 1px, transparent 1px);
  background-size: 80px 80px;
  background-position: center;
  border-radius: 48px;
  box-shadow: 0 40px 80px rgba(0,0,0,0.25), 0 0 0 10px #1a1a1a;
  position: relative;
  overflow: hidden;
}

/* Tai thỏ (Notch) */
.notch {
  position: absolute;
  top: 14px; left: 50%; transform: translateX(-50%);
  width: 120px; height: 34px;
  background: #1a1a1a;
  border-radius: 20px;
  z-index: 100;
}

/* =========================================
   TOP CARD (Thời gian dự kiến)
   ========================================= */
.top-card {
  position: absolute;
  top: 60px; left: 16px; right: 16px;
  background: #fff;
  border-radius: 36px;
  padding: 18px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  z-index: 50;
}

.back-btn {
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: flex-start;
  cursor: pointer;
  color: #1a1a1a;
}

.eta-info {
  text-align: center;
  flex: 1;
}

.eta-label {
  font-size: 10px;
  font-weight: 800;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 2px;
}

.eta-time {
  font-family: 'Sora', sans-serif;
  font-size: 20px;
  font-weight: 800;
  color: #1a1a1a;
}

.time-icon {
  width: 44px; height: 44px;
  background: #FFF0EB;
  color: #FF5A1F;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}

/* =========================================
   BẢN ĐỒ & LỘ TRÌNH (SVG Path)
   ========================================= */
.route-svg {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 1;
}

/* Marker Quán ăn */
.marker-restaurant {
  position: absolute;
  top: 240px; left: 160px; 
  transform: translate(-50%, -50%);
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  z-index: 10;
}

.res-icon {
  background: #1a1a1a;
  width: 48px; height: 48px;
  border-radius: 16px;
  display: flex; justify-content: center; align-items: center;
  font-size: 24px;
  border: 3px solid #fff;
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.res-label {
  background: #fff;
  padding: 6px 14px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 800;
  font-family: 'Sora', sans-serif;
  color: #1a1a1a;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

/* Marker Shipper */
.marker-shipper {
  position: absolute;
  top: 420px; left: 160px; /* Nằm trên đường cam */
  transform: translate(-50%, -50%);
  width: 52px; height: 52px;
  background: #FF5A1F;
  border-radius: 50%;
  display: flex; justify-content: center; align-items: center;
  font-size: 26px;
  border: 3px solid #fff;
  box-shadow: 0 4px 12px rgba(255, 90, 31, 0.4);
  z-index: 11;
  animation: bounce 1s infinite alternate;
}

/* Vòng tròn Radar nhấp nháy bao quanh Shipper */
.radar-pulse {
  position: absolute;
  top: 420px; left: 160px;
  transform: translate(-50%, -50%);
  width: 52px; height: 52px;
  border-radius: 50%;
  background: rgba(255, 90, 31, 0.3);
  border: 2px solid rgba(255, 90, 31, 0.5);
  z-index: 10;
  animation: pulse 2s infinite ease-out;
}

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(2.2); opacity: 0; }
}

@keyframes bounce {
  0% { transform: translate(-50%, -50%); }
  100% { transform: translate(-50%, -54%); }
}

/* =========================================
   BOTTOM SHEET (Thông tin tài xế)
   ========================================= */
.bottom-sheet {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: #fff;
  border-radius: 40px 40px 0 0;
  padding: 16px 24px 32px;
  box-shadow: 0 -10px 40px rgba(0,0,0,0.1);
  z-index: 50;
}

.drag-handle {
  width: 40px; height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  margin: 0 auto 24px;
}

/* Driver Card */
.driver-card {
  display: flex;
  align-items: center;
  background: #fafaf8;
  border-radius: 28px;
  padding: 16px;
  margin-bottom: 28px;
}

.driver-avatar {
  width: 54px; height: 54px;
  background: #FFD600;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Sora', sans-serif;
  font-size: 18px;
  font-weight: 800;
  color: #1a1a1a;
}

.driver-info {
  flex: 1;
  margin-left: 14px;
}

.driver-name {
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  font-size: 17px;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.driver-meta {
  font-size: 13px;
  color: #888;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.star-rating { color: #FFC107; font-weight: 700; display:flex; align-items:center; gap:3px;}

.driver-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  width: 48px; height: 48px;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
}

.btn-chat {
  background: #fff;
  border: 1.5px solid #e8e6e0;
  color: #1a1a1a;
}

.btn-call {
  background: #FF5A1F;
  color: #fff;
  box-shadow: 0 4px 12px rgba(255, 90, 31, 0.3);
}

/* Timeline 5 Bước */
.timeline-wrap {
  position: relative;
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  padding: 0 4px;
}

/* Đường line xám nền */
.timeline-wrap::before {
  content: '';
  position: absolute;
  top: 15px; left: 20px; right: 20px;
  height: 2px;
  background: #f0f0f0;
  z-index: 1;
}

/* Đường line xanh chạy (đến bước 4) */
.timeline-wrap::after {
  content: '';
  position: absolute;
  top: 15px; left: 20px;
  width: 75%; /* Chiếm đến icon thứ 4 */
  height: 2px;
  background: #00C853;
  z-index: 1;
}

.step {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 50px;
}

.step-icon {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: #00C853;
  color: #fff;
}

/* Hiệu ứng viền nhạt cho icon đang active */
.step-icon.current {
  box-shadow: 0 0 0 6px #E8F5E9;
}

.step-icon.inactive {
  background: #f0f0f0;
}
.step-icon.inactive .dot {
  width: 8px; height: 8px; background: #ccc; border-radius: 50%;
}

.step-label {
  font-size: 10px;
  font-weight: 800;
  color: #1a1a1a;
  text-align: center;
  line-height: 1.3;
}

.step.inactive .step-label { color: #999; font-weight: 700; }

.status-text {
  text-align: center;
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  font-size: 16px;
  color: #FF5A1F;
}

</style>
</head>
<body>

<div class="phone-frame">
  <!-- Notch iPhone -->
  <div class="notch"></div>

  <!-- SVG vẽ đường đi (Line cam) -->
  <svg class="route-svg" viewBox="0 0 390 844" fill="none" xmlns="http://www.w3.org/2000/svg">
    <polyline points="160,250 160,490 320,490 320,600" stroke="#FF5A1F" stroke-width="5" stroke-linejoin="round"/>
  </svg>

  <!-- Card Dự kiến giao -->
  <div class="top-card">
    <div class="back-btn">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
    </div>
    <div class="eta-info">
      <div class="eta-label">DỰ KIẾN GIAO</div>
      <div class="eta-time">12 phút nữa</div>
    </div>
    <div class="time-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
      </svg>
    </div>
  </div>

  <!-- Quán Ăn (Bà Lan) -->
  <div class="marker-restaurant">
    <div class="res-icon">🍱</div>
    <div class="res-label">Bà Lan</div>
  </div>

  <!-- Radar Pulse & Shipper (Xe Máy) -->
  <div class="radar-pulse"></div>
  <div class="marker-shipper">🛵</div>

  <!-- Bottom Sheet (Trạng thái đơn) -->
  <div class="bottom-sheet">
    <div class="drag-handle"></div>

    <!-- Thông tin tài xế -->
    <div class="driver-card">
      <div class="driver-avatar">MT</div>
      <div class="driver-info">
        <div class="driver-name">Minh Tuấn</div>
        <div class="driver-meta">
          <span class="star-rating">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            4.9
          </span> 
          <span>• Honda Wave</span>
        </div>
      </div>
      <div class="driver-actions">
        <div class="action-btn btn-chat">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </div>
        <div class="action-btn btn-call">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        </div>
      </div>
    </div>

    <!-- Timeline các bước -->
    <div class="timeline-wrap">
      <!-- Bước 1 -->
      <div class="step">
        <div class="step-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <div class="step-label">Đã xác<br>nhận</div>
      </div>
      <!-- Bước 2 -->
      <div class="step">
        <div class="step-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <div class="step-label">Đang<br>chuẩn bị</div>
      </div>
      <!-- Bước 3 -->
      <div class="step">
        <div class="step-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <div class="step-label">Shipper<br>nhận đơn</div>
      </div>
      <!-- Bước 4 (Current) -->
      <div class="step">
        <div class="step-icon current">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <div class="step-label">Đang giao</div>
      </div>
      <!-- Bước 5 (Inactive) -->
      <div class="step inactive">
        <div class="step-icon inactive">
          <div class="dot"></div>
        </div>
        <div class="step-label">Đã giao</div>
      </div>
    </div>

    <!-- Trạng thái chữ cam -->
    <div class="status-text">Shipper đang trên đường</div>

  </div>
</div>

</body>
</html>
"""

components.html(html_code, height=960, scrolling=False)