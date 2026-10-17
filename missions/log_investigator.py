
"""Scenario data for the Log Investigator mission."""

MISSION_ID = "logs-001"

QUESTIONS = [
    {
        "id": "logs-q1",
        "log": (
            "2026-10-17 01:14:03 | account=alex | "
            "source=192.0.2.45 | event=LOGIN_FAILED\n"
            "2026-10-17 01:14:08 | account=alex | "
            "source=192.0.2.45 | event=LOGIN_FAILED\n"
            "2026-10-17 01:14:13 | account=alex | "
            "source=192.0.2.45 | event=LOGIN_FAILED\n"
            "2026-10-17 01:14:19 | account=alex | "
            "source=192.0.2.45 | event=LOGIN_FAILED"
        ),
        "prompt": "What is the strongest initial concern?",
        "options": {
            "A": "The account name is written in lowercase",
            "B": "Several failed logins occur close together "
                 "from the same source",
            "C": "The timestamps use a 24-hour clock",
            "D": "The log contains a source address",
        },
        "answer": "B",
        "explanation": (
            "Repeated failed logins against one account from "
            "the same source in a short period may indicate "
            "password guessing. Investigate further before "
            "concluding that an attack occurred."
        ),
        "hint": (
            "Compare the timestamps, account name, source address, "
            "and event type across the entries."
        ),
    },
    {
        "id": "logs-q2",
        "log": (
            "2026-10-17 02:03:11 | account=mira | "
            "source=198.51.100.24 | event=LOGIN_SUCCESS\n"
            "2026-10-17 02:03:15 | account=mira | "
            "source=198.51.100.24 | event=PRIVILEGE_CHANGE"
        ),
        "prompt": "What should an investigator do first?",
        "options": {
            "A": "Assume the account is compromised immediately",
            "B": "Delete the log entries",
            "C": "Check whether the login and privilege change "
                 "were authorized",
            "D": "Ignore the events because login succeeded",
        },
        "answer": "C",
        "explanation": (
            "A successful login followed by a privilege change "
            "may be legitimate or suspicious. Correlate the events "
            "with approved activity and other available evidence."
        ),
        "hint": (
            "A successful login doesn't prove an action was authorized. "
            "Think about what changed immediately afterward."
        ),
    },
    {
        "id": "logs-q3",
        "log": (
            "2026-10-17 09:02:41 | account=jamie | "
            "source=203.0.113.17 | event=LOGIN_SUCCESS\n"
            "2026-10-17 09:04:02 | account=jamie | "
            "source=203.0.113.17 | event=FILE_DOWNLOAD"
        ),
        "prompt": "Which conclusion is best supported by these logs?",
        "options": {
            "A": "The user definitely stole confidential files",
            "B": "The source address proves the login was malicious",
            "C": "The logs show a successful login and a file download, "
                 "but more context is needed",
            "D": "Every file download is a security incident",
        },
        "answer": "C",
        "explanation": (
            "Logs provide evidence of recorded events, not necessarily "
            "intent. Check whether the download was expected, what "
            "was accessed, and whether the account activity was authorized."
        ),
        "hint": (
            "Separate what the logs directly show from what you "
            "would still need evidence to conclude."
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
