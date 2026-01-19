import warnings
import os
import sys
import logging

# Tắt tất cả warnings trước khi import bất kỳ thứ gì
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Tắt tất cả logging warnings
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger('streamlit').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger('PIL').setLevel(logging.ERROR)

# Tắt deprecation warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=ImportWarning)
warnings.simplefilter(action='ignore', category=PendingDeprecationWarning)
warnings.simplefilter(action='ignore', category=ResourceWarning)

# Suppress pandas warnings
import pandas as pd
pd.options.mode.chained_assignment = None
pd.set_option('mode.chained_assignment', None)

# Suppress numpy warnings
import numpy as np
np.seterr(all='ignore')

import streamlit as st
from config.settings import PAGE_CONFIG
from ui import (
    overview_tab,
    components_tab,
    regression_tab,
    input_tab,
    admin_tab,
    style
)
from ui.login_tab import render_login
from ui.register_tab import render_register
from utils.auth_manager import logout

# PAGE CONFIGURATION
st.set_page_config(**PAGE_CONFIG)
style.apply_dark_theme()  

# SESSION STATE INIT
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

# LOGIN / REGISTER GIAO DIỆN
if not st.session_state.authenticated:
    if st.session_state.page == "login":
        render_login()
    elif st.session_state.page == "register":
        render_register()
    st.stop()

# NẾU ĐÃ ĐĂNG NHẬP → HIỂN THỊ DASHBOARD
user = st.session_state["user"]
role = st.session_state["role"]

# ---- SIDEBAR ----
# Logo section using base64 to avoid warnings
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo1_base64 = get_base64_image("assets/images/logo 1.png")
logo2_base64 = get_base64_image("assets/images/logo 2.png")

st.sidebar.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; gap: 15px; padding: 10px 0;">
        <img src="data:image/png;base64,{logo1_base64}" width="70" style="border-radius: 8px;">
        <img src="data:image/png;base64,{logo2_base64}" width="70" style="border-radius: 8px;">
    </div>
    <h3 style="text-align: center; margin: 5px 0 10px 0; color: #38bdf8; font-size: 1.1rem;">📘 Vietnam Digital GDP Dashboard</h3>
    <hr style="margin: 5px 0 10px 0; border-color: rgba(56, 189, 248, 0.3);">
    <p style="margin: 3px 0; font-size: 0.9rem;">👤 <strong>User:</strong> {user}</p>
    <p style="margin: 3px 0 8px 0; font-size: 0.9rem;">🎭 <strong>Role:</strong> {role.capitalize()}</p>
    <hr style="margin: 8px 0; border-color: rgba(56, 189, 248, 0.3);">
""", unsafe_allow_html=True)

# ---- INIT MENU STATE ----
if "current_menu" not in st.session_state:
    if role == "admin":
        st.session_state.current_menu = "📈 GDP & DTI Overview"
    else:
        st.session_state.current_menu = "📝 Input Provincial Indicators"

# ---- SIDEBAR BUTTON STYLE ----
st.sidebar.markdown("""
<style>
/* Compact sidebar spacing */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem !important;
}
section[data-testid="stSidebar"] .element-container {
    margin-bottom: 0.2rem !important;
}
section[data-testid="stSidebar"] .stButton button {
    padding: 6px 10px !important;
    margin: 2px 0 !important;
    font-size: 0.9rem !important;
}
section[data-testid="stSidebar"] hr {
    margin: 5px 0 !important;
}

/* Button styling */
.sidebar-btn {
    display: block;
    width: 100%;
    padding: 6px 10px;
    margin: 2px 0;
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 8px;
    color: #e2e8f0;
    font-size: 0.9rem;
    text-align: left;
    cursor: pointer;
    transition: all 0.3s ease;
}
.sidebar-btn:hover {
    background: linear-gradient(145deg, rgba(56, 189, 248, 0.2), rgba(30, 41, 59, 0.9));
    border-color: rgba(56, 189, 248, 0.5);
    transform: translateX(4px);
}
.sidebar-btn.active {
    background: linear-gradient(145deg, rgba(56, 189, 248, 0.3), rgba(30, 41, 59, 0.95));
    border-color: #38bdf8;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
}
</style>
""", unsafe_allow_html=True)

# ---- MENU BUTTONS ----

if role == "admin":
    if st.sidebar.button("📈 GDP & DTI Overview", key="btn_overview", width="stretch"):
        st.session_state.current_menu = "📈 GDP & DTI Overview"
        st.rerun()
    if st.sidebar.button("🧩 Digital Transformation Pillars", key="btn_pillars", width="stretch"):
        st.session_state.current_menu = "🧩 Digital Transformation Pillars"
        st.rerun()
    if st.sidebar.button("📋 Admin Data View", key="btn_admin", width="stretch"):
        st.session_state.current_menu = "📋 Admin Data View"
        st.rerun()
else:
    if st.sidebar.button("📝 Input Provincial Indicators", key="btn_input", width="stretch"):
        st.session_state.current_menu = "📝 Input Provincial Indicators"
        st.rerun()

st.sidebar.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

# ---- LOGOUT ----
logout()

# PAGE ROUTING
menu = st.session_state.current_menu

if menu == "📈 GDP & DTI Overview":
    overview_tab.render()
elif menu == "🧩 Digital Transformation Pillars":
    components_tab.render()
elif menu == "📊 Regression Analysis":
    regression_tab.render()
elif menu == "📋 Admin Data View":
    admin_tab.render()
elif menu == "📝 Input Provincial Indicators":
    input_tab.render()

# FOOTER
st.markdown("<hr style='border: 1px solid #1e293b;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#94a3b8;'>© 2025 Vietnam Digital Transformation & GDP Dashboard</p>",
    unsafe_allow_html=True,
)

