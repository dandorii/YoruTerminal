"""Load registered mission definitions into the database."""

from database.db import get_connection
from missions.registry import get_all_missions


def seed_missions() -> None:
    """Insert or update registered missions without deleting player history."""
    missions = get_all_missions()

    with get_connection() as connection:
        for mission in missions:
            connection.execute(
                """
                INSERT INTO missions (
                    id, title, category, description, difficulty
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    category = excluded.category,
                    description = excluded.description,
                    difficulty = excluded.difficulty
                """,
                (
                    mission["id"],
                    mission["title"],
                    mission["category"],
                    mission["description"],
                    mission["difficulty"],
                ),
            )
