"""Tests for the Marimo cell parameters validator."""

# pyright: reportAttributeAccessIssue=false
from __future__ import annotations

from typing import TYPE_CHECKING

import astroid

import pytest

from pylint.checkers import BaseChecker
from pylint.interfaces import UNDEFINED
from pylint.testutils import MessageTest
from pylint.testutils.unittest_linter import UnittestLinter
from pylint.utils.ast_walker import ASTWalker

from . import assert_adds_messages, assert_no_messages


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


def test_good_cell_params(linter: UnittestLinter, marimo_cell_params_checker: BaseChecker) -> None:
    """Test that properly used cell parameters are not flagged."""
    code = """
    @app.cell
    def __():
        import os, sys
        return (os, sys)

    @app.cell
    def __(os, sys):
        result = os.path.join(sys.path[0])
        return (result,)
    """
    root_node: astroid.Module = astroid.parse(code, "marimo_test.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)


@pytest.mark.parametrize(
    ("code", "param_name", "line_num"),
    [
        (
            """
            @app.cell
            def __():
                import os
                return (os,)

            @app.cell
            def __(os, unused_param):
                result = os.path.join("/tmp")
                return (result,)
            """,
            "unused_param",
            8,
        ),
        (
            """
            @app.cell
            def __():
                import os, sys
                return (os, sys)

            @app.cell
            def __(os, unused1, sys, unused2):
                result = os.path.join(sys.path[0])
                return (result,)
            """,
            "unused1",
            8,
        ),
        (
            """
            @app.cell
            def __():
                import pandas as pd
                return (pd,)

            @app.cell
            def __(pd, extra):
                df = pd.DataFrame()
                return (df,)
            """,
            "extra",
            8,
        ),
    ],
)
def test_bad_cell_params(
    linter: UnittestLinter,
    marimo_cell_params_checker: BaseChecker,
    code: str,
    param_name: str,
    line_num: int,
) -> None:
    """Test that unused cell parameters are properly detected and reported.

    Args:
        linter: The pylint linter instance
        marimo_cell_params_checker: The cell parameter checker
        code: The test code to analyze
        param_name: The name of the parameter expected to be flagged
        line_num: The line number where the error should be reported
    """
    root_node: astroid.Module = astroid.parse(code, "marimo_test.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_adds_messages(
        linter,
        MessageTest(
            msg_id="unused-cell-parameter",
            line=line_num,
            node=root_node.body[2],
            args=(param_name,),
            confidence=UNDEFINED,
            col_offset=0,
            end_line=line_num,
            end_col_offset=13,
        ),
    ):
        walker.walk(root_node)


@pytest.mark.parametrize(
    "code",
    [
        """
        def regular_function(unused_param):
            return 42
        """,
        """
        class TestClass:
            def method(self, unused_param):
                pass
        """,
        """
        @some_other_decorator
        def decorated_func(unused_param):
            return True
        """,
    ],
)
def test_non_cell_functions(linter: UnittestLinter, marimo_cell_params_checker: BaseChecker, code: str) -> None:
    """Test that non-cell functions are properly ignored.

    Args:
        linter: The pylint linter instance
        marimo_cell_params_checker: The cell parameter checker
        code: The test code to analyze
    """
    root_node = astroid.parse(code, "marimo_test.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)


@pytest.mark.parametrize(
    ("filename", "code"),
    [
        (
            "regular_file.py",
            """
            @app.cell
            def __(unused_param):
                return (42,)
            """,
        ),
        (
            "not_marimo.py",
            """
            @app.cell
            def __(x, y, unused):
                return (x + y,)
            """,
        ),
    ],
)
def test_non_marimo_files(
    linter: UnittestLinter,
    marimo_cell_params_checker: BaseChecker,
    filename: str,
    code: str,
) -> None:
    """Test that non-marimo files are properly ignored.

    Args:
        linter: The pylint linter instance
        marimo_cell_params_checker: The cell parameter checker
        filename: The name of the file being tested
        code: The test code to analyze
    """
    root_node = astroid.parse(code, filename)
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)
