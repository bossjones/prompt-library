"""
This type stub file was generated by pyright.
"""

from typing import Any
from marimo._config.config import Theme
from marimo._output.formatters.formatter_factory import FormatterFactory
from marimo._output.hypertext import Html

class PlotlyFormatter(FormatterFactory):
    @staticmethod
    def package_name() -> str:
        ...

    def register(self) -> None:
        ...

    @staticmethod
    def render_plotly_dict(json: dict[Any, Any]) -> Html:
        ...

    def apply_theme(self, theme: Theme) -> None:
        ...
