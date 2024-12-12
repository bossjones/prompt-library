# """Tests for Marimo cell validator pylint plugin."""

# # pyright: reportAttributeAccessIssue=false
# from __future__ import annotations

# import astroid

# from astroid.builder import parse as astroid_parse
# from astroid.nodes import Module

# import pytest

# from pylint.checkers import BaseChecker
# from pylint.interfaces import UNDEFINED
# from pylint.testutils import MessageTest
# from pylint.testutils.unittest_linter import UnittestLinter
# from pylint.utils.ast_walker import ASTWalker

# from . import assert_adds_messages, assert_no_messages


# def test_valid_marimo_cell(linter: UnittestLinter, marimo_checker: BaseChecker) -> None:
#     """Test valid Marimo cell with proper @app.cell decorator and naming."""
#     code = """
#     import marimo as mo
#     app = mo.App()

#     @app.cell
#     def __cell1():
#         return "Hello, World!"
#     """

#     root_node: astroid.Module = astroid_parse(code, "marimo_test.py")
#     walker = ASTWalker(linter)
#     walker.add_checker(marimo_checker)

#     with assert_no_messages(linter):
#         walker.walk(root_node)


# def test_missing_cell_decorator(linter: UnittestLinter, marimo_checker: BaseChecker) -> None:
#     """Test error when @app.cell decorator is missing."""
#     code = """
#     import marimo as mo
#     app = mo.App()

#     def __cell1():
#         return "Hello, World!"
#     """

#     root_node: astroid.Module = astroid_parse(code, "marimo_test.py")
#     walker = ASTWalker(linter)
#     walker.add_checker(marimo_checker)

#     # Register the message with the linter
#     linter.add_message(marimo_checker.msgs["W9001"].msgid)

#     with assert_adds_messages(
#         linter,
#         MessageTest(
#             msg_id="missing-app-cell-decorator",
#             line=5,
#             node=root_node.body[2],
#             args=None,
#             confidence=UNDEFINED,
#             col_offset=0,
#             end_line=5,
#             end_col_offset=13,
#         ),
#     ):
#         walker.walk(root_node)


# def test_invalid_cell_name(linter: UnittestLinter, marimo_checker: BaseChecker) -> None:
#     """Test error when cell function name doesn't start with __."""
#     code = """
#     import marimo as mo
#     app = mo.App()

#     @app.cell
#     def cell1():
#         return "Hello, World!"
#     """

#     root_node: astroid.Module = astroid_parse(code, "marimo_test.py")
#     walker = ASTWalker(linter)
#     walker.add_checker(marimo_checker)

#     # Register the message with the linter
#     linter.add_message(marimo_checker.msgs["W9003"].msgid)

#     with assert_adds_messages(
#         linter,
#         MessageTest(
#             msg_id="invalid-cell-name",
#             line=6,
#             node=root_node.body[2],
#             args=None,
#             confidence=UNDEFINED,
#             col_offset=0,
#             end_line=6,
#             end_col_offset=13,
#         ),
#     ):
#         walker.walk(root_node)


# def test_nested_function_definition(linter: UnittestLinter, marimo_checker: BaseChecker) -> None:
#     """Test error when cell contains nested function definitions."""
#     code = """
#     import marimo as mo
#     app = mo.App()

#     @app.cell
#     def __cell1():
#         def helper():
#             return "Helper"
#         return helper()
#     """

#     root_node: astroid.Module = astroid_parse(code, "marimo_test.py")
#     walker = ASTWalker(linter)
#     walker.add_checker(marimo_checker)

#     # Register the message with the linter
#     linter.add_message(marimo_checker.msgs["W9002"].msgid)

#     with assert_adds_messages(
#         linter,
#         MessageTest(
#             msg_id="function-in-cell",
#             line=7,
#             node=root_node.body[2].body[0],
#             args=None,
#             confidence=UNDEFINED,
#             col_offset=4,
#             end_line=7,
#             end_col_offset=17,
#         ),
#     ):
#         walker.walk(root_node)


# @pytest.mark.parametrize(
#     ("code", "filename"),
#     [
#         (
#             """
#             def regular_function():
#                 return "Not a Marimo cell"
#             """,
#             "regular_module.py",
#         ),
#         (
#             """
#             def __looks_like_cell():
#                 return "Not in a Marimo file"
#             """,
#             "not_marimo.py",
#         ),
#     ],
# )
# def test_non_marimo_files(linter: UnittestLinter, marimo_checker: BaseChecker, code: str, filename: str) -> None:
#     """Test that non-Marimo files are not affected by the validator."""
#     root_node: astroid.Module = astroid_parse(code, filename)
#     walker = ASTWalker(linter)
#     walker.add_checker(marimo_checker)

#     with assert_no_messages(linter):
#         walker.walk(root_node)


# def test_async_cell_function(linter: UnittestLinter, marimo_checker: BaseChecker) -> None:
#     """Test that async cell functions are properly validated."""
#     code = """
#     import marimo as mo
#     app = mo.App()

#     @app.cell
#     async def __async_cell():
#         return "Async cell"
#     """

#     root_node: astroid.Module = astroid_parse(code, "marimo_test.py")
#     walker = ASTWalker(linter)
#     walker.add_checker(marimo_checker)

#     with assert_no_messages(linter):
#         walker.walk(root_node)


# def test_multiple_decorators(linter: UnittestLinter, marimo_checker: BaseChecker) -> None:
#     """Test cell with multiple decorators including @app.cell."""
#     code = """
#     import marimo as mo
#     app = mo.App()

#     def some_decorator(func):
#         return func

#     @some_decorator
#     @app.cell
#     def __cell1():
#         return "Multiple decorators"
#     """

#     root_node: astroid.Module = astroid_parse(code, "marimo_test.py")
#     walker = ASTWalker(linter)
#     walker.add_checker(marimo_checker)

#     with assert_no_messages(linter):
#         walker.walk(root_node)
