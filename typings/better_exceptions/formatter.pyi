"""
This type stub file was generated by pyright.
"""

PIPE_CHAR = ...
CAP_CHAR = ...
THEME = ...
MAX_LENGTH = ...
def isast(v): # -> TypeIs[type[Any]] | bool:
    ...

class ExceptionFormatter:
    COMMENT_REGXP = ...
    CMDLINE_REGXP = ...
    AST_ELEMENTS = ...
    def __init__(self, colored=..., theme=..., max_length=..., pipe_char=..., cap_char=...) -> None:
        ...

    def colorize_comment(self, source): # -> str:
        ...

    def colorize_tree(self, tree, source): # -> str:
        ...

    def get_relevant_names(self, source, tree): # -> list[Name]:
        ...

    def format_value(self, v): # -> str:
        ...

    def get_relevant_values(self, source, frame, tree): # -> list[Any]:
        ...

    def split_cmdline(self, cmdline): # -> list[str]:
        ...

    def get_string_source(self): # -> str:
        ...

    def get_traceback_information(self, tb): # -> tuple[Any | str, int, str, str | Any, str | Any, list[Any]]:
        ...

    def format_traceback_frame(self, tb): # -> tuple[tuple[Any | str, int, str, str], str | Any]:
        ...

    def format_traceback(self, tb=...): # -> tuple[str, str | Any]:
        ...

    def format_exception(self, exc, value, tb): # -> Generator[Any | str, Any, None]:
        ...