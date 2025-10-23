import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the input DataFrame used for DTI–GDP analysis.

    Steps performed:
    ----------------
    1. Drop missing values (NaN) across all columns.
    2. Remove invalid records where GDP growth ≤ 0.
    3. Return a cleaned DataFrame ready for modeling and visualization.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset containing at least the column 'GDP_growth'.

    Returns
    -------
    pd.DataFrame
        Cleaned dataset with valid GDP growth values only.
    """
    df = df.copy()  # avoid mutating original DataFrame

    # Ensure required column exists
    if "GDP_growth" not in df.columns:
        raise KeyError("The DataFrame must contain a 'GDP_growth' column.")

    # Drop missing values and filter positive GDP growth
    df = df.dropna()
    df = df[df["GDP_growth"] > 0]

    return df
