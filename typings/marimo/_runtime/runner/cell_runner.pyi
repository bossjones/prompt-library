"""
This type stub file was generated by pyright.
"""

import contextlib
from dataclasses import dataclass
from typing import Any, Callable, Optional, TYPE_CHECKING, Union
from marimo._ast.cell import CellId_t
from marimo._config.config import ExecutionType, OnCellChangeType
from marimo._messaging.errors import Error
from marimo._runtime import dataflow
from marimo._runtime.marimo_pdb import MarimoPdb
from collections.abc import Sequence
from marimo._runtime.context.types import ExecutionContext
from marimo._runtime.runner.hooks_on_finish import OnFinishHookType
from marimo._runtime.runner.hooks_post_execution import PostExecutionHookType
from marimo._runtime.runner.hooks_pre_execution import PreExecutionHookType
from marimo._runtime.runner.hooks_preparation import PreparationHookType
from marimo._runtime.state import State

LOGGER = ...
if TYPE_CHECKING:
    ...
def cell_filename(cell_id: CellId_t) -> str:
    """Filename to use when running cells through exec."""
    ...

ErrorObjects = Union[BaseException, Error]
@dataclass
class RunResult:
    output: Any
    exception: Optional[ErrorObjects]
    accumulated_output: Any = ...
    def success(self) -> bool:
        """Whether the cell expected successfully"""
        ...



class Runner:
    """Runner for a collection of cells."""
    def __init__(self, roots: set[CellId_t], graph: dataflow.DirectedGraph, glbls: dict[Any, Any], debugger: MarimoPdb | None, execution_mode: OnCellChangeType = ..., execution_type: ExecutionType = ..., excluded_cells: set[CellId_t] | None = ..., execution_context: Callable[[CellId_t], contextlib._GeneratorContextManager[ExecutionContext]] | None = ..., preparation_hooks: Sequence[PreparationHookType] | None = ..., pre_execution_hooks: Sequence[PreExecutionHookType] | None = ..., post_execution_hooks: Sequence[PostExecutionHookType] | None = ..., on_finish_hooks: Sequence[OnFinishHookType] | None = ...) -> None:
        ...

    @staticmethod
    def compute_cells_to_run(graph: dataflow.DirectedGraph, roots: set[CellId_t], excluded_cells: set[CellId_t], execution_mode: OnCellChangeType) -> list[CellId_t]:
        ...

    def cancel(self, cell_id: CellId_t) -> None:
        """Mark a cell (and its descendants) as cancelled."""
        ...

    def cancelled(self, cell_id: CellId_t) -> bool:
        """Return whether a cell has been cancelled."""
        ...

    def pending(self) -> bool:
        """Whether there are more cells to run."""
        ...

    def resolve_state_updates(self, state_updates: dict[State[Any], CellId_t]) -> set[CellId_t]:
        """
        Get cells that need to be run as a consequence of state updates

        A cell is marked as needing to run if all of the following are true:

            1. The runner was not interrupted.
            2. It was not already run after its setter was called.
            3. It isn't the cell that called the setter (unless the state
               object was configured to allow self loops).
            4. It is not errored (unable to run) or cancelled.
            5. It has among its refs the state object whose setter
               was invoked.

        (3) means that a state update in a given cell will never re-trigger
        the same cell to run. This is similar to how interacting with
        a UI element in the cell that created it won't re-trigger the cell,
        and this behavior is useful when tying UI elements together with a
        state object.

        **Arguments.**

        - state_updates: mapping from state object to the cell that last ran
          its setter
        - errored_cells: cell ids that are unable to run
        """
        ...

    def pop_cell(self) -> CellId_t:
        """Get the next cell to run."""
        ...

    async def run(self, cell_id: CellId_t) -> RunResult:
        """Run a cell."""
        ...

    async def run_all(self) -> None:
        ...