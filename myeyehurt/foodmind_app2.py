import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="FoodMind AI - Đăng ký",
    page_icon="🥗",
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

# Đoạn mã HTML/CSS mô phỏng giao diện Đăng ký
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
    padding: 60px 24px 40px;
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

  /* Top Bar */
  .top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32px;
    margin-top: 10px;
  }

  .back-btn {
    width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: flex-start;
    cursor: pointer;
  }

  .brand-header {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .mini-logo {
    width: 28px; height: 28px;
    background: #FF5A1F;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white;
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 16px;
  }

  .brand-text {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: 18px;
    color: #1a1a1a;
  }

  /* Tabs Switcher */
  .auth-tabs {
    background: #f5f5f5;
    border-radius: 16px;
    padding: 4px;
    display: flex;
    margin-bottom: 32px;
  }

  .tab {
    flex: 1;
    text-align: center;
    padding: 12px 0;
    border-radius: 12px;
    font-family: 'Sora', sans-serif;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .tab.active {
    background: white;
    color: #1a1a1a;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  }

  .tab.inactive {
    color: #888;
  }

  /* Welcome Section */
  .welcome-title {
    font-family: 'Sora', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
  }

  .welcome-desc {
    font-size: 15px;
    color: #666;
    line-height: 1.5;
    margin-bottom: 24px; /* Thu gọn chút xíu để đủ chỗ cho 4 ô input */
  }

  /* Form Fields */
  .form-group {
    margin-bottom: 16px; /* Thu gọn margin để fit 4 ô */
  }

  .form-label {
    display: block;
    font-family: 'Sora', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 8px;
  }

  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background: white;
    border: 1.5px solid #eaeaea;
    border-radius: 16px;
    padding: 0 16px;
    height: 56px;
    transition: border-color 0.2s ease;
  }

  .input-wrapper:focus-within {
    border-color: #FF5A1F;
  }

  .input-icon {
    margin-right: 12px;
    display: flex;
    align-items: center;
  }

  .input-field {
    flex: 1;
    height: 100%;
    border: none;
    outline: none;
    font-family: 'Be Vietnam Pro', sans-serif;
    font-size: 15px;
    font-weight: 500;
    color: #1a1a1a;
    background: transparent;
  }

  .input-field::placeholder {
    color: #a0a0a0;
  }

  /* Spacer to push button to bottom */
  .spacer {
    flex: 1;
  }

  /* Submit Button - Orange Version */
  .btn-submit {
    width: 100%;
    background: #FF5A1F; /* Đổi sang màu cam */
    color: white;
    border: none;
    border-radius: 16px;
    padding: 18px;
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: transform 0.15s, box-shadow 0.15s;
    margin-bottom: 16px;
  }

  .btn-submit:hover {
    box-shadow: 0 6px 20px rgba(255,90,31,0.35);
    transform: translateY(-2px);
  }

  .btn-submit:active {
    transform: scale(0.98);
  }

  .form-error {
    color: #e53e3e;
    font-family: 'Be Vietnam Pro', sans-serif;
    font-size: 13px;
    font-weight: 500;
    margin-top: 2px;
    display: none;
  }
</style>
</head>
<body>
<div class="phone-frame">

  <!-- Top Bar -->
  <div class="top-bar">
    <div class="back-btn" onclick="alert('Quay lại!')">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
    </div>
    <div class="brand-header">
      <div class="mini-logo">F</div>
      <div class="brand-text">FoodMind AI</div>
    </div>
    <div style="width: 36px;"></div> <!-- Spacer để cân bằng center -->
  </div>

  <!-- Tabs -->
  <div class="auth-tabs">
    <div class="tab inactive" onclick="alert('Chuyển tab Đăng nhập')">Đăng nhập</div>
    <div class="tab active">Đăng ký</div>
  </div>

  <!-- Welcome -->
  <h1 class="welcome-title">Đăng ký mới 🍱</h1>
  <p class="welcome-desc">Bắt đầu hành trình đặt đồ ăn thông minh hơn</p>

  <!-- Forms -->
  <div class="form-group">
    <label class="form-label">Họ và tên</label>
    <div class="input-wrapper">
      <div class="input-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a0a0a0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </div>
      <input type="text" id="fullname" class="input-field" placeholder="Nguyễn Văn A">
    </div>
  </div>

  <div class="form-group">
    <label class="form-label">Số điện thoại</label>
    <div class="input-wrapper">
      <div class="input-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a0a0a0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
        </svg>
      </div>
      <input type="tel" id="reg-phone" class="input-field" placeholder="09xx xxx xxx">
    </div>
  </div>

  <div class="form-group">
    <label class="form-label">Mật khẩu</label>
    <div class="input-wrapper">
      <div class="input-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a0a0a0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
      </div>
      <input type="password" id="reg-password" class="input-field" placeholder="••••••••">
    </div>
  </div>

  <div class="form-group">
    <label class="form-label">Xác nhận mật khẩu</label>
    <div class="input-wrapper">
      <div class="input-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a0a0a0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
      </div>
      <input type="password" id="reg-confirm" class="input-field" placeholder="••••••••">
    </div>
  </div>

  <div class="form-error" id="register-error">Vui lòng điền đủ thông tin</div>

  <div class="spacer"></div>

  <!-- Bottom Button -->
  <button class="btn-submit" onclick="handleRegister()">
    <span>Tạo tài khoản</span>
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
      <circle cx="12" cy="7" r="4"></circle>
    </svg>
  </button>

</div>

<script>
function handleRegister() {
  var name = document.getElementById('fullname').value.trim();
  var phone = document.getElementById('reg-phone').value.trim();
  var password = document.getElementById('reg-password').value.trim();
  var confirm = document.getElementById('reg-confirm').value.trim();
  var errorEl = document.getElementById('register-error');
  if (!name || !phone || !password || !confirm) {
    errorEl.style.display = 'block';
  } else {
    errorEl.style.display = 'none';
    alert('Xử lý đăng ký...');
  }
}
</script>
</body>
</html>
"""

# Render mã HTML trong Streamlit
components.html(html_code, height=950, scrolling=False)