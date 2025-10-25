# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from models.regression_model import run_regression

# def render():
#     """
#     Render the Regression Analysis tab for the Digital Transformation & GDP Growth Dashboard.
#     Runs an OLS regression to evaluate the impact of CQS, KTS, XHS, and DTI on GDP.
#     """

#     # ======================================================
#     # 1️⃣ Page Header
#     # ======================================================
#     st.title("📈 Regression Analysis: Impact of Digital Indicators on GDP")
#     st.markdown(
#         """
#         This section performs an **Ordinary Least Squares (OLS)** regression  
#         to evaluate how Vietnam's **digital transformation indicators** —  
#         **CQS (Digital Government)**, **KTS (Digital Economy)**, **XHS (Digital Society)**, and **DTI (Overall)**  
#         — influence national **GDP growth**.
#         """
#     )

#     # ======================================================
#     # 2️⃣ Run Regression
#     # ======================================================
#     try:
#         model = run_regression()

#         # Extract coefficients
#         coef_df = model.params.reset_index()
#         coef_df.columns = ["Indicator", "Coefficient"]
#         coef_df = coef_df[coef_df["Indicator"] != "const"]

#         # Extract key stats
#         r2 = model.rsquared
#         pvalues = model.pvalues.round(4)

#         # ======================================================
#         # 3️⃣ Display Summary (Collapsible)
#         # ======================================================
#         with st.expander("📊 Detailed Regression Summary", expanded=True):
#             st.text(model.summary())

#         # ======================================================
#         # 4️⃣ Key Metrics
#         # ======================================================
#         st.markdown("### 🧭 Key Regression Metrics")

#         col1, col2, col3 = st.columns(3)
#         col1.metric("R-squared", f"{r2:.3f}")
#         col2.metric("Number of Variables", len(coef_df))
#         col3.metric("Most Significant (Lowest P-Value)", pvalues.idxmin())

#         # ======================================================
#         # 5️⃣ Visualize Coefficients
#         # ======================================================
#         st.markdown("### 📊 Coefficient Impact on GDP")

#         fig = px.bar(
#             coef_df,
#             x="Indicator", y="Coefficient",
#             text="Coefficient",
#             color="Coefficient",
#             color_continuous_scale="viridis",
#             title="OLS Coefficients: Impact of Each Indicator on GDP"
#         )
#         fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
#         fig.update_layout(yaxis_title="Coefficient β", height=400)
#         st.plotly_chart(fig, use_container_width=True)

#         # ======================================================
#         # 6️⃣ Interpretation
#         # ======================================================
#         st.markdown("---")
#         st.markdown("### 📘 Interpretation Guide")
#         st.markdown(
#             """
#             - **Coefficient (β):** Shows how each indicator contributes to GDP — a positive value indicates a positive impact.  
#             - **P-value:** Tests statistical significance (values < 0.05 suggest a significant relationship).  
#             - **R-squared:** Explains how well the digital indicators collectively explain GDP variation.  
#             - **Highest β:** The indicator with the largest coefficient has the **strongest impact** on GDP.  
#             """
#         )

#     except Exception as e:
#         st.error(f"⚠️ Error running regression: {e}")
#         st.info("""
#         Please ensure the following files exist in your `data/` folder:
#         - GDP.csv  
#         - CQS.csv  
#         - KTS.csv  
#         - XHS.csv  
#         - DTI.csv  
#         Each should contain columns: `Year` and their respective index/value.
#         """)
