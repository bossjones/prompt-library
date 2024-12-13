"""Pylint plugin for checking Marimo cell parameter usage.

This module provides a custom pylint checker for enforcing Marimo cell parameter standards.
It ensures that cell parameters are actually used within the cell.
"""

# pyright: reportAttributeAccessIssue=false
from __future__ import annotations

import copy
import fnmatch
import linecache
import logging
import re
import tokenize

from typing import Any, Dict, Final, Generator, List, Optional, Pattern, Set, Tuple, TypedDict, cast

import astroid
import pysnooper

from astroid import nodes
from astroid.nodes import AssignName, Attribute, Name, NodeNG
from loguru import logger

from pylint import lint
from pylint import utils as pylint_utils
from pylint.checkers import BaseChecker
from pylint.checkers.base.name_checker import NameChecker
from pylint.lint import PyLinter


# NOTE: borrowing from https://github.com/oppia/oppia/blob/develop/scripts/linters/pylint_extensions.py
# List of punctuation symbols that can be used at the end of
# comments and docstrings.
ALLOWED_TERMINATING_PUNCTUATIONS: Final = ['.', '?', '}', ']', ')']

# If any of these phrases are found inside a docstring or comment,
# the punctuation and capital letter checks will be skipped for that
# comment or docstring.
EXCLUDED_PHRASES: Final = [
    'coding:', 'pylint:', 'http://', 'https://', 'scripts/', 'extract_node'
]

ALLOWED_PRAGMAS_FOR_INLINE_COMMENTS: Final = [
    'pylint:', 'isort:', 'type: ignore', 'pragma:', 'https:', 'docker:'
]

ALLOWED_LINES_OF_GAP_IN_COMMENT: Final = 15

from pylint import checkers  # isort:skip  pylint: disable=wrong-import-order, wrong-import-position
from pylint import interfaces  # isort:skip  pylint: disable=wrong-import-order, wrong-import-position
from pylint.checkers import utils as checker_utils  # isort:skip  pylint: disable=wrong-import-order, wrong-import-position
from pylint.extensions import _check_docs_utils # isort:skip  pylint: disable=wrong-import-order, wrong-import-position


def read_from_node(node: astroid.scoped_nodes.Module) -> list[str]:
    """Returns the data read from the ast node in unicode form.

    Args:
        node: astroid.scoped_nodes.Module. Node to access module content.

    Returns:
        list(str). The data read from the ast node.
    """
    # Readlines returns bytes, thus we need to decode them to string.
    return [line.decode('utf-8') for line in node.stream().readlines()]


