 # 🌐 **Digital GDP Dashboard**

**Vietnam Digital Transformation & GDP Growth Analysis**
**Digital GDP Dashboard** là một ứng dụng **Streamlit** giúp trực quan hóa và phân tích **mối quan hệ giữa chuyển đổi số (Digital Transformation)** và **tăng trưởng GDP** tại Việt Nam.
Hệ thống tích hợp **phân quyền người dùng (Admin / Province)**, **đăng nhập – đăng ký**, và **phân tích hồi quy – dự báo GDP** dựa trên dữ liệu thực tế.
---

## 🧱 **Cấu trúc dự án**

```bash
DIGITAL_GDP_DASHBOARD/
│
├── main.py                        # File chính (chạy ứng dụng Streamlit)
│
├── config/
│   └── settings.py                # Cấu hình trang, theme, đường dẫn dữ liệu
│
├── data/                          # Dữ liệu và hình ảnh
│   ├── CQS.csv                    # Chỉ số Chính quyền số
│   ├── DTI.csv                    # Digital Transformation Index
│   ├── GDP.csv                    # GDP theo năm
│   ├── KTS.csv                    # Kinh tế số
│   ├── XHS.csv                    # Xã hội số
│   ├── users.csv                  # Danh sách tài khoản người dùng
│   ├── login.png                  # Giao diện đăng nhập
│   └── register.png               # Giao diện đăng ký
│
├── models/
│   ├── regression_model.py        # Hồi quy: GDP_growth ~ DTI
│   └── forecast_model.py          # Dự báo GDP dựa trên DTI
│
├── ui/
│   ├── overview_tab.py            # Tab Tổng quan GDP & DTI
│   ├── components_tab.py          # Tab 3 trụ cột chuyển đổi số
│   ├── regression_tab.py          # Tab hồi quy & kiểm định mô hình
│   ├── register_tab.py            # Giao diện đăng ký tài khoản
│   ├── login_tab.py               # Giao diện đăng nhập
│   ├── input_tab.py               # Nhập dữ liệu DTI cho user tỉnh
│   ├── admin_tab.py               # Quản lý tài khoản (admin)
│   └── style.py                   # Tùy chỉnh giao diện dark theme
│
├── utils/
│   ├── auth_manager.py            # Xử lý đăng nhập, đăng ký, phân quyền
│   ├── data_loader.py             # Hàm load dữ liệu CSV
│   └── data_cleaner.py            # Hàm xử lý, làm sạch dữ liệu
│
├── requirements.txt               # Danh sách thư viện cần cài
└── README.md                      # Tài liệu hướng dẫn
```

---

## 🚀 **Cách chạy ứng dụng**
### 1️⃣ Cài đặt thư viện
Mở terminal và chạy:

```bash
pip install -r requirements.txt
```
### 2️⃣ Chạy ứng dụng Streamlit
```bash
streamlit run main.py
```
Hoặc:
```bash
python -m streamlit run main.py
```

Ứng dụng sẽ tự động mở tại địa chỉ:
👉 **[http://localhost:8501](http://localhost:8501)**
---

## 🔐 **Phân quyền người dùng**

| Vai trò               | Chức năng chính                                       |
| --------------------- | ----------------------------------------------------- |
| 🏙️ **Province User** | Nhập dữ liệu DTI, xem phân tích GDP & các trụ cột số  |
| 👨‍💼 **Admin**       | Quản lý người dùng, phê duyệt và xem tổng hợp dữ liệu |
---

## 📊 **Các tính năng chính**
✅ **Phân tích & Trực quan hóa**
Hiển thị biểu đồ GDP, DTI và 3 trụ cột CQS – KTS – XHS theo năm.
✅ **Hồi quy & Dự báo GDP**
Mô hình hồi quy tuyến tính giúp đánh giá tác động của DTI tới GDP và dự báo tăng trưởng trong tương lai.
✅ **Phân quyền người dùng**
Tách biệt quyền truy cập và dữ liệu giữa user "province" và "admin".
✅ **Dark Mode Giao diện**
Giao diện được tối ưu với theme tối và biểu tượng rõ ràng.
---

## 🧮 **Công nghệ sử dụng**

| Loại            | Công nghệ                              |
| --------------- | -------------------------------------- |
| Frontend        | Streamlit                              |
| Backend         | Python                                 |
| Visualization   | Plotly, Matplotlib                     |
| Data Processing | Pandas, Statsmodels                    |
| Authentication  | bcrypt, Session State                  |
| Database        | CSV hoặc PostgreSQL (tùy chọn mở rộng) |
---

## 📁 **Dữ liệu mẫu**

* **DTI.csv**: Chỉ số chuyển đổi số của Việt Nam (theo năm)
* **GDP.csv**: Tốc độ tăng trưởng GDP
* **users.csv**: Thông tin tài khoản (username, password hash, role)
---
## 🧠 **Ví dụ mô hình hồi quy**

Phương trình được ước lượng:
```math
GDP_t = β₀ + β₁ * DTI_t + ε_t
```
Ứng dụng hiển thị:
* Hệ số β₁ → mức độ ảnh hưởng của DTI đến GDP
* R², p-value, và hệ số chặn (intercept)
---

## 🛠️ **Hướng phát triển**
* ✅ Kết nối PostgreSQL thay vì CSV
* ✅ Tự động cập nhật dữ liệu DTI theo tỉnh
* 🔜 Tích hợp AI để dự báo xu hướng chuyển đổi số
* 🔜 Giao diện quản trị chuyên sâu với biểu đồ thời gian thực