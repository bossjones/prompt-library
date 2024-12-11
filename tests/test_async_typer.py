"""Test the async Typer class."""

from __future__ import annotations

import asyncio

from collections.abc import AsyncGenerator, Generator
from typing import TYPE_CHECKING, Any

from typer import Typer

import pytest

from prompt_library.asynctyper import AsyncTyper, AsyncTyperImproved


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.logging import LogCaptureFixture

    from pytest_mock import MockerFixture


@pytest.fixture
async def async_typer() -> AsyncGenerator[AsyncTyperImproved, None]:
    """Fixture that provides an AsyncTyperImproved instance.

    Yields:
        AsyncTyperImproved: A fresh instance of AsyncTyperImproved for testing.
    """
    yield AsyncTyperImproved()


@pytest.mark.asyncio
@pytest.mark.asynciotyper
async def test_async_command(capsys: CaptureFixture[str]) -> None:
    """Test the async_command decorator with a simple hello function.

    Args:
        capsys: Pytest fixture to capture stdout/stderr.
    """
    app = AsyncTyper()

    @app.command()
    async def hello() -> None:
        """Say hello."""
        await asyncio.sleep(0.1)  # Reduced sleep time for faster tests
        print("Hello!")

    await hello()
    captured = capsys.readouterr()
    assert captured.out == "Hello!\n"


@pytest.mark.asynciotyper
def test_async_typer_creation(async_typer: AsyncTyperImproved) -> None:
    """Test AsyncTyperImproved instance creation and inheritance.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """
    assert isinstance(async_typer, AsyncTyperImproved)
    assert isinstance(async_typer, Typer)


@pytest.mark.asynciotyper
def test_maybe_run_async_with_sync_function(async_typer: AsyncTyperImproved) -> None:
    """Test maybe_run_async with synchronous function.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    def sync_func() -> str:
        return "sync"

    decorated = async_typer.maybe_run_async(lambda x: x, sync_func)
    assert decorated() == "sync"


@pytest.mark.asyncio
@pytest.mark.asynciotyper
async def test_maybe_run_async_with_async_function(async_typer: AsyncTyperImproved) -> None:
    """Test maybe_run_async with asynchronous function.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    async def async_func() -> str:
        return "async"

    decorated = async_typer.maybe_run_async(lambda x: x, async_func)
    result = await decorated()
    assert result == "async"


@pytest.mark.asynciotyper
def test_callback_with_sync_function(async_typer: AsyncTyperImproved) -> None:
    """Test callback decorator with synchronous function.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    @async_typer.callback()
    def sync_callback() -> str:
        return "sync callback"

    result = sync_callback()
    assert result == "sync callback"


@pytest.mark.asyncio
@pytest.mark.asynciotyper
async def test_callback_with_async_function(async_typer: AsyncTyperImproved) -> None:
    """Test callback decorator with asynchronous function.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    @async_typer.callback()
    async def async_callback() -> str:
        return "async callback"

    result = await async_callback()
    assert result == "async callback"


@pytest.mark.asynciotyper
def test_command_with_sync_function(async_typer: AsyncTyperImproved) -> None:
    """Test command decorator with synchronous function.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    @async_typer.command()
    def sync_command() -> str:
        return "sync command"

    result = sync_command()
    assert result == "sync command"


@pytest.mark.asyncio
@pytest.mark.asynciotyper
async def test_command_with_async_function(async_typer: AsyncTyperImproved) -> None:
    """Test command decorator with asynchronous function.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    @async_typer.command()
    async def async_command() -> str:
        return "async command"

    result = await async_command()
    assert result == "async command"


@pytest.mark.asynciotyper
def test_callback_decorator_application(async_typer: AsyncTyperImproved, mocker: MockerFixture) -> None:
    """Test callback decorator application and mocking.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
        mocker: Pytest mocker fixture.
    """
    mock_decorator = mocker.Mock(return_value=mocker.Mock())
    async_typer.callback = mocker.Mock(return_value=mock_decorator)

    @async_typer.callback()
    def test_callback() -> None:
        pass

    async_typer.callback.assert_called_once_with()
    mock_decorator.assert_called_once()


@pytest.mark.asynciotyper
def test_command_decorator_application(async_typer: AsyncTyperImproved, mocker: MockerFixture) -> None:
    """Test command decorator application and mocking.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
        mocker: Pytest mocker fixture.
    """
    mock_decorator = mocker.Mock(return_value=mocker.Mock())
    async_typer.command = mocker.Mock(return_value=mock_decorator)

    @async_typer.command()
    def test_command() -> None:
        pass

    async_typer.command.assert_called_once_with()
    mock_decorator.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.asynciotyper
async def test_async_command_execution(async_typer: AsyncTyperImproved) -> None:
    """Test async command execution with sleep.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    @async_typer.command()
    async def async_command() -> str:
        await asyncio.sleep(0.1)  # Reduced sleep time for faster tests
        return "async result"

    result = await async_command()
    assert result == "async result"


@pytest.mark.asyncio
@pytest.mark.asynciotyper
async def test_async_callback_execution(async_typer: AsyncTyperImproved) -> None:
    """Test async callback execution with sleep.

    Args:
        async_typer: Fixture providing AsyncTyperImproved instance.
    """

    @async_typer.callback()
    async def async_callback() -> str:
        await asyncio.sleep(0.1)  # Reduced sleep time for faster tests
        return "async callback result"

    result = await async_callback()
    assert result == "async callback result"
