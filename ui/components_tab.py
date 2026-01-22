import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config.settings import DATA_PATHS
from models.regression_model import run_regression


def render():
    """
    Digital Transformation Pillars - Premium Dark Theme UI
    Hiển thị 3 trụ cột chuyển đổi số: CQS, KTS, XHS và tổng hợp DTI
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .pillars-header {
        text-align: center;
        padding: 20px 0 30px;
        animation: fadeIn 0.8s ease-out;
    }
    
    .pillars-header h1 {
        background: linear-gradient(135deg, #a78bfa 0%, #38bdf8 50%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: -0.02em;
    }
    
    .pillars-header p {
        color: #cbd5e1;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Premium Pillar Cards */
    .pillar-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 20px;
        padding: 28px;
        margin: 10px 0;
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .pillar-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
        border-color: rgba(148, 163, 184, 0.25);
    }
    
    .pillar-icon-wrapper {
        width: 56px;
        height: 56px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
        font-size: 1.6rem;
    }
    
    .pillar-icon-wrapper.cqs { background: rgba(96, 165, 250, 0.15); }
    .pillar-icon-wrapper.kts { background: rgba(52, 211, 153, 0.15); }
    .pillar-icon-wrapper.xhs { background: rgba(251, 191, 36, 0.15); }
    .pillar-icon-wrapper.dti { background: rgba(167, 139, 250, 0.15); }
    
    .pillar-title {
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 8px;
        color: #e2e8f0;
        letter-spacing: 0.01em;
    }
    
    .pillar-code {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .pillar-value {
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    
    .pillar-delta {
        font-size: 0.85rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-top: 12px;
    }
    
    .delta-positive { 
        background: rgba(52, 211, 153, 0.15); 
        color: #34d399; 
    }
    .delta-negative { 
        background: rgba(248, 113, 113, 0.15); 
        color: #f87171; 
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 10px 0 20px 0;
        padding: 12px 0;
    }
    
    .section-header h3 {
        color: #f1f5f9;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.01em;
    }
    
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.25), transparent);
        margin: 40px 0;
    }
    
    /* Insight Box */
    .insight-box {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6));
        border-left: 4px solid #38bdf8;
        border-radius: 0 16px 16px 0;
        padding: 24px 28px;
        margin: 15px 0;
    }
    
    .insight-box h4 {
        color: #38bdf8;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 16px;
    }
    
    .insight-box ul {
        color: #e2e8f0;
        line-height: 2;
        font-size: 0.95rem;
        padding-left: 20px;
    }
    
    .insight-box li {
        margin-bottom: 8px;
    }
    
    /* Summary Cards */
    .summary-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 18px;
        padding: 28px;
        margin: 12px 0;
        border: 1px solid rgba(167, 139, 250, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
    
    .summary-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35), 0 0 30px rgba(167, 139, 250, 0.15);
        border-color: rgba(167, 139, 250, 0.4);
    }
    
    .summary-label {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 8px;
        letter-spacing: 0.02em;
    }
    
    .summary-value {
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .summary-sublabel {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 6px;
        font-weight: 500;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pillars-header">
        <h1>🧩 Ba Trụ Cột Chuyển Đổi Số</h1>
        <p>Phân tích chi tiết CQS (Chính quyền số), KTS (Kinh tế số), XHS (Xã hội số)</p>
    </div>
    """, unsafe_allow_html=True)

    gdp = pd.read_csv(DATA_PATHS["GDP"])
    cqs = pd.read_csv(DATA_PATHS["CQS"])
    kts = pd.read_csv(DATA_PATHS["KTS"])
    xhs = pd.read_csv(DATA_PATHS["XHS"])
    dti = pd.read_csv(DATA_PATHS["DTI"])

    # Aggregate by Year
    gdp = gdp.groupby("Year", as_index=False)["GDP"].sum()
    cqs = cqs.groupby("Year", as_index=False)["CQS"].mean()
    kts = kts.groupby("Year", as_index=False)["KTS"].mean()
    xhs = xhs.groupby("Year", as_index=False)["XHS"].mean()
    dti = dti.groupby("Year", as_index=False)["DTI"].mean()

    df = gdp.merge(cqs, on="Year").merge(kts, on="Year").merge(xhs, on="Year").merge(dti, on="Year")


    latest_year = df["Year"].max()
    prev_year = latest_year - 1
    
    latest = df[df["Year"] == latest_year].iloc[0]
    prev = df[df["Year"] == prev_year].iloc[0]
    
    def calc_change(current, previous):
        return ((current - previous) / previous * 100) if previous != 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    
    pillars_data = [
        {"col": col1, "icon": "🏛️", "name": "Chính quyền số", "code": "CQS", "class": "cqs",
         "value": latest["CQS"], "change": calc_change(latest["CQS"], prev["CQS"]), "color": "#60a5fa"},
        {"col": col2, "icon": "💼", "name": "Kinh tế số", "code": "KTS", "class": "kts",
         "value": latest["KTS"], "change": calc_change(latest["KTS"], prev["KTS"]), "color": "#34d399"},
        {"col": col3, "icon": "🌍", "name": "Xã hội số", "code": "XHS", "class": "xhs",
         "value": latest["XHS"], "change": calc_change(latest["XHS"], prev["XHS"]), "color": "#fbbf24"},
        {"col": col4, "icon": "💡", "name": "Chỉ số tổng hợp", "code": "DTI", "class": "dti",
         "value": latest["DTI"], "change": calc_change(latest["DTI"], prev["DTI"]), "color": "#a78bfa"},
    ]
    
    for p in pillars_data:
        with p["col"]:
            delta_class = "delta-positive" if p["change"] >= 0 else "delta-negative"
            delta_sign = "↑ +" if p["change"] >= 0 else "↓ "
            st.markdown(f"""
            <div class="pillar-card" style="border-top: 3px solid {p['color']};">
                <div class="pillar-icon-wrapper {p['class']}">{p['icon']}</div>
                <div class="pillar-title">{p['name']}</div>
                <div class="pillar-code">{p['code']}</div>
                <div class="pillar-value" style="color: {p['color']};">{p['value']:.3f}</div>
                <div class="pillar-delta {delta_class}">{delta_sign}{abs(p['change']):.1f}% vs {prev_year}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
        </svg>
        <h3>Xu hướng phát triển qua các năm</h3>
    </div>
    """, unsafe_allow_html=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["CQS"], name="CQS",
        line=dict(color="#60a5fa", width=3),
        mode="lines+markers",
        marker=dict(size=10, symbol="circle")
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["KTS"], name="KTS",
        line=dict(color="#34d399", width=3),
        mode="lines+markers",
        marker=dict(size=10, symbol="diamond")
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["XHS"], name="XHS",
        line=dict(color="#fbbf24", width=3),
        mode="lines+markers",
        marker=dict(size=10, symbol="square")
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["DTI"], name="DTI (Tổng hợp)",
        line=dict(color="#a78bfa", width=4, dash="dot"),
        mode="lines+markers",
        marker=dict(size=12, symbol="star")
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0", family="Inter", size=13),
        height=420,
        margin=dict(l=50, r=40, t=50, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=13, color="#e2e8f0")
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=14, color="#e2e8f0", weight=500),
            dtick=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
            tickfont=dict(size=12, color="#94a3b8"),
            title=dict(text="Chỉ số", font=dict(size=13, color="#94a3b8"))
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="#38bdf8",
            font=dict(color="#f1f5f9", size=13)
        )
    )
    
    st.plotly_chart(fig, width='stretch')


    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("""
        <div class="section-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
            </svg>
            <h3>So sánh các trụ cột qua các năm</h3>
        </div>
        """, unsafe_allow_html=True)
        
        categories = ["CQS", "KTS", "XHS"]
        

        years_colors = [
            (2021, "#64748b", "rgba(100, 116, 139, 0.1)"),
            (2022, "#fbbf24", "rgba(251, 191, 36, 0.15)"),
            (2023, "#34d399", "rgba(52, 211, 153, 0.2)"),
            (2024, "#38bdf8", "rgba(56, 189, 248, 0.3)")
        ]
        
        fig_radar = go.Figure()
        
        for year, color, fill in years_colors:
            try:
                values = [df[df["Year"] == year][c].values[0] for c in categories]
                fig_radar.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill="toself",
                    name=str(year),
                    line=dict(color=color, width=2),
                    fillcolor=fill
                ))
            except:
                pass
        
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    showticklabels=True,
                    tickfont=dict(color="#94a3b8", size=11),
                    gridcolor="rgba(148, 163, 184, 0.15)"
                ),
                angularaxis=dict(
                    tickfont=dict(color="#e2e8f0", size=14, weight=600),
                    gridcolor="rgba(148, 163, 184, 0.15)"
                )
            ),
            showlegend=True,
            legend=dict(
                x=0.5, y=-0.15, xanchor="center", orientation="h",
                font=dict(size=12, color="#e2e8f0")
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0", family="Inter"),
            height=380,
            margin=dict(l=70, r=70, t=40, b=70)
        )
        
        st.plotly_chart(fig_radar, width='stretch')
    
    with col_right:
        st.markdown(f"""
        <div class="section-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <h3>Tổng kết năm {int(latest_year)}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="summary-card">
            <p class="summary-label" style="text-align: center;">Chỉ số trung bình các trụ cột</p>
            <div style="display: flex; justify-content: space-around; text-align: center; margin-top: 16px;">
                <div style="padding: 12px;">
                    <p class="summary-value" style="color: #60a5fa; font-size: 2.2rem; text-shadow: 0 0 20px rgba(96, 165, 250, 0.4);">{latest['CQS']:.2f}</p>
                    <p class="summary-sublabel">CQS</p>
                </div>
                <div style="padding: 12px;">
                    <p class="summary-value" style="color: #34d399; font-size: 2.2rem; text-shadow: 0 0 20px rgba(52, 211, 153, 0.4);">{latest['KTS']:.2f}</p>
                    <p class="summary-sublabel">KTS</p>
                </div>
                <div style="padding: 12px;">
                    <p class="summary-value" style="color: #fbbf24; font-size: 2.2rem; text-shadow: 0 0 20px rgba(251, 191, 36, 0.4);">{latest['XHS']:.2f}</p>
                    <p class="summary-sublabel">XHS</p>
                </div>
            </div>
        </div>
        
        <div class="summary-card" style="text-align: center;">
            <p class="summary-label">DTI Tổng hợp</p>
            <p class="summary-value" style="color: #a78bfa; font-size: 3.5rem; text-shadow: 0 0 30px rgba(167, 139, 250, 0.5);">{latest['DTI']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
            <circle cx="12" cy="12" r="1"></circle>
            <path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z"></path>
            <path d="M15.5 15.5c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z"></path>
        </svg>
        <h3>Phân tích & Nhận định</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>📌 Điểm nổi bật năm {latest_year}</h4>
        <ul>
            <li><b>DTI tổng hợp</b> đạt <span style="color: #a78bfa; font-weight: 700;">{latest['DTI']:.3f}</span> — 
                tăng <span style="color: #34d399; font-weight: 600;">+{calc_change(latest['DTI'], prev['DTI']):.1f}%</span> so với năm trước</li>
            <li><b>Kinh tế số (KTS)</b> có tốc độ tăng trưởng ấn tượng nhất với 
                <span style="color: #34d399; font-weight: 600;">+{calc_change(latest['KTS'], prev['KTS']):.1f}%</span></li>
            <li><b>Chính quyền số (CQS)</b> và <b>Xã hội số (XHS)</b> phát triển đồng đều, 
                hỗ trợ nền tảng chuyển đổi số quốc gia</li>
            <li>Cả 3 trụ cột đều cho thấy xu hướng <span style="color: #34d399; font-weight: 600;">tăng trưởng tích cực</span> 
                từ 2021 đến {latest_year}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
