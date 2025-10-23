import pandas as pd
import statsmodels.api as sm
from config.settings import DATA_PATH


def run_regression():
    """
    Run an Ordinary Least Squares (OLS) regression to estimate
    the relationship between the Digital Transformation Index (DTI)
    and Vietnam's GDP growth.

    Returns
    -------
    summary : Summary
        A formatted regression summary including coefficients,
        t-statistics, R-squared, and model diagnostics.
    """

    # --- Load dataset ---
    df = pd.read_csv(DATA_PATH)

    # --- Define independent and dependent variables ---
    X = sm.add_constant(df["DTI"])  # Add intercept (β₀)
    y = df["GDP_growth"]

    # --- Fit OLS regression model ---
    model = sm.OLS(y, X).fit()

    # --- Return summary statistics ---
    return model.summary()
