"""
This type stub file was generated by pyright.
"""

from mako import _ast_util

"""
This type stub file was generated by pyright.
"""
reserved = ...
arg_id = ...
def parse(code, mode=..., **exception_kwargs):
    """Parse an expression into AST"""
    ...

class FindIdentifiers(_ast_util.NodeVisitor):
    def __init__(self, listener, **exception_kwargs) -> None:
        ...
    
    def visit_ClassDef(self, node):
        ...
    
    def visit_Assign(self, node):
        ...
    
    def visit_ExceptHandler(self, node):
        ...
    
    def visit_Lambda(self, node, *args):
        ...
    
    def visit_FunctionDef(self, node):
        ...
    
    def visit_ListComp(self, node):
        ...
    
    visit_GeneratorExp = ...
    def visit_DictComp(self, node):
        ...
    
    def visit_For(self, node):
        ...
    
    def visit_Name(self, node):
        ...
    
    def visit_Import(self, node):
        ...
    
    def visit_ImportFrom(self, node):
        ...
    


class FindTuple(_ast_util.NodeVisitor):
    def __init__(self, listener, code_factory, **exception_kwargs) -> None:
        ...
    
    def visit_Tuple(self, node):
        ...
    


class ParseFunc(_ast_util.NodeVisitor):
    def __init__(self, listener, **exception_kwargs) -> None:
        ...
    
    def visit_FunctionDef(self, node):
        ...
    


class ExpressionGenerator:
    def __init__(self, astnode) -> None:
        ...
    
    def value(self):
        ...
    


