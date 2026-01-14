import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from config.settings import DATA_PATHS


def forecast_gdp(data_path: str = DATA_PATHS["DTI"], end_year: int = 2030):
    """
    Forecast Vietnam's GDP growth based on the Digital Transformation Index (DTI)
    using a simple linear regression model.

    Parameters
    ----------
    data_path : str, optional
        Path to the CSV file containing historical DTI and GDP data.
        Default: config.settings.DATA_PATHS["DTI"].
    end_year : int, optional
        Target forecast horizon (default: 2030).

    Returns
    -------
    tuple
        df : DataFrame
            Original dataset containing Year, DTI, and GDP.
        forecast_df : DataFrame
            DataFrame with predicted GDP growth values for future DTI levels.
        coef : float
            Regression coefficient (β1) – sensitivity of GDP growth to DTI.
        intercept : float
            Regression intercept (β0).
    """

    # --- Load dataset ---
    df_dti = pd.read_csv(DATA_PATHS["DTI"])
    df_gdp = pd.read_csv(DATA_PATHS["GDP"])

    # Kiểm tra và gộp dữ liệu theo Year
    if "Year" in df_dti.columns and "Year" in df_gdp.columns:
        df = pd.merge(df_dti, df_gdp, on="Year")
    else:
        raise ValueError("Cả hai file DTI.csv và GDP.csv cần có cột 'Year'.")

    # Đặt lại tên cột nếu cần
    if "Value" in df.columns:
        df.rename(columns={"Value_x": "DTI", "Value_y": "GDP"}, inplace=True)

    # --- Chuẩn bị dữ liệu ---
    X = df[["DTI"]].values
    y = df["GDP"].values

    # --- Huấn luyện mô hình Linear Regression ---
    model = LinearRegression().fit(X, y)

    # --- Tạo khoảng giá trị DTI tương lai ---
    last_year = int(df["Year"].max())
    future_years = np.arange(last_year + 1, end_year + 1)
    last_dti = float(df["DTI"].iloc[-1])

    # Giả định DTI tăng đều 0.2 điểm/năm (hoặc tùy chỉnh)
    future_dti = np.arange(last_dti, last_dti + 0.2 * len(future_years), 0.2)
    future_gdp = model.predict(future_dti.reshape(-1, 1))

    # --- Dự báo GDP ---
    forecast_df = pd.DataFrame({
        "Year": future_years,
        "Predicted_DTI": future_dti[:len(future_years)],
        "Predicted_GDP": future_gdp[:len(future_years)]
    })

    return df, forecast_df, model.coef_[0], model.intercept_
