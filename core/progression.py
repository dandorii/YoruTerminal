
"""Persist mission results and player progression."""

from database.db import get_connection
from core.game_engine import calculate_score, rank_for_xp


def record_mission_attempt(
    user_id: int,
    mission_id: str,
    base_score: int,
    completed: bool,
    hints_used: int = 0,
) -> dict:
    """Save an attempt and award first-completion XP once."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("User ID must be a positive integer.")

    if not isinstance(mission_id, str) or not mission_id.strip():
        raise ValueError("Mission ID cannot be empty.")

    if not isinstance(completed, bool):
        raise ValueError("Completed must be a boolean.")

    final_score = calculate_score(base_score, hints_used)

    with get_connection() as connection:
        # Ensure the player exists before attempting to record progress.
        player = connection.execute(
            "SELECT xp FROM player_progress WHERE user_id = ?",
            (user_id,),
        ).fetchone()

        if player is None:
            raise ValueError("Player progress was not found.")

        mission = connection.execute(
            "SELECT id FROM missions WHERE id = ?",
            (mission_id,),
        ).fetchone()

        if mission is None:
            raise ValueError("Mission was not found.")

        previous_completion = connection.execute(
            """
            SELECT 1
            FROM mission_completions
            WHERE user_id = ? AND mission_id = ?
            """,
            (user_id, mission_id),
        ).fetchone()

        first_completion = completed and previous_completion is None
        xp_awarded = final_score if first_completion else 0

        connection.execute(
            """
            INSERT INTO mission_results
                (user_id, mission_id, score, completed, xp_awarded)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                mission_id,
                final_score,
                int(completed),
                xp_awarded,
            ),
        )

        if first_completion:
            connection.execute(
                """
                INSERT INTO mission_completions (user_id, mission_id)
                VALUES (?, ?)
                """,
                (user_id, mission_id),
            )

        if xp_awarded:
            new_xp = player["xp"] + xp_awarded
            connection.execute(
                """
                UPDATE player_progress
                SET xp = ?, rank = ?,
                    missions_completed = missions_completed + 1
                WHERE user_id = ?
                """,
                (new_xp, rank_for_xp(new_xp), user_id),
            )
        elif first_completion:
            # A completed mission with a score of zero still counts once.
            connection.execute(
                """
                UPDATE player_progress
                SET missions_completed = missions_completed + 1
                WHERE user_id = ?
                """,
                (user_id,),
            )

        return {
            "score": final_score,
            "completed": completed,
            "first_completion": first_completion,
            "xp_awarded": xp_awarded,
        }
