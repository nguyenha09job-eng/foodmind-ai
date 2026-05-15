import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Chế độ ăn",
    page_icon="🥗",
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

# Đoạn mã HTML/CSS/JS mô phỏng giao diện Chọn Chế độ ăn
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

  /* Progress Bar Stepper (5 steps, 4 active for this screen) */
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

  /* Diet Options Grid */
  .grid-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
  }

  .diet-card {
    background: white;
    border: 1.5px solid #f0f0f0;
    border-radius: 20px;
    padding: 20px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .diet-title {
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #666;
    margin-bottom: 12px;
  }

  .diet-cals {
    font-size: 13px;
    font-weight: 600;
    color: #999;
  }

  /* Active Card State */
  .diet-card.active {
    border-color: #FF5A1F;
    background: #FFF9F7;
  }

  .diet-card.active .diet-title {
    color: #1a1a1a;
  }

  /* AI Info Banner */
  .info-banner {
    background: #F4F8FF;
    border-radius: 16px;
    padding: 16px;
    display: flex;
    gap: 12px;
    align-items: center;
    margin-bottom: auto; /* Pushes footer to bottom */
  }

  .info-icon {
    min-width: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .info-text {
    color: #0056D2;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.5;
  }

  /* Bottom Actions */
  .footer-actions {
    display: flex;
    gap: 12px;
    margin-top: 24px;
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
    transition: background 0.2s;
  }
  .btn-back:hover { background: #e0e0e0; }

  .btn-next {
    flex: 1;
    background: #1a1a1a;
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
    transition: transform 0.1s;
  }
  .btn-next:active { transform: scale(0.98); }

</style>
</head>
<body>
<div class="phone-frame">

  <div class="stepper">
    <div class="step active"></div>
    <div class="step active"></div>
    <div class="step active"></div>
    <div class="step active"></div>
    <div class="step"></div>
  </div>

  <div class="icon-box">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path>
      <path d="M7 2v20"></path>
      <path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path>
      <line x1="3" y1="21" x2="21" y2="3"></line> </svg>
  </div>

  <h1 class="title">Chế độ ăn & Calo</h1>
  <p class="subtitle">Lựa chọn phù hợp với mục tiêu dinh dưỡng.</p>

  <div class="grid-container">
    <div class="diet-card" data-diet-key="Diet" onclick="selectOption(this)">
      <div class="diet-title">Eat clean</div>
      <div class="diet-cals">300-500 kcal</div>
    </div>

    <div class="diet-card active" data-diet-key="Normal" onclick="selectOption(this)">
      <div class="diet-title">Healthy</div>
      <div class="diet-cals">450-650 kcal</div>
    </div>

    <div class="diet-card" data-diet-key="Diet" onclick="selectOption(this)">
      <div class="diet-title">Low carb</div>
      <div class="diet-cals">400-600 kcal</div>
    </div>

    <div class="diet-card" data-diet-key="Bulking" onclick="selectOption(this)">
      <div class="diet-title">High protein</div>
      <div class="diet-cals">600-800 kcal</div>
    </div>

    <div class="diet-card" data-diet-key="Bulking" onclick="selectOption(this)">
      <div class="diet-title">Bulking</div>
      <div class="diet-cals">800-1200 kcal</div>
    </div>

    <div class="diet-card" data-diet-key="Normal" onclick="selectOption(this)">
      <div class="diet-title">Không quan tâm</div>
      <div class="diet-cals">Bất kỳ</div>
    </div>
  </div>

  <div class="info-banner">
    <div class="info-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0056D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>
    </div>
    <div class="info-text">
      AI sẽ tự động tính toán khoảng Calo tối ưu dựa trên mức độ đói và chế độ bạn chọn.
    </div>
  </div>

  <div class="footer-actions">
    <button class="btn-back" onclick="alert('Quay lại!')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>
    
    <button class="btn-next" onclick="alert('Tiếp tục!')">
      <span>Tiếp tục</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
  </div>

</div>

<script>
  window.userDiet = 'Normal';

  function selectOption(el) {
    document.querySelectorAll('.diet-card').forEach(card => card.classList.remove('active'));
    el.classList.add('active');
    window.userDiet = el.getAttribute('data-diet-key') || 'Normal';
  }
</script>

</body>
</html>
"""

# Render mã HTML trong Streamlit
components.html(html_code, height=950, scrolling=False)