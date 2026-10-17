
"""Scenario data for the Security Puzzle Room mission."""

MISSION_ID = "puzzle-001"

QUESTIONS = [
    {
        "id": "puzzle-q1",
        "title": "The Encoded Message",
        "prompt": (
            "A teammate gives you this Base64-encoded message. "
            "What does it decode to?"
        ),
        "evidence": "QUNDRVNTIEdSQU5URUQ=",
        "options": {
            "A": "ACCESS GRANTED",
            "B": "ACCESS DENIED",
            "C": "PASSWORD RESET",
            "D": "SYSTEM LOCKED",
        },
        "answer": "A",
        "explanation": (
            "Base64 is an encoding format, not encryption. "
            "Anyone who recognizes the format can decode it, "
            "so it should not be used to protect secrets."
        ),
        "hint": (
            "Base64 commonly uses letters, numbers, and sometimes "
            "plus signs or slashes. The equals sign can appear "
            "at the end as padding."
        ),
    },
    {
        "id": "puzzle-q2",
        "title": "The Weak Password",
        "prompt": (
            "Which password choice is the safest among these options?"
        ),
        "evidence": "Choose based on resistance to guessing.",
        "options": {
            "A": "password123",
            "B": "Marco2006",
            "C": "Summer2026!",
            "D": "vR8!qL2#nP7@xT5",
        },
        "answer": "D",
        "explanation": (
            "A long, unique, randomly generated password is generally "
            "harder to guess. Use a password manager and never reuse "
            "passwords across important accounts."
        ),
        "hint": (
            "Avoid common words, personal information, predictable "
            "patterns, and passwords reused on other accounts."
        ),
    },
    {
        "id": "puzzle-q3",
        "title": "The Exposed Secret",
        "prompt": (
            "You discover an API key committed to a public code "
            "repository. What should you do first?"
        ),
        "evidence": (
            "Finding: A configuration file contains a live API key "
            "in a public repository."
        ),
        "options": {
            "A": "Only delete the line and take no further action",
            "B": "Revoke or rotate the exposed key, then investigate",
            "C": "Rename the variable so nobody notices it",
            "D": "Wait to see whether anyone uses the key",
        },
        "answer": "B",
        "explanation": (
            "Treat an exposed key as compromised. Revoke or rotate it "
            "promptly, check relevant logs, and move secrets into "
            "appropriate secret storage."
        ),
        "hint": (
            "Removing a secret from the latest version does not "
            "invalidate it or erase every historical copy."
        ),
    },
]


def get_questions() -> list[dict]:
    """Return independent copies of the puzzle data."""
    questions = []

    for question in QUESTIONS:
        copied_question = question.copy()
        copied_question["options"] = question["options"].copy()
        questions.append(copied_question)

    return questions
