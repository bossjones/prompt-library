"""
This type stub file was generated by pyright.
"""

from typing import Any, List
from marimo._plugins.ui._impl.tables.table_manager import TableManager, TableManagerFactory

MANAGERS: List[TableManagerFactory] = ...
def get_table_manager(data: Any) -> TableManager[Any]:
    ...

def get_table_manager_or_none(data: Any) -> TableManager[Any] | None:
    ...