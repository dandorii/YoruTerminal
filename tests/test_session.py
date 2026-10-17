
import pytest

from core.session import Session


def test_session_starts_logged_out():
    session = Session()

    assert session.is_authenticated is False
    assert session.user_id is None


def test_login_sets_authenticated_user():
    session = Session()
    session.login(7)

    assert session.is_authenticated is True
    assert session.user_id == 7


def test_logout_clears_session():
    session = Session()
    session.login(7)
    session.logout()

    assert session.is_authenticated is False
    assert session.user_id is None


def test_login_rejects_nonpositive_user_id():
    session = Session()

    with pytest.raises(ValueError):
        session.login(0)

    assert session.is_authenticated is False
