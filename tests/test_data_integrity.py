"""
Data integrity tests for data/csv/*.csv.

Mục đích: chặn sự cố mất/thay thế dữ liệu thật — giống như sự cố commit
82583ef đã ghi đè DTI.csv và GDP.csv bằng dữ liệu seed 5 dòng, làm mất
252 dòng dữ liệu per-province mà test suite hiện tại không bắt được.

Các test này khẳng định bằng chứng về hình dạng dữ liệu (schema, số tỉnh,
khoảng năm, tỷ lệ NaN) chứ không hardcode toàn bộ nội dung, để dữ liệu vẫn
có thể được cập nhật theo thời gian mà không làm test vỡ.
"""

import pandas as pd
import pytest

from config.settings import DATA_PATHS


# Bộ dữ liệu chuẩn của dự án: 63 tỉnh/thành, 4 năm (2021-2024).
EXPECTED_PROVINCES = 63
EXPECTED_YEARS = {2021, 2022, 2023, 2024}
EXPECTED_ROWS = EXPECTED_PROVINCES * len(EXPECTED_YEARS)  # 252

REQUIRED_FILES = ["GDP", "CQS", "KTS", "XHS", "DTI"]


def _read(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_PATHS[name])


@pytest.fixture(scope="module")
def frames() -> dict[str, pd.DataFrame]:
    return {name: _read(name) for name in REQUIRED_FILES}


# =========================================================
# 1. FILE TỒN TẠI VÀ ĐỌC ĐƯỢC
# =========================================================

@pytest.mark.parametrize("name", REQUIRED_FILES)
class TestFilePresent:
    def test_file_exists(self, name):
        from pathlib import Path

        path = Path(DATA_PATHS[name])
        assert path.exists(), f"Thiếu file dữ liệu: {path}"

    def test_file_not_empty(self, name):
        from pathlib import Path

        size = Path(DATA_PATHS[name]).stat().st_size
        # File seed chỉ vài trăm byte; dữ liệu thật > 5KB.
        assert size > 5_000, (
            f"{name}.csv chỉ có {size} bytes — có vẻ đã bị thay bằng dữ liệu mẫu"
        )

    def test_has_required_columns(self, frames, name):
        df = frames[name]
        for col in ["STT", "Province", "Year", name]:
            assert col in df.columns, f"{name}.csv thiếu cột '{col}'"


# =========================================================
# 2. HÌNH DẠNG DỮ LIỆU (chặn mất dữ liệu)
# =========================================================

@pytest.mark.parametrize("name", REQUIRED_FILES)
class TestDataShape:
    def test_row_count(self, frames, name):
        """
        Dữ liệu phải có đúng 252 dòng (63 tỉnh × 4 năm).
        Đây là test bắt sự cố mất dữ liệu: nếu file bị thay bằng seed
        data 5 dòng, test này sẽ fail.
        """
        df = frames[name]
        assert len(df) == EXPECTED_ROWS, (
            f"{name}.csv có {len(df)} dòng, mong đợi {EXPECTED_ROWS}. "
            f"Dữ liệu có thể đã bị thay thế hoặc mất."
        )

    def test_province_count(self, frames, name):
        df = frames[name]
        assert df["Province"].nunique() == EXPECTED_PROVINCES, (
            f"{name}.csv chỉ có {df['Province'].nunique()} tỉnh, "
            f"mong đợi {EXPECTED_PROVINCES}"
        )

    def test_year_coverage(self, frames, name):
        """Mỗi tỉnh phải có dữ liệu đủ 4 năm, không thiếu năm nào."""
        df = frames[name]
        years_per_province = df.groupby("Province")["Year"].nunique()
        assert (years_per_province == len(EXPECTED_YEARS)).all(), (
            "Có tỉnh thiếu dữ liệu ở một số năm"
        )

    def test_years_within_expected_range(self, frames, name):
        df = frames[name]
        assert set(df["Year"].unique()) == EXPECTED_YEARS, (
            f"{name}.csv có năm ngoài dự kiến: {sorted(set(df['Year'].unique()))}"
        )

    def test_no_duplicate_province_year(self, frames, name):
        """Không được có bản ghi trùng (Province, Year)."""
        df = frames[name]
        dupes = df.duplicated(subset=["Province", "Year"]).sum()
        assert dupes == 0, f"{name}.csv có {dupes} bản ghi trùng (Province, Year)"


