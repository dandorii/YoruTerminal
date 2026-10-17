
from unittest.mock import patch

from ui.security_puzzle_room_menu import play_security_puzzle_room


@patch("ui.security_puzzle_room_menu.record_mission_attempt")
@patch("ui.security_puzzle_room_menu.console.input")
def test_perfect_run_awards_score_and_xp(mock_input, mock_record):
    mock_input.side_effect = ["A", "D", "B"]
    mock_record.return_value = {"xp_awarded": 100}

    result = play_security_puzzle_room(user_id=1)

    assert result["score"] == 100
    assert result["correct_answers"] == 3
    assert result["hints_used"] == 0
    assert result["xp_awarded"] == 100

    mock_record.assert_called_once_with(
        user_id=1,
        mission_id="puzzle-001",
        base_score=100,
        completed=True,
        hints_used=0,
    )


@patch("ui.security_puzzle_room_menu.record_mission_attempt")
@patch("ui.security_puzzle_room_menu.console.input")
def test_hint_reduces_score(mock_input, mock_record):
    mock_input.side_effect = ["H", "A", "D", "B"]
    mock_record.return_value = {"xp_awarded": 90}

    result = play_security_puzzle_room(user_id=1)

    assert result["score"] == 90
    assert result["hints_used"] == 1
    assert result["xp_awarded"] == 90

    mock_record.assert_called_once_with(
        user_id=1,
        mission_id="puzzle-001",
        base_score=90,
        completed=True,
        hints_used=0,
    )
