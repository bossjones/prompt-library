"""Pylint plugin for checking Marimo notebook import standards.

This module provides a custom pylint checker for enforcing Marimo notebook import standards.
It ensures imports are in the first cell, properly reloaded, and returned as tuples.
"""

from __future__ import annotations

from typing import Any, Optional, cast

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class MarimoCellImportsChecker(BaseChecker):
    """Checker for enforcing Marimo import standards.

    This checker ensures that:
    1. All imports are in the first cell of marimo notebooks
    2. Development modules use importlib.reload()
    3. All imports are returned as tuples
    4. No imports outside the first cell

    Attributes:
        name: The name of the checker
        priority: The priority level of the checker
        msgs: Dictionary of warning messages and their descriptions
    """

    name = "marimo-imports"
    priority = -1
    msgs = {
        "W9101": (
            "Import statement outside first cell",
            "import-not-in-first-cell",
            "All imports in marimo notebooks must be in the first cell. "
            "Move this import to the first cell.",
        ),
        "W9102": (
            "Missing importlib.reload() for development module",
            "missing-importlib-reload",
            "Development modules should be reloaded using importlib.reload(). "
            "Add importlib.reload() call for this module.",
        ),
        "W9103": (
            "Imports not returned as tuple",
            "imports-not-in-tuple",
            "All imports must be returned as a tuple. "
            "Return all imported modules in a tuple.",
        ),
    }

    def __init__(self, linter: Optional[PyLinter] = None) -> None:
        """Initialize the checker.

        Args:
            linter: The pylint linter instance
        """
        super().__init__(linter)
        self._first_cell_found = False
        self._in_first_cell = False
        self._has_importlib = False
        self._dev_modules = set()

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

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Visit and check a function definition node.

        Args:
            node: The function definition node to visit.
        """
        if not self._is_marimo_notebook():
            return

        if self._has_app_cell_decorator(node):
            if not self._first_cell_found:
                self._first_cell_found = True
                self._in_first_cell = True
            else:
                self._in_first_cell = False

    def visit_import(self, node: nodes.Import) -> None:
        """Visit and check an import node.

        Args:
            node: The import node to visit.
        """
        if not self._is_marimo_notebook():
            return

        if not self._in_first_cell:
            self.add_message("import-not-in-first-cell", node=node)

        if any(name[0].startswith("prompt_library") for name in node.names):
            self._dev_modules.add(node)

        if any(name[0] == "importlib" for name in node.names):
            self._has_importlib = True

    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        """Visit and check an import from node.

        Args:
            node: The import from node to visit.
        """
        if not self._is_marimo_notebook():
            return

        if not self._in_first_cell:
            self.add_message("import-not-in-first-cell", node=node)

        if node.modname.startswith("prompt_library"):
            self._dev_modules.add(node)

    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        """Check function definition when leaving the node.

        Args:
            node: The function definition node being left.
        """
        if not self._is_marimo_notebook() or not self._has_app_cell_decorator(node):
            return

        if self._in_first_cell:
            # Check for importlib.reload() usage
            if self._dev_modules and not self._has_importlib:
                self.add_message("missing-importlib-reload", node=node)

            # Check return value is a tuple
            returns = node.returns if hasattr(node, "returns") else None
            if not returns or not isinstance(returns, nodes.Tuple):
                self.add_message("imports-not-in-tuple", node=node)


def register(linter: PyLinter) -> None:
    """Register the MarimoCellImportsChecker with pylint.

    Args:
        linter: The pylint linter instance to register the checker with.
    """
    linter.register_checker(MarimoCellImportsChecker(linter))
