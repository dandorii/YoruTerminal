
from missions.incident_response_simulator import (
    MISSION_ID,
    get_questions,
)


def test_incident_response_has_three_scenarios():
    questions = get_questions()

    assert MISSION_ID == "incident-001"
    assert len(questions) == 3


def test_each_scenario_has_valid_options_and_answer():
    for question in get_questions():
        assert set(question["options"]) == {"A", "B", "C", "D"}
        assert question["answer"] in question["options"]
        assert question["title"]
        assert question["prompt"]
        assert question["evidence"]
        assert question["explanation"]
        assert question["hint"]


def test_scenario_data_is_independent():
    questions = get_questions()
    questions[0]["options"]["A"] = "Changed option"

    fresh_questions = get_questions()
    assert fresh_questions[0]["options"]["A"] == (
        "Ignore the alert until malware is confirmed"
    )
