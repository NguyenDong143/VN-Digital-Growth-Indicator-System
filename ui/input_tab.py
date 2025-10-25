import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

# Đường dẫn dữ liệu
DATA_PATH = Path("data/province_data.csv")

def render():
    """
    Provincial Data Input Tab
    Allow each province user to enter yearly digital transformation and GDP data.
    """

    st.title("🏙️ Provincial Data Input")

    # ===============================================
    # 1️⃣ Kiểm tra quyền truy cập
    # ===============================================
    if st.session_state.get("role") != "province":
        st.warning("🚫 Only provincial users can access this page.")
        return

    province = st.session_state["user"].capitalize()
    st.subheader(f"📋 Data Entry for {province}")

    # ===============================================
    # 2️⃣ Chọn năm nhập dữ liệu
    # ===============================================
    current_year = date.today().year
    selected_year = st.selectbox("📅 Select Year", [current_year - 3, current_year - 2, current_year - 1, current_year, current_year + 1])

    st.markdown("---")

    # ===============================================
    # 3️⃣ Nhập dữ liệu chính
    # ===============================================
    st.markdown("### 📊 Economic & Digital Transformation Indicators")

    col1, col2, col3 = st.columns(3)
    with col1:
        gdp_growth = st.number_input("GDP Growth (%)", min_value=-5.0, max_value=15.0, step=0.1)
        dti_score = st.number_input("Digital Transformation Index (DTI)", min_value=0.0, max_value=10.0, step=0.1)
    with col2:
        cqs = st.number_input("CQS (Digital Government)", min_value=0.0, max_value=200.0, step=1.0)
        kts = st.number_input("KTS (Digital Economy)", min_value=0.0, max_value=200.0, step=1.0)
    with col3:
        xhs = st.number_input("XHS (Digital Society)", min_value=0.0, max_value=200.0, step=1.0)
        investment = st.number_input("Digital Investment (Billion VND)", min_value=0.0, step=0.1)

    st.markdown("---")

    st.markdown("### 🧩 Supporting Factors")
    infrastructure = st.slider("Infrastructure Score", 0, 200, 100)
    skills = st.slider("Digital Skills Score", 0, 200, 100)
    innovation = st.slider("Innovation Score", 0, 200, 100)

    # ===============================================
    # 4️⃣ Nút lưu dữ liệu
    # ===============================================
    if st.button("💾 Save Data"):
        new_row = {
            "Date": date.today(),
            "Year": selected_year,
            "Province": province,
            "GDP_Growth": gdp_growth,
            "DTI": dti_score,
            "CQS": cqs,
            "KTS": kts,
            "XHS": xhs,
            "Investment": investment,
            "Infrastructure": infrastructure,
            "Skills": skills,
            "Innovation": innovation,
        }

        new_df = pd.DataFrame([new_row])

        # Đọc file cũ nếu có
        if DATA_PATH.exists():
            old_df = pd.read_csv(DATA_PATH)
            # Kiểm tra trùng năm + tỉnh để ghi đè
            mask = (old_df["Province"] == province) & (old_df["Year"] == selected_year)
            old_df = old_df[~mask]
            df = pd.concat([old_df, new_df], ignore_index=True)
        else:
            df = new_df

        # Lưu file CSV
        df.to_csv(DATA_PATH, index=False)
        st.success(f"✅ Data for {province} ({selected_year}) saved successfully!")

        # Hiển thị bảng tóm tắt
        st.markdown("#### 🧾 Current Data Preview")
        st.dataframe(df.tail(10), use_container_width=True)
