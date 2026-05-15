import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FoodMind AI - Đang tính toán",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    background: #f5f3ef;
    border-radius: 48px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.08);
    position: relative;
    padding: 60px 28px 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
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

  /* Ambient glow */
  .glow {
    position: absolute;
    top: 30px; left: 50%; transform: translateX(-50%);
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(255,90,31,0.15) 0%, transparent 70%);
    pointer-events: none;
  }

  /* Logo */
  .logo-wrap {
    margin-top: 10px;
    margin-bottom: 32px;
    position: relative;
  }

  .logo-icon {
    width: 80px; height: 80px;
    background: #FF5A1F;
    border-radius: 26px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 12px 32px rgba(255,90,31,0.40);
    position: relative;
  }

  .logo-icon::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 26px;
    background: linear-gradient(135deg, rgba(255,255,255,0.22) 0%, transparent 55%);
  }

  /* Title */
  .title {
    font-family: 'Sora', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: #1a1a1a;
    text-align: center;
    line-height: 1.2;
    letter-spacing: -1px;
    margin-bottom: 36px;
    width: 100%;
  }

  /* Checklist */
  .checklist {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 36px;
  }

  .check-item {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .check-circle {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: #22C55E;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    opacity: 0;
    transform: scale(0.5);
    animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  }

  .check-item:nth-child(1) .check-circle { animation-delay: 0.3s; }
  .check-item:nth-child(2) .check-circle { animation-delay: 0.9s; }
  .check-item:nth-child(3) .check-circle { animation-delay: 1.5s; }

  @keyframes popIn {
    to { opacity: 1; transform: scale(1); }
  }

  .check-label {
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #1a1a1a;
    opacity: 0;
    transform: translateX(-8px);
    animation: fadeSlide 0.35s ease forwards;
  }

  .check-item:nth-child(1) .check-label { animation-delay: 0.35s; }
  .check-item:nth-child(2) .check-label { animation-delay: 0.95s; }
  .check-item:nth-child(3) .check-label { animation-delay: 1.55s; }

  @keyframes fadeSlide {
    to { opacity: 1; transform: translateX(0); }
  }

  /* Fuzzy Engine Card */
  .engine-card {
    width: 100%;
    background: #ffffff;
    border-radius: 24px;
    padding: 20px 22px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    opacity: 0;
    animation: fadeUp 0.5s ease 2.1s forwards;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .engine-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 18px;
  }

  .live-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #EF4444;
    animation: pulse 1.2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
  }

  .engine-title {
    font-family: 'Sora', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #999;
    text-transform: uppercase;
  }

  /* Progress rows */
  .progress-row {
    margin-bottom: 16px;
  }

  .progress-row:last-child { margin-bottom: 0; }

  .progress-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .progress-label {
    font-size: 14px;
    color: #888;
    font-weight: 500;
  }

  .progress-value {
    font-family: 'Sora', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #1a1a1a;
  }

  .progress-track {
    width: 100%;
    height: 8px;
    background: #f0f0f0;
    border-radius: 99px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    border-radius: 99px;
    width: 0%;
    animation: fillBar 1s ease 2.4s forwards;
  }

  .fill-orange { background: #FF5A1F; }
  .fill-yellow { background: #F59E0B; }

  .bar-hunger { --target: 50%; }
  .bar-budget { --target: 60%; }

  @keyframes fillBar {
    to { width: var(--target); }
  }

</style>
</head>
<body>
<div class="phone-frame">
  <div class="glow"></div>

  <!-- Logo -->
  <div class="logo-wrap">
    <div class="logo-icon">
      <!-- Lightning bolt -->
      <svg width="38" height="38" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="position:relative;z-index:1;">
        <path d="M13 2L4.5 13.5H11.5L10.5 22L19.5 10H12.5L13 2Z" fill="white"/>
      </svg>
    </div>
  </div>

  <!-- Title -->
  <h1 class="title">AI FoodMind đang<br>tính toán cho bạn...</h1>

  <!-- Checklist -->
  <div class="checklist">
    <div class="check-item">
      <div class="check-circle">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>
      <span class="check-label">Phân tích Preference người dùng</span>
    </div>

    <div class="check-item">
      <div class="check-circle">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>
      <span class="check-label">Áp dụng Logic Mờ (Fuzzy Logic)</span>
    </div>

    <div class="check-item">
      <div class="check-circle">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>
      <span class="check-label">Xếp hạng quán ăn theo Match Score</span>
    </div>
  </div>

  <!-- Fuzzy Engine Card -->
  <div class="engine-card">
    <div class="engine-header">
      <div class="live-dot"></div>
      <span class="engine-title">Fuzzy Engine Live</span>
    </div>

    <div class="progress-row">
      <div class="progress-meta">
        <span class="progress-label">Độ đói (50%)</span>
        <span class="progress-value">Cao</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill fill-orange bar-hunger"></div>
      </div>
    </div>

    <div class="progress-row">
      <div class="progress-meta">
        <span class="progress-label">Budget (30k – 50k)</span>
        <span class="progress-value">Hợp lý</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill fill-yellow bar-budget"></div>
      </div>
    </div>
  </div>

</div>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)