"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from pylint.lint.pylinter import PyLinter

"""Everything related to the 'pylint-config generate' command."""
if TYPE_CHECKING:
    ...
def generate_interactive_config(linter: PyLinter) -> None:
    ...

def handle_generate_command(linter: PyLinter) -> int:
    """Handle 'pylint-config generate'."""
    ...
