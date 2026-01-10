import pandas as pd

def clean_data(df: pd.DataFrame, gdp_col: str = "GDP_growth") -> pd.DataFrame:
    """
    Clean the input DataFrame used for DTI–GDP or digital transformation analysis.

    Steps performed:
    ----------------
    1. Drop missing values (NaN) across all columns.
    2. Remove invalid records where GDP growth ≤ 0 (if the column exists).
    3. Remove duplicate rows (if any).
    4. Reset the DataFrame index.
    5. Return a cleaned DataFrame ready for modeling and visualization.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset containing at least the column `GDP_growth` or `GDP`.
    gdp_col : str, optional
        The column name used for GDP growth filtering (default: "GDP_growth").

    Returns
    -------
    pd.DataFrame
        Cleaned dataset with valid records only.
    """
    df = df.copy()  # Avoid mutating original DataFrame

    # --- Drop missing values ---
    df.dropna(inplace=True)

    # --- Remove duplicates ---
    df.drop_duplicates(inplace=True)

    # --- Filter invalid GDP values (allow negative growth, only remove NaN) ---
    if gdp_col in df.columns:
        df = df[df[gdp_col].notna()]
    elif "GDP" in df.columns:
        df = df[df["GDP"].notna()]
    # Note: GDP growth can be negative during recessions, so we don't filter by value

    # --- Reset index after cleaning ---
    df.reset_index(drop=True, inplace=True)

    return df
