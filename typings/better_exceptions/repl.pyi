"""
This type stub file was generated by pyright.
"""

from code import InteractiveConsole

REPL_ID_PREFIX = ...
repl = ...
class BetterExceptionsConsole(InteractiveConsole):
    def __init__(self) -> None:
        ...

    def runcode(self, code): # -> None:
        ...

    def runsource(self, source, loc=..., symbol=...): # -> bool:
        ...

    def showtraceback(self): # -> None:
        ...



def get_repl(): # -> BetterExceptionsConsole | None:
    ...

def interact(quiet=...): # -> None:
    ...
