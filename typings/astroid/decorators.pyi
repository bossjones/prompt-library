"""
This type stub file was generated by pyright.
"""

import sys
from collections.abc import Callable, Generator
from typing import ParamSpec, TypeVar
from astroid import util
from astroid.typing import InferenceResult

"""A few useful function/method decorators."""
if sys.version_info >= (3, 10):
    ...
else:
    ...
_R = TypeVar("_R")
_P = ParamSpec("_P")
def path_wrapper(func): # -> _Wrapped[Callable[..., Any], Any, Callable[..., Any], Generator[Any, None, None]]:
    """Return the given infer function wrapped to handle the path.

    Used to stop inference if the node has already been looked
    at for a given `InferenceContext` to prevent infinite recursion
    """
    ...

def yes_if_nothing_inferred(func: Callable[_P, Generator[InferenceResult]]) -> Callable[_P, Generator[InferenceResult]]:
    ...

def raise_if_nothing_inferred(func: Callable[_P, Generator[InferenceResult]]) -> Callable[_P, Generator[InferenceResult]]:
    ...

if util.check_warnings_filter():
    def deprecate_default_argument_values(astroid_version: str = ..., **arguments: str) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        """Decorator which emits a DeprecationWarning if any arguments specified
        are None or not passed at all.

        Arguments should be a key-value mapping, with the key being the argument to check
        and the value being a type annotation as string for the value of the argument.

        To improve performance, only used when DeprecationWarnings other than
        the default one are enabled.
        """
        ...

    def deprecate_arguments(astroid_version: str = ..., **arguments: str) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        """Decorator which emits a DeprecationWarning if any arguments specified
        are passed.

        Arguments should be a key-value mapping, with the key being the argument to check
        and the value being a string that explains what to do instead of passing the argument.

        To improve performance, only used when DeprecationWarnings other than
        the default one are enabled.
        """
        ...

else:
    def deprecate_default_argument_values(astroid_version: str = ..., **arguments: str) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        """Passthrough decorator to improve performance if DeprecationWarnings are
        disabled.
        """
        ...

    def deprecate_arguments(astroid_version: str = ..., **arguments: str) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        """Passthrough decorator to improve performance if DeprecationWarnings are
        disabled.
        """
        ...