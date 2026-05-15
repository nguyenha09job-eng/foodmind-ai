import streamlit as st
import streamlit.components.v1 as components
import html
from pathlib import Path
import re

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

    window.switchToResults = function() {
        var onboardingView = document.getElementById('onboarding-view');
        var resultsView = document.getElementById('results-view');
        var resultFrame = document.getElementById('main2-frame');
        var resultTemplate = document.getElementById('main2-template');

        if (!onboardingView || !resultsView || !resultFrame || !resultTemplate) {
            return;
        }

        onboardingView.style.display = 'none';
        resultsView.style.display = 'flex';

        // Nạp main2.py đúng lúc bấm nút để màn loading/result trong main2 chạy từ đầu.
        resultFrame.srcdoc = resultTemplate.value;
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
    };

    window.selectBudgetOption = function(el) {
        var container = document.getElementById('screen-budget');
        container.querySelectorAll('.option-card').forEach(function(card) {
            card.classList.remove('active');
        });
        el.classList.add('active');
    };

    window.selectDietOption = function(el) {
        var container = document.getElementById('screen-diet');
        container.querySelectorAll('.diet-card').forEach(function(card) {
            card.classList.remove('active');
        });
        el.classList.add('active');
    };

    window.selectApp7Weather = function(el) {
        var container = document.getElementById('screen-app7');
        container.querySelectorAll('.weather-card').forEach(function(card) {
            card.classList.remove('active');
        });
        el.classList.add('active');
    };

    window.selectApp7Pill = function(el) {
        var container = document.getElementById('screen-app7');
        container.querySelectorAll('.pill').forEach(function(pill) {
            pill.classList.remove('active');
        });
        el.classList.add('active');
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
html_results   = remove_home_top_action_icons(html_results)
html_results   = sync_result_tab_indicator(html_results)
html_results   = add_needs_panel_toggle(html_results)
html_results   = add_map_screen_to_results(html_results, style_map, body_map)

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

# --- Render ---
components.html(combined_html, height=960, scrolling=False)
