import streamlit as st
import streamlit.components.v1 as components
import sys as _sys, os as _os, json as _json
import pandas as _pd
from pathlib import Path as _Path

# --- Thiết lập đường dẫn backend ---
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / 'mybackhurt'))
_os.chdir(str(_Path(__file__).resolve().parent.parent / 'mybackhurt'))
from fuzzylogic import load_data, get_recommendations, generate_daily_plan

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
    position: absolute; inset: 0; z-index: 50; background: #f5f3ef;
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
  #screen-loading .progress-fill { height: 100%; border-radius: 99px; width: 0%; }
  #screen-loading .fill-orange { background: #FF5A1F; } #screen-loading .fill-yellow { background: #F59E0B; }

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
  .meal-type-badge { position: absolute; top: 16px; left: 16px; padding: 6px 14px; border-radius: 20px; font-family: 'Sora', sans-serif; font-size: 10px; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; color: #fff; z-index: 2; }
  .mtype-snack { background: #F59E0B; } .mtype-fast-food { background: #EF4444; } .mtype-full-meal { background: #3B82F6; } .mtype-healthy-meal { background: #22C55E; }
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
  #screen-result1 .scroll-content { padding-bottom: 210px; }
  #screen-result1 .floating-order-box { bottom: 86px; }
  #screen-result1 .needs-card { bottom: 168px; }
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
  .favorite-btn { transition: background 0.2s, transform 0.2s; }
  .favorite-btn:active { transform: scale(0.94); }
  .favorite-btn.is-favorite { background: rgba(255, 90, 31, 0.95); border-color: rgba(255,255,255,0.35); }
  .favorite-btn.is-favorite svg { fill: #fff; stroke: #fff; }
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
  .ai-banner:active { transform: scale(0.98); }
  .ai-banner-left { display: flex; align-items: center; gap: 12px; }
  .ai-icon-wrap { width: 32px; height: 32px; background: #fff0eb; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #FF5A1F; }
  .ai-banner-text { font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; color: #1a1a1a; }
  .ai-insight-panel { display: none; position: absolute; inset: 0; z-index: 70; background: rgba(26,26,26,0.36); align-items: flex-end; padding: 0 18px 26px; }
  .ai-insight-panel.is-open { display: flex; animation: fadeIn 0.2s ease forwards; }
  .ai-insight-sheet { width: 100%; background: #fff; border-radius: 28px; padding: 20px; box-shadow: 0 -14px 38px rgba(0,0,0,0.18); animation: sheetUp 0.24s ease forwards; }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes sheetUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
  .ai-insight-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 14px; }
  .ai-insight-title { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #1a1a1a; line-height: 1.25; }
  .ai-insight-close { width: 34px; height: 34px; border-radius: 12px; border: none; background: #f5f3ef; color: #555; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; }
  .ai-insight-subtitle { font-size: 13px; color: #777; font-weight: 600; line-height: 1.45; margin-bottom: 16px; }
  .ai-reason-list { display: flex; flex-direction: column; gap: 10px; }
  .ai-reason-item { display: flex; gap: 12px; align-items: flex-start; background: #fafaf8; border: 1px solid #f0ede8; border-radius: 18px; padding: 12px; }
  .ai-reason-icon { width: 34px; height: 34px; border-radius: 12px; background: #fff0eb; color: #FF5A1F; display: flex; align-items: center; justify-content: center; font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 800; flex-shrink: 0; }
  .ai-reason-text { flex: 1; min-width: 0; }
  .ai-reason-title { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 800; color: #1a1a1a; margin-bottom: 3px; }
  .ai-reason-desc { font-size: 12px; line-height: 1.45; color: #777; font-weight: 600; }
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
  .quick-cart-bar { width: 100%; background: #1a1a1a; color: #fff; border-radius: 24px; padding: 12px 14px; display: flex; align-items: center; gap: 14px; box-shadow: 0 12px 28px rgba(0,0,0,0.22); }
  .cart-icon-wrap { width: 46px; height: 46px; border-radius: 16px; background: rgba(255,255,255,0.12); display: flex; align-items: center; justify-content: center; position: relative; flex-shrink: 0; cursor: pointer; transition: transform 0.2s, background 0.2s; border: none; color: #fff; }
  .cart-icon-wrap:active { transform: scale(0.94); }
  .cart-icon-wrap.is-active { background: rgba(255,90,31,0.34); }
  .cart-count { position: absolute; top: -5px; right: -5px; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 999px; background: #FF5A1F; color: #fff; font-family: 'Sora', sans-serif; font-size: 10px; font-weight: 800; display: flex; align-items: center; justify-content: center; border: 2px solid #1a1a1a; }
  .cart-summary { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
  .cart-label { font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.6); }
  .cart-total { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #fff; }
  .order-now-btn { border: none; background: #FF5A1F; color: #fff; border-radius: 18px; padding: 14px 18px; font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 800; cursor: pointer; box-shadow: 0 8px 20px rgba(255, 90, 31, 0.35); transition: transform 0.2s; white-space: nowrap; }
  .cart-panel { display: none; position: absolute; left: 0; right: 0; bottom: 82px; background: #fff; color: #1a1a1a; border: 1px solid #f0ede8; border-radius: 24px; padding: 16px; box-shadow: 0 18px 38px rgba(0,0,0,0.18); max-height: 315px; overflow: hidden; }
  .cart-panel.is-open { display: block; animation: cartPanelIn 0.22s ease forwards; }
  @keyframes cartPanelIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  .cart-panel-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
  .cart-panel-title { font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 800; color: #1a1a1a; }
  .cart-panel-close { width: 32px; height: 32px; border-radius: 12px; border: none; background: #f5f3ef; color: #555; display: flex; align-items: center; justify-content: center; cursor: pointer; }
  .cart-items { display: flex; flex-direction: column; gap: 10px; max-height: 218px; overflow-y: auto; padding-right: 2px; scrollbar-width: none; }
  .cart-items::-webkit-scrollbar { display: none; }
  .cart-empty { background: #fafaf8; border-radius: 18px; padding: 18px; text-align: center; color: #888; font-size: 13px; font-weight: 700; }
  .cart-item { display: flex; align-items: center; gap: 12px; background: #fafaf8; border-radius: 18px; padding: 12px; }
  .cart-item-info { flex: 1; min-width: 0; }
  .cart-item-name { font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 800; color: #1a1a1a; line-height: 1.3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .cart-item-price { margin-top: 4px; font-size: 12px; color: #888; font-weight: 700; }
  .qty-control { display: flex; align-items: center; gap: 7px; background: #fff; border: 1px solid #eee9e2; border-radius: 14px; padding: 4px; }
  .qty-btn { width: 26px; height: 26px; border-radius: 10px; border: none; background: #1a1a1a; color: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer; font-family: 'Sora', sans-serif; font-weight: 800; }
  .qty-val { min-width: 18px; text-align: center; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 800; color: #1a1a1a; }
  .remove-cart-item { width: 32px; height: 32px; border-radius: 12px; border: none; background: #fff0eb; color: #FF5A1F; display: flex; align-items: center; justify-content: center; cursor: pointer; }
  .order-now-btn:active { transform: scale(0.96); }
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
  #screen-tracking .timeline-wrap::after { content: ''; position: absolute; top: 15px; left: 20px; width: var(--tracking-progress, 0%); height: 2px; background: #00C853; z-index: 1; transition: width 0.45s ease; }
  #screen-tracking .step { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; gap: 10px; width: 50px; }
  #screen-tracking .step-icon { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: #f0f0f0; color: #fff; transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease; }
  #screen-tracking .step.is-done .step-icon, #screen-tracking .step.is-current .step-icon { background: #00C853; }
  #screen-tracking .step.is-current .step-icon { box-shadow: 0 0 0 6px #E8F5E9; transform: scale(1.04); }
  #screen-tracking .step-icon .dot { width: 8px; height: 8px; background: #ccc; border-radius: 50%; }
  #screen-tracking .step.is-current .step-icon .dot { background: #fff; }
  #screen-tracking .step-label { font-size: 10px; font-weight: 800; color: #1a1a1a; text-align: center; line-height: 1.3; }
  #screen-tracking .step:not(.is-done):not(.is-current) .step-label { color: #999; font-weight: 700; }
  #screen-tracking .status-text { text-align: center; font-family: 'Sora', sans-serif; font-weight: 800; font-size: 16px; color: #FF5A1F; }
  #screen-mealplan { background: #fdfdfc; z-index: 50; padding-bottom: 0; }
  #screen-mealplan .scroll-content { padding-top: 70px; padding-bottom: 120px; }
  #screen-mealplan .header-section { padding: 20px 24px; margin-bottom: 10px; }
  #screen-mealplan .label-wrap { display: flex; align-items: center; gap: 8px; color: #FF5A1F; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; }
  #screen-mealplan .main-title { font-family: 'Sora', sans-serif; font-size: 34px; font-weight: 800; color: #1a1a1a; line-height: 1.15; letter-spacing: -1px; margin-bottom: 8px; }
  #screen-mealplan .sub-title { font-size: 16px; font-weight: 700; color: #999; }
  #screen-mealplan .meal-list { padding: 0 24px; display: flex; flex-direction: column; gap: 18px; margin-bottom: 24px; }
  #screen-mealplan .meal-card { min-height: 112px; background: #fff; border-radius: 24px; padding: 22px 20px 22px 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #f0efeb; position: relative; overflow: hidden; }
  #screen-mealplan .meal-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 6px; }
  #screen-mealplan .meal-card.breakfast::before { background: #FFD600; }
  #screen-mealplan .meal-card.lunch::before { background: #FF5A1F; }
  #screen-mealplan .meal-card.dinner::before { background: #00C853; }
  #screen-mealplan .meal-info { display: flex; flex-direction: column; gap: 6px; }
  #screen-mealplan .meal-time { font-size: 11px; font-weight: 800; color: #aaa; text-transform: uppercase; letter-spacing: 0.5px; }
  #screen-mealplan .meal-name { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #1a1a1a; }
  #screen-mealplan .meal-cals { font-size: 13px; font-weight: 700; color: #aaa; display: flex; align-items: center; gap: 4px; }
  #screen-mealplan .meal-actions { display: flex; align-items: center; justify-content: center; min-width: 78px; margin-left: 14px; }
  #screen-mealplan .btn-order { background: #1a1a1a; color: #fff; border: none; border-radius: 18px; padding: 12px 18px; font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 800; cursor: pointer; white-space: nowrap; box-shadow: 0 10px 22px rgba(0,0,0,0.12); }
  #screen-mealplan .btn-swap { background: #f5f3ef; border: 1px solid #e0ded8; border-radius: 16px; padding: 10px 12px; font-size: 14px; cursor: pointer; transition: transform 0.15s; }
  #screen-mealplan .btn-swap:active { transform: scale(0.9); }
  #screen-mealplan .check-icon { width: 44px; height: 44px; background: #00C853; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 22px rgba(0, 200, 83, 0.24); }
  #screen-mealplan .nutrition-card { margin: 0 24px; background: #fff; border-radius: 32px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #f4f3ef; }
  #screen-mealplan .nutrition-header { display: flex; align-items: center; gap: 10px; margin-bottom: 24px; }
  #screen-mealplan .nutrition-title { font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 800; color: #1a1a1a; }
  #screen-mealplan .nutrient-item { margin-bottom: 20px; }
  #screen-mealplan .nutrient-item:last-child { margin-bottom: 0; }
  #screen-mealplan .nutrient-labels { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px; }
  #screen-mealplan .nutrient-name { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 800; color: #1a1a1a; }
  #screen-mealplan .nutrient-val { font-size: 13px; font-weight: 700; color: #999; }
  #screen-mealplan .progress-bg { width: 100%; height: 8px; background: #f0ede8; border-radius: 10px; overflow: hidden; }
  #screen-mealplan .progress-fill { height: 100%; border-radius: 10px; width: 0%; transition: width 0.65s cubic-bezier(0.22, 0.61, 0.36, 1); }
  #screen-mealplan .fill-orange { background: #FF5A1F; }
  #screen-mealplan .fill-blue { background: #2962FF; }
  #screen-mealplan .fill-green { background: #00C853; }
  #screen-mealplan .mealplan-cart-box { display: none; bottom: 86px; }
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
  #screen-discover .favorite-empty { margin: 0 24px; background: #fff; border: 1px dashed #e8e6e0; border-radius: 20px; padding: 18px; color: #888; font-size: 13px; font-weight: 700; text-align: center; }
  #screen-discover .chevron-icon { color: #ccc; margin-right: 8px; }
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
        <div class="progress-meta"><span class="progress-label" id="hunger-progress-label">Độ đói (50%)</span><span class="progress-value" id="hunger-progress-value">Cao</span></div>
        <div class="progress-track"><div class="progress-fill fill-orange bar-hunger" style="width:0%"></div></div>
      </div>
      <div class="progress-row">
        <div class="progress-meta"><span class="progress-label" id="budget-progress-label">Budget (30k – 50k)</span><span class="progress-value" id="budget-progress-value">Hợp lý</span></div>
        <div class="progress-track"><div class="progress-fill fill-yellow bar-budget" style="width:0%"></div></div>
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
          <div class="meal-type-badge mtype-full-meal">Full meal</div>
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
        <div class="needs-item"><div class="needs-item-label">Độ đói</div><div class="needs-item-val needs-hunger-val">Rất đói 😫</div></div>
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

    <div class="menu-list" id="singles-menu-list"></div>

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
        <div class="needs-item-val needs-hunger-val">Rất đói 😫</div>
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

  <div class="floating-order-box">
    <div class="cart-panel" id="singles-cart-panel">
      <div class="cart-panel-head">
        <div class="cart-panel-title">Giỏ hàng của bạn</div>
        <button class="cart-panel-close" aria-label="Đóng giỏ hàng">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="cart-items">
        <div class="cart-empty">Chưa có món nào trong giỏ</div>
      </div>
    </div>
    <div class="quick-cart-bar">
      <button class="cart-icon-wrap" type="button" aria-label="Mở giỏ hàng">
        <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h8.7a2 2 0 0 0 2-1.6L23 6H6"></path>
        </svg>
        <span class="cart-count">0</span>
      </button>
      <div class="cart-summary">
        <span class="cart-label">Tổng cộng</span>
        <span class="cart-total">0 đ</span>
      </div>
      <button class="order-now-btn">Đặt ngay</button>
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
        <div class="circle-btn detail-back-btn" title="Quay lại">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </div>
        <div class="circle-btn favorite-btn" title="Thêm vào yêu thích">
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
    <div class="menu-list" id="detail-menu-list"></div>
  </div>

  <div class="ai-insight-panel" id="ai-insight-panel">
    <div class="ai-insight-sheet">
      <div class="ai-insight-head">
        <div class="ai-insight-title">Vì sao AI chọn quán này?</div>
        <button class="ai-insight-close" type="button" aria-label="Đóng giải thích AI">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="ai-insight-subtitle"></div>
      <div class="ai-reason-list"></div>
    </div>
  </div>

  <!-- Cố định nút ở dưới cùng màn hình -->
  <div class="floating-order-box">
    <div class="cart-panel" id="detail-cart-panel">
      <div class="cart-panel-head">
        <div class="cart-panel-title">Giỏ hàng của bạn</div>
        <button class="cart-panel-close" aria-label="Đóng giỏ hàng">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="cart-items">
        <div class="cart-empty">Chưa có món nào trong giỏ</div>
      </div>
    </div>
    <div class="quick-cart-bar">
      <button class="cart-icon-wrap" type="button" aria-label="Mở giỏ hàng">
        <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h8.7a2 2 0 0 0 2-1.6L23 6H6"></path>
        </svg>
        <span class="cart-count">0</span>
      </button>
      <div class="cart-summary">
        <span class="cart-label">Tổng cộng</span>
        <span class="cart-total">0 đ</span>
      </div>
      <button class="order-now-btn">Đặt ngay</button>
    </div>
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
        <div class="step-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
        <div class="step-label">Đang giao</div>
      </div>
      <div class="step">
        <div class="step-icon"><div class="dot"></div></div>
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
      <div class="meal-card breakfast" data-meal-id="breakfast">
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
        <div class="meal-actions">
          <button class="btn-order" data-meal-id="breakfast">Đặt món</button>
        </div>
      </div>

      <div class="meal-card lunch" data-meal-id="lunch">
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
        <div class="meal-actions">
          <button class="btn-order btn-order-lunch" data-meal-id="lunch">Đặt món</button>
        </div>
      </div>

      <div class="meal-card dinner" data-meal-id="dinner">
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
        <div class="meal-actions">
          <button class="btn-order btn-order-dinner" data-meal-id="dinner">Đặt món</button>
        </div>
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
          <span class="nutrient-val" data-nutrient="calories">0 / 1800 kcal</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-orange"></div></div>
      </div>

      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Protein</span>
          <span class="nutrient-val" data-nutrient="protein">0 / 120g</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-blue"></div></div>
      </div>

      <div class="nutrient-item">
        <div class="nutrient-labels">
          <span class="nutrient-name">Carbs</span>
          <span class="nutrient-val" data-nutrient="carbs">0 / 250g</span>
        </div>
        <div class="progress-bg"><div class="progress-fill fill-green"></div></div>
      </div>

    </div>

  </div>

  <div class="floating-order-box mealplan-cart-box">
    <div class="quick-cart-bar">
      <div class="cart-icon-wrap">
        <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h8.7a2 2 0 0 0 2-1.6L23 6H6"></path>
        </svg>
        <span class="cart-count">1</span>
      </div>
      <div class="cart-summary">
        <span class="cart-label">Tổng cộng</span>
        <span class="cart-total">0 đ</span>
      </div>
      <button class="order-now-btn">Đặt ngay</button>
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
          <img src="https://images.unsplash.com/photo-1553621042-f6e147245754?auto=format&fit=crop&w=300&q=80" alt="Sushi Haru" class="trend-img">
          <div class="rating-badge"><span style="color:#FFD600">★</span> 4.8</div>
        </div>
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
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
        Danh sách yêu thích
      </div>
    </div>

    <div class="recent-list favorite-list">
      <div class="favorite-empty">Bấm tim ở trang quán ăn để lưu vào danh sách yêu thích</div>
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
  let loadingTimer = null;

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
    if (targetId === 'screen-mealplan') {
      setTimeout(function() { populateMealPlanScreen(); }, 150);
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
  loadingTimer = setTimeout(() => {
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
  let cartItems = [];
  let activeCartPanelId = null;
  let activeOrderContext = 'detail';
  let pendingMealId = null;
  let selectedMealId = null;
  let trackingTimerIds = [];
  const favoriteRestaurants = new Set();
  const mealPlanNutrition = { calories: 0, protein: 0, carbs: 0 };
  const orderedMealIds = new Set();
  const mealPlanMeals = {
    breakfast: { name: 'Đang tải...', price: 0, calories: 0, protein: 0, carbs: 0, fat: 0 },
    lunch: { name: 'Đang tải...', price: 0, calories: 0, protein: 0, carbs: 0, fat: 0 },
    dinner: { name: 'Đang tải...', price: 0, calories: 0, protein: 0, carbs: 0, fat: 0 }
  };
  const todayRecommendedMealPlan = {
    breakfast: { name: 'Bánh mì ốp la', calories: 450, protein: 22, carbs: 48, fat: 18, price: 30000, meal_type: 'Full meal' },
    lunch: { name: 'Cơm tấm sườn bì', calories: 450, protein: 28, carbs: 54, fat: 14, price: 45000, meal_type: 'Full meal' },
    dinner: { name: 'Salad ức gà', calories: 450, protein: 35, carbs: 30, fat: 16, price: 42000, meal_type: 'Healthy meal' }
  };

  function populateMealPlanScreen() {
    ['breakfast', 'lunch', 'dinner'].forEach(function(mealId) {
      var card = document.querySelector('#screen-mealplan .meal-card[data-meal-id="' + mealId + '"]');
      if (!card) return;
      var backendData = window.foodmindMealPlan ? window.foodmindMealPlan[mealId] : {};
      var planData = Object.assign({}, backendData || {}, todayRecommendedMealPlan[mealId]);
      if (!planData) { card.style.display = 'none'; return; }
      card.style.display = '';
      var nameEl = card.querySelector('.meal-name');
      var calsEl = card.querySelector('.meal-cals');
      if (nameEl) nameEl.textContent = planData.name;
      if (calsEl) calsEl.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"></path></svg> ' + planData.calories + ' kcal';
      mealPlanMeals[mealId] = planData;
    });
    renderMealPlanNutrition();
  }

  function swapMealPlanItem(mealId) {
    if (!window.foodmindMealAlternatives) return;
    var alts = window.foodmindMealAlternatives[mealId] || [];
    if (!alts.length) return;
    var pick = alts[Math.floor(Math.random() * alts.length)];
    mealPlanMeals[mealId] = pick;
    var card = document.querySelector('#screen-mealplan .meal-card[data-meal-id="' + mealId + '"]');
    if (card) {
      var nameEl = card.querySelector('.meal-name');
      var calsEl = card.querySelector('.meal-cals');
      if (nameEl) nameEl.textContent = pick.name;
      if (calsEl) calsEl.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"></path></svg> ' + pick.calories + ' kcal';
    }
    renderMealPlanNutrition();
  }

  function getCurrentScreenId() {
    const visibleScreen = document.querySelector('.screen-wrapper[style*="display: flex"]');
    return visibleScreen ? visibleScreen.id : 'screen-result';
  }

  function openRestaurantDetail(name, returnScreen) {
    if (!restaurantDetails[name] && window.foodmindAllRecalculated) {
      var dishForRst = window.foodmindAllRecalculated.find(function(dr) {
        return dr.restaurant_name === name;
      });
      if (dishForRst) {
        restaurantDetails[name] = backendResultToDetail(dishForRst, 0);
      }
    }

    var firstKey = Object.keys(restaurantDetails)[0];
    const detail = restaurantDetails[name] || (firstKey ? restaurantDetails[firstKey] : {});
    const detailTitle = document.querySelector('#screen-detail .hero-title');
    const detailMatch = document.querySelector('#screen-detail .match-box-val');
    const detailBg = document.querySelector('#screen-detail .hero-bg');

    detailReturnScreen = returnScreen || getCurrentScreenId();

    if (detailTitle) detailTitle.innerHTML = detail.title;
    if (detailMatch) detailMatch.textContent = detail.match;
    if (detailBg) detailBg.style.setProperty('--hero-image', detail.image);
    selectedRestaurantName = detail.name;
    updateFavoriteButton();
    closeAiInsight();
    resetQuickCart();
    populateDetailMenu(detail.name);

    switchScreen('screen-detail');
  }

  function formatVnd(amount) {
    return amount.toLocaleString('vi-VN') + ' đ';
  }

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, char => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[char]);
  }

  function getCartTotals() {
    return cartItems.reduce((totals, item) => {
      totals.count += item.quantity;
      totals.amount += item.price * item.quantity;
      return totals;
    }, { count: 0, amount: 0 });
  }

  function updateQuickCart() {
    const totals = getCartTotals();
    const cartHtml = cartItems.length
      ? cartItems.map(item => `
        <div class="cart-item" data-cart-id="${escapeHtml(item.id)}">
          <div class="cart-item-info">
            <div class="cart-item-name">${escapeHtml(item.name)}</div>
            <div class="cart-item-price">${formatVnd(item.price)}</div>
          </div>
          <div class="qty-control" aria-label="Chỉnh số lượng ${escapeHtml(item.name)}">
            <button class="qty-btn cart-qty-minus" type="button" aria-label="Giảm số lượng">−</button>
            <span class="qty-val">${item.quantity}</span>
            <button class="qty-btn cart-qty-plus" type="button" aria-label="Tăng số lượng">+</button>
          </div>
          <button class="remove-cart-item" type="button" aria-label="Xoá ${escapeHtml(item.name)}">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
            </svg>
          </button>
        </div>
      `).join('')
      : '<div class="cart-empty">Chưa có món nào trong giỏ</div>';

    document.querySelectorAll('#screen-detail, #screen-result1').forEach(screen => {
      const countEl = screen.querySelector('.cart-count');
      const totalEl = screen.querySelector('.cart-total');
      const cartIcon = screen.querySelector('.cart-icon-wrap');
      const cartPanel = screen.querySelector('.cart-panel');
      const cartItemsEl = screen.querySelector('.cart-items');
      const orderBtn = screen.querySelector('.order-now-btn');
      const isOpen = Boolean(cartPanel && cartPanel.id === activeCartPanelId);

      if (countEl) countEl.textContent = totals.count;
      if (totalEl) totalEl.textContent = formatVnd(totals.amount);
      if (orderBtn) orderBtn.disabled = totals.count === 0;
      if (cartIcon) {
        cartIcon.classList.toggle('is-active', isOpen);
        cartIcon.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }
      if (cartPanel) cartPanel.classList.toggle('is-open', isOpen);
      if (cartItemsEl) cartItemsEl.innerHTML = cartHtml;
    });
  }

  function resetQuickCart() {
    cartItems = [];
    activeCartPanelId = null;
    updateQuickCart();
  }

  function addMenuItemToCart(menuItem) {
    if (!menuItem) return;
    const name = menuItem.querySelector('.menu-name')?.textContent?.trim() || 'Món ăn';
    const price = parseMenuPrice(menuItem.querySelector('.menu-price')?.textContent);
    const id = name.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-');
    const existingItem = cartItems.find(item => item.id === id);

    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cartItems.push({ id, name, price, quantity: 1 });
    }
    updateQuickCart();
  }

  function changeCartItemQuantity(itemId, delta) {
    const item = cartItems.find(cartItem => cartItem.id === itemId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
      cartItems = cartItems.filter(cartItem => cartItem.id !== itemId);
    }
    if (!cartItems.length) activeCartPanelId = null;
    updateQuickCart();
  }

  function removeCartItem(itemId) {
    cartItems = cartItems.filter(item => item.id !== itemId);
    if (!cartItems.length) activeCartPanelId = null;
    updateQuickCart();
  }

  function parseMenuPrice(priceText) {
    const digits = (priceText || '').replace(/[^0-9]/g, '');
    return digits ? Number(digits) : 0;
  }

  function getRestaurantImageUrl(detail) {
    const match = (detail?.image || '').match(/url\\(['"]?([^'")]+)['"]?\\)/);
    return match ? match[1] : 'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=150&q=80';
  }

  function updateFavoriteButton() {
    const favoriteBtn = document.querySelector('#screen-detail .favorite-btn');
    if (!favoriteBtn) return;

    const isFavorite = favoriteRestaurants.has(selectedRestaurantName);
    favoriteBtn.classList.toggle('is-favorite', isFavorite);
    favoriteBtn.setAttribute('title', isFavorite ? 'Bỏ khỏi yêu thích' : 'Thêm vào yêu thích');
  }

  function renderFavoriteRestaurants() {
    const favoriteList = document.querySelector('#screen-discover .favorite-list');
    if (!favoriteList) return;

    const favoriteItems = Array.from(favoriteRestaurants)
      .map(name => restaurantDetails[name])
      .filter(Boolean);

    if (!favoriteItems.length) {
      favoriteList.innerHTML = '<div class="favorite-empty">Bấm tim ở trang quán ăn để lưu vào danh sách yêu thích</div>';
      return;
    }

    favoriteList.innerHTML = favoriteItems.map(detail => `
      <div class="recent-item" data-restaurant="${escapeHtml(detail.name)}">
        <img src="${escapeHtml(getRestaurantImageUrl(detail))}" alt="${escapeHtml(detail.name)}" class="recent-img">
        <div class="recent-info">
          <div class="recent-name">${escapeHtml(detail.name)}</div>
          <div class="recent-desc">${escapeHtml(detail.price)} • ${escapeHtml(detail.distance.split('•')[0].trim())}</div>
        </div>
        <svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>
    `).join('');
  }

  function renderAiInsight() {
    var firstKey = Object.keys(restaurantDetails)[0];
    const detail = restaurantDetails[selectedRestaurantName] || (firstKey ? restaurantDetails[firstKey] : {});
    const subtitle = document.querySelector('#screen-detail .ai-insight-subtitle');
    const reasonList = document.querySelector('#screen-detail .ai-reason-list');
    if (!subtitle || !reasonList) return;

    subtitle.textContent = detail.name + ' đạt ' + detail.matchText + ' vì khớp tốt với nhu cầu hiện tại của bạn.';
    reasonList.innerHTML = [
      {
        icon: detail.match,
        title: 'Độ phù hợp cao',
        desc: detail.tag.replace('PHÙ HỢP ', 'AI chấm ').toLowerCase() + ', dựa trên ngân sách, khẩu vị và mức độ đói.'
      },
      {
        icon: '⏱',
        title: 'Giao trong khung hợp lý',
        desc: detail.distance + ', phù hợp khi bạn ưu tiên ăn nhanh và ít chờ.'
      },
      {
        icon: '₫',
        title: 'Mức giá vừa với lựa chọn',
        desc: 'Khoảng giá ' + detail.price + ' nằm trong vùng ngân sách đang được hệ thống ưu tiên.'
      },
      {
        icon: '★',
        title: 'Chất lượng ổn định',
        desc: 'Điểm đánh giá ' + detail.rating + ' giúp AI tự tin hơn khi đề xuất quán này.'
      }
    ].map(item => `
      <div class="ai-reason-item">
        <div class="ai-reason-icon">${escapeHtml(item.icon)}</div>
        <div class="ai-reason-text">
          <div class="ai-reason-title">${escapeHtml(item.title)}</div>
          <div class="ai-reason-desc">${escapeHtml(item.desc)}</div>
        </div>
      </div>
    `).join('');
  }

  function openAiInsight() {
    renderAiInsight();
    const panel = document.getElementById('ai-insight-panel');
    if (panel) panel.classList.add('is-open');
  }

  function closeAiInsight() {
    const panel = document.getElementById('ai-insight-panel');
    if (panel) panel.classList.remove('is-open');
  }

  function updateMealPlanCart(mealId) {
    const meal = mealPlanMeals[mealId];
    const cartBox = document.querySelector('#screen-mealplan .mealplan-cart-box');
    if (!cartBox || !meal) return;

    cartBox.style.display = 'block';
    const countEl = cartBox.querySelector('.cart-count');
    const totalEl = cartBox.querySelector('.cart-total');
    if (countEl) countEl.textContent = '1';
    if (totalEl) totalEl.textContent = formatVnd(meal.price);
  }

  const trackingSteps = [
    { progress: 0, status: 'Đơn hàng đã được xác nhận', eta: '12 phút nữa' },
    { progress: 25, status: 'Quán đang chuẩn bị món', eta: '9 phút nữa' },
    { progress: 50, status: 'Shipper đã nhận đơn', eta: '6 phút nữa' },
    { progress: 75, status: 'Shipper đang trên đường', eta: '3 phút nữa' },
    { progress: 100, status: 'Đơn hàng đã giao', eta: 'Đã giao' }
  ];
  const trackingCheckIcon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
  const trackingDotIcon = '<div class="dot"></div>';

  function clearTrackingTimers() {
    trackingTimerIds.forEach(function(timerId) { clearTimeout(timerId); });
    trackingTimerIds = [];
  }

  function updateTrackingTimeline(activeIndex) {
    const screen = document.getElementById('screen-tracking');
    if (!screen) return;
    const timeline = screen.querySelector('.timeline-wrap');
    const steps = Array.from(screen.querySelectorAll('.timeline-wrap .step'));
    const statusText = screen.querySelector('.status-text');
    const etaTime = screen.querySelector('.eta-time');
    const current = trackingSteps[Math.min(activeIndex, trackingSteps.length - 1)];

    if (timeline) timeline.style.setProperty('--tracking-progress', current.progress + '%');
    if (statusText) statusText.textContent = current.status;
    if (etaTime) etaTime.textContent = current.eta;

    steps.forEach(function(step, index) {
      const icon = step.querySelector('.step-icon');
      step.classList.remove('is-done', 'is-current');
      if (index < activeIndex) {
        step.classList.add('is-done');
        if (icon) icon.innerHTML = trackingCheckIcon;
      } else if (index === activeIndex) {
        step.classList.add('is-current');
        if (icon) icon.innerHTML = index === trackingSteps.length - 1 ? trackingCheckIcon : trackingDotIcon;
      } else if (icon) {
        icon.innerHTML = trackingDotIcon;
      }
    });
  }

  function finishTrackingOrder() {
    clearTrackingTimers();
    updateTrackingTimeline(trackingSteps.length - 1);
    completeCurrentOrder();
    switchScreen('screen-success');
  }

  function startTrackingTimeline() {
    clearTrackingTimers();
    updateTrackingTimeline(0);
    trackingSteps.slice(1).forEach(function(_, index) {
      const stepIndex = index + 1;
      const timerId = setTimeout(function() {
        updateTrackingTimeline(stepIndex);
        if (stepIndex === trackingSteps.length - 1) {
          const finishTimer = setTimeout(finishTrackingOrder, 650);
          trackingTimerIds.push(finishTimer);
        }
      }, stepIndex * 1400);
      trackingTimerIds.push(timerId);
    });
  }

  function startDeliveryTracking() {
    window.parent.postMessage({type:'foodmind-show-tracking'}, '*');
    switchScreen('screen-tracking');
    setTimeout(startTrackingTimeline, 120);
  }

  function startMealPlanOrder() {
    if (!selectedMealId) return;
    pendingMealId = selectedMealId;
    activeOrderContext = 'mealplan';
    startDeliveryTracking();
  }

  function hideMealPlanCart() {
    const cartBox = document.querySelector('#screen-mealplan .mealplan-cart-box');
    if (cartBox) cartBox.style.display = 'none';
    selectedMealId = null;
  }

  function renderMealPlanNutrition() {
    const calorieVal = document.querySelector('#screen-mealplan [data-nutrient="calories"]');
    const proteinVal = document.querySelector('#screen-mealplan [data-nutrient="protein"]');
    const carbsVal = document.querySelector('#screen-mealplan [data-nutrient="carbs"]');
    const calorieFill = document.querySelector('#screen-mealplan .fill-orange');
    const proteinFill = document.querySelector('#screen-mealplan .fill-blue');
    const carbsFill = document.querySelector('#screen-mealplan .fill-green');
    const targets = window.foodmindMealTargets || { calories: 1800, protein: 120, carbs: 250 };
    const calories = Math.round(Number(mealPlanNutrition.calories) || 0);
    const protein = Math.round(Number(mealPlanNutrition.protein) || 0);
    const carbs = Math.round(Number(mealPlanNutrition.carbs) || 0);

    if (calorieVal) calorieVal.textContent = calories + ' / ' + targets.calories + ' kcal';
    if (proteinVal) proteinVal.textContent = protein + ' / ' + targets.protein + 'g';
    if (carbsVal) carbsVal.textContent = carbs + ' / ' + targets.carbs + 'g';
    if (calorieFill) calorieFill.style.width = Math.min(100, calories / targets.calories * 100) + '%';
    if (proteinFill) proteinFill.style.width = Math.min(100, protein / targets.protein * 100) + '%';
    if (carbsFill) carbsFill.style.width = Math.min(100, carbs / targets.carbs * 100) + '%';
  }

  function markMealPlanOrdered(mealId) {
    const meal = mealPlanMeals[mealId];
    if (!meal || orderedMealIds.has(mealId)) return;

    orderedMealIds.add(mealId);
    mealPlanNutrition.calories += Number(meal.calories) || 0;
    mealPlanNutrition.protein += Number(meal.protein) || 0;
    mealPlanNutrition.carbs += Number(meal.carbs) || 0;
    renderMealPlanNutrition();

    const mealCard = document.querySelector('#screen-mealplan .meal-card[data-meal-id="' + mealId + '"]');
    const oldAction = mealCard ? mealCard.querySelector('.btn-order') : null;
    if (oldAction) {
      oldAction.outerHTML = '<div class="check-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>';
    }
  }

  function completeCurrentOrder() {
    if (activeOrderContext === 'mealplan' && pendingMealId) {
      markMealPlanOrdered(pendingMealId);
      hideMealPlanCart();
      pendingMealId = null;
      activeOrderContext = 'detail';
    }
  }

  function showRestaurantAsMainCard(name, screenSelector) {
    const detail = restaurantDetails[name] || restaurantDetails[Object.keys(restaurantDetails)[0]] || {};
    if (!detail.name) return;
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
    const mealTypeBadge = screen.querySelector('.meal-type-badge');
    const scrollContent = screen.querySelector('.scroll-content');

    if (imageLayer && detail.image) {
      imageLayer.style.background = detail.image + ' center/cover';
    }
    if (matchPct) matchPct.textContent = detail.match || '';
    if (ratingVal) ratingVal.textContent = detail.rating || '';
    if (distance) distance.textContent = detail.distance || '';
    if (foodName) foodName.textContent = detail.name || '';
    if (priceBadge) priceBadge.textContent = detail.price || '';
    if (firstTag) firstTag.textContent = detail.tag || '';
    if (mealTypeBadge && detail.mealType) {
      mealTypeBadge.textContent = detail.mealType;
      mealTypeBadge.className = 'meal-type-badge mtype-' + detail.mealType.toLowerCase().replace(/\\s+/g, '-');
    }
    if (scrollContent) scrollContent.scrollTo({ top: 140, behavior: 'smooth' });
    updateFavoriteButton();
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
  const backBtn = document.querySelector('#screen-detail .detail-back-btn'); 
  if (backBtn) {
    backBtn.addEventListener('click', () => switchScreen(detailReturnScreen || 'screen-result'));
  }

  const favoriteBtn = document.querySelector('#screen-detail .favorite-btn');
  if (favoriteBtn) {
    favoriteBtn.addEventListener('click', event => {
      event.stopPropagation();
      if (favoriteRestaurants.has(selectedRestaurantName)) {
        favoriteRestaurants.delete(selectedRestaurantName);
      } else {
        favoriteRestaurants.add(selectedRestaurantName);
      }
      updateFavoriteButton();
      renderFavoriteRestaurants();
    });
  }

  const aiBanner = document.querySelector('#screen-detail .ai-banner');
  if (aiBanner) {
    aiBanner.addEventListener('click', openAiInsight);
  }

  const aiInsightPanel = document.getElementById('ai-insight-panel');
  if (aiInsightPanel) {
    aiInsightPanel.addEventListener('click', event => {
      if (event.target === aiInsightPanel || event.target.closest('.ai-insight-close')) {
        closeAiInsight();
      }
    });
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
      switchScreen('screen-result');
    });
  }

  // ==========================================
  // 6. TRACKING SCREEN (Bản đồ Shipper)
  // ==========================================
  document.querySelectorAll('#screen-detail .add-btn, #screen-result1 .add-btn').forEach(addBtn => {
    addBtn.addEventListener('click', event => {
      event.stopPropagation();
      addMenuItemToCart(addBtn.closest('.menu-item'));
    });
  });

  document.addEventListener('click', event => {
    const singlesAddBtn = event.target.closest('#screen-result1 .add-btn');
    if (singlesAddBtn) {
      event.stopPropagation();
      addMenuItemToCart(singlesAddBtn.closest('.menu-item'));
      return;
    }

    const detailAddBtn = event.target.closest('#screen-detail .add-btn');
    if (detailAddBtn) {
      event.stopPropagation();
      addMenuItemToCart(detailAddBtn.closest('.menu-item'));
      return;
    }

    const singlesOrderBtn = event.target.closest('#screen-result1 .order-now-btn');
    if (singlesOrderBtn && cartItems.length) {
      event.stopPropagation();
      activeCartPanelId = null;
      updateQuickCart();
      activeOrderContext = 'singles';
      startDeliveryTracking();
    }
  });

  document.querySelectorAll('#screen-detail .cart-icon-wrap, #screen-result1 .cart-icon-wrap').forEach(cartIcon => {
    cartIcon.addEventListener('click', event => {
      event.stopPropagation();
      const cartPanel = cartIcon.closest('.floating-order-box')?.querySelector('.cart-panel');
      if (!cartPanel) return;
      activeCartPanelId = activeCartPanelId === cartPanel.id ? null : cartPanel.id;
      updateQuickCart();
    });
  });

  document.querySelectorAll('#screen-detail .cart-panel-close, #screen-result1 .cart-panel-close').forEach(cartClose => {
    cartClose.addEventListener('click', event => {
      event.stopPropagation();
      activeCartPanelId = null;
      updateQuickCart();
    });
  });

  document.querySelectorAll('#screen-detail .cart-panel, #screen-result1 .cart-panel').forEach(cartPanel => {
    cartPanel.addEventListener('click', event => {
      event.stopPropagation();
      const cartItem = event.target.closest('.cart-item');
      if (!cartItem) return;

      if (event.target.closest('.cart-qty-plus')) {
        changeCartItemQuantity(cartItem.dataset.cartId, 1);
      } else if (event.target.closest('.cart-qty-minus')) {
        changeCartItemQuantity(cartItem.dataset.cartId, -1);
      } else if (event.target.closest('.remove-cart-item')) {
        removeCartItem(cartItem.dataset.cartId);
      }
    });
  });

  document.querySelectorAll('#screen-detail .order-now-btn, #screen-result1 .order-now-btn').forEach(oldOrderBtn => {
    // Clone node để dọn dẹp các event click cũ bị trùng lặp
    const newOrderBtn = oldOrderBtn.cloneNode(true);
    oldOrderBtn.parentNode.replaceChild(newOrderBtn, oldOrderBtn);
    
    newOrderBtn.addEventListener('click', event => {
      event.stopPropagation();
      if (!cartItems.length) return;
      activeCartPanelId = null;
      updateQuickCart();
      activeOrderContext = newOrderBtn.closest('#screen-result1') ? 'singles' : 'detail';
      startDeliveryTracking();
    });
  });

  const backTracking = document.getElementById('btn-back-tracking');
  if (backTracking) {
    backTracking.addEventListener('click', () => {
      const returnScreen = activeOrderContext === 'mealplan'
        ? 'screen-mealplan'
        : activeOrderContext === 'singles'
          ? 'screen-result1'
          : 'screen-detail';
      switchScreen(returnScreen);
    });
  }

  const shipperMarker = document.getElementById('shipper-btn');
  if (shipperMarker) {
    shipperMarker.style.cursor = 'pointer';
    shipperMarker.addEventListener('click', () => {
      finishTrackingOrder();
    });
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
  const mealPlanScreen = document.getElementById('screen-mealplan');
  if (mealPlanScreen) {
    mealPlanScreen.addEventListener('click', event => {
      const orderBtn = event.target.closest('.btn-order');
      if (!orderBtn || !mealPlanScreen.contains(orderBtn)) return;
      const mealId = orderBtn.dataset.mealId;
      if (!mealId || orderedMealIds.has(mealId)) return;
      selectedMealId = mealId;
      updateMealPlanCart(mealId);
    });
  }

  const mealPlanOrderBtn = document.querySelector('#screen-mealplan .mealplan-cart-box .order-now-btn');
  if (mealPlanOrderBtn) {
    mealPlanOrderBtn.addEventListener('click', startMealPlanOrder);
  }

  window.userPrefs = {
    budget: '30_50k',
    time: 'fast',
    hunger: 3.5,
    diet: 'Normal',
    weather: 'Normal',
    cuisine: 'Việt Nam'
  };

  const budgetLabels = {
    'under_30k': 'Dưới 30k',
    '30_50k': '30k - 50k',
    '50_100k': '50k - 100k',
    'over_100k': 'Trên 100k'
  };
  const timeLabels = {
    'express': 'Cực nhanh',
    'fast': 'Nhanh',
    'normal': 'Bình thường',
    'no_rush': 'Không gấp'
  };
  const dietLabels = {
    'Diet': 'Eat clean',
    'Normal': 'Healthy',
    'Bulking': 'High protein'
  };
  const weatherLabels = {
    'Rainy': 'Mưa',
    'Normal': 'Nắng',
    'Cold': 'Lạnh',
    'Hot': 'Nóng'
  };
  const hungerEmojis = {
    'Snack': '🥗', 'Slightly_Hungry': '😋', 'Hungry': '🤤', 'Very_Hungry': '😫'
  };

  function getHungerLabel(val) {
    val = parseFloat(val) || 3.5;
    if (val <= 2.5) return 'Ăn nhẹ 🥗';
    if (val <= 5) return 'Hơi đói 😋';
    if (val <= 7.5) return 'Đói 🤤';
    return 'Rất đói 😫';
  }

  function applyPrefsToUI() {
    var p = window.userPrefs;
    var budgetEls = document.querySelectorAll('.needs-item-val');
    budgetEls.forEach(function(el) {
      var label = el.parentElement.querySelector('.needs-item-label');
      if (!label) return;
      var text = label.textContent.trim().toLowerCase();
      if (text.includes('budget') || text.includes('ngân sách')) {
        el.textContent = budgetLabels[p.budget] || p.budget;
      }
      if (text.includes('đói') || text.includes('doi')) {
        el.textContent = getHungerLabel(p.hunger);
      }
      if (text.includes('giao') || text.includes('time')) {
        el.textContent = timeLabels[p.time] ? timeLabels[p.time] + ' ⚡' : p.time;
      }
      if (text.includes('tiêu') || text.includes('mục') || text.includes('diet')) {
        el.textContent = dietLabels[p.diet] ? dietLabels[p.diet] + ' 🥗' : p.diet;
      }
      if (text.includes('thực') || text.includes('cuisine')) {
        el.textContent = (p.cuisine || 'Việt Nam') + ' 🇻🇳';
      }
      if (text.includes('weather') || text.includes('thời tiết')) {
        var w = weatherLabels[p.weather] || p.weather;
        var wEmoji = p.weather === 'Hot' ? '🔥' : p.weather === 'Cold' ? '🥶' : p.weather === 'Rainy' ? '🌧️' : '☀️';
        el.textContent = w + ' ' + wEmoji;
      }
    });
  }

  function updateLoadingUI() {
    var p = window.userPrefs;
    var hungerVal = parseFloat(p.hunger) || 3.5;
    var hungerPct = Math.round((hungerVal / 10) * 100);
    var hungerLabel = getHungerLabel(hungerVal);

    var hl = document.getElementById('hunger-progress-label');
    var hv = document.getElementById('hunger-progress-value');
    if (hl) hl.textContent = 'Độ đói (' + hungerPct + '%)';
    if (hv) hv.textContent = hungerLabel;

    var budgetLabel = budgetLabels[p.budget] || p.budget;
    var budgetPcts = { 'under_30k': 18, '30_50k': 40, '50_100k': 70, 'over_100k': 95 };
    var budgetPct = budgetPcts[p.budget] || 50;
    var budgetValText = budgetPct > 60 ? 'Cao' : budgetPct > 30 ? 'Hợp lý' : 'Thấp';

    var bl = document.getElementById('budget-progress-label');
    var bv = document.getElementById('budget-progress-value');
    if (bl) bl.textContent = 'Budget (' + budgetLabel + ')';
    if (bv) bv.textContent = budgetValText;
  }

  function readPrefsFromHash() {
    var hash = window.location.hash;
    if (!hash) { updateLoadingUI(); return; }
    try {
      var params = new URLSearchParams(hash.replace(/^#/, ''));
      if (params.get('budget')) window.userPrefs.budget = params.get('budget');
      if (params.get('time')) window.userPrefs.time = params.get('time');
      if (params.get('hunger')) window.userPrefs.hunger = parseFloat(params.get('hunger'));
      if (params.get('diet')) window.userPrefs.diet = params.get('diet');
      if (params.get('weather')) window.userPrefs.weather = params.get('weather');
      if (params.get('cuisine')) window.userPrefs.cuisine = params.get('cuisine');
    } catch(e) {}
    updateLoadingUI();
  }

  window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'foodmind-prefs' && event.data.prefs) {
      var p = event.data.prefs;
      if (p.budget) window.userPrefs.budget = p.budget;
      if (p.time) window.userPrefs.time = p.time;
      if (p.hunger !== undefined) window.userPrefs.hunger = p.hunger;
      if (p.diet) window.userPrefs.diet = p.diet;
      if (p.weather) window.userPrefs.weather = p.weather;
      if (p.cuisine) window.userPrefs.cuisine = p.cuisine;
      updateLoadingUI();
      applyPrefsToUI();
    }
  });

  var mealTypeGradients = {
    'Fast food': 'linear-gradient(135deg,#8b1a1a,#6b0f0f)',
    'Full meal': 'linear-gradient(135deg,#3d2a1a,#6b3d1e)',
    'Healthy meal': 'linear-gradient(135deg,#2e4a1a,#1a380f)',
    'Snack': 'linear-gradient(135deg,#8b6508,#5c4305)'
  };

  function backendResultToDetail(r, index) {
    var mealType = r.meal_type || 'Full meal';
    var gradient = mealTypeGradients[mealType] || 'linear-gradient(135deg,#1a3a4a,#0f2a38)';
    var matchPct = r.match_score.toFixed(0);

    // Look up real restaurant data for rating & location
    var rating = '4.0';
    var distance = '~1.5 km';
    var realImg = r.image_url;
    if (window.foodmindRestaurants && window.foodmindRestaurants.length) {
      var matchedRest = window.foodmindRestaurants.find(function(rst) {
        return rst.restaurant_id === r.restaurant_id || rst.name === r.restaurant_name;
      });
      if (matchedRest) {
        rating = (matchedRest.rating || 4.0).toFixed(1);
        if (matchedRest.cover_image_url) realImg = matchedRest.cover_image_url;
        if (matchedRest.lat && matchedRest.lng) {
          var userLat = window.userPrefs && window.userPrefs._lat ? window.userPrefs._lat : 10.7614;
          var userLng = window.userPrefs && window.userPrefs._lng ? window.userPrefs._lng : 106.6686;
          var dlat = matchedRest.lat - userLat;
          var dlng = matchedRest.lng - userLng;
          var distKm = Math.sqrt(dlat*dlat + dlng*dlng) * 111;
          distance = distKm < 1 ? (distKm * 1000).toFixed(0) + ' m' : distKm.toFixed(1) + ' km';
        }
      }
    }

    var imgUrl = realImg ? 'url(\"' + realImg + '\")' : 'url(\"data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22390%22 height=%22280%22%3E%3Crect fill=%22%23222%22 width=%22390%22 height=%22280%22/%3E%3Ctext fill=%22%23fff%22 x=%2220%22 y=%22260%22 font-size=%2216%22%3E' + encodeURIComponent(r.restaurant_name) + '%3C/text%3E%3C/svg%3E\")';

    return {
      name: r.restaurant_name,
      title: r.restaurant_name,
      match: matchPct + '%',
      matchText: matchPct + '% match',
      price: Number(r.price).toLocaleString('vi-VN') + 'đ',
      distance: distance,
      rating: rating,
      tag: mealType + ' • ' + matchPct + '% phù hợp',
      image: imgUrl,
      gradient: gradient,
      mealType: mealType,
      backendData: r,
      dishName: r.dish_name
    };
  }

  function buildPeekCardHTML(r, index) {
    var d = backendResultToDetail(r, index);
    return '<div class=\"food-card-peek\" data-restaurant=\"' + d.name.replace(/\"/g, '&quot;') + '\" style=\"cursor:pointer;\">' +
      '<div style=\"position:absolute;inset:0;background:' + d.gradient + ';opacity:0.8;\"></div>' +
      '<span class=\"peek-name\">' + d.name + '</span>' +
      '<div style=\"display:flex;flex-direction:column;align-items:flex-end;position:relative;z-index:1;gap:3px;\">' +
      '<span class=\"peek-price\">' + d.price + '</span>' +
      '<span class=\"peek-match\">' + d.matchText + '</span>' +
      '</div></div>';
  }

  function syncBackendDataToCards() {
    if (!window.foodmindBackendResults || !window.foodmindBackendResults.length) return;

    var uniqueRestaurants = [];
    var seen = {};
    window.foodmindBackendResults.forEach(function(r) {
      if (!seen[r.restaurant_name]) {
        seen[r.restaurant_name] = true;
        uniqueRestaurants.push(r);
      }
    });

    uniqueRestaurants.forEach(function(r) {
      var d = backendResultToDetail(r, 0);
      restaurantDetails[r.restaurant_name] = d;
    });

    var top4 = uniqueRestaurants.slice(0, 4);
    if (top4.length === 0) return;

    ['#screen-result', '#screen-result1'].forEach(function(sel) {
      var screen = document.querySelector(sel);
      if (!screen) return;

      if (top4.length > 0) {
        var detail = restaurantDetails[top4[0].restaurant_name];
        if (detail) {
          selectedRestaurantName = detail.name;
          var mainCard = screen.querySelector('.food-card');
          if (mainCard && mainCard.firstElementChild) {
            mainCard.firstElementChild.style.background = detail.image + ' center/cover';
          }
          var matchPct = screen.querySelector('.match-pct');
          var ratingVal = screen.querySelector('.rating-val');
          var distance = screen.querySelector('.food-distance');
          var foodName = screen.querySelector('.food-name');
          var priceBadge = screen.querySelector('.price-badge');
          var firstTag = screen.querySelector('.tags-row .tag:first-child');
          var mealTypeBadge = screen.querySelector('.meal-type-badge');

          if (matchPct) matchPct.textContent = detail.match;
          if (ratingVal) ratingVal.textContent = detail.rating;
          if (distance) distance.textContent = detail.distance;
          if (foodName) foodName.textContent = detail.name;
          if (priceBadge) priceBadge.textContent = detail.price;
          if (firstTag) firstTag.textContent = detail.tag;
          if (mealTypeBadge) {
            mealTypeBadge.textContent = detail.mealType;
            mealTypeBadge.className = 'meal-type-badge mtype-' + detail.mealType.toLowerCase().replace(/\\s+/g, '-');
          }
        }
      }

      var scrollContent = screen.querySelector('.scroll-content');
      if (!scrollContent) return;
      var existingPeeks = scrollContent.querySelectorAll('.food-card-peek');
      existingPeeks.forEach(function(el) { el.remove(); });

      var tagsRow = scrollContent.querySelector('.tags-row');
      for (var i = 1; i < top4.length; i++) {
        var peekHTML = buildPeekCardHTML(top4[i], i);
        var temp = document.createElement('div');
        temp.innerHTML = peekHTML;
        var peekEl = temp.firstChild;
        if (tagsRow) {
          tagsRow.parentNode.insertBefore(peekEl, tagsRow);
        } else {
          scrollContent.appendChild(peekEl);
        }
        (function(restaurantName) {
          peekEl.addEventListener('click', function() {
            showRestaurantAsMainCard(restaurantName, sel);
          });
        })(top4[i].restaurant_name);
      }
    });
  }

  function populateSinglesMenu() {
    var container = document.getElementById('singles-menu-list');
    if (!container) return;
    if (!window.foodmindBackendResults || !window.foodmindBackendResults.length) return;

    container.innerHTML = '';
    window.foodmindBackendResults.forEach(function(r, idx) {
      var priceFormatted = Number(r.price).toLocaleString('vi-VN') + ' đ';
      var imgSrc = r.image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=150&q=80';
      var desc = (r.meal_type || 'Món ngon') + ' • ' + (r.calories || 0) + ' kcal';

      var itemHTML = '<div class="menu-item" data-dish-id="' + r.dish_id + '">' +
        '<img src="' + imgSrc + '" alt="' + r.dish_name.replace(/"/g, '&quot;') + '" class="menu-img" onerror="this.src=\'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=150&q=80\'">' +
        '<div class="menu-info">' +
          '<div class="menu-name">' + r.dish_name + '</div>' +
          '<div class="menu-desc">' + desc + '</div>' +
          '<div class="menu-meta">' +
            '<span class="menu-cal">🔥 ' + (r.calories || 0) + ' kcal</span>' +
            '<span style="color:#ccc">•</span>' +
            '<span class="menu-price">' + priceFormatted + '</span>' +
          '</div>' +
        '</div>' +
        '<button class="add-btn">' +
          '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">' +
            '<line x1="12" y1="5" x2="12" y2="19"></line>' +
            '<line x1="5" y1="12" x2="19" y2="12"></line>' +
          '</svg>' +
        '</button>' +
      '</div>';
      container.insertAdjacentHTML('beforeend', itemHTML);
    });
  }

  function populateDetailMenu(restaurantName) {
    var container = document.getElementById('detail-menu-list');
    if (!container) return;
    if (!window.foodmindBackendResults || !window.foodmindBackendResults.length) return;

    var restaurantDishes = window.foodmindBackendResults.filter(function(r) {
      return r.restaurant_name === restaurantName;
    });

    container.innerHTML = '';
    if (restaurantDishes.length === 0) {
      container.innerHTML = '<div style="padding:24px;text-align:center;color:#999;">Chưa có món nào từ quán này</div>';
      return;
    }

    restaurantDishes.forEach(function(r) {
      var priceFormatted = Number(r.price).toLocaleString('vi-VN') + ' đ';
      var imgSrc = r.image_url || 'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=150&q=80';
      var matchPct = r.match_score ? r.match_score.toFixed(0) + '% match' : '';
      var desc = (r.meal_type || 'Món ngon') + (matchPct ? ' • ' + matchPct : '');

      var itemHTML = '<div class="menu-item" data-dish-id="' + r.dish_id + '">' +
        '<img src="' + imgSrc + '" alt="' + r.dish_name.replace(/"/g, '&quot;') + '" class="menu-img" onerror="this.src=\'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?auto=format&fit=crop&w=150&q=80\'">' +
        '<div class="menu-info">' +
          '<div class="menu-name">' + r.dish_name + '</div>' +
          '<div class="menu-desc">' + desc + '</div>' +
          '<div class="menu-meta">' +
            '<span class="menu-cal">🔥 ' + (r.calories || 0) + ' kcal</span>' +
            '<span style="color:#ccc">•</span>' +
            '<span class="menu-price">' + priceFormatted + '</span>' +
          '</div>' +
        '</div>' +
        '<button class="add-btn">' +
          '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">' +
            '<line x1="12" y1="5" x2="12" y2="19"></line>' +
            '<line x1="5" y1="12" x2="19" y2="12"></line>' +
          '</svg>' +
        '</button>' +
      '</div>';
      container.insertAdjacentHTML('beforeend', itemHTML);
    });
  }

  readPrefsFromHash();

  // JS animation loop — tự tay animate từng frame, KHÔNG dựa vào CSS transition
  function animateBar(el, targetPct, duration) {
    if (!el) return;
    var startTime = performance.now();
    var startPct = 0;
    el.style.width = '0%';
    function step(now) {
      var elapsed = now - startTime;
      var progress = Math.min(elapsed / duration, 1);
      // ease-out cubic: rõ ràng, mượt
      var eased = 1 - Math.pow(1 - progress, 3);
      el.style.width = (startPct + (targetPct - startPct) * eased) + '%';
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // Chờ card fadeUp gần xong (2.1s + 0.5s = ~2.6s) mới fill bar
  setTimeout(function() {
    var p = window.userPrefs;
    var hungerPct = Math.round((parseFloat(p.hunger) / 10) * 100);
    var budgetPct = ({'under_30k':18,'30_50k':40,'50_100k':70,'over_100k':95}[p.budget] || 50);
    animateBar(document.querySelector('.bar-hunger'), hungerPct, 800);
    animateBar(document.querySelector('.bar-budget'), budgetPct, 800);
  }, 2500);

  function recalculateFuzzyScoresJS() {
    if (!window.foodmindRawResults || !window.userPrefs) return;
    var p = window.userPrefs;

    function getBudgetScore(price, budgetStr) {
      var score = 1.0;
      if (budgetStr === 'under_30k' && price > 35000) score -= (price-30000)/20000;
      if (budgetStr === '30_50k' && (price < 25000 || price > 55000)) score -= Math.abs(price-40000)/40000;
      if (budgetStr === '50_100k' && (price < 40000 || price > 110000)) score -= Math.abs(price-75000)/75000;
      if (budgetStr === 'over_100k' && price < 80000) score -= (90000-price)/40000;
      return Math.max(0.1, Math.min(1.0, score));
    }

    function getHungerScore(cals, hungerVal) {
      var targetCals = (hungerVal || 5) * 100;
      var diff = Math.abs(cals - targetCals);
      return Math.max(0.1, 1.0 - (diff / Math.max(1, targetCals)));
    }

    function getDietScore(protein, carbs, fat, cals, dietStr) {
      if (!dietStr || dietStr === 'Normal' || dietStr === 'Không') return 1.0;
      var score = 1.0;
      if (dietStr === 'Diet' || dietStr === 'Healthy' || dietStr.includes('Giảm cân') || dietStr.includes('Healthy')) {
        if (carbs > 50) score -= (carbs-50)/100;
        if (fat > 20) score -= (fat-20)/50;
        if (cals > 500) score -= (cals-500)/500;
      } else if (dietStr === 'Bulking' || dietStr.includes('Tăng cơ')) {
        if (protein < 30) score -= (30-protein)/50;
        if (carbs < 80) score -= (80-carbs)/100;
        if (cals < 800) score -= (800-cals)/1000;
      }
      return Math.max(0.1, Math.min(1.0, score));
    }

    function getCuisineScore(dishCuisine, userCuisine) {
      if (!userCuisine || userCuisine.toLowerCase() === 'any') return 1.0;
      var dc = (dishCuisine || '').toLowerCase();
      var uc = userCuisine.toLowerCase();
      if (dc.includes(uc) || uc.includes(dc)) return 1.0;
      if (uc.includes('việt nam') && dc.includes('vn')) return 1.0;
      if (uc.includes('hàn') && dc.includes('kr')) return 1.0;
      if (uc.includes('nhật') && dc.includes('jp')) return 1.0;
      if (uc.includes('trung') && dc.includes('cn')) return 1.0;
      return 0.2;
    }

    var recalculated = window.foodmindRawResults.map(function(r) {
      var pScore = getBudgetScore(r.price, p.budget);
      var hScore = getHungerScore(r.calories, p.hunger);
      var dScore = getDietScore(r.protein_g, r.carb_g, r.fat_g, r.calories, p.diet || p.health_goal);
      var cuScore = getCuisineScore(r.cuisine_type, p.cuisine);
      
      var baseScore = (pScore * 0.4) + (0.8 * 0.1) + (hScore * 0.2) + (dScore * 0.2) + (0.8 * 0.1);
      var finalScore = baseScore * cuScore;
      finalScore = Math.min(0.99, finalScore * 1.4);

      return Object.assign({}, r, {
        match_score: finalScore * 100,
        meal_type: r.food_category && r.food_category.toLowerCase().includes('snack') ? 'Snack' : 'Full meal'
      });
    });

    recalculated.sort(function(a, b) { return b.match_score - a.match_score; });
    window.foodmindAllRecalculated = recalculated;
    window.foodmindBackendResults = recalculated.slice(0, 15);
    
    var breakfast = recalculated.find(function(r) { return r.meal_type === 'Snack'; }) || recalculated[2] || recalculated[0];
    var lunch = recalculated.find(function(r) { return r.meal_type === 'Full meal' && r.dish_id !== breakfast.dish_id; }) || recalculated[0];
    var dinner = recalculated.find(function(r) { return r.meal_type === 'Full meal' && r.dish_id !== breakfast.dish_id && r.dish_id !== lunch.dish_id; }) || recalculated[1] || recalculated[0];
    
    window.foodmindMealPlan = {
      Breakfast: breakfast,
      Lunch: lunch,
      Dinner: dinner
    };
  }

  function populateTrendingRestaurants() {
    var container = document.querySelector('.trending-horizontal-scroll');
    if (!container || !window.foodmindRestaurants || !window.foodmindRestaurants.length) return;

    var sortedRests = window.foodmindRestaurants.slice().sort(function(a, b) {
      var rA = a.rating || 0;
      var rB = b.rating || 0;
      return rB - rA;
    });

    var top5 = sortedRests.slice(0, 5);
    container.innerHTML = ''; // clear hardcoded

    top5.forEach(function(r) {
      var img = r.cover_image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=300&q=80';
      var rating = (r.rating || 4.0).toFixed(1);
      
      var address = r.address || '';
      var districtMatch = address.match(/Quận \d+|Q\.\d+|Quận [a-zA-Z\s]+/i);
      var district = districtMatch ? districtMatch[0] : 'Quận 1';

      var card = document.createElement('div');
      card.className = 'trend-card';
      card.setAttribute('data-restaurant', r.name);
      card.innerHTML = '<div class="trend-img-wrap">' +
          '<img src="' + img + '" alt="' + r.name.replace(/"/g, '&quot;') + '" class="trend-img">' +
          '<div class="rating-badge"><span style="color:#FFD600">★</span> ' + rating + '</div>' +
        '</div>' +
        '<div class="trend-info">' +
          '<div class="trend-name">' + r.name + '</div>' +
          '<div class="trend-loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg> ' + district + '</div>' +
        '</div>';
      container.appendChild(card);
    });
  }

  setTimeout(populateTrendingRestaurants, 50);

  setTimeout(function() {
    recalculateFuzzyScoresJS();
    populateMealPlanScreen();
    syncBackendDataToCards();
    populateSinglesMenu();
    applyPrefsToUI();
  }, 4600);

</script>
</body>
</html>
"""

# ============================================================
# BACKEND: Tải dữ liệu thật & inject vào HTML
# ============================================================
try:
    _config, _dishes_df, _restaurants_df = load_data()

    # User preferences mặc định cho lần đầu load
    _default_inputs = {
        'lat': 10.7614, 'lng': 106.6686,
        'budget': '30_50k', 'time': 'fast',
        'hunger': 6.5, 'health_goal': 'Normal',
        'weather': 'Normal', 'cuisine': 'Việt Nam'
    }
    _all_recs = get_recommendations(_default_inputs, _config, _dishes_df, _restaurants_df)

    # --- window.foodmindBackendResults (top 15 recommendations) ---
    _backend_results_json = []
    for _br in _all_recs[:15]:
        _bd = _dishes_df[_dishes_df['dish_id'] == _br['dish_id']]
        if len(_bd) == 0:
            continue
        _bd = _bd.iloc[0]
        _backend_results_json.append({
            'dish_id': str(_br['dish_id']),
            'dish_name': str(_br['dish_name']),
            'restaurant_id': str(_br['restaurant_id']),
            'restaurant_name': str(_br['restaurant_name']),
            'price': int(_br['price']) if _pd.notna(_br.get('price')) else 0,
            'calories': int(float(_bd['calories'])) if _pd.notna(_bd.get('calories')) else 0,
            'protein_g': int(float(_bd['protein_g'])) if _pd.notna(_bd.get('protein_g')) else 0,
            'carb_g': int(float(_bd['carb_g'])) if _pd.notna(_bd.get('carb_g')) else 0,
            'fat_g': int(float(_bd['fat_g'])) if _pd.notna(_bd.get('fat_g')) else 0,
            'image_url': str(_bd.get('image_url', '')),
            'match_score': _br['match_score'],
            'meal_type': str(_br.get('meal_type', ''))
        })

    # --- window.foodmindRestaurants (danh sách quán ăn) ---
    _restaurants_json = []
    for _, row in _restaurants_df.iterrows():
        _restaurants_json.append({
            'restaurant_id': str(row['restaurant_id']),
            'name': str(row['name']),
            'lat': float(row['lat']) if _pd.notna(row.get('lat')) else None,
            'lng': float(row['lng']) if _pd.notna(row.get('lng')) else None,
            'avg_prep_time': float(row.get('avg_prep_time', 15)) if _pd.notna(row.get('avg_prep_time', 15)) else 15,
            'is_open': str(row.get('is_open', 'True')).lower() != 'false',
            'open_hours': str(row.get('open_hours', '00:00-23:59')),
            'cuisine_type': str(row.get('cuisine_type', '')),
            'cover_image_url': str(row.get('cover_image_url', '')),
            'rating': float(row.get('rating', 4.0)),
            'address': str(row.get('address', ''))
        })

    # --- window.foodmindMealPlan (kế hoạch bữa ăn) ---
    _meal_plan = generate_daily_plan(_default_inputs, _config, _dishes_df, _restaurants_df)
    _meal_plan_json = {}
    _used_dish_ids = []
    for _meal_key, _meal_val in _meal_plan.items():
        _dinfo = _dishes_df[_dishes_df['dish_id'] == _meal_val['dish_id']]
        if len(_dinfo) == 0:
            continue
        _dinfo = _dinfo.iloc[0]
        _used_dish_ids.append(str(_meal_val['dish_id']))
        _mprice = int(_meal_val['price']) if _pd.notna(_meal_val.get('price')) else 0
        _mcal = int(float(_dinfo['calories'])) if _pd.notna(_dinfo.get('calories')) else 0
        _mprotein = int(float(_dinfo['protein_g'])) if _pd.notna(_dinfo.get('protein_g')) else 0
        _mcarbs = int(float(_dinfo['carb_g'])) if _pd.notna(_dinfo.get('carb_g')) else 0
        _mfat = int(float(_dinfo['fat_g'])) if _pd.notna(_dinfo.get('fat_g')) else 0
        _meal_plan_json[_meal_key] = {
            'dish_id': str(_meal_val['dish_id']),
            'name': str(_meal_val['dish_name']),
            'restaurant_name': str(_meal_val['restaurant_name']),
            'restaurant_id': str(_meal_val['restaurant_id']),
            'price': _mprice,
            'calories': _mcal,
            'protein': _mprotein,
            'carbs': _mcarbs,
            'fat': _mfat,
            'image_url': str(_dinfo.get('image_url', '')),
            'match_score': _meal_val['match_score'],
            'meal_type': str(_meal_val.get('meal_type', ''))
        }

    # --- Sinh danh sách thay thế cho mỗi bữa ---
    _meal_alternatives = {'breakfast': [], 'lunch': [], 'dinner': []}
    for _r in _all_recs:
        if len(_meal_alternatives['breakfast']) >= 3 and len(_meal_alternatives['lunch']) >= 3 and len(_meal_alternatives['dinner']) >= 3:
            break
        _did = str(_r['dish_id'])
        if _did in _used_dish_ids:
            continue
        _mt = _r.get('meal_type', '')
        _slot = 'breakfast' if _mt == 'Snack' else ('lunch' if _mt == 'Full meal' else 'dinner')
        if len(_meal_alternatives[_slot]) < 3:
            _dinfo2 = _dishes_df[_dishes_df['dish_id'] == _r['dish_id']]
            if len(_dinfo2) == 0:
                continue
            _dinfo2 = _dinfo2.iloc[0]
            _meal_alternatives[_slot].append({
                'dish_id': _did,
                'name': str(_r['dish_name']),
                'restaurant_name': str(_r['restaurant_name']),
                'price': int(_r['price']) if _pd.notna(_r.get('price')) else 0,
                'calories': int(float(_dinfo2['calories'])) if _pd.notna(_dinfo2.get('calories')) else 0,
                'protein': int(float(_dinfo2['protein_g'])) if _pd.notna(_dinfo2.get('protein_g')) else 0,
                'carbs': int(float(_dinfo2['carb_g'])) if _pd.notna(_dinfo2.get('carb_g')) else 0,
                'fat': int(float(_dinfo2['fat_g'])) if _pd.notna(_dinfo2.get('fat_g')) else 0,
                'match_score': _r['match_score']
            })

    # --- Inject dữ liệu vào HTML ---
    _inject_script = (
        '<script>'
        'window.foodmindBackendResults = ' + _json.dumps(_backend_results_json, ensure_ascii=False) + ';'
        'window.foodmindRestaurants = ' + _json.dumps(_restaurants_json, ensure_ascii=False) + ';'
        'window.foodmindMealPlan = ' + _json.dumps(_meal_plan_json, ensure_ascii=False) + ';'
        'window.foodmindMealAlternatives = ' + _json.dumps(_meal_alternatives, ensure_ascii=False) + ';'
        'window.foodmindMealTargets = {calories:1800,protein:120,carbs:250,fat:65};'
        '</script>'
    )
    html_code = html_code.replace('</body>', _inject_script + '\n</body>')

    # Progress bar widths are handled by JS + CSS transition (delayed animation in script)
except Exception as _e:
    html_code = html_code.replace('</body>', f'<script>window.foodmindBackendError = "{str(_e)}";</script>\n</body>')

# Render ra giao diện Streamlit
components.html(html_code, height=950, scrolling=False)
