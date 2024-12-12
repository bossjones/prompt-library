"""
This type stub file was generated by pyright.
"""

import tokenize
from typing import TYPE_CHECKING
from pylint import interfaces
from pylint.lint.pylinter import PyLinter

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
class _MessageStateHandler:
    """Class that handles message disabling & enabling and processing of inline
    pragma's.
    """
    def __init__(self, linter: PyLinter) -> None:
        ...
    
    def disable(self, msgid: str, scope: str = ..., line: int | None = ..., ignore_unknown: bool = ...) -> None:
        """Disable a message for a scope."""
        ...
    
    def disable_next(self, msgid: str, _: str = ..., line: int | None = ..., ignore_unknown: bool = ...) -> None:
        """Disable a message for the next line."""
        ...
    
    def enable(self, msgid: str, scope: str = ..., line: int | None = ..., ignore_unknown: bool = ...) -> None:
        """Enable a message for a scope."""
        ...
    
    def disable_noerror_messages(self) -> None:
        """Disable message categories other than `error` and `fatal`."""
        ...
    
    def list_messages_enabled(self) -> None:
        ...
    
    def is_message_enabled(self, msg_descr: str, line: int | None = ..., confidence: interfaces.Confidence | None = ...) -> bool:
        """Is this message enabled for the current file ?

        Optionally, is it enabled for this line and confidence level ?

        The current file is implicit and mandatory. As a result this function
        can't be cached right now as the line is the line of the currently
        analysed file (self.file_state), if it changes, then the result for
        the same msg_descr/line might need to change.

        :param msg_descr: Either the msgid or the symbol for a MessageDefinition
        :param line: The line of the currently analysed file
        :param confidence: The confidence of the message
        """
        ...
    
    def process_tokens(self, tokens: list[tokenize.TokenInfo]) -> None:
        """Process tokens from the current module to search for module/block level
        options.

        See func_block_disable_msg.py test case for expected behaviour.
        """
        ...
    


