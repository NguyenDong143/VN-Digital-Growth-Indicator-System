import streamlit as st
import time
from utils.auth_manager import verify_user  # dùng hàm xác thực từ CSV

def render_login():
    """
    Giao diện đăng nhập dạng 2 cột:
    - Cột trái: ảnh minh họa
    - Cột phải: form đăng nhập
    """

    st.markdown("<h2 style='text-align:center; color:white;'>🔐 Đăng nhập hệ thống</h2>", unsafe_allow_html=True)
    st.write("")

    # Tạo 2 cột cân đối
    col1, _, col2 = st.columns([10, 1, 10])

    # --- CỘT TRÁI: ẢNH HOẶC VIDEO ---
    with col1:
        st.image("data/login.png", use_container_width=True)

    # --- CỘT PHẢI: FORM LOGIN ---
    with col2:
        st.subheader("Welcome Back 👋")

        username = st.text_input("👤 Tên đăng nhập")
        password = st.text_input("🔑 Mật khẩu", type="password")

        # Nút đăng nhập
        if st.button("Đăng nhập", use_container_width=True):
            time.sleep(1)
            if not (username and password):
                st.error("⚠️ Vui lòng nhập đủ thông tin!")
            else:
                role = verify_user(username, password)
                if role:
                    st.session_state.authenticated = True
                    st.session_state.user = username
                    st.session_state.role = role
                    st.success(f"✅ Đăng nhập thành công! Xin chào, {username}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Sai tên đăng nhập hoặc mật khẩu.")

        # Chuyển sang trang đăng ký
        st.markdown("---")
        if st.button("📝 Chưa có tài khoản? Đăng ký ngay", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
