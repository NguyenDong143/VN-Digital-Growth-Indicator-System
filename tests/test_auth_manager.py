"""
Unit tests cho utils/auth_manager.py.

Các test dùng database SQLite tạm (tmp_path) nên không ảnh hưởng
tới data/db/users.db của ứng dụng thật.
"""

import pytest
from datetime import datetime, timedelta


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """
    Trỏ utils.database.DB_PATH sang file SQLite tạm và khởi tạo schema.
    Patch trước khi import auth_manager để tránh chạm DB thật.
    """
    import utils.database as db

    db.DB_PATH = tmp_path / "test_users.db"
    db.init_db()

    yield db

    db.DB_PATH = tmp_path / "test_users.db"


@pytest.fixture
def auth(temp_db, monkeypatch):
    """Import lại auth_manager sau khi DB_PATH đã trỏ sang DB tạm."""
    import utils.auth_manager as auth_manager

    return auth_manager


STRONG_PW = "Str0ng@Pass"


# =========================================================
# PASSWORD POLICY
# =========================================================

class TestPasswordPolicy:
    """Kiểm tra validate_password_strength."""

    @pytest.mark.parametrize(
        "password,expected_ok",
        [
            ("Str0ng@Pass", True),
            ("Aa1@aaaa", True),          # đúng 8 ký tự
            ("Aa1@aaa", False),          # thiếu 1 ký tự
            ("str0ng@pass", False),      # thiếu chữ hoa
            ("STR0NG@PASS", False),      # thiếu chữ thường
            ("Strong@Pass", False),      # thiếu chữ số
            ("StrongPass1", False),      # thiếu ký tự đặc biệt
            ("Aa1@aaaaa", True),         # dài hơn vẫn OK
            ("", False),                 # rỗng
            ("abc", False),              # quá ngắn
        ],
    )
    def test_validate_password_strength(self, auth, password, expected_ok):
        ok, msg = auth.validate_password_strength(password)
        assert ok is expected_ok
        # Nếu không OK thì bắt buộc phải có thông báo lỗi
        if not ok:
            assert msg

    def test_message_mentions_min_length(self, auth, monkeypatch):
        import config.settings as settings

        monkeypatch.setattr(auth, "PASSWORD_MIN_LENGTH", 12)
        ok, msg = auth.validate_password_strength("Aa1@aaaa")
        assert ok is False
        assert "12" in msg


# =========================================================
# USER CRUD
# =========================================================

class TestSaveAndVerifyUser:
    """save_user / verify_user round-trip."""

    def test_save_user_hashes_password(self, auth, temp_db):
        assert auth.save_user("alice", STRONG_PW, "province") is True

        row = temp_db.get_user("alice")
        assert row is not None
        # Mật khẩu không được lưu dạng plaintext
        assert row["password"] != STRONG_PW
        assert row["password"].startswith("$2")

    def test_duplicate_username_rejected(self, auth):
        assert auth.save_user("bob", STRONG_PW, "province") is True
        assert auth.save_user("bob", STRONG_PW, "province") is False

    def test_save_user_rejects_weak_password(self, auth):
        with pytest.raises(ValueError):
            auth.save_user("weak", "1234", "province")

        assert temp_db_user_missing(auth, "weak") is True

    def test_verify_user_returns_role(self, auth):
        auth.save_user("carol", STRONG_PW, "admin")
        assert auth.verify_user("carol", STRONG_PW) == "admin"

    def test_verify_user_wrong_password(self, auth):
        auth.save_user("dave", STRONG_PW, "province")
        assert auth.verify_user("dave", "Wr0ng@Pass") is None

    def test_verify_unknown_user(self, auth):
        assert auth.verify_user("ghost", STRONG_PW) is None


def temp_db_user_missing(auth, username: str) -> bool:
    """Helper: username chưa tồn tại trong DB hay chưa."""
    return auth.get_user(username) is None


# =========================================================
# RATE LIMITING / LOCKOUT
# =========================================================

