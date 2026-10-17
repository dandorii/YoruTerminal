
from rich.console import Console

from ui import mission_history


def test_mission_history_shows_empty_state(
    test_database, monkeypatch
):
    output = Console(record=True)
    monkeypatch.setattr(mission_history, "console", output)

    mission_history.show_mission_history(user_id=999)

    rendered = output.export_text()
    assert "MISSION HISTORY" in rendered
    assert "NO RECORDS FOUND" in rendered
    assert "No mission attempts recorded yet." in rendered


def test_mission_history_shows_recorded_attempt(
    test_database, monkeypatch
):
    from database.db import get_connection
    from missions.seed import seed_missions

    seed_missions()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            ("history_tester", "test-hash"),
        )
        user_id = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            ("history_tester",),
        ).fetchone()["id"]

        connection.execute(
            """
            INSERT INTO mission_results
                (user_id, mission_id, score, completed, xp_awarded)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, "phishing-001", 90, 1, 90),
        )

    output = Console(record=True)
    monkeypatch.setattr(mission_history, "console", output)

    mission_history.show_mission_history(user_id)

    rendered = output.export_text()
    assert "Suspicious Message" in rendered
    assert "PHISHING-001" in rendered
    assert "90/100" in rendered
    assert "COMPLETE" in rendered
    assert "+90" in rendered
