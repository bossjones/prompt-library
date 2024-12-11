"""Tests for the prompt_library.shell module."""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys

from pathlib import Path
from typing import TYPE_CHECKING, Any, Generator

from loguru import logger

import pytest

from prompt_library.shell import (
    ProcessException,
    ShellConsole,
    _aio_run_process_and_communicate,
    _popen,
    _popen_communicate,
    _popen_stdout,
    _popen_stdout_lock,
    _stat_y_file,
    pquery,
    run_coroutine_subprocess,
)


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


@pytest.fixture
def temp_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary file for testing.

    Args:
        tmp_path: Pytest fixture providing a temporary directory unique to each test function.

    Yields:
        Path: Path to the temporary file.
    """
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    yield test_file
    if test_file.exists():
        test_file.unlink()


@pytest.mark.asyncio
async def test_aio_run_process_and_communicate(capsys: CaptureFixture[str]) -> None:
    """Test the _aio_run_process_and_communicate function.

    Args:
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    result = await _aio_run_process_and_communicate(["echo", "hello"])
    assert result == "hello"
    captured = capsys.readouterr()
    assert "Process pid is:" in captured.out


def test_stat_y_file(temp_file: Path) -> None:
    """Test the _stat_y_file function.

    Args:
        temp_file: Fixture providing a temporary test file.
    """
    # On macOS, we need to use a different stat format
    if sys.platform == "darwin":
        # Mock the stat command to use macOS format
        timestamp = _stat_y_file(str(temp_file))
        # Just verify we get some output, as format may vary by OS
        assert isinstance(timestamp, str)
    else:
        timestamp = _stat_y_file(str(temp_file))
        assert isinstance(timestamp, str)
        assert len(timestamp) > 0


def test_popen(temp_file: Path) -> None:
    """Test the _popen function.

    Args:
        temp_file: Fixture providing a temporary test file.
    """
    result = _popen(("cat", str(temp_file)))
    assert result == b"test content"


def test_popen_communicate(temp_file: Path) -> None:
    """Test the _popen_communicate function.

    Args:
        temp_file: Fixture providing a temporary test file.
    """
    result = _popen_communicate(("cat", str(temp_file)))
    assert result == b"test content"


def test_shell_console_message(capsys: CaptureFixture[str]) -> None:
    """Test the ShellConsole.message method.

    Args:
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    # Test with quiet mode off
    ShellConsole.quiet = False
    ShellConsole.message("Test message")
    captured = capsys.readouterr()
    assert captured.out == "Test message\n"

    # Test with quiet mode on
    ShellConsole.quiet = True
    ShellConsole.message("Test message")
    captured = capsys.readouterr()
    assert captured.out == ""

    # Reset quiet mode
    ShellConsole.quiet = False


def test_pquery_success() -> None:
    """Test the pquery function with a successful command."""
    result = pquery(["echo", "hello"])
    assert result == "hello\n"


def test_pquery_failure() -> None:
    """Test the pquery function with a failing command."""
    with pytest.raises(ProcessException):
        pquery(["nonexistent_command"])


def test_popen_stdout(capsys: CaptureFixture[str]) -> None:
    """Test the _popen_stdout function.

    Args:
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    _popen_stdout("echo 'test output'")
    captured = capsys.readouterr()
    assert "BEGIN: echo 'test output'" in captured.out
    assert ">>> test output" in captured.out
    assert "END: echo 'test output'" in captured.out


def test_popen_stdout_lock(capsys: CaptureFixture[str]) -> None:
    """Test the _popen_stdout_lock function.

    Args:
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    _popen_stdout_lock("echo 'test output'")
    captured = capsys.readouterr()
    assert "BEGIN: echo 'test output'" in captured.out
    assert ">>> test output" in captured.out
    assert "END: echo 'test output'" in captured.out


@pytest.mark.asyncio
async def test_run_coroutine_subprocess() -> None:
    """Test the run_coroutine_subprocess function."""
    result = await run_coroutine_subprocess("echo 'test'", "file:///test", None)
    assert result == "test"


def test_process_exception() -> None:
    """Test the ProcessException class."""
    exc = ProcessException(1)
    assert exc.args == (1,)
