"""
This type stub file was generated by pyright.
"""

from collections.abc import Sequence
from typing import Any, NamedTuple, TypeVar
from astroid import nodes
from pylint.interfaces import Confidence
from pylint.message.message import Message

_T = TypeVar("_T")
class MessageTest(NamedTuple):
    msg_id: str
    line: int | None = ...
    node: nodes.NodeNG | None = ...
    args: Any | None = ...
    confidence: Confidence | None = ...
    col_offset: int | None = ...
    end_line: int | None = ...
    end_col_offset: int | None = ...


class OutputLine(NamedTuple):
    symbol: str
    lineno: int
    column: int
    end_lineno: int | None
    end_column: int | None
    object: str
    msg: str
    confidence: str
    @classmethod
    def from_msg(cls, msg: Message, check_endline: bool = ...) -> OutputLine:
        """Create an OutputLine from a Pylint Message."""
        ...

    @classmethod
    def from_csv(cls, row: Sequence[str] | str, check_endline: bool = ...) -> OutputLine:
        """Create an OutputLine from a comma separated list (the functional tests
        expected output .txt files).
        """
        ...

    def to_csv(self) -> tuple[str, str, str, str, str, str, str, str]:
        """Convert an OutputLine to a tuple of string to be written by a
        csv-writer.
        """
        ...