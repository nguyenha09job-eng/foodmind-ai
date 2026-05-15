import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FoodMind AI",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stAppViewContainer"] { background: #f2f0eb; }
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
  background: #f2f0eb;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  font-family: 'Be Vietnam Pro', sans-serif;
  padding: 24px 0 40px;
}

.phone-frame {
  width: 390px;
  min-height: 844px;
  max-height: 844px;
  background: #fafaf8;
  border-radius: 48px;
  box-shadow: 0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.08);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Notch */
.notch {
  position: absolute;
  top: 14px; left: 50%; transform: translateX(-50%);
  width: 120px; height: 34px;
  background: #1a1a1a;
  border-radius: 20px;
  z-index: 40;
}

/* Scrollable content */
.scroll-content {
  flex: 1;
  overflow-y: auto;
  padding: 70px 0 300px; /* Tăng padding bottom để cuộn qua được phần floating card */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.scroll-content::-webkit-scrollbar { display: none; }

/* Header */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  margin-bottom: 28px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 46px; height: 46px;
  background: #FF5A1F;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #999;
  text-transform: uppercase;
}

.brand-location {
  font-family: 'Sora', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
}

.top-actions {
  display: flex;
  gap: 10px;
}

.icon-btn {
  width: 40px; height: 40px;
  border-radius: 50%;
  border: 1.5px solid #e8e6e0;
  background: #fff;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  position: relative;
}

.notif-dot {
  position: absolute;
  top: 6px; right: 6px;
  width: 8px; height: 8px;
  background: #FF5A1F;
  border-radius: 50%;
  border: 1.5px solid #fff;
}

/* Hero Title */
.hero-title {
  font-family: 'Sora', sans-serif;
  font-size: 36px;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1.15;
  letter-spacing: -1.5px;
  padding: 0 24px;
  margin-bottom: 28px;
}

/* Tab Toggle */
.tab-wrap {
  padding: 0 24px;
  margin-bottom: 24px;
}

.tab-group {
  display: inline-flex;
  background: #eceae4;
  border-radius: 18px;
  padding: 4px;
  gap: 2px;
}

.tab-btn {
  padding: 8px 22px;
  border-radius: 14px;
  font-family: 'Sora', sans-serif;
  font-size: 14px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn.active {
  background: #fff;
  color: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.tab-btn.inactive {
  background: transparent;
  color: #999;
}

/* Food Card */
.food-card-wrap {
  padding: 0 20px;
  margin-bottom: 16px;
}

.food-card {
  border-radius: 26px;
  overflow: hidden;
  position: relative;
  height: 280px;
  background: #2a2a2a;
}

.food-img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  filter: brightness(0.82);
}

/* Gradient overlay */
.food-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 65%;
  background: linear-gradient(to top, rgba(0,0,0,0.82) 0%, transparent 100%);
}

.match-badge {
  position: absolute;
  top: 16px; right: 16px;
  background: rgba(255,255,255,0.96);
  border-radius: 16px;
  padding: 8px 14px;
  text-align: center;
  z-index: 2;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.match-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #999;
  text-transform: uppercase;
  display: block;
  margin-bottom: 2px;
}

.match-pct {
  font-family: 'Sora', sans-serif;
  font-size: 22px;
  font-weight: 800;
  color: #FF5A1F;
  line-height: 1;
}

.food-info {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 16px 18px;
  z-index: 2;
}

.food-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.rating-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #FFD600;
  border-radius: 20px;
  padding: 4px 10px;
}

.rating-star {
  font-size: 13px;
}

.rating-val {
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #1a1a1a;
}

.food-distance {
  font-size: 13px;
  color: rgba(255,255,255,0.75);
  font-weight: 500;
}

.food-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.food-name {
  font-family: 'Sora', sans-serif;
  font-size: 24px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.5px;
}

.price-badge {
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.28);
  border-radius: 12px;
  padding: 6px 12px;
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  backdrop-filter: blur(8px);
  white-space: nowrap;
}

/* Tags */
.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 20px;
  margin-bottom: 20px;
}

.tag {
  background: #fff;
  border: 1.5px solid #e8e6e0;
  border-radius: 20px;
  padding: 6px 14px;
  font-family: 'Sora', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #555;
  text-transform: uppercase;
}

