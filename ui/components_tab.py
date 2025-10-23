import streamlit as st
import pandas as pd
import plotly.express as px


def render():
    """
    Render the Overview tab for the Digital Transformation and GDP Growth Dashboard.

    This section visualizes the three main pillars of Vietnam's digital transformation:
    1. Digital Transformation (Government)
    2. Digital Economy
    3. Digital Society
    """

    # --- PAGE TITLE ---
    st.title("📊 DTI & GDP Growth Overview")

    # --- Create layout columns ---
    col1, col2, col3 = st.columns(3)

    # --- DIGITAL TRANSFORMATION ---
    df_transformation = pd.DataFrame({
        "Component": ["Infrastructure", "Skills", "E-Government Services", "Innovation"],
        "Score": [160, 180, 190, 210]
    })

    # --- DIGITAL ECONOMY ---
    df_economy = pd.DataFrame({
        "Component": ["Digital Business", "E-Payment", "Innovation", "Productivity"],
        "Score": [180, 210, 225, 205]
    })

    # --- DIGITAL SOCIETY ---
    df_society = pd.DataFrame({
        "Component": ["Internet Access", "Digital Skills", "Awareness", "Inclusion"],
        "Score": [150, 175, 190, 180]
    })

    # --- VISUALIZATION: DIGITAL TRANSFORMATION ---
    with col1:
        st.markdown("### 💡 Digital Transformation")
        fig1 = px.bar(
            df_transformation,
            x="Component",
            y="Score",
            text="Score",
            color="Component",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.update_traces(textposition="outside")
        fig1.update_layout(
            title="Government Digitalization",
            title_x=0.2,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)

    # --- VISUALIZATION: DIGITAL ECONOMY ---
    with col2:
        st.markdown("### 💼 Digital Economy")
        fig2 = px.bar(
            df_economy,
            x="Component",
            y="Score",
            text="Score",
            color="Component",
            color_discrete_sequence=px.colors.qualitative.Pastel2
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(
            title="Private Sector Digitalization",
            title_x=0.2,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # --- VISUALIZATION: DIGITAL SOCIETY ---
    with col3:
        st.markdown("### 🌍 Digital Society")
        fig3 = px.bar(
            df_society,
            x="Component",
            y="Score",
            text="Score",
            color="Component",
            color_discrete_sequence=px.colors.qualitative.Pastel1
        )
        fig3.update_traces(textposition="outside")
        fig3.update_layout(
            title="Social Inclusion & Awareness",
            title_x=0.2,
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)
