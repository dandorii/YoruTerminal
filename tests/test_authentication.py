import pytest

from auth.accounts import authenticate_user, register_user


def test_login_accepts_correct_password(test_database):
    user_id = register_user("NightOwl", "a-long-test-password")

    assert authenticate_user(
        "NightOwl", "a-long-test-password"
    ) == user_id


def test_login_rejects_wrong_password(test_database):
    register_user("NightOwl", "a-long-test-password")

    assert authenticate_user("NightOwl", "incorrect-password") is None


def test_login_rejects_unknown_username(test_database):
    assert authenticate_user(
        "UnknownPlayer", "a-long-test-password"
    ) is None


def test_login_is_case_insensitive_for_username(test_database):
    user_id = register_user("NightOwl", "a-long-test-password")

    assert authenticate_user(
        "nightowl", "a-long-test-password"
    ) == user_id
