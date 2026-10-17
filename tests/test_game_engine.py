
import pytest

from core.game_engine import (
    calculate_score,
    calculate_xp_award,
    rank_for_xp,
)


@pytest.mark.parametrize(
    ("base_score", "hints", "expected"),
    [
        (100, 0, 100),
        (100, 1, 90),
        (80, 2, 60),
        (10, 1, 0),
        (0, 5, 0),
    ],
)
def test_calculate_score(base_score, hints, expected):
    assert calculate_score(base_score, hints) == expected


@pytest.mark.parametrize(
    ("score", "completed", "first_completion", "expected"),
    [
        (90, True, True, 90),
        (0, True, True, 0),
        (90, True, False, 0),
        (90, False, True, 0),
        (90, False, False, 0),
    ],
)
def test_calculate_xp_award(
    score, completed, first_completion, expected
):
    assert calculate_xp_award(
        score, completed, first_completion
    ) == expected


@pytest.mark.parametrize(
    ("xp", "expected"),
    [
        (0, "Novice"),
        (99, "Novice"),
        (100, "Operative"),
        (299, "Operative"),
        (300, "Shadow Agent"),
        (599, "Shadow Agent"),
        (600, "Elite Shinobi"),
    ],
)
def test_rank_for_xp(xp, expected):
    assert rank_for_xp(xp) == expected


@pytest.mark.parametrize("score", [-1, 101])
def test_calculate_score_rejects_out_of_range_values(score):
    with pytest.raises(ValueError):
        calculate_score(score)


def test_calculate_score_rejects_negative_hints():
    with pytest.raises(ValueError):
        calculate_score(100, -1)


def test_xp_is_not_awarded_for_replays():
    assert calculate_xp_award(100, True, False) == 0


def test_rank_rejects_negative_xp():
    with pytest.raises(ValueError):
        rank_for_xp(-1)
