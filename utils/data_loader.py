import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a dataset from the specified CSV file path.

    This function reads the data, handles basic errors,
    and caches the result to improve Streamlit performance.

    Parameters
    ----------
    file_path : str
        Path to the CSV file to be loaded.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the dataset.

    Raises
    ------
    Exception
        If the file cannot be read or does not exist.
    """
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        return df
    except Exception as e:
        raise Exception(f"Failed to load data from '{file_path}': {e}")
