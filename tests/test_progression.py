
import pytest

from auth.accounts import register_user
from core.progression import record_mission_attempt
from database.db import get_connection


@pytest.fixture
def player_and_mission(test_database):
    user_id = register_user("NightOwl", "a-long-test-password")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO missions
                (id, title, category, description, difficulty)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "phishing-001",
                "Suspicious Message",
                "Phishing Detective",
                "Identify warning signs in a suspicious message.",
                "Beginner",
            ),
        )

    return user_id, "phishing-001"


def test_first_completion_awards_score_based_xp(player_and_mission):
    user_id, mission_id = player_and_mission

    result = record_mission_attempt(
        user_id, mission_id, base_score=90, completed=True
    )

    assert result["score"] == 90
    assert result["first_completion"] is True
    assert result["xp_awarded"] == 90

    with get_connection() as connection:
        player = connection.execute(
            "SELECT xp, missions_completed FROM player_progress "
            "WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    assert player["xp"] == 90
    assert player["missions_completed"] == 1


def test_hints_reduce_score_but_reward_uses_final_score(
    player_and_mission,
):
    user_id, mission_id = player_and_mission

    result = record_mission_attempt(
        user_id,
        mission_id,
        base_score=90,
        completed=True,
        hints_used=2,
    )

    assert result["score"] == 70
    assert result["xp_awarded"] == 70


def test_replay_does_not_award_xp_twice(player_and_mission):
    user_id, mission_id = player_and_mission

    record_mission_attempt(user_id, mission_id, 90, True)
    replay = record_mission_attempt(user_id, mission_id, 100, True)

    assert replay["score"] == 100
    assert replay["first_completion"] is False
    assert replay["xp_awarded"] == 0

    with get_connection() as connection:
        player = connection.execute(
            "SELECT xp, missions_completed FROM player_progress "
            "WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    assert player["xp"] == 90
    assert player["missions_completed"] == 1


def test_incomplete_attempt_does_not_award_xp(player_and_mission):
    user_id, mission_id = player_and_mission

    result = record_mission_attempt(
        user_id, mission_id, base_score=80, completed=False
    )

    assert result["first_completion"] is False
    assert result["xp_awarded"] == 0

    with get_connection() as connection:
        player = connection.execute(
            "SELECT xp, missions_completed FROM player_progress "
            "WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    assert player["xp"] == 0
    assert player["missions_completed"] == 0


def test_rank_updates_when_player_reaches_threshold(
    player_and_mission,
):
    user_id, mission_id = player_and_mission

    record_mission_attempt(user_id, mission_id, 100, True)

    with get_connection() as connection:
        player = connection.execute(
            "SELECT xp, rank FROM player_progress WHERE user_id = ?",
            (user_id,),
        ).fetchone()

    assert player["xp"] == 100
    assert player["rank"] == "Operative"


def test_unknown_mission_is_rejected_without_saving_result(
    player_and_mission,
):
    user_id, _ = player_and_mission

    with pytest.raises(ValueError, match="Mission was not found"):
        record_mission_attempt(
            user_id, "missing-mission", 80, True
        )

    with get_connection() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM mission_results WHERE user_id = ?",
            (user_id,),
        ).fetchone()[0]

    assert count == 0


def test_progress_is_isolated_between_players(player_and_mission):
    first_user_id, mission_id = player_and_mission
    second_user_id = register_user(
        "ShadowPlayer", "another-long-test-password"
    )

    record_mission_attempt(first_user_id, mission_id, 80, True)

    with get_connection() as connection:
        second_player = connection.execute(
            "SELECT xp, missions_completed FROM player_progress "
            "WHERE user_id = ?",
            (second_user_id,),
        ).fetchone()

    assert second_player["xp"] == 0
    assert second_player["missions_completed"] == 0
