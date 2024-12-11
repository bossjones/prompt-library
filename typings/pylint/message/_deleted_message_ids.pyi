"""
This type stub file was generated by pyright.
"""

from functools import cache
from typing import NamedTuple

class DeletedMessage(NamedTuple):
    msgid: str
    symbol: str
    old_names: list[tuple[str, str]] = ...


DELETED_MSGID_PREFIXES: list[int] = ...
DELETED_MESSAGES_IDS = ...
MOVED_TO_EXTENSIONS = ...
@cache
def is_deleted_symbol(symbol: str) -> str | None:
    """Return the explanation for removal if the message was removed."""
    ...

@cache
def is_deleted_msgid(msgid: str) -> str | None:
    """Return the explanation for removal if the message was removed."""
    ...

@cache
def is_moved_symbol(symbol: str) -> str | None:
    """Return the explanation for moving if the message was moved to extensions."""
    ...

@cache
def is_moved_msgid(msgid: str) -> str | None:
    """Return the explanation for moving if the message was moved to extensions."""
    ...