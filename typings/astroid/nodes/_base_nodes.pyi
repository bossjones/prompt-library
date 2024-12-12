"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Generator, Iterator
from functools import cached_property, lru_cache, partial
from typing import ClassVar, Optional, TYPE_CHECKING, Union
from astroid import nodes
from astroid.context import InferenceContext
from astroid.nodes.node_ng import NodeNG
from astroid.typing import InferenceResult
from astroid.nodes.node_classes import LocalsDictNodeNG

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    GetFlowFactory = Callable[[InferenceResult, Optional[InferenceResult], Union[nodes.AugAssign, nodes.BinOp], InferenceResult, Optional[InferenceResult], InferenceContext, InferenceContext], list[partial[Generator[InferenceResult]]],]
class Statement(NodeNG):
    """Statement node adding a few attributes.

    NOTE: This class is part of the public API of 'astroid.nodes'.
    """
    is_statement = ...
    def next_sibling(self):
        """The next sibling statement node.

        :returns: The next sibling statement node.
        :rtype: NodeNG or None
        """
        ...
    
    def previous_sibling(self):
        """The previous sibling statement.

        :returns: The previous sibling statement node.
        :rtype: NodeNG or None
        """
        ...
    


class NoChildrenNode(NodeNG):
    """Base nodes for nodes with no children, e.g. Pass."""
    def get_children(self) -> Iterator[NodeNG]:
        ...
    


class FilterStmtsBaseNode(NodeNG):
    """Base node for statement filtering and assignment type."""
    def assign_type(self):
        ...
    


class AssignTypeNode(NodeNG):
    """Base node for nodes that can 'assign' such as AnnAssign."""
    def assign_type(self):
        ...
    


class ParentAssignNode(AssignTypeNode):
    """Base node for nodes whose assign_type is determined by the parent node."""
    def assign_type(self):
        ...
    


class ImportNode(FilterStmtsBaseNode, NoChildrenNode, Statement):
    """Base node for From and Import Nodes."""
    modname: str | None
    names: list[tuple[str, str | None]]
    def do_import_module(self, modname: str | None = ...) -> nodes.Module:
        """Return the ast for a module whose name is <modname> imported by <self>."""
        ...
    
    def real_name(self, asname: str) -> str:
        """Get name from 'as' name."""
        ...
    


class MultiLineBlockNode(NodeNG):
    """Base node for multi-line blocks, e.g. For and FunctionDef.

    Note that this does not apply to every node with a `body` field.
    For instance, an If node has a multi-line body, but the body of an
    IfExpr is not multi-line, and hence cannot contain Return nodes,
    Assign nodes, etc.
    """
    _multi_line_block_fields: ClassVar[tuple[str, ...]] = ...


class MultiLineWithElseBlockNode(MultiLineBlockNode):
    """Base node for multi-line blocks that can have else statements."""
    @cached_property
    def blockstart_tolineno(self):
        ...
    


class LookupMixIn(NodeNG):
    """Mixin to look up a name in the right scope."""
    @lru_cache
    def lookup(self, name: str) -> tuple[LocalsDictNodeNG, list[NodeNG]]:
        """Lookup where the given variable is assigned.

        The lookup starts from self's scope. If self is not a frame itself
        and the name is found in the inner frame locals, statements will be
        filtered to remove ignorable statements according to self's location.

        :param name: The name of the variable to find assignments for.

        :returns: The scope node and the list of assignments associated to the
            given name according to the scope where it has been found (locals,
            globals or builtin).
        """
        ...
    
    def ilookup(self, name):
        """Lookup the inferred values of the given variable.

        :param name: The variable name to find values for.
        :type name: str

        :returns: The inferred values of the statements returned from
            :meth:`lookup`.
        :rtype: iterable
        """
        ...
    


BIN_OP_METHOD = ...
REFLECTED_BIN_OP_METHOD = ...
AUGMENTED_OP_METHOD = ...
class OperatorNode(NodeNG):
    ...


