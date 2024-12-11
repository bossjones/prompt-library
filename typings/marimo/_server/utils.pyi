"""
This type stub file was generated by pyright.
"""

from typing import Any, TYPE_CHECKING, TypeVar
from collections.abc import Coroutine

if TYPE_CHECKING:
    ...
TAB = ...
LOGGER = ...
def print_tabbed(string: str, n_tabs: int = ...) -> None:
    ...

def canonicalize_filename(filename: str) -> str:
    ...

def find_free_port(port: int, attempts: int = ...) -> int:
    """Find a free port or move to the next one recursively"""
    ...

def initialize_mimetypes() -> None:
    ...

def initialize_asyncio() -> None:
    """Platform-specific initialization of asyncio.

    Sessions use the `add_reader()` API, which is only available in the
    SelectorEventLoop policy; Windows uses the Proactor by default.
    """
    ...

def initialize_fd_limit(limit: int) -> None:
    """Raise the limit on open file descriptors.

    Not applicable on Windows.
    """
    ...

T = TypeVar("T")
def asyncio_run(coro: Coroutine[Any, Any, T], **kwargs: dict[Any, Any]) -> T:
    """asyncio.run() with platform-specific initialization.

    When using Sessions, make sure to use this method instead of `asyncio.run`.

    If not using a Session, don't call this method.

    `kwargs` are passed to `asyncio.run()`
    """
    ...

def print_(*args: Any, **kwargs: Any) -> None:
    ...