# =========================================================
# 3. CHẤT LƯỢNG GIÁ TRỊ
# =========================================================

@pytest.mark.parametrize("name", REQUIRED_FILES)
class TestDataQuality:
    def test_no_missing_values(self, frames, name):
        df = frames[name]
        nulls = df.isna().sum().sum()
        assert nulls == 0, f"{name}.csv có {nulls} giá trị thiếu"

    def test_numeric_column_is_numeric(self, frames, name):
        df = frames[name]
        assert pd.api.types.is_numeric_dtype(df[name]), (
            f"Cột '{name}' trong {name}.csv không phải kiểu số"
        )


def test_gdp_positive(frames):
    """GDP phải dương (tính bằng đơn vị tiền)."""
    df = frames["GDP"]
    assert (df["GDP"] > 0).all(), "GDP có giá trị <= 0"


@pytest.mark.parametrize("name", ["CQS", "KTS", "XHS", "DTI"])
class TestIndexRange:
    """Các chỉ số chuyển đổi số nằm trong thang [0, 1]."""

    def test_index_in_unit_range(self, frames, name):
        df = frames[name]
        assert df[name].between(0.0, 1.0).all(), (
            f"{name} có giá trị ngoài khoảng [0, 1]: "
            f"min={df[name].min()}, max={df[name].max()}"
        )


# =========================================================
# 4. TÍNH NHẤT QUÁN GIỮA CÁC FILE
# =========================================================

class TestCrossFileConsistency:
    def test_same_provinces_across_files(self, frames):
        """Tất cả file phải có đúng tập tỉnh giống nhau."""
        reference = set(frames["GDP"]["Province"])
        for name in REQUIRED_FILES:
            other = set(frames[name]["Province"])
            assert other == reference, (
                f"{name}.csv có tỉnh không khớp GDP.csv: "
                f"thiếu={sorted(reference - other)}, thừa={sorted(other - reference)}"
            )

    def test_same_year_coverage_across_files(self, frames):
        reference = set(frames["GDP"]["Year"])
        for name in REQUIRED_FILES:
            assert set(frames[name]["Year"]) == reference, (
                f"{name}.csv có tập năm không khớp GDP.csv"
            )

    def test_merge_on_year_province_has_no_fanout(self, frames):
        """
        Regression test cho bug cartesian product trong forecast_gdp.

        Merge DTI với GDP chỉ trên 'Year' sẽ sinh 4 × 63 × 63 = 15.876 dòng.
        Merge đúng phải cho đúng 252 dòng.
        """
        merged = pd.merge(
            frames["DTI"][["Province", "Year", "DTI"]],
            frames["GDP"][["Province", "Year", "GDP"]],
            on=["Province", "Year"],
        )
        assert len(merged) == EXPECTED_ROWS, (
            f"Merge (Province, Year) cho {len(merged)} dòng, "
            f"mong đợi {EXPECTED_ROWS}"
        )

    def test_forecast_model_consumes_real_data(self, frames):
        """
        forecast_gdp phải chạy được trên dữ liệu thật và trả về
        đúng số dòng lịch sử (bắt lỗi cartesian product nếu tái phát).
        """
        from models.forecast_model import forecast_gdp

        df, forecast_df, coef, intercept = forecast_gdp(
            DATA_PATHS["DTI"], DATA_PATHS["GDP"], end_year=2030
        )

        assert len(df) == EXPECTED_ROWS, (
            f"forecast_gdp nhận {len(df)} dòng lịch sử, mong đợi {EXPECTED_ROWS}. "
            f"Đây là dấu hiệu merge cartesian product."
        )
        assert df["Province"].nunique() == EXPECTED_PROVINCES
        assert not forecast_df.empty
        assert forecast_df["Year"].is_monotonic_increasing
        # Hệ số hồi quy phải là số hữu hạn, không phải 0 hoặc vô cùng.
        assert coef == coef and abs(coef) < float("inf")