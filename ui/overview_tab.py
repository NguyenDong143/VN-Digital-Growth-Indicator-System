import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render():
    """
    Trang tổng quan (Overview) - Premium Dark Theme
    """

    # ============================================================
    # CUSTOM CSS
    # ============================================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .overview-header {
        text-align: center;
        padding: 15px 0 25px;
    }
    
    .overview-header h1 {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .overview-header p {
        color: #94a3b8;
        font-size: 1rem;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
        padding: 10px 15px;
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.1) 0%, transparent 100%);
        border-left: 4px solid #38bdf8;
        border-radius: 0 10px 10px 0;
    }
    
    .section-header h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9)) !important;
        border-radius: 12px !important;
        padding: 30px 15px !important;
        margin: 10px 5px !important;
        text-align: center !important;
        border: 1px solid rgba(56, 189, 248, 0.2);
        min-height: 130px !important;
    }
    
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        transform: translateY(-3px);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.85rem !important; }
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; font-size: 1.6rem !important; font-weight: 700 !important; }
    div[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }
    
    .pillar-header {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 15px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .pillar-cqs { background: rgba(96, 165, 250, 0.2); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3); }
    .pillar-dti { background: rgba(167, 139, 250, 0.2); color: #a78bfa; border: 1px solid rgba(167, 139, 250, 0.3); }
    .pillar-kts { background: rgba(52, 211, 153, 0.2); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }
    .pillar-xhs { background: rgba(251, 191, 36, 0.2); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
    
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.3), transparent);
        margin: 25px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ============================================================
    # PAGE HEADER
    # ============================================================
    st.markdown("""
    <div class="overview-header">
        <h1>📊 Tổng quan Tác động Chuyển đổi số tới Tăng trưởng GDP</h1>
        <p>Phân tích dữ liệu GDP và các chỉ số chuyển đổi số theo năm</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # LOAD DATA
    # ============================================================
    gdp_df = pd.read_csv("data/csv/GDP.csv")
    cqs_df = pd.read_csv("data/csv/CQS.csv")
    dti_df = pd.read_csv("data/csv/DTI.csv")
    kts_df = pd.read_csv("data/csv/KTS.csv")
    xhs_df = pd.read_csv("data/csv/XHS.csv")

    for df in [gdp_df, cqs_df, dti_df, kts_df, xhs_df]:
        df["Year"] = df["Year"].astype(int)

    gdp_df = gdp_df.groupby("Year", as_index=False)["GDP"].sum()
    cqs_df = cqs_df.groupby("Year", as_index=False)["CQS"].mean()
    dti_df = dti_df.groupby("Year", as_index=False)["DTI"].mean()
    kts_df = kts_df.groupby("Year", as_index=False)["KTS"].mean()
    xhs_df = xhs_df.groupby("Year", as_index=False)["XHS"].mean()

    # ============================================================
    # LAYOUT: GDP Chart (left) + Key Metrics (right)
    # ============================================================
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("""
        <div class="section-header">
            <span style="font-size: 1.3rem;">💰</span>
            <h3>GDP theo từng năm</h3>
        </div>
        """, unsafe_allow_html=True)
        
        fig_gdp = go.Figure()
        
        fig_gdp.add_trace(go.Bar(
            x=gdp_df["Year"],
            y=gdp_df["GDP"],
            text=[f"{v/1e9:.1f}B" for v in gdp_df["GDP"]],
            textposition="inside",
            textfont=dict(size=11, color="white"),
            marker=dict(
                color=gdp_df["GDP"],
                colorscale=[[0, "#0ea5e9"], [0.5, "#38bdf8"], [1, "#7dd3fc"]],
            )
        ))
        
        fig_gdp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=60, r=40, t=50, b=60),
            height=420,
            xaxis=dict(
                showgrid=False,
                tickmode="array",
                tickvals=gdp_df["Year"].tolist(),
                ticktext=[str(int(y)) for y in gdp_df["Year"]]
            ),
            yaxis=dict(showgrid=True, gridcolor="rgba(56, 189, 248, 0.1)", tickformat=".2s")
        )
        
        st.plotly_chart(fig_gdp, width="stretch")

    with col_right:
        st.markdown("""
        <div class="section-header">
            <span style="font-size: 1.3rem;">🧭</span>
            <h3>Key Metrics – Tác động ước lượng</h3>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            from models.regression_model import run_regression
            
            model_comp = run_regression(model_type="components")
            params_comp = model_comp.params
            
            model_dti = run_regression(model_type="dti")
            dti_coef = model_dti.params.get("DTI", 0)
            
            cqs_coef = params_comp.get("CQS", 0) / 1e9
            kts_coef = params_comp.get("KTS", 0) / 1e9
            xhs_coef = params_comp.get("XHS", 0) / 1e9
            dti_scaled = dti_coef / 1e9
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🏛️ CQS → GDP", f"{cqs_coef:.2f}B", f"{cqs_coef/100:.2f}%")
            with col2:
                st.metric("💼 KTS → GDP", f"{kts_coef:.2f}B", f"{kts_coef/100:.2f}%")

            col3, col4 = st.columns(2)
            with col3:
                st.metric("🌍 XHS → GDP", f"{xhs_coef:.2f}B", f"{xhs_coef/100:.2f}%")
            with col4:
                st.metric("💡 DTI → GDP", f"{dti_scaled:.2f}B", f"{dti_scaled/100:.2f}%")
                
        except Exception as e:
            st.error(f"Không thể tính metrics: {e}")

    # ============================================================
    # DIVIDER
    # ============================================================
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ============================================================
    # 4 PILLARS
    # ============================================================
    st.markdown("""
    <div class="section-header">
        <span style="font-size: 1.3rem;">🧩</span>
        <h3>Các trụ cột Chuyển đổi số theo năm</h3>
    </div>
    """, unsafe_allow_html=True)

    def create_pillar_chart(df, x_col, y_col, color):
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[y_col],
            text=[f"{v:.2f}" for v in df[y_col]],
            textposition="inside",
            textfont=dict(size=10, color="white"),
            marker=dict(color=color, opacity=0.9)
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=50, r=30, t=30, b=50),
            height=280,
            xaxis=dict(
                showgrid=False,
                tickmode="array",
                tickvals=df[x_col].tolist(),
                ticktext=[str(int(y)) for y in df[x_col]],
                tickfont=dict(size=11)
            ),
            yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.1)", tickfont=dict(size=10))
        )
        
        return fig

    col_a, col_b = st.columns(2)
    col_c, col_d = st.columns(2)

    with col_a:
        st.markdown('<span class="pillar-header pillar-cqs">🏛️ CQS (Chính quyền số)</span>', unsafe_allow_html=True)
        st.plotly_chart(create_pillar_chart(cqs_df, "Year", "CQS", "#60a5fa"), width="stretch")

    with col_b:
        st.markdown('<span class="pillar-header pillar-dti">💡 DTI (Chuyển đổi số tổng hợp)</span>', unsafe_allow_html=True)
        st.plotly_chart(create_pillar_chart(dti_df, "Year", "DTI", "#a78bfa"), width="stretch")

    with col_c:
        st.markdown('<span class="pillar-header pillar-kts">💼 KTS (Kinh tế số)</span>', unsafe_allow_html=True)
        st.plotly_chart(create_pillar_chart(kts_df, "Year", "KTS", "#34d399"), width="stretch")

    with col_d:
        st.markdown('<span class="pillar-header pillar-xhs">🌍 XHS (Xã hội số)</span>', unsafe_allow_html=True)
        st.plotly_chart(create_pillar_chart(xhs_df, "Year", "XHS", "#fbbf24"), width="stretch")
