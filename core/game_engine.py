"""Core scoring and progression rules for YoruTerminal."""

MAX_SCORE = 100
HINT_PENALTY = 10


def calculate_score(base_score: int, hints_used: int = 0) -> int:
    """Calculate the final score after applying hint penalties."""
    if not isinstance(base_score, int) or isinstance(base_score, bool):
        raise ValueError("Base score must be an integer.")

    if not 0 <= base_score <= MAX_SCORE:
        raise ValueError("Base score must be between 0 and 100.")

    if not isinstance(hints_used, int) or isinstance(hints_used, bool):
        raise ValueError("Hints used must be a non-negative integer.")

    if hints_used < 0:
        raise ValueError("Hints used must be a non-negative integer.")

    return max(0, base_score - hints_used * HINT_PENALTY)


def calculate_xp_award(
    score: int,
    completed: bool,
    first_completion: bool,
) -> int:
    """Award score-based XP only for a first successful completion."""
    if not isinstance(score, int) or isinstance(score, bool):
        raise ValueError("Score must be an integer.")

    if not 0 <= score <= MAX_SCORE:
        raise ValueError("Score must be between 0 and 100.")

    if not isinstance(completed, bool) or not isinstance(
        first_completion, bool
    ):
        raise ValueError("Completion flags must be booleans.")

    if completed and first_completion:
        return score

    return 0


def rank_for_xp(xp: int) -> str:
    """Return the player's rank based on total XP."""
    if not isinstance(xp, int) or isinstance(xp, bool) or xp < 0:
        raise ValueError("XP must be a non-negative integer.")

    if xp >= 600:
        return "Elite Shinobi"
    if xp >= 300:
        return "Shadow Agent"
    if xp >= 100:
        return "Operative"

    return "Novice"
