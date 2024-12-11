"""
This type stub file was generated by pyright.
"""

import narwhals.stable.v1 as nw
from dataclasses import dataclass
from typing import Any, Callable, Dict, Final, List, Optional, TYPE_CHECKING, TypedDict, Union
from narwhals.typing import IntoDataFrame
from marimo._output.rich_help import mddoc
from marimo._plugins.ui._core.ui_element import UIElement

LOGGER = ...
if TYPE_CHECKING:
    ...
@dataclass
class DataEditorValue:
    data: List[Dict[str, Any]]
    ...


class PositionalEdit(TypedDict):
    rowIdx: int
    columnId: str
    value: Any
    ...


class DataEdits(TypedDict):
    edits: List[PositionalEdit]
    ...


RowOrientedData = List[Dict[str, Any]]
ColumnOrientedData = Dict[str, List[Any]]
@mddoc
class data_editor(UIElement[DataEdits, Union[RowOrientedData, ColumnOrientedData, IntoDataFrame],]):
    """
    **[EXPERIMENTAL]**

    This component is experimental and intentionally limited in features,
    if you have any feature requests, please file an issue at
    https://github.com/marimo-team/marimo/issues.

    A data editor component for editing tabular data.

    The data can be supplied as:
    1. a Pandas, Polars, or Pyarrow DataFrame
    2. a list of dicts, with one dict for each row, keyed by column names
    3. a dict of lists, with each list representing a column

    **Examples.**

    Create a data editor from a Pandas dataframe:

    ```python
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
    editor = mo.ui.experimental_data_editor(data=df, label="Edit Data")
    ```

    Create a data editor from a list of dicts:

    ```python
    data = [{"A": 1, "B": "a"}, {"A": 2, "B": "b"}, {"A": 3, "B": "c"}]
    editor = mo.ui.experimental_data_editor(data=data, label="Edit Data")
    ```

    Create a data editor from a dict of lists:

    ```python
    data = {"A": [1, 2, 3], "B": ["a", "b", "c"]}
    editor = mo.ui.experimental_data_editor(data=data, label="Edit Data")
    ```

    **Attributes.**

    - `value`: the current state of the edited data
    - `data`: the original data passed to the editor

    **Initialization Args.**

    - `data`: The data to be edited. Can be a Pandas dataframe,
        a list of dicts, or a dict of lists.
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    """
    _name: Final[str] = ...
    LIMIT: Final[int] = ...
    def __init__(self, data: Union[RowOrientedData, ColumnOrientedData, IntoDataFrame], *, pagination: bool = ..., page_size: int = ..., label: str = ..., on_change: Optional[Callable[[Union[RowOrientedData, ColumnOrientedData, IntoDataFrame]], None,]] = ...) -> None:
        ...

    @property
    def data(self) -> Union[RowOrientedData, ColumnOrientedData, IntoDataFrame]:
        ...

    def __hash__(self) -> int:
        ...



def apply_edits(data: Union[RowOrientedData, ColumnOrientedData, IntoDataFrame], edits: DataEdits, schema: Optional[nw.Schema] = ...) -> Union[RowOrientedData, ColumnOrientedData, IntoDataFrame]:
    ...
