import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render():
    """
    Trang tổng quan (Overview) - Premium Dark Theme with Enhanced UI
    """
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
    
    /* Premium Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        padding: 10px 0;
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9));
        border-radius: 16px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        border-radius: 4px 0 0 4px;
    }
    
    .metric-card.cqs::before { background: linear-gradient(180deg, #60a5fa, #3b82f6); }
    .metric-card.kts::before { background: linear-gradient(180deg, #34d399, #10b981); }
    .metric-card.xhs::before { background: linear-gradient(180deg, #fbbf24, #f59e0b); }
    .metric-card.dti::before { background: linear-gradient(180deg, #a78bfa, #8b5cf6); }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(148, 163, 184, 0.2);
    }
    
    .metric-card.cqs:hover { box-shadow: 0 20px 40px rgba(96, 165, 250, 0.15); }
    .metric-card.kts:hover { box-shadow: 0 20px 40px rgba(52, 211, 153, 0.15); }
    .metric-card.xhs:hover { box-shadow: 0 20px 40px rgba(251, 191, 36, 0.15); }
    .metric-card.dti:hover { box-shadow: 0 20px 40px rgba(167, 139, 250, 0.15); }
    
    .metric-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        font-size: 1.2rem;
    }
    
    .metric-card.cqs .metric-icon { background: rgba(96, 165, 250, 0.15); }
    .metric-card.kts .metric-icon { background: rgba(52, 211, 153, 0.15); }
    .metric-card.xhs .metric-icon { background: rgba(251, 191, 36, 0.15); }
    .metric-card.dti .metric-icon { background: rgba(167, 139, 250, 0.15); }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 6px;
        letter-spacing: 0.02em;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }
    
    .metric-card.cqs .metric-value { color: #60a5fa; }
    .metric-card.kts .metric-value { color: #34d399; }
    .metric-card.xhs .metric-value { color: #fbbf24; }
    .metric-card.dti .metric-value { color: #a78bfa; }
    
    .metric-delta {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .metric-delta.positive {
        background: rgba(52, 211, 153, 0.15);
        color: #34d399;
    }
    
    .metric-delta.negative {
        background: rgba(248, 113, 113, 0.15);
        color: #f87171;
    }
    
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
    
    /* Chart container styling */
    .chart-container {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.6), rgba(30, 41, 59, 0.4));
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(56, 189, 248, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="overview-header">
        <h1>📊 Tổng quan Tác động Chuyển đổi số tới Tăng trưởng GDP</h1>
        <p>Phân tích dữ liệu GDP và các chỉ số chuyển đổi số theo năm</p>
    </div>
    """, unsafe_allow_html=True)

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

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("""
        <div class="section-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
            <h3>GDP theo từng năm</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced GDP Chart
        fig_gdp = go.Figure()
        
        # Create gradient-like effect with multiple traces
        colors = ['#0284c7', '#0ea5e9', '#38bdf8', '#7dd3fc']
        
        fig_gdp.add_trace(go.Bar(
            x=gdp_df["Year"],
            y=gdp_df["GDP"],
            text=[f"{v/1e9:.1f}B" for v in gdp_df["GDP"]],
            textposition="outside",
            textfont=dict(size=13, color="#ffffff", family="Inter", weight=600),
            marker=dict(
                color=colors[:len(gdp_df)],
                line=dict(color='rgba(56, 189, 248, 0.3)', width=1),
                cornerradius=8
            ),
            hovertemplate="<b>Năm %{x}</b><br>GDP: %{y:,.0f} VND<extra></extra>"
        ))
        
        fig_gdp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0", family="Inter"),
            margin=dict(l=60, r=40, t=60, b=60),
            height=420,
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                tickmode="array",
                tickvals=gdp_df["Year"].tolist(),
                ticktext=[str(int(y)) for y in gdp_df["Year"]],
                tickfont=dict(size=14, color="#e2e8f0", weight=500),
                title=None
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor="rgba(56, 189, 248, 0.08)",
                gridwidth=1,
                tickformat=".2s",
                tickfont=dict(size=11, color="#64748b"),
                title=None,
                zeroline=False
            ),
            hoverlabel=dict(
                bgcolor="rgba(15, 23, 42, 0.95)",
                bordercolor="#38bdf8",
                font=dict(color="#f1f5f9", size=13)
            ),
            bargap=0.3
        )
        
        st.plotly_chart(fig_gdp, width='stretch')

    with col_right:
        st.markdown("""
        <div class="section-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>
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
            
            # Premium Metric Cards HTML
            def get_delta_class(value):
                return "positive" if value >= 0 else "negative"
            
            def get_delta_arrow(value):
                return "↑" if value >= 0 else "↓"
            
            metrics_html = f"""
            <div class="metric-grid">
                <div class="metric-card cqs">
                    <div class="metric-icon">🏛️</div>
                    <div class="metric-label">CQS → GDP</div>
                    <div class="metric-value">{cqs_coef:.2f}B</div>
                    <span class="metric-delta {get_delta_class(cqs_coef)}">
                        {get_delta_arrow(cqs_coef)} {abs(cqs_coef/100):.2f}%
                    </span>
                </div>
                <div class="metric-card kts">
                    <div class="metric-icon">💼</div>
                    <div class="metric-label">KTS → GDP</div>
                    <div class="metric-value">{kts_coef:.2f}B</div>
                    <span class="metric-delta {get_delta_class(kts_coef)}">
                        {get_delta_arrow(kts_coef)} {abs(kts_coef/100):.2f}%
                    </span>
                </div>
                <div class="metric-card xhs">
                    <div class="metric-icon">🌍</div>
                    <div class="metric-label">XHS → GDP</div>
                    <div class="metric-value">{xhs_coef:.2f}B</div>
                    <span class="metric-delta {get_delta_class(xhs_coef)}">
                        {get_delta_arrow(xhs_coef)} {abs(xhs_coef/100):.2f}%
                    </span>
                </div>
                <div class="metric-card dti">
                    <div class="metric-icon">💡</div>
                    <div class="metric-label">DTI → GDP</div>
                    <div class="metric-value">{dti_scaled:.2f}B</div>
                    <span class="metric-delta {get_delta_class(dti_scaled)}">
                        {get_delta_arrow(dti_scaled)} {abs(dti_scaled/100):.2f}%
                    </span>
                </div>
            </div>
            """
            st.markdown(metrics_html, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Không thể tính metrics: {e}")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
        </svg>
        <h3>Các trụ cột Chuyển đổi số theo năm</h3>
    </div>
    """, unsafe_allow_html=True)

    def create_pillar_chart(df, x_col, y_col, primary_color, gradient_start, gradient_end, pillar_name):
        """Create enhanced bar chart with gradient colors and growth annotation"""
        fig = go.Figure()
        
        # Calculate growth percentage
        first_val = df[y_col].iloc[0]
        last_val = df[y_col].iloc[-1]
        growth_pct = ((last_val - first_val) / first_val * 100) if first_val != 0 else 0
        
        # Generate gradient colors for each bar
        n_bars = len(df)
        bar_colors = []
        for i in range(n_bars):
            ratio = i / (n_bars - 1) if n_bars > 1 else 0
            r = int(int(gradient_start[1:3], 16) * (1 - ratio) + int(gradient_end[1:3], 16) * ratio)
            g = int(int(gradient_start[3:5], 16) * (1 - ratio) + int(gradient_end[3:5], 16) * ratio)
            b = int(int(gradient_start[5:7], 16) * (1 - ratio) + int(gradient_end[5:7], 16) * ratio)
            bar_colors.append(f'rgb({r}, {g}, {b})')
        
        # Bar chart with gradient colors
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[y_col],
            text=[f"{v:.2f}" for v in df[y_col]],
            textposition="outside",
            textfont=dict(size=13, color="#ffffff", family="Inter", weight=600),
            marker=dict(
                color=bar_colors,
                line=dict(color=primary_color, width=1),
                cornerradius=8
            ),
            hovertemplate=f"<b>{pillar_name}</b><br>Năm: %{{x}}<br>Giá trị: %{{y:.3f}}<extra></extra>"
        ))
        
        # Add trend arrow annotation
        arrow_color = "#34d399" if growth_pct >= 0 else "#f87171"
        arrow_symbol = "↑" if growth_pct >= 0 else "↓"
        
        fig.add_annotation(
            x=df[x_col].iloc[-1],
            y=last_val,
            text=f"<b>{arrow_symbol} {abs(growth_pct):.1f}%</b>",
            showarrow=False,
            font=dict(size=11, color=arrow_color, family="Inter"),
            xshift=40,
            yshift=15,
            bgcolor="rgba(15, 23, 42, 0.9)",
            bordercolor=arrow_color,
            borderwidth=1,
            borderpad=4
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0", family="Inter"),
            margin=dict(l=45, r=60, t=40, b=45),
            height=280,
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                tickmode="array",
                tickvals=df[x_col].tolist(),
                ticktext=[str(int(y)) for y in df[x_col]],
                tickfont=dict(size=13, color="#e2e8f0", family="Inter", weight=500)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(148, 163, 184, 0.08)",
                gridwidth=1,
                tickfont=dict(size=10, color="#64748b", family="Inter"),
                zeroline=False,
                range=[0, df[y_col].max() * 1.25]
            ),
            hoverlabel=dict(
                bgcolor="rgba(15, 23, 42, 0.95)",
                bordercolor=primary_color,
                font=dict(color="#f1f5f9", size=13, family="Inter")
            ),
            bargap=0.3
        )
        
        return fig


    # Enhanced pillar headers with glass card styling
    st.markdown("""
    <style>
    .pillar-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.6), rgba(30, 41, 59, 0.4));
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 16px 16px 8px 16px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .pillar-card:hover {
        border-color: rgba(148, 163, 184, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    .pillar-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }
    .pillar-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .pillar-icon.cqs { background: rgba(96, 165, 250, 0.15); }
    .pillar-icon.dti { background: rgba(167, 139, 250, 0.15); }
    .pillar-icon.kts { background: rgba(52, 211, 153, 0.15); }
    .pillar-icon.xhs { background: rgba(251, 191, 36, 0.15); }
    .pillar-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #f1f5f9;
    }
    .pillar-name span {
        font-weight: 400;
        color: #94a3b8;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    col_c, col_d = st.columns(2)

    with col_a:
        st.markdown('''
        <div class="pillar-card">
            <div class="pillar-title">
                <div class="pillar-icon cqs">🏛️</div>
                <div class="pillar-name">CQS <span>• Chính quyền số</span></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.plotly_chart(
            create_pillar_chart(cqs_df, "Year", "CQS", "#60a5fa", "#2563eb", "#93c5fd", "CQS"), 
            width='stretch'
        )

    with col_b:
        st.markdown('''
        <div class="pillar-card">
            <div class="pillar-title">
                <div class="pillar-icon dti">💡</div>
                <div class="pillar-name">DTI <span>• Chuyển đổi số tổng hợp</span></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.plotly_chart(
            create_pillar_chart(dti_df, "Year", "DTI", "#a78bfa", "#7c3aed", "#c4b5fd", "DTI"), 
            width='stretch'
        )

    with col_c:
        st.markdown('''
        <div class="pillar-card">
            <div class="pillar-title">
                <div class="pillar-icon kts">💼</div>
                <div class="pillar-name">KTS <span>• Kinh tế số</span></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.plotly_chart(
            create_pillar_chart(kts_df, "Year", "KTS", "#34d399", "#059669", "#6ee7b7", "KTS"), 
            width='stretch'
        )

    with col_d:
        st.markdown('''
        <div class="pillar-card">
            <div class="pillar-title">
                <div class="pillar-icon xhs">🌍</div>
                <div class="pillar-name">XHS <span>• Xã hội số</span></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.plotly_chart(
            create_pillar_chart(xhs_df, "Year", "XHS", "#fbbf24", "#d97706", "#fcd34d", "XHS"), 
            width='stretch'
        )

