"""
This type stub file was generated by pyright.
"""

from typing import Callable
from marimo._output.formatters.formatter_factory import FormatterFactory

class IPythonFormatter(FormatterFactory):
    @staticmethod
    def package_name() -> str:
        ...

    def register(self) -> Callable[[], None]:
        ...