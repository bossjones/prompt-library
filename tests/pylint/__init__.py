"""Tests for pylint."""

from __future__ import annotations

import contextlib

import pysnooper

from loguru import logger

from pylint.testutils.unittest_linter import UnittestLinter


# @pysnooper.snoop(thread_info=True, max_variable_length=None, depth=10)
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
    # import bpdb

    # bpdb.set_trace()
    got = linter.release_messages()
    no_msg = "No message."
    expected = "\n".join(repr(m) for m in messages) or no_msg
    got_str = "\n".join(repr(m) for m in got) or no_msg
    msg = f"Expected messages did not match actual.\n\nExpected:\n{expected}\n\nGot:\n{got_str}\n"
    assert got == list(messages), msg


# > /Users/malcolm/dev/bossjones/prompt-library/tests/pylint/__init__.py(34)assert_adds_messages()
# -> got = linter.release_messages()
# (BPdb) l
#  29         """
#  30         yield
#  31         import bpdb
#  32
#  33         bpdb.set_trace()
#  34  ->     got = linter.release_messages()
#  35         no_msg = "No message."
#  36         expected = "\n".join(repr(m) for m in messages) or no_msg
#  37         got_str = "\n".join(repr(m) for m in got) or no_msg
#  38         msg = f"Expected messages did not match actual.\n\nExpected:\n{expected}\n\nGot:\n{got_str}\n"
#  39         assert got == list(messages), msg
# (BPdb) p __name__
# 'tests.pylint'
# (BPdb) args
# linter = Checker 'main' (responsible for 'F0001', 'F0002', 'F0010', 'F0011', 'I0001', 'I0010', 'I0011', 'I0013', 'I0020', 'I0021', 'I0022', 'E0001', 'E0011', 'W0012', 'R0022', 'E0013', 'E0014', 'E0015')
# messages = ()
