import streamlit as st
import streamlit.components.v1 as components
import re
from pathlib import Path

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
def extract_html(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    match = re.search(r'html_code = """(.*?)"""\s*\n\s*#\s*Render', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

BASE_DIR = Path(__file__).resolve().parent

# --- Trích xuất phần <style> và <body> từ HTML ---
def split_html(html_str):
    style_match = re.search(r'<style>(.*?)</style>', html_str, re.DOTALL)
    body_match = re.search(r'<body>(.*?)</body>', html_str, re.DOTALL)
    style = style_match.group(1) if style_match else ''
    body  = body_match.group(1) if body_match else ''
    return style.strip(), body.strip()

# --- Đọc HTML từ 6 file gốc ---
html_splash   = extract_html(BASE_DIR / 'foodmind_app.py')
html_login    = extract_html(BASE_DIR / 'foodmind_app1.py')
html_register = extract_html(BASE_DIR / 'foodmind_app2.py')
html_home     = extract_html(BASE_DIR / 'foodmind_app3.py')
html_budget   = extract_html(BASE_DIR / 'foodmind_app4.py')
html_hunger   = extract_html(BASE_DIR / 'foodmind_app5.py')
html_diet     = extract_html(BASE_DIR / 'foodmind_app6.py')
html_app7     = extract_html(BASE_DIR / 'foodmind_app7.py')

if not html_splash or not html_login or not html_register or not html_home or not html_budget or not html_hunger or not html_diet or not html_app7:
    st.error("Không thể đọc file foodmind_app.py, foodmind_app1.py, foodmind_app2.py, foodmind_app3.py, foodmind_app4.py, foodmind_app5.py, foodmind_app6.py hoặc foodmind_app7.py")
    st.stop()

style_splash,   body_splash   = split_html(html_splash)
style_login,    body_login    = split_html(html_login)
style_register, body_register = split_html(html_register)
style_home,     body_home     = split_html(html_home)
style_budget,   body_budget   = split_html(html_budget)
style_hunger,   body_hunger   = split_html(html_hunger)
style_diet,     body_diet     = split_html(html_diet)
style_app7,     body_app7     = split_html(html_app7)

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
        // Redirect đến main2.py bằng cách thay thế 'main' thành 'main2' trong URL
        let currentHref = window.location.href;
        // Xử lý nhiều trường hợp: /main, /main?..., ?script=main, main.py, etc.
        let newHref = currentHref
            .replace(/([/?&])main([/?&#]|$)/, '$1main2$2')
            .replace(/main\\.py/, 'main2.py');
        
        if (newHref !== currentHref) {
            window.location.href = newHref;
        } else {
            // Nếu URL không chứa 'main', thử thêm ?page=main2
            window.location.href = currentHref.split('?')[0] + '?page=main2';
        }
    };

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

style_splash   = scope_css(style_splash,   'screen-splash')
style_login    = scope_css(style_login,    'screen-login')
style_register = scope_css(style_register, 'screen-register')
style_home     = scope_css(style_home,     'screen-home')
style_budget   = scope_css(style_budget,   'screen-budget')
style_hunger   = scope_css(style_hunger,   'screen-hunger')
style_diet     = scope_css(style_diet,     'screen-diet')
style_app7     = scope_css(style_app7,     'screen-app7')

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
combined_html = combined_html.replace('TRANSITION_JS_PLACEHOLDER', transition_js)

# --- Render ---
components.html(combined_html, height=960, scrolling=False)
