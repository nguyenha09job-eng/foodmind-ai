import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(
    page_title="FoodMind AI - Meal Plan",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn UI mặc định của Streamlit
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
  background: #fdfdfc;
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

/* Nội dung có thể cuộn */
.scroll-content {
  flex: 1;
  overflow-y: auto;
  padding-top: 70px;
  padding-bottom: 120px; /* Chừa không gian cho bottom nav */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.scroll-content::-webkit-scrollbar { display: none; }

/* Header Section */
.header-section {
  padding: 20px 24px;
  margin-bottom: 10px;
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
  font-size: 34px;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1.15;
  letter-spacing: -1px;
  margin-bottom: 8px;
}

.sub-title {
  font-size: 16px;
  font-weight: 700;
  color: #999;
}

/* Meal List */
.meal-list {
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.meal-card {
  background: #fff;
  border-radius: 24px;
  padding: 20px 20px 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  border: 1px solid #f4f3ef;
  position: relative;
  overflow: hidden;
}

/* Vạch màu bên trái thẻ ăn uống */
.meal-card::before {
  content: '';
  position: absolute;
  left: 0; top: 20px; bottom: 20px;
  width: 6px;
  border-radius: 0 6px 6px 0;
}

.meal-card.breakfast::before { background: #FFD600; }
.meal-card.lunch::before { background: #FF5A1F; }
.meal-card.dinner::before { background: #00C853; }

.meal-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.meal-time {
  font-size: 11px;
  font-weight: 800;
  color: #aaa;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.meal-name {
  font-family: 'Sora', sans-serif;
  font-size: 18px;
  font-weight: 800;
  color: #1a1a1a;
}

.meal-cals {
  font-size: 13px;
  font-weight: 700;
  color: #aaa;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Nút Đặt Món & Dấu Check */
.btn-order {
  background: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 16px;
  padding: 10px 18px;
  font-family: 'Sora', sans-serif;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.check-icon {
  width: 40px; height: 40px;
  background: #00C853;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 200, 83, 0.2);
}

/* Nutrition Goal Card */
.nutrition-card {
  margin: 0 24px;
  background: #fff;
  border-radius: 32px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  border: 1px solid #f4f3ef;
}

.nutrition-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
}

.nutrition-title {
  font-family: 'Sora', sans-serif;
  font-size: 18px;
  font-weight: 800;
  color: #1a1a1a;
}

/* Nutrient Item */
.nutrient-item {
  margin-bottom: 20px;
}
.nutrient-item:last-child {
  margin-bottom: 0;
}

.nutrient-labels {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 8px;
}

.nutrient-name {
  font-family: 'Sora', sans-serif;
  font-size: 15px;
  font-weight: 800;
  color: #1a1a1a;
}

.nutrient-val {
  font-size: 13px;
  font-weight: 700;
  color: #999;
}

/* Progress Bars */
.progress-bg {
  width: 100%;
  height: 8px;
  background: #f0ede8;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
}

.fill-orange { background: #FF5A1F; width: 76%; }
.fill-blue { background: #2962FF; width: 68%; }
.fill-green { background: #00C853; width: 60%; }

/* Bottom Nav Fixed */
.bottom-nav {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 84px;
  background: rgba(255, 255, 255, 0.96);
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
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        LỊCH TRÌNH
      </div>
      <h1 class="main-title">Kế hoạch ăn uống<br>hôm nay</h1>
      <div class="sub-title">Thứ Tư, 13 Tháng 5</div>
    </div>

    <!-- Meal Cards -->
    <div class="meal-list">
      <!-- Breakfast -->
      <div class="meal-card breakfast">
        <div class="meal-info">
          <div class="meal-time">07:30 • BỮA SÁNG</div>
          <div class="meal-name">Bánh mì ốp la</div>
          <div class="meal-cals">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"></path>
            </svg>
            450 kcal
          </div>
        </div>
        <div class="check-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
      </div>

      <!-- Lunch -->
      <div class="meal-card lunch">
        <div class="meal-info">
          <div class="meal-time">12:15 • BỮA TRƯA</div>
          <div class="meal-name">Cơm tấm sườn bì</div>
          <div class="meal-cals">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"></path>
            </svg>
            450 kcal
          </div>
        </div>
        <button class="btn-order">Đặt món</button>
      </div>

      <!-- Dinner -->
      <div class="meal-card dinner">
        <div class="meal-info">
          <div class="meal-time">18:30 • BỮA TỐI</div>
          <div class="meal-name">Salad ức gà</div>
          <div class="meal-cals">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"></path>
            </svg>
            450 kcal
          </div>
        </div>
        <button class="btn-order">Đặt món</button>
      </div>
    </div>

    <!-- Nutrition Goals -->
    <div class="nutrition-card">
      <div class="nutrition-header">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <circle cx="12" cy="12" r="6"></circle>
          <circle cx="12" cy="12" r="2"></circle>
        </svg>
        <span class="nutrition-title">Mục tiêu dinh dưỡng</span>
      </div>
      
      <!-- Calories -->
      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Calories</span>
          <span class="nutrient-val">1380 / 1800 kcal</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-orange"></div></div>
      </div>

      <!-- Protein -->
      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Protein</span>
          <span class="nutrient-val">82 / 120g</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-blue"></div></div>
      </div>

      <!-- Carbs -->
      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Carbs</span>
          <span class="nutrient-val">150 / 250g</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-green"></div></div>
      </div>

    </div>

  </div> <!-- End Scroll Content -->

  <!-- Bottom Navigation -->
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
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>
      <div class="nav-dot"></div>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
    </div>
  </div>

</div>
</body>
</html>
"""

# Render HTML vào Streamlit
components.html(html_code, height=960, scrolling=False)