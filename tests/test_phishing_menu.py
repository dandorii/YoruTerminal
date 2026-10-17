
from unittest.mock import patch

from auth.accounts import register_user
from database.db import get_connection
from missions.seed import seed_missions
from ui.phishing_menu import play_phishing_mission
from rich.panel import Panel


def create_test_user():
    """Create a test account and initialize mission data."""
    seed_missions()
    return register_user(
        "mission_tester",
        "TestPassword123!",
    )


def test_perfect_run_returns_full_score(test_database):
    user_id = create_test_user()

    with patch(
        "ui.phishing_menu.console.input",
        side_effect=["B", "C", "D"],
    ):
        result = play_phishing_mission(user_id)

    assert result["completed"] is True
    assert result["correct_answers"] == 3
    assert result["total_questions"] == 3
    assert result["hints_used"] == 0
    assert result["score"] == 100
    assert result["xp_awarded"] == 100


def test_wrong_answers_reduce_score(test_database):
    user_id = create_test_user()

    with patch(
        "ui.phishing_menu.console.input",
        side_effect=["A", "A", "A"],
    ):
        result = play_phishing_mission(user_id)

    assert result["completed"] is True
    assert result["correct_answers"] == 0
    assert result["score"] == 0
    assert result["xp_awarded"] == 0


def test_hint_applies_score_penalty(test_database):
    user_id = create_test_user()

    with patch(
        "ui.phishing_menu.console.input",
        side_effect=["H", "B", "C", "D"],
    ):
        result = play_phishing_mission(user_id)

    assert result["completed"] is True
    assert result["hints_used"] == 1
    assert result["score"] == 90
    assert result["xp_awarded"] == 90


def test_quitting_returns_incomplete_result(test_database):
    user_id = create_test_user()

    with patch(
        "ui.phishing_menu.console.input",
        side_effect=["Q"],
    ):
        result = play_phishing_mission(user_id)

    assert result["completed"] is False
    assert result["score"] == 0
    assert result["correct_answers"] == 0
    assert result["xp_awarded"] == 0


def test_replaying_completed_mission_does_not_award_xp_again(
    test_database,
):
    user_id = create_test_user()

    with patch(
        "ui.phishing_menu.console.input",
        side_effect=["B", "C", "D", "B", "C", "D"],
    ):
        first_result = play_phishing_mission(user_id)
        second_result = play_phishing_mission(user_id)

    assert first_result["xp_awarded"] == 100
    assert second_result["score"] == 100
    assert second_result["xp_awarded"] == 0

    with get_connection() as connection:
        progress = connection.execute(
            """
            SELECT xp, missions_completed
            FROM player_progress
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

    assert progress["xp"] == 100
    assert progress["missions_completed"] == 1

def test_hint_does_not_reveal_correct_answer(test_database):
    user_id = create_test_user()

    with patch(
        "ui.phishing_menu.console.input",
        side_effect=["H", "B", "C", "D"],
    ):
        with patch(
            "ui.phishing_menu.console.print"
        ) as mock_print:
            result = play_phishing_mission(user_id)

    # Confirm the hint penalty is applied.
    assert result["hints_used"] == 1
    assert result["score"] == 90

    # Find the Rich Panel that displays the hint.
    hint_panels = [
        call.args[0]
        for call in mock_print.call_args_list
        if call.args
        and isinstance(call.args[0], Panel)
        and str(call.args[0].title) == "Hint"
    ]

    assert len(hint_panels) == 1

    hint_text = str(hint_panels[0].renderable)

    # Confirm the hint provides a clue without revealing the answer.
    assert "Look for pressure to act quickly" in hint_text
    assert "Consider option B" not in hint_text