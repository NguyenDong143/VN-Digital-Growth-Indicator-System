import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

DATA_PATH = Path("data/csv/province_data.csv")


def render():
    """
    Provincial Data Input - Premium Dark Theme UI
    Cho phép user tỉnh nhập dữ liệu chuyển đổi số hàng năm
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Header Section */
    .input-header {
        text-align: center;
        padding: 25px 0 35px;
        animation: fadeIn 0.8s ease-out;
    }
    
    .input-header h1 {
        background: linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 12px;
        letter-spacing: -0.02em;
    }
    
    .input-header p {
        color: #e2e8f0;
        font-size: 1.15rem;
        font-weight: 400;
    }
    
    /* Province Welcome Card */
    .welcome-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 20px;
        padding: 30px;
        margin: 0 auto 30px;
        max-width: 500px;
        text-align: center;
        border: 1px solid rgba(52, 211, 153, 0.3);
        box-shadow: 0 12px 40px rgba(52, 211, 153, 0.1);
    }
    
    .welcome-icon {
        width: 70px;
        height: 70px;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(56, 189, 248, 0.2));
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px;
        font-size: 2rem;
    }
    
    .welcome-province {
        font-size: 1.8rem;
        font-weight: 700;
        color: #34d399;
        margin-bottom: 8px;
        text-shadow: 0 0 30px rgba(52, 211, 153, 0.4);
    }
    
    .welcome-role {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* Year Selector */
    .year-card {
        background: linear-gradient(145deg, rgba(56, 189, 248, 0.1), rgba(30, 41, 59, 0.8));
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .year-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        background: rgba(56, 189, 248, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .year-label {
        color: #e2e8f0;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Form Section Cards */
    .form-section {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
    
    .form-section:hover {
        border-color: rgba(148, 163, 184, 0.25);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .section-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
    }
    
    .section-icon.economy { background: rgba(251, 191, 36, 0.15); }
    .section-icon.digital { background: rgba(167, 139, 250, 0.15); }
    .section-icon.pillars { background: rgba(96, 165, 250, 0.15); }
    .section-icon.support { background: rgba(52, 211, 153, 0.15); }
    
    .section-title {
        color: #f1f5f9;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.01em;
    }
    
    /* Pillar Score Cards */
    .pillar-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6));
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .pillar-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    }
    
    .pillar-card.cqs { border-top: 3px solid #60a5fa; }
    .pillar-card.kts { border-top: 3px solid #34d399; }
    .pillar-card.xhs { border-top: 3px solid #fbbf24; }
    
    .pillar-icon-wrapper {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px;
        font-size: 1.4rem;
    }
    
    .pillar-icon-wrapper.cqs { background: rgba(96, 165, 250, 0.15); }
    .pillar-icon-wrapper.kts { background: rgba(52, 211, 153, 0.15); }
    .pillar-icon-wrapper.xhs { background: rgba(251, 191, 36, 0.15); }
    
    .pillar-name {
        color: #e2e8f0;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 4px;
    }
    
    .pillar-code {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
    }
    
    .pillar-value {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .pillar-value.cqs { color: #60a5fa; }
    .pillar-value.kts { color: #34d399; }
    .pillar-value.xhs { color: #fbbf24; }
    
    /* Support Factor Cards */
    .factor-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6));
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .factor-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #34d399;
        margin-bottom: 4px;
    }
    
    .factor-label {
        color: #e2e8f0;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Save Button Area */
    .save-section {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        border-radius: 20px;
        padding: 30px;
        margin-top: 30px;
        text-align: center;
        border: 1px solid rgba(52, 211, 153, 0.2);
    }
    
    .save-hint {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 15px;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(56, 189, 248, 0.1));
        border: 1px solid rgba(52, 211, 153, 0.4);
        border-radius: 18px;
        padding: 28px;
        margin: 25px 0;
        text-align: center;
    }
    
    .success-icon {
        font-size: 3rem;
        margin-bottom: 12px;
    }
    
    .success-title {
        color: #34d399;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .success-detail {
        color: #e2e8f0;
        font-size: 0.95rem;
    }
    
    /* Input Styling */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    .stSlider > div > div > div > div {
        font-weight: 600 !important;
    }
    
    /* Label Styling */
    .stNumberInput label, .stSlider label, .stSelectbox label {
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #e2e8f0 !important;
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
    <div class="input-header">
        <h1>📝 Nhập Dữ liệu Chuyển đổi số</h1>
        <p>Cập nhật chỉ số kinh tế và chuyển đổi số của tỉnh thành</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("role") != "province":
        st.error("🚫 Chỉ user tỉnh mới có thể truy cập trang này.")
        return

    province = st.session_state["user"].capitalize()

    # Welcome Card
    st.markdown(f"""
    <div class="welcome-card">
        <div class="welcome-icon">🏙️</div>
        <div class="welcome-province">{province}</div>
        <div class="welcome-role">Đang nhập dữ liệu với vai trò Province User</div>
    </div>
    """, unsafe_allow_html=True)

    current_year = date.today().year
    
    # Year Selector
    col_year1, col_year2, col_year3 = st.columns([1, 2, 1])
    with col_year2:
        st.markdown("""
        <div class="year-card">
            <div class="year-icon">📅</div>
            <div class="year-label">Chọn năm báo cáo</div>
        </div>
        """, unsafe_allow_html=True)
        selected_year = st.selectbox(
            "Năm",
            [current_year - 3, current_year - 2, current_year - 1, current_year, current_year + 1],
            index=3,
            label_visibility="collapsed"
        )

    # ============================================================
    # SECTION 1: Economic Indicators
    # ============================================================
    st.markdown("""
    <div class="form-section">
        <div class="section-header">
            <div class="section-icon economy">💰</div>
            <h3 class="section-title">Chỉ số Kinh tế</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        gdp_growth = st.number_input(
            "📈 Tăng trưởng GDP (%)",
            min_value=-20.0,
            max_value=30.0,
            value=5.0,
            step=0.1,
            help="Tỷ lệ tăng trưởng GDP so với năm trước"
        )
    
    with col2:
        investment = st.number_input(
            "💵 Đầu tư số (Tỷ VND)",
            min_value=0.0,
            value=100.0,
            step=10.0,
            help="Tổng đầu tư vào chuyển đổi số"
        )

    # ============================================================
    # SECTION 2: Digital Transformation Index
    # ============================================================
    st.markdown("""
    <div class="form-section">
        <div class="section-header">
            <div class="section-icon digital">💡</div>
            <h3 class="section-title">Chỉ số Chuyển đổi số tổng hợp (DTI)</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_dti1, col_dti2, col_dti3 = st.columns([1, 2, 1])
    with col_dti2:
        dti_score = st.slider(
            "Chỉ số DTI (0 - 1)",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            help="Digital Transformation Index tổng hợp"
        )
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 3rem; font-weight: 700; color: #a78bfa; text-shadow: 0 0 30px rgba(167, 139, 250, 0.5);">{dti_score:.2f}</span>
            <p style="color: #94a3b8; margin-top: 8px; font-size: 0.9rem;">Digital Transformation Index</p>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # SECTION 3: Three Pillars
    # ============================================================
    st.markdown("""
    <div class="form-section">
        <div class="section-header">
            <div class="section-icon pillars">🧩</div>
            <h3 class="section-title">Ba Trụ cột Chuyển đổi số</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        cqs = st.slider("CQS - Chính quyền số", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")
        st.markdown(f"""
        <div class="pillar-card cqs">
            <div class="pillar-icon-wrapper cqs">🏛️</div>
            <div class="pillar-name">Chính quyền số</div>
            <div class="pillar-code">CQS</div>
            <div class="pillar-value cqs">{cqs:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p2:
        kts = st.slider("KTS - Kinh tế số", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")
        st.markdown(f"""
        <div class="pillar-card kts">
            <div class="pillar-icon-wrapper kts">💼</div>
            <div class="pillar-name">Kinh tế số</div>
            <div class="pillar-code">KTS</div>
            <div class="pillar-value kts">{kts:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p3:
        xhs = st.slider("XHS - Xã hội số", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")
        st.markdown(f"""
        <div class="pillar-card xhs">
            <div class="pillar-icon-wrapper xhs">🌍</div>
            <div class="pillar-name">Xã hội số</div>
            <div class="pillar-code">XHS</div>
            <div class="pillar-value xhs">{xhs:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # SECTION 4: Support Factors
    # ============================================================
    st.markdown("""
    <div class="form-section">
        <div class="section-header">
            <div class="section-icon support">⚙️</div>
            <h3 class="section-title">Yếu tố Hỗ trợ</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        infrastructure = st.slider("🔌 Hạ tầng số", 0, 100, 50, help="Chất lượng hạ tầng CNTT")
        st.markdown(f"""
        <div class="factor-card">
            <div class="factor-value">{infrastructure}%</div>
            <div class="factor-label">Hạ tầng số</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_s2:
        skills = st.slider("📚 Kỹ năng số", 0, 100, 50, help="Trình độ kỹ năng số của người dân")
        st.markdown(f"""
        <div class="factor-card">
            <div class="factor-value">{skills}%</div>
            <div class="factor-label">Kỹ năng số</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_s3:
        innovation = st.slider("💡 Đổi mới sáng tạo", 0, 100, 50, help="Mức độ đổi mới công nghệ")
        st.markdown(f"""
        <div class="factor-card">
            <div class="factor-value">{innovation}%</div>
            <div class="factor-label">Đổi mới sáng tạo</div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # SAVE SECTION
    # ============================================================
    def validate_inputs():
        errors = []
        if not -20 <= gdp_growth <= 30:
            errors.append("⚠️ GDP Growth phải trong khoảng -20% đến 30%")
        if not 0 <= dti_score <= 1:
            errors.append("⚠️ DTI phải trong khoảng 0-1")
        return errors

    st.markdown("""
    <div class="save-section">
        <p class="save-hint">💡 Kiểm tra lại thông tin trước khi lưu</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("💾 Lưu dữ liệu", width='stretch', type="primary"):
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
                    <div class="success-icon">✅</div>
                    <div class="success-title">Lưu thành công!</div>
                    <div class="success-detail">
                        Dữ liệu của <b>{province}</b> năm <b>{selected_year}</b> đã được cập nhật.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Preview
                st.markdown("#### 📋 Dữ liệu đã lưu")
                st.dataframe(df[df["Province"] == province].tail(5), width='stretch')