class TestLockout:
    """Kiểm tra cơ chế khóa tài khoản sau nhiều lần nhập sai."""

    def test_failed_attempts_increment(self, auth):
        auth.save_user("eve", STRONG_PW, "province")

        auth.verify_user("eve", "Wr0ng@Pass1")
        auth.verify_user("eve", "Wr0ng@Pass2")

        assert auth.get_user("eve")["failed_attempts"] == 2

    def test_successful_login_resets_counter(self, auth):
        auth.save_user("frank", STRONG_PW, "province")

        auth.verify_user("frank", "Wr0ng@Pass")
        auth.verify_user("frank", "Wr0ng@Pass")
        assert auth.get_user("frank")["failed_attempts"] == 2

        assert auth.verify_user("frank", STRONG_PW) == "province"
        assert auth.get_user("frank")["failed_attempts"] == 0
        assert auth.get_user("frank")["last_failed_at"] is None

    def test_lockout_blocks_correct_password(self, auth, monkeypatch):
        """
        Bug regression: register_login_failure ghi datetime.utcnow() còn
        _is_locked_out so sánh datetime.now() → chênh ~7h ở VN khiến
        lockout không bao giờ trigger.
        """
        import config.settings as settings

        monkeypatch.setattr(auth, "LOGIN_MAX_ATTEMPTS", 3)
        monkeypatch.setattr(auth, "LOGIN_LOCKOUT_MINUTES", 15)

        auth.save_user("grace", STRONG_PW, "province")

        for i in range(3):
            auth.verify_user("grace", f"Wr0ng@Pass{i}")

        row = auth.get_user("grace")
        assert row["failed_attempts"] >= 3

        # Đúng mật khẩu nhưng vẫn phải bị chặn vì đang lockout
        assert auth.verify_user("grace", STRONG_PW) is None

    def test_lockout_expires(self, auth, temp_db, monkeypatch):
        """Sau LOGIN_LOCKOUT_MINUTES, tài khoản phải mở khóa."""
        monkeypatch.setattr(auth, "LOGIN_MAX_ATTEMPTS", 3)
        monkeypatch.setattr(auth, "LOGIN_LOCKOUT_MINUTES", 15)

        auth.save_user("heidi", STRONG_PW, "province")

        for i in range(3):
            auth.verify_user("heidi", f"Wr0ng@Pass{i}")
        assert auth.verify_user("heidi", STRONG_PW) is None

        # Giả lập: lần sai cuối đã cách đây 20 phút (> 15 phút lockout)
        stale = (datetime.now() - timedelta(minutes=20)).isoformat(timespec="seconds")
        with temp_db.get_connection() as conn:
            conn.execute(
                "UPDATE users SET last_failed_at = ? WHERE username = ?",
                (stale, "heidi"),
            )
            conn.commit()

        assert auth.verify_user("heidi", STRONG_PW) == "province"

    def test_is_locked_out_parsing_garbage_timestamp(self, auth):
        """Timestamp hỏng không được gây crash."""
        user = {"failed_attempts": 99, "last_failed_at": "khong-phai-timestamp"}
        locked, mins = auth._is_locked_out(user)
        assert locked is False
        assert mins == 0

    def test_is_locked_out_handles_missing_fields(self, auth):
        user = {}
        assert auth._is_locked_out(user) == (False, 0)

    def test_is_locked_out_reports_minutes_remaining(self, auth, monkeypatch):
        monkeypatch.setattr(auth, "LOGIN_MAX_ATTEMPTS", 5)
        monkeypatch.setattr(auth, "LOGIN_LOCKOUT_MINUTES", 30)

        user = {
            "failed_attempts": 5,
            "last_failed_at": (datetime.now() - timedelta(minutes=10)).isoformat(
                timespec="seconds"
            ),
        }
        locked, mins = auth._is_locked_out(user)
        assert locked is True
        assert 19 <= mins <= 21


# =========================================================
# LOAD / HELPERS
# =========================================================

class TestHelpers:
    def test_load_users(self, auth):
        auth.save_user("ivan", STRONG_PW, "province")
        auth.save_user("judy", STRONG_PW, "admin")

        users = auth.load_users()
        usernames = {u["username"] for u in users}
        assert {"ivan", "judy"} <= usernames
        # load_users không được trả về mật khẩu hash
        assert all("password" not in u for u in users)

    def test_login_user_rejects_empty_input(self, auth, monkeypatch):
        import streamlit as st

        called = []
        monkeypatch.setattr(st, "warning", lambda msg: called.append(msg))
        monkeypatch.setattr(st, "error", lambda msg: called.append(msg))

        assert auth.login_user("", "") is None
        assert called, "Phải hiển thị cảnh báo khi thiếu thông tin"