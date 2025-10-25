import streamlit as st
import pandas as pd
import plotly.express as px


def render():
    """
    Trang tổng quan (Overview):
    Bố cục:
    - Bên trái: Biểu đồ GDP theo năm
    - Bên phải: 6 Key Metrics chia 3 hàng (2 cột/hàng)
    - Dưới cùng: 4 biểu đồ phụ (CQS, DTI, KTS, XHS) chia 2×2
    """

    # ============================================================
    # 1️⃣ PAGE TITLE
    # ============================================================
    st.markdown(
        "<h2 style='text-align:center; color:white;'>📊 Tổng quan Tác động Chuyển đổi số tới Tăng trưởng GDP</h2>",
        unsafe_allow_html=True
    )

    # ============================================================
    # 2️⃣ LOAD DATA
    # ============================================================
    gdp_df = pd.read_csv("data/GDP.csv")
    cqs_df = pd.read_csv("data/CQS.csv")
    dti_df = pd.read_csv("data/DTI.csv")
    kts_df = pd.read_csv("data/KTS.csv")
    xhs_df = pd.read_csv("data/XHS.csv")

    # Đảm bảo cột "Year" là số nguyên
    for df in [gdp_df, cqs_df, dti_df, kts_df, xhs_df]:
        df["Year"] = df["Year"].astype(int)

    # Gộp dữ liệu theo năm
    gdp_df = gdp_df.groupby("Year", as_index=False)["GDP"].sum()
    cqs_df = cqs_df.groupby("Year", as_index=False)["CQS"].mean()
    dti_df = dti_df.groupby("Year", as_index=False)["DTI"].mean()
    kts_df = kts_df.groupby("Year", as_index=False)["KTS"].mean()
    xhs_df = xhs_df.groupby("Year", as_index=False)["XHS"].mean()

    # ============================================================
    # 3️⃣ BỐ CỤC CHÍNH: 2 CỘT — GDP (trái) & Key Metrics (phải)
    # ============================================================
    col_left, col_right = st.columns([2, 1])

    # --------- BIỂU ĐỒ GDP THEO NĂM ---------
    with col_left:
        st.markdown("### 💰 GDP theo từng năm")
        fig_gdp = px.bar(
            gdp_df,
            x="Year",
            y="GDP",
            text_auto=".2s",
            color_discrete_sequence=["#38bdf8"]
        )
        fig_gdp.update_traces(textposition="outside", textfont=dict(size=12, color="white"))
        fig_gdp.update_layout(
            title="GDP qua các năm",
            title_x=0.4,
            yaxis_title="GDP (VNĐ)",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            uniformtext_minsize=8,
            uniformtext_mode="hide",
            bargap=0.3
        )
        fig_gdp.update_xaxes(showgrid=False)
        fig_gdp.update_yaxes(showgrid=False, tickprefix="₫", tickformat=".2s")
        st.plotly_chart(fig_gdp, use_container_width=True)

    # --------- 6 KEY METRICS (3 hàng × 2 cột) ---------
    with col_right:
        st.markdown("### 🧭 Key Metrics – Tác động ước lượng")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏛️ CQS → GDP", "0.0309", "+0.31%")
        with col2:
            st.metric("💼 KTS → GDP", "0.0256", "+0.26%")

        col3, col4 = st.columns(2)
        with col3:
            st.metric("🌍 XHS → GDP", "0.0274", "+0.27%")
        with col4:
            st.metric("💡 DTI → GDP", "0.0319", "+0.32%")

        col5, col6 = st.columns(2)
        with col5:
            st.metric("💰 Vốn đầu tư (K) → GDP", "0.055", "+0.55%")
        with col6:
            st.metric("👷 Lao động (L) → GDP", "-0.024", "-0.24%")

    # ============================================================
    # 4️⃣ BIỂU ĐỒ 4 TRỤ CỘT CHUYỂN ĐỔI SỐ (2×2)
    # ============================================================
    st.markdown("<hr style='border: 1px solid #1e293b;'>", unsafe_allow_html=True)
    st.markdown("### 🧩 Các trụ cột chuyển đổi số theo năm")

    col_a, col_b = st.columns(2)
    col_c, col_d = st.columns(2)

    def style_bar_chart(df, x_col, y_col, color_seq, title):
        fig = px.bar(df, x=x_col, y=y_col, text_auto=".2s", color_discrete_sequence=[color_seq])
        fig.update_traces(textposition="outside", textfont=dict(size=11, color="white"))
        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white"),
            uniformtext_minsize=8,
            uniformtext_mode="hide",
            bargap=0.3,
            title=title,
            title_x=0.4,
            yaxis_title=None
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, tickprefix="₫", tickformat=".2s")
        return fig

    with col_a:
        st.markdown("#### 🏛️ CQS (Chính quyền số)")
        st.plotly_chart(style_bar_chart(cqs_df, "Year", "CQS", "#60a5fa", "CQS qua các năm"), use_container_width=True)

    with col_b:
        st.markdown("#### 💡 DTI (Chuyển đổi số tổng hợp)")
        st.plotly_chart(style_bar_chart(dti_df, "Year", "DTI", "#a78bfa", "DTI qua các năm"), use_container_width=True)

    with col_c:
        st.markdown("#### 💼 KTS (Kinh tế số)")
        st.plotly_chart(style_bar_chart(kts_df, "Year", "KTS", "#34d399", "KTS qua các năm"), use_container_width=True)

    with col_d:
        st.markdown("#### 🌍 XHS (Xã hội số)")
        st.plotly_chart(style_bar_chart(xhs_df, "Year", "XHS", "#fbbf24", "XHS qua các năm"), use_container_width=True)
