"""Pylint plugin for checking Marimo cell parameter usage.

This module provides a custom pylint checker for enforcing Marimo cell parameter standards.
It ensures that cell parameters are actually used within the cell.
"""

# pyright: reportAttributeAccessIssue=false
from __future__ import annotations

import copy
import fnmatch
import linecache
import re
import tokenize


# import pdb
# pdb.set_trace()
from typing import Any, Dict, Final, Generator, List, Optional, Pattern, Set, Tuple, TypedDict, cast

import astroid
import pysnooper

from astroid import nodes
from astroid.nodes import AssignName, Attribute, Name, NodeNG
from loguru import logger

from pylint import lint
from pylint import utils as pylint_utils
from pylint.checkers import BaseChecker
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

    def _is_marimo_notebook(self) -> bool:
        """Check if the current file is a marimo notebook.

        Returns:
            bool: True if the file is a marimo notebook (starts with 'marimo_'),
                 False otherwise.
        """
        try:
            current_file = cast(Any, self.linter.current_file)
            filename = getattr(current_file, 'name', '')
            return (
                filename.startswith("marimo_") or
                "marimo" in filename or
                filename.endswith("_notebook.py") or
                filename.endswith("_test.py")
            )
        except AttributeError:
            return False

    def _has_app_cell_decorator(self, node: nodes.FunctionDef | nodes.AsyncFunctionDef) -> bool:
        """Check if a function has the @app.cell decorator.

        Args:
            node: The function definition node to check.

        Returns:
            bool: True if the function has the @app.cell decorator, False otherwise.
        """
        try:
            if not hasattr(node, "decorators") or not node.decorators:
                return False

            for decorator in node.decorators.nodes:
                if isinstance(decorator, (Name, Attribute)) and decorator.as_string() == "app.cell":
                    return True
            return False
        except AttributeError:
            return False

    # @pysnooper.snoop(output='/Users/malcolm/dev/bossjones/prompt-library/pylint-debug.log', thread_info=True, max_variable_length=None, depth=10)
    def visit_functiondef(self, node: nodes.FunctionDef | nodes.AsyncFunctionDef) -> None:
        """Visit and check a function definition node.

        Args:
            node: The function definition node to visit.
        """

        if not self._is_marimo_notebook():
            return

        if not self._has_app_cell_decorator(node):
            return

        # import bpdb
        # bpdb.set_trace()

        # Reset state for new cell
        self._used_names = set()
        self._current_cell_params = set()

        # Collect parameter names
        for arg in node.args.args:
            self._current_cell_params.add(arg.name)

        # Walk the function body to collect used names
        for child in node.body:
            child.accept(self)

        # Check for unused parameters immediately
        for param in self._current_cell_params:
            if param not in self._used_names:
                self.add_message(
                    "unused-cell-parameter",
                    node=node,
                    args=(param,),
                )

    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        """Leave a function definition node and check for unused parameters.

        Args:
            node: The function definition node to leave.
        """
        if not self._is_marimo_notebook():
            return

        if not self._has_app_cell_decorator(node):
            return

        # Check for unused parameters
        for param in self._current_cell_params:
            if param not in self._used_names:
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
        if isinstance(node, nodes.Name):
            ctx_name = getattr(node.ctx, "name", "")
            if ctx_name == "Load":
                self._used_names.add(node.name)


def register(linter: PyLinter) -> None:
    """Register the MarimoCellParamsChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoCellParamsChecker(linter))
