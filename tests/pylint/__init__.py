"""Tests for pylint."""

from __future__ import annotations

import contextlib

import pysnooper

from loguru import logger

from pylint.testutils.unittest_linter import UnittestLinter


@pysnooper.snoop(thread_info=True, max_variable_length=None, depth=10)
@contextlib.contextmanager
def assert_no_messages(linter: UnittestLinter):
    """Assert that no messages are added by the given method."""
    with assert_adds_messages(linter):
        yield


@contextlib.contextmanager
def assert_adds_messages(linter: UnittestLinter, *messages):
    """Assert that exactly the given method adds the given messages.

    The list of messages must exactly match *all* the messages added by the
    method. Additionally, we check to see whether the args in each message can
    actually be substituted into the message string.
    """
    yield
    got = linter.release_messages()
    no_msg = "No message."
    expected = "\n".join(repr(m) for m in messages) or no_msg
    got_str = "\n".join(repr(m) for m in got) or no_msg
    msg = f"Expected messages did not match actual.\n\nExpected:\n{expected}\n\nGot:\n{got_str}\n"
    assert got == list(messages), msg
