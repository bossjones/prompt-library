"""
This type stub file was generated by pyright.
"""

import ast
import dataclasses
from typing import Any, Literal, Mapping, Optional, TYPE_CHECKING
from marimo._ast.visitor import ImportData, Language, Name, VariableData
from collections.abc import Awaitable, Iterable
from types import CodeType
from marimo._ast.app import InternalApp
from marimo._messaging.types import Stream

CellId_t = str
if TYPE_CHECKING:
    ...
@dataclasses.dataclass
class CellConfig:
    column: Optional[int] = ...
    disabled: bool = ...
    hide_code: bool = ...
    @classmethod
    def from_dict(cls, kwargs: dict[str, Any]) -> CellConfig:
        ...

    def asdict(self) -> dict[str, Any]:
        ...

    def asdict_without_defaults(self) -> dict[str, Any]:
        ...

    def is_different_from_default(self) -> bool:
        ...

    def configure(self, update: dict[str, Any] | CellConfig) -> None:
        """Update the config in-place.

        `update` can be a partial config or a CellConfig
        """
        ...



CellConfigKeys = ...
RuntimeStateType = Literal["idle", "queued", "running", "disabled-transitively"]
@dataclasses.dataclass
class RuntimeState:
    state: Optional[RuntimeStateType] = ...


RunResultStatusType = Literal["success", "exception", "cancelled", "interrupted", "marimo-error", "disabled",]
@dataclasses.dataclass
class RunResultStatus:
    state: Optional[RunResultStatusType] = ...


@dataclasses.dataclass
class ImportWorkspace:
    """A workspace for runtimes to use to manage a cell's imports."""
    is_import_block: bool = ...
    imported_defs: set[Name] = ...


@dataclasses.dataclass
class CellStaleState:
    state: bool = ...


@dataclasses.dataclass
class CellOutput:
    output: Any = ...


@dataclasses.dataclass
class ParsedSQLStatements:
    parsed: Optional[list[str]] = ...


@dataclasses.dataclass(frozen=True)
class CellImpl:
    key: int
    code: str
    mod: ast.Module
    defs: set[Name]
    refs: set[Name]
    temporaries: set[Name]
    variable_data: dict[Name, list[VariableData]]
    deleted_refs: set[Name]
    body: Optional[CodeType]
    last_expr: Optional[CodeType]
    language: Language
    cell_id: CellId_t
    config: CellConfig = ...
    import_workspace: ImportWorkspace = ...
    _status: RuntimeState = ...
    _run_result_status: RunResultStatus = ...
    _stale: CellStaleState = ...
    _output: CellOutput = ...
    _sqls: ParsedSQLStatements = ...
    def configure(self, update: dict[str, Any] | CellConfig) -> CellImpl:
        """Update the cell config.

        `update` can be a partial config.
        """
        ...

    @property
    def runtime_state(self) -> Optional[RuntimeStateType]:
        ...

    @property
    def run_result_status(self) -> Optional[RunResultStatusType]:
        ...

    @property
    def sqls(self) -> list[str]:
        """Return a list of SQL statements for this cell."""
        ...

    @property
    def stale(self) -> bool:
        ...

    @property
    def disabled_transitively(self) -> bool:
        ...

    @property
    def imports(self) -> Iterable[ImportData]:
        """Return a set of import data for this cell."""
        ...

    @property
    def imported_namespaces(self) -> set[Name]:
        """Return a set of the namespaces imported by this cell."""
        ...

    def namespace_to_variable(self, namespace: str) -> Name | None:
        """Returns the variable name corresponding to an imported namespace

        Relevant for imports "as" imports, eg

        import matplotlib.pyplot as plt

        In this case the namespace is "matplotlib" but the name is "plt".
        """
        ...

    def is_coroutine(self) -> bool:
        ...

    def set_runtime_state(self, status: RuntimeStateType, stream: Stream | None = ...) -> None:
        """Set execution status and broadcast to frontends."""
        ...

    def set_run_result_status(self, run_result_status: RunResultStatusType) -> None:
        ...

    def set_stale(self, stale: bool, stream: Stream | None = ...) -> None:
        ...

    def set_output(self, output: Any) -> None:
        ...

    @property
    def output(self) -> Any:
        ...



