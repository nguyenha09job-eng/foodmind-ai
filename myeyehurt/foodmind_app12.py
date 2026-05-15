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

  body {
    background: #f2f0eb;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Be Vietnam Pro', sans-serif;
    padding: 24px 0 40px;
  }

  /* Phone Frame */
  .phone-frame {
    width: 390px;
    height: 844px; /* Fixed height for iPhone 16 */
    background: #ffffff;
    border-radius: 48px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.08);
    position: relative;
    padding: 24px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Notch */
  .notch {
    position: absolute;
    top: 14px; left: 50%; transform: translateX(-50%);
    width: 120px; height: 34px;
    background: #1a1a1a;
    border-radius: 20px;
    z-index: 40;
  }

  /* Main Content Wrapper - Centered */
  .content-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-bottom: 80px; /* Space for the bottom button */
  }

  /* Success Icon */
  .success-icon-wrap {
    width: 120px;
    height: 120px;
    background-color: #00C853; /* Bright Green */
    border-radius: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 20px 40px rgba(0, 200, 83, 0.25);
    margin-bottom: 32px;
  }

  /* Typography */
  .main-title {
    font-family: 'Sora', sans-serif;
    font-size: 34px;
    font-weight: 800;
    color: #1a1a1a;
    text-align: center;
    line-height: 1.25;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
  }

  .sub-title {
    font-size: 15px;
    color: #666;
    text-align: center;
    line-height: 1.6;
    margin-bottom: 40px;
    font-weight: 500;
    padding: 0 10px;
  }

  /* Rating Card */
  .rating-card {
    width: 100%;
    background: #FAFAFA;
    border: 1px solid #F0F0F0;
    border-radius: 32px;
    padding: 28px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .rating-title {
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 24px;
  }

  .stars {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
  }

  .star {
    width: 40px;
    height: 40px;
    cursor: pointer;
    transition: transform 0.2s, fill 0.2s, stroke 0.2s;
    fill: none;
    stroke: #D9D9D9;
    stroke-width: 1.5;
  }

  .star:active {
    transform: scale(0.9);
  }

  .star.filled {
    fill: #FFD600; /* Yellow star */
    stroke: #FFD600;
  }

  .rating-hint {
    font-size: 13px;
    font-weight: 700;
    color: #FF5A1F; /* Orange */
  }

  /* Bottom Button */
  .btn-home {
    position: absolute;
    bottom: 40px;
    left: 24px;
    right: 24px;
    background: #1a1a1a;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 20px;
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    transition: transform 0.2s;
  }

  .btn-home:active {
    transform: scale(0.98);
  }

</style>
</head>
<body>
<div class="phone-frame">
  
  <!-- Notch -->
  <div class="notch"></div>

  <!-- Main content centered -->
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
        <!-- SVG Stars -->
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <svg class="star" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
      </div>
      <div class="rating-hint" id="rating-text">Chạm sao để đánh giá</div>
    </div>

  </div>

  <!-- Bottom Home Button -->
  <button class="btn-home" onclick="alert('Đang về trang chủ...')">
    Về trang chủ 
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
      <polyline points="9 22 9 12 15 12 15 22"></polyline>
    </svg>
  </button>

</div>

<script>
  // Logic xử lý click để tô màu đánh giá Sao
  const stars = document.querySelectorAll('.star');
  const ratingText = document.getElementById('rating-text');
  const ratingMessages = ["Rất tệ", "Tệ", "Bình thường", "Tốt", "Tuyệt vời! Cảm ơn bạn"];

  stars.forEach((star, index) => {
    star.addEventListener('click', () => {
      // Đặt lại text hint tùy theo số sao
      ratingText.innerText = ratingMessages[index];
      ratingText.style.color = index >= 3 ? '#00C853' : '#FF5A1F';
      
      // Đổ màu sao
      stars.forEach((s, i) => {
        if (i <= index) {
          s.classList.add('filled');
        } else {
          s.classList.remove('filled');
        }
      });
    });
  });
</script>

</body>
</html>
"""

# Render mã HTML trong Streamlit
components.html(html_code, height=950, scrolling=False)