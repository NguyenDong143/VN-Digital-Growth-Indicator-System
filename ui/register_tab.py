import streamlit as st
from utils.auth_manager import register_user

def render_register():
    """
    Giao diện đăng ký tài khoản mới (bố cục 2 cột: ảnh + form)
    """
    st.markdown(
        "<h2 style='text-align:center; color:white;'>📝 Đăng ký tài khoản mới</h2>",
        unsafe_allow_html=True
    )
    st.write("")  # khoảng cách nhỏ

    # ============================================================
    # 2 CỘT: ẢNH (TRÁI) — FORM (PHẢI)
    # ============================================================
    col1, _, col2 = st.columns([10, 1, 10])

    # ----------- CỘT TRÁI: ẢNH MINH HỌA -----------
    with col1:
        st.image("data/register.png", use_container_width=True)

    # ----------- CỘT PHẢI: FORM ĐĂNG KÝ -----------
    with col2:
        st.markdown(
            "<h4 style='text-align:center; color:#60a5fa;'>Tạo tài khoản người dùng</h4>",
            unsafe_allow_html=True
        )

        # --- INPUTS ---
        with st.container(border=True):
            username = st.text_input("👤 Tên đăng nhập")
            password = st.text_input("🔑 Mật khẩu", type="password")
            confirm_pw = st.text_input("🔁 Nhập lại mật khẩu", type="password")
            role = st.selectbox("🔧 Vai trò", ["province", "admin"])

            # --- ĐĂNG KÝ ---
            if st.button("🚀 Đăng ký ngay", use_container_width=True, type="primary"):
                register_user(username, password, confirm_pw, role)

        st.markdown("---")

        # --- QUAY LẠI LOGIN ---
        st.markdown(
            "<p style='text-align:center; color:#94a3b8;'>Đã có tài khoản?</p>",
            unsafe_allow_html=True
        )
        if st.button("⬅️ Quay lại đăng nhập", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
