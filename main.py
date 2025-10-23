import streamlit as st
from config.settings import PAGE_CONFIG
from ui import (
    overview_tab,
    components_tab,
    roi_tab,
    regression_tab,
    input_tab,
    admin_tab,
    style
)
from utils.auth_manager import login_or_register, logout

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(**PAGE_CONFIG)
# style.apply_dark_theme()

# =========================================================
# LOGIN / REGISTER
# =========================================================
login_or_register()

if "user" not in st.session_state:
    st.stop()

role = st.session_state["role"]

# =========================================================
# SIDEBAR MENU
# =========================================================
st.sidebar.title("📘 Digital GDP Dashboard")

if role == "admin":
    menu = st.sidebar.radio(
        "Select Section:",
        [
            "📈 GDP & DTI Overview",
            "🧩 Digital Transformation Pillars",
            "💰 ROI of Digital Investment",
            "📊 Regression Analysis",
            "📋 Admin Data View"
        ]
    )
else:
    menu = st.sidebar.radio("Select Section:", ["📝 Input Provincial Indicators"])

logout()

# =========================================================
# PAGE ROUTING
# =========================================================
if menu == "📈 GDP & DTI Overview":
    overview_tab.render()
elif menu == "🧩 Digital Transformation Pillars":
    components_tab.render()
elif menu == "💰 ROI of Digital Investment":
    roi_tab.render()
elif menu == "📊 Regression Analysis":
    regression_tab.render()
elif menu == "📋 Admin Data View":
    admin_tab.render()
elif menu == "📝 Input Provincial Indicators":
    input_tab.render()
