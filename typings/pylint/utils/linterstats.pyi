"""
This type stub file was generated by pyright.
"""

from typing import Literal, TypedDict
from pylint.typing import MessageTypesFullName

"""
This type stub file was generated by pyright.
"""
class BadNames(TypedDict):
    """TypedDict to store counts of node types with bad names."""
    argument: int
    attr: int
    klass: int
    class_attribute: int
    class_const: int
    const: int
    inlinevar: int
    function: int
    method: int
    module: int
    variable: int
    typevar: int
    typealias: int
    ...


class CodeTypeCount(TypedDict):
    """TypedDict to store counts of lines of code types."""
    code: int
    comment: int
    docstring: int
    empty: int
    total: int
    ...


class DuplicatedLines(TypedDict):
    """TypedDict to store counts of lines of duplicated code."""
    nb_duplicated_lines: int
    percent_duplicated_lines: float
    ...


class NodeCount(TypedDict):
    """TypedDict to store counts of different types of nodes."""
    function: int
    klass: int
    method: int
    module: int
    ...


class UndocumentedNodes(TypedDict):
    """TypedDict to store counts of undocumented node types."""
    function: int
    klass: int
    method: int
    module: int
    ...


class ModuleStats(TypedDict):
    """TypedDict to store counts of types of messages and statements."""
    convention: int
    error: int
    fatal: int
    info: int
    refactor: int
    statement: int
    warning: int
    ...


class LinterStats:
    """Class used to linter stats."""
    def __init__(self, bad_names: BadNames | None = ..., by_module: dict[str, ModuleStats] | None = ..., by_msg: dict[str, int] | None = ..., code_type_count: CodeTypeCount | None = ..., dependencies: dict[str, set[str]] | None = ..., duplicated_lines: DuplicatedLines | None = ..., node_count: NodeCount | None = ..., undocumented: UndocumentedNodes | None = ...) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        ...

    def init_single_module(self, module_name: str) -> None:
        """Use through PyLinter.set_current_module so PyLinter.current_name is
        consistent.
        """
        ...

    def get_bad_names(self, node_name: Literal["argument", "attr", "class", "class_attribute", "class_const", "const", "inlinevar", "function", "method", "module", "variable", "typevar", "typealias",]) -> int:
        """Get a bad names node count."""
        ...

    def increase_bad_name(self, node_name: str, increase: int) -> None:
        """Increase a bad names node count."""
        ...

    def reset_bad_names(self) -> None:
        """Resets the bad_names attribute."""
        ...

    def get_code_count(self, type_name: Literal["code", "comment", "docstring", "empty", "total"]) -> int:
        """Get a code type count."""
        ...

    def reset_code_count(self) -> None:
        """Resets the code_type_count attribute."""
        ...

    def reset_duplicated_lines(self) -> None:
        """Resets the duplicated_lines attribute."""
        ...

    def get_node_count(self, node_name: Literal["function", "class", "method", "module"]) -> int:
        """Get a node count while handling some extra conditions."""
        ...

    def reset_node_count(self) -> None:
        """Resets the node count attribute."""
        ...

    def get_undocumented(self, node_name: Literal["function", "class", "method", "module"]) -> float:
        """Get a undocumented node count."""
        ...

    def reset_undocumented(self) -> None:
        """Resets the undocumented attribute."""
        ...

    def get_global_message_count(self, type_name: str) -> int:
        """Get a global message count."""
        ...

    def get_module_message_count(self, modname: str, type_name: MessageTypesFullName) -> int:
        """Get a module message count."""
        ...

    def increase_single_message_count(self, type_name: str, increase: int) -> None:
        """Increase the message type count of an individual message type."""
        ...

    def increase_single_module_message_count(self, modname: str, type_name: MessageTypesFullName, increase: int) -> None:
        """Increase the message type count of an individual message type of a
        module.
        """
        ...

    def reset_message_count(self) -> None:
        """Resets the message type count of the stats object."""
        ...



def merge_stats(stats: list[LinterStats]) -> LinterStats:
    """Used to merge multiple stats objects into a new one when pylint is run in
    parallel mode.
    """
    ...
