"""
Unit tests for regression_model.py
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


class TestRunRegression:
    """Test cases for the run_regression function."""

    @pytest.fixture
    def mock_data(self):
        """Create mock data for testing."""
        years = [2021, 2022, 2023, 2024]
        gdp_data = pd.DataFrame({
            "Year": years * 2,
            "Province": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "GDP": [100, 110, 120, 130, 200, 220, 240, 260]
        })
        cqs_data = pd.DataFrame({
            "Year": years * 2,
            "Province": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "CQS": [0.3, 0.4, 0.5, 0.6, 0.35, 0.45, 0.55, 0.65]
        })
        kts_data = pd.DataFrame({
            "Year": years * 2,
            "Province": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "KTS": [0.2, 0.3, 0.4, 0.5, 0.25, 0.35, 0.45, 0.55]
        })
        xhs_data = pd.DataFrame({
            "Year": years * 2,
            "Province": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "XHS": [0.4, 0.5, 0.6, 0.7, 0.45, 0.55, 0.65, 0.75]
        })
        dti_data = pd.DataFrame({
            "Year": years * 2,
            "Province": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "DTI": [0.3, 0.4, 0.5, 0.6, 0.35, 0.45, 0.55, 0.65]
        })
        return {
            "GDP": gdp_data,
            "CQS": cqs_data,
            "KTS": kts_data,
            "XHS": xhs_data,
            "DTI": dti_data
        }

    @patch("models.regression_model.pd.read_csv")
    def test_run_regression_dti_model(self, mock_read_csv, mock_data):
        """Test regression with DTI only model."""
        from models.regression_model import run_regression
        
        def side_effect(path):
            if "GDP" in path:
                return mock_data["GDP"]
            elif "CQS" in path:
                return mock_data["CQS"]
            elif "KTS" in path:
                return mock_data["KTS"]
            elif "XHS" in path:
                return mock_data["XHS"]
            elif "DTI" in path:
                return mock_data["DTI"]
        
        mock_read_csv.side_effect = side_effect
        
        model = run_regression(model_type="dti")
        
        # Check model has expected attributes
        assert hasattr(model, "params")
        assert hasattr(model, "rsquared")
        assert "DTI" in model.params.index
        assert "const" in model.params.index

    @patch("models.regression_model.pd.read_csv")
    def test_run_regression_components_model(self, mock_read_csv, mock_data):
        """Test regression with components model (CQS, KTS, XHS)."""
        from models.regression_model import run_regression
        
        def side_effect(path):
            if "GDP" in path:
                return mock_data["GDP"]
            elif "CQS" in path:
                return mock_data["CQS"]
            elif "KTS" in path:
                return mock_data["KTS"]
            elif "XHS" in path:
                return mock_data["XHS"]
            elif "DTI" in path:
                return mock_data["DTI"]
        
        mock_read_csv.side_effect = side_effect
        
        model = run_regression(model_type="components")
        
        # Check model has expected variables
        assert "CQS" in model.params.index
        assert "KTS" in model.params.index
        assert "XHS" in model.params.index
        assert "DTI" not in model.params.index


class TestRegressionModelIntegration:
    """Integration tests (require actual data files)."""

    @pytest.mark.skipif(True, reason="Requires actual data files")
    def test_regression_with_real_data(self):
        """Test with real data files."""
        from models.regression_model import run_regression
        
        model = run_regression(model_type="dti")
        assert model.rsquared >= 0 and model.rsquared <= 1
