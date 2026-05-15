import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Ngân sách",
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

# Đoạn mã HTML/CSS mô phỏng giao diện Chọn Ngân Sách
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

  /* Wallet Icon Container */
  .icon-box {
    width: 56px;
    height: 56px;
    background: #FFF0EB;
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

  /* Option List */
  .options-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .option-card {
    background: white;
    border: 1.5px solid #f0f0f0;
    border-radius: 20px;
    padding: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .option-text {
    font-family: 'Sora', sans-serif;
    font-size: 18px;
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

  /* Spacer */
  .spacer { flex: 1; }

  /* Submit Button */
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
    font-size: 17px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
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

  <!-- Progress Bar -->
  <div class="stepper">
    <div class="step active"></div>
    <div class="step"></div>
    <div class="step"></div>
    <div class="step"></div>
    <div class="step"></div>
  </div>

  <!-- Wallet Icon -->
  <div class="icon-box">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4"></path>
      <path d="M4 6v12c0 1.1.9 2 2 2h14v-4"></path>
      <path d="M18 12a2 2 0 0 0-2 2c0 1.1.9 2 2 2h4v-4h-4z"></path>
    </svg>
  </div>

  <!-- Heading -->
  <h1 class="title">Ngân sách của<br>bạn là bao nhiêu?</h1>
  <p class="subtitle">Hệ thống sẽ lọc các quán phù hợp nhất.</p>

  <!-- Options -->
  <div class="options-container">
    <div class="option-card" data-budget-key="under_30k" onclick="selectOption(this)">
      <span class="option-text">Dưới 30k</span>
    </div>

    <div class="option-card active" data-budget-key="30_50k" onclick="selectOption(this)">
      <span class="option-text">30k - 50k</span>
    </div>

    <div class="option-card" data-budget-key="50_100k" onclick="selectOption(this)">
      <span class="option-text">50k - 100k</span>
    </div>

    <div class="option-card" data-budget-key="over_100k" onclick="selectOption(this)">
      <span class="option-text">Trên 100k</span>
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
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
  </div>

</div>

<script>
  window.userBudget = '30_50k';

  function selectOption(el) {
    document.querySelectorAll('.option-card').forEach(card => {
      card.classList.remove('active');
    });
    el.classList.add('active');
    window.userBudget = el.getAttribute('data-budget-key') || '30_50k';
  }
</script>

</body>
</html>
"""

# Render mã HTML trong Streamlit
components.html(html_code, height=950, scrolling=False)