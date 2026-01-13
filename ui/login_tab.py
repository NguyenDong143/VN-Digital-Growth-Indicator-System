import streamlit as st
import time
from utils.auth_manager import verify_user


def render_login():
    """
    Giao diện đăng nhập - Galaxy Theme
    """
    
    # Custom CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide sidebar */
    section[data-testid="stSidebar"] { display: none; }
    header[data-testid="stHeader"] { display: none; }
    
    /* Galaxy Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Stars effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: 
            radial-gradient(2px 2px at 20px 30px, white, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, white, transparent),
            radial-gradient(2px 2px at 160px 120px, rgba(255,255,255,0.9), transparent);
        background-repeat: repeat;
        background-size: 250px 150px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main Title */
    .main-title {
        text-align: center;
        padding: 25px 0;
        position: relative;
        z-index: 1;
    }
    
    .main-title h1 {
        background: linear-gradient(135deg, #c084fc 0%, #a78bfa 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .main-title p {
        color: #94a3b8;
        font-size: 1rem;
    }
    
    /* Style cho cột trái (ảnh) */
    [data-testid="stHorizontalBlock"] > div:first-child > div {
        background: rgba(20, 20, 40, 0.6);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 15px;
    }
    
    /* Style cho cột phải (form) */
    [data-testid="stHorizontalBlock"] > div:last-child > div {
        background: rgba(20, 20, 40, 0.8);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 25px;
    }
    
    /* Form Header */
    .form-header {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .form-header .icon { font-size: 2.5rem; margin-bottom: 10px; }
    .form-header h2 { color: #f1f5f9; font-size: 1.4rem; font-weight: 600; margin-bottom: 5px; }
    .form-header p { color: #94a3b8; font-size: 0.9rem; }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(30, 30, 60, 0.9) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        color: #e2e8f0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.3) !important;
    }
    
    .stTextInput > label { color: #cbd5e1 !important; font-weight: 500 !important; }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #8b5cf6, #a855f7) !important;
        border: none !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
    }
    
    /* Secondary button - Gold */
    .stButton > button:not([kind="primary"]) {
        background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
        border: none !important;
        color: #1e1b4b !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    .divider {
        display: flex;
        align-items: center;
        margin: 15px 0;
        color: #64748b;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(148, 163, 184, 0.3);
    }
    .divider span { padding: 0 15px; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

    # Main Title
    st.markdown("""
    <div class="main-title">
        <h1>🚀 Digital GDP Dashboard</h1>
        <p>Hệ thống quản lý và phân tích GDP số</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2 Column Layout
    col_img, col_form = st.columns([1, 1.2])
    
    # LEFT: Image
    with col_img:
        try:
            st.image("assets/images/login_badge.png", width="stretch")
        except:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <span style="font-size: 5rem;">🔐</span>
                <h2 style="color: #a78bfa; margin-top: 15px;">LOGIN</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # RIGHT: Form
    with col_form:
        st.markdown("""
        <div class="form-header">
            <div class="icon">👋</div>
            <h2>Chào mừng trở lại!</h2>
            <p>Đăng nhập để tiếp tục sử dụng hệ thống</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Tên đăng nhập", placeholder="Nhập tên đăng nhập của bạn", key="login_user")
        password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Nhập mật khẩu", key="login_pass")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ Đăng nhập", type="primary", key="login_btn"):
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
        
        if st.button("✨ Tạo tài khoản mới", key="register_btn"):
            st.session_state.page = "register"
            st.rerun()
