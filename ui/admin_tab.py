import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from config.settings import DATA_PATHS

def render():
    """
    Render the Admin Data View tab:
    - Display all data submitted by provinces
    - Allow export to CSV
    - Show summary stats and a simple visualization
    """

    st.title("🧭 Provincial Data Management")

    # ============================================
    # 1️⃣ Kiểm tra quyền truy cập
    # ============================================
    if st.session_state.get("role") != "admin":
        st.warning("🚫 Only admin users can access this section.")
        st.stop()

    # ============================================
    # 2️⃣ Đọc dữ liệu từ file users hoặc dữ liệu tỉnh
    # ============================================
    data_path = "data/province_data.csv"

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        st.info("⚠️ No provincial data found yet. Please wait for provinces to submit their indicators.")
        return

    if df.empty:
        st.info("✅ File exists but contains no records.")
        return

    # ============================================
    # 3️⃣ Hiển thị dữ liệu
    # ============================================
    st.subheader("🗂️ Submitted Data from Provinces")
    st.dataframe(df, use_container_width=True, height=420)

    # ============================================
    # 4️⃣ Thống kê nhanh
    # ============================================
    st.markdown("### 📊 Summary Statistics")
    with st.expander("View Descriptive Stats"):
        st.write(df.describe())

    # ============================================
    # 5️⃣ Bộ lọc theo tỉnh
    # ============================================
    provinces = sorted(df["Province"].unique())
    selected = st.multiselect("🏙️ Filter by Province", provinces, default=provinces)
    filtered_df = df[df["Province"].isin(selected)]

    # ============================================
    # 6️⃣ Biểu đồ: DTI vs GDP Growth
    # ============================================
    if not filtered_df.empty and "DTI" in df.columns and "GDP_Growth" in df.columns:
        st.subheader("📈 DTI vs GDP Growth (Latest Year)")

        latest_df = filtered_df.groupby("Province").last().reset_index()

        fig = px.scatter(
            latest_df,
            x="DTI",
            y="GDP_Growth",
            color="Province",
            size="DTI",
            hover_name="Province",
            title="Relationship between DTI and GDP Growth across Provinces",
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📉 Missing columns 'DTI' or 'GDP_Growth' — cannot render chart.")

    # ============================================
    # 7️⃣ Nút tải dữ liệu xuống
    # ============================================
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Download Provincial Data (CSV)",
        data=csv_data,
        file_name=f"province_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

    # ============================================
    # 8️⃣ Placeholder cho tính toán nâng cao
    # ============================================
    st.markdown("---")
    st.markdown("🧮 *Calculation module (e.g. weighted DTI impact) will be added once formulas from Prof. Nguyên are finalized.*")
