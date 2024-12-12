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
    from _pytest.fixtures import FixtureRequest
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


def test_used_cell_parameter(
    linter: UnittestLinter, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture
) -> None:
    """Test that used cell parameters are not flagged."""
    code = """
    @app.cell
    def __():
        import os
        return (os,)

    @app.cell
    def __(os):  # os is used, should not trigger warning
        result = os.path.join("/tmp")
        return (result,)
    """
    root_node: astroid.Module = astroid.parse(code, "marimo_test.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)
    mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=True)

    with assert_no_messages(linter):
        walker.walk(root_node)


@pytest.mark.parametrize(
    ("code", "param_name"),
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
        ),
    ],
)
def test_unused_cell_parameter(
    linter: UnittestLinter,
    marimo_cell_params_checker: BaseChecker,
    mocker: MockerFixture,
    code: str,
    param_name: str,
) -> None:
    """Test that unused cell parameters are detected."""
    root_node: astroid.Module = astroid.parse(code, "marimo_test.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)
    mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=True)

    with assert_adds_messages(
        linter,
        MessageTest(
            msg_id="unused-cell-parameter",
            line=8,
            node=root_node.body[2],
            args=(param_name,),
            confidence=UNDEFINED,
            col_offset=0,
            end_line=8,
            end_col_offset=13,
        ),
    ):
        walker.walk(root_node)


def test_non_cell_function(
    linter: UnittestLinter, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture
) -> None:
    """Test that non-cell functions are ignored."""
    code = """
    def regular_function(unused_param):  # Should not trigger warning
        return 42
    """
    root_node: astroid.Module = astroid.parse(code, "marimo_test.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)
    mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=True)

    with assert_no_messages(linter):
        walker.walk(root_node)


def test_non_marimo_file(
    linter: UnittestLinter, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture
) -> None:
    """Test that non-marimo files are ignored."""
    code = """
    @app.cell
    def __(unused_param):  # Should not trigger warning in non-marimo file
        return (42,)
    """
    root_node: astroid.Module = astroid.parse(code, "regular_file.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)
    mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=False)

    with assert_no_messages(linter):
        walker.walk(root_node)
