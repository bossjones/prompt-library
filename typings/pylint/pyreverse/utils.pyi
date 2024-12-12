"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import Any, Optional, TYPE_CHECKING, Union
from astroid import nodes
from astroid.typing import InferenceResult
from pylint.pyreverse.diagrams import ClassDiagram, PackageDiagram

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    _CallbackT = Callable[[nodes.NodeNG], Union[tuple[ClassDiagram], tuple[PackageDiagram, ClassDiagram], None],]
    _CallbackTupleT = tuple[Optional[_CallbackT], Optional[_CallbackT]]
RCFILE = ...
def get_default_options() -> list[str]:
    """Read config file and return list of options."""
    ...

def insert_default_options() -> None:
    """Insert default options to sys.argv."""
    ...

SPECIAL = ...
PRIVATE = ...
PROTECTED = ...
def get_visibility(name: str) -> str:
    """Return the visibility from a name: public, protected, private or special."""
    ...

def is_exception(node: nodes.ClassDef) -> bool:
    ...

_SPECIAL = ...
_PROTECTED = ...
_PRIVATE = ...
MODES = ...
VIS_MOD = ...
class FilterMixIn:
    """Filter nodes according to a mode and nodes' visibility."""
    def __init__(self, mode: str) -> None:
        """Init filter modes."""
        ...

    def show_attr(self, node: nodes.NodeNG | str) -> bool:
        """Return true if the node should be treated."""
        ...



class LocalsVisitor:
    """Visit a project by traversing the locals dictionary.

    * visit_<class name> on entering a node, where class name is the class of
    the node in lower case

    * leave_<class name> on leaving a node, where class name is the class of
    the node in lower case
    """
    def __init__(self) -> None:
        ...

    def get_callbacks(self, node: nodes.NodeNG) -> _CallbackTupleT:
        """Get callbacks from handler for the visited node."""
        ...

    def visit(self, node: nodes.NodeNG) -> Any:
        """Launch the visit starting from the given node."""
        ...



def get_annotation_label(ann: nodes.Name | nodes.NodeNG) -> str:
    ...

def get_annotation(node: nodes.AssignAttr | nodes.AssignName) -> nodes.Name | nodes.Subscript | None:
    """Return the annotation for `node`."""
    ...

def infer_node(node: nodes.AssignAttr | nodes.AssignName) -> set[InferenceResult]:
    """Return a set containing the node annotation if it exists
    otherwise return a set of the inferred types using the NodeNG.infer method.
    """
    ...

def check_graphviz_availability() -> None:
    """Check if the ``dot`` command is available on the machine.

    This is needed if image output is desired and ``dot`` is used to convert
    from *.dot or *.gv into the final output format.
    """
    ...

def check_if_graphviz_supports_format(output_format: str) -> None:
    """Check if the ``dot`` command supports the requested output format.

    This is needed if image output is desired and ``dot`` is used to convert
    from *.gv into the final output format.
    """
    ...
