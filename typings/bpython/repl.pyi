"""
This type stub file was generated by pyright.
"""

import abc
import code
from abc import abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING, Tuple, Type
from ._typing_compat import Literal
from pygments.token import _TokenType
from . import autocomplete
from .config import Config

have_pyperclip = ...
class RuntimeTimer:
    """Calculate running time"""
    def __init__(self) -> None:
        ...
    
    def __enter__(self) -> None:
        ...
    
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> Literal[False]:
        ...
    
    def reset_timer(self) -> None:
        ...
    
    def estimate(self) -> float:
        ...
    


class Interpreter(code.InteractiveInterpreter):
    """Source code interpreter for use in bpython."""
    bpython_input_re = ...
    def __init__(self, locals: Optional[Dict[str, Any]] = ...) -> None:
        """Constructor.

        The optional 'locals' argument specifies the dictionary in which code
        will be executed; it defaults to a newly created dictionary with key
        "__name__" set to "__main__".

        The syntaxerror callback can be set at any time and will be called
        on a caught syntax error. The purpose for this in bpython is so that
        the repl can be instantiated after the interpreter (which it
        necessarily must be with the current factoring) and then an exception
        callback can be added to the Interpreter instance afterwards - more
        specifically, this is so that autoindentation does not occur after a
        traceback.
        """
        ...
    
    def runsource(self, source: str, filename: Optional[str] = ..., symbol: str = ...) -> bool:
        """Execute Python code.

        source, filename and symbol are passed on to
        code.InteractiveInterpreter.runsource."""
        ...
    
    def showsyntaxerror(self, filename: Optional[str] = ...) -> None:
        """Override the regular handler, the code's copied and pasted from
        code.py, as per showtraceback, but with the syntaxerror callback called
        and the text in a pretty colour."""
        ...
    
    def showtraceback(self) -> None:
        """This needs to override the default traceback thing
        so it can put it into a pretty colour and maybe other
        stuff, I don't know"""
        ...
    
    def writetb(self, lines: Iterable[str]) -> None:
        """This outputs the traceback and should be overridden for anything
        fancy."""
        ...
    


class MatchesIterator:
    """Stores a list of matches and which one is currently selected if any.

    Also responsible for doing the actual replacement of the original line with
    the selected match.

    A MatchesIterator can be `clear`ed to reset match iteration, and
    `update`ed to set what matches will be iterated over."""
    def __init__(self) -> None:
        ...
    
    def __nonzero__(self) -> bool:
        """MatchesIterator is False when word hasn't been replaced yet"""
        ...
    
    def __bool__(self) -> bool:
        ...
    
    @property
    def candidate_selected(self) -> bool:
        """True when word selected/replaced, False when word hasn't been
        replaced yet"""
        ...
    
    def __iter__(self) -> MatchesIterator:
        ...
    
    def current(self) -> str:
        ...
    
    def __next__(self) -> str:
        ...
    
    def previous(self) -> str:
        ...
    
    def cur_line(self) -> Tuple[int, str]:
        """Returns a cursor offset and line with the current substitution
        made"""
        ...
    
    def substitute(self, match: str) -> Tuple[int, str]:
        """Returns a cursor offset and line with match substituted in"""
        ...
    
    def is_cseq(self) -> bool:
        ...
    
    def substitute_cseq(self) -> Tuple[int, str]:
        """Returns a new line by substituting a common sequence in, and update
        matches"""
        ...
    
    def update(self, cursor_offset: int, current_line: str, matches: List[str], completer: autocomplete.BaseCompletionType) -> None:
        """Called to reset the match index and update the word being replaced

        Should only be called if there's a target to update - otherwise, call
        clear"""
        ...
    
    def clear(self) -> None:
        ...
    


class Interaction(metaclass=abc.ABCMeta):
    def __init__(self, config: Config) -> None:
        ...
    
    @abc.abstractmethod
    def confirm(self, s: str) -> bool:
        ...
    
    @abc.abstractmethod
    def notify(self, s: str, n: float = ..., wait_for_keypress: bool = ...) -> None:
        ...
    
    @abc.abstractmethod
    def file_prompt(self, s: str) -> Optional[str]:
        ...
    


