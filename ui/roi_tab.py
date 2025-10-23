import streamlit as st
import pandas as pd
import plotly.express as px


def render():
    """
    Render the ROI (Return on Investment) Analysis tab for the
    Digital Transformation & GDP Growth Dashboard.

    This visualization estimates the efficiency of digital investment
    in contributing to Vietnam’s GDP growth over time.
    """

    # --- Page title ---
    st.title("💰 ROI of Digital Investment in Vietnam")

    # --- Sample data (can be replaced with real data) ---
    years = list(range(2020, 2029))
    digital_investment = [2, 2.5, 3, 3.8, 4.5, 5.5, 6.5, 7.2, 8.0]   # USD billions
    gdp_contribution = [4, 5, 6, 7.8, 9.5, 11.5, 13.5, 15.8, 18.0]  # USD billions

    df = pd.DataFrame({
        "Year": years,
        "Digital Investment (Billion USD)": digital_investment,
        "GDP Contribution (Billion USD)": gdp_contribution
    })

    # --- Calculate ROI ---
    df["ROI"] = df["GDP Contribution (Billion USD)"] / df["Digital Investment (Billion USD)"]

    # --- Plot ROI trend ---
    fig = px.line(
        df,
        x="Year",
        y="ROI",
        markers=True,
        title="Return on Digital Investment (ROI)",
        color_discrete_sequence=["#38bdf8"]
    )

    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        title_x=0.3,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white", size=14),
        yaxis_title="ROI (×)",
        xaxis_title="Year"
    )

    # --- Display chart ---
    st.plotly_chart(fig, use_container_width=True)

    # --- Add source note ---
    st.caption("Source: Simulated data for demonstration purposes. Replace with official statistics if available.")
