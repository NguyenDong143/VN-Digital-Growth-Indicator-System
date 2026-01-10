import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from config.settings import DATA_PATHS
from utils.database import get_all_users


def render():
    """
    Admin Data View - Premium Dark Theme UI
    Quản lý dữ liệu tỉnh và người dùng
    """

    # ============================================================
    # CUSTOM CSS
    # ============================================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .admin-header {
        text-align: center;
        padding: 20px 0 30px;
        animation: fadeIn 0.8s ease-out;
    }
    
    .admin-header h1 {
        background: linear-gradient(135deg, #f472b6 0%, #c084fc 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        font-family: 'Inter', sans-serif;
    }
    
    .admin-header p {
        color: #94a3b8;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stat-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 25px 0 15px;
        padding: 12px 18px;
        background: linear-gradient(90deg, rgba(244, 114, 182, 0.1) 0%, transparent 100%);
        border-left: 4px solid #f472b6;
        border-radius: 0 12px 12px 0;
    }
    
    .section-header h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }
    
    .user-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .badge-admin { background: rgba(244, 114, 182, 0.2); color: #f472b6; }
    .badge-province { background: rgba(96, 165, 250, 0.2); color: #60a5fa; }
    
    .data-table {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .download-btn {
        background: linear-gradient(135deg, #f472b6, #c084fc);
        color: white;
        padding: 12px 24px;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 16px;
        border: 2px dashed rgba(148, 163, 184, 0.2);
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
    <div class="admin-header">
        <h1>👨‍💼 Quản trị Dữ liệu</h1>
        <p>Xem và quản lý dữ liệu từ các tỉnh thành</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # ACCESS CONTROL
    # ============================================================
    if st.session_state.get("role") != "admin":
        st.error("🚫 Chỉ admin mới có thể truy cập trang này.")
        st.stop()

    # ============================================================
    # TABS
    # ============================================================
    tab1, tab2 = st.tabs(["📊 Dữ liệu Tỉnh", "👥 Quản lý User"])
    
    # ============================================================
    # TAB 1: PROVINCIAL DATA
    # ============================================================
    with tab1:
        data_path = DATA_PATHS.get("PROVINCE_DATA", "data/csv/province_data.csv")
        
        try:
            df = pd.read_csv(data_path)
        except FileNotFoundError:
            st.markdown("""
            <div class="empty-state">
                <span style="font-size: 4rem;">📭</span>
                <h3 style="color: #94a3b8; margin-top: 20px;">Chưa có dữ liệu</h3>
                <p style="color: #64748b;">Các tỉnh chưa gửi dữ liệu. Vui lòng chờ...</p>
            </div>
            """, unsafe_allow_html=True)
            df = None
        
        if df is not None and not df.empty:
            # Stats Cards
            col1, col2, col3, col4 = st.columns(4)
            
            num_provinces = df["Province"].nunique() if "Province" in df.columns else 0
            num_records = len(df)
            latest_year = df["Year"].max() if "Year" in df.columns else "N/A"
            avg_dti = df["DTI"].mean() if "DTI" in df.columns else 0
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color: #60a5fa;">{num_provinces}</div>
                    <div class="stat-label">Số tỉnh thành</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color: #34d399;">{num_records}</div>
                    <div class="stat-label">Bản ghi</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color: #fbbf24;">{latest_year}</div>
                    <div class="stat-label">Năm mới nhất</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color: #a78bfa;">{avg_dti:.2f}</div>
                    <div class="stat-label">DTI trung bình</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Data Table Section
            st.markdown("""
            <div class="section-header">
                <span style="font-size: 1.3rem;">📋</span>
                <h3>Dữ liệu chi tiết</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Filter
            if "Province" in df.columns:
                provinces = sorted(df["Province"].unique())
                selected = st.multiselect(
                    "🔍 Lọc theo tỉnh",
                    provinces,
                    default=provinces[:5] if len(provinces) > 5 else provinces
                )
                filtered_df = df[df["Province"].isin(selected)]
            else:
                filtered_df = df
            
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )
            
            # Chart Section
            if "DTI" in df.columns and "GDP_Growth" in df.columns and not filtered_df.empty:
                st.markdown("""
                <div class="section-header">
                    <span style="font-size: 1.3rem;">📈</span>
                    <h3>Biểu đồ DTI vs GDP Growth</h3>
                </div>
                """, unsafe_allow_html=True)
                
                fig = px.scatter(
                    filtered_df,
                    x="DTI",
                    y="GDP_Growth",
                    color="Province",
                    size="DTI",
                    hover_name="Province",
                    size_max=30
                )
                
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", family="Inter"),
                    height=450,
                    margin=dict(l=40, r=40, t=40, b=40),
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="rgba(148, 163, 184, 0.1)",
                        title="DTI"
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="rgba(148, 163, 184, 0.1)",
                        title="GDP Growth (%)"
                    ),
                    legend=dict(
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(size=10)
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Download Button
            st.markdown("<br>", unsafe_allow_html=True)
            csv_data = df.to_csv(index=False).encode("utf-8")
            col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
            with col_dl2:
                st.download_button(
                    label="💾 Tải xuống dữ liệu (CSV)",
                    data=csv_data,
                    file_name=f"province_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    # ============================================================
    # TAB 2: USER MANAGEMENT
    # ============================================================
    with tab2:
        st.markdown("""
        <div class="section-header">
            <span style="font-size: 1.3rem;">👥</span>
            <h3>Danh sách người dùng</h3>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            users = get_all_users()
            
            if users:
                # User stats
                admin_count = sum(1 for u in users if u.get("role") == "admin")
                province_count = sum(1 for u in users if u.get("role") == "province")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("👥 Tổng users", len(users))
                with col2:
                    st.metric("👨‍💼 Admin", admin_count)
                with col3:
                    st.metric("🏙️ Province", province_count)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # User table
                user_df = pd.DataFrame(users)
                if "password" in user_df.columns:
                    user_df = user_df.drop(columns=["password"])
                
                st.dataframe(user_df, use_container_width=True)
                
            else:
                st.info("Chưa có user nào trong hệ thống.")
                
        except Exception as e:
            st.error(f"Không thể tải danh sách user: {e}")
