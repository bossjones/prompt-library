"""
This type stub file was generated by pyright.
"""

from marimo._ast.cell import CellId_t
from marimo._messaging.errors import CycleError, DeleteNonlocalError, Error, MultipleDefinitionError
from marimo._runtime.dataflow import DirectedGraph

def check_for_multiple_definitions(graph: DirectedGraph) -> dict[CellId_t, list[MultipleDefinitionError]]:
    """Check whether multiple cells define the same global name."""
    ...

def check_for_delete_nonlocal(graph: DirectedGraph) -> dict[CellId_t, list[DeleteNonlocalError]]:
    """Check whether cells delete their refs."""
    ...

def check_for_cycles(graph: DirectedGraph) -> dict[CellId_t, list[CycleError]]:
    """Return cycle errors, if any."""
    ...

def check_for_errors(graph: DirectedGraph) -> dict[CellId_t, tuple[Error, ...]]:
    """
    Check graph for violations of marimo semantics.

    Return a dict of errors in the graph, with an entry for each cell
    that is involved in an error.
    """
    ...