
import pytest

from missions.mission_engine import (
    calculate_mission_score,
    get_hint_penalty,
    validate_answer,
)


def test_validate_correct_answer():
    question = {"answer": "B"}

    assert validate_answer(question, "B") is True


def test_validate_answer_ignores_case_and_surrounding_spaces():
    question = {"answer": "B"}

    assert validate_answer(question, " b ") is True


def test_validate_wrong_answer():
    question = {"answer": "B"}

    assert validate_answer(question, "A") is False


def test_validate_non_string_answer():
    question = {"answer": "B"}

    assert validate_answer(question, None) is False


def test_perfect_score_without_hints():
    assert calculate_mission_score(3, 3) == 100


def test_partial_score_without_hints():
    assert calculate_mission_score(2, 3) == 66


def test_hint_penalty():
    assert calculate_mission_score(3, 3, hints_used=2) == 80


def test_score_never_drops_below_zero():
    assert calculate_mission_score(0, 3, hints_used=5) == 0


def test_hint_penalty_matches_game_engine():
    assert get_hint_penalty() == 10


@pytest.mark.parametrize(
    ("correct", "total", "hints"),
    [
        (-1, 3, 0),
        (4, 3, 0),
        (1, 0, 0),
        (1, -1, 0),
        (1, 3, -1),
        (True, 3, 0),
        (1, True, 0),
        (1, 3, True),
    ],
)
def test_invalid_scoring_inputs(correct, total, hints):
    with pytest.raises(ValueError):
        calculate_mission_score(correct, total, hints)
