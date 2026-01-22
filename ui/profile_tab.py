import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from utils.database import get_user

DATA_PATH = Path("data/csv/province_data.csv")


def render():
    """
    User Profile Tab - Premium Dark Theme UI
    Cho phép user xem thông tin tài khoản và dữ liệu đã nhập
    """
    
    # ============================================================
    # CUSTOM CSS
    # ============================================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .profile-header {
        text-align: center;
        padding: 20px 0 30px;
        animation: fadeIn 0.8s ease-out;
    }
    
    .profile-header h1 {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: -0.02em;
    }
    
    .profile-header p {
        color: #cbd5e1;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    .info-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 18px;
        padding: 28px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .info-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(96, 165, 250, 0.3);
    }
    
    .info-item {
        display: flex;
        align-items: center;
        padding: 14px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .info-item:last-child {
        border-bottom: none;
    }
    
    .info-label {
        color: #e2e8f0;
        font-size: 0.95rem;
        min-width: 160px;
        font-weight: 500;
    }
    
    .info-value {
        color: #f1f5f9;
        font-size: 1.05rem;
        font-weight: 600;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 25px 0 15px;
        padding: 14px 20px;
        background: linear-gradient(90deg, rgba(96, 165, 250, 0.1) 0%, transparent 100%);
        border-left: 4px solid #60a5fa;
        border-radius: 0 12px 12px 0;
    }
    
    .section-header h3 {
        color: #f1f5f9;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.01em;
    }
    
    .stat-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stat-value {
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .stat-label {
        color: #e2e8f0;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 8px;
    }
    
    .empty-state {
        text-align: center;
        padding: 50px 20px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 16px;
        border: 2px dashed rgba(148, 163, 184, 0.2);
    }
    
    .empty-state h3 {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    .empty-state p {
        color: #94a3b8 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 500;
        color: #e2e8f0;
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
    <div class="profile-header">
        <h1>👤 Tài khoản của tôi</h1>
        <p>Xem thông tin tài khoản và dữ liệu đã nhập</p>
    </div>
    """, unsafe_allow_html=True)

    current_user = st.session_state.get("user", "")
    
    # ============================================================
    # TABS
    # ============================================================
    tab1, tab2, tab3 = st.tabs(["📋 Thông tin tài khoản", "📊 Dữ liệu đã nhập", "📜 Lịch sử hoạt động"])
    
    # ============================================================
    # TAB 1: ACCOUNT INFO
    # ============================================================
    with tab1:
        st.markdown("""
        <div class="section-header">
            <span style="font-size: 1.3rem;">📋</span>
            <h3>Thông tin tài khoản</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get user info from database
        user_info = get_user(current_user)
        
        if user_info:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-item">
                        <span class="info-label">👤 Tên đăng nhập</span>
                        <span class="info-value">{user_info.get('username', 'N/A')}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">🎭 Vai trò</span>
                        <span class="info-value">{'👨‍💼 Admin' if user_info.get('role') == 'admin' else '🏙️ Province'}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                created_at = user_info.get('created_at', 'N/A')
                if created_at and created_at != 'N/A':
                    try:
                        # Parse and format date
                        if isinstance(created_at, str):
                            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            created_at_formatted = dt.strftime('%d/%m/%Y %H:%M')
                        else:
                            created_at_formatted = str(created_at)
                    except:
                        created_at_formatted = str(created_at)
                else:
                    created_at_formatted = 'N/A'
                
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-item">
                        <span class="info-label">📅 Ngày tạo</span>
                        <span class="info-value">{created_at_formatted}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">🔐 Trạng thái</span>
                        <span class="info-value" style="color: #34d399;">✅ Đang hoạt động</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Không thể tải thông tin người dùng.")
    
    # ============================================================
    # TAB 2: SUBMITTED DATA
    # ============================================================
    with tab2:
        st.markdown("""
        <div class="section-header">
            <span style="font-size: 1.3rem;">📊</span>
            <h3>Dữ liệu đã nhập</h3>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            if DATA_PATH.exists():
                df = pd.read_csv(DATA_PATH)
                
                # Filter by current user's submitted data
                # Assuming there's a 'submitted_by' or 'Province' column
                if 'submitted_by' in df.columns:
                    user_data = df[df['submitted_by'] == current_user]
                elif 'Province' in df.columns:
                    # If username matches province name pattern
                    user_data = df[df['Province'].str.lower() == current_user.lower()]
                else:
                    # Show all data if no filter column
                    user_data = df
                
                if not user_data.empty:
                    # Stats
                    num_records = len(user_data)
                    years = user_data['Year'].unique() if 'Year' in user_data.columns else []
                    latest_year = max(years) if len(years) > 0 else 'N/A'
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-value" style="color: #60a5fa;">{num_records}</div>
                            <div class="stat-label">Bản ghi</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-value" style="color: #34d399;">{len(years)}</div>
                            <div class="stat-label">Năm dữ liệu</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-value" style="color: #fbbf24;">{latest_year}</div>
                            <div class="stat-label">Năm mới nhất</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Data table
                    st.dataframe(
                        user_data,
                        width="stretch",
                        height=400
                    )
                    
                    # Download button
                    csv_data = user_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="💾 Tải xuống dữ liệu của tôi",
                        data=csv_data,
                        file_name=f"my_data_{current_user}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        width='stretch'
                    )
                else:
                    st.markdown("""
                    <div class="empty-state">
                        <span style="font-size: 3rem;">📭</span>
                        <h3 style="color: #94a3b8; margin-top: 15px;">Chưa có dữ liệu</h3>
                        <p style="color: #64748b;">Bạn chưa nhập dữ liệu nào. Hãy vào tab "Nhập dữ liệu" để bắt đầu.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📭 Chưa có dữ liệu trong hệ thống.")
        except Exception as e:
            st.error(f"Lỗi khi tải dữ liệu: {e}")
    
    # ============================================================
    # TAB 3: ACTIVITY HISTORY
    # ============================================================
    with tab3:
        st.markdown("""
        <div class="section-header">
            <span style="font-size: 1.3rem;">📜</span>
            <h3>Lịch sử hoạt động</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Current login session info
        st.markdown(f"""
        <div class="info-card">
            <div class="info-item">
                <span class="info-label">🟢 Phiên đăng nhập hiện tại</span>
                <span class="info-value">{datetime.now().strftime('%d/%m/%Y %H:%M')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="empty-state" style="margin-top: 20px;">
            <span style="font-size: 3rem;">📋</span>
            <h3 style="color: #94a3b8; margin-top: 15px;">Lịch sử hoạt động</h3>
            <p style="color: #64748b;">Tính năng đang được phát triển. Lịch sử đăng nhập sẽ được hiển thị tại đây.</p>
        </div>
        """, unsafe_allow_html=True)
