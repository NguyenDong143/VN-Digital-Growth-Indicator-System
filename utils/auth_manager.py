import streamlit as st
import pandas as pd
import bcrypt
from pathlib import Path

USER_FILE = Path("data/users.csv")

# =========================================================
# Utility Functions
# =========================================================
def load_users():
    """Đọc danh sách người dùng, tạo file nếu chưa tồn tại"""
    if not USER_FILE.exists():
        df = pd.DataFrame(columns=["username", "password", "role"])
        df.to_csv(USER_FILE, index=False)
    return pd.read_csv(USER_FILE)


def save_user(username: str, password: str, role: str = "province") -> bool:
    """
    Lưu tài khoản mới vào file CSV (mật khẩu được mã hóa).
    Trả về False nếu username đã tồn tại.
    """
    df = load_users()
    if username in df["username"].values:
        return False  # Username đã tồn tại

    # Mã hóa mật khẩu
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_user = pd.DataFrame([[username, hashed_pw, role]],
                            columns=["username", "password", "role"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True


def verify_user(username: str, password: str):
    """Xác thực username và mật khẩu"""
    df = load_users()
    user = df[df["username"] == username]
    if not user.empty:
        stored_pw = user.iloc[0]["password"].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_pw):
            return user.iloc[0]["role"]
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
