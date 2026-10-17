
from database.db import get_connection
from missions.seed import seed_missions


def test_seed_missions_inserts_all_registered_missions(test_database):
    seed_missions()

    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title FROM missions ORDER BY id"
        ).fetchall()

    assert len(rows) == 4
    assert {row["id"] for row in rows} == {
        "phishing-001",
        "logs-001",
        "puzzle-001",
        "incident-001",
    }


def test_seed_missions_is_safe_to_run_repeatedly(test_database):
    seed_missions()
    seed_missions()

    with get_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM missions"
        ).fetchone()[0]

    assert count == 4


def test_seed_missions_updates_changed_metadata(test_database):
    seed_missions()

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE missions
            SET title = ?
            WHERE id = ?
            """,
            ("Outdated Title", "phishing-001"),
        )

    seed_missions()

    with get_connection() as connection:
        mission = connection.execute(
            "SELECT title FROM missions WHERE id = ?",
            ("phishing-001",),
        ).fetchone()

    assert mission["title"] == "Suspicious Message"