# @pysnooper.snoop(thread_info=True, max_variable_length=None, depth=10)
class MarimoCellParamsChecker(BaseChecker):  # type: ignore[misc]
    """Checker for enforcing Marimo cell parameter usage standards.

    This checker ensures that:
    1. All cell parameters are actually used within the cell
    2. No unused parameters in cell function definitions
    3. Only necessary dependencies are declared

    Attributes:
        name: The name of the checker
        priority: The priority level of the checker
        msgs: Dictionary of warning messages and their descriptions
        linter: The pylint linter instance
    """


    name = "marimo_cell_params_validator"
    priority = -1
    msgs = {
        # Each message has a code, a message that the user will see,
        # a unique symbol that identifies the message,
        # and a detailed help message
        # that will be included in the documentation.

        "W9301": (
            "Unused cell parameter '%s'",
            "unused-cell-parameter",
            "Cell parameters should only include variables that are actually used in the cell. "
            "Remove unused parameters.",
        ),
    }

    # This class variable declares the options
    # that are configurable by the user.

    options = (
        # Each option definition has a name which is used on the command line
        # and in config files, and a dictionary of arguments
        # (similar to argparse.ArgumentParser.add_argument).
        (
            "ignore-marimo-unused-params",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Force checking of unused parameters even in non-marimo files",
            },
        ),
    )

    def __init__(self, linter: Optional[PyLinter] = None) -> None:
        """Initialize the checker.

        Args:
            linter: The pylint linter instance
        """
        super().__init__(linter if linter is not None else PyLinter())
        self._used_names: set[str] = set()
        self._current_cell_params: set[str] = set()



    def _get_pytest_fixture_node(self, node: nodes.FunctionDef) -> nodes.Call | None:
        """Get the pytest.fixture decorator node if it exists.

        Args:
            node: The function definition node to check.

        Returns:
            nodes.Call | None: The pytest.fixture decorator node if found, None otherwise.
        """
        for decorator in node.decorators.nodes:
            if (
                isinstance(decorator, nodes.Call)
                and decorator.func.as_string() == "pytest.fixture"
            ):
                return decorator

        return None

    def _get_pytest_fixture_node_keyword(
        self, decorator: nodes.Call, search_arg: str
    ) -> nodes.Keyword | None:
        """Get a keyword argument from a pytest.fixture decorator.

        Args:
            decorator: The pytest.fixture decorator node.
            search_arg: The name of the keyword argument to find.

        Returns:
            nodes.Keyword | None: The keyword node if found, None otherwise.
        """
        for keyword in decorator.keywords:
            if keyword.arg == search_arg:
                return keyword

        return None

    def _check_pytest_fixture(
        self, node: nodes.FunctionDef, decoratornames: set[str]
    ) -> None:
        """Check pytest fixture decorators for proper usage.

        Args:
            node: The function definition node to check.
            decoratornames: Set of decorator names to check.

        Returns:
            None
        """
        if (
            "_pytest.fixtures.FixtureFunctionMarker" not in decoratornames
            or not (root_name := node.root().name).startswith("tests.")
            or (decorator := self._get_pytest_fixture_node(node)) is None
            or not (
                scope_keyword := self._get_pytest_fixture_node_keyword(
                    decorator, "scope"
                )
            )
            or not isinstance(scope_keyword.value, nodes.Const)
            or not (scope := scope_keyword.value.value)
        ):
            return

        parts = root_name.split(".")
        test_component: str | None = None
        if root_name.startswith("tests.components.") and parts[2] != "conftest": # type: ignore
            test_component = parts[2] # type: ignore

        if scope == "session":
            if test_component:
                self.add_message(
                    "hass-pytest-fixture-decorator",
                    node=decorator,
                    args=("scope `session`", "use `package` or lower"),
                )
                return
            if not (
                autouse_keyword := self._get_pytest_fixture_node_keyword(
                    decorator, "autouse"
                )
            ) or (
                isinstance(autouse_keyword.value, nodes.Const)
                and not autouse_keyword.value.value
            ):
                self.add_message(
                    "hass-pytest-fixture-decorator",
                    node=decorator,
                    args=(
                        "scope/autouse combination",
                        "set `autouse=True` or reduce scope",
                    ),
                )
            return

        test_module = parts[3] if len(parts) > 3 else "" # type: ignore

        if test_component and scope == "package" and test_module != "conftest":
            self.add_message(
                "hass-pytest-fixture-decorator",
                node=decorator,
                args=("scope `package`", "use `module` or lower"),
            )

    def _is_marimo_notebook(self) -> bool:
        """Check if the current file is a marimo notebook.

        Returns:
            bool: True if the file is a marimo notebook (starts with 'marimo_'),
                 False otherwise.
        """
        try:
            current_file = cast(Any, self.linter.current_file)
            filename = getattr(current_file, 'name', '')
            logger.debug(f"current_file: {current_file}")
            logger.debug(f"Checking if file is marimo notebook: {filename}")

            is_marimo = (
                filename.startswith("marimo_") or
                "marimo" in filename or
                filename.endswith("_notebook.py") or
                filename.endswith("_test.py")
            )

            logger.debug(f"File {filename} {'is' if is_marimo else 'is not'} a marimo notebook")
            return is_marimo

        except AttributeError as e:
            logger.debug(f"AttributeError while checking marimo notebook: {e!s}")
            return False

    def _has_app_cell_decorator(self, node: nodes.FunctionDef) -> bool:
        """Check if a function has the @app.cell decorator.

        Args:
            node: The function definition node to check.

        Returns:
            bool: True if the function has the @app.cell decorator, False otherwise.
        """
        try:
            logger.debug(f"Checking decorators for function: {node.name}")

            if not hasattr(node, "decorators") or not node.decorators:
                logger.debug(f"No decorators found for function: {node.name}")
                return False

            for decorator in node.decorators.nodes:
                logger.debug(f"Found decorator: {decorator.as_string()}")
                if isinstance(decorator, (Name, Attribute)) and decorator.as_string() == "app.cell":
                    logger.debug(f"Found app.cell decorator for function: {node.name}")
                    return True
            logger.debug(f"No app.cell decorator found for function: {node.name}")
            return False
        except AttributeError as e:
            logger.debug(f"AttributeError while checking decorators: {e!s}")
            return False

    @pysnooper.snoop(output='/Users/malcolm/dev/bossjones/prompt-library/pylint-debug.log', thread_info=True, max_variable_length=None, depth=10, color=False)
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Visit and check a function definition node.

        Args:
            node: The function definition node to visit.
        """
        logger.debug(f"Visiting function definition: {node.name}")

        if not self._is_marimo_notebook():
            logger.debug(f"Skipping non-marimo notebook function: {node.name}")
            return

        if not self._has_app_cell_decorator(node):
            logger.debug(f"Skipping function without app.cell decorator: {node.name}")
            return

        # Reset state for new cell
        logger.debug(f"Processing marimo cell function: {node.name}")
        self._used_names = set()
        self._current_cell_params = set()

        # Collect parameter names
        for arg in node.args.args:
            logger.debug(f"Found parameter: {arg.name}")
            self._current_cell_params.add(arg.name)

        logger.debug(f"Cell parameters: {self._current_cell_params}")

        # Walk the function body to collect used names
        for child in node.body:
            child.accept(self)

        # Check for unused parameters
        for param in self._current_cell_params:
            if param not in self._used_names:
                logger.debug(f"Found unused parameter: {param}")
                self.add_message(
                    "unused-cell-parameter",
                    node=node,
                    args=(param,),
                )

    def visit_name(self, node: nodes.Name) -> None:
        """Visit and check a name node.

        Args:
            node: The name node to visit.
        """
        if not self._is_marimo_notebook():
            return

        # Track name usage in load context (when variable is used)
        if isinstance(node, nodes.Name) and node.name in self._current_cell_params:
            ctx_name = getattr(node.ctx, "name", "")
            logger.debug(f"Checking name node: {node.name} with context: {ctx_name}")
            if ctx_name == "Load":
                logger.debug(f"Found usage of parameter: {node.name}")
                self._used_names.add(node.name)

    # def load_configuration(self, linter: PyLinter) -> None:

    #     name_checker: NameChecker = linter.get_checker(NameChecker)
    #     # We consider as good names of variables Hello and World
    #     name_checker.config.good_names += ('Hello', 'World')

    #     # We ignore bin directory
    #     linter.config.black_list += ('bin',)


def register(linter: PyLinter) -> None:
    """Register the MarimoCellParamsChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoCellParamsChecker(linter))

