import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FoodMind AI - Detail",
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
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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

/* Phone Frame */
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

/* Scrollable Content */
.scroll-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 120px; /* Padding lớn ở dưới để nội dung không bị che bởi nút bấm cố định */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.scroll-content::-webkit-scrollbar { display: none; }

/* Hero Section */
.hero-header {
  position: relative;
  height: 380px;
  background: #2a2a2a;
  border-bottom-left-radius: 44px;
  border-bottom-right-radius: 44px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 60px 24px 30px;
}

.hero-bg {
  position: absolute;
  inset: 0;
  /* Sử dụng màu gradient thay thế ảnh thực tế để đảm bảo luôn hiển thị tốt */
  background: linear-gradient(150deg, #5c3c22 0%, #2a1505 100%);
  z-index: 0;
}
.hero-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('https://images.unsplash.com/photo-1615557960916-5f4791effe9d?q=80&w=600&auto=format&fit=crop') center/cover;
  opacity: 0.6;
  mix-blend-mode: overlay;
}
.hero-bg::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 70%;
  background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, transparent 100%);
}

.top-nav {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.circle-btn {
  width: 44px; height: 44px;
  border-radius: 50%;
  background: rgba(255,255,255,0.25);
  backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  border: 1px solid rgba(255,255,255,0.1);
}

.hero-content {
  position: relative;
  z-index: 10;
}

.rec-badge {
  display: inline-block;
  background: #FF5A1F;
  color: #fff;
  font-family: 'Sora', sans-serif;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1px;
  padding: 6px 12px;
  border-radius: 12px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.hero-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.hero-title {
  font-family: 'Sora', sans-serif;
  font-size: 34px;
  font-weight: 800;
  color: #fff;
  line-height: 1.1;
  letter-spacing: -1px;
}

.match-box {
  background: #fff;
  border-radius: 18px;
  padding: 8px 16px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.match-box-label {
  font-size: 9px;
  font-weight: 800;
  color: #999;
  letter-spacing: 1px;
}

.match-box-val {
  font-family: 'Sora', sans-serif;
  font-size: 22px;
  font-weight: 800;
  color: #FF5A1F;
  line-height: 1.1;
}

/* Stats Row */
.stats-row {
  display: flex;
  justify-content: space-between;
  padding: 24px 30px;
  margin-top: 4px;
}

.stat-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.stat-col.border {
  border-left: 1px solid #e8e6e0;
}

.stat-val {
  font-family: 'Sora', sans-serif;
  font-size: 15px;
  font-weight: 800;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-label {
  font-size: 10px;
  font-weight: 700;
  color: #999;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* AI Banner */
.ai-banner {
  margin: 0 24px 24px;
  background: #fff;
  border-radius: 20px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
  border: 1px solid #f0ede8;
  cursor: pointer;
}

.ai-banner-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-icon-wrap {
  width: 32px; height: 32px;
  background: #fff0eb;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #FF5A1F;
}

.ai-banner-text {
  font-family: 'Sora', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #1a1a1a;
}

/* Tabs */
.menu-tabs {
  display: flex;
  gap: 10px;
  padding: 0 24px;
  margin-bottom: 24px;
  overflow-x: auto;
  scrollbar-width: none;
}
.menu-tabs::-webkit-scrollbar { display: none; }

.m-tab {
  padding: 12px 24px;
  border-radius: 20px;
  font-family: 'Sora', sans-serif;
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s;
}

.m-tab.active {
  background: #1a1a1a;
  color: #fff;
}

.m-tab.inactive {
  background: #fff;
  color: #888;
  border: 1px solid #f0ede8;
}

/* Menu List */
.menu-list {
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.menu-item {
  background: #fff;
  border-radius: 24px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
  border: 1px solid #f5f3ef;
}

.menu-img {
  width: 80px; height: 80px;
  border-radius: 16px;
  background: #eee;
  object-fit: cover;
}

.menu-info {
  flex: 1;
}

.menu-name {
  font-family: 'Sora', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 4px;
  line-height: 1.3;
}

.menu-desc {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
  font-weight: 500;
}

.menu-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.menu-cal {
  font-weight: 700;
  color: #FF5A1F;
}

.menu-price {
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  color: #1a1a1a;
}

.add-btn {
  width: 40px; height: 40px;
  border-radius: 14px;
  background: #1a1a1a;
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  border: none;
  cursor: pointer;
}

/* Floating Order Button (Fixed) */
.floating-order-box {
  position: absolute;
  bottom: 30px;
  left: 24px;
  right: 24px;
  z-index: 50;
}

.btn-primary {
  width: 100%;
  background: #FF5A1F;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 18px 24px;
  font-family: 'Sora', sans-serif;
  font-size: 16px;
  font-weight: 800;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(255, 90, 31, 0.35);
  transition: transform 0.2s;
}

.btn-primary:active {
  transform: scale(0.98);
}
</style>
</head>
<body>
<div class="phone-frame">
  <!-- Notch -->
  <div class="notch"></div>

  <!-- Scrollable content -->
  <div class="scroll-content">
    
    <!-- Hero Header -->
    <div class="hero-header">
      <div class="hero-bg"></div>
      
      <div class="top-nav">
        <div class="circle-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </div>
        <div class="circle-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
        </div>
      </div>

      <div class="hero-content">
        <span class="rec-badge">TOP RECOMMENDATION</span>
        <div class="hero-title-row">
          <h1 class="hero-title">Cơm Tấm Bà<br>Lan</h1>
          <div class="match-box">
            <div class="match-box-label">MATCH</div>
            <div class="match-box-val">94%</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-col">
        <div class="stat-val"><span style="color:#FFD600">⭐</span> 4.8</div>
        <div class="stat-label">RATING</div>
      </div>
      <div class="stat-col border">
        <div class="stat-val"><span style="color:#FF5A1F">📍</span> 1.2km</div>
        <div class="stat-label">KHOẢNG CÁCH</div>
      </div>
      <div class="stat-col border">
        <div class="stat-val"><span style="color:#00C853">🕒</span> 15ph</div>
        <div class="stat-label">GIAO HÀNG</div>
      </div>
    </div>

    <!-- AI Insight Banner -->
    <div class="ai-banner">
      <div class="ai-banner-left">
        <div class="ai-icon-wrap">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <span class="ai-banner-text">Tại sao AI gợi ý quán này?</span>
      </div>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </div>

    <!-- Tabs -->
    <div class="menu-tabs">
      <div class="m-tab active">Món chính</div>
      <div class="m-tab inactive">Món thêm</div>
      <div class="m-tab inactive">Đồ uống</div>
    </div>

    <!-- Menu List -->
    <div class="menu-list">
      <!-- Item 1 -->
      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=150&q=80" alt="Food" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Cơm tấm sườn bì chả</div>
          <div class="menu-desc">Sườn nướng than hoa, b...</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 650 kcal</span>
            <span style="color:#ccc">•</span>
            <span class="menu-price">45,000 đ</span>
          </div>
        </div>
        <button class="add-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>

      <!-- Item 2 -->
      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?auto=format&fit=crop&w=150&q=80" alt="Food" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Cơm tấm sườn mỡ hành</div>
          <div class="menu-desc">Sườn mềm mọng nước,...</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 580 kcal</span>
            <span style="color:#ccc">•</span>
            <span class="menu-price">40,000 đ</span>
          </div>
        </div>
        <button class="add-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>
      
      <!-- Item 3 (Để test scroll) -->
      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1548943487-a2e4d43b4853?auto=format&fit=crop&w=150&q=80" alt="Food" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Cơm tấm đùi gà nướng</div>
          <div class="menu-desc">Đùi gà góc tư nướng sốt...</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 720 kcal</span>
            <span style="color:#ccc">•</span>
            <span class="menu-price">55,000 đ</span>
          </div>
        </div>
        <button class="add-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Cố định nút ở dưới cùng màn hình -->
  <div class="floating-order-box">
    <button class="btn-primary">
      <span>Đặt món nhanh ngay</span>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
  </div>

</div>

<script>
  // Chuyển đổi tab effect
  const tabs = document.querySelectorAll('.m-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => { t.className = 'm-tab inactive'; });
      tab.className = 'm-tab active';
    });
  });
</script>
</body>
</html>
"""

components.html(html_code, height=960, scrolling=False)