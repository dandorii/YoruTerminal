from missions.log_investigator import (
    MISSION_ID,
    get_questions,
)


def test_log_investigator_has_three_questions():
    questions = get_questions()

    assert MISSION_ID == "logs-001"
    assert len(questions) == 3


def test_each_question_has_valid_options_and_answer():
    for question in get_questions():
        assert set(question["options"]) == {"A", "B", "C", "D"}
        assert question["answer"] in question["options"]
        assert question["prompt"]
        assert question["log"]
        assert question["explanation"]
        assert question["hint"]


def test_question_data_is_independent():
    questions = get_questions()
    questions[0]["options"]["A"] = "Changed option"

    fresh_questions = get_questions()
    assert fresh_questions[0]["options"]["A"] != "Changed option"
