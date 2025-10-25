import pandas as pd
import statsmodels.api as sm
from config.settings import DATA_PATHS


def run_regression():
    """
    Run an Ordinary Least Squares (OLS) regression to estimate
    the impact of Digital Transformation indicators
    (CQS, KTS, XHS, DTI) on Vietnam's GDP.

    Returns
    -------
    model : RegressionResultsWrapper
        Fitted OLS model object for further analysis or plotting.
    """

    # =========================================================
    # 1️⃣ Load datasets
    # =========================================================
    gdp = pd.read_csv(DATA_PATHS["GDP"])
    cqs = pd.read_csv(DATA_PATHS["CQS"])
    kts = pd.read_csv(DATA_PATHS["KTS"])
    xhs = pd.read_csv(DATA_PATHS["XHS"])
    dti = pd.read_csv(DATA_PATHS["DTI"])

    # =========================================================
    # 2️⃣ Merge datasets on "Year"
    # =========================================================
    df = gdp.merge(cqs, on="Year", suffixes=("", "_CQS")) \
            .merge(kts, on="Year", suffixes=("", "_KTS")) \
            .merge(xhs, on="Year", suffixes=("", "_XHS")) \
            .merge(dti, on="Year", suffixes=("", "_DTI"))

    # Rename standardized columns (nếu cột là Value)
    df.columns = ["Year", "GDP", "CQS", "KTS", "XHS", "DTI"]

    # =========================================================
    # 3️⃣ Define variables
    # =========================================================
    y = df["GDP"]                            # Biến phụ thuộc
    X = df[["CQS", "KTS", "XHS", "DTI"]]     # Biến độc lập
    X = sm.add_constant(X)                   # Thêm hằng số β₀

    # =========================================================
    # 4️⃣ Fit OLS Regression model
    # =========================================================
    model = sm.OLS(y, X).fit()

    # =========================================================
    # 5️⃣ Return model & summary
    # =========================================================
    return model
