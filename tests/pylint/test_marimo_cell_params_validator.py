"""Tests for the Marimo cell parameters validator."""

from __future__ import annotations

from typing import TYPE_CHECKING

import astroid

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
class TestMarimoCellParamsChecker(CheckerTestCase):
    """Test class for the MarimoCellParamsChecker."""

    CHECKER_CLASS = None  # Set by fixture

    @pytest.mark.usefixtures("marimo_cell_params_checker")
    def test_unused_cell_parameter(self, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that unused cell parameters are detected.

        Args:
            marimo_cell_params_checker: The Marimo cell parameters checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            import os
            return (os,)

        @app.cell
        def __(os, unused_param):  # unused_param should trigger a warning
            result = os.path.join("/tmp")
            return (result,)
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=True)
        marimo_cell_params_checker.visit(module)

        messages = marimo_cell_params_checker.linter.release_messages()
        assert any(msg.msg_id == "unused-cell-parameter" and msg.args[0] == "unused_param" for msg in messages), (
            "Expected unused-cell-parameter message for 'unused_param'"
        )

    @pytest.mark.usefixtures("marimo_cell_params_checker")
    def test_used_cell_parameter(self, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that used cell parameters are not flagged.

        Args:
            marimo_cell_params_checker: The Marimo cell parameters checker instance
            mocker: The pytest mocker fixture
        """
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
        module = astroid.parse(code)
        mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=True)
        marimo_cell_params_checker.visit(module)

        messages = marimo_cell_params_checker.linter.release_messages()
        assert not messages, "Expected no messages for used parameters"

    @pytest.mark.usefixtures("marimo_cell_params_checker")
    def test_multiple_unused_parameters(self, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that multiple unused parameters are detected.

        Args:
            marimo_cell_params_checker: The Marimo cell parameters checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            import os
            import sys
            return (os, sys)

        @app.cell
        def __(os, unused1, sys, unused2):  # unused1 and unused2 should trigger warnings
            result = os.path.join(sys.path[0])
            return (result,)
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=True)
        marimo_cell_params_checker.visit(module)

        messages = marimo_cell_params_checker.linter.release_messages()
        unused_params = {msg.args[0] for msg in messages if msg.msg_id == "unused-cell-parameter"}
        assert unused_params == {"unused1", "unused2"}, "Expected warnings for 'unused1' and 'unused2'"

    @pytest.mark.usefixtures("marimo_cell_params_checker")
    def test_non_cell_function(self, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that non-cell functions are ignored.

        Args:
            marimo_cell_params_checker: The Marimo cell parameters checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        def regular_function(unused_param):  # Should not trigger warning
            return 42
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=True)
        marimo_cell_params_checker.visit(module)

        messages = marimo_cell_params_checker.linter.release_messages()
        assert not messages, "Expected no messages for non-cell functions"

    @pytest.mark.usefixtures("marimo_cell_params_checker")
    def test_non_marimo_file(self, marimo_cell_params_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that non-marimo files are ignored.

        Args:
            marimo_cell_params_checker: The Marimo cell parameters checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __(unused_param):  # Should not trigger warning in non-marimo file
            return (42,)
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_cell_params_checker, "_is_marimo_notebook", return_value=False)
        marimo_cell_params_checker.visit(module)

        messages = marimo_cell_params_checker.linter.release_messages()
        assert not messages, "Expected no messages for non-marimo files"
