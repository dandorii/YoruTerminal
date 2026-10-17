"""Central registry of YoruTerminal missions."""

MISSIONS = [
    {
        "id": "phishing-001",
        "title": "Suspicious Message",
        "category": "Phishing Detective",
        "description": "Identify warning signs in a suspicious message.",
        "difficulty": "Beginner",
    },
    {
        "id": "logs-001",
        "title": "After-Hours Access",
        "category": "Log Investigator",
        "description": "Investigate a fictional authentication log.",
        "difficulty": "Beginner",
    },
    {
        "id": "puzzle-001",
        "title": "Security Checkpoint",
        "category": "Security Puzzle Room",
        "description": "Solve a foundational security knowledge challenge.",
        "difficulty": "Intermediate",
    },
    {
        "id": "incident-001",
        "title": "Contain the Incident",
        "category": "Incident Response Simulator",
        "description": "Choose appropriate responses to a simulated incident.",
        "difficulty": "Intermediate",
    },
]


def get_all_missions() -> list[dict]:
    """Return copies of all registered mission definitions."""
    return [mission.copy() for mission in MISSIONS]


def get_mission(mission_id: str) -> dict | None:
    """Find a mission by its unique ID."""
    for mission in MISSIONS:
        if mission["id"] == mission_id:
            return mission.copy()

    return None