class NoInteraction(Interaction):
    def __init__(self, config: Config) -> None:
        ...
    
    def confirm(self, s: str) -> bool:
        ...
    
    def notify(self, s: str, n: float = ..., wait_for_keypress: bool = ...) -> None:
        ...
    
    def file_prompt(self, s: str) -> Optional[str]:
        ...
    


class SourceNotFound(Exception):
    """Exception raised when the requested source could not be found."""
    ...


@dataclass
class _FuncExpr:
    """Stack element in Repl._funcname_and_argnum"""
    full_expr: str
    function_expr: str
    arg_number: int
    opening: str
    keyword: Optional[str] = ...


class Repl(metaclass=abc.ABCMeta):
    """Implements the necessary guff for a Python-repl-alike interface

    The execution of the code entered and all that stuff was taken from the
    Python code module, I had to copy it instead of inheriting it, I can't
    remember why. The rest of the stuff is basically what makes it fancy.

    It reads what you type, passes it to a lexer and highlighter which
    returns a formatted string. This then gets passed to echo() which
    parses that string and prints to the curses screen in appropriate
    colours and/or bold attribute.

    The Repl class also keeps two stacks of lines that the user has typed in:
    One to be used for the undo feature. I am not happy with the way this
    works.  The only way I have been able to think of is to keep the code
    that's been typed in in memory and re-evaluate it in its entirety for each
    "undo" operation. Obviously this means some operations could be extremely
    slow.  I'm not even by any means certain that this truly represents a
    genuine "undo" implementation, but it does seem to be generally pretty
    effective.

    If anyone has any suggestions for how this could be improved, I'd be happy
    to hear them and implement it/accept a patch. I researched a bit into the
    idea of keeping the entire Python state in memory, but this really seems
    very difficult (I believe it may actually be impossible to work) and has
    its own problems too.

    The other stack is for keeping a history for pressing the up/down keys
    to go back and forth between lines.

    XXX Subclasses should implement echo, current_line, cw
    """
    @abc.abstractmethod
    def reevaluate(self): # -> None:
        ...
    
    @abc.abstractmethod
    def reprint_line(self, lineno: int, tokens: List[Tuple[_TokenType, str]]) -> None:
        ...
    
    @property
    def current_line(self) -> str:
        """The current line"""
        ...
    
    @current_line.setter
    def current_line(self, value: str) -> None:
        ...
    
    @property
    def cursor_offset(self) -> int:
        """The current cursor offset from the front of the "line"."""
        ...
    
    @cursor_offset.setter
    def cursor_offset(self, value: int) -> None:
        ...
    
    if TYPE_CHECKING:
        cpos: int
        ...
    def __init__(self, interp: Interpreter, config: Config) -> None:
        """Initialise the repl.

        interp is a Python code.InteractiveInterpreter instance

        config is a populated bpython.config.Struct.
        """
        ...
    
    @property
    def ps1(self) -> str:
        ...
    
    @property
    def ps2(self) -> str:
        ...
    
    def startup(self) -> None:
        """
        Execute PYTHONSTARTUP file if it exits. Call this after front
        end-specific initialisation.
        """
        ...
    
    def current_string(self, concatenate=...): # -> LiteralString | Literal['']:
        """If the line ends in a string get it, otherwise return ''"""
        ...
    
    def get_object(self, name: str) -> Any:
        ...
    
    def get_args(self): # -> bool:
        """Check if an unclosed parenthesis exists, then attempt to get the
        argspec() for it. On success, update self.funcprops,self.arg_pos and
        return True, otherwise set self.funcprops to None and return False"""
        ...
    
    def get_source_of_current_name(self) -> str:
        """Return the unicode source code of the object which is bound to the
        current name in the current input line. Throw `SourceNotFound` if the
        source cannot be found."""
        ...
    
    def set_docstring(self) -> None:
        ...
    
    def complete(self, tab: bool = ...) -> Optional[bool]:
        """Construct a full list of possible completions and
        display them in a window. Also check if there's an available argspec
        (via the inspect module) and bang that on top of the completions too.
        The return value is whether the list_win is visible or not.

        If no matches are found, just return whether there's an argspec to show
        If any matches are found, save them and select the first one.

        If tab is True exactly one match found, make the replacement and return
          the result of running complete() again on the new line.
        """
        ...
    
    def format_docstring(self, docstring: str, width: int, height: int) -> List[str]:
        """Take a string and try to format it into a sane list of strings to be
        put into the suggestion box."""
        ...
    
    def next_indentation(self) -> int:
        """Return the indentation of the next line based on the current
        input buffer."""
        ...
    
    @abstractmethod
    def getstdout(self) -> str:
        ...
    
    def get_session_formatted_for_file(self) -> str:
        """Format the stdout buffer to something suitable for writing to disk,
        i.e. without >>> and ... at input lines and with "# OUT: " prepended to
        output lines and "### " prepended to current line"""
        ...
    
    def write2file(self) -> None:
        """Prompt for a filename and write the current contents of the stdout
        buffer to disk."""
        ...
    
    def copy2clipboard(self) -> None:
        """Copy current content to clipboard."""
        ...
    
    def pastebin(self, s=...) -> Optional[str]:
        """Upload to a pastebin and display the URL in the status bar."""
        ...
    
    def do_pastebin(self, s) -> Optional[str]:
        """Actually perform the upload."""
        ...
    
    def push(self, s, insert_into_history=...) -> bool:
        """Push a line of code onto the buffer so it can process it all
        at once when a code block ends"""
        ...
    
    def insert_into_history(self, s: str): # -> None:
        ...
    
    def prompt_undo(self) -> int:
        """Returns how many lines to undo, 0 means don't undo"""
        ...
    
    def undo(self, n: int = ...) -> None:
        """Go back in the undo history n steps and call reevaluate()
        Note that in the program this is called "Rewind" because I
        want it to be clear that this is by no means a true undo
        implementation, it is merely a convenience bonus."""
        ...
    
    def flush(self) -> None:
        """Olivier Grisel brought it to my attention that the logging
        module tries to call this method, since it makes assumptions
        about stdout that may not necessarily be true. The docs for
        sys.stdout say:

        "stdout and stderr needn't be built-in file objects: any
         object is acceptable as long as it has a write() method
         that takes a string argument."

        So I consider this to be a bug in logging, and this is a hack
        to fix it, unfortunately. I'm sure it's not the only module
        to do it."""
        ...
    
    def close(self): # -> None:
        """See the flush() method docstring."""
        ...
    
    def tokenize(self, s, newline=...) -> List[Tuple[_TokenType, str]]:
        """Tokenizes a line of code, returning pygments tokens
        with side effects/impurities:
        - reads self.cpos to see what parens should be highlighted
        - reads self.buffer to see what came before the passed in line
        - sets self.highlighted_paren to (buffer_lineno, tokens_for_that_line)
          for buffer line that should replace that line to unhighlight it,
          or None if no paren is currently highlighted
        - calls reprint_line with a buffer's line's tokens and the buffer
          lineno that has changed if line other than the current line changes
        """
        ...
    
    def clear_current_line(self) -> None:
        """This is used as the exception callback for the Interpreter instance.
        It prevents autoindentation from occurring after a traceback."""
        ...
    
    def send_to_external_editor(self, text: str) -> str:
        """Returns modified text from an editor, or the original text if editor
        exited with non-zero"""
        ...
    
    def open_in_external_editor(self, filename): # -> bool:
        ...
    
    def edit_config(self): # -> Literal[False] | None:
        ...
    


def next_indentation(line, tab_length) -> int:
    """Given a code line, return the indentation of the next line."""
    ...

def split_lines(tokens): # -> Generator[tuple[Any, Any] | tuple[_TokenType, Any], Any, None]:
    ...

def token_is(token_type): # -> Callable[..., bool]:
    """Return a callable object that returns whether a token is of the
    given type `token_type`."""
    ...

def token_is_any_of(token_types): # -> Callable[..., bool]:
    """Return a callable object that returns whether a token is any of the
    given types `token_types`."""
    ...

def extract_exit_value(args: Tuple[Any, ...]) -> Any:
    """Given the arguments passed to `SystemExit`, return the value that
    should be passed to `sys.exit`.
    """
    ...