if __name__ == "__main__":
    import sys

    from pathlib import Path

    import astroid
    import bpdb
    import rich

    from astroid import nodes
    from astroid.builder import parse as astroid_parse
    from astroid.nodes import Module
    from loguru import logger

    from prompt_library.bot_logger import get_logger, global_log_config
    from pylint.checkers import BaseChecker
    from pylint.checkers.base_checker import BaseChecker
    from pylint.checkers.utils import only_required_for_messages
    from pylint.interfaces import UNDEFINED
    from pylint.testutils import MessageTest
    from pylint.utils import ASTWalker
    # SOURCE: https://github.com/Delgan/loguru/blob/420704041797daf804b505e5220805528fe26408/docs/resources/recipes.rst#L1083
    global_log_config(
        log_level=logging.getLevelName("DEBUG"),
        json=False,
    )

    # """Decorator to store messages that are handled by a checker method as an
    # attribute of the function object.

    # This information is used by ``ASTWalker`` to decide whether to call the decorated
    # method or not. If none of the messages is enabled, the method will be skipped.
    # Therefore, the list of messages must be well maintained at all times!
    # This decorator only has an effect on ``visit_*`` and ``leave_*`` methods
    # of a class inheriting from ``BaseChecker``.
    # """

    class MockLinter:
        def __init__(self, msgs: dict[str, bool]) -> None:
            self._msgs = msgs

        def is_message_enabled(self, msgid: str) -> bool:
            return self._msgs.get(msgid, True)

    class Checker(BaseChecker):
        # pylint: disable-next=super-init-not-called
        def __init__(self) -> None:
            self.called: set[str] = set()

        @only_required_for_messages("first-message")
        def visit_module(
            self, module: nodes.Module  # pylint: disable=unused-argument
        ) -> None:
            self.called.add("module")
            logger.debug(f"module: {module}")

        @only_required_for_messages("second-message")
        def visit_call(self, module: nodes.Call) -> None:
            raise NotImplementedError

        @only_required_for_messages("second-message", "third-message")
        def visit_assignname(
            self, module: nodes.AssignName  # pylint: disable=unused-argument
        ) -> None:
            self.called.add("assignname")
            logger.debug(f"assignname: {module}")
        @only_required_for_messages("second-message")
        def leave_assignname(self, module: nodes.AssignName) -> None:
            raise NotImplementedError

    # Read the file content
    file_path = Path("marimo_bad.py")
    file_content = file_path.read_text()

    # Extract nodes from the file content
    module: Module = astroid.parse(file_content, module_name="marimo_bad.py", path=f"{file_path}")
    rich.inspect(module, all=True)
    rich.print(module.repr_tree())
    rich.print(module.as_string())

    linter = PyLinter()
    walker = ASTWalker(linter)
    checker = MarimoCellParamsChecker(linter)
    walker.add_checker(checker)

    walker.walk(module)
    node=next(
    node
    for node in module.body
    if isinstance(node, astroid.nodes.FunctionDef)
    and node.name == "__"
    and any(
        isinstance(dec, (astroid.nodes.Name, astroid.nodes.Attribute)) and dec.as_string() == "app.cell"
        for dec in node.decorators.nodes
        )
    )
    bpdb.set_trace()
    rich.print(checker.messages)
    # produces [MessageDefinition:unused-cell-parameter (W9301)]


