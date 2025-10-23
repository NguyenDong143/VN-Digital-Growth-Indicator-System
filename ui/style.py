import streamlit as st

def apply_dark_theme():
    """
    Apply a custom dark theme for the entire Streamlit dashboard.

    Features:
    ----------
    - Deep navy background (#0f172a)
    - Light text color (#e2e8f0)
    - Accent blue highlight (#38bdf8)
    - Rounded boxes, soft shadows for charts and metrics
    - Clean sidebar with subtle blue headers
    - Hidden Streamlit default footer and menu
    """
    st.markdown("""
        <style>
        /* ===============================
           GLOBAL PAGE SETTINGS
        =============================== */
        .stApp {
            background-color: #0f172a;
            color: #e2e8f0;
            font-family: 'Segoe UI', sans-serif;
        }

        /* ===============================
           HEADINGS
        =============================== */
        h1, h2, h3, h4, h5 {
            color: #38bdf8;
            font-weight: 600;
        }

        /* ===============================
           SIDEBAR
        =============================== */
        section[data-testid="stSidebar"] {
            background-color: #1e293b !important;
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label {
            color: #93c5fd !important;
        }
        div[role="radiogroup"] label span {
            color: #e2e8f0 !important;
        }

        /* ===============================
           METRIC BOXES
        =============================== */
        div[data-testid="stMetricValue"] {
            color: #38bdf8 !important;
            font-size: 1.6em;
            font-weight: 600;
        }
        div[data-testid="stMetricLabel"] {
            color: #cbd5e1 !important;
            font-size: 0.9em;
        }

        /* ===============================
           PLOTLY CHARTS
        =============================== */
        .plotly-graph-div {
            border-radius: 12px;
            background-color: #1e293b;
            padding: 10px;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
        }

        /* ===============================
           TEXT, TABLES, CODE BLOCKS
        =============================== */
        .stText, .stMarkdown, .stDataFrame, .stTable {
            color: #e2e8f0;
        }

        /* ===============================
           BUTTONS
        =============================== */
        button[kind="primary"] {
            background-color: #38bdf8 !important;
            color: black !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
        }
        button[kind="primary"]:hover {
            background-color: #0ea5e9 !important;
            color: white !important;
        }

        /* ===============================
           DATA TABLES
        =============================== */
        .stDataFrame, .stTable {
            background-color: #1e293b;
            border-radius: 10px;
        }

        /* ===============================
           FOOTER / HEADER CLEANUP
        =============================== */
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
