"""
This type stub file was generated by pyright.
"""

import types
from collections.abc import Sequence
from io import TextIOWrapper
from astroid import nodes, raw_building
from astroid.const import PY312_PLUS
from astroid.manager import AstroidManager

"""The AstroidBuilder makes astroid from living object and / or from _ast.

The builder is not thread safe and can't be used to parse different sources
at the same time.
"""
_TRANSIENT_FUNCTION = ...
_STATEMENT_SELECTOR = ...
if PY312_PLUS:
    ...
def open_source_file(filename: str) -> tuple[TextIOWrapper, str, str]:
    ...

class AstroidBuilder(raw_building.InspectBuilder):
    """Class for building an astroid tree from source code or from a live module.

    The param *manager* specifies the manager class which should be used.
    If no manager is given, then the default one will be used. The
    param *apply_transforms* determines if the transforms should be
    applied after the tree was built from source or from a live object,
    by default being True.
    """
    def __init__(self, manager: AstroidManager | None = ..., apply_transforms: bool = ...) -> None:
        ...

    def module_build(self, module: types.ModuleType, modname: str | None = ...) -> nodes.Module:
        """Build an astroid from a living module instance."""
        ...

    def file_build(self, path: str, modname: str | None = ...) -> nodes.Module:
        """Build astroid from a source code file (i.e. from an ast).

        *path* is expected to be a python source file
        """
        ...

    def string_build(self, data: str, modname: str = ..., path: str | None = ...) -> nodes.Module:
        """Build astroid from source code string."""
        ...

    def add_from_names_to_locals(self, node: nodes.ImportFrom) -> None:
        """Store imported names to the locals.

        Resort the locals if coming from a delayed node
        """
        ...

    def delayed_assattr(self, node: nodes.AssignAttr) -> None:
        """Visit a AssAttr node.

        This adds name to locals and handle members definition.
        """
        ...



def build_namespace_package_module(name: str, path: Sequence[str]) -> nodes.Module:
    ...

def parse(code: str, module_name: str = ..., path: str | None = ..., apply_transforms: bool = ...) -> nodes.Module:
    """Parses a source string in order to obtain an astroid AST from it.

    :param str code: The code for the module.
    :param str module_name: The name for the module, if any
    :param str path: The path for the module
    :param bool apply_transforms:
        Apply the transforms for the give code. Use it if you
        don't want the default transforms to be applied.
    """
    ...

def extract_node(code: str, module_name: str = ...) -> nodes.NodeNG | list[nodes.NodeNG]:
    """Parses some Python code as a module and extracts a designated AST node.

    Statements:
     To extract one or more statement nodes, append #@ to the end of the line

     Examples:
       >>> def x():
       >>>   def y():
       >>>     return 1 #@

       The return statement will be extracted.

       >>> class X(object):
       >>>   def meth(self): #@
       >>>     pass

      The function object 'meth' will be extracted.

    Expressions:
     To extract arbitrary expressions, surround them with the fake
     function call __(...). After parsing, the surrounded expression
     will be returned and the whole AST (accessible via the returned
     node's parent attribute) will look like the function call was
     never there in the first place.

     Examples:
       >>> a = __(1)

       The const node will be extracted.

       >>> def x(d=__(foo.bar)): pass

       The node containing the default argument will be extracted.

       >>> def foo(a, b):
       >>>   return 0 < __(len(a)) < b

       The node containing the function call 'len' will be extracted.

    If no statements or expressions are selected, the last toplevel
    statement will be returned.

    If the selected statement is a discard statement, (i.e. an expression
    turned into a statement), the wrapped expression is returned instead.

    For convenience, singleton lists are unpacked.

    :param str code: A piece of Python code that is parsed as
    a module. Will be passed through textwrap.dedent first.
    :param str module_name: The name of the module.
    :returns: The designated node from the parse tree, or a list of nodes.
    """
    ...