#!/usr/bin/env python
"""prompt_library.shell module containing utility functions for running shell commands."""

from __future__ import annotations

import asyncio
import os
import pathlib
import subprocess
import sys
import time

from asyncio.subprocess import Process
from pathlib import Path
from typing import List, Tuple, Union

import uritools

from codetiming import Timer


HOME_PATH = os.environ.get("HOME")


async def _aio_run_process_and_communicate(cmd: list[str], cwd: str | None = None) -> str:
    """
    Run a command asynchronously using asyncio.create_subprocess_exec and communicate.

    Args:
        cmd (List[str]): The command to run as a list of strings.
        cwd (Union[str, None], optional): The working directory to run the command in. Defaults to None.

    Returns:
        str: The decoded stdout output of the command.
    """
    program = cmd
    process: Process = await asyncio.create_subprocess_exec(*program, stdout=asyncio.subprocess.PIPE, cwd=cwd)
    print(f"Process pid is: {process.pid}")
    stdout, stderr = await process.communicate()
    return stdout.decode("utf-8").strip()


def _stat_y_file(fname: str, env: dict = None, cwd: str | None = None) -> str:
    """
    Get the timestamp of a file using the 'stat' command.

    Args:
        fname (str): The name of the file to get the timestamp for.
        env (dict, optional): Environment variables to use when running the command. Defaults to None.
        cwd (Union[str, None], optional): The working directory to run the command in. Defaults to None.

    Returns:
        str: The timestamp of the file.
    """
    if env is None:
        env = {}
    cmd_arg_without_str_fmt = f"""stat -c %y {fname}"""
    print(f"cmd_arg_without_str_fmt={cmd_arg_without_str_fmt}")

    cmd_arg = rf"""{cmd_arg_without_str_fmt}"""
    print(f"cmd_arg={cmd_arg}")
    try:
        result = subprocess.run(
            [cmd_arg],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            shell=True,
            check=False,
        )
        timestamp = result.stdout.replace("\n", "")
        print(f"timestamp={timestamp}")
    except subprocess.CalledProcessError as e:
        print(e.output)
    return timestamp


def _popen(cmd_arg: tuple, env: dict = None, cwd: str | None = None) -> bytes:
    """
    Run a command using subprocess.Popen and read the stdout output.

    Args:
        cmd_arg (Tuple): The command to run as a tuple of arguments.
        env (dict, optional): Environment variables to use when running the command. Defaults to None.
        cwd (Union[str, None], optional): The working directory to run the command in. Defaults to None.

    Raises:
        RuntimeError: If there was an error closing the command stream.

    Returns:
        bytes: The stdout output of the command.
    """
    if env is None:
        env = {}
    with open("/dev/null") as devnull:
        with subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=devnull, env=env, cwd=cwd) as cmd:
            retval = cmd.stdout.read().strip()
            err = cmd.wait()
        if err:
            raise RuntimeError(f"Failed to close {cmd_arg} stream")
    return retval


def _popen_communicate(cmd_arg: tuple, env: dict = None, cwd: str | None = None) -> bytes:
    """
    Run a command using subprocess.Popen, wait for it to finish, and read the stdout output.

    Args:
        cmd_arg (Tuple): The command to run as a tuple of arguments.
        env (dict, optional): Environment variables to use when running the command. Defaults to None.
        cwd (Union[str, None], optional): The working directory to run the command in. Defaults to None.

    Raises:
        RuntimeError: If there was an error closing the command stream.

    Returns:
        bytes: The stdout output of the command.
    """
    if env is None:
        env = {}
    # devnull = open("/dev/null")
    with subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=cwd) as cmd:
        try:
            time.sleep(0.2)
            retval = cmd.stdout.read().strip()
            err = cmd.wait()

        finally:
            cmd.terminate()
            try:
                outs, _ = cmd.communicate(timeout=0.2)
                print("== subprocess exited with rc =", cmd.returncode)
                print(outs.decode("utf-8"))
            except subprocess.TimeoutExpired:
                print("subprocess did not terminate in time")

    if err:
        raise RuntimeError(f"Failed to close {cmd_arg} stream")
    return retval


# SOURCE: https://github.com/ARMmbed/mbed-cli/blob/f168237fabd0e32edcb48e214fc6ce2250046ab3/test/util.py
# Process execution
class ProcessException(Exception):
    """Exception raised when there is an error running a process."""


