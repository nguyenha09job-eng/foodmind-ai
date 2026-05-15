import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Khám Phá",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn các thành phần mặc định của Streamlit
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

/* Khung iPhone 16 */
.phone-frame {
  width: 390px;
  min-height: 844px;
  max-height: 844px;
  background: #fdfdfc; /* Trắng ngà nhẹ */
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

/* Khu vực nội dung có thể cuộn dọc */
.scroll-content {
  flex: 1;
  overflow-y: auto;
  padding-top: 70px;
  padding-bottom: 120px; /* Tránh bị che bởi bottom nav */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.scroll-content::-webkit-scrollbar { display: none; }

/* Header */
.header-section {
  padding: 10px 24px 20px;
}

.label-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #FF5A1F;
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.main-title {
  font-family: 'Sora', sans-serif;
  font-size: 36px;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1.15;
  letter-spacing: -1px;
}

/* Search Bar */
.search-box {
  margin: 0 24px 30px;
  background: #fff;
  border: 1px solid #f0ede8;
  border-radius: 20px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}

.search-text {
  font-size: 15px;
  color: #999;
  font-weight: 500;
}

/* Section Titles */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  margin-bottom: 16px;
}

.section-title {
  font-family: 'Sora', sans-serif;
  font-size: 18px;
  font-weight: 800;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 8px;
}

.view-all {
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #FF5A1F;
  cursor: pointer;
}

/* Cuộn ngang cho danh sách Xu hướng */
.trending-horizontal-scroll {
  display: flex;
  gap: 16px;
  padding: 0 24px 10px;
  overflow-x: auto;
  scrollbar-width: none;
  margin-bottom: 24px;
}
.trending-horizontal-scroll::-webkit-scrollbar { display: none; }

.trend-card {
  min-width: 160px;
  width: 160px;
  background: #fff;
  border-radius: 24px;
  border: 1px solid #f0ede8;
  box-shadow: 0 4px 15px rgba(0,0,0,0.02);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.trend-img-wrap {
  width: 100%;
  height: 140px;
  position: relative;
}

.trend-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.rating-badge {
  position: absolute;
  top: 10px; right: 10px;
  background: rgba(255, 255, 255, 0.95);
  padding: 4px 8px;
  border-radius: 12px;
  font-family: 'Sora', sans-serif;
  font-size: 11px;
  font-weight: 800;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 4px;
}

.trend-info {
  padding: 16px;
}

.trend-name {
  font-family: 'Sora', sans-serif;
  font-size: 15px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.trend-loc {
  font-size: 12px;
  color: #888;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Danh sách vừa xem dọc */
.recent-list {
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recent-item {
  background: #fff;
  border-radius: 20px;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid #f0ede8;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  cursor: pointer;
}

.recent-img {
  width: 60px; height: 60px;
  border-radius: 16px;
  object-fit: cover;
}

.recent-info {
  flex: 1;
}

.recent-name {
  font-family: 'Sora', sans-serif;
  font-size: 14px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.recent-desc {
  font-size: 12px;
  color: #999;
  font-weight: 500;
}

.chevron-icon {
  color: #ccc;
  margin-right: 8px;
}

/* Bottom Nav Fixed */
.bottom-nav {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 84px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border-top: 1px solid #f0ede8;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 0 16px 12px;
  z-index: 50;
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

  <!-- Scrollable Area -->
  <div class="scroll-content">
    
    <!-- Header -->
    <div class="header-section">
      <div class="label-wrap">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
        </svg>
        KHÁM PHÁ
      </div>
      <h1 class="main-title">Mở rộng khẩu vị<br>của bạn</h1>
    </div>

    <!-- Search Box -->
    <div class="search-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
        <polyline points="16 7 22 7 22 13"></polyline>
      </svg>
      <span class="search-text">Mọi người đang tìm: "Cơm tấm"</span>
    </div>

    <!-- Trending Section -->
    <div class="section-header">
      <div class="section-title">Xu hướng hiện nay</div>
      <div class="view-all">Xem tất cả</div>
    </div>

    <div class="trending-horizontal-scroll">
      <!-- Card 1 -->
      <div class="trend-card">
        <div class="trend-img-wrap">
          <img src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=300&q=80" alt="Healthy Bowl" class="trend-img">
          <div class="rating-badge">
            <span style="color:#FFD600">★</span> 4.9
          </div>
        </div>
        <div class="trend-info">
          <div class="trend-name">Healthy Bowl</div>
          <div class="trend-loc">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle>
            </svg>
            Quận 1
          </div>
        </div>
      </div>

      <!-- Card 2 -->
      <div class="trend-card">
        <div class="trend-img-wrap">
          <img src="https://images.unsplash.com/photo-1579871494447-0811cf80d49c?auto=format&fit=crop&w=300&q=80" alt="Sushi Haru" class="trend-img">
        </div>
        <div class="trend-info">
          <div class="trend-name">Sushi Haru</div>
          <div class="trend-loc">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle>
            </svg>
            Quận 3
          </div>
        </div>
      </div>
      
      <!-- Card 3 (cho thao tác vuốt ngang mượt) -->
      <div class="trend-card">
        <div class="trend-img-wrap">
          <img src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=300&q=80" alt="Pizza" class="trend-img">
          <div class="rating-badge">
            <span style="color:#FFD600">★</span> 4.7
          </div>
        </div>
        <div class="trend-info">
          <div class="trend-name">Pizza Ngon</div>
          <div class="trend-loc">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle>
            </svg>
            Quận 2
          </div>
        </div>
      </div>
    </div>

    <!-- Recently Viewed Section -->
    <div class="section-header">
      <div class="section-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        Vừa xem gần đây
      </div>
    </div>

    <div class="recent-list">
      <!-- Item 1 -->
      <div class="recent-item">
        <img src="https://images.unsplash.com/photo-1555126634-323283e090fa?auto=format&fit=crop&w=150&q=80" alt="Quán Ngon" class="recent-img">
        <div class="recent-info">
          <div class="recent-name">Quán Ngon Sài Gòn</div>
          <div class="recent-desc">Cơm, Bún, Phở • 2.1 km</div>
        </div>
        <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>

      <!-- Item 2 -->
      <div class="recent-item">
        <img src="https://images.unsplash.com/photo-1548943487-a2e4d43b4853?auto=format&fit=crop&w=150&q=80" alt="Cơm Tấm" class="recent-img">
        <div class="recent-info">
          <div class="recent-name">Cơm Tấm Bà Lan</div>
          <div class="recent-desc">Đồ nướng, Cơm • 1.2 km</div>
        </div>
        <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
      
      <!-- Item 3 (Để test cuộn dọc) -->
      <div class="recent-item">
        <img src="https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?auto=format&fit=crop&w=150&q=80" alt="Bún bò" class="recent-img">
        <div class="recent-info">
          <div class="recent-name">Bún Bò Huế Chu</div>
          <div class="recent-desc">Bún, Phở, Món nước • 3.5 km</div>
        </div>
        <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
    </div>

  </div> <!-- End Scroll Content -->

  <!-- Bottom Navigation Fixed -->
  <div class="bottom-nav">
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon>
        <line x1="9" y1="3" x2="9" y2="18"></line>
        <line x1="15" y1="6" x2="15" y2="21"></line>
      </svg>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>
    </div>
    
    <!-- Profile Icon Active -->
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
      <div class="nav-dot"></div>
    </div>
  </div>

</div>
</body>
</html>
"""

# Render HTML vào Streamlit
components.html(html_code, height=960, scrolling=False)