@dataclasses.dataclass
class Cell:
    """An executable notebook cell

    A `Cell` object can be executed as a function via its `run()` method, which
    returns the cell's last expression (output) and a mapping from its defined
    names to its values.

    Cells can be named via the marimo editor in the browser, or by
    changing the cell's function name in the notebook file. Named
    cells can then be executed for use in other notebooks, or to test
    in unit tests.

    For example:

    ```python
    from my_notebook import my_cell

    output, definitions = my_cell.run()
    ```

    See the documentation of `run` for info and examples.
    """
    _name: str
    _cell: CellImpl
    _app: InternalApp | None = ...
    @property
    def name(self) -> str:
        ...

    @property
    def refs(self) -> set[str]:
        """The references that this cell takes as input"""
        ...

    @property
    def defs(self) -> set[str]:
        """The definitions made by this cell"""
        ...

    def run(self, **refs: Any) -> (tuple[Any, Mapping[str, Any]] | Awaitable[tuple[Any, Mapping[str, Any]]]):
        """Run this cell and return its visual output and definitions

        Use this method to run **named cells** and retrieve their output and
        definitions.

        This lets you use reuse cells defined in one notebook in another
        notebook or Python file. It also makes it possible to write and execute
        unit tests for notebook cells using a test framework like `pytest`.

        **Example.** marimo cells can be given names either through the
        editor cell menu or by manually changing the function name in the
        notebook file. For example, consider a notebook `notebook.py`:

        ```python
        import marimo

        app = marimo.App()


        @app.cell
        def __():
            import marimo as mo

            return (mo,)


        @app.cell
        def __():
            x = 0
            y = 1
            return (x, y)


        @app.cell
        def add(mo, x, y):
            z = x + y
            mo.md(f"The value of z is {z}")
            return (z,)


        if __name__ == "__main__":
            app.run()
        ```

        To reuse the `add` cell in another notebook, you'd simply write

        ```python
        from notebook import add

        # `output` is the markdown rendered by `add`
        # defs["z"] == `1`
        output, defs = add.run()
        ```

        When `run` is called without arguments, it automatically computes the
        values that the cell depends on (in this case, `mo`, `x`, and `y`). You
        can override these values by providing any subset of them as keyword
        arguments. For example,

        ```python
        # defs["z"] == 4
        output, defs = add.run(x=2, y=2)
        ```

        **Defined UI Elements.** If the cell's `output` has UI elements
        that are in `defs`, interacting with the output in the frontend will
        trigger reactive execution of cells that reference the `defs` object.
        For example, if `output` has a slider defined by the cell, then
        scrubbing the slider will cause cells that reference `defs` to run.

        **Async cells.** If this cell is a coroutine function (starting with
        `async`), or if any of its ancestors are coroutine functions, then
        you'll need to `await` the result: `output, defs = await cell.run()`.
        You can check whether the result is an awaitable using:

        ```python
        from collections.abc import Awaitable

        ret = cell.run()
        if isinstance(ret, Awaitable):
            output, defs = await ret
        else:
            output, defs = ret
        ```

        **Arguments**:

        - You may pass values for any of this cell's references as keyword
          arguments. marimo will automatically compute values for any refs
          that are not provided by executing the parent cells that compute
          them.

        **Returns**:

        - a tuple `(output, defs)`, or an awaitable of the same, where `output`
          is the cell's last expression and `defs` is a `Mapping` from the
          cell's defined names to their values.
        """
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        ...



@dataclasses.dataclass
class SourcePosition:
    filename: str
    lineno: int
    col_offset: int
    ...


def is_ws(char: str) -> bool:
    ...