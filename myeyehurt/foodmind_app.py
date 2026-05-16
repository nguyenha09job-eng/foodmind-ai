import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn các thành phần mặc định của Streamlit (header, footer, padding) để giao diện tràn viền đẹp hơn
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

# Đoạn mã HTML/CSS của bạn
html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600&display=swap" rel="stylesheet">
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
    min-height: 844px;
    background: #f5f3ef;
    border-radius: 48px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.08);
    overflow: hidden;
    position: relative;
    padding: 60px 28px 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
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

  /* Logo */
  .logo-wrap {
    margin-top: 16px;
    margin-bottom: 28px;
  }

  .logo-icon {
    width: 72px; height: 72px;
    background: #FF5A1F;
    border-radius: 22px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 8px 24px rgba(255,90,31,0.35);
    position: relative;
  }

  .logo-icon::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(255,255,255,0.25) 0%, transparent 60%);
  }

  .logo-icon svg {
    width: 36px; height: 36px;
    fill: white;
    position: relative; z-index: 1;
  }

  /* Brand name */
  .brand-name {
    font-family: 'Sora', sans-serif;
    font-size: 38px;
    font-weight: 800;
    color: #0f0f0f;
    text-align: center;
    letter-spacing: -1.5px;
    margin-bottom: 10px;
  }

  .tagline {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: #555;
    font-weight: 500;
  }

  .tagline .spark {
    color: #FF5A1F;
    font-size: 16px;
  }

  /* Card stack */
  .cards-section {
    width: 100%;
    position: relative;
    height: 170px;
    margin: 32px 0 24px;
  }

  .card-back {
    position: absolute;
    top: 18px;
    left: -8px;
    right: 36px;
    height: 130px;
    background: #fff;
    border-radius: 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    display: flex;
    align-items: center;
    padding: 16px 20px;
    gap: 14px;
    opacity: 0.7;
  }

  .card-back-img {
    width: 56px; height: 56px;
    background: #fde8c8;
    border-radius: 14px;
    overflow: hidden;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
  }

  .card-back-text {
    font-family: 'Sora', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #888;
  }

  .card-main {
    position: absolute;
    top: 0;
    left: 24px;
    right: 0;
    height: 140px;
    background: #1a1a1a;
    border-radius: 22px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.22);
    display: flex;
    align-items: center;
    padding: 18px 20px;
    gap: 14px;
  }

  .food-emoji-wrap {
    width: 52px; height: 52px;
    background: rgba(255,255,255,0.1);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    flex-shrink: 0;
  }

  .card-info {
    flex: 1;
  }

  .match-badge {
    display: inline-flex;
    align-items: center;
    background: #FF5A1F;
    color: white;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Sora', sans-serif;
    letter-spacing: 0.5px;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
  }

  .card-food-name {
    font-family: 'Sora', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #fff;
    line-height: 1.2;
    letter-spacing: -0.5px;
  }

  /* Buttons */
  .btn-primary {
    width: 100%;
    background: #FF5A1F;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 18px 28px;
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
    box-shadow: 0 6px 20px rgba(255,90,31,0.35);
    transition: transform 0.15s, box-shadow 0.15s;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(255,90,31,0.42);
  }

  .btn-primary:active { transform: scale(0.98); }

  .btn-arrow {
    width: 32px; height: 32px;
    background: rgba(255,255,255,0.25);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
  }

  .btn-secondary {
    width: 100%;
    background: white;
    color: #1a1a1a;
    border: 1.5px solid rgba(0,0,0,0.08);
    border-radius: 50px;
    padding: 16px 28px;
    font-family: 'Be Vietnam Pro', sans-serif;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-bottom: 22px;
    transition: background 0.15s;
  }

  .btn-secondary:hover { background: #f0f0f0; }

  .spark-icon { color: #FF5A1F; font-size: 18px; }

  /* Login text */
  .login-text {
    font-size: 14px;
    color: #888;
    margin-bottom: 24px;
  }

  .login-text a {
    color: #1a1a1a;
    font-weight: 700;
    text-decoration: none;
  }

  /* Footer */
  .footer-text {
    font-size: 12px;
    color: #aaa;
    text-align: center;
    line-height: 1.6;
    padding: 0 8px;
  }

  .divider {
    width: 40px; height: 4px;
    background: #1a1a1a;
    border-radius: 2px;
    margin: 0 auto;
    margin-top: 16px;
  }

  /* Ambient glow behind logo */
  .glow {
    position: absolute;
    top: 40px; left: 50%; transform: translateX(-50%);
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,90,31,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }
</style>
</head>
<body>
<div class="phone-frame">
  <div class="glow"></div>

  <!-- Logo -->
  <div class="logo-wrap">
    <div class="logo-icon">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 12l7-7 7 7M12 5v14"/>
        <path d="M4 12l8-8 8 8" style="display:none"/>
        <path d="M2 12L12 2l10 10M12 2v20" style="display:none"/>
      </svg>
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;margin:auto;width:36px;height:36px;">
        <path d="M22 2L11 13M22 2L15 22L11 13L2 9L22 2Z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </svg>
    </div>
  </div>

  <!-- Brand -->
  <div class="brand-name">FoodMind AI</div>
  <div class="tagline">
    <span class="spark">✦</span>
    <span>Thế hệ đặt đồ ăn thông minh mới</span>
  </div>

  <!-- Card Stack -->
  <div class="cards-section">
    <div class="card-back">
      <div class="card-back-img">🍱</div>
      <div class="card-back-text">Cơm...</div>
    </div>
    <div class="card-main">
      <div class="food-emoji-wrap">🥗</div>
      <div class="card-info">
        <div class="match-badge">96% MATCH</div>
        <div class="card-food-name">Healthy Poke<br>Bowl</div>
      </div>
    </div>
  </div>

  <!-- Buttons -->
  <button class="btn-primary" onclick="alert('Bắt đầu khám phá!')">
    <span>Khám phá ngay</span>
    <div class="btn-arrow">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
    </div>
  </button>

  <button class="btn-secondary" onclick="document.getElementById('guide-modal').style.display='flex'">
    <span class="spark-icon">✦</span>
    <span>Xem giới thiệu tính năng</span>
  </button>

  <!-- Login -->
  <p class="login-text">Đã có tài khoản? <a href="#">Đăng nhập</a></p>

  <!-- Footer -->
  <p class="footer-text">
    FoodMind AI sử dụng hệ thống Logic Mờ để đưa ra gợi ý tốt nhất cho sức khỏe và ngân sách của bạn.
  </p>

  <div class="divider"></div>

  <!-- Guide Modal -->
  <div id="guide-modal" style="display:none; position:absolute; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.88); z-index:9999; justify-content:center; align-items:flex-start; overflow-y:auto; -webkit-overflow-scrolling:touch; padding:16px; border-radius:48px;">
    <div style="position:relative; width:100%;">
      <div onclick="document.getElementById('guide-modal').style.display='none'" style="position:sticky; top:0; z-index:10000; display:flex; justify-content:flex-end; padding:8px 0;">
        <div style="width:36px; height:36px; background:rgba(255,255,255,0.2); backdrop-filter:blur(10px); border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; border:1px solid rgba(255,255,255,0.25);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </div>
      </div>
      <img src="__HUONGDAN_BASE64__" style="width:100%; border-radius:12px;" />
    </div>
  </div>
</div>
</body>
</html>
"""

# Render mã HTML trong Streamlit
# Chiều cao (height) được đặt ở mức 900px để chứa đủ thiết kế khung điện thoại 844px + lề
components.html(html_code, height=950, scrolling=False)