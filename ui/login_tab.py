import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import time
from utils.auth_manager import verify_user


def render_login():
    """
    Giao diện đăng nhập - Enhanced Galaxy Theme
    """
    
    # Custom CSS - Enhanced Version
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide sidebar */
    section[data-testid="stSidebar"] { display: none; }
    header[data-testid="stHeader"] { display: none; }
    
    /* Galaxy Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        overflow: hidden;
    }
    
    /* Animated Stars Layer 1 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 200%; height: 200%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, white, transparent),
            radial-gradient(2px 2px at 60% 70%, white, transparent),
            radial-gradient(1px 1px at 50% 50%, white, transparent),
            radial-gradient(1px 1px at 80% 10%, white, transparent),
            radial-gradient(2px 2px at 90% 60%, rgba(255,255,255,0.9), transparent),
            radial-gradient(1px 1px at 33% 80%, rgba(255,255,255,0.8), transparent),
            radial-gradient(2px 2px at 70% 40%, white, transparent);
        background-size: 200px 200px, 250px 250px, 300px 300px, 350px 350px, 400px 400px, 180px 180px, 220px 220px;
        background-position: 0 0, 40px 60px, 130px 270px, 70px 100px, 150px 50px, 90px 150px, 210px 80px;
        animation: sparkle 120s linear infinite;
        pointer-events: none;
        z-index: 0;
        opacity: 0.6;
    }
    
    /* Animated Stars Layer 2 - Twinkling */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: 
            radial-gradient(1px 1px at 15% 25%, rgba(168, 139, 250, 0.8), transparent),
            radial-gradient(2px 2px at 85% 15%, rgba(192, 132, 252, 0.9), transparent),
            radial-gradient(1px 1px at 45% 85%, rgba(167, 139, 250, 0.7), transparent),
            radial-gradient(1px 1px at 75% 55%, rgba(139, 92, 246, 0.8), transparent);
        background-size: 300px 300px, 400px 400px, 350px 350px, 280px 280px;
        animation: twinkle 6s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes sparkle {
        from { transform: translateY(0); }
        to { transform: translateY(-50%); }
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.8; }
    }
    
    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); }
        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.6); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Main Title */
    .main-title {
        text-align: center;
        padding: 20px 0 25px 0;
        position: relative;
        z-index: 1;
        animation: float 6s ease-in-out infinite;
    }
    
    .main-title h1 {
        background: linear-gradient(135deg, #c084fc 0%, #a78bfa 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 8px;
        text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
        letter-spacing: -0.5px;
    }
    
    .main-title p {
        color: #cbd5e1;
        font-size: 0.95rem;
        font-weight: 400;
    }
    
    /* Container cho columns */
    [data-testid="stHorizontalBlock"] {
        gap: 2rem !important;
        position: relative;
        z-index: 1;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Style cho cột trái (ảnh) */
    [data-testid="stHorizontalBlock"] > div:first-child > div {
        background: rgba(30, 27, 75, 0.4);
        border: 2px solid rgba(139, 92, 246, 0.4);
        border-radius: 24px;
        padding: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 520px;
        width: fit-content;
        margin: 0 auto;
    }
    
    /* Giảm kích thước ảnh login_badge.png */
    [data-testid="stHorizontalBlock"] > div:first-child img {
        max-width: 100% !important;
        max-height: 480px !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    [data-testid="stHorizontalBlock"] > div:first-child > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.3);
        border-color: rgba(139, 92, 246, 0.6);
    }
    
    /* Style cho cột phải (form) */
    [data-testid="stHorizontalBlock"] > div:last-child > div {
        background: rgba(30, 27, 75, 0.6);
        border: 2px solid rgba(139, 92, 246, 0.4);
        border-radius: 24px;
        padding: 30px 35px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.25);
        height: 520px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Form Header */
    .form-header {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .form-header h2 { 
        color: #f1f5f9; 
        font-size: 1.4rem; 
        font-weight: 700; 
        margin-bottom: 6px;
        letter-spacing: -0.3px;
    }
    
    .form-header p { 
        color: #94a3b8; 
        font-size: 0.9rem; 
        line-height: 1.4;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(15, 12, 41, 0.8) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #a78bfa !important;
        background: rgba(15, 12, 41, 0.95) !important;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15), 0 0 20px rgba(139, 92, 246, 0.3) !important;
        transform: translateY(-2px);
    }
    
    .stTextInput > label { 
        color: #cbd5e1 !important; 
        font-weight: 600 !important; 
        font-size: 0.9rem !important;
        margin-bottom: 8px !important;
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #8b5cf6, #a855f7, #c084fc) !important;
        border: none !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        letter-spacing: 0.3px !important;
        margin-bottom: 0 !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.6) !important;
        background: linear-gradient(135deg, #7c3aed, #9333ea, #a855f7) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }
    
    /* Secondary button - Enhanced Gold */
    .stButton > button:not([kind="primary"]) {
        background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706) !important;
        border: none !important;
        color: #1e1b4b !important;
        border-radius: 12px !important;
        padding: 14px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3) !important;
        letter-spacing: 0.3px !important;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(251, 191, 36, 0.5) !important;
        background: linear-gradient(135deg, #f59e0b, #d97706, #b45309) !important;
    }
    
    .stButton > button:not([kind="primary"]):active {
        transform: translateY(0px) !important;
    }
    
    .divider {
        display: flex;
        align-items: center;
        margin: 12px 0;
        color: #64748b;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(148, 163, 184, 0.25);
    }
    .divider span { 
        padding: 0 20px; 
        font-size: 0.85rem; 
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Loading spinner customization */
    .stSpinner > div {
        border-top-color: #a78bfa !important;
    }
    
    /* Alert styling */
    .stAlert {
        background: rgba(30, 27, 75, 0.8) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title h1 { font-size: 1.8rem; }
        .main-title p { font-size: 0.9rem; }
        [data-testid="stHorizontalBlock"] > div:first-child { display: none; }
        [data-testid="stHorizontalBlock"] > div:last-child > div { 
            padding: 25px;
            height: auto;
        }
    }
    
    /* Force columns to display on desktop */
    @media (min-width: 769px) {
        [data-testid="stHorizontalBlock"] > div:first-child,
        [data-testid="stHorizontalBlock"] > div:last-child {
            display: block !important;
            visibility: visible !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Main Title
    st.markdown("""
    <div class="main-title">
        <h1>🚀 Digital Transformation - GDP</h1>
        <p>Hệ thống phân tích tác động của Chuyển đổi số tới tăng trưởng GDP Việt Nam</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2 Column Layout - Ảnh trái bo sát, form phải rộng hơn
    col_img, col_form = st.columns([0.85, 1.15], gap="large")
    
    # LEFT: Image
    with col_img:
        try:
            st.image("assets/images/login_badge.png", use_container_width=True)
        except:
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <div style="
                    width: 240px;
                    height: 240px;
                    margin: 0 auto;
                    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(168, 139, 250, 0.2));
                    border-radius: 25px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 3px solid rgba(139, 92, 246, 0.4);
                    box-shadow: 0 0 40px rgba(139, 92, 246, 0.3);
                ">
                    <svg width="120" height="120" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M2 17L12 22L22 17" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M2 12L12 17L22 12" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <h2 style="color: #a78bfa; margin-top: 20px; font-size: 1.3rem; font-weight: 700;">SECURE ACCESS</h2>
                <p style="color: #94a3b8; margin-top: 8px; font-size: 0.9rem;">Xác thực an toàn</p>
            </div>
            """, unsafe_allow_html=True)
    
    # RIGHT: Form
    with col_form:
        st.markdown("""
        <div class="form-header">
            <h2>Xin chào! 👋</h2>
            <p>Đăng nhập hoặc đăng ký để truy cập hệ thống phân tích GDP</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Tên đăng nhập", placeholder="Nhập tên đăng nhập của bạn", key="login_user")
        password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Nhập mật khẩu", key="login_pass")
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        if st.button("✨ Đăng nhập", type="primary", key="login_btn", use_container_width=True):
            if not username or not password:
                st.error("⚠️ Vui lòng nhập đầy đủ thông tin!")
            else:
                with st.spinner("Đang xác thực..."):
                    time.sleep(0.5)
                    role = verify_user(username, password)
                    if role:
                        st.session_state.authenticated = True
                        st.session_state.user = username
                        st.session_state.role = role
                        st.success("✅ Đăng nhập thành công!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Sai tên đăng nhập hoặc mật khẩu")
        
        st.markdown('<div class="divider"><span>hoặc</span></div>', unsafe_allow_html=True)
        
        if st.button("✨ Đăng ký", key="register_btn", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()