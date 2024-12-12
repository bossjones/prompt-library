"""Tests for the Marimo imports validator."""

# pyright: reportAttributeAccessIssue=false
from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

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
class TestMarimoImportsChecker(CheckerTestCase):
    """Test class for the MarimoImportsChecker.

    This class tests the following rules:
    1. All imports must be in the first cell
    2. No global state mutations
    3. All cells must return tuples
    """

    @pytest.mark.usefixtures("marimo_imports_checker")
    def test_import_not_in_first_cell(self, marimo_imports_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that imports not in first cell are detected.

        Args:
            marimo_imports_checker: The Marimo imports checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            import os
            return (os,)

        @app.cell
        def __(os):
            import sys  # This should trigger a warning
            return (os, sys)
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_imports_checker, "_is_marimo_notebook", return_value=True)
        marimo_imports_checker.visit(module)

        messages = marimo_imports_checker.linter.release_messages()
        assert any(msg.msg_id == "import-not-in-first-cell" for msg in messages), (
            "Expected import-not-in-first-cell message"
        )

    @pytest.mark.usefixtures("marimo_imports_checker")
    def test_global_state_mutation(self, marimo_imports_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that global state mutations are detected.

        Args:
            marimo_imports_checker: The Marimo imports checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        counter = 0

        @app.cell
        def __():
            global counter
            counter += 1
            return (counter,)
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_imports_checker, "_is_marimo_notebook", return_value=True)
        marimo_imports_checker.visit(module)

        messages = marimo_imports_checker.linter.release_messages()
        assert any(msg.msg_id == "global-state-mutation" for msg in messages), "Expected global-state-mutation message"

    @pytest.mark.usefixtures("marimo_imports_checker")
    def test_missing_tuple_return(self, marimo_imports_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that non-tuple returns are detected.

        Args:
            marimo_imports_checker: The Marimo imports checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            x = 42
            return x  # Should be (x,)
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_imports_checker, "_is_marimo_notebook", return_value=True)
        marimo_imports_checker.visit(module)

        messages = marimo_imports_checker.linter.release_messages()
        assert any(msg.msg_id == "missing-tuple-return" for msg in messages), "Expected missing-tuple-return message"

    @pytest.mark.usefixtures("marimo_imports_checker")
    def test_valid_marimo_notebook(self, marimo_imports_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that valid marimo notebook code passes all checks.

        Args:
            marimo_imports_checker: The Marimo imports checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        @app.cell
        def __():
            import os
            import sys
            return (os, sys)

        @app.cell
        def __(os, sys):
            result = os.path.join(sys.path[0])
            return (result,)
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_imports_checker, "_is_marimo_notebook", return_value=True)
        marimo_imports_checker.visit(module)

        messages = marimo_imports_checker.linter.release_messages()
        assert not messages, "Expected no messages for valid marimo notebook"

    @pytest.mark.usefixtures("marimo_imports_checker")
    def test_non_marimo_file(self, marimo_imports_checker: BaseChecker, mocker: MockerFixture) -> None:
        """Test that non-marimo files are ignored.

        Args:
            marimo_imports_checker: The Marimo imports checker instance
            mocker: The pytest mocker fixture
        """
        code = """
        import os
        import sys

        def some_function():
            global some_var
            some_var = 42
            return some_var
        """
        module = astroid.parse(code)
        mocker.patch.object(marimo_imports_checker, "_is_marimo_notebook", return_value=False)
        marimo_imports_checker.visit(module)

        messages = marimo_imports_checker.linter.release_messages()
        assert not messages, "Expected no messages for non-marimo file"
