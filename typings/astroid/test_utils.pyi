"""
This type stub file was generated by pyright.
"""

import contextlib
from collections.abc import Callable

"""Utility functions for test code that uses astroid ASTs as input."""
def require_version(minver: str = ..., maxver: str = ...) -> Callable:
    """Compare version of python interpreter to the given one and skips the test if older."""
    ...

def get_name_node(start_from, name, index=...):
    ...

@contextlib.contextmanager
def enable_warning(warning): # -> Generator[None, Any, None]:
    ...

def brainless_manager(): # -> AstroidManager:
    ...