"""
This type stub file was generated by pyright.
"""

from collections import OrderedDict
from typing import Any, TypeVar
from astroid.context import InferenceContext
from astroid.nodes import NodeNG
from astroid.typing import InferFn, InferenceResult, TransformFn

"""
This type stub file was generated by pyright.
"""
_cache: OrderedDict[tuple[InferFn[Any], NodeNG, InferenceContext | None], list[InferenceResult]] = ...
_CURRENTLY_INFERRING: set[tuple[InferFn[Any], NodeNG]] = ...
_NodesT = TypeVar("_NodesT", bound=NodeNG)
def clear_inference_tip_cache() -> None:
    """Clear the inference tips cache."""
    ...

def inference_tip(infer_function: InferFn[_NodesT], raise_on_overwrite: bool = ...) -> TransformFn[_NodesT]:
    """Given an instance specific inference function, return a function to be
    given to AstroidManager().register_transform to set this inference function.

    :param bool raise_on_overwrite: Raise an `InferenceOverwriteError`
        if the inference tip will overwrite another. Used for debugging

    Typical usage

    .. sourcecode:: python

       AstroidManager().register_transform(Call, inference_tip(infer_named_tuple),
                                  predicate)

    .. Note::

        Using an inference tip will override
        any previously set inference tip for the given
        node. Use a predicate in the transform to prevent
        excess overwrites.
    """
    ...

