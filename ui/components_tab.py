import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from config.settings import DATA_PATHS


def render():
    """
    Giao diện:
    - Bên trái: Biểu đồ GDP theo năm
    - Bên phải: 6 Key Metrics chia 3 hàng (2 cột/hàng)
    - Dưới cùng: 4 biểu đồ phụ (CQS, DTI, KTS, XHS) chia 2×2
    """

    # =====================================================
    # 1️⃣ PAGE TITLE
    # =====================================================
    st.markdown(
        "<h2 style='text-align:center; color:white;'>📊 Tổng quan Tác động Chuyển đổi số tới Tăng trưởng GDP</h2>",
        unsafe_allow_html=True
    )

    # =====================================================
    # 2️⃣ LOAD DATA
    # =====================================================
    gdp = pd.read_csv(DATA_PATHS["GDP"])
    cqs = pd.read_csv(DATA_PATHS["CQS"])
    kts = pd.read_csv(DATA_PATHS["KTS"])
    xhs = pd.read_csv(DATA_PATHS["XHS"])
    dti = pd.read_csv(DATA_PATHS["DTI"])

    df = gdp.merge(cqs, on="Year").merge(kts, on="Year").merge(xhs, on="Year").merge(dti, on="Year")
    df.columns = ["Year", "GDP", "CQS", "KTS", "XHS", "DTI"]

    # =====================================================
    # 3️⃣ OLS REGRESSION
    # =====================================================
    X = sm.add_constant(df[["CQS", "KTS", "XHS", "DTI"]])
    y = df["GDP"]
    model = sm.OLS(y, X).fit()
    coef_df = model.params.reset_index()
    coef_df.columns = ["Indicator", "Coefficient"]
    coef_df = coef_df[coef_df["Indicator"] != "const"]

    # =====================================================
    # 4️⃣ GIAO DIỆN CHÍNH
    # =====================================================
    left, right = st.columns([2, 1])  # GDP chart left, metrics right

    # GDP CHART (LEFT)
    with left:
        fig_gdp = px.bar(
            df, x="Year", y="GDP", text="GDP", color="GDP",
            color_continuous_scale="Blues", title="GDP Growth by Year"
        )
        fig_gdp.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_gdp.update_layout(yaxis_title="GDP", height=450)
        st.plotly_chart(fig_gdp, use_container_width=True)

    # 6 METRICS (RIGHT)
    with right:
        st.markdown("#### 💡 Key Metrics (Impact on GDP)")
        c1, c2 = st.columns(2)
        c1.metric("CQS → GDP", f"{coef_df.loc[coef_df['Indicator']=='CQS','Coefficient'].values[0]:.3f}")
        c2.metric("KTS → GDP", f"{coef_df.loc[coef_df['Indicator']=='KTS','Coefficient'].values[0]:.3f}")

        c3, c4 = st.columns(2)
        c3.metric("XHS → GDP", f"{coef_df.loc[coef_df['Indicator']=='XHS','Coefficient'].values[0]:.3f}")
        c4.metric("DTI → GDP", f"{coef_df.loc[coef_df['Indicator']=='DTI','Coefficient'].values[0]:.3f}")

        c5, c6 = st.columns(2)
        c5.metric("R² Score", f"{model.rsquared:.3f}")
        c6.metric("Adj. R²", f"{model.rsquared_adj:.3f}")

    # =====================================================
    # 5️⃣ BIỂU ĐỒ 4 CHỈ SỐ (2x2)
    # =====================================================
    st.markdown("### 🔍 Digital Transformation Components Over Years")
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        fig_cqs = px.bar(df, x="Year", y="CQS", color="CQS",
                         color_continuous_scale="Purples", title="CQS (Government)")
        st.plotly_chart(fig_cqs, use_container_width=True)

    with row1_col2:
        fig_kts = px.bar(df, x="Year", y="KTS", color="KTS",
                         color_continuous_scale="Blues", title="KTS (Economy)")
        st.plotly_chart(fig_kts, use_container_width=True)

    with row2_col1:
        fig_xhs = px.bar(df, x="Year", y="XHS", color="XHS",
                         color_continuous_scale="Greens", title="XHS (Society)")
        st.plotly_chart(fig_xhs, use_container_width=True)

    with row2_col2:
        fig_dti = px.bar(df, x="Year", y="DTI", color="DTI",
                         color_continuous_scale="Oranges", title="DTI (Overall Index)")
        st.plotly_chart(fig_dti, use_container_width=True)

    # =====================================================
    # 6️⃣ INSIGHTS
    # =====================================================
    st.markdown("### 🧠 Insights")
    st.write("""
    - **GDP** tăng ổn định phản ánh tiến trình chuyển đổi số tổng thể.
    - **KTS (Digital Economy)** có ảnh hưởng mạnh nhất tới GDP.
    - **CQS** và **XHS** hỗ trợ môi trường quản trị và kỹ năng số.
    - **DTI** phản ánh mức độ trưởng thành chuyển đổi số tổng hợp.
    """)
