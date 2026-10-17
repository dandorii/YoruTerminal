
from missions.security_puzzle_room import (
    MISSION_ID,
    get_questions,
)


def test_security_puzzle_room_has_three_questions():
    questions = get_questions()

    assert MISSION_ID == "puzzle-001"
    assert len(questions) == 3


def test_each_puzzle_has_valid_options_and_answer():
    for question in get_questions():
        assert set(question["options"]) == {"A", "B", "C", "D"}
        assert question["answer"] in question["options"]
        assert question["title"]
        assert question["prompt"]
        assert question["evidence"]
        assert question["explanation"]
        assert question["hint"]


def test_question_data_is_independent():
    questions = get_questions()
    questions[0]["options"]["A"] = "Changed option"

    fresh_questions = get_questions()
    assert fresh_questions[0]["options"]["A"] == "ACCESS GRANTED"
