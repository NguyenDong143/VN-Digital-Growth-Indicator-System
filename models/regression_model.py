import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import statsmodels.api as sm
from config.settings import DATA_PATHS


def run_regression(model_type="dti"):
    """
    Run an Ordinary Least Squares (OLS) regression to estimate
    the impact of Digital Transformation indicators on Vietnam's GDP.

    Parameters
    ----------
    model_type : str
        - "dti": Use only DTI (composite index) - avoids multicollinearity
        - "components": Use CQS, KTS, XHS (individual pillars)
        - "all": Use all indicators (WARNING: causes multicollinearity)

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
    # 2️⃣ Aggregate by Year (mean across provinces cho tính nhất quán)
    # =========================================================
    gdp_agg = "mean" if "GDP" in gdp.columns else None
    gdp = gdp.groupby("Year", as_index=False)["GDP"].mean() if gdp_agg else gdp
    cqs = cqs.groupby("Year", as_index=False)["CQS"].mean()
    kts = kts.groupby("Year", as_index=False)["KTS"].mean()
    xhs = xhs.groupby("Year", as_index=False)["XHS"].mean()
    dti = dti.groupby("Year", as_index=False)["DTI"].mean()

    # =========================================================
    # 3️⃣ Merge datasets on "Year"
    # =========================================================
    df = gdp.merge(cqs, on="Year") \
           .merge(kts, on="Year") \
           .merge(xhs, on="Year") \
           .merge(dti, on="Year")

    # =========================================================
    # 4️⃣ Define variables based on model_type
    # =========================================================
    y = df["GDP"]  # Dependent variable

    if model_type == "dti":
        # Use only DTI (composite index) - recommended to avoid multicollinearity
        X = df[["DTI"]]
    elif model_type == "components":
        # Use individual pillars (CQS, KTS, XHS)
        X = df[["CQS", "KTS", "XHS"]]
    else:
        # Use all (WARNING: multicollinearity issue)
        X = df[["CQS", "KTS", "XHS", "DTI"]]

    X = sm.add_constant(X)  # Add intercept β₀

    # =========================================================
    # 5️⃣ Fit OLS Regression model
    # =========================================================
    model = sm.OLS(y, X).fit()

    return model

