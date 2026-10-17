"""Answer validation and scoring for YoruTerminal missions."""

from core.game_engine import calculate_score, HINT_PENALTY


def validate_answer(question: dict, answer: str) -> bool:
    """Check whether an answer matches the question's correct option."""
    if not isinstance(answer, str):
        return False

    return answer.strip().upper() == question["answer"]


def calculate_mission_score(
    correct_answers: int,
    total_questions: int,
    hints_used: int = 0,
) -> int:
    """Calculate a mission score out of 100 after hint penalties."""
    if (
        not isinstance(total_questions, int)
        or isinstance(total_questions, bool)
        or total_questions <= 0
    ):
        raise ValueError("Total questions must be a positive integer.")

    if (
        not isinstance(correct_answers, int)
        or isinstance(correct_answers, bool)
        or not 0 <= correct_answers <= total_questions
    ):
        raise ValueError(
            "Correct answers must be between zero and total questions."
        )

    if (
        not isinstance(hints_used, int)
        or isinstance(hints_used, bool)
        or hints_used < 0
    ):
        raise ValueError("Hints used must be a non-negative integer.")

    base_score = (correct_answers * 100) // total_questions

    return calculate_score(base_score, hints_used)


def get_hint_penalty() -> int:
    """Return the score penalty for using one hint."""
    return HINT_PENALTY
