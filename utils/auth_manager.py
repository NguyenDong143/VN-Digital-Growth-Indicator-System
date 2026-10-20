import warnings
warnings.filterwarnings('ignore')

import re
import bcrypt
import streamlit as st
from datetime import datetime, timedelta
from utils.database import (
    init_db,
    get_user,
    add_user,
    get_all_users,
    register_login_failure,
    reset_login_failures,
)
from config.settings import (
    PASSWORD_MIN_LENGTH,
    LOGIN_MAX_ATTEMPTS,
    LOGIN_LOCKOUT_MINUTES,
)

init_db()


# =========================================================
# PASSWORD POLICY
# =========================================================

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate mật khẩu theo policy nội bộ.

    Rules:
        - Độ dài tối thiểu (PASSWORD_MIN_LENGTH).
        - Có ít nhất 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 ký tự đặc biệt.

    Returns
    -------
    (ok, message)
    """
    if not password or len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Mật khẩu phải có ít nhất {PASSWORD_MIN_LENGTH} ký tự."
    if not re.search(r"[A-Z]", password):
        return False, "Cần ít nhất 1 chữ cái in hoa."
    if not re.search(r"[a-z]", password):
        return False, "Cần ít nhất 1 chữ cái in thường."
    if not re.search(r"\d", password):
        return False, "Cần ít nhất 1 chữ số."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\;'/`~]", password):
        return False, "Cần ít nhất 1 ký tự đặc biệt."
    return True, ""


# =========================================================
# RATE LIMITING (persisted in SQLite)
# =========================================================

def _is_locked_out(user: dict) -> tuple[bool, int]:
    """
    Check nếu user đang bị lockout do nhập sai quá nhiều lần.

    Returns
    -------
    (is_locked, minutes_remaining)
    """
    last_failed = user.get("last_failed_at")
    failed_count = user.get("failed_attempts", 0) or 0
    if not last_failed or failed_count < LOGIN_MAX_ATTEMPTS:
        return False, 0
    try:
        last_dt = datetime.fromisoformat(last_failed)
    except (TypeError, ValueError):
        return False, 0
    elapsed = datetime.now() - last_dt
    if elapsed < timedelta(minutes=LOGIN_LOCKOUT_MINUTES):
        remaining = LOGIN_LOCKOUT_MINUTES - int(elapsed.total_seconds() // 60)
        return True, max(1, remaining)
    return False, 0


def load_users():
    """Get list of all users from database."""
    return get_all_users()


def save_user(username: str, password: str, role: str = "province") -> bool:
    """
    Save a new user to the database (password is hashed + validated).
    Returns False if username already exists.
    Raises ValueError nếu mật khẩu yếu.
    """
    is_strong, msg = validate_password_strength(password)
    if not is_strong:
        raise ValueError(f"Password yếu: {msg}")
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return add_user(username, hashed_pw, role)


def verify_user(username: str, password: str):
    """
    Verify username and password, return role if valid.
    Side-effect: cập nhật failed_attempts và last_failed_at trong DB.
    """
    user = get_user(username)
    if user is None:
        return None
    locked, _mins = _is_locked_out(user)
    if locked:
        return None
    stored_pw = user["password"].encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), stored_pw):
        reset_login_failures(username)
        return user["role"]
    register_login_failure(username)
    return None


def login_user(username: str, password: str):
    """Xử lý đăng nhập với rate-limit."""
    if not username or not password:
        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
        return
    user = get_user(username)
    if user is not None:
        locked, mins = _is_locked_out(user)
        if locked:
            st.error(
                f"🔒 Tài khoản tạm thời bị khóa {mins} phút do nhập sai "
                f"{LOGIN_MAX_ATTEMPTS} lần liên tiếp."
            )
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
    """Xử lý đăng ký với password policy."""
    if not username or not password or not confirm_pw:
        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")
        return
    if password != confirm_pw:
        st.error("❌ Mật khẩu không khớp.")
        return
    is_strong, msg = validate_password_strength(password)
    if not is_strong:
        st.error(f"❌ {msg}")
        return
    try:
        success = save_user(username, password, role)
    except ValueError as e:
        st.error(f"❌ {e}")
        return
    if success:
        st.success("✅ Tạo tài khoản thành công! Vui lòng đăng nhập.")
        st.session_state.page = "login"
        st.rerun()
    else:
        st.error("⚠️ Tên đăng nhập đã tồn tại.")


def logout():
    """Đăng xuất và làm sạch session"""
    if st.sidebar.button("🚪 Đăng xuất"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.sidebar.success("✅ Đã đăng xuất.")
        st.rerun()
