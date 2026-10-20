"""
Configuration file for the Digital GDP Dashboard.
Contains page settings, theme colors, data paths, and security.
Environment variables are resolved in this order:

    1. Real OS environment variables (highest priority — used by Streamlit Cloud)
    2. Values from a local ``.env`` file (development convenience)
    3. Built-in defaults below

This lets you keep secrets out of git while still being able to run the app
locally without exporting variables in every terminal.
"""

import os
from pathlib import Path

# =========================================================
# ENVIRONMENT LOADING
# =========================================================

def _load_dotenv() -> None:
    """
    Load key=value pairs from a ``.env`` file into ``os.environ``.

    Existing environment variables always win — we never overwrite a value
    that is already set, so real deploy-time configuration (e.g. Streamlit
    Cloud secrets) is not clobbered by a stale local file.

    Uses a minimal parser so the project does not depend on an extra package.
    """
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    try:
        content = env_path.read_text(encoding="utf-8")
    except OSError:
        return
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

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

