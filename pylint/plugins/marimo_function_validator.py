"""Pylint plugin for checking Marimo function definition standards.

This module provides a custom pylint checker for enforcing Marimo function definition standards.
It ensures that no functions are defined in marimo notebook files, as they should be imported from modules.
"""

from __future__ import annotations

from typing import Any, Sequence, cast

import astroid

from astroid import nodes
from astroid.nodes import AsyncFunctionDef, Attribute, Decorators, FunctionDef, Lambda, Name, NodeNG

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class MarimoFunctionChecker(BaseChecker):
    """Checker for enforcing Marimo function definition standards.

    This checker ensures that:
    1. No function definitions in marimo notebook files
    2. Functions should be imported from separate modules
    3. Only cell definitions with @app.cell decorator are allowed

    Attributes:
        name (str): The name of the checker
        priority (int): The priority level of the checker (-1 for normal)
        msgs (dict): Dictionary of warning messages and their descriptions
        linter (PyLinter): The pylint linter instance
    """

    name = "marimo-functions"
    priority = -1
    msgs = {
        "W9201": (
            "Function definition in marimo notebook file",
            "function-in-notebook",
            "No function definitions allowed in marimo notebook files. "
            "Move function definitions to a separate module and import them.",
        ),
        "W9202": (
            "Lambda function in marimo notebook file",
            "lambda-in-notebook",
            "No lambda function definitions allowed in marimo notebook files. "
            "Move lambda functions to a separate module and import them.",
        ),
        "W9203": (
            "Async function definition in marimo notebook file",
            "async-function-in-notebook",
            "No async function definitions allowed in marimo notebook files. "
            "Move async function definitions to a separate module and import them.",
        ),
    }

    def _is_marimo_notebook(self) -> bool:
        """Check if the current file is a marimo notebook.

        Returns:
            bool: True if the file is a marimo notebook (starts with 'marimo_'),
                 False otherwise.
        """
        try:
            current_file = cast(Any, self.linter.current_file)
            return current_file.name.startswith("marimo_")
        except AttributeError:
            return False

    def _has_app_cell_decorator(self, node: FunctionDef | AsyncFunctionDef) -> bool:
        """Check if a function has the @app.cell decorator.

        Args:
            node: The function definition node to check.

        Returns:
            bool: True if the function has the @app.cell decorator, False otherwise.
        """
        try:
            if not hasattr(node, "decorators") or not node.decorators:
                return False

            decorators: Decorators = node.decorators
            decorator_nodes: Sequence[NodeNG] = getattr(decorators, "nodes", [])

            for decorator in decorator_nodes:
                if isinstance(decorator, (Name, Attribute)) and decorator.as_string() == "app.cell":
                    return True
            return False
        except AttributeError:
            return False

    def visit_functiondef(self, node: FunctionDef) -> None:
        """Visit and check a function definition node.

        Args:
            node: The function definition node to visit.
        """
        if not self._is_marimo_notebook():
            return

        # Allow cell definitions with @app.cell decorator
        if self._has_app_cell_decorator(node):
            return

        # Disallow all other function definitions
        self.add_message("function-in-notebook", node=node)

    def visit_asyncfunctiondef(self, node: AsyncFunctionDef) -> None:
        """Visit and check an async function definition node.

        Args:
            node: The async function definition node to visit.
        """
        if not self._is_marimo_notebook():
            return

        # Allow cell definitions with @app.cell decorator
        if self._has_app_cell_decorator(node):
            return

        # Disallow all other async function definitions
        self.add_message("async-function-in-notebook", node=node)

    def visit_lambda(self, node: Lambda) -> None:
        """Visit and check a lambda function node.

        Args:
            node: The lambda function node to visit.
        """
        if not self._is_marimo_notebook():
            return

        # Disallow all lambda functions
        self.add_message("lambda-in-notebook", node=node)


def register(linter: PyLinter) -> None:
    """Register the MarimoFunctionChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoFunctionChecker(linter))
