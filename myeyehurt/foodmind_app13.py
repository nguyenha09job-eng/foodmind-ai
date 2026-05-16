import streamlit as st
import streamlit.components.v1 as components
import sys, json
from pathlib import Path

# --- Import backend & Folium ---
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'mybackhurt'))
from fuzzylogic import get_nearby_restaurants_for_map
from geopy.distance import geodesic
import folium

st.set_page_config(
    page_title="FoodMind AI - Tracking",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stAppViewContainer"] { background: #333; }
    </style>
""", unsafe_allow_html=True)

# --- Tải dữ liệu thật ---
USER_LAT, USER_LNG = 10.7614, 106.6686
restaurants_data = get_nearby_restaurants_for_map(USER_LAT, USER_LNG)
target = restaurants_data[0] if restaurants_data else {
    'name': 'Quán ăn', 'lat': 10.765, 'lng': 106.672,
    'distance_str': '~1 km', 'rating': 4.5, 'avg_prep_time': 15
}
TARGET_LAT, TARGET_LNG = target['lat'], target['lng']
SHIPPER_LAT = USER_LAT + (TARGET_LAT - USER_LAT) * 0.55
SHIPPER_LNG = USER_LNG + (TARGET_LNG - USER_LNG) * 0.55
dist_km = geodesic((USER_LAT, USER_LNG), (TARGET_LAT, TARGET_LNG)).kilometers
ETA_MIN = int(dist_km * 4 + target.get('avg_prep_time', 15) + 5)
REST_NAME = target['name']

# --- Tạo Folium map tracking ---
m = folium.Map(location=[SHIPPER_LAT, SHIPPER_LNG], zoom_start=15, control_scale=True, tiles='OpenStreetMap')
folium.Marker(location=[USER_LAT, USER_LNG], popup=folium.Popup("📍 Vị trí của bạn", max_width=200), icon=folium.Icon(color="blue", icon="home", prefix="fa")).add_to(m)
folium.Marker(location=[TARGET_LAT, TARGET_LNG], popup=folium.Popup(f"🏪 {REST_NAME}", max_width=200), icon=folium.Icon(color="red", icon="cutlery", prefix="fa")).add_to(m)
folium.Marker(location=[SHIPPER_LAT, SHIPPER_LNG], popup=folium.Popup("🛵 Shipper đang trên đường", max_width=200), icon=folium.Icon(color="orange", icon="motorcycle", prefix="fa")).add_to(m)
folium.PolyLine(locations=[[TARGET_LAT, TARGET_LNG], [SHIPPER_LAT, SHIPPER_LNG], [USER_LAT, USER_LNG]], color="#FF5A1F", weight=5, opacity=0.8).add_to(m)
m.fit_bounds([[min(USER_LAT, TARGET_LAT), min(USER_LNG, TARGET_LNG)], [max(USER_LAT, TARGET_LAT), max(USER_LNG, TARGET_LNG)]], padding=[40, 40])

FOLIUM_HTML = m.get_root().render()
FOLIUM_HTML = FOLIUM_HTML.replace('</head>', '<meta name="viewport" content="width=device-width, initial-scale=1.0"><style>html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;}.folium-map{width:100%!important;height:100%!important;position:absolute;top:0;left:0;}</style></head>')
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

.phone-frame {
  width: 390px;
  min-height: 844px;
  max-height: 844px;
  background-color: #e5e2d8;
  border-radius: 48px;
  box-shadow: 0 40px 80px rgba(0,0,0,0.25), 0 0 0 10px #1a1a1a;
  position: relative;
  overflow: hidden;
}

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

.notch {
  position: absolute;
  top: 14px; left: 50%; transform: translateX(-50%);
  width: 120px; height: 34px;
  background: #1a1a1a;
  border-radius: 20px;
  z-index: 100;
}

.top-card {
  position: absolute;
  top: 60px; left: 16px; right: 16px;
  background: #fff;
  border-radius: 36px;
  padding: 18px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  z-index: 50;
}

.back-btn {
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: flex-start;
  cursor: pointer;
  color: #1a1a1a;
}

.eta-info { text-align: center; flex: 1; }

.eta-label {
  font-size: 10px;
  font-weight: 800;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 2px;
}

.eta-time {
  font-family: 'Sora', sans-serif;
  font-size: 20px;
  font-weight: 800;
  color: #1a1a1a;
}

.time-icon {
  width: 44px; height: 44px;
  background: #FFF0EB;
  color: #FF5A1F;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}

.route-svg {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 1;
}



.bottom-sheet {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: #fff;
  border-radius: 40px 40px 0 0;
  padding: 16px 24px 32px;
  box-shadow: 0 -10px 40px rgba(0,0,0,0.1);
  z-index: 50;
}

.drag-handle {
  width: 40px; height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  margin: 0 auto 24px;
}

.driver-card {
  display: flex;
  align-items: center;
  background: #fafaf8;
  border-radius: 28px;
  padding: 16px;
  margin-bottom: 28px;
}

.driver-avatar {
  width: 54px; height: 54px;
  background: #FFD600;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Sora', sans-serif;
  font-size: 18px;
  font-weight: 800;
  color: #1a1a1a;
}

.driver-info { flex: 1; margin-left: 14px; }

.driver-name {
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  font-size: 17px;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.driver-meta {
  font-size: 13px;
  color: #888;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.star-rating { color: #FFC107; font-weight: 700; display:flex; align-items:center; gap:3px;}

.driver-actions { display: flex; gap: 10px; }

.action-btn {
  width: 48px; height: 48px;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
}

.btn-chat { background: #fff; border: 1.5px solid #e8e6e0; color: #1a1a1a; }

.btn-call {
  background: #FF5A1F;
  color: #fff;
  box-shadow: 0 4px 12px rgba(255, 90, 31, 0.3);
}

.timeline-wrap {
  position: relative;
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  padding: 0 4px;
}

.timeline-wrap::before {
  content: '';
  position: absolute;
  top: 15px; left: 20px; right: 20px;
  height: 2px;
  background: #f0f0f0;
  z-index: 1;
}

.progress-line {
  position: absolute;
  top: 15px; left: 20px;
  width: 0%;
  height: 2px;
  background: #00C853;
  z-index: 1;
  transition: width 0.5s linear;
}

.step {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 50px;
}

.step-icon {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: #00C853;
  color: #fff;
}

.step-icon.current { box-shadow: 0 0 0 6px #E8F5E9; }

.step-icon.inactive { background: #f0f0f0; }
.step-icon.inactive .dot { width: 8px; height: 8px; background: #ccc; border-radius: 50%; }

.step-label {
  font-size: 10px;
  font-weight: 800;
  color: #1a1a1a;
  text-align: center;
  line-height: 1.3;
}

.step.inactive .step-label { color: #999; font-weight: 700; }

.status-text {
  text-align: center;
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  font-size: 16px;
  color: #FF5A1F;
}
</style>
</head>
<body>

<div class="phone-frame">
  <div class="notch"></div>

  <div class="map-iframe-wrapper" id="map-wrapper"></div>

  <div class="top-card">
    <div class="back-btn" onclick="window.parent.postMessage({type:'foodmind-back-from-tracking'},'*')">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
    </div>
    <div class="eta-info">
      <div class="eta-label">DỰ KIẾN GIAO</div>
      <div class="eta-time">__ETA_MIN__ phút nữa</div>
    </div>
    <div class="time-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
      </svg>
    </div>
  </div>



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
        <div class="action-btn btn-call">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        </div>
      </div>
    </div>

    <div class="timeline-wrap" id="tracking-timeline">
      <div class="progress-line" id="progress-line"></div>
      <div class="step"><div class="step-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div><div class="step-label">Đã xác<br>nhận</div></div>
      <div class="step inactive"><div class="step-icon inactive"><div class="dot"></div></div><div class="step-label">Đang<br>chuẩn bị</div></div>
      <div class="step inactive"><div class="step-icon inactive"><div class="dot"></div></div><div class="step-label">Shipper<br>nhận đơn</div></div>
      <div class="step inactive"><div class="step-icon inactive"><div class="dot"></div></div><div class="step-label">Đang giao</div></div>
      <div class="step inactive"><div class="step-icon inactive"><div class="dot"></div></div><div class="step-label">Đã giao</div></div>
    </div>

    <div class="status-text">Shipper đang trên đường</div>
  </div>
</div>

<script>
(function() {
    var mapWrapper = document.getElementById('map-wrapper');
    if (mapWrapper) {
        var mapIframe = document.createElement('iframe');
        mapIframe.srcdoc = `__FOLIUM_HTML__`;
        mapIframe.setAttribute('allow', 'geolocation');
        mapWrapper.appendChild(mapIframe);
    }

    // Progress bar animation logic
    var duration = 30000; // 30 seconds
    var startTime = performance.now();
    var progressLine = document.getElementById('progress-line');
    var steps = document.querySelectorAll('#tracking-timeline .step');
    var statusText = document.querySelector('.status-text');

    var svgCheck = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
    var dotDiv = '<div class="dot"></div>';

    var statusMessages = [
        "Đơn hàng đã được xác nhận",
        "Nhà hàng đang chuẩn bị món",
        "Shipper đã nhận được món",
        "Shipper đang trên đường giao đến bạn",
        "Đơn hàng đã giao thành công!"
    ];

    function updateStep(index, isCurrent, isDone) {
        var step = steps[index];
        if (!step) return;
        var iconDiv = step.querySelector('.step-icon');
        
        if (isDone) {
            step.classList.remove('inactive');
            iconDiv.classList.remove('inactive', 'current');
            iconDiv.innerHTML = svgCheck;
        } else if (isCurrent) {
            step.classList.remove('inactive');
            iconDiv.classList.remove('inactive');
            iconDiv.classList.add('current');
            iconDiv.innerHTML = svgCheck;
        } else {
            step.classList.add('inactive');
            iconDiv.classList.add('inactive');
            iconDiv.classList.remove('current');
            iconDiv.innerHTML = dotDiv;
        }
    }

    function animate(now) {
        var elapsed = now - startTime;
        var pct = Math.min(100, (elapsed / duration) * 100);
        progressLine.style.width = pct + '%';

        var stage = Math.floor(pct / 25); // 0, 1, 2, 3, 4
        stage = Math.min(4, stage);

        for (var i = 0; i < 5; i++) {
            if (i < stage) {
                updateStep(i, false, true); // done
            } else if (i === stage) {
                updateStep(i, true, false); // current
            } else {
                updateStep(i, false, false); // inactive
            }
        }

        if (statusText) {
            statusText.textContent = statusMessages[stage];
        }

        if (pct < 100) {
            requestAnimationFrame(animate);
        }
    }

    requestAnimationFrame(animate);
})();
</script>

</body>
</html>
"""

# --- Chèn dữ liệu thật vào placeholder ---
html_code = html_code.replace('__ETA_MIN__', str(ETA_MIN))
html_code = html_code.replace('__REST_NAME__', REST_NAME)
html_code = html_code.replace('__FOLIUM_HTML__', FOLIUM_JS_SAFE)

components.html(html_code, height=960, scrolling=False)
