"""
This type stub file was generated by pyright.
"""

from typing import Optional
from marimo._ast.app import _AppConfig

def markdown_to_marimo(source: str) -> str:
    ...

def generate_from_sources(sources: list[str], config: Optional[_AppConfig] = ..., header_comments: Optional[str] = ...) -> str:
    """
    Given a list of Python source code,
    generate the marimo file contents.
    """
    ...
