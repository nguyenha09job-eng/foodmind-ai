import streamlit as st
import streamlit.components.v1 as components
import sys, os, json
from pathlib import Path

# --- Import backend & Folium ---
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'mybackhurt'))
from fuzzylogic import get_nearby_restaurants_for_map
import folium

st.set_page_config(
    page_title="FoodMind AI - Map Explore",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stAppViewContainer"] { background: #333; } /* Nền tối để tôn lên điện thoại */
    </style>
""", unsafe_allow_html=True)

# --- Tải dữ liệu thật + tạo Folium map ---
USER_LAT, USER_LNG = 10.7614, 106.6686
restaurants_data = get_nearby_restaurants_for_map(USER_LAT, USER_LNG)

# Tạo Folium map với marker rõ ràng
m = folium.Map(location=[USER_LAT, USER_LNG], zoom_start=15, control_scale=True, tiles='OpenStreetMap')

# Marker vị trí người dùng (xanh dương)
folium.Marker(
    location=[USER_LAT, USER_LNG],
    popup=folium.Popup("📍 Vị trí của bạn", max_width=200),
    icon=folium.Icon(color="blue", icon="home", prefix="fa")
).add_to(m)

# Marker nhà hàng
for r in restaurants_data:
    match_pct = r.get('top_match', 50)
    if match_pct >= 80:
        color = 'red'
        label = '🔥 '
    elif match_pct >= 60:
        color = 'orange'
        label = '⭐ '
    else:
        color = 'green'
        label = ''
    popup_html = (
        f'<div style="font-family:Be Vietnam Pro,sans-serif;min-width:200px;">'
        f'<b style="font-size:15px;">{r["name"]}</b><br>'
        f'⭐ {r.get("rating",4.0):.1f} | 🏆 {match_pct:.0f}% Match<br>'
        f'📍 Cách {r.get("distance_str","~1 km")}'
        f'</div>'
    )
    folium.Marker(
        location=[r['lat'], r['lng']],
        popup=folium.Popup(popup_html, max_width=280),
        icon=folium.Icon(color=color, icon="cutlery", prefix="fa"),
        tooltip=f'{label}{r["name"]} ({match_pct:.0f}%)'
    ).add_to(m)

# Fit bounds để hiển thị tất cả marker
if restaurants_data:
    lats = [USER_LAT] + [r['lat'] for r in restaurants_data]
    lngs = [USER_LNG] + [r['lng'] for r in restaurants_data]
    m.fit_bounds([[min(lats), min(lngs)], [max(lats), max(lngs)]], padding=[30, 30])
FOLIUM_HTML = m.get_root().render()
FOLIUM_HTML = FOLIUM_HTML.replace('</head>', (
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    '<style>html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;}'
    '.folium-map{width:100%!important;height:100%!important;position:absolute;top:0;left:0;}</style></head>'
))
RESTAURANTS_JSON = json.dumps(restaurants_data, ensure_ascii=False)
# Escape cho JS template literal (tránh vỡ script tag)
FOLIUM_JS_SAFE = FOLIUM_HTML.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('</', '<\\/')

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
  background: transparent;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  font-family: 'Be Vietnam Pro', sans-serif;
  padding: 24px 0 40px;
}

/* =========================================
   KHUNG ĐIỆN THOẠI
   ========================================= */
.phone-frame {
  width: 390px;
  min-height: 844px;
  max-height: 844px;
  /* Nền bản đồ dạng lưới mờ */
  background-color: #ebe8dc;
  background-image: 
    linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
  background-size: 90px 90px;
  background-position: center;
  border-radius: 48px;
  box-shadow: 0 40px 80px rgba(0,0,0,0.25), 0 0 0 10px #1a1a1a;
  position: relative;
  overflow: hidden;
}

/* Tai thỏ (Notch) */
.notch {
  position: absolute;
  top: 14px; left: 50%; transform: translateX(-50%);
  width: 120px; height: 34px;
  background: #1a1a1a;
  border-radius: 20px;
  z-index: 100;
}

/* =========================================
   THANH TÌM KIẾM (SEARCH BAR)
   ========================================= */
.search-area {
  position: absolute;
  top: 64px; left: 20px; right: 20px;
  display: flex;
  gap: 12px;
  z-index: 60;
  pointer-events: auto;
}

.search-box {
  flex: 1;
  background: #fff;
  border-radius: 24px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  pointer-events: auto;
}

.search-input {
  border: none;
  outline: none;
  font-family: 'Be Vietnam Pro', sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: #333;
  width: 100%;
  padding: 18px 0;
  margin-left: 12px;
  background: transparent;
  pointer-events: auto;
}

.search-input::placeholder { color: #aaa; }

.filter-btn {
  width: 58px; height: 58px;
  background: #1a1a1a;
  border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  cursor: pointer;
  flex-shrink: 0;
}

/* =========================================
   BẢN ĐỒ & MARKERS
   ========================================= */
.map-marker {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  transform: translate(-50%, -50%);
  z-index: 5;
  cursor: pointer;
  transition: transform 0.2s;
}

.map-marker:hover { transform: translate(-50%, -55%); z-index: 15; }

.match-tag {
  background: #fff;
  color: #FF5A1F;
  font-size: 10px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 14px;
  margin-bottom: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  font-family: 'Sora', sans-serif;
}

.marker-bubble {
  width: 46px; height: 46px;
  background: #fff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  position: relative;
}

.marker-bubble::after {
  content: '';
  position: absolute;
  bottom: -6px; left: 50%;
  transform: translateX(-50%);
  border-width: 8px 6px 0;
  border-style: solid;
  border-color: #fff transparent transparent transparent;
}

/* Marker vị trí người dùng */
.user-dot-wrapper {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  z-index: 4;
}
.user-dot {
  width: 20px; height: 20px;
  background: #4285F4;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.user-pulse {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 20px; height: 20px;
  background: rgba(66, 133, 244, 0.4);
  border-radius: 50%;
  animation: pulse 2s infinite ease-out;
}
@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(3.5); opacity: 0; }
}

/* =========================================
   BOTTOM SHEET & SCROLL AREA
   ========================================= */
.bottom-sheet {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: #fff;
  border-radius: 40px 40px 0 0;
  display: flex;
  flex-direction: column;
  height: 52%; /* Độ cao của bottom sheet */
  box-shadow: 0 -10px 40px rgba(0,0,0,0.06);
  z-index: 20;
}

.drag-handle {
  width: 40px; height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  margin: 16px auto 0;
}

.sheet-header {
  padding: 20px 24px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.sheet-title {
  font-family: 'Sora', sans-serif;
  font-size: 22px;
  font-weight: 800;
  color: #1a1a1a;
}

.view-all {
  font-size: 13px;
  font-weight: 700;
  color: #FF5A1F;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

/* Khu vực cuộn danh sách nhà hàng */
.sheet-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 0 24px 100px; /* Thêm padding-bottom để không bị che bởi bottom nav */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.sheet-scroll-area::-webkit-scrollbar { display: none; }

/* Thẻ nhà hàng */
.res-card {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 1px solid #f0ede8;
  border-radius: 24px;
  margin-bottom: 16px;
  background: #fff;
  transition: border-color 0.2s;
  cursor: pointer;
}
.res-card:hover { border-color: #FF5A1F; box-shadow: 0 4px 15px rgba(255, 90, 31, 0.05); }
.res-card.is-hidden,
.map-marker.is-hidden {
  display: none;
}

.empty-results {
  display: none;
  padding: 22px 16px;
  text-align: center;
  color: #999;
  font-size: 14px;
  font-weight: 700;
}
.empty-results.is-visible {
  display: block;
}

.res-img-box {
  width: 56px; height: 56px;
  background: #f8f8f8;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px;
  margin-right: 16px;
  border: 1px solid #f0ede8;
}

.res-info { flex: 1; }

.res-name {
  font-family: 'Sora', sans-serif;
  font-size: 16px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 6px;
}

.res-meta {
  font-size: 12px;
  color: #999;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.rating { color: #1a1a1a; font-weight: 700; display: flex; align-items: center; gap: 4px;}

.res-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.match-badge {
  background: #FFF0EB;
  color: #FF5A1F;
  font-size: 11px;
  font-weight: 800;
  padding: 6px 10px;
  border-radius: 12px;
  font-family: 'Sora', sans-serif;
}

.chevron-icon { color: #ccc; }

/* =========================================
   FOLIUM MAP IFRAME WRAPPER
   ========================================= */
.map-iframe-wrapper {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  border-radius: 48px;
  overflow: hidden;
  z-index: 1;
}
.map-iframe-wrapper iframe {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

/* =========================================
   BOTTOM NAV (Cố định dưới cùng)
   ========================================= */
.bottom-nav {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 84px;
  background: rgba(255, 255, 255, 0.98);
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
  <div class="notch"></div>

  <div class="map-iframe-wrapper" id="map-wrapper"></div>

  <div class="search-area">
    <div class="search-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input type="text" class="search-input" placeholder="Tìm kiếm quán gần đây..." oninput="filterRestaurants()">
    </div>
  </div>

  <div class="user-dot-wrapper">
    <div class="user-pulse"></div>
    <div class="user-dot"></div>
  </div>

  <div class="bottom-sheet">
    <div class="drag-handle"></div>
    <div class="sheet-header">
      <div class="sheet-title">Quán gần nhất</div>
    </div>
    <div class="sheet-scroll-area" id="cards-container">
      <div class="empty-results" id="empty-msg">Không tìm thấy quán phù hợp</div>
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
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF5A1F" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon>
        <line x1="9" y1="3" x2="9" y2="18"></line>
        <line x1="15" y1="6" x2="15" y2="21"></line>
      </svg>
      <div class="nav-dot"></div>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
        <line x1="16" y1="2" x2="16" y2="6"></line>
        <line x1="8" y1="2" x2="8" y2="6"></line>
        <line x1="3" y1="10" x2="21" y2="10"></line>
      </svg>
    </div>
    <div class="nav-item">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
      </svg>
    </div>
  </div>

</div>

<script>
var restaurants = RESTAURANTS_JSON_PLACEHOLDER;

var MAP_TOP = 180, MAP_BOTTOM = 620, MAP_LEFT = 15, MAP_RIGHT = 375;
var MAP_WIDTH = MAP_RIGHT - MAP_LEFT;
var MAP_HEIGHT = MAP_BOTTOM - MAP_TOP;
var allLats = restaurants.map(function(r) { return r.lat; }).concat([USER_LAT_PLACEHOLDER]);
var allLngs = restaurants.map(function(r) { return r.lng; }).concat([USER_LNG_PLACEHOLDER]);
var minLat = Math.min.apply(null, allLats) - 0.003;
var maxLat = Math.max.apply(null, allLats) + 0.003;
var minLng = Math.min.apply(null, allLngs) - 0.003;
var maxLng = Math.max.apply(null, allLngs) + 0.003;

function latToY(lat) {
    var frac = (maxLat - lat) / (maxLat - minLat);
    if (isNaN(frac)) frac = 0.5;
    return MAP_TOP + frac * MAP_HEIGHT;
}

function lngToX(lng) {
    var frac = (lng - minLng) / (maxLng - minLng);
    if (isNaN(frac)) frac = 0.5;
    return MAP_LEFT + frac * MAP_WIDTH;
}

function buildCardHTML(r) {
    return '<div class="res-card" data-id="' + r.restaurant_id + '">'
        + '<div class="res-img-box">' + (r.emoji || '🍽️') + '</div>'
        + '<div class="res-info">'
        + '<div class="res-name">' + r.name + '</div>'
        + '<div class="res-meta">'
        + '<span class="rating"><span style="color:#FFD600;">★</span> ' + parseFloat(r.rating).toFixed(1) + '</span>'
        + '<span>•</span>'
        + '<span>Cách đây<br>' + (r.distance_str || '~1 km') + '</span>'
        + '</div>'
        + '</div>'
        + '<div class="res-right">'
        + '<div class="match-badge">' + Math.round(r.top_match) + '% Match</div>'
        + '<svg class="chevron-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>'
        + '</div>'
        + '</div>';
}

function renderAll() {
    var cardsHtml = '';
    for (var i = 0; i < restaurants.length; i++) {
        cardsHtml += buildCardHTML(restaurants[i]);
    }
    var cc = document.getElementById('cards-container');
    if (cc) cc.innerHTML = cardsHtml + '<div class="empty-results" id="empty-msg">Không tìm thấy quán phù hợp</div>';
}

function filterRestaurants() {
    var query = (document.querySelector('.search-input') || {}).value || '';
    query = query.toLowerCase().trim();
    var cards = document.querySelectorAll('.res-card');
    var emptyMsg = document.getElementById('empty-msg');
    var visibleCount = 0;
    cards.forEach(function(c) {
        var id = c.getAttribute('data-id');
        var r = restaurants.find(function(x) { return x.restaurant_id === id; });
        var name = (r ? r.name : '').toLowerCase();
        var match = !query || name.indexOf(query) !== -1;
        c.classList.toggle('is-hidden', !match);
        if (match) visibleCount++;
    });
    if (emptyMsg) emptyMsg.classList.toggle('is-visible', visibleCount === 0 && !!query);
}

// Nhúng Folium map
(function() {
    var mapWrapper = document.getElementById('map-wrapper');
    if (mapWrapper) {
        var mapIframe = document.createElement('iframe');
        mapIframe.srcdoc = FOLIUM_PLACEHOLDER;
        mapIframe.setAttribute('allow', 'geolocation');
        mapWrapper.appendChild(mapIframe);
    }
    renderAll();
})();
</script>

</body>
</html>
"""

# --- Chèn dữ liệu thật vào placeholder ---
html_code = html_code.replace('RESTAURANTS_JSON_PLACEHOLDER', RESTAURANTS_JSON)
html_code = html_code.replace('USER_LAT_PLACEHOLDER', str(USER_LAT))
html_code = html_code.replace('USER_LNG_PLACEHOLDER', str(USER_LNG))
html_code = html_code.replace('FOLIUM_PLACEHOLDER', '`' + FOLIUM_JS_SAFE + '`')

components.html(html_code, height=960, scrolling=False)
