import streamlit as st
import time
from utils.auth_manager import register_user


def render_register():
    """
    Giao diện đăng ký - Galaxy Theme
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
        background: linear-gradient(135deg, #0f0c29 0%, #1e3a5f 50%, #24243e 100%);
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
            radial-gradient(1px 1px at 90px 40px, white, transparent);
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
        background: linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .main-title p { color: #94a3b8; font-size: 1rem; }
    
    /* Style cho cột trái (ảnh) */
    [data-testid="stHorizontalBlock"] > div:first-child > div {
        background: rgba(20, 30, 50, 0.6);
        border: 2px solid rgba(52, 211, 153, 0.3);
        border-radius: 20px;
        padding: 15px;
    }
    
    /* Style cho cột phải (form) */
    [data-testid="stHorizontalBlock"] > div:last-child > div {
        background: rgba(20, 30, 50, 0.8);
        border: 2px solid rgba(52, 211, 153, 0.3);
        border-radius: 20px;
        padding: 25px;
    }
    
    /* Form Header */
    .form-header {
        text-align: center;
        margin-bottom: 15px;
    }
    .form-header .icon { font-size: 2.5rem; margin-bottom: 10px; }
    .form-header h2 { color: #f1f5f9; font-size: 1.4rem; font-weight: 600; margin-bottom: 5px; }
    .form-header p { color: #94a3b8; font-size: 0.9rem; }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(30, 40, 60, 0.9) !important;
        border: 1px solid rgba(52, 211, 153, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        color: #e2e8f0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #34d399 !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.3) !important;
    }
    
    .stTextInput > label { color: #cbd5e1 !important; font-weight: 500 !important; font-size: 0.9rem !important; }
    
    /* Select box */
    .stSelectbox > div > div {
        background: rgba(30, 40, 60, 0.9) !important;
        border: 1px solid rgba(52, 211, 153, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #34d399, #38bdf8) !important;
        border: none !important;
        color: #0f172a !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    /* Secondary button */
    .stButton > button:not([kind="primary"]) {
        background: rgba(148, 163, 184, 0.2) !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        width: 100% !important;
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
        border-bottom: 1px solid rgba(148, 163, 184, 0.3);
    }
    .divider span { padding: 0 15px; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

    # Main Title
    st.markdown("""
    <div class="main-title">
        <h1>✨ Tạo Tài Khoản</h1>
        <p>Tham gia Digital GDP Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2 Column Layout
    col_img, col_form = st.columns([1, 1.2])
    
    # LEFT: Image
    with col_img:
        try:
            st.image("assets/images/register_badge.png", use_column_width=True)
        except:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <span style="font-size: 5rem;">✨</span>
                <h2 style="color: #34d399; margin-top: 15px;">REGISTER</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # RIGHT: Form
    with col_form:
        st.markdown("""
        <div class="form-header">
            <div class="icon">🎉</div>
            <h2>Đăng ký tài khoản</h2>
            <p>Điền thông tin để tạo tài khoản</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Username", placeholder="Chọn username", key="reg_user")
        password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Tạo mật khẩu", key="reg_pass")
        confirm = st.text_input("🔐 Xác nhận", type="password", placeholder="Nhập lại", key="reg_confirm")
        
        role = st.selectbox("🎭 Vai trò", ["province", "admin"],
            format_func=lambda x: "🏙️ Province" if x == "province" else "👨‍💼 Admin")
        
        if st.button("✨ Đăng ký", type="primary", key="register_submit"):
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
        
        st.markdown('<div class="divider"><span>đã có tài khoản?</span></div>', unsafe_allow_html=True)
        
        if st.button("⬅️ Đăng nhập", key="back_login"):
            st.session_state.page = "login"
            st.rerun()
