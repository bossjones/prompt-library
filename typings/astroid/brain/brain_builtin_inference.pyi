"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, Union
from astroid import nodes, objects
from astroid.context import InferenceContext
from astroid.manager import AstroidManager

"""Astroid hooks for various builtins."""
if TYPE_CHECKING:
    ...
ContainerObjects = Union[objects.FrozenSet, objects.DictItems, objects.DictKeys, objects.DictValues,]
BuiltContainers = Union[type[tuple], type[list], type[set], type[frozenset],]
CopyResult = Union[nodes.Dict, nodes.List, nodes.Set, objects.FrozenSet,]
OBJECT_DUNDER_NEW = ...
STR_CLASS = ...
BYTES_CLASS = ...
def on_bootstrap(): # -> None:
    """Called by astroid_bootstrapping()."""
    ...

def register_builtin_transform(manager: AstroidManager, transform, builtin_name) -> None:
    """Register a new transform function for the given *builtin_name*.

    The transform function must accept two parameters, a node and
    an optional context.
    """
    ...

infer_tuple = ...
infer_list = ...
infer_set = ...
infer_frozenset = ...
def infer_dict(node: nodes.Call, context: InferenceContext | None = ...) -> nodes.Dict:
    """Try to infer a dict call to a Dict node.

    The function treats the following cases:

        * dict()
        * dict(mapping)
        * dict(iterable)
        * dict(iterable, **kwargs)
        * dict(mapping, **kwargs)
        * dict(**kwargs)

    If a case can't be inferred, we'll fallback to default inference.
    """
    ...

def infer_super(node: nodes.Call, context: InferenceContext | None = ...) -> objects.Super:
    """Understand super calls.

    There are some restrictions for what can be understood:

        * unbounded super (one argument form) is not understood.

        * if the super call is not inside a function (classmethod or method),
          then the default inference will be used.

        * if the super arguments can't be inferred, the default inference
          will be used.
    """
    ...

def infer_getattr(node, context: InferenceContext | None = ...): # -> UninferableBase:
    """Understand getattr calls.

    If one of the arguments is an Uninferable object, then the
    result will be an Uninferable object. Otherwise, the normal attribute
    lookup will be done.
    """
    ...

def infer_hasattr(node, context: InferenceContext | None = ...): # -> UninferableBase | Const:
    """Understand hasattr calls.

    This always guarantees three possible outcomes for calling
    hasattr: Const(False) when we are sure that the object
    doesn't have the intended attribute, Const(True) when
    we know that the object has the attribute and Uninferable
    when we are unsure of the outcome of the function call.
    """
    ...

def infer_callable(node, context: InferenceContext | None = ...): # -> UninferableBase | Const:
    """Understand callable calls.

    This follows Python's semantics, where an object
    is callable if it provides an attribute __call__,
    even though that attribute is something which can't be
    called.
    """
    ...

def infer_property(node: nodes.Call, context: InferenceContext | None = ...) -> objects.Property:
    """Understand `property` class.

    This only infers the output of `property`
    call, not the arguments themselves.
    """
    ...

def infer_bool(node, context: InferenceContext | None = ...): # -> Const | UninferableBase:
    """Understand bool calls."""
    ...

def infer_type(node, context: InferenceContext | None = ...): # -> InferenceResult | None:
    """Understand the one-argument form of *type*."""
    ...

def infer_slice(node, context: InferenceContext | None = ...): # -> Slice:
    """Understand `slice` calls."""
    ...

def infer_issubclass(callnode, context: InferenceContext | None = ...): # -> Const:
    """Infer issubclass() calls.

    :param nodes.Call callnode: an `issubclass` call
    :param InferenceContext context: the context for the inference
    :rtype nodes.Const: Boolean Const value of the `issubclass` call
    :raises UseInferenceDefault: If the node cannot be inferred
    """
    ...

def infer_isinstance(callnode: nodes.Call, context: InferenceContext | None = ...) -> nodes.Const:
    """Infer isinstance calls.

    :param nodes.Call callnode: an isinstance call
    :raises UseInferenceDefault: If the node cannot be inferred
    """
    ...

def infer_len(node, context: InferenceContext | None = ...): # -> Const:
    """Infer length calls.

    :param nodes.Call node: len call to infer
    :param context.InferenceContext: node context
    :rtype nodes.Const: a Const node with the inferred length, if possible
    """
    ...

def infer_str(node, context: InferenceContext | None = ...): # -> Const:
    """Infer str() calls.

    :param nodes.Call node: str() call to infer
    :param context.InferenceContext: node context
    :rtype nodes.Const: a Const containing an empty string
    """
    ...

def infer_int(node, context: InferenceContext | None = ...): # -> Const:
    """Infer int() calls.

    :param nodes.Call node: int() call to infer
    :param context.InferenceContext: node context
    :rtype nodes.Const: a Const containing the integer value of the int() call
    """
    ...

def infer_dict_fromkeys(node, context: InferenceContext | None = ...): # -> Dict:
    """Infer dict.fromkeys.

    :param nodes.Call node: dict.fromkeys() call to infer
    :param context.InferenceContext context: node context
    :rtype nodes.Dict:
        a Dictionary containing the values that astroid was able to infer.
        In case the inference failed for any reason, an empty dictionary
        will be inferred instead.
    """
    ...

def register(manager: AstroidManager) -> None:
    ...
