"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from pylint.interfaces import Confidence
from pylint.typing import MessageLocationTuple

"""
This type stub file was generated by pyright.
"""
@dataclass(unsafe_hash=True)
class Message:
    """This class represent a message to be issued by the reporters."""
    msg_id: str
    symbol: str
    msg: str
    C: str
    category: str
    confidence: Confidence
    abspath: str
    path: str
    module: str
    obj: str
    line: int
    column: int
    end_line: int | None
    end_column: int | None
    def __init__(self, msg_id: str, symbol: str, location: MessageLocationTuple, msg: str, confidence: Confidence | None) -> None:
        ...

    def format(self, template: str) -> str:
        """Format the message according to the given template.

        The template format is the one of the format method :
        cf. https://docs.python.org/2/library/string.html#formatstrings
        """
        ...

    @property
    def location(self) -> MessageLocationTuple:
        ...