/* Needs Summary Card (Floating & Transparent) */
.needs-card {
  position: absolute;
  bottom: 85px; /* Đặt phía trên thanh điều hướng dưới */
  left: 16px;
  right: 16px;
  /* Nền trắng trong suốt mờ */
  background: rgba(252, 252, 252, 0.75); 
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 24px;
  padding: 18px 20px;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.05), 0 8px 24px rgba(0,0,0,0.1);
  z-index: 20; /* Đảm bảo nằm trên nội dung cuộn */
}

.needs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.needs-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.needs-icon {
  width: 34px; height: 34px;
  background: #1a1a1a;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
}

.needs-label {
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #1a1a1a;
  text-transform: uppercase;
}

.needs-actions {
  display: flex;
  gap: 8px;
}

.needs-btn {
  width: 32px; height: 32px;
  border-radius: 50%;
  border: 1.5px solid rgba(232, 230, 224, 0.8);
  background: rgba(245, 245, 245, 0.6);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  color: #1a1a1a;
}

.needs-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px 6px;
}

.needs-item {}

.needs-item-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #888;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.needs-item-val {
  font-family: 'Sora', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #1a1a1a;
}

/* Food card (peek) */
.food-card-peek {
  margin: 0 20px 20px;
  border-radius: 26px;
  background: #2a2a2a;
  height: 80px;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 18px;
  justify-content: space-between;
}

.food-card-peek::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.55);
}

.peek-name {
  font-family: 'Sora', sans-serif;
  font-size: 18px;
  font-weight: 800;
  color: #fff;
  position: relative; z-index: 1;
  letter-spacing: -0.3px;
}

.peek-price {
  font-family: 'Sora', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: rgba(255,255,255,0.8);
  position: relative; z-index: 1;
}

.peek-match {
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #FF5A1F;
  position: relative; z-index: 1;
}

/* Bottom Nav */
.bottom-nav {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 72px;
  background: #fff;
  border-top: 1px solid #f0ede8;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 0 16px;
  z-index: 30;
  border-bottom-left-radius: 48px;
  border-bottom-right-radius: 48px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 8px 16px;
}

.nav-icon {
  width: 24px; height: 24px;
  display: flex; align-items: center; justify-content: center;
  position: relative;
}

