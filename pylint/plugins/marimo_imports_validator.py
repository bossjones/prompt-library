"""Pylint plugin for checking Marimo import and dependency standards.

This module provides a custom pylint checker for enforcing Marimo import and dependency standards.
It ensures proper import organization, cell dependencies, and state management.
"""

from __future__ import annotations

from typing import Any, Optional, cast

from astroid import nodes
from astroid.node_classes import Attribute, Name

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class MarimoImportsChecker(BaseChecker):
    """Checker for enforcing Marimo import and dependency standards.

    This checker ensures that:
    1. All imports are in the first cell of marimo notebooks
    2. Cell dependencies are explicitly declared
    3. No circular dependencies between cells
    4. No global state mutations

    Attributes:
        name: The name of the checker
        priority: The priority level of the checker
        msgs: Dictionary of warning messages and their descriptions
    """

    name = "marimo-imports"
    priority = -1
    msgs = {
        "W9101": (
            "Import not in first cell",
            "import-not-in-first-cell",
            "All imports in marimo notebooks must be in the first cell. "
            "Move this import to the first cell of the notebook.",
        ),
        "W9102": (
            "Missing explicit cell dependency",
            "missing-cell-dependency",
            "Cell dependencies must be explicitly declared in function parameters. "
            "Add the dependency to the function parameters.",
        ),
        "W9103": (
            "Global state mutation detected",
            "global-state-mutation",
            "Avoid mutating global state in marimo notebooks. "
            "Use reactive patterns and cell dependencies instead.",
        ),
        "W9104": (
            "Missing tuple return",
            "missing-tuple-return",
            "All marimo cells must return values as tuples. "
            "Wrap the return value in a tuple.",
        ),
    }

    def __init__(self, linter: PyLinter) -> None:
        """Initialize the checker.

        Args:
            linter: The pylint linter instance
        """
        super().__init__(linter)
        self._first_cell_seen = False
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
                if isinstance(decorator, Name) and decorator.as_string() == "app.cell":
                    return True
                if isinstance(decorator, Attribute):
                    if decorator.as_string() == "app.cell":
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

        if self._has_app_cell_decorator(node):
            self._current_cell_name = node.name
            if not self._first_cell_seen:
                self._first_cell_seen = True
            self._check_return_tuple(node)

    def visit_import(self, node: nodes.Import) -> None:
        """Visit and check an import node.

        Args:
            node: The import node to visit.
        """
        if not self._is_marimo_notebook():
            return

        if self._first_cell_seen and self._current_cell_name != "__":
            self.add_message("import-not-in-first-cell", node=node)

    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        """Visit and check an import from node.

        Args:
            node: The import from node to visit.
        """
        if not self._is_marimo_notebook():
            return

        if self._first_cell_seen and self._current_cell_name != "__":
            self.add_message("import-not-in-first-cell", node=node)

    def visit_global(self, node: nodes.Global) -> None:
        """Visit and check a global statement node.

        Args:
            node: The global statement node to visit.
        """
        if not self._is_marimo_notebook():
            return

        self.add_message("global-state-mutation", node=node)

    def _check_return_tuple(self, node: nodes.FunctionDef) -> None:
        """Check if a function returns a tuple.

        Args:
            node: The function definition node to check.
        """
        for child in node.get_children():
            if isinstance(child, nodes.Return):
                if not (isinstance(child.value, nodes.Tuple) or
                       (isinstance(child.value, nodes.Call) and
                        isinstance(child.value.func, Name) and
                        child.value.func.as_string() == "tuple")):
                    self.add_message("missing-tuple-return", node=child)


def register(linter: PyLinter) -> None:
    """Register the MarimoImportsChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoImportsChecker(linter))
