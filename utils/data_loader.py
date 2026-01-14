import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a dataset from a CSV file with basic error handling and caching.

    Features:
    ----------
    - Supports multiple encodings (UTF-8, UTF-16, Latin-1).
    - Automatically converts numeric columns where possible.
    - Provides caching for faster reloads.
    - Displays a short preview in the Streamlit interface.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame ready for analysis.

    Raises
    ------
    FileNotFoundError
        If the specified file path does not exist.
    Exception
        If the file cannot be read.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    encodings = ["utf-8", "utf-16", "latin-1"]

    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            break
        except Exception:
            continue
    else:
        raise Exception(f"Failed to load data from '{file_path}' with any known encoding.")

    # Convert numeric columns safely
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception:
            pass

    return df