class ShellConsole:  # pylint: disable=too-few-public-methods
    """Utility class for printing messages to the console."""

    quiet = False

    @classmethod
    def message(cls, str_format: str, *args: any) -> None:
        """
        Print a message to the console if quiet mode is not enabled.

        Args:
            str_format (str): The message format string.
            *args (any): Arguments to substitute into the format string.
        """
        if cls.quiet:
            return

        if args:
            print(str_format % args)
        else:
            print(str_format)

        # Flush so that messages are printed at the right time
        # as we use many subprocesses.
        sys.stdout.flush()


def pquery(command: str | list, stdin: bool = None, **kwargs: any) -> str:
    """
    Run a command using subprocess.Popen and return the decoded stdout output.

    Args:
        command (Union[str, list]): The command to run as a string or list of arguments.
        stdin (bool, optional): Whether to enable stdin for the process. Defaults to None.
        **kwargs (any): Additional keyword arguments to pass to subprocess.Popen.

    Raises:
        ProcessException: If there was an error running the command.

    Returns:
        str: The decoded stdout output of the command.
    """
    # SOURCE: https://github.com/ARMmbed/mbed-cli/blob/f168237fabd0e32edcb48e214fc6ce2250046ab3/test/util.py
    # Example:
    if type(command) == list:
        print(" ".join(command))
    elif type(command) == str:
        command = command.split(" ")
        print(f"cmd: {command}")
    try:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs) as proc:
            stdout, _ = proc.communicate(stdin)
    except Exception:
        print("[fail] cmd={command}, ret={proc.returncode}")
        raise

    if proc.returncode != 0:
        raise ProcessException(proc.returncode)

    return stdout.decode("utf-8")


def _popen_stdout(cmd_arg: str, cwd: str | None = None) -> None:
    """
    Run a command using subprocess.Popen and print the stdout output line by line.

    Args:
        cmd_arg (str): The command to run as a string.
        cwd (Union[str, None], optional): The working directory to run the command in. Defaults to None.
    """
    # if passing a single string, either shell mut be True or else the string must simply name the program to be executed without specifying any arguments
    with subprocess.Popen(
        cmd_arg,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        bufsize=4096,
        shell=True,
    ) as cmd:
        ShellConsole.message(f"BEGIN: {cmd_arg}")
        # output, err = cmd.communicate()

        for line in iter(cmd.stdout.readline, b""):
            # Print line
            _line = line.rstrip()
            ShellConsole.message(f">>> {_line.decode('utf-8')}")

        ShellConsole.message(f"END: {cmd_arg}")
        # subprocess.CompletedProcess(args=cmd_arg, returncode=0)


def _popen_stdout_lock(cmd_arg: str, cwd: str | None = None) -> None:
    """
    Run a command using subprocess.Popen with a lock and print the stdout output line by line.

    Args:
        cmd_arg (str): The command to run as a string.
        cwd (Union[str, None], optional): The working directory to run the command in. Defaults to None.
    """
    # if passing a single string, either shell mut be True or else the string must simply name the program to be executed without specifying any arguments
    with subprocess.Popen(
        cmd_arg,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        bufsize=4096,
        shell=True,
    ) as cmd:
        ShellConsole.message(f"BEGIN: {cmd_arg}")
        # output, err = cmd.communicate()

        for line in iter(cmd.stdout.readline, b""):
            # Print line
            _line = line.rstrip()
            ShellConsole.message(f">>> {_line.decode('utf-8')}")

        ShellConsole.message(f"END: {cmd_arg}")
        subprocess.CompletedProcess(args=cmd_arg, returncode=0)


async def run_coroutine_subprocess(cmd: str, uri: str, working_dir: str | None = None) -> str:
    """
    Run a command as a coroutine subprocess using asyncio.create_subprocess_shell.

    Args:
        cmd (str): The command to run as a string.
        uri (str): The URI associated with the command.
        working_dir (str | None, optional): The working directory to run the command in. Defaults to the current directory.

    Returns:
        str: The decoded stdout output of the command.
    """
    if working_dir is None:
        working_dir = f"{pathlib.Path('./').absolute()}"

    await asyncio.sleep(0.05)

    timer = Timer(text=f"Task {__name__} elapsed time: {{:.1f}}")

    env = dict(os.environ)
    dl_uri = uritools.urisplit(uri)

    result = "0"
    cmd = f"{cmd}"

    timer.start()
    process = await asyncio.create_subprocess_shell(
        cmd,
        env=env,
        cwd=working_dir,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=None,
    )
    stdout, stderr = await process.communicate()
    result = stdout.decode("utf-8").strip()
    timer.stop()
    return result
