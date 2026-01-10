import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

# Đường dẫn dữ liệu
DATA_PATH = Path("data/csv/province_data.csv")


def render():
    """
    Provincial Data Input - Premium Dark Theme UI
    Cho phép user tỉnh nhập dữ liệu chuyển đổi số hàng năm
    """

    # ============================================================
    # CUSTOM CSS
    # ============================================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .user-header {
        text-align: center;
        padding: 20px 0 30px;
        animation: fadeIn 0.8s ease-out;
    }
    
    .user-header h1 {
        background: linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        font-family: 'Inter', sans-serif;
    }
    
    .user-header p {
        color: #94a3b8;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .province-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(56, 189, 248, 0.2));
        padding: 12px 24px;
        border-radius: 30px;
        margin: 10px 0 20px;
        border: 1px solid rgba(52, 211, 153, 0.3);
    }
    
    .province-badge span {
        color: #34d399;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .input-section {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(148, 163, 184, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .section-title h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }
    
    .year-selector {
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 25px;
    }
    
    .save-button {
        background: linear-gradient(135deg, #34d399, #38bdf8) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 15px 40px !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .save-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(52, 211, 153, 0.4);
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(56, 189, 248, 0.1));
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .info-card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .info-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    .info-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 5px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

    # ============================================================
    # HEADER
    # ============================================================
    st.markdown("""
    <div class="user-header">
        <h1>📝 Nhập Dữ liệu Tỉnh</h1>
        <p>Cập nhật chỉ số chuyển đổi số và tăng trưởng kinh tế</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # ACCESS CONTROL
    # ============================================================
    if st.session_state.get("role") != "province":
        st.error("🚫 Chỉ user tỉnh mới có thể truy cập trang này.")
        return

    province = st.session_state["user"].capitalize()
    
    # Province Badge
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="province-badge">
            <span>🏙️ {province}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # YEAR SELECTOR
    # ============================================================
    current_year = date.today().year
    
    col_year1, col_year2, col_year3 = st.columns([1, 2, 1])
    with col_year2:
        st.markdown("""
        <div class="year-selector">
            <p style="color: #94a3b8; margin-bottom: 8px; font-size: 0.9rem;">📅 Chọn năm báo cáo</p>
        </div>
        """, unsafe_allow_html=True)
        selected_year = st.selectbox(
            "Năm",
            [current_year - 3, current_year - 2, current_year - 1, current_year, current_year + 1],
            index=3,
            label_visibility="collapsed"
        )

    # ============================================================
    # MAIN INDICATORS SECTION
    # ============================================================
    st.markdown("""
    <div class="input-section">
        <div class="section-title">
            <span style="font-size: 1.5rem;">📊</span>
            <h3>Chỉ số Kinh tế & Chuyển đổi số</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 💰 Chỉ số Kinh tế")
        gdp_growth = st.number_input(
            "Tăng trưởng GDP (%)",
            min_value=-20.0,
            max_value=30.0,
            value=5.0,
            step=0.1,
            help="Tỷ lệ tăng trưởng GDP so với năm trước"
        )
        investment = st.number_input(
            "Đầu tư số (Tỷ VND)",
            min_value=0.0,
            value=100.0,
            step=10.0,
            help="Tổng đầu tư vào chuyển đổi số"
        )
    
    with col2:
        st.markdown("##### 💡 Chỉ số Chuyển đổi số")
        dti_score = st.number_input(
            "Chỉ số DTI (0-1)",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            help="Digital Transformation Index tổng hợp"
        )

    # ============================================================
    # THREE PILLARS SECTION
    # ============================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="input-section">
        <div class="section-title">
            <span style="font-size: 1.5rem;">🧩</span>
            <h3>Ba Trụ cột Chuyển đổi số</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("##### 🏛️ Chính quyền số")
        cqs = st.slider("CQS", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")
        st.markdown(f"""
        <div class="info-card">
            <div class="info-value" style="color: #60a5fa;">{cqs:.2f}</div>
            <div class="info-label">CQS Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p2:
        st.markdown("##### 💼 Kinh tế số")
        kts = st.slider("KTS", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")
        st.markdown(f"""
        <div class="info-card">
            <div class="info-value" style="color: #34d399;">{kts:.2f}</div>
            <div class="info-label">KTS Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p3:
        st.markdown("##### 🌍 Xã hội số")
        xhs = st.slider("XHS", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")
        st.markdown(f"""
        <div class="info-card">
            <div class="info-value" style="color: #fbbf24;">{xhs:.2f}</div>
            <div class="info-label">XHS Score</div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # SUPPORTING FACTORS
    # ============================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="input-section">
        <div class="section-title">
            <span style="font-size: 1.5rem;">⚙️</span>
            <h3>Yếu tố Hỗ trợ</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        infrastructure = st.slider("🔌 Hạ tầng số", 0, 100, 50, help="Chất lượng hạ tầng CNTT")
    
    with col_s2:
        skills = st.slider("📚 Kỹ năng số", 0, 100, 50, help="Trình độ kỹ năng số của người dân")
    
    with col_s3:
        innovation = st.slider("💡 Đổi mới sáng tạo", 0, 100, 50, help="Mức độ đổi mới công nghệ")

    # ============================================================
    # VALIDATION & SAVE
    # ============================================================
    def validate_inputs():
        errors = []
        if not -20 <= gdp_growth <= 30:
            errors.append("⚠️ GDP Growth phải trong khoảng -20% đến 30%")
        if not 0 <= dti_score <= 1:
            errors.append("⚠️ DTI phải trong khoảng 0-1")
        return errors

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("💾 Lưu dữ liệu", use_container_width=True, type="primary"):
            validation_errors = validate_inputs()
            
            if validation_errors:
                for err in validation_errors:
                    st.error(err)
            else:
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
                    mask = (old_df["Province"] == province) & (old_df["Year"] == selected_year)
                    old_df = old_df[~mask]
                    df = pd.concat([old_df, new_df], ignore_index=True)
                else:
                    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
                    df = new_df

                df.to_csv(DATA_PATH, index=False)
                
                st.markdown(f"""
                <div class="success-box">
                    <h3 style="color: #34d399; margin: 0;">✅ Lưu thành công!</h3>
                    <p style="color: #94a3b8; margin-top: 10px;">
                        Dữ liệu của <b>{province}</b> năm <b>{selected_year}</b> đã được cập nhật.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Preview
                st.markdown("#### 📋 Dữ liệu đã lưu")
                st.dataframe(df[df["Province"] == province].tail(5), use_container_width=True)
