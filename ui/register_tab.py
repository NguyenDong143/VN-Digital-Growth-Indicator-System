import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import time
from utils.auth_manager import register_user


def render_register():
    """
    Giao diện đăng ký - Optimized Galaxy Theme
    """
    
    # Custom CSS - Optimized
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide sidebar */
    section[data-testid="stSidebar"] { display: none; }
    header[data-testid="stHeader"] { display: none; }
    
    /* Galaxy Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1e3a5f 50%, #24243e 100%);
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
    
    /* Animated Stars Layer 2 */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: 
            radial-gradient(1px 1px at 15% 25%, rgba(52, 211, 153, 0.8), transparent),
            radial-gradient(2px 2px at 85% 15%, rgba(56, 189, 248, 0.9), transparent),
            radial-gradient(1px 1px at 45% 85%, rgba(96, 165, 250, 0.7), transparent),
            radial-gradient(1px 1px at 75% 55%, rgba(52, 211, 153, 0.8), transparent);
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
        background: linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2px;
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
        background: rgba(20, 30, 50, 0.4);
        border: 2px solid rgba(52, 211, 153, 0.4);
        border-radius: 24px;
        padding: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(52, 211, 153, 0.2);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 520px;
        width: fit-content;
        margin: 0 auto;
    }
    
    [data-testid="stHorizontalBlock"] > div:first-child > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(52, 211, 153, 0.3);
        border-color: rgba(52, 211, 153, 0.6);
    }
    
    /* Giảm kích thước ảnh register */
    [data-testid="stHorizontalBlock"] > div:first-child img {
        max-width: 100% !important;
        max-height: 480px !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    /* Style cho cột phải (form) */
    [data-testid="stHorizontalBlock"] > div:last-child > div {
        background: rgba(20, 30, 50, 0.6);
        border: 2px solid rgba(52, 211, 153, 0.4);
        border-radius: 24px;
        padding: 30px 35px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(52, 211, 153, 0.25);
        height: 520px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Form Header */
    .form-header {
        text-align: center;
        margin-bottom: 18px;
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
        background: rgba(15, 20, 41, 0.8) !important;
        border: 2px solid rgba(52, 211, 153, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #34d399 !important;
        background: rgba(15, 20, 41, 0.95) !important;
        box-shadow: 0 0 0 4px rgba(52, 211, 153, 0.15), 0 0 20px rgba(52, 211, 153, 0.3) !important;
        transform: translateY(-2px);
    }
    
    .stTextInput > label { 
        color: #cbd5e1 !important; 
        font-weight: 600 !important; 
        font-size: 0.85rem !important;
        margin-bottom: 6px !important;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        background: rgba(15, 20, 41, 0.8) !important;
        border: 2px solid rgba(52, 211, 153, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #34d399 !important;
        box-shadow: 0 0 0 4px rgba(52, 211, 153, 0.15) !important;
    }
    
    .stSelectbox > label {
        color: #cbd5e1 !important; 
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 6px !important;
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #34d399, #38bdf8, #60a5fa) !important;
        border: none !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(52, 211, 153, 0.4) !important;
        letter-spacing: 0.3px !important;
        margin-bottom: 0 !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(52, 211, 153, 0.6) !important;
        background: linear-gradient(135deg, #10b981, #0ea5e9, #3b82f6) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }
    
    /* Secondary button */
    .stButton > button:not([kind="primary"]) {
        background: rgba(148, 163, 184, 0.15) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.3px !important;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        transform: translateY(-2px) !important;
        background: rgba(148, 163, 184, 0.25) !important;
        box-shadow: 0 8px 25px rgba(148, 163, 184, 0.3) !important;
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
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #34d399 !important;
    }
    
    /* Alert styling */
    .stAlert {
        background: rgba(20, 30, 50, 0.8) !important;
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
    
    /* Force columns display on desktop */
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
        <h1>✨ Tạo Tài Khoản</h1>
        <p>Tham gia Digital GDP Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    col_img, col_form = st.columns([0.85, 1.15], gap="large")
    with col_img:
        try:
            st.image("assets/images/register_badge.png", width="stretch")
        except:
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <div style="
                    width: 240px;
                    height: 240px;
                    margin: 0 auto;
                    background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(56, 189, 248, 0.2));
                    border-radius: 25px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 3px solid rgba(52, 211, 153, 0.4);
                    box-shadow: 0 0 40px rgba(52, 211, 153, 0.3);
                ">
                    <svg width="120" height="120" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M8.5 11C10.7091 11 12.5 9.20914 12.5 7C12.5 4.79086 10.7091 3 8.5 3C6.29086 3 4.5 4.79086 4.5 7C4.5 9.20914 6.29086 11 8.5 11Z" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M20 8V14M17 11H23" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <h2 style="color: #34d399; margin-top: 20px; font-size: 1.3rem; font-weight: 700;">NEW ACCOUNT</h2>
                <p style="color: #94a3b8; margin-top: 8px; font-size: 0.9rem;">Tạo tài khoản mới</p>
            </div>
            """, unsafe_allow_html=True)
    with col_form:
        st.markdown("""
        <div class="form-header">
            <h2>Đăng ký tài khoản 🎉</h2>
            <p>Điền thông tin để tạo tài khoản mới</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Tên đăng nhập", placeholder="Chọn tên đăng nhập", key="reg_user")
        password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Tạo mật khẩu (tối thiểu 4 ký tự)", key="reg_pass")
        confirm = st.text_input("🔐 Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu", key="reg_confirm")
        
        role = st.selectbox("🎭 Vai trò", ["province", "admin"],
            format_func=lambda x: "🏙️ Province" if x == "province" else "👨‍💼 Admin")
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        if st.button("✨ Đăng ký", type="primary", key="register_submit", width="stretch"):
            if not username or not password or not confirm:
                st.error("⚠️ Vui lòng nhập đầy đủ thông tin!")
            elif password != confirm:
                st.error("❌ Mật khẩu không khớp!")
            elif len(password) < 4:
                st.error("⚠️ Mật khẩu phải có ít nhất 4 ký tự!")
            else:
                with st.spinner("Đang tạo tài khoản..."):
                    time.sleep(0.5)
                    success = register_user(username, password, confirm, role)
                    if success != False:
                        st.success("✅ Tạo tài khoản thành công!")
                        time.sleep(0.5)
                        st.session_state.page = "login"
                        st.rerun()
        
        st.markdown('<div class="divider"><span>Đã có tài khoản?</span></div>', unsafe_allow_html=True)
        
        if st.button("⬅️ Quay lại đăng nhập", key="back_login", width="stretch"):
            st.session_state.page = "login"
            st.rerun()