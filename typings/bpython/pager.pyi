"""
This type stub file was generated by pyright.
"""

from typing import List

def get_pager_command(default: str = ...) -> List[str]:
    ...

def page_internal(data: str) -> None:
    """A more than dumb pager function."""
    ...

def page(data: str, use_internal: bool = ...) -> None:
    ...
