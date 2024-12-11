"""
This type stub file was generated by pyright.
"""

from collections import OrderedDict
from typing import Any, Optional, TYPE_CHECKING, TypeVar
from marimo._save.cache import Cache, CacheType
from marimo._save.loaders.loader import Loader
from pathlib import Path

if TYPE_CHECKING:
    ...
T = TypeVar("T")
class MemoryLoader(Loader):
    """In memory loader for saved objects."""
    def __init__(self, *args: Any, max_size: int = ..., cache: Optional[OrderedDict[Path, Cache]] = ..., **kwargs: Any) -> None:
        ...

    def cache_hit(self, hashed_context: str, cache_type: CacheType) -> bool:
        ...

    def load_cache(self, hashed_context: str, cache_type: CacheType) -> Cache:
        ...

    def save_cache(self, cache: Cache) -> None:
        ...

    def resize(self, max_size: int) -> None:
        ...