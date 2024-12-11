"""
This type stub file was generated by pyright.
"""

from collections.abc import Iterator
from functools import cached_property
from typing import Literal, NoReturn, TypeVar
from astroid import bases
from astroid.context import InferenceContext
from astroid.nodes import node_classes, scoped_nodes
from astroid.typing import InferenceResult, SuccessfulInferenceResult

"""
Inference objects are a way to represent composite AST nodes,
which are used only as inference results, so they can't be found in the
original AST tree. For instance, inferring the following frozenset use,
leads to an inferred FrozenSet:

    Call(func=Name('frozenset'), args=Tuple(...))
"""
_T = TypeVar("_T")
class FrozenSet(node_classes.BaseContainer):
    """Class representing a FrozenSet composite node."""
    def pytype(self) -> Literal["builtins.frozenset"]:
        ...



class Super(node_classes.NodeNG):
    """Proxy class over a super call.

    This class offers almost the same behaviour as Python's super,
    which is MRO lookups for retrieving attributes from the parents.

    The *mro_pointer* is the place in the MRO from where we should
    start looking, not counting it. *mro_type* is the object which
    provides the MRO, it can be both a type or an instance.
    *self_class* is the class where the super call is, while
    *scope* is the function where the super call is.
    """
    special_attributes = ...
    def __init__(self, mro_pointer: SuccessfulInferenceResult, mro_type: SuccessfulInferenceResult, self_class: scoped_nodes.ClassDef, scope: scoped_nodes.FunctionDef, call: node_classes.Call) -> None:
        ...

    def super_mro(self): # -> list[ClassDef] | Any:
        """Get the MRO which will be used to lookup attributes in this super."""
        ...

    def pytype(self) -> Literal["builtins.super"]:
        ...

    def display_type(self) -> str:
        ...

    @property
    def name(self): # -> Any:
        """Get the name of the MRO pointer."""
        ...

    def qname(self) -> Literal["super"]:
        ...

    def igetattr(self, name: str, context: InferenceContext | None = ...) -> Iterator[InferenceResult]:
        """Retrieve the inferred values of the given attribute name."""
        ...

    def getattr(self, name, context: InferenceContext | None = ...): # -> list[InferenceResult]:
        ...



class ExceptionInstance(bases.Instance):
    """Class for instances of exceptions.

    It has special treatment for some of the exceptions's attributes,
    which are transformed at runtime into certain concrete objects, such as
    the case of .args.
    """
    @cached_property
    def special_attributes(self):
        ...



class DictInstance(bases.Instance):
    """Special kind of instances for dictionaries.

    This instance knows the underlying object model of the dictionaries, which means
    that methods such as .values or .items can be properly inferred.
    """
    special_attributes = ...


class DictItems(bases.Proxy):
    __str__ = ...
    __repr__ = ...


class DictKeys(bases.Proxy):
    __str__ = ...
    __repr__ = ...


class DictValues(bases.Proxy):
    __str__ = ...
    __repr__ = ...


class PartialFunction(scoped_nodes.FunctionDef):
    """A class representing partial function obtained via functools.partial."""
    def __init__(self, call, name=..., lineno=..., col_offset=..., parent=...) -> None:
        ...

    def infer_call_result(self, caller: SuccessfulInferenceResult | None, context: InferenceContext | None = ...) -> Iterator[InferenceResult]:
        ...

    def qname(self) -> str:
        ...



class Property(scoped_nodes.FunctionDef):
    """Class representing a Python property."""
    def __init__(self, function, name=..., lineno=..., col_offset=..., parent=...) -> None:
        ...

    special_attributes = ...
    type = ...
    def pytype(self) -> Literal["builtins.property"]:
        ...

    def infer_call_result(self, caller: SuccessfulInferenceResult | None, context: InferenceContext | None = ...) -> NoReturn:
        ...
