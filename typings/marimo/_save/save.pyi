"""
This type stub file was generated by pyright.
"""

import ast
from typing import Any, Callable, Optional, TYPE_CHECKING, Type
from marimo._runtime.state import State
from marimo._save.loaders import Loader, MemoryLoader
from types import TracebackType
from typing_extensions import Self
from marimo._runtime.dataflow import DirectedGraph

UNEXPECTED_FAILURE_BOILERPLATE = ...
if TYPE_CHECKING:
    ...
class SkipWithBlock(Exception):
    """Special exception to get around executing the with block body."""
    ...


class _cache_base:
    """Like functools.cache but notebook-aware. See `cache` docstring`"""
    graph: DirectedGraph
    cell_id: str
    module: ast.Module
    _args: list[str]
    _loader: Optional[State[MemoryLoader]] = ...
    name: str
    fn: Optional[Callable[..., Any]]
    def __init__(self, _fn: Optional[Callable[..., Any]] = ..., *, maxsize: int = ..., pin_modules: bool = ..., hash_type: str = ..., frame_offset: int = ...) -> None:
        ...

    @property
    def hits(self) -> int:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...



def cache(_fn: Optional[Callable[..., Any]] = ..., *, pin_modules: bool = ...) -> _cache_base:
    """Cache the value of a function based on args and closed-over variables.

    Decorating a function with `@mo.cache` will cache its value based on
    the function's arguments, closed-over values, and the notebook code.

    **Usage.**

    ```python
    import marimo as mo


    @mo.cache
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    ```

    `mo.cache` is similar to `functools.cache`, but with three key benefits:

    1. `mo.cache` persists its cache even if the cell defining the
        cached function is re-run, as long as the code defining the function
        (excluding comments and formatting) has not changed.
    2. `mo.cache` keys on closed-over values in addition to function arguments,
        preventing accumulation of hidden state associated with
        `functools.cache`.
    3. `mo.cache` does not require its arguments to be
        hashable (only pickleable), meaning it can work with lists, sets, NumPy
        arrays, PyTorch tensors, and more.

    `mo.cache` obtains these benefits at the cost of slightly higher overhead
    than `functools.cache`, so it is best used for expensive functions.

    Like `functools.cache`, `mo.cache` is thread-safe.

    The cache has an unlimited maximum size. To limit the cache size, use
    `@mo.lru_cache`. `mo.cache` is slightly faster than `mo.lru_cache`, but in
    most applications the difference is negligible.

    **Args**:

    - `pin_modules`: if True, the cache will be invalidated if module versions
      differ.
    """
    ...

def lru_cache(_fn: Optional[Callable[..., Any]] = ..., *, maxsize: int = ..., pin_modules: bool = ...) -> _cache_base:
    """Decorator for LRU caching the return value of a function.

    `mo.lru_cache` is a version of `mo.cache` with a bounded cache size. As an
    LRU (Least Recently Used) cache, only the last used `maxsize` values are
    retained, with the oldest values being discarded. For more information,
    see the documentation of `mo.cache`.

    **Usage.**

    ```python
    import marimo as mo


    @mo.lru_cache
    def factorial(n):
        return n * factorial(n - 1) if n else 1
    ```

    **Args**:

    - `maxsize`: the maximum number of entries in the cache; defaults to 128.
      Setting to -1 disables cache limits.
    - `pin_modules`: if True, the cache will be invalidated if module versions
      differ.
    """
    ...

class persistent_cache:
    """Save variables to disk and restore them thereafter.

    The `mo.persistent_cache` context manager lets you delimit a block of code
    in which variables will be cached to disk when they are first computed. On
    subsequent runs of the cell, if marimo determines that this block of code
    hasn't changed and neither has its ancestors, it will restore the variables
    from disk instead of re-computing them, skipping execution of the block
    entirely.

    Restoration happens even across notebook runs, meaning you can use
    `mo.persistent_cache` to make notebooks start *instantly*, with variables
    that would otherwise be expensive to compute already materialized in
    memory.

    **Usage.**

    ```python
    with persistent_cache(name="my_cache"):
        variable = expensive_function()  # This will be cached to disk.
        print("hello, cache")  # this will be skipped on cache hits
    ```

    In this example, `variable` will be cached the first time the block
    is executed, and restored on subsequent runs of the block. If cache
    conditions are hit, the contents of `with` block will be skipped on
    execution. This means that side-effects such as writing to stdout and
    stderr will be skipped on cache hits.

    For function-level memoization, use `@mo.cache` or `@mo.lru_cache`.

    Note that `mo.state` and `UIElement` changes will also trigger cache
    invalidation, and be accordingly updated.

    **Warning.** Since context abuses sys frame trace, this may conflict with
    debugging tools or libraries that also use `sys.settrace`.

    **Args**:

    - `name`: the name of the cache, used to set saving path- to manually
      invalidate the cache, change the name.
    - `save_path`: the folder in which to save the cache, defaults to
      "__marimo__/cache" in the directory of the notebook file
    - `pin_modules`: if True, the cache will be invalidated if module versions
      differ between runs, defaults to False.
    """
    def __init__(self, name: str, *, save_path: str | None = ..., pin_modules: bool = ..., _loader: Optional[Loader] = ...) -> None:
        ...

    def __enter__(self) -> Self:
        ...

    def __exit__(self, exception: Optional[Type[BaseException]], instance: Optional[BaseException], _tracebacktype: Optional[TracebackType]) -> bool:
        ...