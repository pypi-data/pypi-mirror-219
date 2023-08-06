from webexception.webexception import WebException


class BackendException(WebException):
    pass


class RevisionConflict(BackendException):
    status_code: int = 409  # Conflict

    def __init__(self, revision: str) -> None:
        super().__init__(f"revision changed to {revision}", revision=revision)


class NotFound(BackendException):
    status_code: int = 404  # Not found

    def __init__(self, uid: str) -> None:
        super().__init__(f"Entry with uid '{uid}' not found.", uid=uid)


class AlreadyExists(BackendException):
    status_code: int = 409  # Conflict

    def __init__(self, uid: str) -> None:
        super().__init__(f"Entry with uid '{uid}' already exists.", uid=uid)
