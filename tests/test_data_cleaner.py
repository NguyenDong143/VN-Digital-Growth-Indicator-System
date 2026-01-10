"""
Unit tests for data_cleaner.py
"""

import pytest
import pandas as pd
from utils.data_cleaner import clean_data


class TestCleanData:
    """Test cases for the clean_data function."""

    def test_removes_nan_values(self):
        """Test that NaN values are removed."""
        df = pd.DataFrame({
            "GDP": [100, None, 120, 130],
            "Year": [2021, 2022, 2023, 2024]
        })
        result = clean_data(df, gdp_col="GDP")
        assert len(result) == 3
        assert result["GDP"].isna().sum() == 0

    def test_removes_duplicates(self):
        """Test that duplicate rows are removed."""
        df = pd.DataFrame({
            "GDP": [100, 100, 120],
            "Year": [2021, 2021, 2022]
        })
        result = clean_data(df, gdp_col="GDP")
        assert len(result) == 2

    def test_allows_negative_gdp_growth(self):
        """Test that negative GDP growth values are allowed (for recessions)."""
        df = pd.DataFrame({
            "GDP_growth": [-2.5, 3.0, 5.0],
            "Year": [2020, 2021, 2022]
        })
        result = clean_data(df, gdp_col="GDP_growth")
        
        # Should keep all 3 rows including negative growth
        assert len(result) == 3
        assert -2.5 in result["GDP_growth"].values

    def test_resets_index(self):
        """Test that index is reset after cleaning."""
        df = pd.DataFrame({
            "GDP": [100, None, 120],
            "Year": [2021, 2022, 2023]
        })
        result = clean_data(df, gdp_col="GDP")
        
        # Index should be 0, 1 not 0, 2
        assert list(result.index) == [0, 1]

    def test_fallback_to_gdp_column(self):
        """Test fallback to 'GDP' column when gdp_col not found."""
        df = pd.DataFrame({
            "GDP": [100, None, 120],
            "Year": [2021, 2022, 2023]
        })
        result = clean_data(df, gdp_col="NonExistent")
        assert len(result) == 2

    def test_preserves_original_dataframe(self):
        """Test that original DataFrame is not modified."""
        df = pd.DataFrame({
            "GDP": [100, None, 120],
            "Year": [2021, 2022, 2023]
        })
        original_len = len(df)
        clean_data(df, gdp_col="GDP")
        
        assert len(df) == original_len
