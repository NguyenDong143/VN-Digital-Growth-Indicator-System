import warnings
warnings.filterwarnings('ignore')

import pandas as pd

def clean_data(
    df: pd.DataFrame,
    gdp_col: str = "GDP_growth",
    drop_nonpositive: bool = False,
) -> pd.DataFrame:
    """
    Clean the input DataFrame used for DTI–GDP or digital transformation analysis.

    Steps performed:
    ----------------
    1. Drop rows co bat ky cot nao NaN.
    2. Neu drop_nonpositive=True, loai cac dong co gdp_col <= 0
       (mac dinh False de giu gia tri am hop le nhu suy thoai kinh te).
    3. Remove duplicate rows.
    4. Reset index.
    5. Return cleaned DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset.
    gdp_col : str, optional
        Ten cot GDP dung de filter.
    drop_nonpositive : bool, optional
        Neu True, loai bo cac dong co gia tri gdp_col <= 0.
        Mac dinh False (giu gia tri am - hop le voi GDP growth).

    Returns
    -------
    pd.DataFrame
        Cleaned dataset with valid records only.
    """
    df = df.copy()
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    target_col = None
    if gdp_col in df.columns:
        target_col = gdp_col
    elif "GDP" in df.columns:
        target_col = "GDP"
    if target_col is not None:
        df = df[df[target_col].notna()]
        if drop_nonpositive:
            df = df[df[target_col] > 0]
    df.reset_index(drop=True, inplace=True)
    return df
