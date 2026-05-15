import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Mức độ đói",
    page_icon="😋",
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

# Đoạn mã HTML/CSS/JS mô phỏng giao diện Chọn Mức độ đói
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

  /* Progress Bar Stepper (4 steps, 3 active for this screen) */
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

  /* Clock Icon Container -> changed to Flame Icon */
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
    font-size: 38px;
    font-weight: 800;
    color: #1a1a1a;
    line-height: 1.15;
    margin-bottom: 12px;
  }

  .subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #757575;
    margin-bottom: 40px;
  }

  /* Slider UI Area */
  .slider-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-top: -40px; /* Adjusting center alignment */
  }

  .emoji-display {
    font-size: 80px;
    line-height: 1;
    margin-bottom: 16px;
    filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1));
    transition: all 0.3s ease;
  }

  .status-badge {
    background: #1a1a1a;
    color: white;
    font-family: 'Sora', sans-serif;
    font-size: 18px;
    font-weight: 700;
    padding: 14px 32px;
    border-radius: 30px;
    margin-bottom: 48px;
    transition: all 0.3s ease;
  }

  .slider-wrapper {
    width: 100%;
    position: relative;
  }

  /* Custom Range Input */
  input[type=range] {
    -webkit-appearance: none;
    width: 100%;
    height: 16px;
    border-radius: 8px;
    background: #eeeeee;
    background-image: linear-gradient(90deg, #FFB703 0%, #FF5A1F 100%);
    background-size: 50% 100%;
    background-repeat: no-repeat;
    outline: none;
  }

  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    height: 30px;
    width: 30px;
    border-radius: 50%;
    background: transparent; /* Invisible thumb for clean look */
    cursor: pointer;
  }

  .slider-labels {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-top: 12px;
    font-family: 'Sora', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #999;
  }

  .slider-labels span {
    text-align: center;
    line-height: 1.25;
  }

  .slider-labels span.active {
    color: #FF5A1F;
  }

  /* Bottom Actions */
  .btn-row {
    display: flex;
    gap: 12px;
    margin-bottom: 10px;
    margin-top: auto;
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
    <div class="step"></div>
  </div>

  <div class="icon-box">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"></path>
    </svg>
  </div>

  <h1 class="title">Mức độ đói của<br>bạn hiện tại?</h1>
  <p class="subtitle">Kéo thanh trượt để tính toán khẩu phần.</p>

  <div class="slider-section">
    <div class="emoji-display" id="emoji">😋</div>
    <div class="status-badge" id="statusText">Hơi đói</div>
    
    <div class="slider-wrapper">
      <input type="range" min="0" max="3" step="1" value="1" id="hungerSlider">
      <div class="slider-labels">
        <span class="active">Ăn nhẹ</span>
        <span>Hơi đói</span>
        <span>Đói</span>
        <span>Rất đói</span>
      </div>
    </div>
  </div>

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
  const slider = document.getElementById('hungerSlider');
  const emoji = document.getElementById('emoji');
  const statusText = document.getElementById('statusText');
  const labels = document.querySelectorAll('.slider-labels span');

  const hungerStates = [
    { emoji: '🥗', text: 'Ăn nhẹ' },
    { emoji: '😋', text: 'Hơi đói' },
    { emoji: '🤤', text: 'Đói' },
    { emoji: '😫', text: 'Rất đói' }
  ];

  // Hàm cập nhật giao diện khi kéo slider
  function updateHungerSlider() {
    const val = Number(slider.value);
    const state = hungerStates[val] || hungerStates[1];
    const fill = (val / (hungerStates.length - 1)) * 100;

    // Cập nhật background fill cho thanh trượt
    slider.style.backgroundSize = fill + '% 100%';

    // Cập nhật Text và Emoji theo 4 nấc
    emoji.textContent = state.emoji;
    statusText.textContent = state.text;
    labels.forEach((label, index) => {
      label.classList.toggle('active', index === val);
    });
  }

  slider.addEventListener('input', updateHungerSlider);
  updateHungerSlider();
</script>

</body>
</html>
"""

# Render mã HTML trong Streamlit
components.html(html_code, height=950, scrolling=False)
