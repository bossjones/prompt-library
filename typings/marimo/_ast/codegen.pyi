"""
This type stub file was generated by pyright.
"""

from typing import Optional, TYPE_CHECKING
from marimo._ast.app import App, _AppConfig
from marimo._ast.cell import CellConfig, CellImpl
from marimo._ast.visitor import Name

if TYPE_CHECKING:
    ...
INDENT = ...
MAX_LINE_LENGTH = ...
def indent_text(text: str) -> str:
    ...

def to_functiondef(cell: CellImpl, name: str, unshadowed_builtins: Optional[set[Name]] = ...) -> str:
    ...

def generate_unparsable_cell(code: str, name: Optional[str], config: CellConfig) -> str:
    ...

def generate_app_constructor(config: Optional[_AppConfig]) -> str:
    ...

def generate_filecontents(codes: list[str], names: list[str], cell_configs: list[CellConfig], config: Optional[_AppConfig] = ..., header_comments: Optional[str] = ...) -> str:
    """Translates a sequences of codes (cells) to a Python file"""
    ...

class MarimoFileError(Exception):
    ...


def get_app(filename: Optional[str]) -> Optional[App]:
    """Load and return app from a marimo-generated module"""
    ...

RECOVERY_CELL_MARKER = ...
def recover(filename: str) -> str:
    """Generate a module for code recovered from a disconnected frontend"""
    ...

def get_header_comments(filename: str) -> Optional[str]:
    """Gets the header comments from a file. Returns
    None if the file does not exist or the header is
    invalid, which is determined by:
        1. If the file is does not contain the marimo
            import statement
        2. If the section before the marimo import
            statement contains any non-comment code
    """
    ...