"""Pylint plugin for checking Marimo cell parameter usage.

This module provides a custom pylint checker for enforcing Marimo cell parameter standards.
It ensures that cell parameters are actually used within the cell.
"""

# pyright: reportAttributeAccessIssue=false
from __future__ import annotations

from typing import Any, Set, cast

import astroid

from astroid import nodes
from astroid.nodes import AssignName, Attribute, Name, NodeNG

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class MarimoCellParamsChecker(BaseChecker):
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

    name = "marimo-cell-params"
    priority = -1
    msgs = {
        "W9301": (
            "Unused cell parameter '%s'",
            "unused-cell-parameter",
            "Cell parameters should only include variables that are actually used in the cell. "
            "Remove unused parameters.",
        ),
    }

    def __init__(self, linter: PyLinter | None = None) -> None:
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
                if isinstance(decorator, (Name, Attribute)) and decorator.as_string() == "app.cell":
                    return True
            return False
        except AttributeError:
            return False

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Visit and check a function definition node.

        Args:
            node: The function definition node to visit.
        """
        if not self._is_marimo_notebook():
            return

        if not self._has_app_cell_decorator(node):
            return

        # Reset state for new cell
        self._used_names.clear()
        self._current_cell_params.clear()

        # Collect parameter names
        for arg in node.args.args:
            if isinstance(arg, AssignName):
                self._current_cell_params.add(arg.name)

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

        # Only track name usage in load context (when variable is used)
        if isinstance(node, nodes.Name) and getattr(node.ctx, "name", "") == "Load":
            self._used_names.add(node.name)


def register(linter: PyLinter) -> None:
    """Register the MarimoCellParamsChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoCellParamsChecker(linter))
