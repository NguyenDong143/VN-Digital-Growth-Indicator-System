# 🌐 Digital GDP Dashboard

**Vietnam Digital Transformation & GDP Growth Analysis**

Dashboard phân tích mối quan hệ giữa **Chuyển đổi số** và **Tăng trưởng GDP** của 63 tỉnh/thành phố Việt Nam.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Screenshots

### Login Page
- Giao diện đăng nhập hiện đại với galaxy theme
- Hỗ trợ đăng ký tài khoản mới

### GDP & DTI Overview
- Biểu đồ GDP theo năm
- 4 Key Metrics: CQS, KTS, XHS, DTI → GDP
- 4 biểu đồ trụ cột chuyển đổi số

### Digital Transformation Pillars
- 4 Pillar Cards với hiệu ứng hover
- Biểu đồ xu hướng theo năm
- Radar chart so sánh các năm
- Phân tích & nhận định

---

## Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| **GDP Analysis** | Biểu đồ tương tác với Plotly |
| **3 Trụ cột** | CQS (Chính quyền số), KTS (Kinh tế số), XHS (Xã hội số) |
| **DTI Index** | Chỉ số chuyển đổi số tổng hợp |
| **Regression** | Phân tích OLS: DTI → GDP |
| **Phân quyền** | Admin (xem tất cả) / Province (nhập liệu) |
| **Bảo mật** | bcrypt hash + SQLite database |
| **Dark Theme** | Giao diện tối hiện đại với hiệu ứng |

---

## � Cấu trúc dự án

```
DIGITAL_GDP_DASHBOARD/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker config
├── README.md
│
├── config/
│   └── settings.py         # Cấu hình ứng dụng
│
├── data/
│   ├── csv/                # Dữ liệu CSV
│   │   ├── GDP.csv
│   │   ├── CQS.csv
│   │   ├── KTS.csv
│   │   ├── XHS.csv
│   │   └── DTI.csv
│   └── db/                 # SQLite database
│       └── users.db
│
├── assets/
│   └── images/             # Hình ảnh
│
├── models/
│   ├── regression_model.py # Mô hình hồi quy OLS
│   └── forecast_model.py   # Dự báo
│
├── ui/
│   ├── style.py            # Dark theme
│   ├── login_tab.py        # Đăng nhập
│   ├── register_tab.py     # Đăng ký
│   ├── overview_tab.py     # Tổng quan GDP
│   ├── components_tab.py   # 3 trụ cột
│   ├── admin_tab.py        # Admin view
│   └── input_tab.py        # Province input
│
├── utils/
│   ├── auth_manager.py     # Xác thực
│   ├── database.py         # SQLite
│   ├── data_loader.py      # Load dữ liệu
│   └── data_cleaner.py     # Xử lý dữ liệu
│
└── tests/                  # Unit tests
```

---

## Cài đặt & Chạy

### Yêu cầu
- Python 3.11+

### Cách 1: UV

```bash
# Cài UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clone & Setup
git clone https://github.com/your-username/DIGITAL_GDP_DASHBOARD.git
cd DIGITAL_GDP_DASHBOARD

uv venv
uv pip install -r requirements.txt
.venv\Scripts\activate
streamlit run main.py
```

### Cách 2: venv
```bash
git clone https://github.com/your-username/DIGITAL_GDP_DASHBOARD.git
cd DIGITAL_GDP_DASHBOARD

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

### Cách 3: Docker

```bash
docker build -t gdp-dashboard .
docker run -p 8501:8501 gdp-dashboard
```

---

## 🌐 Truy cập

```
http://localhost:8501
```

### Tài khoản mặc định
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| user | user123 | Province |

---

## 👥 Vai trò người dùng

### Admin
- Xem GDP & DTI Overview
- Xem Digital Transformation Pillars
- Quản lý dữ liệu (Admin Data View)

### User
- Nhập liệu chỉ số tỉnh/thành phố

---

