import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Thời gian",
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

# Đoạn mã HTML/CSS mô phỏng giao diện Chọn Thời Gian Chờ
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

  /* Progress Bar Stepper */
  .stepper {
    display: flex;
    gap: 8px;
    margin-top: 40px;
    margin-bottom: 40px;
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

  /* Clock Icon Container - Green Style */
  .icon-box {
    width: 56px;
    height: 56px;
    background: #E8F5E9;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
  }

  /* Typography */
  .title {
    font-family: 'Sora', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #1a1a1a;
    line-height: 1.1;
    margin-bottom: 12px;
  }

  .subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #888;
    margin-bottom: 40px;
  }

  /* Grid Layout for Options */
  .grid-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .option-card {
    background: white;
    border: 1.5px solid #f0f0f0;
    border-radius: 24px;
    padding: 24px 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 160px;
    text-align: center;
  }

  .card-icon {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .option-text {
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #555;
  }

  /* Active State */
  .option-card.active {
    border-color: #FF5A1F;
    background: #FFF9F7;
  }

  .option-card.active .option-text {
    color: #1a1a1a;
  }

  /* Icons Colors */
  .bg-orange { background: #FFF3E0; }
  .bg-green { background: #E8F5E9; }
  .bg-blue { background: #E3F2FD; }
  .bg-gray { background: #F5F5F5; }

  /* Bottom Actions */
  .spacer { flex: 1; }

  .btn-row {
    display: flex;
    gap: 12px;
    margin-bottom: 10px;
  }

  .btn-back {
    width: 56px;
    height: 56px;
    background: #e8e8e8;
    color: #555;
    border: none;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex-shrink: 0;
    transition: background 0.2s ease;
  }

  .btn-back:hover {
    background: #d8d8d8;
  }

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
  }

</style>
</head>
<body>
<div class="phone-frame">

  <!-- Progress Bar (Step 2 active) -->
  <div class="stepper">
    <div class="step active"></div>
    <div class="step active"></div>
    <div class="step"></div>
    <div class="step"></div>
    <div class="step"></div>
  </div>

  <!-- Header Icon -->
  <div class="icon-box">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2E7D32" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"></circle>
      <polyline points="12 6 12 12 16 14"></polyline>
    </svg>
  </div>

  <!-- Heading -->
  <h1 class="title">Bạn có thể chờ<br>trong bao lâu?</h1>
  <p class="subtitle">Tốc độ giao hàng mong muốn.</p>

  <!-- Grid Options -->
  <div class="grid-container">
    <!-- Option 1 -->
    <div class="option-card" data-time-key="express" onclick="selectOption(this)">
      <div class="card-icon bg-orange">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FB8C00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
      </div>
      <span class="option-text">Cực nhanh</span>
    </div>

    <!-- Option 2 (Active) -->
    <div class="option-card active" data-time-key="fast" onclick="selectOption(this)">
      <div class="card-icon bg-green">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2E7D32" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </div>
      <span class="option-text">Nhanh</span>
    </div>

    <!-- Option 3 -->
    <div class="option-card" data-time-key="normal" onclick="selectOption(this)">
      <div class="card-icon bg-blue">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1976D2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </div>
      <span class="option-text">Bình thường</span>
    </div>

    <!-- Option 4 -->
    <div class="option-card" data-time-key="no_rush" onclick="selectOption(this)">
      <div class="card-icon bg-gray">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#757575" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </div>
      <span class="option-text">Không gấp</span>
    </div>
  </div>

  <div class="spacer"></div>

  <!-- Footer Buttons -->
  <div class="btn-row">
    <button class="btn-back" onclick="goBack()">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
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
  window.userTime = 'fast';

  function selectOption(el) {
    document.querySelectorAll('.option-card').forEach(card => card.classList.remove('active'));
    el.classList.add('active');
    window.userTime = el.getAttribute('data-time-key') || 'fast';
  }
</script>

</body>
</html>
"""

# Render mã HTML trong Streamlit
components.html(html_code, height=950, scrolling=False)