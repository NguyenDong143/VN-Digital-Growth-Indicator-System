## 🧱 Cấu trúc dự án

```
DIGITAL_GDP_DASHBOARD/
│
├── main.py                        # File chính (chạy ứng dụng Streamlit)
│
├── config/
│   └── settings.py                # Cấu hình trang, theme, đường dẫn dữ liệu
│
├── models/
│   ├── regression_model.py        # Hồi quy : GDP_growth ~ DTI
│   ├── forecast_model.py          # Dự báo GDP dựa trên DTI (Linear Regression)
│
├── ui/
│   ├── overview_tab.py            # Tab Tổng quan GDP & DTI
│   ├── components_tab.py          # Tab 3 trụ cột chuyển đổi số
│   ├── roi_tab.py                 # Tab ROI đầu tư số
│   ├── regression_tab.py          # Tab hồi quy kinh tế lượng
│   └── style.py                   # Tùy chỉnh giao diện dark mode
│
├── utils/
│   ├── data_loader.py             # Hàm load dữ liệu CSV
│   └── data_cleaner.py            # Hàm xử lý, làm sạch dữ liệu
│
├── data/
│   └── vietnam_dti_gdp.csv        # Dữ liệu DTI & GDP (2020–2028, ví dụ minh họa)
│
├── requirements.txt               # Danh sách thư viện cần cài
└── README.md                      # Tài liệu hướng dẫn 
```

## 🚀 Cách chạy ứng dụng

### 1️⃣ Cài đặt thư viện

```bash
pip install -r requirements.txt
python -m pip install -r requirements.txt
```

### 2️⃣ Chạy dashboard

```bash
# streamlit run main.py

python -m streamlit run main.py
```

Ứng dụng sẽ mở tự động tại:
👉 [http://localhost:8501](http://localhost:8501)

