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
        font-family: 'Inter', sans-serif;
    }
    
    .pillars-header p {
        color: #94a3b8;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .pillar-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        border: 1px solid rgba(148, 163, 184, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .pillar-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .pillar-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .pillar-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    .pillar-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    
    .pillar-delta {
        font-size: 0.9rem;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 8px;
    }
    
    .delta-positive { background: rgba(52, 211, 153, 0.2); color: #34d399; }
    .delta-negative { background: rgba(248, 113, 113, 0.2); color: #f87171; }
    
    .cqs-color { color: #60a5fa; }
    .kts-color { color: #34d399; }
    .xhs-color { color: #fbbf24; }
    .dti-color { color: #a78bfa; }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.3), transparent);
        margin: 35px 0;
    }
    
    .insight-box {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(167, 139, 250, 0.1));
        border-left: 4px solid #38bdf8;
        border-radius: 0 15px 15px 0;
        padding: 20px;
        margin: 15px 0;
    }
    
    .summary-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 16px;
        padding: 25px;
        margin: 10px 0;
        border: 1px solid rgba(167, 139, 250, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .summary-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 30px rgba(167, 139, 250, 0.2);
        border-color: rgba(167, 139, 250, 0.5);
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
        {"col": col1, "icon": "🏛️", "name": "Chính quyền số", "code": "CQS", 
         "value": latest["CQS"], "change": calc_change(latest["CQS"], prev["CQS"]), "color": "#60a5fa"},
        {"col": col2, "icon": "💼", "name": "Kinh tế số", "code": "KTS",
         "value": latest["KTS"], "change": calc_change(latest["KTS"], prev["KTS"]), "color": "#34d399"},
        {"col": col3, "icon": "🌍", "name": "Xã hội số", "code": "XHS",
         "value": latest["XHS"], "change": calc_change(latest["XHS"], prev["XHS"]), "color": "#fbbf24"},
        {"col": col4, "icon": "💡", "name": "Chỉ số tổng hợp", "code": "DTI",
         "value": latest["DTI"], "change": calc_change(latest["DTI"], prev["DTI"]), "color": "#a78bfa"},
    ]
    
    for p in pillars_data:
        with p["col"]:
            delta_class = "delta-positive" if p["change"] >= 0 else "delta-negative"
            delta_sign = "+" if p["change"] >= 0 else ""
            st.markdown(f"""
            <div class="pillar-card" style="border-top: 3px solid {p['color']};">
                <div class="pillar-icon">{p['icon']}</div>
                <div class="pillar-title" style="color: #94a3b8;">{p['name']}</div>
                <div class="pillar-value" style="color: {p['color']};">{p['value']:.3f}</div>
                <div class="pillar-delta {delta_class}">{delta_sign}{p['change']:.1f}% vs {prev_year}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📈 Xu hướng phát triển qua các năm")
    
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
        font=dict(color="white", family="Inter"),
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12),
            dtick=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.1)",
            tickfont=dict(size=11),
            title="Chỉ số"
        ),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, width="stretch")


    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("### 🎯 So sánh các trụ cột qua các năm")
        
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
                    tickfont=dict(color="#94a3b8", size=10),
                    gridcolor="rgba(148, 163, 184, 0.2)"
                ),
                angularaxis=dict(
                    tickfont=dict(color="white", size=12),
                    gridcolor="rgba(148, 163, 184, 0.2)"
                )
            ),
            showlegend=True,
            legend=dict(x=0.5, y=-0.1, xanchor="center", orientation="h"),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=350,
            margin=dict(l=60, r=60, t=40, b=60)
        )
        
        st.plotly_chart(fig_radar, width="stretch")
    
    with col_right:
        st.markdown("### 📊 Tổng kết năm " + str(int(latest_year)))
        
        st.markdown(f"""
        <div class="summary-card">
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; text-align: center;">Chỉ số trung bình</p>
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div style="padding: 10px;">
                    <p style="color: #60a5fa; font-size: 2rem; font-weight: 700; margin: 0; text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);">{latest['CQS']:.2f}</p>
                    <p style="color: #64748b; font-size: 0.85rem; margin-top: 5px;">CQS</p>
                </div>
                <div style="padding: 10px;">
                    <p style="color: #34d399; font-size: 2rem; font-weight: 700; margin: 0; text-shadow: 0 0 20px rgba(52, 211, 153, 0.5);">{latest['KTS']:.2f}</p>
                    <p style="color: #64748b; font-size: 0.85rem; margin-top: 5px;">KTS</p>
                </div>
                <div style="padding: 10px;">
                    <p style="color: #fbbf24; font-size: 2rem; font-weight: 700; margin: 0; text-shadow: 0 0 20px rgba(251, 191, 36, 0.5);">{latest['XHS']:.2f}</p>
                    <p style="color: #64748b; font-size: 0.85rem; margin-top: 5px;">XHS</p>
                </div>
            </div>
        </div>
        
        <div class="summary-card" style="text-align: center;">
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 10px;">DTI Tổng hợp</p>
            <p style="color: #a78bfa; font-size: 3rem; font-weight: 700; margin: 0; text-shadow: 0 0 30px rgba(167, 139, 250, 0.6);">{latest['DTI']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 💡 Phân tích & Nhận định")
    
    st.markdown(f"""
    <div class="insight-box">
        <h4 style="color: #38bdf8; margin-bottom: 15px;">📌 Điểm nổi bật năm {latest_year}</h4>
        <ul style="color: #e2e8f0; line-height: 1.8;">
            <li><b>DTI tổng hợp</b> đạt <span style="color: #a78bfa; font-weight: 600;">{latest['DTI']:.3f}</span> - 
                tăng <span style="color: #34d399;">{calc_change(latest['DTI'], prev['DTI']):.1f}%</span> so với năm trước</li>
            <li><b>Kinh tế số (KTS)</b> có tốc độ tăng trưởng ấn tượng nhất với 
                <span style="color: #34d399;">{calc_change(latest['KTS'], prev['KTS']):.1f}%</span></li>
            <li><b>Chính quyền số (CQS)</b> và <b>Xã hội số (XHS)</b> phát triển đồng đều, 
                hỗ trợ nền tảng chuyển đổi số quốc gia</li>
            <li>Cả 3 trụ cột đều cho thấy xu hướng <span style="color: #34d399;">tăng trưởng tích cực</span> 
                từ 2021 đến {latest_year}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
