import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Đơn đã đến",
    page_icon="✅",
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

# Đoạn mã HTML/CSS/JS cho giao diện Success Screen
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

  body { background: #f2f0eb; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: 'Be Vietnam Pro', sans-serif; }

  .phone-frame {
    width: 390px; height: 844px; background: #f5f3ef; border-radius: 48px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.08);
    position: relative; overflow: hidden; display: flex; flex-direction: column;
  }

  /* Notch (Camera trước) - Tăng z-index để luôn nổi lên trên cùng */
  .phone-frame::before {
    content: ''; position: absolute; top: 14px; left: 50%; transform: translateX(-50%);
    width: 120px; height: 34px; background: #1a1a1a; border-radius: 20px; z-index: 100;
  }

  /* ================= CSS MÀN HÌNH 1 (LOADING) ================= */
  #screen-loading {
    display: flex; flex-direction: column; align-items: center;
    padding: 60px 28px 48px; width: 100%; height: 100%;
  }
  .glow { position: absolute; top: 30px; left: 50%; transform: translateX(-50%); width: 240px; height: 240px; background: radial-gradient(circle, rgba(255,90,31,0.15) 0%, transparent 70%); pointer-events: none; }
  .logo-wrap { margin-top: 10px; margin-bottom: 32px; position: relative; }
  .logo-icon { width: 80px; height: 80px; background: #FF5A1F; border-radius: 26px; display: flex; align-items: center; justify-content: center; box-shadow: 0 12px 32px rgba(255,90,31,0.40); position: relative; }
  .logo-icon::after { content: ''; position: absolute; inset: 0; border-radius: 26px; background: linear-gradient(135deg, rgba(255,255,255,0.22) 0%, transparent 55%); }
  .title { font-family: 'Sora', sans-serif; font-size: 34px; font-weight: 800; color: #1a1a1a; text-align: center; line-height: 1.2; letter-spacing: -1px; margin-bottom: 36px; width: 100%; }
  
  .checklist { width: 100%; display: flex; flex-direction: column; gap: 20px; margin-bottom: 36px; }
  .check-item { display: flex; align-items: center; gap: 16px; }
  .check-circle { width: 32px; height: 32px; border-radius: 50%; background: #22C55E; display: flex; align-items: center; justify-content: center; flex-shrink: 0; opacity: 0; transform: scale(0.5); animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
  .check-item:nth-child(1) .check-circle { animation-delay: 0.3s; }
  .check-item:nth-child(2) .check-circle { animation-delay: 0.9s; }
  .check-item:nth-child(3) .check-circle { animation-delay: 1.5s; }
  @keyframes popIn { to { opacity: 1; transform: scale(1); } }
  .check-label { font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 700; color: #1a1a1a; opacity: 0; transform: translateX(-8px); animation: fadeSlide 0.35s ease forwards; }
  .check-item:nth-child(1) .check-label { animation-delay: 0.35s; }
  .check-item:nth-child(2) .check-label { animation-delay: 0.95s; }
  .check-item:nth-child(3) .check-label { animation-delay: 1.55s; }
  @keyframes fadeSlide { to { opacity: 1; transform: translateX(0); } }

  .engine-card { width: 100%; background: #ffffff; border-radius: 24px; padding: 20px 22px; box-shadow: 0 2px 16px rgba(0,0,0,0.06); opacity: 0; animation: fadeUp 0.5s ease 2.1s forwards; }
  @keyframes fadeUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
  .engine-header { display: flex; align-items: center; gap: 8px; margin-bottom: 18px; }
  .live-dot { width: 8px; height: 8px; border-radius: 50%; background: #EF4444; animation: pulse 1.2s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(0.8); } }
  .engine-title { font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 700; letter-spacing: 1.5px; color: #999; text-transform: uppercase; }
  .progress-row { margin-bottom: 16px; }
  .progress-row:last-child { margin-bottom: 0; }
  .progress-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .progress-label { font-size: 14px; color: #888; font-weight: 500; }
  .progress-value { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 700; color: #1a1a1a; }
  #screen-loading .progress-track { width: 100%; height: 8px; background: #f0f0f0; border-radius: 99px; overflow: hidden; }
  #screen-loading .progress-fill { height: 100%; border-radius: 99px; width: 0%; animation: fillBar 1s ease 2.4s forwards; }
  #screen-loading .fill-orange { background: #FF5A1F; } #screen-loading .fill-yellow { background: #F59E0B; }
  #screen-loading .bar-hunger { --target: 50%; } #screen-loading .bar-budget { --target: 60%; }
  @keyframes fillBar { to { width: var(--target); } }

  /* ================= CSS MÀN HÌNH 2 (RESULT) ================= */
  #screen-result {
    display: none; /* Ẩn mặc định, JS sẽ bật lên thành flex */
    flex-direction: column; position: absolute; inset: 0;
    background: #fafaf8; z-index: 50;
  }
  .scroll-content { flex: 1; overflow-y: auto; padding: 70px 0 300px; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
  .scroll-content::-webkit-scrollbar { display: none; }
  .top-bar { display: flex; align-items: center; justify-content: space-between; padding: 0 24px; margin-bottom: 28px; }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-icon { width: 46px; height: 46px; background: #FF5A1F; border-radius: 14px; display: flex; align-items: center; justify-content: center; }
  .brand-text { display: flex; flex-direction: column; }
  .brand-label { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; color: #999; text-transform: uppercase; }
  .brand-location { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 700; color: #1a1a1a; }
  .top-actions { display: flex; gap: 10px; }
  .icon-btn { width: 40px; height: 40px; border-radius: 50%; border: 1.5px solid #e8e6e0; background: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer; position: relative; }
  .notif-dot { position: absolute; top: 6px; right: 6px; width: 8px; height: 8px; background: #FF5A1F; border-radius: 50%; border: 1.5px solid #fff; }
  .hero-title { font-family: 'Sora', sans-serif; font-size: 36px; font-weight: 800; color: #1a1a1a; line-height: 1.15; letter-spacing: -1.5px; padding: 0 24px; margin-bottom: 28px; }
  .tab-wrap { padding: 0 24px; margin-bottom: 24px; }
  .tab-group { display: inline-flex; background: #eceae4; border-radius: 18px; padding: 4px; gap: 2px; }
  .tab-btn { padding: 8px 22px; border-radius: 14px; font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; border: none; cursor: pointer; transition: all 0.2s; }
  .tab-btn.active { background: #fff; color: #1a1a1a; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .tab-btn.inactive { background: transparent; color: #999; }
  .food-card-wrap { padding: 0 20px; margin-bottom: 16px; }
  .food-card { border-radius: 26px; overflow: hidden; position: relative; height: 280px; background: #2a2a2a; }
  .food-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 65%; background: linear-gradient(to top, rgba(0,0,0,0.82) 0%, transparent 100%); }
  .match-badge { position: absolute; top: 16px; right: 16px; background: rgba(255,255,255,0.96); border-radius: 16px; padding: 8px 14px; text-align: center; z-index: 2; box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
  .match-label { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; color: #999; text-transform: uppercase; display: block; margin-bottom: 2px; }
  .match-pct { font-family: 'Sora', sans-serif; font-size: 22px; font-weight: 800; color: #FF5A1F; line-height: 1; }
  .food-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px 18px; z-index: 2; }
  .food-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
  .rating-badge { display: inline-flex; align-items: center; gap: 5px; background: #FFD600; border-radius: 20px; padding: 4px 10px; }
  .rating-star { font-size: 13px; }
  .rating-val { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; color: #1a1a1a; }
  .food-distance { font-size: 13px; color: rgba(255,255,255,0.75); font-weight: 500; }
  .food-bottom { display: flex; align-items: center; justify-content: space-between; }
  .food-name { font-family: 'Sora', sans-serif; font-size: 24px; font-weight: 800; color: #fff; letter-spacing: -0.5px; }
  .price-badge { background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.28); border-radius: 12px; padding: 6px 12px; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; color: #fff; backdrop-filter: blur(8px); white-space: nowrap; }
  .tags-row { display: flex; flex-wrap: wrap; gap: 8px; padding: 0 20px; margin-bottom: 20px; }
  .tag { background: #fff; border: 1.5px solid #e8e6e0; border-radius: 20px; padding: 6px 14px; font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; color: #555; text-transform: uppercase; }
  .needs-card { position: absolute; bottom: 85px; left: 16px; right: 16px; background: rgba(252, 252, 252, 0.75); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 24px; padding: 18px 20px; box-shadow: 0 -4px 20px rgba(0,0,0,0.05), 0 8px 24px rgba(0,0,0,0.1); z-index: 20; }
  .needs-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
  .needs-title-row { display: flex; align-items: center; gap: 10px; }
  .needs-icon { width: 34px; height: 34px; background: #1a1a1a; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
  .needs-label { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 1px; color: #1a1a1a; text-transform: uppercase; }
  .needs-actions { display: flex; gap: 8px; }
  .needs-btn { width: 32px; height: 32px; border-radius: 50%; border: 1.5px solid rgba(232, 230, 224, 0.8); background: rgba(245, 245, 245, 0.6); display: flex; align-items: center; justify-content: center; cursor: pointer; color: #1a1a1a; }
  .needs-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px 6px; }
  .needs-item-label { font-size: 10px; font-weight: 700; letter-spacing: 1px; color: #888; text-transform: uppercase; margin-bottom: 4px; }
  .needs-item-val { font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; color: #1a1a1a; }
  #screen-result .scroll-content > .hero-title,
  #screen-result1 .scroll-content > .hero-title { font-family: 'Sora', sans-serif; font-size: 36px; font-weight: 800; color: #1a1a1a; line-height: 1.15; letter-spacing: -1.5px; padding: 0 24px; margin-bottom: 28px; }
  .food-card-peek { margin: 0 20px 20px; border-radius: 26px; background: #2a2a2a; height: 80px; overflow: hidden; position: relative; display: flex; align-items: center; padding: 0 18px; justify-content: space-between; cursor: pointer; }
  .food-card-peek::after { content: ''; position: absolute; inset: 0; background: rgba(0,0,0,0.55); }
  .peek-name { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #fff; position: relative; z-index: 1; letter-spacing: -0.3px; }
  .peek-price { font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; color: rgba(255,255,255,0.8); position: relative; z-index: 1; }
  .peek-match { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; color: #FF5A1F; position: relative; z-index: 1; }
  .bottom-nav { position: absolute; bottom: 0; left: 0; right: 0; height: 72px; background: #fff; border-top: 1px solid #f0ede8; display: flex; align-items: center; justify-content: space-around; padding: 0 16px; z-index: 30; border-bottom-left-radius: 48px; border-bottom-right-radius: 48px; }
  .nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; cursor: pointer; padding: 8px 16px; }
  .nav-icon { width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; position: relative; }
  .nav-dot { position: absolute; bottom: -4px; left: 50%; transform: translateX(-50%); width: 5px; height: 5px; background: #FF5A1F; border-radius: 50%; }
  /* BẮT ĐẦU COPY CSS SCREEN-DETAIL */
  #screen-detail .scroll-content { padding: 0 0 120px; } /* Hero quán ăn lấp đầy từ mép trên */
  .hero-header { position: relative; height: 380px; background: #2a2a2a; border-bottom-left-radius: 44px; border-bottom-right-radius: 44px; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; padding: 60px 24px 30px; }
  .hero-bg { position: absolute; inset: 0; background: linear-gradient(150deg, #5c3c22 0%, #2a1505 100%); z-index: 0; }
  .hero-bg::before { content: ''; position: absolute; inset: 0; background: var(--hero-image, url('https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=600&q=80')) center/cover; opacity: 0.6; mix-blend-mode: overlay; }  .hero-bg::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 70%; background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, transparent 100%); }
  .top-nav { position: relative; z-index: 10; display: flex; justify-content: space-between; align-items: center; }
  .circle-btn { width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,0.25); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; cursor: pointer; border: 1px solid rgba(255,255,255,0.1); }
  .hero-content { position: relative; z-index: 10; }
  .rec-badge { display: inline-block; background: #FF5A1F; color: #fff; font-family: 'Sora', sans-serif; font-size: 10px; font-weight: 800; letter-spacing: 1px; padding: 6px 12px; border-radius: 12px; text-transform: uppercase; margin-bottom: 12px; }
  .hero-title-row { display: flex; justify-content: space-between; align-items: flex-end; }
  .hero-title { font-family: 'Sora', sans-serif; font-size: 34px; font-weight: 800; color: #fff; line-height: 1.1; letter-spacing: -1px; }
  .match-box { background: #fff; border-radius: 18px; padding: 8px 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
  .match-box-label { font-size: 9px; font-weight: 800; color: #999; letter-spacing: 1px; }
  .match-box-val { font-family: 'Sora', sans-serif; font-size: 22px; font-weight: 800; color: #FF5A1F; line-height: 1.1; }
  .stats-row { display: flex; justify-content: space-between; padding: 24px 30px; margin-top: 4px; }
  .stat-col { display: flex; flex-direction: column; align-items: center; gap: 6px; flex: 1; }
  .stat-col.border { border-left: 1px solid #e8e6e0; }
  .stat-val { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: #1a1a1a; display: flex; align-items: center; gap: 4px; }
  .stat-label { font-size: 10px; font-weight: 700; color: #999; letter-spacing: 0.5px; text-transform: uppercase; }
  .ai-banner { margin: 0 24px 24px; background: #fff; border-radius: 20px; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 10px rgba(0,0,0,0.03); border: 1px solid #f0ede8; cursor: pointer; }
  .ai-banner-left { display: flex; align-items: center; gap: 12px; }
  .ai-icon-wrap { width: 32px; height: 32px; background: #fff0eb; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #FF5A1F; }
  .ai-banner-text { font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; color: #1a1a1a; }
  .menu-tabs { display: flex; gap: 10px; padding: 0 24px; margin-bottom: 24px; overflow-x: auto; scrollbar-width: none; }
  .m-tab { padding: 12px 24px; border-radius: 20px; font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; white-space: nowrap; cursor: pointer; transition: all 0.2s; }
  .m-tab.active { background: #1a1a1a; color: #fff; }
  .m-tab.inactive { background: #fff; color: #888; border: 1px solid #f0ede8; }
  .menu-list { padding: 0 24px; display: flex; flex-direction: column; gap: 16px; }
  .menu-item { background: #fff; border-radius: 24px; padding: 16px; display: flex; align-items: center; gap: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.02); border: 1px solid #f5f3ef; }
  .menu-img { width: 80px; height: 80px; border-radius: 16px; background: #eee; object-fit: cover; }
  .menu-info { flex: 1; }
  .menu-name { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; line-height: 1.3; }
  .menu-desc { font-size: 12px; color: #888; margin-bottom: 8px; font-weight: 500; }
  .menu-meta { display: flex; align-items: center; gap: 8px; font-size: 12px; }
  .menu-cal { font-weight: 700; color: #FF5A1F; }
  .menu-price { font-family: 'Sora', sans-serif; font-weight: 800; color: #1a1a1a; }
  .add-btn { width: 40px; height: 40px; border-radius: 14px; background: #1a1a1a; color: #fff; display: flex; align-items: center; justify-content: center; border: none; cursor: pointer; }
  .floating-order-box { position: absolute; bottom: 30px; left: 24px; right: 24px; z-index: 50; }
  .btn-primary { width: 100%; background: #FF5A1F; color: #fff; border: none; border-radius: 24px; padding: 18px 24px; font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; cursor: pointer; box-shadow: 0 8px 24px rgba(255, 90, 31, 0.35); transition: transform 0.2s; }
  .btn-primary:active { transform: scale(0.98); }
  #screen-success { background: #ffffff; padding: 24px; }
  #screen-success .content-wrapper { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding-bottom: 80px; }
  #screen-success .success-icon-wrap { width: 120px; height: 120px; background-color: #00C853; border-radius: 40px; display: flex; justify-content: center; align-items: center; box-shadow: 0 20px 40px rgba(0, 200, 83, 0.25); margin-bottom: 32px; }
  #screen-success .main-title { font-family: 'Sora', sans-serif; font-size: 34px; font-weight: 800; color: #1a1a1a; text-align: center; line-height: 1.25; margin-bottom: 16px; letter-spacing: -0.5px; }
  #screen-success .sub-title { font-size: 15px; color: #666; text-align: center; line-height: 1.6; margin-bottom: 40px; font-weight: 500; padding: 0 10px; }
  #screen-success .rating-card { width: 100%; background: #FAFAFA; border: 1px solid #F0F0F0; border-radius: 32px; padding: 28px 20px; display: flex; flex-direction: column; align-items: center; }
  #screen-success .rating-title { font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 800; color: #1a1a1a; margin-bottom: 24px; }
  #screen-success .stars { display: flex; gap: 12px; margin-bottom: 24px; }
  #screen-success .star { width: 40px; height: 40px; cursor: pointer; transition: transform 0.2s, fill 0.2s, stroke 0.2s; fill: none; stroke: #D9D9D9; stroke-width: 1.5; }
  #screen-success .star:active { transform: scale(0.9); }
  #screen-success .star.filled { fill: #FFD600; stroke: #FFD600; }
  #screen-success .rating-hint { font-size: 13px; font-weight: 700; color: #FF5A1F; }
  #screen-success .btn-home { position: absolute; bottom: 40px; left: 24px; right: 24px; background: #1a1a1a; color: white; border: none; border-radius: 20px; padding: 20px; font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 700; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 10px; box-shadow: 0 15px 30px rgba(0,0,0,0.15); transition: transform 0.2s; }
  #screen-success .btn-home:active { transform: scale(0.98); }
  #screen-tracking { overflow: hidden; z-index: 50; }
  #screen-tracking .top-card { position: absolute; top: 60px; left: 16px; right: 16px; background: #fff; border-radius: 36px; padding: 18px 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 8px 24px rgba(0,0,0,0.06); z-index: 50; }
  #screen-tracking .back-btn { width: 40px; height: 40px; display: flex; align-items: center; justify-content: flex-start; cursor: pointer; color: #1a1a1a; }
  #screen-tracking .eta-info { text-align: center; flex: 1; }
  #screen-tracking .eta-label { font-size: 10px; font-weight: 800; color: #999; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 2px; }
  #screen-tracking .eta-time { font-family: 'Sora', sans-serif; font-size: 20px; font-weight: 800; color: #1a1a1a; }
  #screen-tracking .time-icon { width: 44px; height: 44px; background: #FFF0EB; color: #FF5A1F; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
  #screen-tracking .route-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
  #screen-tracking .marker-restaurant { position: absolute; top: 240px; left: 160px; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; gap: 6px; z-index: 10; }
  #screen-tracking .res-icon { background: #1a1a1a; width: 48px; height: 48px; border-radius: 16px; display: flex; justify-content: center; align-items: center; font-size: 24px; border: 3px solid #fff; box-shadow: 0 8px 16px rgba(0,0,0,0.15); }
  #screen-tracking .res-label { background: #fff; padding: 6px 14px; border-radius: 12px; font-size: 12px; font-weight: 800; font-family: 'Sora', sans-serif; color: #1a1a1a; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
  #screen-tracking .marker-shipper { position: absolute; top: 420px; left: 160px; transform: translate(-50%, -50%); width: 52px; height: 52px; background: #FF5A1F; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 26px; border: 3px solid #fff; box-shadow: 0 4px 12px rgba(255, 90, 31, 0.4); z-index: 11; animation: bounce 1s infinite alternate; }
  #screen-tracking .radar-pulse { position: absolute; top: 420px; left: 160px; transform: translate(-50%, -50%); width: 52px; height: 52px; border-radius: 50%; background: rgba(255, 90, 31, 0.3); border: 2px solid rgba(255, 90, 31, 0.5); z-index: 10; animation: pulse 2s infinite ease-out; }
  @keyframes pulse { 0% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 100% { transform: translate(-50%, -50%) scale(2.2); opacity: 0; } }
  @keyframes bounce { 0% { transform: translate(-50%, -50%); } 100% { transform: translate(-50%, -54%); } }
  #screen-tracking .bottom-sheet { position: absolute; bottom: 0; left: 0; right: 0; background: #fff; border-radius: 40px 40px 0 0; padding: 16px 24px 32px; box-shadow: 0 -10px 40px rgba(0,0,0,0.1); z-index: 50; }
  #screen-tracking .drag-handle { width: 40px; height: 4px; background: #e0e0e0; border-radius: 2px; margin: 0 auto 24px; }
  #screen-tracking .driver-card { display: flex; align-items: center; background: #fafaf8; border-radius: 28px; padding: 16px; margin-bottom: 28px; }
  #screen-tracking .driver-avatar { width: 54px; height: 54px; background: #FFD600; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #1a1a1a; }
  #screen-tracking .driver-info { flex: 1; margin-left: 14px; }
  #screen-tracking .driver-name { font-family: 'Sora', sans-serif; font-weight: 800; font-size: 17px; color: #1a1a1a; margin-bottom: 4px; }
  #screen-tracking .driver-meta { font-size: 13px; color: #888; font-weight: 600; display: flex; align-items: center; gap: 6px; }
  #screen-tracking .star-rating { color: #FFC107; font-weight: 700; display:flex; align-items:center; gap:3px;}
  #screen-tracking .driver-actions { display: flex; gap: 10px; }
  #screen-tracking .action-btn { width: 48px; height: 48px; border-radius: 16px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
  #screen-tracking .btn-chat { background: #fff; border: 1.5px solid #e8e6e0; color: #1a1a1a; }
  #screen-tracking .btn-call { background: #FF5A1F; color: #fff; box-shadow: 0 4px 12px rgba(255, 90, 31, 0.3); }
  #screen-tracking .timeline-wrap { position: relative; display: flex; justify-content: space-between; margin-bottom: 32px; padding: 0 4px; }
  #screen-tracking .timeline-wrap::before { content: ''; position: absolute; top: 15px; left: 20px; right: 20px; height: 2px; background: #f0f0f0; z-index: 1; }
  #screen-tracking .timeline-wrap::after { content: ''; position: absolute; top: 15px; left: 20px; width: 75%; height: 2px; background: #00C853; z-index: 1; }
  #screen-tracking .step { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; gap: 10px; width: 50px; }
  #screen-tracking .step-icon { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: #00C853; color: #fff; }
  #screen-tracking .step-icon.current { box-shadow: 0 0 0 6px #E8F5E9; }
  #screen-tracking .step-icon.inactive { background: #f0f0f0; }
  #screen-tracking .step-icon.inactive .dot { width: 8px; height: 8px; background: #ccc; border-radius: 50%; }
  #screen-tracking .step-label { font-size: 10px; font-weight: 800; color: #1a1a1a; text-align: center; line-height: 1.3; }
  #screen-tracking .step.inactive .step-label { color: #999; font-weight: 700; }
  #screen-tracking .status-text { text-align: center; font-family: 'Sora', sans-serif; font-weight: 800; font-size: 16px; color: #FF5A1F; }
  #screen-mealplan { background: #fdfdfc; z-index: 50; padding-bottom: 0; }
  #screen-mealplan .scroll-content { padding-top: 70px; padding-bottom: 120px; }
  #screen-mealplan .header-section { padding: 20px 24px; margin-bottom: 10px; }
  #screen-mealplan .label-wrap { display: flex; align-items: center; gap: 8px; color: #FF5A1F; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; }
  #screen-mealplan .main-title { font-family: 'Sora', sans-serif; font-size: 34px; font-weight: 800; color: #1a1a1a; line-height: 1.15; letter-spacing: -1px; margin-bottom: 8px; }
  #screen-mealplan .sub-title { font-size: 16px; font-weight: 700; color: #999; }
  #screen-mealplan .meal-list { padding: 0 24px; display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; }
  #screen-mealplan .meal-card { background: #fff; border-radius: 24px; padding: 20px 20px 20px 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #f4f3ef; position: relative; overflow: hidden; }
  #screen-mealplan .meal-card::before { content: ''; position: absolute; left: 0; top: 20px; bottom: 20px; width: 6px; border-radius: 0 6px 6px 0; }
  #screen-mealplan .meal-card.breakfast::before { background: #FFD600; }
  #screen-mealplan .meal-card.lunch::before { background: #FF5A1F; }
  #screen-mealplan .meal-card.dinner::before { background: #00C853; }
  #screen-mealplan .meal-info { display: flex; flex-direction: column; gap: 6px; }
  #screen-mealplan .meal-time { font-size: 11px; font-weight: 800; color: #aaa; text-transform: uppercase; letter-spacing: 0.5px; }
  #screen-mealplan .meal-name { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #1a1a1a; }
  #screen-mealplan .meal-cals { font-size: 13px; font-weight: 700; color: #aaa; display: flex; align-items: center; gap: 4px; }
  #screen-mealplan .btn-order { background: #1a1a1a; color: #fff; border: none; border-radius: 16px; padding: 10px 18px; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; cursor: pointer; }
  #screen-mealplan .check-icon { width: 40px; height: 40px; background: #00C853; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0, 200, 83, 0.2); }
  #screen-mealplan .nutrition-card { margin: 0 24px; background: #fff; border-radius: 32px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #f4f3ef; }
  #screen-mealplan .nutrition-header { display: flex; align-items: center; gap: 10px; margin-bottom: 24px; }
  #screen-mealplan .nutrition-title { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #1a1a1a; }
  #screen-mealplan .nutrient-item { margin-bottom: 20px; }
  #screen-mealplan .nutrient-item:last-child { margin-bottom: 0; }
  #screen-mealplan .nutrient-labels { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px; }
  #screen-mealplan .nutrient-name { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: #1a1a1a; }
  #screen-mealplan .nutrient-val { font-size: 13px; font-weight: 700; color: #999; }
  #screen-mealplan .progress-bg { width: 100%; height: 8px; background: #f0ede8; border-radius: 10px; overflow: hidden; }
  #screen-mealplan .progress-fill { height: 100%; border-radius: 10px; }
  #screen-mealplan .fill-orange { background: #FF5A1F; width: 76%; }
  #screen-mealplan .fill-blue { background: #2962FF; width: 68%; }
  #screen-mealplan .fill-green { background: #00C853; width: 60%; }
  #screen-discover { background: #fdfdfc; z-index: 50; padding-bottom: 0; }
  #screen-discover .scroll-content { padding-top: 70px; padding-bottom: 120px; }
  #screen-discover .header-section { padding: 10px 24px 20px; }
  #screen-discover .label-wrap { display: flex; align-items: center; gap: 8px; color: #FF5A1F; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; }
  #screen-discover .main-title { font-family: 'Sora', sans-serif; font-size: 36px; font-weight: 800; color: #1a1a1a; line-height: 1.15; letter-spacing: -1px; }
  #screen-discover .search-box { margin: 0 24px 30px; background: #fff; border: 1px solid #f0ede8; border-radius: 20px; padding: 18px 20px; display: flex; align-items: center; gap: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
  #screen-discover .search-text { font-size: 15px; color: #999; font-weight: 500; }
  #screen-discover .section-header { display: flex; justify-content: space-between; align-items: center; padding: 0 24px; margin-bottom: 16px; }
  #screen-discover .section-title { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #1a1a1a; display: flex; align-items: center; gap: 8px; }
  #screen-discover .view-all { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 700; color: #FF5A1F; cursor: pointer; }
  #screen-discover .trending-horizontal-scroll { display: flex; gap: 16px; padding: 0 24px 10px; overflow-x: auto; scrollbar-width: none; margin-bottom: 24px; }
  #screen-discover .trending-horizontal-scroll::-webkit-scrollbar { display: none; }
  #screen-discover .trend-card { min-width: 160px; width: 160px; background: #fff; border-radius: 24px; border: 1px solid #f0ede8; box-shadow: 0 4px 15px rgba(0,0,0,0.02); position: relative; overflow: hidden; cursor: pointer; }
  #screen-discover .trend-img-wrap { width: 100%; height: 140px; position: relative; }
  #screen-discover .trend-img { width: 100%; height: 100%; object-fit: cover; }
  #screen-discover .rating-badge { position: absolute; top: 10px; right: 10px; background: rgba(255, 255, 255, 0.95); padding: 4px 8px; border-radius: 12px; font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 800; color: #1a1a1a; display: flex; align-items: center; gap: 4px; }
  #screen-discover .trend-info { padding: 16px; }
  #screen-discover .trend-name { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: #1a1a1a; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  #screen-discover .trend-loc { font-size: 12px; color: #888; font-weight: 500; display: flex; align-items: center; gap: 4px; }
  #screen-discover .recent-list { padding: 0 24px; display: flex; flex-direction: column; gap: 12px; }
  #screen-discover .recent-item { background: #fff; border-radius: 20px; padding: 12px; display: flex; align-items: center; gap: 14px; border: 1px solid #f0ede8; box-shadow: 0 2px 10px rgba(0,0,0,0.02); cursor: pointer; }
  #screen-discover .recent-img { width: 60px; height: 60px; border-radius: 16px; object-fit: cover; }
  #screen-discover .recent-info { flex: 1; }
  #screen-discover .recent-name { font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 800; color: #1a1a1a; margin-bottom: 4px; }
  #screen-discover .recent-desc { font-size: 12px; color: #999; font-weight: 500; }
  #screen-discover .chevron-icon { color: #ccc; margin-right: 8px; }
  #screen-loading { position: absolute; inset: 0; z-index: 50; background: #f5f3ef; }

  /* 1. Spark Burst Ring */
  .burst-ring {
    position: absolute;
    top: 50%; left: 50%;
    width: 150px; height: 150px;
    margin-top: -75px; margin-left: -75px;
    border: solid #FF5A1F;
    border-radius: 50%;
    z-index: 9999; /* Đè lên mọi thứ */
    pointer-events: none; /* Không chặn click chuột */
    opacity: 0;
  }

  .burst-anim {
    animation: burst 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }

  @keyframes burst {
    0% { transform: scale(0); opacity: 1; border-width: 40px; }
    100% { transform: scale(2.5); opacity: 0; border-width: 0px; }
  }

  /* 2. Page Slide-in & Crossfade */
  .page-enter {
    animation: pageSlideIn 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  }

  .page-exit {
    animation: pageSlideOut 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  }

  @keyframes pageSlideIn {
    0% { opacity: 0; transform: translateY(24px) scale(0.96); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
  }

  @keyframes pageSlideOut {
    0% { opacity: 1; transform: translateY(0) scale(1); }
    100% { opacity: 0; transform: translateY(12px) scale(0.98); } /* Tụt nhẹ xuống */
  }
</style>
</head>
<body>
<div class="phone-frame">

  <!-- =============== SCREEN 1: LOADING =============== -->
  <div id="screen-loading">
    <div class="glow"></div>
    <!-- Logo -->
    <div class="logo-wrap">
      <div class="logo-icon">
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
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <span class="check-label">Phân tích Preference người dùng</span>
      </div>
      <div class="check-item">
        <div class="check-circle">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <span class="check-label">Áp dụng Logic Mờ (Fuzzy Logic)</span>
      </div>
      <div class="check-item">
        <div class="check-circle">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
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
        <div class="progress-meta"><span class="progress-label">Độ đói (50%)</span><span class="progress-value">Cao</span></div>
        <div class="progress-track"><div class="progress-fill fill-orange bar-hunger"></div></div>
      </div>
      <div class="progress-row">
        <div class="progress-meta"><span class="progress-label">Budget (30k – 50k)</span><span class="progress-value">Hợp lý</span></div>
        <div class="progress-track"><div class="progress-fill fill-yellow bar-budget"></div></div>
      </div>
    </div>
  </div>

  <!-- =============== SCREEN 2: RESULT =============== -->
  <div id="screen-result">
    <!-- Scrollable area -->
    <div class="scroll-content">
      <!-- Top Bar -->
      <div class="top-bar">
        <div class="brand">
          <div class="brand-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2C9.5 5 6 7 6 11C6 13.8 7.8 16.2 10.5 17.3V20H13.5V17.3C16.2 16.2 18 13.8 18 11C18 7 14.5 5 12 2Z" fill="white"/>
              <path d="M10 22H14" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="brand-text">
            <span class="brand-label">FoodMind AI</span>
            <span class="brand-location">Quận 1, TP. HCM</span>
          </div>
        </div>
        <div class="top-actions">
          <div class="icon-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg></div>
          <div class="icon-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg><div class="notif-dot"></div></div>
        </div>
      </div>

      <!-- Hero & Tabs -->
      <div class="hero-title">Gợi ý AI cho<br>bạn hôm nay</div>
      <div class="tab-wrap">
        <div class="tab-group">
          <button class="tab-btn active">Quán ăn</button>
          <button class="tab-btn inactive">Món lẻ</button>
        </div>
      </div>

      <!-- Main Food Card -->
      <div class="food-card-wrap">
        <div class="food-card">
          <div style="width:100%;height:100%;background:url('https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=600&q=80') center/cover;position:relative;">
          </div>
          <div class="match-badge"><span class="match-label">Match</span><span class="match-pct">94%</span></div>
          <div class="food-info">
            <div class="food-meta">
              <div class="rating-badge"><span class="rating-star">⭐</span><span class="rating-val">4.8</span></div>
              <span class="food-distance">1.2 km • 15–20 ph</span>
            </div>
            <div class="food-bottom">
              <span class="food-name">Cơm Tấm Bà Lan</span>
              <span class="price-badge">45k – 65k</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tags & Peeks -->
      <div class="tags-row">
        <span class="tag">PHÙ HỢP 94% VỚI NHU CẦU</span><span class="tag">GIAO NHANH</span><span class="tag">NGON RẺ</span>
      </div>
      <div class="food-card-peek">
        <div style="position:absolute;inset:0;background:linear-gradient(135deg,#8b1a1a,#6b0f0f);"></div>
        <span class="peek-name">Bún Bò Huế Chu</span>
        <div style="display:flex;flex-direction:column;align-items:flex-end;position:relative;z-index:1;gap:3px;"><span class="peek-price">50k – 70k</span><span class="peek-match">87% match</span></div>
      </div>
      <div class="food-card-peek">
        <div style="position:absolute;inset:0;background:linear-gradient(135deg,#1a3a4a,#0f2a38);"></div>
        <span class="peek-name">Phở Bò Hà Nội</span>
        <div style="display:flex;flex-direction:column;align-items:flex-end;position:relative;z-index:1;gap:3px;"><span class="peek-price">45k – 60k</span><span class="peek-match">82% match</span></div>
      </div>
      <div class="food-card-peek" style="margin-bottom:0;">
        <div style="position:absolute;inset:0;background:linear-gradient(135deg,#2e4a1a,#1a380f);"></div>
        <span class="peek-name">Salad Healthy Xanh</span>
        <div style="display:flex;flex-direction:column;align-items:flex-end;position:relative;z-index:1;gap:3px;"><span class="peek-price">60k – 85k</span><span class="peek-match">78% match</span></div>
      </div>
    </div> <!-- End Scroll Content -->

    <!-- Floating Needs Summary Card -->
    <div class="needs-card">
      <div class="needs-header">
        <div class="needs-title-row">
          <div class="needs-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M8 6V4h8v2M4 12h16M6 18h12"/></svg></div>
          <span class="needs-label">Tóm tắt nhu cầu</span>
        </div>
        <div class="needs-actions">
          <div class="needs-btn needs-edit-btn" title="Chỉnh sửa nhu cầu"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></div>
          <div class="needs-btn needs-close-btn" title="Ẩn tóm tắt nhu cầu"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></div>
        </div>
      </div>
      <div class="needs-grid">
        <div class="needs-item"><div class="needs-item-label">Budget</div><div class="needs-item-val">30k - 50k</div></div>
        <div class="needs-item"><div class="needs-item-label">Độ đói</div><div class="needs-item-val">Rất đói 🔥</div></div>
        <div class="needs-item"><div class="needs-item-label">Giao hàng</div><div class="needs-item-val">Nhanh ⚡</div></div>
        <div class="needs-item"><div class="needs-item-label">Mục tiêu</div><div class="needs-item-val">Healthy 🥗</div></div>
        <div class="needs-item"><div class="needs-item-label">Ẩm thực</div><div class="needs-item-val">Việt Nam 🇻🇳</div></div>
        <div class="needs-item"><div class="needs-item-label">Weather</div><div class="needs-item-val">Nắng ☀️</div></div>
      </div>
    </div>

    <!-- Bottom Nav -->
    <div class="bottom-nav">
      <div class="nav-item"><div class="nav-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="#FF5A1F"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg><div class="nav-dot"></div></div></div>
      <div class="nav-item"><div class="nav-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg></div></div>
      <div class="nav-item"><div class="nav-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div></div>
      <div class="nav-item"><div class="nav-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div></div>
    </div>
  </div>
  <!-- BẮT ĐẦU COPY HTML SCREEN-RESULT1 -->
<div id="screen-result1" class="screen-wrapper" style="display: none; position: absolute; inset: 0; background: #fafaf8; z-index: 50; flex-direction: column;">
  <div class="scroll-content">
    <div class="top-bar">
      <div class="brand">
        <div class="brand-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M12 2C9.5 5 6 7 6 11C6 13.8 7.8 16.2 10.5 17.3V20H13.5V17.3C16.2 16.2 18 13.8 18 11C18 7 14.5 5 12 2Z" fill="white"/>
            <path d="M10 22H14" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-label">FoodMind AI</span>
          <span class="brand-location">Quận 1, TP. HCM</span>
        </div>
      </div>
      <div class="top-actions">
        <div class="icon-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.2" stroke-linecap="round">
            <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
          </svg>
        </div>
        <div class="icon-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <div class="notif-dot"></div>
        </div>
      </div>
    </div>

    <div class="hero-title">Gợi ý AI cho<br>bạn hôm nay</div>

    <div class="tab-wrap">
      <div class="tab-group">
        <button class="tab-btn active">Quán ăn</button>
        <button class="tab-btn inactive">Món lẻ</button>
      </div>
    </div>

    <div class="menu-list">
      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=150&q=80" alt="Salad ức gà áp chảo" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Salad ức gà áp chảo</div>
          <div class="menu-desc">Ức gà mềm, rau xanh, sốt mè rang nhẹ</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 430 kcal</span>
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

      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=150&q=80" alt="Cơm gạo lứt bò áp chảo" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Cơm gạo lứt bò áp chảo</div>
          <div class="menu-desc">Bò áp chảo, rau củ, cơm gạo lứt</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 610 kcal</span>
            <span style="color:#ccc">•</span>
            <span class="menu-price">62,000 đ</span>
          </div>
        </div>
        <button class="add-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>

      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&w=150&q=80" alt="Bún bò tô nhỏ" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Bún bò tô nhỏ</div>
          <div class="menu-desc">Nước dùng đậm vị, phần vừa đủ no</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 520 kcal</span>
            <span style="color:#ccc">•</span>
            <span class="menu-price">48,000 đ</span>
          </div>
        </div>
        <button class="add-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>

      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=150&q=80" alt="Greek yogurt granola" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Greek yogurt granola</div>
          <div class="menu-desc">Yogurt Hy Lạp, granola, trái cây tươi</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 310 kcal</span>
            <span style="color:#ccc">•</span>
            <span class="menu-price">42,000 đ</span>
          </div>
        </div>
        <button class="add-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>

      <div class="menu-item">
        <img src="https://images.unsplash.com/photo-1582450871972-ab5ca641643d?auto=format&fit=crop&w=150&q=80" alt="Gỏi cuốn tôm thịt" class="menu-img">
        <div class="menu-info">
          <div class="menu-name">Gỏi cuốn tôm thịt</div>
          <div class="menu-desc">Tôm, thịt nạc, rau thơm, nước chấm đậu</div>
          <div class="menu-meta">
            <span class="menu-cal">🔥 360 kcal</span>
            <span style="color:#ccc">•</span>
            <span class="menu-price">38,000 đ</span>
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

  <div class="needs-card">
    <div class="needs-header">
      <div class="needs-title-row">
        <div class="needs-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round">
            <path d="M4 6h16M8 6V4h8v2M4 12h16M6 18h12"/>
          </svg>
        </div>
        <span class="needs-label">Tóm tắt nhu cầu</span>
      </div>
      <div class="needs-actions">
        <div class="needs-btn needs-edit-btn" title="Chỉnh sửa nhu cầu">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </div>
        <div class="needs-btn needs-close-btn" title="Ẩn tóm tắt nhu cầu">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </div>
      </div>
    </div>
    <div class="needs-grid">
      <div class="needs-item">
        <div class="needs-item-label">Ngân sách</div>
        <div class="needs-item-val">30k - 50k</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Độ đói</div>
        <div class="needs-item-val">Rất đói</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Sức khỏe</div>
        <div class="needs-item-val">Healthy</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Ưu tiên</div>
        <div class="needs-item-val">Giao nhanh</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Ẩm thực</div>
        <div class="needs-item-val">Việt Nam</div>
      </div>
      <div class="needs-item">
        <div class="needs-item-label">Thời tiết</div>
        <div class="needs-item-val">Nắng ☀️</div>
      </div>
    </div>
  </div>

  <div class="bottom-nav">
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="#FF5A1F">
          <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
        </svg>
        <div class="nav-dot"></div>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/>
          <line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/>
        </svg>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
        </svg>
      </div>
    </div>
  </div>
</div>
<div id="screen-detail" class="screen-wrapper" style="display: none; position: absolute; inset: 0; background: #fafaf8; z-index: 50; flex-direction: column;">
  
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
      
      <!-- Item 3 -->
      <div class="menu-item">
<img src="https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?auto=format&fit=crop&w=150&q=80" alt="Cơm tấm đùi gà nướng" class="menu-img">        <div class="menu-info">
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
<div id="screen-success" class="screen-wrapper" style="display: none; position: absolute; inset: 0; background: #ffffff; z-index: 50; flex-direction: column; padding: 24px;">
  <div class="content-wrapper">
    <div class="success-icon-wrap">
      <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
    </div>
    <h1 class="main-title">Tuyệt vời! 👋<br>Đơn đã đến.</h1>
    <p class="sub-title">Bữa ăn của bạn đã được giao đến<br>điểm hẹn. Hãy thưởng thức nhé!</p>
    <div class="rating-card">
      <div class="rating-title">Bạn thấy thế nào?</div>
      <div class="stars">
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
      </div>
      <div class="rating-hint" id="rating-text">Chạm sao để đánh giá</div>
    </div>
  </div>
  <button class="btn-home">
    Về trang chủ 
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
      <polyline points="9 22 9 12 15 12 15 22"></polyline>
    </svg>
  </button>
</div>
<!-- BẮT ĐẦU COPY HTML SCREEN-TRACKING -->
<div id="screen-tracking" class="screen-wrapper" style="display: none; position: absolute; inset: 0; z-index: 50; flex-direction: column; background-color: #e5e2d8; background-image: linear-gradient(rgba(0,0,0,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,0.04) 1px, transparent 1px); background-size: 80px 80px; background-position: center; overflow: hidden;">
  
  <svg class="route-svg" viewBox="0 0 390 844" fill="none" xmlns="http://www.w3.org/2000/svg">
    <polyline points="160,250 160,490 320,490 320,600" stroke="#FF5A1F" stroke-width="5" stroke-linejoin="round"/>
  </svg>

  <div class="top-card">
    <div class="back-btn" id="btn-back-tracking">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
    </div>
    <div class="eta-info">
      <div class="eta-label">DỰ KIẾN GIAO</div>
      <div class="eta-time">12 phút nữa</div>
    </div>
    <div class="time-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
      </svg>
    </div>
  </div>

  <div class="marker-restaurant">
    <div class="res-icon">🍱</div>
    <div class="res-label">Bà Lan</div>
  </div>

  <div class="radar-pulse"></div>
  <div class="marker-shipper" id="shipper-btn" title="Bấm vào shipper để hoàn thành đơn nhanh">🛵</div>

  <div class="bottom-sheet">
    <div class="drag-handle"></div>

    <div class="driver-card">
      <div class="driver-avatar">MT</div>
      <div class="driver-info">
        <div class="driver-name">Minh Tuấn</div>
        <div class="driver-meta">
          <span class="star-rating">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            4.9
          </span> 
          <span>• Honda Wave</span>
        </div>
      </div>
      <div class="driver-actions">
        <div class="action-btn btn-chat">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </div>
        <div class="action-btn btn-call">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        </div>
      </div>
    </div>

    <div class="timeline-wrap">
      <div class="step">
        <div class="step-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div class="step-label">Đã xác<br>nhận</div>
      </div>
      <div class="step">
        <div class="step-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div class="step-label">Đang<br>chuẩn bị</div>
      </div>
      <div class="step">
        <div class="step-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div class="step-label">Shipper<br>nhận đơn</div>
      </div>
      <div class="step">
        <div class="step-icon current"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div class="step-label">Đang giao</div>
      </div>
      <div class="step inactive">
        <div class="step-icon inactive"><div class="dot"></div></div>
        <div class="step-label">Đã giao</div>
      </div>
    </div>

    <div class="status-text">Shipper đang trên đường</div>
  </div>
</div>
<div id="screen-mealplan" class="screen-wrapper" style="display: none; position: absolute; inset: 0; z-index: 50; flex-direction: column; background: #fdfdfc;">
  
  <div class="scroll-content">
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

    <div class="meal-list">
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
        <button class="btn-order btn-order-lunch">Đặt món</button>
      </div>

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
        <button class="btn-order btn-order-dinner">Đặt món</button>
      </div>
    </div>

    <div class="nutrition-card">
      <div class="nutrition-header">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <circle cx="12" cy="12" r="6"></circle>
          <circle cx="12" cy="12" r="2"></circle>
        </svg>
        <span class="nutrition-title">Mục tiêu dinh dưỡng</span>
      </div>
      
      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Calories</span>
          <span class="nutrient-val">1380 / 1800 kcal</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-orange"></div></div>
      </div>

      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Protein</span>
          <span class="nutrient-val">82 / 120g</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-blue"></div></div>
      </div>

      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Carbs</span>
          <span class="nutrient-val">150 / 250g</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-green"></div></div>
      </div>

    </div>

  </div>

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
<div id="screen-discover" class="screen-wrapper" style="display: none; position: absolute; inset: 0; z-index: 50; flex-direction: column; background: #fdfdfc;">
  
  <div class="scroll-content">
    <div class="header-section">
      <div class="label-wrap">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
        KHÁM PHÁ
      </div>
      <h1 class="main-title">Mở rộng khẩu vị<br>của bạn</h1>
    </div>

    <div class="search-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>
      <span class="search-text">Mọi người đang tìm: "Cơm tấm"</span>
    </div>

    <div class="section-header">
      <div class="section-title">Xu hướng hiện nay</div>
      <div class="view-all">Xem tất cả</div>
    </div>

    <div class="trending-horizontal-scroll">
      <div class="trend-card" data-restaurant="Healthy Bowl">
        <div class="trend-img-wrap">
          <img src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=300&q=80" alt="Healthy Bowl" class="trend-img">
          <div class="rating-badge"><span style="color:#FFD600">★</span> 4.9</div>
        </div>
        <div class="trend-info">
          <div class="trend-name">Healthy Bowl</div>
          <div class="trend-loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg> Quận 1</div>
        </div>
      </div>
      <div class="trend-card" data-restaurant="Sushi Haru">
        <div class="trend-img-wrap">
        <img src="https://images.unsplash.com/photo-1553621042-f6e147245754?auto=format&fit=crop&w=300&q=80" alt="Sushi Haru" class="trend-img">        </div>
        <div class="trend-info">
          <div class="trend-name">Sushi Haru</div>
          <div class="trend-loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg> Quận 3</div>
        </div>
      </div>
      <div class="trend-card" data-restaurant="Pizza Ngon">
        <div class="trend-img-wrap">
          <img src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=300&q=80" alt="Pizza" class="trend-img">
          <div class="rating-badge"><span style="color:#FFD600">★</span> 4.7</div>
        </div>
        <div class="trend-info">
          <div class="trend-name">Pizza Ngon</div>
          <div class="trend-loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg> Quận 2</div>
        </div>
      </div>
    </div>

    <div class="section-header">
      <div class="section-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        Vừa xem gần đây
      </div>
    </div>

    <div class="recent-list">
      <div class="recent-item" data-restaurant="Quán Ngon Sài Gòn">
        <img src="https://images.unsplash.com/photo-1555126634-323283e090fa?auto=format&fit=crop&w=150&q=80" alt="Quán Ngon" class="recent-img">
        <div class="recent-info">
          <div class="recent-name">Quán Ngon Sài Gòn</div>
          <div class="recent-desc">Cơm, Bún, Phở • 2.1 km</div>
        </div>
        <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
      <!-- ID ĐƯỢC GẮN VÀO ĐÂY ĐỂ BẤM CHUYỂN TRANG -->
      <div class="recent-item" id="btn-recent-comtam" data-restaurant="Cơm Tấm Bà Lan">
        <img src="https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=150&q=80" alt="Cơm Tấm Bà Lan" class="recent-img">        <div class="recent-info">
          <div class="recent-name">Cơm Tấm Bà Lan</div>
          <div class="recent-desc">Đồ nướng, Cơm • 1.2 km</div>
        </div>
        <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
      <div class="recent-item" data-restaurant="Bún Bò Huế Chu">
        <img src="https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?auto=format&fit=crop&w=150&q=80" alt="Bún bò" class="recent-img">
        <div class="recent-info">
          <div class="recent-name">Bún Bò Huế Chu</div>
          <div class="recent-desc">Bún, Phở, Món nước • 3.5 km</div>
        </div>
        <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    </div>

  </div>

  <div class="bottom-nav">
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" y1="3" x2="9" y2="18"></line><line x1="15" y1="6" x2="15" y2="21"></line></svg>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
      <div class="nav-dot"></div>
    </div>
  </div>
</div>
</div>

<script>
  // ==========================================
  // 1. CÔNG TẮC CHÍNH 
  // ==========================================
  let currentScreenId = 'screen-loading'; // Biến nhớ màn hình hiện tại
  let isAnimating = false; // Khóa không cho user bấm loạn xạ lúc đang chuyển cảnh

  function switchScreen(targetId) {
    // Bỏ qua nếu bấm lại đúng trang hiện tại hoặc đang trong lúc animation
    if (currentScreenId === targetId || isAnimating) return;
    isAnimating = true;

    const oldScreen = document.getElementById(currentScreenId);
    const newScreen = document.getElementById(targetId);

    // [EFFECT 1] Tạo Spark Burst Ring
    const phoneFrame = document.querySelector('.phone-frame');
    const burstRing = document.createElement('div');
    burstRing.className = 'burst-ring burst-anim';
    phoneFrame.appendChild(burstRing);

    // Dọn rác vòng tròn sau 0.55s
    setTimeout(() => burstRing.remove(), 550);

    // [EFFECT 2] Page Slide-in cho màn hình mới
    if (newScreen) {
      newScreen.style.display = 'flex';
      newScreen.classList.remove('page-exit');
      newScreen.classList.add('page-enter');
    }

    // [EFFECT 3] Crossfade mờ dần màn hình cũ
    if (oldScreen) {
      oldScreen.classList.remove('page-enter');
      oldScreen.classList.add('page-exit');
      
      // Đợi đúng 0.4s (bằng thời gian CSS) rồi mới gỡ hẳn màn hình cũ ra
      setTimeout(() => {
        oldScreen.style.display = 'none';
        oldScreen.classList.remove('page-exit');
        currentScreenId = targetId; // Cập nhật vị trí hiện tại
        isAnimating = false; // Mở khóa cho bấm tiếp
      }, 400); 
    } else {
      currentScreenId = targetId;
      isAnimating = false;
    }
  }

  function switchResultTab(targetId) {
    const oldScreen = document.getElementById(currentScreenId);
    const newScreen = document.getElementById(targetId);
    if (!newScreen || currentScreenId === targetId) return;

    isAnimating = false;
    if (oldScreen) {
      oldScreen.style.display = 'none';
      oldScreen.classList.remove('page-enter', 'page-exit');
    }
    newScreen.style.display = 'flex';
    newScreen.classList.remove('page-enter', 'page-exit');
    currentScreenId = targetId;
  }
  // ==========================================
  // 2. TỰ ĐỘNG CHUYỂN LOADING -> RESULT
  // ==========================================
  setTimeout(() => {
    switchScreen('screen-result');
  }, 4500);

  // ==========================================
  // 3. LOGIC LUỒNG ĐI CÁC MÀN HÌNH
  // ==========================================
  
  const restaurantDetails = {
    'Cơm Tấm Bà Lan': {
      name: 'Cơm Tấm Bà Lan',
      title: 'Cơm Tấm Bà<br>Lan',
      match: '94%',
      matchText: '94% match',
      price: '45k – 65k',
      distance: '1.2 km • 15–20 ph',
      rating: '4.8',
      tag: 'PHÙ HỢP 94% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=600&q=80')"
    },
    'Bún Bò Huế Chu': {
      name: 'Bún Bò Huế Chu',
      title: 'Bún Bò Huế<br>Chu',
      match: '87%',
      matchText: '87% match',
      price: '50k – 70k',
      distance: '1.5 km • 18–25 ph',
      rating: '4.7',
      tag: 'PHÙ HỢP 87% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&w=600&q=80')"
    },
    'Bún Bò Huế Chú Hải': {
      name: 'Bún Bò Huế Chú Hải',
      title: 'Bún Bò Huế<br>Chú Hải',
      match: '87%',
      matchText: '87% match',
      price: '50k – 70k',
      distance: '1.5 km • 18–25 ph',
      rating: '4.7',
      tag: 'PHÙ HỢP 87% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&w=600&q=80')"
    },
    'Phở Bò Hà Nội': {
      name: 'Phở Bò Hà Nội',
      title: 'Phở Bò<br>Hà Nội',
      match: '82%',
      matchText: '82% match',
      price: '45k – 60k',
      distance: '1.8 km • 20–25 ph',
      rating: '4.6',
      tag: 'PHÙ HỢP 82% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&w=600&q=80')"
    },
    'Salad Healthy Xanh': {
      name: 'Salad Healthy Xanh',
      title: 'Salad Healthy<br>Xanh',
      match: '78%',
      matchText: '78% match',
      price: '60k – 85k',
      distance: '2.0 km • 22–30 ph',
      rating: '4.5',
      tag: 'PHÙ HỢP 78% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80')"
    },
    'Healthy Bowl': {
      name: 'Healthy Bowl',
      title: 'Healthy<br>Bowl',
      match: '96%',
      matchText: '96% match',
      price: '65k – 90k',
      distance: '420 m • 8–12 ph',
      rating: '4.8',
      tag: 'PHÙ HỢP 96% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80')"
    },
    'Sushi Hokkaido': {
      name: 'Sushi Hokkaido',
      title: 'Sushi<br>Hokkaido',
      match: '88%',
      matchText: '88% match',
      price: '80k – 140k',
      distance: '600 m • 12–18 ph',
      rating: '4.7',
      tag: 'PHÙ HỢP 88% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=600&q=80')"
    },
    'Sushi Haru': {
      name: 'Sushi Haru',
      title: 'Sushi<br>Haru',
      match: '89%',
      matchText: '89% match',
      price: '85k – 150k',
      distance: '2.4 km • 25–30 ph',
      rating: '4.8',
      tag: 'PHÙ HỢP 89% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1553621042-f6e147245754?auto=format&fit=crop&w=600&q=80')"
    },
    'Pizza Ngon': {
      name: 'Pizza Ngon',
      title: 'Pizza<br>Ngon',
      match: '81%',
      matchText: '81% match',
      price: '90k – 180k',
      distance: '2.0 km • 20–30 ph',
      rating: '4.7',
      tag: 'PHÙ HỢP 81% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=600&q=80')"
    },
    'Quán Ngon Sài Gòn': {
      name: 'Quán Ngon Sài Gòn',
      title: 'Quán Ngon<br>Sài Gòn',
      match: '84%',
      matchText: '84% match',
      price: '45k – 90k',
      distance: '2.1 km • 20–25 ph',
      rating: '4.6',
      tag: 'PHÙ HỢP 84% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1555126634-323283e090fa?auto=format&fit=crop&w=600&q=80')"
    },
    'Gà Rán Jollibee': {
      name: 'Gà Rán Jollibee',
      title: 'Gà Rán<br>Jollibee',
      match: '75%',
      matchText: '75% match',
      price: '40k – 90k',
      distance: '1.6 km • 18–25 ph',
      rating: '4.4',
      tag: 'PHÙ HỢP 75% VỚI NHU CẦU',
      image: "url('https://images.unsplash.com/photo-1562967916-eb82221dfb36?auto=format&fit=crop&w=600&q=80')"
    }
  };

  let selectedRestaurantName = 'Cơm Tấm Bà Lan';
  let detailReturnScreen = 'screen-result';

  function getCurrentScreenId() {
    const visibleScreen = document.querySelector('.screen-wrapper[style*="display: flex"]');
    return visibleScreen ? visibleScreen.id : 'screen-result';
  }

  function openRestaurantDetail(name, returnScreen) {
    const detail = restaurantDetails[name] || restaurantDetails['Cơm Tấm Bà Lan'];
    const detailTitle = document.querySelector('#screen-detail .hero-title');
    const detailMatch = document.querySelector('#screen-detail .match-box-val');
    const detailBg = document.querySelector('#screen-detail .hero-bg');

    detailReturnScreen = returnScreen || getCurrentScreenId();

    if (detailTitle) detailTitle.innerHTML = detail.title;
    if (detailMatch) detailMatch.textContent = detail.match;
    if (detailBg) detailBg.style.setProperty('--hero-image', detail.image);

    switchScreen('screen-detail');
  }

  function showRestaurantAsMainCard(name, screenSelector) {
    const detail = restaurantDetails[name] || restaurantDetails['Cơm Tấm Bà Lan'];
    const screen = document.querySelector(screenSelector || '#screen-result');
    if (!screen) return;

    selectedRestaurantName = detail.name;

    const mainCard = screen.querySelector('.food-card');
    const imageLayer = mainCard ? mainCard.querySelector(':scope > div:first-child') : null;
    const matchPct = screen.querySelector('.match-pct');
    const ratingVal = screen.querySelector('.rating-val');
    const distance = screen.querySelector('.food-distance');
    const foodName = screen.querySelector('.food-name');
    const priceBadge = screen.querySelector('.price-badge');
    const firstTag = screen.querySelector('.tags-row .tag:first-child');
    const scrollContent = screen.querySelector('.scroll-content');

    if (imageLayer) {
      imageLayer.style.background = detail.image + ' center/cover';
    }
    if (matchPct) matchPct.textContent = detail.match;
    if (ratingVal) ratingVal.textContent = detail.rating;
    if (distance) distance.textContent = detail.distance;
    if (foodName) foodName.textContent = detail.name;
    if (priceBadge) priceBadge.textContent = detail.price;
    if (firstTag) firstTag.textContent = detail.tag;
    if (scrollContent) scrollContent.scrollTo({ top: 140, behavior: 'smooth' });
  }

  // Từ Result -> Detail
  const mainFoodCards = document.querySelectorAll('#screen-result .food-card, #screen-result1 .food-card');
  mainFoodCards.forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => openRestaurantDetail(selectedRestaurantName));
  });

  const restaurantPeekCards = document.querySelectorAll('#screen-result .food-card-peek, #screen-result1 .food-card-peek');
  restaurantPeekCards.forEach(card => {
    card.addEventListener('click', () => {
      const nameEl = card.querySelector('.peek-name');
      const screen = card.closest('#screen-result, #screen-result1');
      if (nameEl && screen) showRestaurantAsMainCard(nameEl.textContent.trim(), '#' + screen.id);
    });
  });

  // Từ Map -> lọc danh sách và mở chi tiết quán
  function normalizeMapSearchText(value) {
    return (value || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/đ/g, 'd');
  }

  window.filterMapRestaurants = function() {
    const mapSearchInput = document.querySelector('#screen-map .search-input');
    const mapRestaurantCards = document.querySelectorAll('#screen-map .res-card');
    const mapMarkers = document.querySelectorAll('#screen-map .map-marker');
    const mapEmptyResults = document.querySelector('#screen-map .empty-results');
    const keyword = normalizeMapSearchText(mapSearchInput ? mapSearchInput.value : '');
    let visibleCount = 0;

    mapRestaurantCards.forEach(card => {
      const searchableText = normalizeMapSearchText(
        card.dataset.restaurant || card.querySelector('.res-name')?.textContent
      );
      const isMatch = !keyword || searchableText.includes(keyword);
      card.classList.toggle('is-hidden', !isMatch);
      if (isMatch) visibleCount += 1;
    });

    mapMarkers.forEach(marker => {
      const searchableText = normalizeMapSearchText(marker.dataset.restaurant);
      marker.classList.toggle('is-hidden', Boolean(keyword) && !searchableText.includes(keyword));
    });

    if (mapEmptyResults) {
      mapEmptyResults.classList.toggle('is-visible', visibleCount === 0);
    }
  };

  document.addEventListener('input', event => {
    if (event.target.matches('#screen-map .search-input')) {
      window.filterMapRestaurants();
    }
  });

  document.addEventListener('click', event => {
    const mapRestaurant = event.target.closest('#screen-map .res-card, #screen-map .map-marker');
    if (mapRestaurant) {
      openRestaurantDetail(mapRestaurant.dataset.restaurant, 'screen-map');
    }
  });

  document.addEventListener('click', event => {
    const discoverRestaurant = event.target.closest('#screen-discover .trend-card, #screen-discover .recent-item');
    if (discoverRestaurant) {
      const restaurantName = discoverRestaurant.dataset.restaurant
        || discoverRestaurant.querySelector('.trend-name, .recent-name')?.textContent?.trim();
      openRestaurantDetail(restaurantName, 'screen-discover');
    }
  });

  document.addEventListener('click', event => {
    const editNeedsBtn = event.target.closest('.needs-edit-btn');
    if (editNeedsBtn) {
      window.parent.postMessage({ type: 'foodmind-edit-needs' }, '*');
      return;
    }

    const closeNeedsBtn = event.target.closest('.needs-close-btn');
    if (closeNeedsBtn) {
      const needsCard = closeNeedsBtn.closest('.needs-card');
      if (needsCard) needsCard.style.display = 'none';
    }
  });

  // Back từ Detail -> Result
  const backBtn = document.querySelector('#screen-detail .circle-btn'); 
  if (backBtn) {
    backBtn.addEventListener('click', () => switchScreen(detailReturnScreen || 'screen-result'));
  }

  // Đổi tab "Quán ăn" và "Món lẻ" (giữa Result và Result 1)
  const tabsResult = document.querySelectorAll('#screen-result .tab-btn');
  if (tabsResult.length > 1) {
    tabsResult[1].addEventListener('click', () => switchResultTab('screen-result1'));
  }
  const tabsResult1 = document.querySelectorAll('#screen-result1 .tab-btn');
  if (tabsResult1.length > 0) {
    tabsResult1[0].addEventListener('click', () => switchResultTab('screen-result'));
  }

  // ==========================================
  // 4. HIỆU ỨNG ĐỔI MÀU NÚT TAB CHUNG
  // ==========================================
  const allTabs = document.querySelectorAll('.tab-btn, .m-tab');
  allTabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      const parentGroup = e.target.parentElement; 
      const siblings = parentGroup.querySelectorAll('.tab-btn, .m-tab');
      siblings.forEach(t => { 
        if(t.classList.contains('tab-btn')) t.className = 'tab-btn inactive';
        if(t.classList.contains('m-tab')) t.className = 'm-tab inactive';
      });
      if(tab.classList.contains('tab-btn')) tab.className = 'tab-btn active';
      if(tab.classList.contains('m-tab')) tab.className = 'm-tab active';
    });
  });

  // ==========================================
  // 5. SUCCESS SCREEN (Đánh giá sao & Về bờ)
  // ==========================================
  const stars = document.querySelectorAll('#screen-success .star');
  const ratingText = document.getElementById('rating-text');
  const ratingMessages = ["Rất tệ", "Tệ", "Bình thường", "Tốt", "Tuyệt vời! Cảm ơn bạn"];
  
  stars.forEach((star, index) => {
    star.addEventListener('click', () => {
      ratingText.innerText = ratingMessages[index];
      ratingText.style.color = index >= 3 ? '#00C853' : '#FF5A1F';
      stars.forEach((s, i) => {
        if (i <= index) s.classList.add('filled');
        else s.classList.remove('filled');
      });
    });
  });

  const homeBtn = document.querySelector('#screen-success .btn-home');
  if (homeBtn) {
    homeBtn.addEventListener('click', () => {
      switchScreen('screen-loading');
      setTimeout(() => switchScreen('screen-result'), 4500); 
    });
  }

  // ==========================================
  // 6. TRACKING SCREEN (Bản đồ Shipper)
  // ==========================================
  const oldOrderBtn = document.querySelector('#screen-detail .btn-primary');
  if (oldOrderBtn) {
    // Clone node để dọn dẹp các event click cũ bị trùng lặp
    const newOrderBtn = oldOrderBtn.cloneNode(true);
    oldOrderBtn.parentNode.replaceChild(newOrderBtn, oldOrderBtn);
    
    newOrderBtn.addEventListener('click', () => {
      switchScreen('screen-tracking');
      // Sau 5s tự nhảy sang báo thành công
      setTimeout(() => {
        if(document.getElementById('screen-tracking').style.display === 'flex') {
          switchScreen('screen-success');
        }
      }, 5000);
    });
  }

  const backTracking = document.getElementById('btn-back-tracking');
  if (backTracking) {
    backTracking.addEventListener('click', () => switchScreen('screen-detail'));
  }

  const shipperMarker = document.getElementById('shipper-btn');
  if (shipperMarker) {
    shipperMarker.style.cursor = 'pointer';
    shipperMarker.addEventListener('click', () => switchScreen('screen-success'));
  }

  // ==========================================
  // 7. BOTTOM NAV (Thanh điều hướng dưới)
  // ==========================================
  const allBottomNavs = document.querySelectorAll('.bottom-nav');
  allBottomNavs.forEach(nav => {
    const items = nav.querySelectorAll('.nav-item');
    if (items.length >= 4) {
      items[0].addEventListener('click', () => switchScreen('screen-result'));   // Tab Home
      items[2].addEventListener('click', () => switchScreen('screen-mealplan')); // Tab Lịch trình
      items[3].addEventListener('click', () => switchScreen('screen-discover')); // Tab Khám phá
    }
  });

  // ==========================================
  // 8. CÁC NÚT ĐẶC BIỆT KHÁC
  // ==========================================
  
  // Nút đặt món bên Meal Plan
  document.querySelectorAll('#screen-mealplan .btn-order').forEach(orderBtn => {
    orderBtn.addEventListener('click', () => switchScreen('screen-detail'));
  });

</script>
</body>
</html>
"""

# Render ra giao diện Streamlit
components.html(html_code, height=950, scrolling=False)
