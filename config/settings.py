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
    "GDP": "data/GDP.csv",
    "CQS": "data/CQS.csv",
    "KTS": "data/KTS.csv",
    "XHS": "data/XHS.csv",
    "DTI": "data/DTI.csv",
    "USERS": "data/users.csv",   # Nếu có user management
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

