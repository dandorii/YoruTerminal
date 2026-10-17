
from missions.registry import get_all_missions, get_mission


def test_registry_contains_four_missions():
    assert len(get_all_missions()) == 4


def test_mission_ids_are_unique():
    missions = get_all_missions()
    ids = [mission["id"] for mission in missions]

    assert len(ids) == len(set(ids))


def test_get_mission_returns_expected_definition():
    mission = get_mission("phishing-001")

    assert mission is not None
    assert mission["title"] == "Suspicious Message"
    assert mission["difficulty"] == "Beginner"


def test_unknown_mission_returns_none():
    assert get_mission("does-not-exist") is None


def test_registry_returns_independent_copies():
    mission = get_mission("phishing-001")
    mission["title"] = "Changed Title"

    assert get_mission("phishing-001")["title"] == "Suspicious Message"
