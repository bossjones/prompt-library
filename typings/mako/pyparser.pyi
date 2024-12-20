"""
This type stub file was generated by pyright.
"""

from mako import _ast_util

"""Handles parsing of Python code.

Parsing to AST is done via _ast on Python > 2.5, otherwise the compiler
module is used.
"""
reserved = ...
arg_id = ...
def parse(code, mode=..., **exception_kwargs): # -> AST:
    """Parse an expression into AST"""
    ...

class FindIdentifiers(_ast_util.NodeVisitor):
    def __init__(self, listener, **exception_kwargs) -> None:
        ...

    def visit_ClassDef(self, node): # -> None:
        ...

    def visit_Assign(self, node): # -> None:
        ...

    def visit_ExceptHandler(self, node): # -> None:
        ...

    def visit_Lambda(self, node, *args): # -> None:
        ...

    def visit_FunctionDef(self, node): # -> None:
        ...

    def visit_ListComp(self, node): # -> None:
        ...

    visit_GeneratorExp = ...
    def visit_DictComp(self, node): # -> None:
        ...

    def visit_For(self, node): # -> None:
        ...

    def visit_Name(self, node): # -> None:
        ...

    def visit_Import(self, node): # -> None:
        ...

    def visit_ImportFrom(self, node): # -> None:
        ...



class FindTuple(_ast_util.NodeVisitor):
    def __init__(self, listener, code_factory, **exception_kwargs) -> None:
        ...

    def visit_Tuple(self, node): # -> None:
        ...



class ParseFunc(_ast_util.NodeVisitor):
    def __init__(self, listener, **exception_kwargs) -> None:
        ...

    def visit_FunctionDef(self, node): # -> None:
        ...



class ExpressionGenerator:
    def __init__(self, astnode) -> None:
        ...

    def value(self): # -> LiteralString:
        ...
