import pytest

from database.db import init_db


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
