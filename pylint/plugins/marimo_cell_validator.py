"""Pylint plugin for checking Marimo notebook standards.

This module provides a custom pylint checker for enforcing Marimo notebook coding standards.
It ensures proper cell decoration, function naming, and prevents nested function definitions.
"""

from __future__ import annotations

from typing import Any, Optional, cast

from astroid import nodes

from pylint.checkers import BaseChecker

# from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter


class MarimoChecker(BaseChecker):
    """Checker for enforcing Marimo notebook coding standards.

    This checker ensures that:
    1. All cells in marimo notebooks are decorated with @app.cell
    2. No function definitions are allowed in marimo notebook cells
    3. All cell functions are named with double underscores

    Attributes:
        name: The name of the checker
        priority: The priority level of the checker
        msgs: Dictionary of warning messages and their descriptions
    """

    # __implements__ = IAstroidChecker

    name = "marimo"
    priority = -1
    msgs = {
        "W9001": (
            "Cell not decorated with @app.cell",
            "missing-app-cell-decorator",
            "All cells in marimo notebooks must be decorated with @app.cell. "
            "Add the @app.cell decorator to make this a valid marimo cell.",
        ),
        "W9002": (
            "Function definition in marimo notebook cell",
            "function-in-cell",
            "No function definitions allowed in marimo notebook cells. "
            "Move function definitions to a separate module and import them.",
        ),
        "W9003": (
            "Invalid cell function name",
            "invalid-cell-name",
            "All cell functions in marimo notebooks must start with '__'. "
            "Rename the function to start with double underscores.",
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
                if isinstance(decorator, nodes.Name) and decorator.name == "app.cell":
                    return True
                if isinstance(decorator, nodes.Attribute):
                    if decorator.as_string() == "app.cell":
                        return True
            return False
        except AttributeError:
            return False

    def _check_marimo_cell(self, node: nodes.FunctionDef | nodes.AsyncFunctionDef) -> None:
        """Check if a function definition follows marimo cell standards.

        This method checks for:
        1. Presence of @app.cell decorator
        2. No nested function definitions
        3. Proper cell function naming

        Args:
            node: The function definition node to check.
        """
        if not self._is_marimo_notebook():
            return

        if not self._has_app_cell_decorator(node):
            self.add_message("missing-app-cell-decorator", node=node)

        if not node.name.startswith("__"):
            self.add_message("invalid-cell-name", node=node)

        # Check for nested function definitions
        for child in node.get_children():
            if isinstance(child, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
                self.add_message("function-in-cell", node=child)

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Visit and check a function definition node.

        Args:
            node: The function definition node to visit.
        """
        self._check_marimo_cell(node)

    def visit_asyncfunctiondef(self, node: nodes.AsyncFunctionDef) -> None:
        """Visit and check an async function definition node.

        Args:
            node: The async function definition node to visit.
        """
        self._check_marimo_cell(node)


def register(linter: PyLinter) -> None:
    """Register the MarimoChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoChecker(linter))
