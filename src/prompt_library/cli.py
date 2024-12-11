"""prompt_library.cli"""

# pyright: reportMissingTypeStubs=false
# pylint: disable=no-member
# pylint: disable=no-value-for-parameter
# pyright: reportAttributeAccessIssue=false
# SOURCE: https://github.com/tiangolo/typer/issues/88#issuecomment-1732469681
from __future__ import annotations

import asyncio
import importlib.util
import inspect
import json
import logging
import os
import signal
import subprocess
import sys
import tempfile
import traceback
import typing

from collections.abc import Awaitable, Iterable, Sequence
from enum import Enum
from functools import partial, wraps
from importlib import import_module, metadata
from importlib.metadata import version as importlib_metadata_version
from pathlib import Path
from re import Pattern
from typing import Annotated, Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union
from urllib.parse import urlparse

import anyio
import bpdb
import rich
import typer

from langchain.globals import set_debug, set_verbose
from langchain_chroma import Chroma as ChromaVectorStore
from loguru import logger
from rich import print, print_json
from rich.console import Console
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.table import Table
from typer import Typer

import prompt_library

from prompt_library.asynctyper import AsyncTyper, AsyncTyperImproved
from prompt_library.bot_logger import get_logger, global_log_config
from prompt_library.types import PathLike


# # SOURCE: https://python.langchain.com/v0.2/docs/how_to/debugging/
# if aiosettings.debug_langchain:
#     # Setting the global debug flag will cause all LangChain components with callback support (chains, models, agents, tools, retrievers) to print the inputs they receive and outputs they generate. This is the most verbose setting and will fully log raw inputs and outputs.
#     set_debug(True)
#     # Setting the verbose flag will print out inputs and outputs in a slightly more readable format and will skip logging certain raw outputs (like the token usage stats for an LLM call) so that you can focus on application logic.
#     set_verbose(True)

# SOURCE: https://github.com/Delgan/loguru/blob/420704041797daf804b505e5220805528fe26408/docs/resources/recipes.rst#L1083
global_log_config(
    log_level=logging.getLevelName("DEBUG"),
    json=False,
)


class ChromaChoices(str, Enum):
    load = "load"
    generate = "generate"
    get_response = "get_response"


# Load existing subcommands
def load_commands(directory: str = "subcommands") -> None:
    """
    Load subcommands from the specified directory.

    This function loads subcommands from the specified directory and adds them to the main Typer app.
    It iterates over the files in the directory, imports the modules that end with "_cmd.py", and adds
    their Typer app to the main app if they have one.

    Args:
        directory (str, optional): The directory to load subcommands from. Defaults to "subcommands".

    Returns:
        None
    """
    script_dir = Path(__file__).parent
    subcommands_dir = script_dir / directory

    logger.debug(f"Loading subcommands from {subcommands_dir}")

    for filename in os.listdir(subcommands_dir):
        logger.debug(f"Filename: {filename}")
        if filename.endswith("_cmd.py"):
            module_name = f"{__name__.split('.')[0]}.{directory}.{filename[:-3]}"
            logger.debug(f"Loading subcommand: {module_name}")
            module = import_module(module_name)
            if hasattr(module, "APP"):
                logger.debug(f"Adding subcommand: {filename[:-7]}")
                APP.add_typer(module.APP, name=filename[:-7])


# APP = AsyncTyper()
APP = AsyncTyperImproved()
console = Console()
cprint = console.print
load_commands()


def version_callback(version: bool) -> None:
    """Print the version of prompt_library."""
    if version:
        rich.print(f"prompt_library version: {prompt_library.__version__}")
        raise typer.Exit()


@APP.command()
def version(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed version info")] = False,
) -> None:
    """Display version information."""
    rich.print(f"prompt_library version: {prompt_library.__version__}")
    if verbose:
        rich.print(f"Python version: {sys.version}")


@APP.command()
def deps() -> None:
    """Deps command"""
    rich.print(f"prompt_library version: {prompt_library.__version__}")
    rich.print(f"langchain_version: {importlib_metadata_version('langchain')}")
    rich.print(f"langchain_community_version: {importlib_metadata_version('langchain_community')}")
    rich.print(f"langchain_core_version: {importlib_metadata_version('langchain_core')}")
    rich.print(f"langchain_openai_version: {importlib_metadata_version('langchain_openai')}")
    rich.print(f"langchain_text_splitters_version: {importlib_metadata_version('langchain_text_splitters')}")
    rich.print(f"langchain_chroma_version: {importlib_metadata_version('langchain_chroma')}")
    rich.print(f"chromadb_version: {importlib_metadata_version('chromadb')}")
    rich.print(f"langsmith_version: {importlib_metadata_version('langsmith')}")
    rich.print(f"pydantic_version: {importlib_metadata_version('pydantic')}")
    rich.print(f"pydantic_settings_version: {importlib_metadata_version('pydantic_settings')}")
    rich.print(f"ruff_version: {importlib_metadata_version('ruff')}")


@APP.command()
def about() -> None:
    """About command"""
    typer.echo("This is GoobBot CLI")


@APP.command()
def show() -> None:
    """Show command"""
    cprint("\nShow prompt_library", style="yellow")


# @pysnooper.snoop(thread_info=True, max_variable_length=None, watch=["APP"], depth=10)
def main():
    APP()
    load_commands()


# @pysnooper.snoop(thread_info=True, max_variable_length=None, depth=10)
def entry():
    """Required entry point to enable hydra to work as a console_script."""
    main()  # pylint: disable=no-value-for-parameter


@APP.command()
def run_load_commands() -> None:
    """Load subcommands"""
    typer.echo("Loading subcommands....")
    load_commands()


def handle_sigterm(signo, frame):
    sys.exit(128 + signo)  # this will raise SystemExit and cause atexit to be called


signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    # # SOURCE: https://github.com/Delgan/loguru/blob/420704041797daf804b505e5220805528fe26408/docs/resources/recipes.rst#L1083
    # global_log_config(
    #     log_level=logging.getLevelName("DEBUG"),
    #     json=False,
    # )
    APP()
