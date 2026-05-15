import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Sở thích",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn các thành phần mặc định của Streamlit
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Đoạn mã HTML/CSS/JS mô phỏng giao diện Sở thích bổ sung
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
    align-items: center;
    min-height: 100vh;
    font-family: 'Be Vietnam Pro', sans-serif;
  }

  .phone-frame {
    width: 390px;
    height: 844px;
    background: #ffffff;
    border-radius: 48px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.08);
    position: relative;
    padding: 20px 24px 40px;
    display: flex;
    flex-direction: column;
  }

  /* Notch */
  .phone-frame::before {
    content: '';
    position: absolute;
    top: 14px; left: 50%; transform: translateX(-50%);
    width: 120px; height: 34px;
    background: #1a1a1a;
    border-radius: 20px;
    z-index: 10;
  }

  /* Progress Bar Stepper (Toàn bộ 5 bước đã hoàn thành) */
  .stepper {
    display: flex;
    gap: 8px;
    margin-top: 40px;
    margin-bottom: 30px;
  }

  .step {
    height: 6px;
    flex: 1;
    background: #eeeeee;
    border-radius: 10px;
  }

  .step.active {
    background: #FF5A1F;
  }

  /* Icon Container */
  .icon-box {
    width: 56px;
    height: 56px;
    background: #FFF3E0;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
  }

  /* Typography */
  .title {
    font-family: 'Sora', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: #1a1a1a;
    line-height: 1.2;
    margin-bottom: 12px;
  }

  .subtitle {
    font-size: 15px;
    font-weight: 600;
    color: #757575;
    margin-bottom: 32px;
  }

  .section-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Sora', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 16px;
  }

  .realtime-tag {
    background: #FFF3E0;
    color: #FF5A1F;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 8px;
    font-weight: 700;
  }

  /* Weather Grid */
  .weather-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 32px;
  }

  .weather-card {
    background: white;
    border: 1.5px solid #f0f0f0;
    border-radius: 20px;
    padding: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .weather-card.active {
    border-color: #FF5A1F;
    background: #FFF9F7;
  }

  .weather-card span {
    font-weight: 700;
    color: #555;
  }

  .weather-card.active span {
    color: #1a1a1a;
  }

  /* Country Pills */
  .country-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 32px;
  }

  .pill {
    padding: 14px 24px;
    background: white;
    border: 1.5px solid #f0f0f0;
    border-radius: 30px;
    font-weight: 700;
    color: #555;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .pill.active {
    background: #1a1a1a;
    color: white;
    border-color: #1a1a1a;
  }

  /* Bottom Actions */
  .spacer { flex: 1; }

  .footer-actions {
    display: flex;
    gap: 12px;
    margin-bottom: 10px;
  }

  .btn-back {
    width: 70px;
    height: 64px;
    background: #f2f2f2;
    border: none;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

  .btn-discover {
    flex: 1;
    background: #FF6B35; /* Orange color from image */
    color: white;
    border: none;
    border-radius: 20px;
    padding: 20px;
    font-family: 'Sora', sans-serif;
    font-size: 17px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    box-shadow: 0 10px 20px rgba(255, 107, 53, 0.2);
  }

</style>
</head>
<body>
<div class="phone-frame">

  <div class="stepper">
    <div class="step active"></div>
    <div class="step active"></div>
    <div class="step active"></div>
    <div class="step active"></div>
    <div class="step active"></div>
  </div>

  <div class="icon-box">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="5"></circle>
      <line x1="12" y1="1" x2="12" y2="3"></line>
      <line x1="12" y1="21" x2="12" y2="23"></line>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
      <line x1="1" y1="12" x2="3" y2="12"></line>
      <line x1="21" y1="12" x2="23" y2="12"></line>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    </svg>
  </div>

  <h1 class="title">Sở thích bổ sung</h1>
  <p class="subtitle">Tối ưu gợi ý theo thời tiết và quốc gia.</p>

  <div class="section-label">
    <span>Thời tiết hiện tại</span>
    <span class="realtime-tag">Real-time</span>
  </div>

  <div class="weather-grid">
    <div class="weather-card" onclick="toggleActive(this, 'weather')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M16 13v8m-8-8v8m-4-10a9 9 0 0 1 18 0v0a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/></svg>
      <span>Mưa</span>
    </div>
    <div class="weather-card active" onclick="toggleActive(this, 'weather')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2M4.2 4.2l1.4 1.4m12.8 12.8l1.4 1.4M1 12h2m18 0h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
      <span>Nắng</span>
    </div>
    <div class="weather-card" onclick="toggleActive(this, 'weather')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M14 4c0-1.1.9-2 2-2s2 .9 2 2v12a4 4 0 0 1-8 0V4c0-1.1.9-2 2-2s2 .9 2 2z"/></svg>
      <span>Lạnh</span>
    </div>
    <div class="weather-card" onclick="toggleActive(this, 'weather')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M12 9a4 4 0 0 0-2 7.5V20a2 2 0 1 0 4 0v-3.5A4 4 0 0 0 12 9z"/></svg>
      <span>Nóng</span>
    </div>
  </div>

  <div class="section-label">
    <span>Bạn thích đồ ăn nước nào?</span>
  </div>

  <div class="country-list">
    <div class="pill active" onclick="toggleActive(this, 'pill')">Việt Nam</div>
    <div class="pill" onclick="toggleActive(this, 'pill')">Hàn Quốc</div>
    <div class="pill" onclick="toggleActive(this, 'pill')">Nhật Bản</div>
      <div class="pill" onclick="toggleActive(this, 'pill')">Trung Quốc</div>
      <div class="pill" onclick="toggleActive(this, 'pill')">Thái Lan</div>
      <div class="pill" onclick="toggleActive(this, 'pill')">Đồ Âu</div>
  </div>

  <div class="spacer"></div>

  <div class="footer-actions">
    <button class="btn-back" onclick="alert('Quay lại!')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>
    
    <button class="btn-discover" onclick="alert('Bắt đầu khám phá món ăn!')">
      <span>Khám phá ngay</span>
      <span>🍴</span>
    </button>
  </div>

</div>

<script>
  function toggleActive(el, type) {
    const selector = type === 'weather' ? '.weather-card' : '.pill';
    document.querySelectorAll(selector).forEach(item => item.classList.remove('active'));
    el.classList.add('active');
  }
</script>

</body>
</html>
"""

# Render mã HTML trong Streamlit
components.html(html_code, height=950, scrolling=False)