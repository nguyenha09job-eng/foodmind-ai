import streamlit as st
import streamlit.components.v1 as components
import html
from pathlib import Path
import re

# --- Import backend cho bản đồ ---
import sys as _sys, os as _os, json as _json
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / 'mybackhurt'))
from fuzzylogic import get_nearby_restaurants_for_map
import folium as _folium

# --- Cấu hình ---
st.set_page_config(
    page_title="FoodMind AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Ẩn thành phần Streamlit thừa ---
st.markdown("""
<style>
    .block-container {
        padding-top: 0rem; padding-bottom: 0rem;
        padding-left: 0rem; padding-right: 0rem;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- Hàm trích xuất HTML từ file ---
BASE_DIR = Path(__file__).resolve().parent


def extract_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'html_code\s*=\s*"""(.*?)"""', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

# --- Trích xuất phần <style> và <body> từ HTML ---
def split_html(html_str):
    style_match = re.search(r'<style>(.*?)</style>', html_str, re.DOTALL)
    body_match = re.search(r'<body>(.*?)</body>', html_str, re.DOTALL)
    style = style_match.group(1) if style_match else ''
    body  = body_match.group(1) if body_match else ''
    return style.strip(), body.strip()


APP_FONT_CSS = """
@font-face {
  font-family: 'Pacifico';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/pacifico/v23/FwZY7-Qmy14u9lezJ-6I6MmBp0u-zK4.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
@font-face {
  font-family: 'Pacifico';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/pacifico/v23/FwZY7-Qmy14u9lezJ-6H6MmBp0u-.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Work Sans';
  font-style: normal;
  font-weight: 400 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/worksans/v24/QGYsz_wNahGAdqQ43Rh_c6DptfpA4cD3.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
@font-face {
  font-family: 'Work Sans';
  font-style: normal;
  font-weight: 400 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/worksans/v24/QGYsz_wNahGAdqQ43Rh_fKDptfpA4Q.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
:root {
  --foodmind-font: 'Work Sans', 'Be Vietnam Pro', 'Sora', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
body,
button,
input,
textarea,
select,
body *:not(svg):not(path):not(polyline):not(circle):not(line):not(rect):not(polygon) {
  font-family: var(--foodmind-font) !important;
}
"""


def apply_app_font(html_str):
    return html_str.replace('</style>', APP_FONT_CSS + '\n</style>', 1)

# --- Đọc HTML từ các file gốc ---
html_splash   = extract_html(BASE_DIR / "foodmind_app.py")
html_login    = extract_html(BASE_DIR / "foodmind_app1.py")
html_register = extract_html(BASE_DIR / "foodmind_app2.py")
html_home     = extract_html(BASE_DIR / "foodmind_app3.py")
html_budget   = extract_html(BASE_DIR / "foodmind_app4.py")
html_hunger   = extract_html(BASE_DIR / "foodmind_app5.py")
html_diet     = extract_html(BASE_DIR / "foodmind_app6.py")
html_app7     = extract_html(BASE_DIR / "foodmind_app7.py")
html_results  = extract_html(BASE_DIR / "main2.py")
html_map      = extract_html(BASE_DIR / "foodmind_app16.py")

html_files = {
    "foodmind_app.py": html_splash,
    "foodmind_app1.py": html_login,
    "foodmind_app2.py": html_register,
    "foodmind_app3.py": html_home,
    "foodmind_app4.py": html_budget,
    "foodmind_app5.py": html_hunger,
    "foodmind_app6.py": html_diet,
    "foodmind_app7.py": html_app7,
    "main2.py": html_results,
    "foodmind_app16.py": html_map,
}
missing_files = [name for name, content in html_files.items() if not content]

if missing_files:
    st.error("Không thể đọc HTML từ: " + ", ".join(missing_files))
    st.stop()

style_splash,   body_splash   = split_html(html_splash)
style_login,    body_login    = split_html(html_login)
style_register, body_register = split_html(html_register)
style_home,     body_home     = split_html(html_home)
style_budget,   body_budget   = split_html(html_budget)
style_hunger,   body_hunger   = split_html(html_hunger)
style_diet,     body_diet     = split_html(html_diet)
style_app7,     body_app7     = split_html(html_app7)

# --- Chèn dữ liệu thật + Folium map vào html_map (từ foodmind_app16) ---
_MAP_USER_LAT, _MAP_USER_LNG = 10.7614, 106.6686
_map_restaurants = get_nearby_restaurants_for_map(_MAP_USER_LAT, _MAP_USER_LNG)
_fm = _folium.Map(location=[_MAP_USER_LAT, _MAP_USER_LNG], zoom_start=15, control_scale=True, tiles='OpenStreetMap')
_folium.Marker(location=[_MAP_USER_LAT, _MAP_USER_LNG], popup=_folium.Popup("📍 Vị trí của bạn", max_width=200), icon=_folium.Icon(color="blue", icon="home", prefix="fa")).add_to(_fm)
for _r in _map_restaurants:
    _mp = _r.get('top_match', 50)
    _c = 'red' if _mp >= 80 else ('orange' if _mp >= 60 else 'green')
    _ph = f'<div style="font-family:Be Vietnam Pro,sans-serif;min-width:200px;"><b style="font-size:15px;">{_r["name"]}</b><br>⭐ {_r.get("rating",4.0):.1f} | 🏆 {_mp:.0f}% Match<br>📍 Cách {_r.get("distance_str","~1 km")}</div>'
    _folium.Marker(location=[_r['lat'], _r['lng']], popup=_folium.Popup(_ph, max_width=280), icon=_folium.Icon(color=_c, icon="cutlery", prefix="fa"), tooltip=f"{_r['name']} ({_mp:.0f}%)").add_to(_fm)
if _map_restaurants:
    _lats = [_MAP_USER_LAT] + [r['lat'] for r in _map_restaurants]
    _lngs = [_MAP_USER_LNG] + [r['lng'] for r in _map_restaurants]
    _fm.fit_bounds([[min(_lats), min(_lngs)], [max(_lats), max(_lngs)]], padding=[30, 30])
_FOLIUM_HTML = _fm.get_root().render()
_FOLIUM_HTML = _FOLIUM_HTML.replace('</head>', '<meta name="viewport" content="width=device-width, initial-scale=1.0"><style>html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;}.folium-map{width:100%!important;height:100%!important;position:absolute;top:0;left:0;}</style></head>')
_FOLIUM_JS_SAFE = _FOLIUM_HTML.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('</', '<\\/')
_REST_JSON = _json.dumps(_map_restaurants, ensure_ascii=False)
html_map = html_map.replace('RESTAURANTS_JSON_PLACEHOLDER', _REST_JSON)
html_map = html_map.replace('USER_LAT_PLACEHOLDER', str(_MAP_USER_LAT))
html_map = html_map.replace('USER_LNG_PLACEHOLDER', str(_MAP_USER_LNG))
html_map = html_map.replace('FOLIUM_PLACEHOLDER', '`' + _FOLIUM_JS_SAFE + '`')

style_map,      body_map      = split_html(html_map)

# --- Sửa onclick để gọi JavaScript chuyển trang ---
body_splash = body_splash.replace(
    '''onclick="alert('Bắt đầu khám phá!')"''',
    '''onclick="switchToLogin()"'''
)
# Link "Đăng nhập" cạnh "Đã có tài khoản?"
body_splash = body_splash.replace(
    '''<a href="#">Đăng nhập</a>''',
    '''<a href="#" onclick="switchToLogin(); return false;">Đăng nhập</a>'''
)
body_login = body_login.replace(
    '''onclick="alert('Quay lại!')"''',
    '''onclick="switchToSplash()"'''
)
# Tab "Đăng ký" trong màn Login -> chuyển sang Register
body_login = body_login.replace(
    '''onclick="alert('Chuyển tab Đăng ký')"''',
    '''onclick="switchToRegister()"'''
)

# Back button trong màn Register -> quay về Splash
body_register = body_register.replace(
    '''onclick="alert('Quay lại!')"''',
    '''onclick="switchToSplash()"'''
)
# Tab "Đăng nhập" trong màn Register -> chuyển sang Login
body_register = body_register.replace(
    '''onclick="alert('Chuyển tab Đăng nhập')"''',
    '''onclick="switchToLogin()"'''
)

# Thay alert trong script login/register -> chuyển sang Home
body_login = body_login.replace(
    '''alert('Xử lý đăng nhập...')''',
    '''window.switchToHome()'''
)
body_register = body_register.replace(
    '''alert('Xử lý đăng ký...')''',
    '''window.switchToHome()'''
)

# Nút "Tiếp tục" trong màn Home -> chuyển sang Budget (không animation)
body_home = body_home.replace(
    '''onclick="alert('Tiếp tục!')"''',
    '''onclick="switchToBudget()"'''
)

# Nút Back trong màn Home -> quay về Register (không animation)
body_home = body_home.replace(
    '''onclick="goBack()"''',
    '''onclick="switchToRegisterNoAnim()"'''
)

# Sửa selectOption trong Home -> dùng hàm scoped, tránh xung đột toàn cục
body_home = body_home.replace(
    '''onclick="selectOption(this)"''',
    '''onclick="selectHomeOption(this)"'''
)

# Nút Back trong màn Budget -> quay về Home (không animation)
body_budget = body_budget.replace(
    '''onclick="goBack()"''',
    '''onclick="switchToHomeNoAnim()"'''
)

# Nút "Tiếp tục" trong màn Budget -> chuyển sang Hunger (không animation)
body_budget = body_budget.replace(
    '''onclick="alert('Tiếp tục!')"''',
    '''onclick="switchToHunger()"'''
)

# Sửa selectOption trong Budget -> dùng hàm scoped, tránh xung đột toàn cục
body_budget = body_budget.replace(
    '''onclick="selectOption(this)"''',
    '''onclick="selectBudgetOption(this)"'''
)

# Nút Back trong màn Hunger -> quay về Budget (không animation)
body_hunger = body_hunger.replace(
    '''onclick="goBack()"''',
    '''onclick="switchToBudgetNoAnim()"'''
)

# Nút "Tiếp tục" trong màn Hunger -> chuyển sang Diet (không animation)
body_hunger = body_hunger.replace(
    '''onclick="alert('Tiếp tục!')"''',
    '''onclick="switchToDiet()"'''
)

# Nút Back trong màn Diet -> quay về Hunger (không animation)
body_diet = body_diet.replace(
    '''onclick="alert('Quay lại!')"''',
    '''onclick="switchToHungerNoAnim()"'''
)

# Nút "Tiếp tục" trong màn Diet -> chuyển sang App7 (không animation)
body_diet = body_diet.replace(
    '''onclick="alert('Tiếp tục!')"''',
    '''onclick="switchToApp7()"'''
)

# Sửa selectOption trong Diet -> dùng hàm scoped, tránh xung đột toàn cục
body_diet = body_diet.replace(
    '''onclick="selectOption(this)"''',
    '''onclick="selectDietOption(this)"'''
)

# Nút Back trong màn App7 -> quay về Diet (không animation)
body_app7 = body_app7.replace(
    '''onclick="alert('Quay lại!')"''',
    '''onclick="switchToDietNoAnim()"'''
)

# Nút "Khám phá ngay" trong màn App7 -> chuyển sang trang kết quả (không animation)
body_app7 = body_app7.replace(
    '''onclick="alert('Bắt đầu khám phá món ăn!')"''',
    '''onclick="switchToResults()"'''
)

# Sửa toggleActive trong App7 -> dùng hàm scoped, tránh xung đột toàn cục
body_app7 = body_app7.replace(
    '''onclick="toggleActive(this, 'weather')"''',
    '''onclick="selectApp7Weather(this)"'''
)
body_app7 = body_app7.replace(
    '''onclick="toggleActive(this, 'pill')"''',
    '''onclick="selectApp7Pill(this)"'''
)

# --- Gọi API thời tiết thật & chèn ô thông tin vào App7 ---
import requests
try:
    _W_API_KEY = "ac08301614e960cf24bf27409d6a2b9f"
    _W_URL = f"http://api.openweathermap.org/data/2.5/weather?lat=10.7614&lon=106.6686&appid={_W_API_KEY}&units=metric"
    _W_RES = requests.get(_W_URL, timeout=5).json()
    _W_TEMP = int(_W_RES['main']['temp'])
    _W_COND = _W_RES['weather'][0]['description']
    _W_HUM = _W_RES['main']['humidity']
    _W_COND_VI = {'clear sky': 'Trời quang', 'few clouds': 'Ít mây', 'scattered clouds': 'Mây rải rác', 'broken clouds': 'Nhiều mây', 'overcast clouds': 'U ám', 'light rain': 'Mưa nhỏ', 'moderate rain': 'Mưa vừa', 'heavy rain': 'Mưa to', 'thunderstorm': 'Giông bão', 'drizzle': 'Mưa phùn', 'haze': 'Sương mù'}.get(_W_COND, _W_COND)
    _W_HTML = f'<div class="weather-info-box"><span class="weather-temp">{_W_TEMP}°C</span><span class="weather-desc">{_W_COND_VI}</span><span class="weather-hum">💧 {_W_HUM}%</span></div>'
except:
    _W_HTML = '<div class="weather-info-box"><span class="weather-temp">--°C</span><span class="weather-desc">Không có dữ liệu</span></div>'

body_app7 = body_app7.replace(
    '<span class="realtime-tag">Real-time</span>',
    ''
)

# Chèn ô thông tin thời tiết sau section-label
body_app7 = body_app7.replace(
    '</div>\n\n  <div class="weather-grid">',
    '</div>\n' + _W_HTML + '\n\n  <div class="weather-grid">'
)

# --- CSS cho ô thông tin thời tiết ---
_WEATHER_CSS = '''
#screen-app7 .weather-info-box {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #f8f6f2;
  border-radius: 16px;
  padding: 14px 18px;
  margin-bottom: 8px;
}
#screen-app7 .weather-temp {
  font-family: 'Sora', sans-serif;
  font-size: 28px;
  font-weight: 800;
  color: #FF5A1F;
}
#screen-app7 .weather-desc {
  font-size: 14px;
  font-weight: 600;
  color: #555;
}
#screen-app7 .weather-hum {
  font-size: 13px;
  font-weight: 600;
  color: #888;
  margin-left: auto;
}
'''

# ============================================================
# CSS VÀ JS CHO ANIMATION CHUYỂN TRANG
# ============================================================
transition_css = """
/* ===== Animation Transition ===== */
@keyframes sparkBurst {
    0%   { transform: scale(0); opacity: 1; }
    100% { transform: scale(2.5); opacity: 0; }
}
.transition-ring {
    position: absolute;
    top: 50%; left: 50%;
    width: 40px; height: 40px;
    margin-left: -20px; margin-top: -20px;
    border-radius: 50%;
    background: #FF5A1F;
    z-index: 100;
    pointer-events: none;
    animation: sparkBurst 0.55s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    display: none;
}
@keyframes pageSlideIn {
    0%   { opacity: 0; transform: translateY(24px) scale(0.96); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}
.screen.just-entered {
    animation: pageSlideIn 0.4s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
"""

transition_js = """
<script>
(function() {
    var splashScreen   = document.getElementById('screen-splash');
    var loginScreen    = document.getElementById('screen-login');
    var registerScreen = document.getElementById('screen-register');
    var homeScreen     = document.getElementById('screen-home');
    var budgetScreen   = document.getElementById('screen-budget');
    var hungerScreen   = document.getElementById('screen-hunger');
    var dietScreen     = document.getElementById('screen-diet');
    var app7Screen     = document.getElementById('screen-app7');
    var ring           = document.getElementById('transition-ring');
    var isAnimating    = false;

    function animateRing(callback) {
        if (isAnimating) return;
        isAnimating = true;
        ring.style.display = 'block';
        ring.style.animation = 'none';
        ring.offsetHeight;
        ring.style.animation = 'sparkBurst 0.55s cubic-bezier(0.4, 0, 0.2, 1) forwards';

        setTimeout(function() {
            ring.style.display = 'none';
            isAnimating = false;
            if (callback) callback();
        }, 250);
    }

    function switchTo(screenOut, screenIn) {
        animateRing(function() {
            screenOut.classList.remove('active', 'just-entered');
            screenIn.classList.add('active', 'just-entered');
            setTimeout(function() {
                screenIn.classList.remove('just-entered');
            }, 400);
        });
    }

    function switchTab(screenOut, screenIn) {
        if (isAnimating) return;
        // Tắt transition để chuyển màn hình tức thì, không animation
        screenOut.style.transition = 'none';
        screenIn.style.transition = 'none';
        screenOut.classList.remove('active', 'just-entered');
        screenIn.classList.add('active');
        // Force reflow rồi bật lại transition cho các lần chuyển khác
        screenIn.offsetHeight;
        screenOut.style.transition = '';
        screenIn.style.transition = '';
    }

    function getActiveScreen() {
        if (splashScreen.classList.contains('active')) return splashScreen;
        if (loginScreen.classList.contains('active')) return loginScreen;
        if (registerScreen.classList.contains('active')) return registerScreen;
        if (homeScreen.classList.contains('active')) return homeScreen;
        if (budgetScreen.classList.contains('active')) return budgetScreen;
        if (hungerScreen.classList.contains('active')) return hungerScreen;
        if (dietScreen.classList.contains('active')) return dietScreen;
        if (app7Screen.classList.contains('active')) return app7Screen;
        return null;
    }

    window.switchToHunger = function() {
        switchTab(budgetScreen, hungerScreen);
    };

    window.switchToBudget = function() {
        switchTab(homeScreen, budgetScreen);
    };

    window.switchToHome = function() {
        var active = getActiveScreen();
        if (active && active !== homeScreen) {
            switchTo(active, homeScreen);
        }
    };

    window.switchToLogin = function() {
        var active = getActiveScreen();
        if (active === registerScreen) {
            switchTab(registerScreen, loginScreen);
        } else if (active && active !== loginScreen) {
            switchTo(active, loginScreen);
        }
    };

    window.switchToRegister = function() {
        switchTab(loginScreen, registerScreen);
    };

    window.switchToSplash = function() {
        var active = getActiveScreen();
        if (active && active !== splashScreen) {
            switchTo(active, splashScreen);
        }
    };

    window.switchToRegisterNoAnim = function() {
        if (isAnimating) return;
        switchTab(homeScreen, registerScreen);
    };

    window.switchToHomeNoAnim = function() {
        if (isAnimating) return;
        switchTab(budgetScreen, homeScreen);
    };

    window.switchToBudgetNoAnim = function() {
        if (isAnimating) return;
        switchTab(hungerScreen, budgetScreen);
    };

    window.switchToHungerNoAnim = function() {
        if (isAnimating) return;
        switchTab(dietScreen, hungerScreen);
    };

    window.switchToDiet = function() {
        switchTab(hungerScreen, dietScreen);
    };

    window.switchToApp7 = function() {
        switchTab(dietScreen, app7Screen);
    };

    window.switchToDietNoAnim = function() {
        if (isAnimating) return;
        switchTab(app7Screen, dietScreen);
    };

    window.collectPreferences = function() {
        return {
            budget: (window.userBudget) || '30_50k',
            time: (window.userTime) || 'fast',
            hunger: (window.foodmindHunger && window.foodmindHunger.value) || (window.userHunger) || 3.5,
            diet: (window.userDiet) || 'Normal',
            weather: (window.userWeather) || 'Normal',
            cuisine: (window.userCuisine) || 'Việt Nam'
        };
    };

    window.switchToResults = function() {
        var onboardingView = document.getElementById('onboarding-view');
        var resultsView = document.getElementById('results-view');
        var resultFrame = document.getElementById('main2-frame');
        var resultTemplate = document.getElementById('main2-template');

        if (!onboardingView || !resultsView || !resultFrame || !resultTemplate) {
            return;
        }

        var prefs = window.collectPreferences();

        onboardingView.style.display = 'none';
        resultsView.style.display = 'flex';

        resultFrame.addEventListener('load', function() {
            resultFrame.contentWindow.postMessage({
                type: 'foodmind-prefs',
                prefs: prefs
            }, '*');
        });

        resultFrame.srcdoc = resultTemplate.value;

        setTimeout(function() {
            try {
                resultFrame.contentWindow.postMessage({
                    type: 'foodmind-prefs',
                    prefs: prefs
                }, '*');
            } catch(e) {}
        }, 500);
    };

    window.switchToHomeFromResults = function() {
        var onboardingView = document.getElementById('onboarding-view');
        var resultsView = document.getElementById('results-view');

        if (resultsView) resultsView.style.display = 'none';
        if (onboardingView) onboardingView.style.display = 'flex';

        [splashScreen, loginScreen, registerScreen, homeScreen, budgetScreen, hungerScreen, dietScreen, app7Screen].forEach(function(screen) {
            if (screen) screen.classList.remove('active', 'just-entered');
        });
        if (homeScreen) {
            homeScreen.classList.add('active', 'just-entered');
            setTimeout(function() {
                homeScreen.classList.remove('just-entered');
            }, 400);
        }
    };

    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'foodmind-edit-needs') {
            window.switchToHomeFromResults();
        }
    });

    // --- Single-selection radio behavior (scoped per screen) ---
    window.selectHomeOption = function(el) {
        var container = document.getElementById('screen-home');
        container.querySelectorAll('.option-card').forEach(function(card) {
            card.classList.remove('active');
        });
        el.classList.add('active');
        window.userBudget = el.getAttribute('data-budget-key') || '30_50k';
    };

    window.selectBudgetOption = function(el) {
        var container = document.getElementById('screen-budget');
        container.querySelectorAll('.option-card').forEach(function(card) {
            card.classList.remove('active');
        });
        el.classList.add('active');
        window.userTime = el.getAttribute('data-time-key') || 'fast';
    };

    window.selectDietOption = function(el) {
        var container = document.getElementById('screen-diet');
        container.querySelectorAll('.diet-card').forEach(function(card) {
            card.classList.remove('active');
        });
        el.classList.add('active');
        window.userDiet = el.getAttribute('data-diet-key') || 'Normal';
    };

    window.selectApp7Weather = function(el) {
        var container = document.getElementById('screen-app7');
        container.querySelectorAll('.weather-card').forEach(function(card) {
            card.classList.remove('active');
        });
        el.classList.add('active');
        window.userWeather = el.getAttribute('data-weather-key') || 'Normal';
    };

    window.selectApp7Pill = function(el) {
        var container = document.getElementById('screen-app7');
        container.querySelectorAll('.pill').forEach(function(pill) {
            pill.classList.remove('active');
        });
        el.classList.add('active');
        window.userCuisine = el.getAttribute('data-cuisine-key') || 'Việt Nam';
    };
})();
</script>
"""

# ============================================================
# DỰNG TRANG HTML TỔNG HỢP
# ============================================================
combined_html = """<!DOCTYPE html>
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
    overflow: hidden;
}
.app-view {
    width: 100%;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
#results-view {
    display: none;
}
.result-frame {
    width: 100%;
    height: 960px;
    border: 0;
    display: block;
    background: #f2f0eb;
}
.screens-wrapper {
    position: relative;
    width: 390px;
    height: 844px;
}
.screen {
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.4s cubic-bezier(0.22, 0.61, 0.36, 1),
                transform 0.4s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.screen.active {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
}
.screen:not(.active) {
    transform: translateY(28px) scale(0.97);
}
STYLE_SPLASH_PLACEHOLDER
STYLE_LOGIN_PLACEHOLDER
STYLE_REGISTER_PLACEHOLDER
STYLE_HOME_PLACEHOLDER
STYLE_BUDGET_PLACEHOLDER
STYLE_HUNGER_PLACEHOLDER
STYLE_DIET_PLACEHOLDER
STYLE_APP7_PLACEHOLDER
TRANSITION_CSS_PLACEHOLDER
</style>
</head>
<body>

<div class="app-view" id="onboarding-view">
    <div class="screens-wrapper">
        <div class="screen active" id="screen-splash">
BODY_SPLASH_PLACEHOLDER
        </div>
        <div class="screen" id="screen-login">
BODY_LOGIN_PLACEHOLDER
        </div>
        <div class="screen" id="screen-register">
BODY_REGISTER_PLACEHOLDER
        </div>
        <div class="screen" id="screen-home">
BODY_HOME_PLACEHOLDER
        </div>
        <div class="screen" id="screen-budget">
BODY_BUDGET_PLACEHOLDER
        </div>
        <div class="screen" id="screen-hunger">
BODY_HUNGER_PLACEHOLDER
        </div>
        <div class="screen" id="screen-diet">
BODY_DIET_PLACEHOLDER
        </div>
        <div class="screen" id="screen-app7">
BODY_APP7_PLACEHOLDER
        </div>
        <div class="transition-ring" id="transition-ring"></div>
    </div>
</div>

<div class="app-view" id="results-view">
    <iframe class="result-frame" id="main2-frame" title="FoodMind AI Results"></iframe>
</div>
<textarea id="main2-template" hidden>RESULT_HTML_PLACEHOLDER</textarea>

TRANSITION_JS_PLACEHOLDER

</body>
</html>"""

# --- Scope CSS: thêm #screen-splash hoặc #screen-login vào selector ---
def scope_css(css_text, screen_id):
    """Bọc CSS selectors trong scope của screen tương ứng để tránh xung đột."""
    lines = css_text.split('\n')
    scoped_lines = []
    in_at_rule = 0  # depth counter cho @keyframes, @media, etc.
    for line in lines:
        stripped = line.strip()
        # Bỏ qua dòng trống hoặc comment
        if not stripped or stripped.startswith('/*') or stripped.startswith('//'):
            scoped_lines.append(line)
            continue
        # @keyframes, @media - giữ nguyên, track depth
        if stripped.startswith('@'):
            scoped_lines.append(line)
            if '{' in stripped:
                in_at_rule += 1
            continue
        # Đóng block - giảm depth
        if stripped == '}':
            scoped_lines.append(line)
            if in_at_rule > 0:
                in_at_rule -= 1
            continue
        # Trong @keyframes/@media, không scope
        if in_at_rule > 0:
            scoped_lines.append(line)
            continue
        # CSS selector có dấu {
        if '{' in stripped:
            selector_part = stripped.split('{')[0].strip()
            selectors = [s.strip() for s in selector_part.split(',')]
            scoped_selectors = []
            for sel in selectors:
                # Giữ nguyên selector toàn cục (body, html, *)
                if sel in ('body', 'html', '*') or sel.startswith('body ') or sel.startswith('html ') or sel.startswith('* '):
                    scoped_selectors.append(sel)
                else:
                    scoped_selectors.append(f'#{screen_id} {sel}')
            new_selector = ', '.join(scoped_selectors)
            # Giữ nguyên indentation gốc
            indent = line[:len(line) - len(line.lstrip())]
            remaining = stripped.split('{', 1)[1] if '{' in stripped[stripped.index('{'):] else ''
            if remaining.strip():
                scoped_lines.append(indent + new_selector + ' {' + remaining)
            else:
                scoped_lines.append(indent + new_selector + ' {')
        else:
            scoped_lines.append(line)
    return '\n'.join(scoped_lines)


def extract_phone_frame_inner(body_html):
    """Lấy nội dung bên trong .phone-frame để đặt vào phone-frame hiện có của main2."""
    match = re.search(r'^\s*<div class="phone-frame">\s*(.*?)\s*</div>\s*$', body_html, re.DOTALL)
    if not match:
        return body_html

    inner_html = match.group(1).strip()
    # main2 đã có notch ở phone-frame ngoài, bỏ notch trùng để giao diện không bị đè lớp.
    inner_html = re.sub(r'^\s*<div class="notch"></div>\s*', '', inner_html, count=1)
    return inner_html


def prepare_map_css(css_text):
    """Scope CSS của foodmind_app16 để không ảnh hưởng các màn hình và bottom nav hiện tại."""
    css_text = re.sub(r'body\s*\{.*?\}\s*', '', css_text, flags=re.DOTALL)

    bottom_nav_pos = css_text.find('BOTTOM NAV')
    if bottom_nav_pos != -1:
        comment_start = css_text.rfind('/*', 0, bottom_nav_pos)
        if comment_start != -1:
            css_text = css_text[:comment_start].rstrip()

    map_base_css = """
#screen-map {
  display: none;
  position: absolute;
  inset: 0;
  z-index: 50;
  flex-direction: column;
  background-color: #ebe8dc;
  background-image:
    linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
  background-size: 90px 90px;
  background-position: center;
  overflow: hidden;
}
#screen-map .nav-item {
  position: relative;
}
#screen-map .bottom-sheet .view-all,
#screen-map .bottom-sheet .match-badge {
  display: none !important;
}
#screen-map .search-area .filter-btn {
  display: none !important;
}
"""
    return map_base_css + "\n" + scope_css(css_text, 'screen-map')


def remove_home_top_action_icons(results_html):
    """Ẩn cụm icon search/bell ở góc phải màn home trong HTML của main2."""
    hide_top_actions_css = """
#screen-result .top-actions,
#screen-result1 .top-actions {
  display: none !important;
}
#screen-discover .search-box,
#screen-discover .section-header .view-all {
  display: none !important;
}
"""
    return results_html.replace('</style>', hide_top_actions_css + '\n</style>', 1)


def sync_result_tab_indicator(results_html):
    """Đồng bộ active indicator của segmented tabs ngay khi đổi Quán ăn/Món lẻ."""
    sync_helper_js = """
  function syncResultTabIndicator(targetId) {
    const tabState = {
      'screen-result': 0,
      'screen-result1': 1
    };
    const activeIndex = tabState[targetId];
    if (activeIndex === undefined) return;

    ['screen-result', 'screen-result1'].forEach(screenId => {
      const buttons = document.querySelectorAll('#' + screenId + ' .tab-btn');
      buttons.forEach((button, index) => {
        button.classList.toggle('active', index === activeIndex);
        button.classList.toggle('inactive', index !== activeIndex);
      });
    });

    if (targetId === 'screen-result1') {
      document.querySelectorAll('#screen-result1 .needs-filter-fab').forEach(fab => {
        fab.classList.remove('is-visible');
      });
    }
  }
