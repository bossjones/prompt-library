"""Tests for the Marimo cell parameters validator."""

from __future__ import annotations

import logging

from types import ModuleType

import astroid
import pysnooper

from _pytest.logging import LogCaptureFixture
from astroid.builder import parse as astroid_parse
from astroid.nodes import Module
from loguru import logger

import pytest

from pylint.checkers import BaseChecker
from pylint.interfaces import UNDEFINED
from pylint.testutils import MessageTest
from pylint.testutils.unittest_linter import UnittestLinter
from pylint.utils.ast_walker import ASTWalker

from . import assert_adds_messages, assert_no_messages


def test_good_cell_params(linter: UnittestLinter, marimo_cell_params_checker: ModuleType) -> None:
    """Test that properly used cell parameters are not flagged.

    Args:
        linter: The pylint linter instance
        marimo_cell_params_checker: The cell parameter checker
    """
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
    root_node = astroid_parse(code, "marimo_test.py")
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)


# @pysnooper.snoop(thread_info=True, max_variable_length=None, depth=10)
@pytest.mark.parametrize(
    ("code", "param_name", "line_num", "path"),
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
            "marimo_test.py",
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
            "marimo_test.py",
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
            "marimo_test.py",
        ),
        (
            """
            @app.cell
            def __():
                import numpy as np
                return (np,)

            @app.cell
            def __(np, unused_config):
                arr = np.array([1, 2, 3])
                return (arr,)
            """,
            "unused_config",
            8,
            "marimo_notebook.py",
        ),
    ],
)
def test_bad_cell_params(
    linter: UnittestLinter,
    marimo_cell_params_checker: ModuleType,
    code: str,
    param_name: str,
    line_num: int,
    path: str,
    caplog: LogCaptureFixture,
) -> None:
    """Test that unused cell parameters are properly detected and reported.

    Args:
        linter: The pylint linter instance
        marimo_cell_params_checker: The cell parameter checker
        code: The test code to analyze
        param_name: The name of the parameter expected to be flagged
        line_num: The line number where the error should be reported
        path: The file path to use for the test
    """
    caplog.set_level(logging.DEBUG)
    logger.info(f"Running test_bad_cell_params with code: {code}")
    logger.info(f"Path: {path}")
    logger.info(f"Line num: {line_num}")
    logger.info(f"Param name: {param_name}")

    # import bpdb
    # bpdb.set_trace()

    root_node: Module = astroid_parse(code, path)
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_adds_messages(
        linter,
        MessageTest(
            msg_id="unused-cell-parameter",
            line=line_num,
            node=next(
                node
                for node in root_node.body
                if isinstance(node, astroid.nodes.FunctionDef)
                and node.name == "__"
                and any(
                    isinstance(dec, (astroid.nodes.Name, astroid.nodes.Attribute)) and dec.as_string() == "app.cell"
                    for dec in node.decorators.nodes
                )
            ),
            args=(param_name,),
            confidence=UNDEFINED,
            col_offset=0,
            end_line=line_num,
            end_col_offset=13,
        ),
    ):
        walker.walk(root_node)


@pytest.mark.parametrize(
    ("code", "path"),
    [
        (
            """
            def regular_function(unused_param):
                return 42
            """,
            "marimo_test.py",
        ),
        (
            """
            class TestClass:
                def method(self, unused_param):
                    pass
            """,
            "marimo_test.py",
        ),
        (
            """
            @some_other_decorator
            def decorated_func(unused_param):
                return True
            """,
            "marimo_test.py",
        ),
        (
            """
            def __init__(self, unused_param):
                pass
            """,
            "marimo_test.py",
        ),
    ],
)
def test_non_cell_functions(
    linter: UnittestLinter,
    marimo_cell_params_checker: ModuleType,
    code: str,
    path: str,
) -> None:
    """Test that non-cell functions are properly ignored.

    Args:
        linter: The pylint linter instance
        marimo_cell_params_checker: The cell parameter checker
        code: The test code to analyze
        path: The file path to use for the test
    """
    root_node = astroid_parse(code, path)
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)


@pytest.mark.parametrize(
    ("code", "path"),
    [
        (
            """
            @app.cell
            def __(unused_param):
                return (42,)
            """,
            "regular_file.py",
        ),
        (
            """
            @app.cell
            def __(x, y, unused):
                return (x + y,)
            """,
            "not_marimo.py",
        ),
        (
            """
            @app.cell
            def __(data, config):
                # Config is used in a string context
                print(f"Using config: {config}")
                return (data,)
            """,
            "marimo_test.py",
        ),
    ],
)
def test_non_marimo_files_and_special_cases(
    linter: UnittestLinter,
    marimo_cell_params_checker: ModuleType,
    code: str,
    path: str,
) -> None:
    """Test that non-marimo files and special parameter cases are properly handled.

    Args:
        linter: The pylint linter instance
        marimo_cell_params_checker: The cell parameter checker
        code: The test code to analyze
        path: The file path to use for the test
    """
    root_node = astroid_parse(code, path)
    walker = ASTWalker(linter)
    walker.add_checker(marimo_cell_params_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)
