"""
This type stub file was generated by pyright.
"""

import ast
from typing import NamedTuple
from astroid.const import Context

class FunctionType(NamedTuple):
    argtypes: list[ast.expr]
    returns: ast.expr
    ...


class ParserModule(NamedTuple):
    unary_op_classes: dict[type[ast.unaryop], str]
    cmp_op_classes: dict[type[ast.cmpop], str]
    bool_op_classes: dict[type[ast.boolop], str]
    bin_op_classes: dict[type[ast.operator], str]
    context_classes: dict[type[ast.expr_context], Context]
    def parse(self, string: str, type_comments: bool = ..., filename: str | None = ...) -> ast.Module:
        ...



def parse_function_type_comment(type_comment: str) -> FunctionType | None:
    """Given a correct type comment, obtain a FunctionType object."""
    ...

def get_parser_module(type_comments: bool = ...) -> ParserModule:
    ...