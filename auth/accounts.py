import sqlite3

from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    VerificationError,
    VerifyMismatchError,
)

from database.db import get_connection


_password_hasher = PasswordHasher()


class RegistrationError(Exception):
    """Raised when account registration cannot be completed."""


def register_user(username: str, password: str) -> int:
    """Register a user and return the new account ID."""
    username = username.strip()

    if not 3 <= len(username) <= 24:
        raise RegistrationError(
            "Username must be between 3 and 24 characters."
        )

    if not username.isascii() or not all(
        char.isalnum() or char in "_-" for char in username
    ):
        raise RegistrationError(
            "Username may contain only letters, numbers, "
            "underscores, and hyphens."
        )

    if len(password) < 12:
        raise RegistrationError(
            "Password must be at least 12 characters long."
        )

    try:
        password_hash = _password_hasher.hash(password)
    except HashingError as exc:
        raise RegistrationError(
            "Password could not be processed."
        ) from exc

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO users (username, password_hash) "
                "VALUES (?, ?)",
                (username, password_hash),
            )
            user_id = cursor.lastrowid

            connection.execute(
                "INSERT INTO player_progress (user_id) VALUES (?)",
                (user_id,),
            )

            return user_id

    except sqlite3.IntegrityError as exc:
        if "users.username" in str(exc):
            raise RegistrationError(
                "That username is already taken."
            ) from exc
        raise RegistrationError(
            "The account could not be created."
        ) from exc


def authenticate_user(username: str, password: str) -> int | None:
    """Return the account ID if credentials are valid; otherwise None."""
    username = username.strip()

    with get_connection() as connection:
        user = connection.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if user is None:
        return None

    try:
        if _password_hasher.verify(user["password_hash"], password):
            return user["id"]
    except (VerifyMismatchError, VerificationError):
        return None

    return None