"""
    results_html = results_html.replace(
        "  function switchResultTab(targetId) {\n",
        sync_helper_js + "\n  function switchResultTab(targetId) {\n",
        1
    )
    results_html = results_html.replace(
        "    if (!newScreen || currentScreenId === targetId) return;\n\n    isAnimating = false;",
        "    if (!newScreen || currentScreenId === targetId) return;\n\n    syncResultTabIndicator(targetId);\n    isAnimating = false;",
        1
    )
    return results_html


def add_needs_panel_toggle(results_html):
    """Thêm animation ẩn/hiện summary panel và floating filter button."""
    needs_toggle_css = """
.needs-card.needs-panel-hiding {
  pointer-events: none;
  animation: needsPanelHide 0.26s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
.needs-card.needs-panel-restoring {
  animation: needsPanelShow 0.30s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}
@keyframes needsPanelHide {
  from { opacity: 1; transform: translateY(0) scale(1); }
  to { opacity: 0; transform: translateY(24px) scale(0.94); }
}
@keyframes needsPanelShow {
  from { opacity: 0; transform: translateY(24px) scale(0.94); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.needs-filter-fab {
  position: absolute;
  right: 24px;
  bottom: 104px;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: none;
  background: #1a1a1a;
  color: #fff;
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 45;
  box-shadow: 0 14px 30px rgba(0,0,0,0.24);
  transition: transform 0.18s ease, opacity 0.18s ease;
}
.needs-filter-fab:active {
  transform: scale(0.94);
}
.needs-filter-fab.is-visible {
  display: flex;
  animation: needsFabShow 0.22s ease both;
}
#screen-result1 .needs-filter-fab,
#screen-result1 .needs-filter-fab.is-visible {
  display: none !important;
}
#screen-result1 .needs-card {
  display: none !important;
}
@keyframes needsFabShow {
  from { opacity: 0; transform: translateY(12px) scale(0.86); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
"""
    needs_toggle_js = """
  function getNeedsScreen(el) {
    return el.closest('#screen-result, #screen-result1, #screen-map, .screen-wrapper') || document.querySelector('.phone-frame');
  }

  function ensureNeedsFilterFab(screen) {
    if (screen && screen.id === 'screen-result1') return null;

    let fab = screen.querySelector(':scope > .needs-filter-fab');
    if (fab) return fab;

    fab = document.createElement('button');
    fab.type = 'button';
    fab.className = 'needs-filter-fab';
    fab.setAttribute('aria-label', 'Mở tóm tắt nhu cầu');
    fab.innerHTML = `
      <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="4" y1="6" x2="14" y2="6"></line>
        <line x1="18" y1="6" x2="20" y2="6"></line>
        <circle cx="16" cy="6" r="2"></circle>
        <line x1="4" y1="12" x2="8" y2="12"></line>
        <line x1="12" y1="12" x2="20" y2="12"></line>
        <circle cx="10" cy="12" r="2"></circle>
        <line x1="4" y1="18" x2="13" y2="18"></line>
        <line x1="17" y1="18" x2="20" y2="18"></line>
        <circle cx="15" cy="18" r="2"></circle>
      </svg>`;
    screen.appendChild(fab);

    fab.addEventListener('click', event => {
      event.stopPropagation();
      const needsCard = screen.querySelector('.needs-card');
      if (!needsCard) return;

      fab.classList.remove('is-visible');
      needsCard.style.display = '';
      needsCard.classList.remove('needs-panel-hiding', 'needs-panel-restoring');
      needsCard.offsetHeight;
      needsCard.classList.add('needs-panel-restoring');
      setTimeout(() => needsCard.classList.remove('needs-panel-restoring'), 320);
    });

    return fab;
  }

  function hideNeedsPanel(closeBtn) {
    const needsCard = closeBtn.closest('.needs-card');
    if (!needsCard) return;

    const screen = getNeedsScreen(needsCard);
    const fab = ensureNeedsFilterFab(screen);
    needsCard.classList.remove('needs-panel-restoring', 'needs-panel-hiding');
    needsCard.offsetHeight;
    needsCard.classList.add('needs-panel-hiding');

    setTimeout(() => {
      needsCard.style.display = 'none';
      needsCard.classList.remove('needs-panel-hiding');
      if (fab) fab.classList.add('is-visible');
    }, 270);
  }
"""
    results_html = results_html.replace('</style>', needs_toggle_css + '\n</style>', 1)
    results_html = results_html.replace(
        "  document.addEventListener('click', event => {\n    const editNeedsBtn = event.target.closest('.needs-edit-btn');",
        needs_toggle_js + "\n  document.addEventListener('click', event => {\n    const editNeedsBtn = event.target.closest('.needs-edit-btn');",
        1
    )
    results_html = results_html.replace(
        "    const closeNeedsBtn = event.target.closest('.needs-close-btn');\n"
        "    if (closeNeedsBtn) {\n"
        "      const needsCard = closeNeedsBtn.closest('.needs-card');\n"
        "      if (needsCard) needsCard.style.display = 'none';\n"
        "    }",
        "    const closeNeedsBtn = event.target.closest('.needs-close-btn');\n"
        "    if (closeNeedsBtn) {\n"
        "      hideNeedsPanel(closeNeedsBtn);\n"
        "    }",
        1
    )
    return results_html


def add_map_screen_to_results(results_html, map_style, map_body):
    """Tiêm screen-map vào HTML của main2 và dùng lại switchScreen/bottom-nav sẵn có."""
    map_screen = f"""
<div id="screen-map" class="screen-wrapper">
{extract_phone_frame_inner(map_body)}
</div>
"""
    results_html = results_html.replace('</style>', prepare_map_css(map_style) + '\n</style>', 1)

    phone_frame_close = '</div>\n\n<script>'
    if phone_frame_close in results_html:
        results_html = results_html.replace(phone_frame_close, map_screen + '\n</div>\n\n<script>', 1)

    results_html = results_html.replace(
        "items[0].addEventListener('click', () => switchScreen('screen-result'));   // Tab Home\n"
        "      items[2].addEventListener('click', () => switchScreen('screen-mealplan')); // Tab Lịch trình",
        "items[0].addEventListener('click', () => switchScreen('screen-result'));   // Tab Home\n"
        "      items[1].addEventListener('click', () => switchScreen('screen-map'));      // Tab Bản đồ\n"
        "      items[2].addEventListener('click', () => switchScreen('screen-mealplan')); // Tab Lịch trình"
    )
    return results_html

style_splash   = scope_css(style_splash,   'screen-splash')
style_login    = scope_css(style_login,    'screen-login')
style_register = scope_css(style_register, 'screen-register')
style_home     = scope_css(style_home,     'screen-home')
style_budget   = scope_css(style_budget,   'screen-budget')
style_hunger   = scope_css(style_hunger,   'screen-hunger')
style_diet     = scope_css(style_diet,     'screen-diet')
style_app7     = scope_css(style_app7,     'screen-app7')
style_app7    += _WEATHER_CSS
html_results   = remove_home_top_action_icons(html_results)
html_results   = sync_result_tab_indicator(html_results)
html_results   = add_needs_panel_toggle(html_results)
html_results   = add_map_screen_to_results(html_results, style_map, body_map)
html_results   = apply_app_font(html_results)

# --- Gọi backend fuzzy logic để lấy dữ liệu thật ---
import sys, os, json
sys.path.insert(0, str(BASE_DIR.parent / 'mybackhurt'))
os.chdir(str(BASE_DIR.parent / 'mybackhurt'))
from fuzzylogic import load_data

try:
    import pandas as pd
    _config, _dishes_df, _restaurants_df = load_data()

    # --- Inject window.foodmindConfig ---
    _config_js = {
        'price_membership_fn': _config.get('price_membership_fn', {}),
        'time_membership_fn': _config.get('time_membership_fn', {}),
        'hunger_membership_fn': _config.get('hunger_membership_fn', {}),
        'hunger_to_calorie_map': _config.get('hunger_to_calorie_map', {}),
        'diet_macro_targets': _config.get('diet_macro_targets', {}),
        'weather_food_map': _config.get('weather_food_map', {}),
        'score_weights': _config.get('score_weights', {})
    }

    # --- Inject window.foodmindRawResults (toàn bộ món) ---
    _raw_results = []
    for _, row in _dishes_df.iterrows():
        _rest_match = _restaurants_df[_restaurants_df['restaurant_id'] == row['restaurant_id']]
        _rname = str(_rest_match['name'].values[0]) if len(_rest_match) > 0 else 'Unknown'
        _raw_results.append({
            'dish_id': str(row['dish_id']),
            'dish_name': str(row['name']),
            'restaurant_id': str(row['restaurant_id']),
            'restaurant_name': _rname,
            'price': float(row['price']),
            'calories': float(row['calories']),
            'protein_g': float(row['protein_g']),
            'carb_g': float(row['carb_g']),
            'fat_g': float(row['fat_g']),
            'cuisine_type': str(row.get('cuisine_type', '')),
            'food_category': str(row.get('food_category', '')),
            'rating': float(row.get('rating', 4.0)),
            'order_count': float(row.get('order_count', 100)),
            'is_available': str(row.get('is_available', 'True')).lower() == 'true',
            'image_url': str(row.get('image_url', ''))
        })

    # --- Inject window.foodmindRestaurants ---
    _restaurants_json = []
    for _, row in _restaurants_df.iterrows():
        _restaurants_json.append({
            'restaurant_id': str(row['restaurant_id']),
            'name': str(row['name']),
            'lat': float(row['lat']) if pd.notna(row.get('lat')) else None,
            'lng': float(row['lng']) if pd.notna(row.get('lng')) else None,
            'avg_prep_time': float(row.get('avg_prep_time', 15)) if pd.notna(row.get('avg_prep_time', 15)) else 15,
            'is_open': str(row.get('is_open', 'True')).lower() != 'false',
            'open_hours': str(row.get('open_hours', '00:00-23:59')),
            'cuisine_type': str(row.get('cuisine_type', '')),
            'cover_image_url': str(row.get('cover_image_url', '')),
            'rating': float(row.get('rating', 4.0)),
            'address': str(row.get('address', ''))
        })

    # --- Tạo kế hoạch ăn uống (meal plan) từ dữ liệu thật ---
    from fuzzylogic import get_recommendations, generate_daily_plan
    _default_inputs = {
        'lat': 10.7614, 'lng': 106.6686,
        'budget': '30_50k', 'time': 'fast',
        'hunger': 6.5, 'health_goal': 'Normal',
        'weather': 'Normal', 'cuisine': 'Việt Nam'
    }
    _meal_plan = generate_daily_plan(_default_inputs, _config, _dishes_df, _restaurants_df)
    _meal_plan_json = {}
    _used_dish_ids = []
    for _meal_key, _meal_val in _meal_plan.items():
        _dinfo = _dishes_df[_dishes_df['dish_id'] == _meal_val['dish_id']].iloc[0]
        _used_dish_ids.append(str(_meal_val['dish_id']))
        _mprice = int(_meal_val['price']) if pd.notna(_meal_val.get('price')) else 0
        _mcal = int(float(_dinfo['calories'])) if pd.notna(_dinfo.get('calories')) else 0
        _mprotein = int(float(_dinfo['protein_g'])) if pd.notna(_dinfo.get('protein_g')) else 0
        _mcarbs = int(float(_dinfo['carb_g'])) if pd.notna(_dinfo.get('carb_g')) else 0
        _mfat = int(float(_dinfo['fat_g'])) if pd.notna(_dinfo.get('fat_g')) else 0
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
    # Sinh danh sách thay thế cho mỗi bữa (top 3 alternatives)
    _all_recs = get_recommendations(_default_inputs, _config, _dishes_df, _restaurants_df)
    _meal_alternatives = {'breakfast': [], 'lunch': [], 'dinner': []}
    _meal_type_map = {'Breakfast': 'breakfast', 'Lunch': 'lunch', 'Dinner': 'dinner'}
    for _r in _all_recs:
        if len(_meal_alternatives['breakfast']) >= 3 and len(_meal_alternatives['lunch']) >= 3 and len(_meal_alternatives['dinner']) >= 3:
            break
        _did = str(_r['dish_id'])
        if _did in _used_dish_ids: continue
        _mt = _r.get('meal_type', '')
        _slot = None
        if _mt == 'Snack':
            _slot = 'breakfast'
        elif _mt == 'Full meal':
            _slot = 'lunch'
        else:
            _slot = 'dinner'
        if _slot and len(_meal_alternatives[_slot]) < 3:
            _dinfo2 = _dishes_df[_dishes_df['dish_id'] == _r['dish_id']].iloc[0]
            _meal_alternatives[_slot].append({
                'dish_id': _did,
                'name': str(_r['dish_name']),
                'restaurant_name': str(_r['restaurant_name']),
                'price': int(_r['price']) if pd.notna(_r.get('price')) else 0,
                'calories': int(float(_dinfo2['calories'])) if pd.notna(_dinfo2.get('calories')) else 0,
                'protein': int(float(_dinfo2['protein_g'])) if pd.notna(_dinfo2.get('protein_g')) else 0,
                'carbs': int(float(_dinfo2['carb_g'])) if pd.notna(_dinfo2.get('carb_g')) else 0,
                'fat': int(float(_dinfo2['fat_g'])) if pd.notna(_dinfo2.get('fat_g')) else 0,
                'match_score': _r['match_score']
            })

    # --- Tính toán recommendations cho màn Results ---
    _backend_results = _all_recs[:15]  # Top 15 món đề xuất
    _backend_results_json = []
    for _br in _backend_results:
        _bd = _dishes_df[_dishes_df['dish_id'] == _br['dish_id']].iloc[0]
        _backend_results_json.append({
            'dish_id': str(_br['dish_id']),
            'dish_name': str(_br['dish_name']),
            'restaurant_id': str(_br['restaurant_id']),
            'restaurant_name': str(_br['restaurant_name']),
            'price': int(_br['price']) if pd.notna(_br.get('price')) else 0,
            'calories': int(float(_bd['calories'])) if pd.notna(_bd.get('calories')) else 0,
            'protein_g': int(float(_bd['protein_g'])) if pd.notna(_bd.get('protein_g')) else 0,
            'carb_g': int(float(_bd['carb_g'])) if pd.notna(_bd.get('carb_g')) else 0,
            'fat_g': int(float(_bd['fat_g'])) if pd.notna(_bd.get('fat_g')) else 0,
            'image_url': str(_bd.get('image_url', '')),
            'match_score': _br['match_score'],
            'meal_type': str(_br.get('meal_type', ''))
        })

    # --- Inject tất cả vào HTML ---
    _inject_script = (
        '<script>'
        'window.foodmindConfig = ' + json.dumps(_config_js, ensure_ascii=False) + ';'
        'window.foodmindRawResults = ' + json.dumps(_raw_results, ensure_ascii=False) + ';'
        'window.foodmindRestaurants = ' + json.dumps(_restaurants_json, ensure_ascii=False) + ';'
        'window.foodmindBackendResults = ' + json.dumps(_backend_results_json, ensure_ascii=False) + ';'
        'window.foodmindMealPlan = ' + json.dumps(_meal_plan_json, ensure_ascii=False) + ';'
        'window.foodmindMealAlternatives = ' + json.dumps(_meal_alternatives, ensure_ascii=False) + ';'
        'window.foodmindMealTargets = {calories:1800,protein:120,carbs:250,fat:65};'
        '</script>'
    )
    html_results = html_results.replace('</body>', _inject_script + '\n</body>')
except Exception as _e:
    _inject_script = f'<script>window.foodmindBackendError = "{str(_e)}";</script>'
    html_results = html_results.replace('</body>', _inject_script + '\n</body>')

# --- Chèn nội dung vào placeholder ---
combined_html = combined_html.replace('STYLE_SPLASH_PLACEHOLDER', style_splash)
combined_html = combined_html.replace('STYLE_LOGIN_PLACEHOLDER', style_login)
combined_html = combined_html.replace('STYLE_REGISTER_PLACEHOLDER', style_register)
combined_html = combined_html.replace('STYLE_HOME_PLACEHOLDER', style_home)
combined_html = combined_html.replace('STYLE_BUDGET_PLACEHOLDER', style_budget)
combined_html = combined_html.replace('STYLE_HUNGER_PLACEHOLDER', style_hunger)
combined_html = combined_html.replace('STYLE_DIET_PLACEHOLDER', style_diet)
combined_html = combined_html.replace('STYLE_APP7_PLACEHOLDER', style_app7)
combined_html = combined_html.replace('TRANSITION_CSS_PLACEHOLDER', transition_css)
combined_html = combined_html.replace('BODY_SPLASH_PLACEHOLDER', body_splash)
combined_html = combined_html.replace('BODY_LOGIN_PLACEHOLDER', body_login)
combined_html = combined_html.replace('BODY_REGISTER_PLACEHOLDER', body_register)
combined_html = combined_html.replace('BODY_HOME_PLACEHOLDER', body_home)
combined_html = combined_html.replace('BODY_BUDGET_PLACEHOLDER', body_budget)
combined_html = combined_html.replace('BODY_HUNGER_PLACEHOLDER', body_hunger)
combined_html = combined_html.replace('BODY_DIET_PLACEHOLDER', body_diet)
combined_html = combined_html.replace('BODY_APP7_PLACEHOLDER', body_app7)
combined_html = combined_html.replace('RESULT_HTML_PLACEHOLDER', html.escape(html_results, quote=False))
combined_html = combined_html.replace('TRANSITION_JS_PLACEHOLDER', transition_js)
combined_html = apply_app_font(combined_html)

# --- Render ---
components.html(combined_html, height=960, scrolling=False)
