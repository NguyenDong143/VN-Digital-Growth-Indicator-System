import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from config.settings import DATA_PATHS
from utils.database import get_all_users, delete_user, update_user_role, update_user_password, add_user


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
            
            # Editable table for admin
            st.info("📝 Bạn có thể chỉnh sửa trực tiếp trên bảng dữ liệu bên dưới")
            
            # Use dynamic key to allow reset
            if "data_editor_reset_counter" not in st.session_state:
                st.session_state.data_editor_reset_counter = 0
            
            edited_df = st.data_editor(
                filtered_df,
                width="stretch",
                height=400,
                num_rows="dynamic",  # Allow adding/deleting rows
                key=f"province_data_editor_{st.session_state.data_editor_reset_counter}"
            )
            
            # Save changes button
            col_save, col_reset = st.columns(2)
            with col_save:
                if st.button("💾 Lưu thay đổi", type="primary", width="stretch", key="btn_save_data"):
                    try:
                        # Update the full dataframe with edited values
                        if "Province" in df.columns:
                            # Remove old filtered rows and add edited ones
                            df_updated = df[~df["Province"].isin(selected)]
                            df_updated = pd.concat([df_updated, edited_df], ignore_index=True)
                        else:
                            df_updated = edited_df
                        
                        df_updated.to_csv(data_path, index=False)
                        st.success("✅ Đã lưu thay đổi thành công!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi khi lưu: {e}")
            
            with col_reset:
                if st.button("🔄 Hủy thay đổi", width="stretch", key="btn_reset_data"):
                    # Increment counter to generate new key and reset data_editor
                    st.session_state.data_editor_reset_counter += 1
                    st.rerun()
            
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
                
                st.plotly_chart(fig, width="stretch")
            
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
                    width="stretch"
                )
    
    # ============================================================
    # TAB 2: USER MANAGEMENT
    # ============================================================
    with tab2:
        
        # --------------------------------------------------------
        # SECTION 2: USER LIST WITH EDIT/DELETE
        # --------------------------------------------------------
        st.markdown("""
        <div class="section-header">
            <span style="font-size: 1.3rem;">👥</span>
            <h3>Danh sách người dùng</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize session state for editing
        if "editing_user_id" not in st.session_state:
            st.session_state.editing_user_id = None
        
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
                
                # Edit form (appears when editing a user)
                if st.session_state.editing_user_id is not None:
                    editing_user = next((u for u in users if u.get("id") == st.session_state.editing_user_id), None)
                    if editing_user:
                        st.markdown("""
                        <div class="section-header" style="background: linear-gradient(90deg, rgba(96, 165, 250, 0.2) 0%, transparent 100%); border-left-color: #60a5fa;">
                            <span style="font-size: 1.3rem;">✏️</span>
                            <h3>Sửa thông tin: {}</h3>
                        </div>
                        """.format(editing_user.get("username", "")), unsafe_allow_html=True)
                        
                        with st.container():
                            col_e1, col_e2 = st.columns(2)
                            with col_e1:
                                edit_role = st.selectbox(
                                    "🎭 Vai trò",
                                    ["province", "admin"],
                                    index=0 if editing_user.get("role") == "province" else 1,
                                    format_func=lambda x: "🏙️ Province" if x == "province" else "👨‍💼 Admin",
                                    key="edit_role"
                                )
                            with col_e2:
                                edit_password = st.text_input(
                                    "🔑 Mật khẩu mới (để trống nếu không đổi)",
                                    type="password",
                                    placeholder="Nhập mật khẩu mới",
                                    key="edit_password"
                                )
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.button("💾 Lưu thay đổi", type="primary", width="stretch", key="btn_save_edit"):
                                    success = False
                                    # Update role
                                    if update_user_role(editing_user.get("username"), edit_role):
                                        success = True
                                    # Update password if provided
                                    if edit_password and len(edit_password) >= 4:
                                        import bcrypt
                                        hashed_pw = bcrypt.hashpw(edit_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                                        if update_user_password(editing_user.get("username"), hashed_pw):
                                            success = True
                                    
                                    if success:
                                        st.success("✅ Đã cập nhật thành công!")
                                        st.session_state.editing_user_id = None
                                        st.rerun()
                                    else:
                                        st.error("❌ Cập nhật thất bại!")
                            
                            with col_cancel:
                                if st.button("❌ Hủy", width="stretch", key="btn_cancel_edit"):
                                    st.session_state.editing_user_id = None
                                    st.rerun()
                        
                        st.markdown("<hr style='border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
                
                # Add User Button - at top of table
                if "show_add_user_form" not in st.session_state:
                    st.session_state.show_add_user_form = False
                
                add_col1, add_col2 = st.columns([1, 3])
                with add_col1:
                    if st.button("➕ Thêm người dùng", type="primary", width="stretch", key="btn_show_add"):
                        st.session_state.show_add_user_form = not st.session_state.show_add_user_form
                        st.session_state.editing_user_id = None
                
                # Add User Form (appears when button clicked)
                if st.session_state.show_add_user_form:
                    st.markdown("""
                    <div class="section-header" style="background: linear-gradient(90deg, rgba(34, 197, 94, 0.2) 0%, transparent 100%); border-left-color: #22c55e;">
                        <span style="font-size: 1.3rem;">➕</span>
                        <h3>Thêm người dùng mới</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a1, col_a2 = st.columns(2)
                    with col_a1:
                        add_username = st.text_input("👤 Username", placeholder="Nhập username", key="add_new_username")
                        add_password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Nhập mật khẩu", key="add_new_password")
                    with col_a2:
                        add_role = st.selectbox(
                            "🎭 Vai trò",
                            ["province", "admin"],
                            format_func=lambda x: "🏙️ Province" if x == "province" else "👨‍💼 Admin",
                            key="add_new_role"
                        )
                        add_confirm = st.text_input("🔐 Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu", key="add_new_confirm")
                    
                    col_add_btn, col_cancel_btn = st.columns(2)
                    with col_add_btn:
                        if st.button("✅ Thêm user", type="primary", width="stretch", key="btn_confirm_add"):
                            if not add_username or not add_password or not add_confirm:
                                st.error("⚠️ Vui lòng nhập đầy đủ thông tin!")
                            elif add_password != add_confirm:
                                st.error("❌ Mật khẩu không khớp!")
                            elif len(add_password) < 4:
                                st.error("⚠️ Mật khẩu phải có ít nhất 4 ký tự!")
                            else:
                                import bcrypt
                                hashed_pw = bcrypt.hashpw(add_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                                if add_user(add_username, hashed_pw, add_role):
                                    st.success(f"✅ Đã tạo user '{add_username}' thành công!")
                                    st.session_state.show_add_user_form = False
                                    st.rerun()
                                else:
                                    st.error("⚠️ Username đã tồn tại!")
                    with col_cancel_btn:
                        if st.button("❌ Hủy", width="stretch", key="btn_cancel_add"):
                            st.session_state.show_add_user_form = False
                            st.rerun()
                    
                    st.markdown("<hr style='border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
                
                # Table Header
                header_cols = st.columns([0.5, 1.5, 1.2, 1.5])
                headers = ["ID", "Username", "Role", "Thao tác"]
                for col, header in zip(header_cols, headers):
                    col.markdown(f"**{header}**")
                
                st.markdown("<hr style='margin: 5px 0; border-color: rgba(148, 163, 184, 0.2);'>", unsafe_allow_html=True)
                
                # Table Rows with inline buttons
                current_login_user = st.session_state.get("user", "")
                
                for user in users:
                    cols = st.columns([0.5, 1.5, 1.2, 1.5])
                    
                    with cols[0]:
                        st.write(user.get("id", ""))
                    with cols[1]:
                        st.write(user.get("username", ""))
                    with cols[2]:
                        role = user.get("role", "province")
                        if role == "admin":
                            st.markdown("👨‍💼 Admin")
                        else:
                            st.markdown("🏙️ Province")
                    with cols[3]:
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("✏️ Sửa", key=f"edit_{user.get('id')}", type="primary", width="stretch"):
                                st.session_state.editing_user_id = user.get("id")
                                st.rerun()
                        with btn_col2:
                            is_self = (user.get("username") == current_login_user)
                            if st.button("🗑️ Xóa", key=f"delete_{user.get('id')}", type="secondary", width="stretch", disabled=is_self):
                                if not is_self:
                                    if delete_user(user.get("username")):
                                        st.success(f"✅ Đã xóa user '{user.get('username')}'!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Xóa thất bại!")
                
            else:
                st.info("Chưa có user nào trong hệ thống.")
                
        except Exception as e:
            st.error(f"Không thể tải danh sách user: {e}")
