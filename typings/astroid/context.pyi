"""
This type stub file was generated by pyright.
"""

import contextlib
from collections.abc import Iterator, Sequence
from typing import Optional, TYPE_CHECKING
from astroid.typing import InferenceResult, SuccessfulInferenceResult
from astroid import nodes
from astroid.nodes.node_classes import Keyword, NodeNG

"""Various context related utilities, including inference and call contexts."""
if TYPE_CHECKING:
    ...
_InferenceCache = dict[tuple["NodeNG", Optional[str], Optional[str], Optional[str]], Sequence["NodeNG"]]
_INFERENCE_CACHE: _InferenceCache = ...
class InferenceContext:
    """Provide context for inference.

    Store already inferred nodes to save time
    Account for already visited nodes to stop infinite recursion
    """
    __slots__ = ...
    max_inferred = ...
    def __init__(self, path: set[tuple[nodes.NodeNG, str | None]] | None = ..., nodes_inferred: list[int] | None = ...) -> None:
        ...

    @property
    def nodes_inferred(self) -> int:
        """
        Number of nodes inferred in this context and all its clones/descendents.

        Wrap inner value in a mutable cell to allow for mutating a class
        variable in the presence of __slots__
        """
        ...

    @nodes_inferred.setter
    def nodes_inferred(self, value: int) -> None:
        ...

    @property
    def inferred(self) -> _InferenceCache:
        """
        Inferred node contexts to their mapped results.

        Currently the key is ``(node, lookupname, callcontext, boundnode)``
        and the value is tuple of the inferred results
        """
        ...

    def push(self, node: nodes.NodeNG) -> bool:
        """Push node into inference path.

        Allows one to see if the given node has already
        been looked at for this inference context
        """
        ...

    def clone(self) -> InferenceContext:
        """Clone inference path.

        For example, each side of a binary operation (BinOp)
        starts with the same context but diverge as each side is inferred
        so the InferenceContext will need be cloned
        """
        ...

    @contextlib.contextmanager
    def restore_path(self) -> Iterator[None]:
        ...

    def is_empty(self) -> bool:
        ...

    def __str__(self) -> str:
        ...



class CallContext:
    """Holds information for a call site."""
    __slots__ = ...
    def __init__(self, args: list[NodeNG], keywords: list[Keyword] | None = ..., callee: InferenceResult | None = ...) -> None:
        ...



def copy_context(context: InferenceContext | None) -> InferenceContext:
    """Clone a context if given, or return a fresh context."""
    ...

def bind_context_to_node(context: InferenceContext | None, node: SuccessfulInferenceResult) -> InferenceContext:
    """Give a context a boundnode
    to retrieve the correct function name or attribute value
    with from further inference.

    Do not use an existing context since the boundnode could then
    be incorrectly propagated higher up in the call stack.
    """
    ...
