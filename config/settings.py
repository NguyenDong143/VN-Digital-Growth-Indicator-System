"""
Configuration file for the Digital GDP Dashboard.
Contains page settings, theme colors, data paths, and security.
"""

import os

# =========================================================
# STREAMLIT PAGE SETTINGS
# =========================================================
PAGE_CONFIG = {
    "page_title": "Vietnam Digital Transformation & GDP Growth",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# =========================================================
# THEME COLORS
# =========================================================
THEME = {
    "background_color": "#0f172a",
    "text_color": "white",
    "accent_color": "#38bdf8",
}

# =========================================================
# SECURITY CONFIGURATION
# =========================================================
# Admin secret phải được set qua env var. Nếu không có, admin self-registration bị disable.
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "")
if not ADMIN_SECRET:
    import warnings
    warnings.warn(
        "ADMIN_SECRET not set in environment. Admin self-registration will be disabled. "
        "Set ADMIN_SECRET=<a-strong-passphrase> in .env or system env.",
        RuntimeWarning,
    )
PASSWORD_MIN_LENGTH = int(os.environ.get("PASSWORD_MIN_LENGTH", "8"))
LOGIN_MAX_ATTEMPTS = int(os.environ.get("LOGIN_MAX_ATTEMPTS", "5"))
LOGIN_LOCKOUT_MINUTES = int(os.environ.get("LOGIN_LOCKOUT_MINUTES", "15"))
SESSION_TIMEOUT_SECONDS = int(os.environ.get("SESSION_TIMEOUT_SECONDS", "3600"))

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

