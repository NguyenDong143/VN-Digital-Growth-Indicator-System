import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import plotly.express as px

from models.regression_model import run_regression


def render():
    """
    Render Regression Analysis tab: OLS impact of digital indicators on GDP.
    """
    st.title("📈 Regression Analysis: DTI → GDP")

    st.markdown(
        "Phân tích hồi quy OLS đánh giá tác động của các chỉ số "
        "**CQS (Chính quyền số), KTS (Kinh tế số), XHS (Xã hội số), DTI** "
        "tới tăng trưởng GDP."
    )

    try:
        model = run_regression()
    except Exception as exc:  # surface the error to user
        st.error(f"⚠️ Không chạy được hồi quy: {exc}")
        st.info(
            "Đảm bảo các file tồn tại trong `data/csv/`: "
            "GDP.csv, CQS.csv, KTS.csv, XHS.csv, DTI.csv "
            "(cần cột `Year` và cột giá trị tương ứng)."
        )
        return

    # ----- Coefficients table -----
    coef_df = (
        pd.DataFrame({"Indicator": model.params.index, "Coefficient": model.params.values})
        .query("Indicator != 'const'")
        .reset_index(drop=True)
    )
    pvalues = model.pvalues

    # ----- Metrics row -----
    cols = st.columns(4)
    cols[0].metric("R²", f"{model.rsquared:.3f}")
    cols[1].metric("Adj. R²", f"{model.rsquared_adj:.3f}")
    cols[2].metric("F-statistic", f"{model.fvalue:.2f}")
    cols[3].metric("Observations", f"{int(model.nobs)}")

    st.markdown("### 🧭 Ý nghĩa thống kê")
    sig_df = pd.DataFrame({
        "Indicator": coef_df["Indicator"],
        "Coefficient": coef_df["Coefficient"].round(4),
        "P-value": [pvalues[ind] for ind in coef_df["Indicator"]],
        "Significant (p<0.05)": [pvalues[ind] < 0.05 for ind in coef_df["Indicator"]],
    })
    st.dataframe(sig_df, use_container_width=True)

    if int(model.nobs) < 8:
        st.warning(
            f"⚠️ Chỉ có {int(model.nobs)} quan sát — kết quả OLS chưa đủ tin cậy "
            "về mặt thống kê. Khuyến nghị ≥ 8 năm dữ liệu (tốt nhất ≥ 20)."
        )

    # ----- Bar chart of coefficients -----
    st.markdown("### 📊 Hệ số hồi quy OLS")
    fig = px.bar(
        coef_df,
        x="Indicator",
        y="Coefficient",
        color="Coefficient",
        color_continuous_scale="RdBu_r",
        title="OLS Coefficients: Impact of Each Indicator on GDP",
    )
    fig.update_layout(height=420, yaxis_title="Coefficient β")
    st.plotly_chart(fig, use_container_width=True)

    # ----- Full OLS summary -----
    with st.expander("📋 OLS Summary chi tiết (statsmodels)"):
        st.text(model.summary())
