import pytest

from argon2 import PasswordHasher

from auth.accounts import RegistrationError, register_user
from database.db import get_connection


def test_register_creates_user_and_progress(test_database):
    user_id = register_user("NightOwl", "a-long-test-password")

    with get_connection() as connection:
        user = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

        progress = connection.execute(
            "SELECT * FROM player_progress WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    assert user["username"] == "NightOwl"
    assert PasswordHasher().verify(
        user["password_hash"], "a-long-test-password"
    )
    assert user["password_hash"] != "a-long-test-password"
    assert progress["xp"] == 0
    assert progress["rank"] == "Novice"


def test_register_rejects_duplicate_username(test_database):
    register_user("NightOwl", "a-long-test-password")

    with pytest.raises(RegistrationError, match="already taken"):
        register_user("nightowl", "another-long-password")


@pytest.mark.parametrize("username", ["ab", "bad name", "bad/name"])
def test_register_rejects_invalid_username(test_database, username):
    with pytest.raises(RegistrationError):
        register_user(username, "a-long-test-password")


def test_register_rejects_short_password(test_database):
    with pytest.raises(RegistrationError, match="12 characters"):
        register_user("NightOwl", "short")
