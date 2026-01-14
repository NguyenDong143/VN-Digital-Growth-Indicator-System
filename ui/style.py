import streamlit as st

def apply_dark_theme():
    """
    Final Dark Theme (Centered Balanced Glow Edition)
    - Nền gradient lam–đen đều và sang
    - Metric card bo tròn, sáng lam, hover glow
    - Chart Plotly nằm CHÍNH GIỮA khung sáng, viền đều 4 cạnh
    - Sidebar, table, button, input đồng bộ tông tối cao cấp
    """
    st.markdown("""
        <style>
        /* =========================================
           GLOBAL PAGE SETTINGS
        ========================================= */
        .stApp {
            background: linear-gradient(145deg, #0f172a, #1e293b);
            color: #e2e8f0;
            font-family: "Segoe UI", sans-serif;
        }

        /* =========================================
           HEADINGS
        ========================================= */
        h1, h2, h3, h4, h5, h6 {
            color: #38bdf8 !important;
            font-weight: 600;
        }

        /* =========================================
           SIDEBAR
        ========================================= */
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

        /* =========================================
           METRIC BOXES – GLOW CARDS
        ========================================= */
        div[data-testid="stMetric"] {
            background: linear-gradient(160deg, #1e293b, #111827) !important;
            border-radius: 14px !important;
            padding: 16px 12px !important;
            margin: 8px 0 !important;
            text-align: center !important;
            border: 1px solid rgba(56, 189, 248, 0.15);
            box-shadow:
                inset 0 0 8px rgba(56,189,248,0.08),
                0 0 14px rgba(56,189,248,0.12);
            transition: all 0.25s ease-in-out;
        }
        div[data-testid="stMetric"]:hover {
            box-shadow:
                inset 0 0 10px rgba(56,189,248,0.12),
                0 0 22px rgba(56,189,248,0.35);
            transform: translateY(-3px);
        }

        /* Metric Text */
        div[data-testid="stMetricLabel"] {
            color: #cbd5e1 !important;
            font-size: 0.9em !important;
            margin-bottom: 4px !important;
        }
        div[data-testid="stMetricValue"] {
            color: #38bdf8 !important;
            font-size: 1.6em !important;
            font-weight: 600 !important;
        }
        div[data-testid="stMetricDelta"] {
            font-size: 0.85em !important;
            font-weight: 500 !important;
        }

        /* Delta: Up / Down */
        [data-testid="stMetricDelta"][style*="color: rgb(0, 200, 0)"] {
            background-color: rgba(34,197,94,0.15) !important;
            color: #4ade80 !important;
            border-radius: 6px;
            padding: 3px 6px;
        }
        [data-testid="stMetricDelta"][style*="color: rgb(255, 75, 75)"] {
            background-color: rgba(239,68,68,0.15) !important;
            color: #f87171 !important;
            border-radius: 6px;
            padding: 3px 6px;
        }

        /* =========================================
           CHART CONTAINERS – CENTERED BALANCED GLOW
        ========================================= */
        .plotly-graph-div, .stPlotlyChart {
            background: radial-gradient(circle at 50% 50%, #18243e, #0f172a) !important;
            border-radius: 18px !important;

            padding: 28px 28px 24px 28px !important;
            margin: 18px auto 28px auto !important;

            border: 1px solid rgba(56, 189, 248, 0.12);
            box-shadow:
                inset 0 0 10px rgba(56, 189, 248, 0.08),
                0 0 14px rgba(56, 189, 248, 0.14),
                0 4px 10px rgba(0, 0, 0, 0.4);

            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;

            overflow: hidden !important;
            transition: all 0.35s ease-in-out;
        }

        .stPlotlyChart:hover {
            transform: translateY(-3px);
            box-shadow:
                inset 0 0 12px rgba(56, 189, 248, 0.12),
                0 0 26px rgba(56, 189, 248, 0.28),
                0 6px 16px rgba(0, 0, 0, 0.55) !important;
            border-color: rgba(56, 189, 248, 0.18);
        }

        /* Căn giữa nội dung Plotly thật */
        .js-plotly-plot {
            margin: 0 auto !important;
            width: 100% !important;
            max-width: 96% !important;
        }
        .plotly {
            border-radius: 14px !important;
        }
        .plotly .main-svg {
            display: block !important;
            margin: 0 auto !important;
            padding: 0 !important;
        }

        /* =========================================
           TABLES
        ========================================= */
        .stDataFrame, .stTable {
            background-color: #1e293b !important;
            color: #e2e8f0 !important;
            border-radius: 10px !important;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.1) !important;
        }

        /* =========================================
           BUTTONS
        ========================================= */
        .stButton>button {
            background-color: #38bdf8 !important;
            color: #0f172a !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            transition: 0.3s ease-in-out !important;
        }
        .stButton>button:hover {
            background-color: #0ea5e9 !important;
            color: white !important;
        }

        /* =========================================
           INPUTS / FORMS
        ========================================= */
        input, textarea, select {
            background-color: #1e293b !important;
            color: #e2e8f0 !important;
            border-radius: 6px !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }

        /* =========================================
           GENERAL TEXT
        ========================================= */
        .stText, .stMarkdown, p, span, label {
            color: #e2e8f0 !important;
        }

        /* =========================================
           FOOTER / HEADER CLEANUP
        ========================================= */
        footer, #MainMenu {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)
