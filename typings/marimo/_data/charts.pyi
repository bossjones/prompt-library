"""
This type stub file was generated by pyright.
"""

import abc
from dataclasses import dataclass
from typing import Any
from marimo._data.models import DataType

@abc.abstractmethod
class ChartBuilder:
    @abc.abstractmethod
    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_json(self, data: Any, column: str) -> str:
        ...

    @abc.abstractmethod
    def altair_code(self, data: str, column: str) -> str:
        ...



@dataclass
class ChartParams:
    table_name: str
    column: str
    ...


class NumberChartBuilder(ChartBuilder):
    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_code(self, data: str, column: str) -> str:
        ...



class StringChartBuilder(ChartBuilder):
    def __init__(self, should_limit_to_10_items: bool) -> None:
        ...

    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_code(self, data: str, column: str) -> str:
        ...



class DateChartBuilder(ChartBuilder):
    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_code(self, data: str, column: str) -> str:
        ...



class BooleanChartBuilder(ChartBuilder):
    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_code(self, data: str, column: str) -> str:
        ...



class IntegerChartBuilder(ChartBuilder):
    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_code(self, data: str, column: str) -> str:
        ...



class UnknownChartBuilder(ChartBuilder):
    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_code(self, data: str, column: str) -> str:
        ...



class WrapperChartBuilder(ChartBuilder):
    def __init__(self, delegate: ChartBuilder) -> None:
        ...

    def altair(self, data: Any, column: str) -> Any:
        ...

    def altair_code(self, data: str, column: str) -> str:
        ...



def get_chart_builder(column_type: DataType, should_limit_to_10_items: bool = ...) -> ChartBuilder:
    ...
