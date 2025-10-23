import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_gdp(data_path: str = "data/vietnam_dti_gdp.csv", end_year: int = 2030):
    """
    Forecast Vietnam's GDP growth based on the Digital Transformation Index (DTI)
    using a simple linear regression model.

    Parameters
    ----------
    data_path : str, optional
        Path to the CSV file containing historical DTI and GDP growth data.
    end_year : int, optional
        Target forecast horizon (default: 2030).

    Returns
    -------
    tuple
        df : DataFrame
            Original dataset containing DTI and GDP growth.
        forecast_df : DataFrame
            DataFrame with predicted GDP growth values for future DTI levels.
        coef : float
            Regression coefficient (β1) – sensitivity of GDP growth to DTI.
        intercept : float
            Regression intercept (β0).
    """

    # --- Load dataset ---
    df = pd.read_csv(data_path)

    # --- Define X and y ---
    X = df[["DTI"]].values
    y = df["GDP_growth"].values

    # --- Fit Linear Regression Model ---
    model = LinearRegression().fit(X, y)

    # --- Create future DTI range for forecast ---
    last_dti = df["DTI"].iloc[-1]
    future_dti = np.arange(last_dti, last_dti + 1.5, 0.1)
    future_gdp = model.predict(future_dti.reshape(-1, 1))

    # --- Build Forecast DataFrame ---
    forecast_df = pd.DataFrame({
        "DTI": future_dti,
        "Predicted_GDP_Growth": future_gdp
    })

    return df, forecast_df, model.coef_[0], model.intercept_
