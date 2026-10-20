"""
Unit tests cho models/forecast_model.py.

Tập trung vào các edge case đã từng gây bug:
- Index mismatch giữa future_years và future_dti.
- Thiếu cột bắt buộc trong CSV.
- Dữ liệu lịch sử quá ngắn.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_csv(tmp_path):
    """Tạo 2 file CSV (DTI + GDP) trong thư mục tạm."""
    dti = pd.DataFrame({"Year": [2020, 2021, 2022, 2023], "DTI": [0.40, 0.45, 0.50, 0.55]})
    gdp = pd.DataFrame({"Year": [2020, 2021, 2022, 2023], "GDP": [5.0, 6.0, 6.5, 7.5]})

    dti_path = tmp_path / "DTI.csv"
    gdp_path = tmp_path / "GDP.csv"
    dti.to_csv(dti_path, index=False)
    gdp.to_csv(gdp_path, index=False)

    return str(dti_path), str(gdp_path)


class TestForecastHappyPath:
    def test_returns_four_values(self, sample_csv):
        from models.forecast_model import forecast_gdp

        dti_path, gdp_path = sample_csv
        result = forecast_gdp(dti_path, gdp_path, end_year=2026)

        assert len(result) == 4
        df, forecast_df, coef, intercept = result
        assert isinstance(df, pd.DataFrame)
        assert isinstance(forecast_df, pd.DataFrame)
        assert isinstance(coef, float)
        assert isinstance(intercept, float)

    def test_forecast_index_matches_years(self, sample_csv):
        """
        Regression test cho bug cũ: future_dti được tạo với độ dài khác
        future_years, gây lỗi 'Length mismatch'.
        """
        from models.forecast_model import forecast_gdp

        dti_path, gdp_path = sample_csv
        _, forecast_df, _, _ = forecast_gdp(dti_path, gdp_path, end_year=2030)

        years = forecast_df["Year"].tolist()
        assert len(years) == len(forecast_df["Predicted_DTI"])
        assert len(years) == len(forecast_df["Predicted_GDP"])
        assert years == list(range(2024, 2031))
        assert not forecast_df.empty

    def test_dti_stays_in_unit_interval(self, sample_csv):
        """Giá trị DTI dự báo phải nằm trong [0, 1] do đã được clip."""
        from models.forecast_model import forecast_gdp

        dti_path, gdp_path = sample_csv
        _, forecast_df, _, _ = forecast_gdp(dti_path, gdp_path, end_year=2060)

        assert forecast_df["Predicted_DTI"].between(0.0, 1.0).all()

    def test_history_frame_merged_correctly(self, sample_csv):
        from models.forecast_model import forecast_gdp

        dti_path, gdp_path = sample_csv
        df, _, _, _ = forecast_gdp(dti_path, gdp_path, end_year=2025)

        assert list(df.columns) == ["Year", "DTI", "GDP"]
        assert len(df) == 4
        assert not df.isna().any().any()


class TestForecastProvinceAwareMerge:
    """
    Regression test: khi CSV có cột Province, merge chỉ theo Year sẽ tạo
    cartesian product (N tỉnh × N tỉnh) và làm sai hoàn toàn hệ số hồi quy.
    """

    @pytest.fixture
    def provincial_csv(self, tmp_path):
        """3 tỉnh × 2 năm cho cả DTI và GDP."""
        provinces = ["An Giang", "Bà Rịa - Vũng Tàu", "Cà Mau"]
        rows_dti, rows_gdp = [], []
        for prov in provinces:
            for year, dti, gdp in [(2021, 0.30, 100.0), (2022, 0.50, 200.0)]:
                rows_dti.append({"Province": prov, "Year": year, "DTI": dti})
                rows_gdp.append({"Province": prov, "Year": year, "GDP": gdp})

        dti_path = tmp_path / "DTI_prov.csv"
        gdp_path = tmp_path / "GDP_prov.csv"
        pd.DataFrame(rows_dti).to_csv(dti_path, index=False)
        pd.DataFrame(rows_gdp).to_csv(gdp_path, index=False)

        return str(dti_path), str(gdp_path)

    def test_no_cartesian_product(self, provincial_csv):
        """3 tỉnh × 2 năm = 6 dòng, không phải 18 (cartesian)."""
        from models.forecast_model import forecast_gdp

        dti_path, gdp_path = provincial_csv
        df, _, _, _ = forecast_gdp(dti_path, gdp_path, end_year=2023)

        assert len(df) == 6
        assert df["Province"].nunique() == 3

    def test_rows_pair_correct_province(self, provincial_csv):
        """DTI và GDP phải thuộc cùng một tỉnh, không bị cross-product."""
        from models.forecast_model import forecast_gdp

        dti_path, gdp_path = provincial_csv
        df, _, _, _ = forecast_gdp(dti_path, gdp_path, end_year=2023)

        # Mỗi tỉnh có đúng 1 giá trị DTI và 1 GDP tương ứng theo năm
        for province, group in df.groupby("Province"):
            assert group["Year"].nunique() == 2
            assert not group.duplicated(subset=["Year"]).any()

    def test_coefficient_matches_known_pairing(self, provincial_csv):
        """
        Dữ liệu: DTI ∈ {0.3, 0.5}, GDP ∈ {100, 200} → đường thẳng GDP = 500·DTI − 50.
        Nếu merge sai thành cartesian product, hệ số sẽ khác hẳn.
        """
        from models.forecast_model import forecast_gdp

        dti_path, gdp_path = provincial_csv
        _, _, coef, intercept = forecast_gdp(dti_path, gdp_path, end_year=2023)

        assert coef == pytest.approx(500.0, rel=1e-6)
        assert intercept == pytest.approx(-50.0, rel=1e-6)

    def test_duplicate_province_year_deduped(self, tmp_path):
        """Bản ghi trùng (Province, Year) phải được loại bỏ."""
        from models.forecast_model import forecast_gdp

        dti = pd.DataFrame({
            "Province": ["A", "A", "B"],
            "Year": [2021, 2021, 2021],
            "DTI": [0.3, 0.9, 0.5],
        })
        gdp = pd.DataFrame({
            "Province": ["A", "A", "B"],
            "Year": [2021, 2021, 2021],
            "GDP": [10.0, 20.0, 30.0],
        })

        dti_path = tmp_path / "dti_dup.csv"
        gdp_path = tmp_path / "gdp_dup.csv"
        dti.to_csv(dti_path, index=False)
        gdp.to_csv(gdp_path, index=False)

        df, _, _, _ = forecast_gdp(str(dti_path), str(gdp_path), end_year=2022)
        assert len(df) == 2
        assert not df.duplicated(subset=["Province", "Year"]).any()


class TestForecastAcceptsValueColumn:
    """CSV dùng tên cột 'Value' thay vì 'DTI'/'GDP' vẫn phải chạy được."""

    def test_value_column_alias(self, tmp_path):
        from models.forecast_model import forecast_gdp

        dti = pd.DataFrame({"Year": [2020, 2021, 2022], "Value": [0.3, 0.4, 0.5]})
        gdp = pd.DataFrame({"Year": [2020, 2021, 2022], "Value": [5.0, 6.0, 7.0]})

        dti_path = tmp_path / "dti_v.csv"
        gdp_path = tmp_path / "gdp_v.csv"
        dti.to_csv(dti_path, index=False)
        gdp.to_csv(gdp_path, index=False)

        _, forecast_df, _, _ = forecast_gdp(str(dti_path), str(gdp_path), end_year=2024)
        # Dữ liệu lịch sử kết thúc ở 2022 → dự báo 2023 và 2024.
        assert forecast_df["Year"].tolist() == [2023, 2024]
        assert len(forecast_df) == 2


class TestForecastValidation:
    def test_missing_year_column(self, tmp_path):
        from models.forecast_model import forecast_gdp

        dti_path = tmp_path / "dti_bad.csv"
        gdp_path = tmp_path / "gdp_bad.csv"
        pd.DataFrame({"DTI": [0.4, 0.5]}).to_csv(dti_path, index=False)
        pd.DataFrame({"GDP": [5.0, 6.0]}).to_csv(gdp_path, index=False)

        with pytest.raises(ValueError, match="Year"):
            forecast_gdp(str(dti_path), str(gdp_path))

    def test_missing_value_column(self, tmp_path):
        from models.forecast_model import forecast_gdp

        dti_path = tmp_path / "dti_nodti.csv"
        gdp_path = tmp_path / "gdp_nogdp.csv"
        pd.DataFrame({"Year": [2020, 2021], "Foo": [1, 2]}).to_csv(dti_path, index=False)
        pd.DataFrame({"Year": [2020, 2021], "Bar": [1, 2]}).to_csv(gdp_path, index=False)

        with pytest.raises(ValueError):
            forecast_gdp(str(dti_path), str(gdp_path))

    def test_insufficient_history(self, tmp_path):
        from models.forecast_model import forecast_gdp

        dti_path = tmp_path / "dti_one.csv"
        gdp_path = tmp_path / "gdp_one.csv"
        pd.DataFrame({"Year": [2020], "DTI": [0.4]}).to_csv(dti_path, index=False)
        pd.DataFrame({"Year": [2020], "GDP": [5.0]}).to_csv(gdp_path, index=False)

        with pytest.raises(ValueError, match="2 dòng"):
            forecast_gdp(str(dti_path), str(gdp_path))

    def test_no_overlapping_years(self, tmp_path):
        """DTI và GDP không giao nhau năm nào → không đủ dữ liệu để fit."""
        from models.forecast_model import forecast_gdp

        dti_path = tmp_path / "dti_x.csv"
        gdp_path = tmp_path / "gdp_x.csv"
        pd.DataFrame({"Year": [2000, 2001], "DTI": [0.1, 0.2]}).to_csv(dti_path, index=False)
        pd.DataFrame({"Year": [2020, 2021], "GDP": [5.0, 6.0]}).to_csv(gdp_path, index=False)

        with pytest.raises(ValueError):
            forecast_gdp(str(dti_path), str(gdp_path))

    def test_end_year_before_history(self, tmp_path):
        """end_year <= năm cuối dữ liệu → không có năm dự báo, nhưng không crash."""
        from models.forecast_model import forecast_gdp

        dti_path = tmp_path / "dti_p.csv"
        gdp_path = tmp_path / "gdp_p.csv"
        pd.DataFrame({"Year": [2020, 2021, 2022], "DTI": [0.3, 0.4, 0.5]}).to_csv(
            dti_path, index=False
        )
        pd.DataFrame({"Year": [2020, 2021, 2022], "GDP": [5.0, 6.0, 7.0]}).to_csv(
            gdp_path, index=False
        )

        _, forecast_df, _, _ = forecast_gdp(str(dti_path), str(gdp_path), end_year=2021)
        assert forecast_df.empty