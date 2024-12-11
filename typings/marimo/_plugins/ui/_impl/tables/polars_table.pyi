"""
This type stub file was generated by pyright.
"""

from typing import Any, Union
from marimo._plugins.ui._impl.tables.narwhals_table import NarwhalsTableManager
from marimo._plugins.ui._impl.tables.table_manager import TableManager, TableManagerFactory

class PolarsTableManagerFactory(TableManagerFactory):
    @staticmethod
    def package_name() -> str:
        ...

    @staticmethod
    def create() -> type[TableManager[Any]]:
        class PolarsTableManager(NarwhalsTableManager[Union[pl.DataFrame, pl.LazyFrame]]):
            ...