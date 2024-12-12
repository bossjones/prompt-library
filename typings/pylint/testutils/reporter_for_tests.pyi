"""
This type stub file was generated by pyright.
"""

from io import StringIO
from typing import TYPE_CHECKING
from pylint.message import Message
from pylint.reporters import BaseReporter
from pylint.reporters.ureports.nodes import Section

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
class GenericTestReporter(BaseReporter):
    """Reporter storing plain text messages."""
    out: StringIO
    def __init__(self) -> None:
        ...
    
    def reset(self) -> None:
        ...
    
    def handle_message(self, msg: Message) -> None:
        """Append messages to the list of messages of the reporter."""
        ...
    
    def finalize(self) -> str:
        """Format and print messages in the context of the path."""
        ...
    
    def on_set_current_module(self, module: str, filepath: str | None) -> None:
        ...
    
    def display_reports(self, layout: Section) -> None:
        """Ignore layouts."""
        ...
    


class MinimalTestReporter(BaseReporter):
    def on_set_current_module(self, module: str, filepath: str | None) -> None:
        ...
    


class FunctionalTestReporter(BaseReporter):
    def display_reports(self, layout: Section) -> None:
        """Ignore layouts and don't call self._display()."""
        ...
    


