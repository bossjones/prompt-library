"""
This type stub file was generated by pyright.
"""

from pdb import Pdb
from typing import Any, TYPE_CHECKING
from marimo._messaging.types import Stdin, Stdout
from types import FrameType

if TYPE_CHECKING:
    ...
LOGGER = ...
class MarimoPdb(Pdb):
    def __init__(self, completekey: str = ..., stdout: Stdout | None = ..., stdin: Stdin | None = ..., skip: Any = ..., nosigint: bool = ..., readrc: bool = ...) -> None:
        ...

    def set_trace(self, frame: FrameType | None = ..., header: str | None = ...) -> None:
        ...



def set_trace(debugger: MarimoPdb, frame: FrameType | None = ..., header: str | None = ...) -> None:
    ...
