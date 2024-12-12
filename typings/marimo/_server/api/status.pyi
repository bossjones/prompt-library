"""
This type stub file was generated by pyright.
"""

from enum import IntEnum
from typing import Optional

class HTTPStatus(IntEnum):
    OK = ...
    NOT_MODIFIED = ...
    BAD_REQUEST = ...
    FORBIDDEN = ...
    REQUEST_TIMEOUT = ...
    NOT_FOUND = ...
    METHOD_NOT_ALLOWED = ...
    UNSUPPORTED_MEDIA_TYPE = ...
    PRECONDITION_REQUIRED = ...
    SERVER_ERROR = ...


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: Optional[str] = ...) -> None:
        ...



def is_client_error(status_code: int) -> bool:
    ...
