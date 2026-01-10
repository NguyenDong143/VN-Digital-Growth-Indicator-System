"""
Configuration file for the Digital GDP Dashboard.
Contains page settings, theme colors, and data paths.
"""

# =========================================================
# STREAMLIT PAGE SETTINGS
# =========================================================
PAGE_CONFIG = {
    "page_title": "Vietnam Digital Transformation & GDP Growth",
    "layout": "wide",
    "initial_sidebar_state": "expanded",  # Sidebar luôn mở mặc định
}

# =========================================================
# THEME COLORS
# =========================================================
THEME = {
    "background_color": "#0f172a",  # Dark navy background
    "text_color": "white",          # Light text for contrast
    "accent_color": "#38bdf8",      # Bright blue accent
}

# =========================================================
# DATA CONFIGURATION
# =========================================================
DATA_PATHS = {
    "GDP": "data/csv/GDP.csv",
    "CQS": "data/csv/CQS.csv",
    "KTS": "data/csv/KTS.csv",
    "XHS": "data/csv/XHS.csv",
    "DTI": "data/csv/DTI.csv",
    "USERS_DB": "data/db/users.db",
    "PROVINCE_DATA": "data/csv/province_data.csv",
}

# =========================================================
# ASSETS CONFIGURATION
# =========================================================
ASSETS_PATHS = {
    "LOGIN_BG": "assets/images/login.png",
    "REGISTER_BG": "assets/images/register.png",
    "LOGIN_BADGE": "assets/images/login_badge.png",
    "REGISTER_BADGE": "assets/images/register_badge.png",
    "GALAXY_BG": "assets/images/galaxy_bg.png",
}

# =========================================================
# DATABASE (tuỳ chọn, dùng nếu có PostgreSQL sau này)
# =========================================================

# =========================================================
# GLOBAL CONSTANTS
# =========================================================
APP_DESCRIPTION = """
This dashboard visualizes the relationship between
Digital Transformation indicators (CQS, KTS, XHS, DTI)
and GDP Growth in Vietnam.
"""

