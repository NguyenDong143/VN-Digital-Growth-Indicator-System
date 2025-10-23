import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    # --- PAGE TITLE ---
    st.markdown(
        "<h2 style='text-align:center; color:white;'>DTI & GDP Growth Analysis</h2>",
        unsafe_allow_html=True
    )

    # --- GDP FORECAST CHART ---
    years = list(range(2020, 2029))
    baseline = [100, 102, 104, 106, 108, 110, 113, 116, 118]
    high_dti = [100, 103, 106, 110, 115, 120, 126, 133, 140]

    df = pd.DataFrame({
        "Year": years,
        "Baseline": baseline,
        "High DTI Impact": high_dti
    })

    fig = px.line(
        df, x="Year", y=["Baseline", "High DTI Impact"],
        markers=True,
        color_discrete_map={
            "Baseline": "#38bdf8",
            "High DTI Impact": "#f472b6"
        }
    )
    fig.update_layout(
        title="GDP Growth Forecast (2020–2028)",
        title_x=0.25,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white"),
        legend=dict(orientation="h", y=-0.3, x=0.25)
    )

    # --- MAIN LAYOUT: CHART + METRICS ---
    col_chart, col_metrics = st.columns([2.5, 1])

    with col_chart:
        st.plotly_chart(fig, use_container_width=True)

    with col_metrics:
        st.markdown("#### 🧭 Key Metrics")
        st.markdown(
            """
            <div style='background-color:white; border-radius:10px; padding:10px; margin-bottom:10px; text-align:center;'>
                <h3 style='color:#0f172a;'>+2.5%</h3>
                <p style='color:#475569;'>Projected GDP Increase</p>
            </div>
            <div style='background-color:white; border-radius:10px; padding:10px; margin-bottom:10px; text-align:center;'>
                <h3 style='color:#0f172a;'>7.2%</h3>
                <p style='color:#475569;'>Current DTI Score</p>
            </div>
            <div style='background-color:white; border-radius:10px; padding:10px; margin-bottom:10px; text-align:center;'>
                <h3 style='color:#0f172a;'>1.5×</h3>
                <p style='color:#475569;'>Current DTI Efficiency</p>
            </div>
            <div style='background-color:white; border-radius:10px; padding:10px; text-align:center;'>
                <h3 style='color:#0f172a;'>1.5×</h3>
                <p style='color:#475569;'>ROI on Digital Investment</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- DIVIDER ---
    st.markdown("<hr style='border: 1px solid #1e293b;'>", unsafe_allow_html=True)

    # --- 3 PILLARS SECTION ---
    st.markdown("### 🧩 Digital Transformation Pillars")

    col1, col2, col3 = st.columns(3)

    df_trans = pd.DataFrame({
        "Component": ["Infrastructure", "Skills", "Services", "Innovation"],
        "Score": [160, 180, 190, 210]
    })
    df_econ = pd.DataFrame({
        "Component": ["Digital Business", "E-Payment", "Innovation", "Productivity"],
        "Score": [180, 210, 225, 205]
    })
    df_soc = pd.DataFrame({
        "Component": ["Internet Access", "Digital Skills", "Awareness", "Inclusion"],
        "Score": [150, 175, 190, 180]
    })

    with col1:
        st.markdown("#### 💡 Digital Transformation")
        st.plotly_chart(px.bar(df_trans, x="Component", y="Score", text="Score",
                               color="Component", color_discrete_sequence=px.colors.qualitative.Pastel),
                        use_container_width=True)

    with col2:
        st.markdown("#### 💼 Digital Economy")
        st.plotly_chart(px.bar(df_econ, x="Component", y="Score", text="Score",
                               color="Component", color_discrete_sequence=px.colors.qualitative.Pastel2),
                        use_container_width=True)

    with col3:
        st.markdown("#### 🌍 Digital Society")
        st.plotly_chart(px.bar(df_soc, x="Component", y="Score", text="Score",
                               color="Component", color_discrete_sequence=px.colors.qualitative.Pastel1),
                        use_container_width=True)
