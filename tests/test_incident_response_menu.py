
from unittest.mock import patch

from ui.incident_response_menu import play_incident_response


@patch("ui.incident_response_menu.record_mission_attempt")
@patch("ui.incident_response_menu.console.input")
def test_perfect_run_awards_score_and_xp(mock_input, mock_record):
    mock_input.side_effect = ["B", "C", "C"]
    mock_record.return_value = {"xp_awarded": 100}

    result = play_incident_response(user_id=1)

    assert result["score"] == 100
    assert result["correct_answers"] == 3
    assert result["hints_used"] == 0
    assert result["xp_awarded"] == 100

    mock_record.assert_called_once_with(
        user_id=1,
        mission_id="incident-001",
        base_score=100,
        completed=True,
        hints_used=0,
    )


@patch("ui.incident_response_menu.record_mission_attempt")
@patch("ui.incident_response_menu.console.input")
def test_hint_reduces_score(mock_input, mock_record):
    mock_input.side_effect = ["H", "B", "C", "C"]
    mock_record.return_value = {"xp_awarded": 90}

    result = play_incident_response(user_id=1)

    assert result["score"] == 90
    assert result["hints_used"] == 1
    assert result["xp_awarded"] == 90

    mock_record.assert_called_once_with(
        user_id=1,
        mission_id="incident-001",
        base_score=90,
        completed=True,
        hints_used=0,
    )
