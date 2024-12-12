"""Tests for the Marimo function validator."""

# pyright: reportAttributeAccessIssue=false
from __future__ import annotations

from typing import TYPE_CHECKING

import astroid

from astroid.builder import parse as astroid_parse

import pytest

from pylint.checkers import BaseChecker
from pylint.testutils import CheckerTestCase, MessageTest


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


@pytest.mark.pylint
class TestMarimoFunctionChecker(CheckerTestCase):
    """Test class for the MarimoFunctionChecker."""

    @pytest.mark.usefixtures("marimo_function_checker")
    def test_regular_function_in_notebook(self, marimo_function_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that regular function definitions in notebooks are detected.

        Args:
            marimo_function_checker: The Marimo function checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            import os
            return (os,)

        def helper_function():  # This should trigger a warning
            return "helper"

        @app.cell
        def __(os):
            result = helper_function()
            return (result,)
        """
        module: astroid.Module = astroid_parse(code)
        mocker.patch.object(marimo_function_checker, "_is_marimo_notebook", return_value=True)
        marimo_function_checker.visit(module)

        messages = marimo_function_checker.linter.release_messages()
        assert any(msg.msg_id == "function-in-notebook" for msg in messages), "Expected function-in-notebook message"

    @pytest.mark.usefixtures("marimo_function_checker")
    def test_lambda_function_in_notebook(self, marimo_function_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that lambda function definitions in notebooks are detected.

        Args:
            marimo_function_checker: The Marimo function checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            # This should trigger a warning
            square = lambda x: x * x
            return (square(5),)
        """
        module: astroid.Module = astroid_parse(code)
        mocker.patch.object(marimo_function_checker, "_is_marimo_notebook", return_value=True)
        marimo_function_checker.visit(module)

        messages = marimo_function_checker.linter.release_messages()
        assert any(msg.msg_id == "lambda-in-notebook" for msg in messages), "Expected lambda-in-notebook message"

    @pytest.mark.usefixtures("marimo_function_checker")
    def test_async_function_in_notebook(self, marimo_function_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that async function definitions in notebooks are detected.

        Args:
            marimo_function_checker: The Marimo function checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            import aiohttp
            return (aiohttp,)

        async def fetch_data():  # This should trigger a warning
            return "data"

        @app.cell
        def __(aiohttp):
            result = await fetch_data()
            return (result,)
        """
        module: astroid.Module = astroid_parse(code)
        mocker.patch.object(marimo_function_checker, "_is_marimo_notebook", return_value=True)
        marimo_function_checker.visit(module)

        messages = marimo_function_checker.linter.release_messages()
        assert any(msg.msg_id == "async-function-in-notebook" for msg in messages), (
            "Expected async-function-in-notebook message"
        )

    @pytest.mark.usefixtures("marimo_function_checker")
    def test_valid_marimo_notebook(self, marimo_function_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that valid marimo notebook code passes all checks.

        Args:
            marimo_function_checker: The Marimo function checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            from my_module import helper_function
            return (helper_function,)

        @app.cell
        def __(helper_function):
            result = helper_function()
            return (result,)
        """
        module: astroid.Module = astroid_parse(code)
        mocker.patch.object(marimo_function_checker, "_is_marimo_notebook", return_value=True)
        marimo_function_checker.visit(module)

        messages = marimo_function_checker.linter.release_messages()
        assert not messages, "Expected no messages for valid marimo notebook"

    @pytest.mark.usefixtures("marimo_function_checker")
    def test_non_marimo_file(self, marimo_function_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that non-marimo files are ignored.

        Args:
            marimo_function_checker: The Marimo function checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        def helper_function():
            return "helper"

        async def async_helper():
            return "async helper"

        square = lambda x: x * x
        """
        module: astroid.Module = astroid_parse(code)
        mocker.patch.object(marimo_function_checker, "_is_marimo_notebook", return_value=False)
        marimo_function_checker.visit(module)

        messages = marimo_function_checker.linter.release_messages()
        assert not messages, "Expected no messages for non-marimo file"