# nnotations__ = {'decorators': 'node_classes.Decorators | None', 'doc_node': 'Const | None', 'args': 'Arguments'}                                                           │
# │                             args = <Arguments l.3 at 0x109b88e00>                                                                                                                              │
# │           _assign_nodes_in_scope = []                                                                                                                                                          │
# │                  _astroid_fields = ('decorators', 'args', 'returns', 'type_params', 'doc_node', 'body')                                                                                        │
# │              blockstart_tolineno = 3                                                                                                                                                           │
# │                             body = [<Import l.4 at 0x109b89dc0>, <Return l.5 at 0x109b89fd0>]                                                                                                  │
# │                       col_offset = 0                                                                                                                                                           │
# │                       decorators = <Decorators l.2 at 0x109b89100>                                                                                                                             │
# │                         __dict__ = {                                                                                                                                                           │
# │                                        'name': '__',                                                                                                                                           │
# │                                        'locals': {'os': [<Import l.4 at 0x109b89dc0>]},                                                                                                        │
# │                                        'body': [<Import l.4 at 0x109b89dc0>, <Return l.5 at 0x109b89fd0>],                                                                                     │
# │                                        'type_params': [],                                                                                                                                      │
# │                                        'instance_attrs': {},                                                                                                                                   │
# │                                        'lineno': 2,                                                                                                                                            │
# │                                        'col_offset': 0,                                                                                                                                        │
# │                                        'parent': <Module.marimo_test.py l.0 at 0x109ad20f0>,                                                                                                   │
# │                                        'end_lineno': 5,                                                                                                                                        │
# │                                        'end_col_offset': 16,                                                                                                                                   │
# │                                        'position': Position(lineno=3, col_offset=0, end_lineno=3, end_col_offset=6),                                                                           │
# │                                        'args': <Arguments l.3 at 0x109b88e00>,                                                                                                                 │
# │                                        'decorators': <Decorators l.2 at 0x109b89100>,                                                                                                          │
# │                                        'returns': None,                                                                                                                                        │
# │                                        'type_comment_returns': None,                                                                                                                           │
# │                                        'type_comment_args': None,                                                                                                                              │
# │                                        'doc_node': None,                                                                                                                                       │
# │                                        'fromlineno': 3,                                                                                                                                        │
# │                                        '_multi_line_blocks': ([<Import l.4 at 0x109b89dc0>, <Return l.5 at 0x109b89fd0>],),                                                                    │
# │                                        '_assign_nodes_in_scope': [],                                                                                                                           │
# │                                        'blockstart_tolineno': 3,                                                                                                                               │
# │                                        'extra_decorators': [],                                                                                                                                 │
# │                                        'tolineno': 5,                                                                                                                                          │
# │                                        'ty
