"""
This type stub file was generated by pyright.
"""

import abc
import functools
from collections.abc import Iterable, Sequence
from tokenize import TokenInfo
from typing import Any, TYPE_CHECKING
from astroid import nodes
from pylint.config.arguments_provider import _ArgumentsProvider
from pylint.interfaces import Confidence
from pylint.message.message_definition import MessageDefinition
from pylint.typing import MessageDefinitionTuple, OptionDict, Options, ReportsCallable
from pylint.lint import PyLinter

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
@functools.total_ordering
class BaseChecker(_ArgumentsProvider):
    name: str = ...
    options: Options = ...
    msgs: dict[str, MessageDefinitionTuple] = ...
    reports: tuple[tuple[str, str, ReportsCallable], ...] = ...
    enabled: bool = ...
    def __init__(self, linter: PyLinter) -> None:
        """Checker instances should have the linter as argument."""
        ...

    def __gt__(self, other: Any) -> bool:
        """Permits sorting checkers for stable doc and tests.

        The main checker is always the first one, then builtin checkers in alphabetical
        order, then extension checkers in alphabetical order.
        """
        ...

    def __eq__(self, other: object) -> bool:
        """Permit to assert Checkers are equal."""
        ...

    def __hash__(self) -> int:
        """Make Checker hashable."""
        ...

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        """This might be incomplete because multiple classes inheriting BaseChecker
        can have the same name.

        See: MessageHandlerMixIn.get_full_documentation()
        """
        ...

    def get_full_documentation(self, msgs: dict[str, MessageDefinitionTuple], options: Iterable[tuple[str, OptionDict, Any]], reports: Sequence[tuple[str, str, ReportsCallable]], doc: str | None = ..., module: str | None = ..., show_options: bool = ...) -> str:
        ...

    def add_message(self, msgid: str, line: int | None = ..., node: nodes.NodeNG | None = ..., args: Any = ..., confidence: Confidence | None = ..., col_offset: int | None = ..., end_lineno: int | None = ..., end_col_offset: int | None = ...) -> None:
        ...

    def check_consistency(self) -> None:
        """Check the consistency of msgid.

        msg ids for a checker should be a string of len 4, where the two first
        characters are the checker id and the two last the msg id in this
        checker.

        :raises InvalidMessageError: If the checker id in the messages are not
        always the same.
        """
        ...

    def create_message_definition_from_tuple(self, msgid: str, msg_tuple: MessageDefinitionTuple) -> MessageDefinition:
        ...

    @property
    def messages(self) -> list[MessageDefinition]:
        ...

    def open(self) -> None:
        """Called before visiting project (i.e. set of modules)."""
        ...

    def close(self) -> None:
        """Called after visiting project (i.e set of modules)."""
        ...

    def get_map_data(self) -> Any:
        ...

    def reduce_map_data(self, linter: PyLinter, data: list[Any]) -> None:
        ...



class BaseTokenChecker(BaseChecker):
    """Base class for checkers that want to have access to the token stream."""
    @abc.abstractmethod
    def process_tokens(self, tokens: list[TokenInfo]) -> None:
        """Should be overridden by subclasses."""
        ...



class BaseRawFileChecker(BaseChecker):
    """Base class for checkers which need to parse the raw file."""
    @abc.abstractmethod
    def process_module(self, node: nodes.Module) -> None:
        """Process a module.

        The module's content is accessible via ``astroid.stream``
        """
        ...
