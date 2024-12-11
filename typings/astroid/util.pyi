"""
This type stub file was generated by pyright.
"""

from typing import Any, Final, Literal, TYPE_CHECKING
from astroid import bases, nodes
from astroid.context import InferenceContext
from astroid.typing import InferenceResult

if TYPE_CHECKING:
    ...
class UninferableBase:
    """Special inference object, which is returned when inference fails.

    This is meant to be used as a singleton. Use astroid.util.Uninferable to access it.
    """
    def __repr__(self) -> Literal["Uninferable"]:
        ...

    __str__ = ...
    def __getattribute__(self, name: str) -> Any:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> UninferableBase:
        ...

    def __bool__(self) -> Literal[False]:
        ...

    __nonzero__ = ...
    def accept(self, visitor):
        ...



Uninferable: Final = ...
class BadOperationMessage:
    """Object which describes a TypeError occurred somewhere in the inference chain.

    This is not an exception, but a container object which holds the types and
    the error which occurred.
    """
    ...


class BadUnaryOperationMessage(BadOperationMessage):
    """Object which describes operational failures on UnaryOps."""
    def __init__(self, operand, op, error) -> None:
        ...

    def __str__(self) -> str:
        ...



class BadBinaryOperationMessage(BadOperationMessage):
    """Object which describes type errors for BinOps."""
    def __init__(self, left_type, op, right_type) -> None:
        ...

    def __str__(self) -> str:
        ...



def check_warnings_filter() -> bool:
    """Return True if any other than the default DeprecationWarning filter is enabled.

    https://docs.python.org/3/library/warnings.html#default-warning-filter
    """
    ...

def safe_infer(node: nodes.NodeNG | bases.Proxy | UninferableBase, context: InferenceContext | None = ...) -> InferenceResult | None:
    """Return the inferred value for the given node.

    Return None if inference failed or if there is some ambiguity (more than
    one node has been inferred).
    """
    ...