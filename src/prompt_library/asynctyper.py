"""prompt_library.utils.asynctyper"""

from __future__ import annotations

import asyncio
import inspect
import logging

from collections.abc import Awaitable, Callable, Coroutine, Iterable, Sequence
from functools import partial, wraps
from typing import Any, Dict, List, Optional, ParamSpec, Set, Tuple, Type, TypeVar, Union, cast

import anyio
import asyncer
import discord
import rich
import typer

from rich.pretty import pprint
from typer import Typer
from typer.core import TyperCommand, TyperGroup
from typer.models import CommandFunctionType

import prompt_library

from prompt_library.bot_logger import get_logger


P = ParamSpec("P")
R = TypeVar("R")


F = TypeVar("F", bound=Callable[..., Any])


class AsyncTyperImproved(Typer):
    @staticmethod
    def maybe_run_async(
        decorator: Callable[[CommandFunctionType], CommandFunctionType],
        f: CommandFunctionType,
    ) -> CommandFunctionType:
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            async def async_runner(*args: Any, **kwargs: Any) -> Any:
                return await f(*args, **kwargs)

            @wraps(f)
            def sync_runner(*args: Any, **kwargs: Any) -> Any:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    return async_runner(*args, **kwargs)
                return loop.run_until_complete(async_runner(*args, **kwargs))

            return decorator(cast(CommandFunctionType, sync_runner))
        return decorator(f)

    # noinspection PyShadowingBuiltins
    def callback(
        self,
        name: str | None = None,
        *,
        cls: type[TyperGroup] | None = None,
        invoke_without_command: bool = False,
        no_args_is_help: bool = False,
        subcommand_metavar: str | None = None,
        chain: bool = False,
        result_callback: Callable[..., Any] | None = None,
        context_settings: dict[Any, Any] | None = None,
        help: str | None = None,
        epilog: str | None = None,
        short_help: str | None = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        hidden: bool = False,
        deprecated: bool = False,
        rich_help_panel: str | None = None,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        decorator = super().callback(
            name=name,
            cls=cls,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            context_settings=context_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
            rich_help_panel=rich_help_panel,
        )
        return lambda f: self.maybe_run_async(decorator, f)

    # noinspection PyShadowingBuiltins
    def command(
        self,
        name: str | None = None,
        *,
        cls: type[TyperCommand] | None = None,
        context_settings: dict[Any, Any] | None = None,
        help: str | None = None,
        epilog: str | None = None,
        short_help: str | None = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
        rich_help_panel: str | None = None,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        decorator = super().command(
            name=name,
            cls=cls,
            context_settings=context_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            rich_help_panel=rich_help_panel,
        )
        return lambda f: self.maybe_run_async(decorator, f)


class AsyncTyper(Typer):
    """
    A custom Typer class that supports asynchronous functions.

    This class decorates functions with the given decorator, but only if the function
    is not already a coroutine function.
    """

    @staticmethod
    def maybe_run_async(decorator: Callable[[F], F], f: F) -> F:
        """
        Decorates a function with the given decorator if it's not a coroutine function.

        Args:
            decorator: The decorator to apply to the function.
            f: The function to decorate.

        Returns:
            The decorated function.
        """
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            def runner(*args: Any, **kwargs: Any) -> Any:
                return asyncer.runnify(f)(*args, **kwargs)

            decorator(runner)
        else:
            decorator(f)
        return f

    def callback(self, *args: Any, **kwargs: Any) -> Callable[[F], F]:
        """
        Overrides the callback method to support asynchronous functions.

        Returns:
            A partial function that applies the async decorator to the callback.
        """
        decorator = super().callback(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)

    def command(self, *args: Any, **kwargs: Any) -> Callable[[F], F]:
        """
        Overrides the command method to support asynchronous functions.

        Returns:
            A partial function that applies the async decorator to the command.
        """
        decorator = super().command(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)
