
"""Scenario data for the Incident Response Simulator mission."""

MISSION_ID = "incident-001"

QUESTIONS = [
    {
        "id": "incident-q1",
        "title": "Suspicious Endpoint Activity",
        "prompt": (
            "An employee reports that their computer is behaving "
            "strangely. Your monitoring system also flags unusual "
            "outbound network traffic. What is the best initial action?"
        ),
        "evidence": (
            "Alert: Unusual outbound connections detected.\n"
            "Status: Investigation required; compromise not confirmed."
        ),
        "options": {
            "A": "Ignore the alert until malware is confirmed",
            "B": "Follow the incident procedure to isolate the "
                 "potentially affected endpoint and notify the "
                 "security team",
            "C": "Immediately delete suspicious files and logs",
            "D": "Post the alert publicly to ask for advice",
        },
        "answer": "B",
        "explanation": (
            "Containment can limit potential harm. Follow the "
            "organization's incident-response procedure and preserve "
            "relevant evidence rather than deleting files or logs."
        ),
        "hint": (
            "Consider which action limits potential spread while "
            "keeping the investigation and evidence intact."
        ),
    },
    {
        "id": "incident-q2",
        "title": "Possible Account Compromise",
        "prompt": (
            "An account shows a successful login from an unfamiliar "
            "location followed by an unexpected privilege change. "
            "What should the response team do?"
        ),
        "evidence": (
            "Event 1: Successful login from an unfamiliar location.\n"
            "Event 2: Unexpected privilege change shortly afterward."
        ),
        "options": {
            "A": "Assume the account owner is responsible",
            "B": "Delete the account immediately without documenting it",
            "C": "Validate the activity, notify the appropriate team, "
                 "and contain the account according to policy",
            "D": "Ignore the privilege change because the login succeeded",
        },
        "answer": "C",
        "explanation": (
            "Correlate events and verify whether activity was authorized. "
            "If compromise is reasonably suspected, use approved "
            "containment steps and document the actions taken."
        ),
        "hint": (
            "Look at both events together. Focus on verification, "
            "appropriate escalation, and controlled containment."
        ),
    },
    {
        "id": "incident-q3",
        "title": "Recovery and Lessons Learned",
        "prompt": (
            "The security team has contained an incident and removed "
            "the confirmed threat. What should happen before normal "
            "operations are fully restored?"
        ),
        "evidence": (
            "Status: Threat contained.\n"
            "Status: Remediation completed; recovery checks pending."
        ),
        "options": {
            "A": "Restore systems without checking whether they are safe",
            "B": "Delete all incident records to avoid confusion",
            "C": "Verify remediation, restore from trusted sources when "
                 "needed, monitor systems, and document lessons learned",
            "D": "Assume the same incident cannot happen again",
        },
        "answer": "C",
        "explanation": (
            "Recovery should include validation, monitoring, and "
            "documentation. Lessons learned help improve future "
            "prevention and response."
        ),
        "hint": (
            "Containment is not the same as recovery. Think about "
            "validation, monitoring, and improving future response."
        ),
    },
]


def get_questions() -> list[dict]:
    """Return independent copies of the incident scenarios."""
    questions = []

    for question in QUESTIONS:
        copied_question = question.copy()
        copied_question["options"] = question["options"].copy()
        questions.append(copied_question)

    return questions
