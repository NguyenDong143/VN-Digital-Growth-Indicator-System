import streamlit as st
import bcrypt
from utils.database import init_db, get_user, add_user, get_all_users

# Initialize database on module load
init_db()


# =========================================================
# Utility Functions
# =========================================================
def load_users():
    """Get list of all users from database."""
    return get_all_users()


def save_user(username: str, password: str, role: str = "province") -> bool:
    """
    Save a new user to the database (password is hashed).
    Returns False if username already exists.
    """
    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return add_user(username, hashed_pw, role)


def verify_user(username: str, password: str):
    """Verify username and password, return role if valid."""
    user = get_user(username)
    if user:
        stored_pw = user["password"].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_pw):
            return user["role"]
    return None


# =========================================================
# LOGIN / REGISTER HANDLERS
# =========================================================
def login_user(username: str, password: str):
    """Xử lý đăng nhập"""
    if not username or not password:
        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
        return

    role = verify_user(username, password)
    if role:
        st.session_state.authenticated = True
        st.session_state.user = username
        st.session_state.role = role
        st.success(f"✅ Đăng nhập thành công! Xin chào, {username} ({role}).")
        st.rerun()
    else:
        st.error("❌ Sai tên đăng nhập hoặc mật khẩu.")


def register_user(username: str, password: str, confirm_pw: str, role: str = "province"):
    """Xử lý đăng ký"""
    if not username or not password or not confirm_pw:
        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
        return
    if password != confirm_pw:
        st.error("❌ Mật khẩu không khớp.")
        return

    if save_user(username, password, role):
        st.success("✅ Tạo tài khoản thành công! Vui lòng đăng nhập.")
        st.session_state.page = "login"
        st.rerun()
    else:
        st.error("⚠️ Tên đăng nhập đã tồn tại.")


# =========================================================
# Logout Function
# =========================================================
def logout():
    """Đăng xuất và làm sạch session"""
    if st.sidebar.button("🚪 Đăng xuất"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.sidebar.success("✅ Đã đăng xuất.")
        st.rerun()
