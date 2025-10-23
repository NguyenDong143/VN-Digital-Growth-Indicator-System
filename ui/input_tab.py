import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

DATA_PATH = Path("data/province_data.csv")

def render():
    st.title("🏙️ Provincial Data Input")

    if st.session_state.get("role") != "province":
        st.warning("Only provincial users can access this page.")
        return

    province = st.session_state["user"].capitalize()
    st.subheader(f"Data Entry for {province}")

    dti_score = st.number_input("Digital Transformation Index (DTI)", min_value=0.0, max_value=10.0, step=0.1)
    gdp_growth = st.number_input("GDP Growth (%)", min_value=-5.0, max_value=15.0, step=0.1)
    investment = st.number_input("Digital Investment (Billion VND)", min_value=0.0, step=0.1)
    infrastructure = st.slider("Infrastructure Score", 0, 200, 100)
    skills = st.slider("Digital Skills Score", 0, 200, 100)
    innovation = st.slider("Innovation Score", 0, 200, 100)

    if st.button("💾 Save Data"):
        new_row = {
            "Date": date.today(),
            "Province": province,
            "DTI": dti_score,
            "GDP_Growth": gdp_growth,
            "Investment": investment,
            "Infrastructure": infrastructure,
            "Skills": skills,
            "Innovation": innovation,
        }

        df = pd.DataFrame([new_row])
        if DATA_PATH.exists():
            df_old = pd.read_csv(DATA_PATH)
            df = pd.concat([df_old, df], ignore_index=True)

        df.to_csv(DATA_PATH, index=False)
        st.success("✅ Data saved successfully!")
