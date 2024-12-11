"""
This type stub file was generated by pyright.
"""

from collections import Counter
from typing import TextIO
from _pytest.config import Config
from pylint.testutils.functional.test_file import FunctionalTestFile
from pylint.testutils.output_line import OutputLine

MessageCounter = Counter[tuple[int, str]]
PYLINTRC = ...
class LintModuleTest:
    maxDiff = ...
    def __init__(self, test_file: FunctionalTestFile, config: Config | None = ...) -> None:
        ...

    def setUp(self) -> None:
        ...

    def runTest(self) -> None:
        ...

    def __str__(self) -> str:
        ...

    @staticmethod
    def get_expected_messages(stream: TextIO) -> MessageCounter:
        """Parses a file and get expected messages.

        :param stream: File-like input stream.
        :type stream: enumerable
        :returns: A dict mapping line,msg-symbol tuples to the count on this line.
        :rtype: dict
        """
        ...

    @staticmethod
    def multiset_difference(expected_entries: MessageCounter, actual_entries: MessageCounter) -> tuple[MessageCounter, dict[tuple[int, str], int]]:
        """Takes two multisets and compares them.

        A multiset is a dict with the cardinality of the key as the value.
        """
        ...

    def error_msg_for_unequal_messages(self, actual_messages: MessageCounter, expected_messages: MessageCounter, actual_output: list[OutputLine]) -> str:
        ...

    def error_msg_for_unequal_output(self, expected_lines: list[OutputLine], received_lines: list[OutputLine]) -> str:
        ...
