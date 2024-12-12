"""Pylint plugin for checking Marimo state management standards.

This module provides a custom pylint checker for enforcing Marimo state management standards.
It ensures proper state handling, prevents mutations, and validates typing.
"""

from __future__ import annotations

from typing import Any, Optional, cast

from astroid import nodes
from astroid.nodes import Assign, AssignAttr, AssignName, Attribute, Call, Name, NodeNG

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class MarimoStateChecker(BaseChecker):
    """Checker for enforcing Marimo state management standards.

    This checker ensures that:
    1. No direct mutations of shared state between cells
    2. All state changes happen through reactive updates
    3. State variables have proper typing annotations
    4. No global state modifications

    Attributes:
        name: The name of the checker
        priority: The priority level of the checker
        msgs: Dictionary of warning messages and their descriptions
    """

    name = "marimo-state"
    priority = -1
    msgs = {
        "W9201": (
            "Direct state mutation detected",
            "direct-state-mutation",
            "Avoid directly mutating state in marimo notebooks. "
            "Use reactive patterns and cell dependencies instead.",
        ),
        "W9202": (
            "Missing type annotation for state variable",
            "missing-state-type",
            "All state variables in marimo notebooks should have type annotations. "
            "Add proper typing to the variable.",
        ),
        "W9203": (
            "Shared state modification",
            "shared-state-modification",
            "Avoid modifying shared state between cells. "
            "Use cell parameters and return values instead.",
        ),
        "W9204": (
            "Global variable usage",
            "global-variable-usage",
            "Avoid using global variables in marimo notebooks. "
            "Use cell parameters for dependencies.",
        ),
    }

    def __init__(self, linter: PyLinter) -> None:
        """Initialize the checker.

        Args:
            linter: The pylint linter instance
        """
        super().__init__(linter)
        self._current_cell_name: Optional[str] = None

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
                if isinstance(decorator, Name) and decorator.name == "app.cell":
                    return True
                if isinstance(decorator, Attribute):
                    if decorator.as_string() == "app.cell":
                        return True
            return False
        except AttributeError:
            return False

    def visit_assign(self, node: nodes.Assign) -> None:
        """Visit and check assignment nodes.

        Args:
            node: The assignment node to check
        """
        if not self._is_marimo_notebook():
            return

        # Check for direct state mutations
        if isinstance(node.targets[0], (AssignAttr, AssignName)):
            target = node.targets[0]
            if isinstance(target, AssignAttr):
                if isinstance(target.expr, Name):
                    self.add_message("direct-state-mutation", node=node)
            elif isinstance(target, AssignName):
                if target.name in self.linter.config.additional_builtins:
                    self.add_message("global-variable-usage", node=node)

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Visit and check function definition nodes.

        Args:
            node: The function definition node to check
        """
        if not self._is_marimo_notebook():
            return

        if self._has_app_cell_decorator(node):
            self._current_cell_name = node.name

            # Check for missing type annotations in parameters
            for arg in node.args.args:
                if arg.annotation is None and arg.name != "self":
                    self.add_message("missing-state-type", node=arg)

    def visit_global(self, node: nodes.Global) -> None:
        """Visit and check global statement nodes.

        Args:
            node: The global statement node to check
        """
        if not self._is_marimo_notebook():
            return

        self.add_message("shared-state-modification", node=node)


def register(linter: PyLinter) -> None:
    """Register the MarimoStateChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoStateChecker(linter))
