"""
This type stub file was generated by pyright.
"""

import collections
from collections.abc import MutableSequence
from typing import TYPE_CHECKING
from pylint.reporters.ureports.nodes import Section
from pylint.typing import ReportsCallable
from pylint.utils import LinterStats
from pylint.checkers import BaseChecker
from pylint.lint.pylinter import PyLinter

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
ReportsDict = collections.defaultdict["BaseChecker", list[tuple[str, str, ReportsCallable]]]
class ReportsHandlerMixIn:
    """A mix-in class containing all the reports and stats manipulation
    related methods for the main lint class.
    """
    def __init__(self) -> None:
        ...
    
    def report_order(self) -> MutableSequence[BaseChecker]:
        """Return a list of reporters."""
        ...
    
    def register_report(self, reportid: str, r_title: str, r_cb: ReportsCallable, checker: BaseChecker) -> None:
        """Register a report.

        :param reportid: The unique identifier for the report
        :param r_title: The report's title
        :param r_cb: The method to call to make the report
        :param checker: The checker defining the report
        """
        ...
    
    def enable_report(self, reportid: str) -> None:
        """Enable the report of the given id."""
        ...
    
    def disable_report(self, reportid: str) -> None:
        """Disable the report of the given id."""
        ...
    
    def report_is_enabled(self, reportid: str) -> bool:
        """Is the report associated to the given identifier enabled ?"""
        ...
    
    def make_reports(self: PyLinter, stats: LinterStats, old_stats: LinterStats | None) -> Section:
        """Render registered reports."""
        ...
    


