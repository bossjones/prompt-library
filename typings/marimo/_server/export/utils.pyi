"""
This type stub file was generated by pyright.
"""

from typing import Optional
from marimo._ast.cell import Cell
from marimo._server.file_manager import AppFileManager

def format_filename_title(filename: str) -> str:
    ...

def get_filename(file_manager: AppFileManager, default: str = ...) -> str:
    ...

def get_app_title(file_manager: AppFileManager) -> str:
    ...

def get_download_filename(file_manager: AppFileManager, extension: str) -> str:
    ...

def get_markdown_from_cell(cell: Cell, code: str, native_callout: bool = ...) -> Optional[str]:
    """Attempt to extract markdown from a cell, or return None"""
    ...