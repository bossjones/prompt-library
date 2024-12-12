"""
This type stub file was generated by pyright.
"""

from astroid.context import CallContext, InferenceContext
from astroid.typing import InferenceResult

"""
This type stub file was generated by pyright.
"""
class CallSite:
    """Class for understanding arguments passed into a call site.

    It needs a call context, which contains the arguments and the
    keyword arguments that were passed into a given call site.
    In order to infer what an argument represents, call :meth:`infer_argument`
    with the corresponding function node and the argument name.

    :param callcontext:
        An instance of :class:`astroid.context.CallContext`, that holds
        the arguments for the call site.
    :param argument_context_map:
        Additional contexts per node, passed in from :attr:`astroid.context.Context.extra_context`
    :param context:
        An instance of :class:`astroid.context.Context`.
    """
    def __init__(self, callcontext: CallContext, argument_context_map=..., context: InferenceContext | None = ...) -> None:
        ...
    
    @classmethod
    def from_call(cls, call_node, context: InferenceContext | None = ...):
        """Get a CallSite object from the given Call node.

        context will be used to force a single inference path.
        """
        ...
    
    def has_invalid_arguments(self):
        """Check if in the current CallSite were passed *invalid* arguments.

        This can mean multiple things. For instance, if an unpacking
        of an invalid object was passed, then this method will return True.
        Other cases can be when the arguments can't be inferred by astroid,
        for example, by passing objects which aren't known statically.
        """
        ...
    
    def has_invalid_keywords(self) -> bool:
        """Check if in the current CallSite were passed *invalid* keyword arguments.

        For instance, unpacking a dictionary with integer keys is invalid
        (**{1:2}), because the keys must be strings, which will make this
        method to return True. Other cases where this might return True if
        objects which can't be inferred were passed.
        """
        ...
    
    def infer_argument(self, funcnode: InferenceResult, name: str, context: InferenceContext):
        """Infer a function argument value according to the call context."""
        ...
    


