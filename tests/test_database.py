import sqlite3

import pytest

from database.db import get_connection, init_db


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Give each test an isolated temporary database."""
    database_path = tmp_path / "test_yoru_terminal.db"

    monkeypatch.setattr(
        "database.db.DATABASE_PATH",
        database_path,
    )
    monkeypatch.setattr(
        "database.db.DATABASE_DIR",
        tmp_path,
    )

    init_db()
    return database_path


def test_init_db_creates_all_tables(test_database):
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table'"
        ).fetchall()

    table_names = {row["name"] for row in rows}

    assert {
        "users",
        "player_progress",
        "missions",
        "mission_results",
        "mission_completions",
    }.issubset(table_names)


def test_foreign_keys_are_enabled(test_database):
    with get_connection() as connection:
        enabled = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]

    assert enabled == 1


def test_duplicate_usernames_are_rejected(test_database):
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO users (username, password_hash) "
            "VALUES (?, ?)",
            ("NightOwl", "test-hash"),
        )

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO users (username, password_hash) "
                "VALUES (?, ?)",
                ("nightowl", "another-test-hash"),
            )


def test_negative_xp_is_rejected(test_database):
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO users (username, password_hash) "
            "VALUES (?, ?)",
            ("TestPlayer", "test-hash"),
        )

        user_id = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            ("TestPlayer",),
        ).fetchone()["id"]

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO player_progress (user_id, xp) "
                "VALUES (?, ?)",
                (user_id, -1),
            )
