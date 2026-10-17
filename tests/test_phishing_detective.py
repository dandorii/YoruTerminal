
from missions.phishing_detective import (
    MISSION_ID,
    get_questions,
)


def test_mission_uses_registered_mission_id():
    assert MISSION_ID == "phishing-001"


def test_mission_has_three_questions():
    assert len(get_questions()) == 3


def test_every_question_has_four_options_and_valid_answer():
    for question in get_questions():
        assert len(question["options"]) == 4
        assert question["answer"] in question["options"]


def test_every_question_has_an_explanation():
    for question in get_questions():
        assert question["explanation"].strip()


def test_get_questions_returns_independent_data():
    questions = get_questions()
    questions[0]["options"]["A"] = "Changed option"
    questions[0]["message"] = "Changed message"

    original = get_questions()[0]

    assert original["options"]["A"] == "The message mentions an account"
    assert original["message"].startswith("From: Campus IT Support")


def test_question_ids_are_unique():
    questions = get_questions()
    ids = [question["id"] for question in questions]

    assert len(ids) == len(set(ids))
