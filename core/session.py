
class Session:
    """Track the currently authenticated player in memory."""

    def __init__(self):
        self._user_id: int | None = None

    @property
    def is_authenticated(self) -> bool:
        return self._user_id is not None

    @property
    def user_id(self) -> int | None:
        return self._user_id

    def login(self, user_id: int) -> None:
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer.")

        self._user_id = user_id

    def logout(self) -> None:
        self._user_id = None
