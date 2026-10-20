import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_gdp(
    data_path: str = "data/csv/DTI.csv",
    gdp_path: str = "data/csv/GDP.csv",
    end_year: int = 2030,
):
    """
    Forecast Vietnam's GDP growth based on the Digital Transformation Index (DTI)
    using a simple linear regression model.

    Parameters
    ----------
    data_path : str
        Đường dẫn CSV chứa DTI theo năm (bắt buộc cột 'Year' và 'DTI' hoặc 'Value').
    gdp_path : str
        Đường dẫn CSV chứa GDP theo năm (bắt buộc cột 'Year' và 'GDP' hoặc 'Value').
    end_year : int
        Năm cuối cùng của khoảng dự báo (mặc định 2030).

    Returns
    -------
    tuple (df, forecast_df, coef, intercept)
        df : DataFrame gốc sau khi merge (Year, DTI, GDP).
        forecast_df : DataFrame kết quả dự báo (Year, Predicted_DTI, Predicted_GDP).
        coef : hệ số góc của hồi quy tuyến tính DTI → GDP.
        intercept : hệ số chặn.
    """
    # --- Load dataset (dùng đúng data_path được truyền vào, không hardcode) ---
    df_dti = pd.read_csv(data_path)
    df_gdp = pd.read_csv(gdp_path)

    # Chuẩn hóa tên cột: chấp nhận cả 'Value' và tên chuẩn
    if "DTI" not in df_dti.columns and "Value" in df_dti.columns:
        df_dti = df_dti.rename(columns={"Value": "DTI"})
    if "GDP" not in df_gdp.columns and "Value" in df_gdp.columns:
        df_gdp = df_gdp.rename(columns={"Value": "GDP"})

    if "Year" not in df_dti.columns or "Year" not in df_gdp.columns:
        raise ValueError("Cả hai file cần có cột 'Year'.")
    if "DTI" not in df_dti.columns:
        raise ValueError(f"File {data_path} thiếu cột 'DTI' hoặc 'Value'.")
    if "GDP" not in df_gdp.columns:
        raise ValueError(f"File {gdp_path} thiếu cột 'GDP' hoặc 'Value'.")

    # Dữ liệu có cấu trúc theo tỉnh (mỗi tỉnh một dòng cho mỗi năm) nên bắt buộc
    # merge theo (Year, Province). Chỉ merge theo Year sẽ tạo cartesian product
    # (63 tỉnh × 63 tỉnh × 4 năm = 15.876 dòng thay vì 252) và làm sai hệ số hồi quy.
    merge_keys = ["Year"]
    if "Province" in df_dti.columns and "Province" in df_gdp.columns:
        merge_keys.append("Province")

    df = pd.merge(
        df_dti[[*merge_keys, "DTI"]],
        df_gdp[[*merge_keys, "GDP"]],
        on=merge_keys,
    )
    df = df.dropna(subset=["Year", "DTI", "GDP"])

    # Loại bỏ bản ghi trùng (Year, Province) — giữ bản ghi đầu tiên.
    df = df.drop_duplicates(subset=merge_keys, keep="first")

    if len(df) < 2:
        raise ValueError(
            "Cần ít nhất 2 dòng dữ liệu lịch sử để fit mô hình hồi quy."
        )

    # --- Huấn luyện Linear Regression ---
    X = df[["DTI"]].values
    y = df["GDP"].values
    model = LinearRegression().fit(X, y)

    # --- Sinh giá trị DTI tương lai, đảm bảo length = len(future_years) ---
    last_year = int(df["Year"].max())
    last_dti = float(df["DTI"].iloc[-1])
    future_years = np.arange(last_year + 1, end_year + 1)
    n_future = len(future_years)

    # Không có năm nào cần dự báo (end_year <= năm cuối dữ liệu).
    # Trả về DataFrame rỗng đúng schema thay vì để sklearn ném lỗi
    # "Found array with 0 sample(s)" khi predict với mảng rỗng.
    if n_future == 0:
        empty_forecast = pd.DataFrame({
            "Year": future_years,
            "Predicted_DTI": pd.Series(dtype="float64"),
            "Predicted_GDP": pd.Series(dtype="float64"),
        })
        return df, empty_forecast, float(model.coef_[0]), float(model.intercept_)

    # Tốc độ tăng DTI/năm dựa trên lịch sử (cap ở [0, 1])
    if len(df) >= 2:
        avg_dti_growth = (df["DTI"].iloc[-1] - df["DTI"].iloc[0]) / max(
            1, (df["Year"].iloc[-1] - df["Year"].iloc[0])
        )
    else:
        avg_dti_growth = 0.05

    future_dti = np.array(
        [
            max(0.0, min(1.0, last_dti + avg_dti_growth * (i + 1)))
            for i in range(n_future)
        ],
        dtype=float,
    )

    # Predict — đảm bảo kích thước khớp
    future_gdp = model.predict(future_dti.reshape(-1, 1))
    assert len(future_gdp) == n_future, (
        f"Length mismatch: future_gdp={len(future_gdp)} vs future_years={n_future}"
    )

    forecast_df = pd.DataFrame({
        "Year": future_years,
        "Predicted_DTI": np.round(future_dti, 4),
        "Predicted_GDP": np.round(future_gdp, 2),
    })

    return df, forecast_df, model.coef_[0], model.intercept_