.nav-dot {
  position: absolute;
  bottom: -4px; left: 50%; transform: translateX(-50%);
  width: 5px; height: 5px;
  background: #FF5A1F;
  border-radius: 50%;
}
</style>
</head>
<body>
<div class="phone-frame">
  <!-- Notch -->
  <div class="notch"></div>

  <!-- Scrollable area -->
  <div class="scroll-content">

    <!-- Top Bar -->
    <div class="top-bar">
      <div class="brand">
        <div class="brand-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M12 2C9.5 5 6 7 6 11C6 13.8 7.8 16.2 10.5 17.3V20H13.5V17.3C16.2 16.2 18 13.8 18 11C18 7 14.5 5 12 2Z" fill="white"/>
            <path d="M10 22H14" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-label">FoodMind AI</span>
          <span class="brand-location">Quận 1, TP. HCM</span>
        </div>
      </div>
      <div class="top-actions">
        <div class="icon-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.2" stroke-linecap="round">
            <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
          </svg>
        </div>
        <div class="icon-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <div class="notif-dot"></div>
        </div>
      </div>
    </div>

    <!-- Hero -->
    <div class="hero-title">Gợi ý AI cho<br>bạn hôm nay</div>

    <!-- Tabs -->
    <div class="tab-wrap">
      <div class="tab-group">
        <button class="tab-btn active">Quán ăn</button>
        <button class="tab-btn inactive">Món lẻ</button>
      </div>
    </div>

    <!-- Main Food Card -->
    <div class="food-card-wrap">
      <div class="food-card">
        <div style="width:100%;height:100%;background:linear-gradient(160deg,#3d2a1a 0%,#6b3d1e 35%,#8b4513 60%,#5a3010 100%);position:relative;">
          <div style="position:absolute;top:40px;left:60px;width:180px;height:140px;background:radial-gradient(ellipse,rgba(200,160,100,0.5),transparent 70%);border-radius:50%;"></div>
          <div style="position:absolute;bottom:70px;right:40px;width:120px;height:90px;background:radial-gradient(ellipse,rgba(255,220,150,0.3),transparent 70%);border-radius:50%;"></div>
          <div style="position:absolute;top:60px;right:80px;width:70px;height:70px;background:rgba(255,255,255,0.08);border-radius:50%;"></div>
        </div>

        <div class="match-badge">
          <span class="match-label">Match</span>
          <span class="match-pct">94%</span>
        </div>

        <div class="food-info">
          <div class="food-meta">
            <div class="rating-badge">
              <span class="rating-star">⭐</span>
              <span class="rating-val">4.8</span>
            </div>
            <span class="food-distance">1.2 km • 15–20 ph</span>
          </div>
          <div class="food-bottom">
            <span class="food-name">Cơm Tấm Bà Lan</span>
            <span class="price-badge">45k – 65k</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Tags -->
    <div class="tags-row">
      <span class="tag">PHÙ HỢP 94% VỚI NHU CẦU</span>
      <span class="tag">GIAO NHANH</span>
      <span class="tag">NGON RẺ</span>
    </div>

    <!-- Second restaurant peek card -->
    <div class="food-card-peek">
      <div style="position:absolute;inset:0;background:linear-gradient(135deg,#8b1a1a,#6b0f0f);"></div>
      <span class="peek-name">Bún Bò Huế Chu</span>
      <div style="display:flex;flex-direction:column;align-items:flex-end;position:relative;z-index:1;gap:3px;">
        <span class="peek-price">50k – 70k</span>
        <span class="peek-match">87% match</span>
      </div>
    </div>

    <!-- Third restaurant peek card -->
    <div class="food-card-peek">
      <div style="position:absolute;inset:0;background:linear-gradient(135deg,#1a3a4a,#0f2a38);"></div>
      <span class="peek-name">Phở Bò Hà Nội</span>
      <div style="display:flex;flex-direction:column;align-items:flex-end;position:relative;z-index:1;gap:3px;">
        <span class="peek-price">45k – 60k</span>
        <span class="peek-match">82% match</span>
      </div>
    </div>
    
    <!-- Fourth restaurant peek card to show scroll effect -->
    <div class="food-card-peek" style="margin-bottom:0;">
      <div style="position:absolute;inset:0;background:linear-gradient(135deg,#2e4a1a,#1a380f);"></div>
      <span class="peek-name">Salad Healthy Xanh</span>
      <div style="display:flex;flex-direction:column;align-items:flex-end;position:relative;z-index:1;gap:3px;">
        <span class="peek-price">60k – 85k</span>
        <span class="peek-match">78% match</span>
      </div>
    </div>

  </div> <!-- End Scroll Content -->

  <!-- Floating Needs Summary Card -->
  <div class="needs-card">
    <div class="needs-header">
      <div class="needs-title-row">
        <div class="needs-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round">
            <path d="M4 6h16M8 6V4h8v2M4 12h16M6 18h12"/>
          </svg>
        </div>
        <span class="needs-label">Tóm tắt nhu cầu</span>
      </div>
      <div class="needs-actions">
        <div class="needs-btn">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </div>
        <div class="needs-btn">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </div>
      </div>
    </div>
    <div class="needs-grid">
      <div class="needs-item">
        <div class="needs-item-label">Budget</div>
        <div class="needs-item-val">30k - 50k</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Độ đói</div>
        <div class="needs-item-val">Rất đói 🔥</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Giao hàng</div>
        <div class="needs-item-val">Nhanh ⚡</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Mục tiêu</div>
        <div class="needs-item-val">Healthy 🥗</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Ẩm thực</div>
        <div class="needs-item-val">Việt Nam 🇻🇳</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Weather</div>
        <div class="needs-item-val">Nắng ☀️</div>
      </div>
    </div>
  </div>

  <!-- Bottom Nav -->
  <div class="bottom-nav">
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="#FF5A1F">
          <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
        </svg>
        <div class="nav-dot"></div>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/>
          <line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/>
        </svg>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
        </svg>
      </div>
    </div>
  </div>
</div>

<script>
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => { t.className = 'tab-btn inactive'; });
      tab.className = 'tab-btn active';
    });
  });
</script>
</body>
</html>
"""

components.html(html_code, height=960, scrolling=False)