"""
This type stub file was generated by pyright.
"""

class AuthToken:
    """
    Holds a string value that should not be revealed in tracebacks etc.
    You should cast the value to `str` at the point it is required.
    """
    def __init__(self, value: str) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        ...

    def __bool__(self) -> bool:
        ...

    @staticmethod
    def random() -> AuthToken:
        ...

    @staticmethod
    def from_code(code: str) -> AuthToken:
        ...

    @staticmethod
    def is_empty(token: AuthToken) -> bool:
        ...



class SkewProtectionToken:
    """
    Provides a token that is sent to the client on the first request and
    is used to protect against version skew bugs.

    This can happen when new code is deployed to the server but the client
    still has only application loaded.
    """
    def __init__(self, token: str) -> None:
        ...

    @staticmethod
    def from_code(code: str) -> SkewProtectionToken:
        ...

    @staticmethod
    def random() -> SkewProtectionToken:
        ...

    def __str__(self) -> str:
        ...
