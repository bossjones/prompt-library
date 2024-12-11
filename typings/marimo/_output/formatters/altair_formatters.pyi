"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from marimo._config.config import Theme
from marimo._output.formatters.formatter_factory import FormatterFactory

if TYPE_CHECKING:
    ...
class AltairFormatter(FormatterFactory):
    @staticmethod
    def package_name() -> str:
        ...

    def register(self) -> None:
        ...

    def apply_theme(self, theme: Theme) -> None:
        ...