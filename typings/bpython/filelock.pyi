"""
This type stub file was generated by pyright.
"""

from typing import IO, Optional, Type
from ._typing_compat import Literal
from types import TracebackType

has_fcntl = ...
has_msvcrt = ...
class BaseLock:
    """Base class for file locking"""
    def __init__(self) -> None:
        ...
    
    def acquire(self) -> None:
        ...
    
    def release(self) -> None:
        ...
    
    def __enter__(self) -> BaseLock:
        ...
    
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], exc_tb: Optional[TracebackType]) -> Literal[False]:
        ...
    
    def __del__(self) -> None:
        ...
    


class UnixFileLock(BaseLock):
    """Simple file locking for Unix using fcntl"""
    def __init__(self, fileobj, mode: int = ...) -> None:
        ...
    
    def acquire(self) -> None:
        ...
    
    def release(self) -> None:
        ...
    


class WindowsFileLock(BaseLock):
    """Simple file locking for Windows using msvcrt"""
    def __init__(self, filename: str) -> None:
        ...
    
    def acquire(self) -> None:
        ...
    
    def release(self) -> None:
        ...
    


def FileLock(fileobj: IO, mode: int = ..., filename: Optional[str] = ...) -> BaseLock:
    ...
