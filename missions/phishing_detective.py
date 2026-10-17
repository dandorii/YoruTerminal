"""Scenario data for the Phishing Detective mission."""

MISSION_ID = "phishing-001"

QUESTIONS = [
    {
        "id": "phish-q1",
        "message": (
            "From: Campus IT Support\n"
            "Subject: Urgent — Verify Your Account\n\n"
            "Your account will be suspended today. "
            "Visit http://campus-login.example.invalid "
            "and enter your password to keep access."
        ),
        "prompt": "What is the strongest warning sign?",
        "options": {
            "A": "The message mentions an account",
            "B": "It creates urgency and requests a password "
                 "through a suspicious link",
            "C": "It uses a subject line",
            "D": "It claims to come from IT Support",
        },
        "answer": "B",
        "explanation": (
            "Urgent threats combined with a link requesting "
            "credentials are strong phishing indicators. "
            "Verify account issues through an official channel."
        ),
    },
    {
        "id": "phish-q2",
        "message": (
            "From: Library Services\n"
            "Subject: Document available\n\n"
            "A message says a document is ready. "
            "The sender's address is unfamiliar, and the "
            "link's displayed text does not match its destination."
        ),
        "prompt": "What should you do first?",
        "options": {
            "A": "Open the link to see what it contains",
            "B": "Reply with your student details",
            "C": "Verify the sender and document through "
                 "a known, official channel",
            "D": "Forward it to everyone",
        },
        "answer": "C",
        "explanation": (
            "An unfamiliar sender and a mismatched link deserve "
            "verification. Use a known official website or "
            "contact method instead of the supplied link."
        ),
    },
    {
        "id": "phish-q3",
        "message": (
            "From: Student Activities\n"
            "Subject: Event schedule update\n\n"
            "The message matches an event you registered for. "
            "It contains no unexpected attachment or credential "
            "request. You can confirm the update on the "
            "organization's official page."
        ),
        "prompt": "What is the safest conclusion?",
        "options": {
            "A": "Every email about an event is malicious",
            "B": "The message is definitely safe because "
                 "it looks familiar",
            "C": "Delete it without checking",
            "D": "The available signs are less suspicious, "
                 "but verify the update through the official page",
        },
        "answer": "D",
        "explanation": (
            "Not every unfamiliar message is phishing, and "
            "familiar-looking messages are not automatically safe. "
            "Check important claims through an official source."
        ),
    },
]


def get_questions() -> list[dict]:
    """Return independent copies of the question data."""
    questions = []

    for question in QUESTIONS:
        copied_question = question.copy()
        copied_question["options"] = question["options"].copy()
        questions.append(copied_question)

    return questions
