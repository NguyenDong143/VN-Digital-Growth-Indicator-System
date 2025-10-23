"""
Configuration file for the Digital GDP Dashboard.
Contains page settings, theme colors, and data path.
"""

# =========================================================
# STREAMLIT PAGE SETTINGS
# =========================================================
PAGE_CONFIG = {
    "page_title": "Vietnam Digital Transformation & GDP Growth",
    "layout": "wide",
    "initial_sidebar_state": "expanded"  # 🔹 Sidebar luôn mở mặc định
}

# =========================================================
# THEME COLORS
# =========================================================
THEME = {
    "background_color": "#0f172a",  # Dark navy background
    "text_color": "white",          # Light text for contrast
    "accent_color": "#38bdf8"       # Bright blue accent
}

# =========================================================
# DATA CONFIGURATION
# =========================================================
DATA_PATH = "data/vietnam_dti_gdp.csv"
