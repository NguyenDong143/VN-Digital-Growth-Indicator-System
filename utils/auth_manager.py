import streamlit as st
import pandas as pd
from pathlib import Path

USER_FILE = Path("data/users.csv")


# -----------------------------
# Utility Functions
# -----------------------------
def load_users():
    if not USER_FILE.exists():
        df = pd.DataFrame(columns=["username", "password", "role"])
        df.to_csv(USER_FILE, index=False)
    return pd.read_csv(USER_FILE)


def save_user(username, password, role="province"):
    df = load_users()
    if username in df["username"].values:
        return False  # Username đã tồn tại
    new_user = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True


# -----------------------------
# Authentication System
# -----------------------------
def login_or_register():
    st.sidebar.subheader("🔐 Account Access")

    mode = st.sidebar.radio("Choose action:", ["Login", "Register"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # ---------------------
    # Login Section
    # ---------------------
    if mode == "Login":
        if st.sidebar.button("Login"):
            df = load_users()
            user = df[(df["username"] == username) & (df["password"] == password)]
            if not user.empty:
                st.session_state["user"] = username
                st.session_state["role"] = user.iloc[0]["role"]
                st.sidebar.success(f"Welcome, {username}!")
            else:
                st.sidebar.error("❌ Invalid username or password.")

    # ---------------------
    # Register Section
    # ---------------------
    elif mode == "Register":
        if st.sidebar.button("Register"):
            if len(username) < 3 or len(password) < 3:
                st.sidebar.warning("⚠️ Username and password must be at least 3 characters.")
            elif save_user(username, password):
                st.sidebar.success("✅ Account created successfully! Please log in again.")
                # Xóa session và reset giao diện → quay lại Login
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            else:
                st.sidebar.error("⚠️ Username already exists.")


def logout():
    """Xóa session và quay về trang đăng nhập"""
    if "user" in st.session_state:
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.sidebar.success("Logged out successfully.")
            st.rerun()
