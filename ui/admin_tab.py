import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_PATH = Path("data/province_data.csv")

def render():
    """
    Render the Admin Data View tab:
    - Display all data submitted by provinces
    - Allow export to CSV
    - Prepare placeholder for computed results (later integration)
    """
    st.title("📋 Provincial Data Overview")

    # Chỉ cho admin truy cập
    if st.session_state.get("role") != "admin":
        st.warning("Only admin users can access this section.")
        return

    # Kiểm tra file dữ liệu
    if not DATA_PATH.exists():
        st.info("No provincial data found yet. Please wait for provinces to submit their indicators.")
        return

    # Đọc dữ liệu
    df = pd.read_csv(DATA_PATH)

    # Hiển thị bảng
    st.subheader("🗂️ Submitted Data from Provinces")
    st.dataframe(df, use_container_width=True, height=400)

    # Thống kê nhanh
    st.markdown("### 📊 Summary Statistics")
    st.write(df.describe())

    # Cho phép lọc theo tỉnh
    provinces = sorted(df["Province"].unique())
    selected = st.multiselect("Filter by Province", provinces, default=provinces)
    filtered_df = df[df["Province"].isin(selected)]

    # Hiển thị biểu đồ nhập liệu
    if not filtered_df.empty:
        st.markdown("### 📈 DTI vs GDP Growth (Latest Submissions)")
        latest_df = filtered_df.groupby("Province").last().reset_index()

        chart = pd.DataFrame({
            "Province": latest_df["Province"],
            "DTI": latest_df["DTI"],
            "GDP Growth": latest_df["GDP_Growth"]
        }).sort_values(by="DTI", ascending=False)

        st.bar_chart(chart.set_index("Province"))

    # Nút xuất dữ liệu
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Download Provincial Data (CSV)",
        data=csv,
        file_name=f"province_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.markdown("🧮 *Calculation module will be added here once the formula from Prof. Nguyên is available.*")
