"""
This type stub file was generated by pyright.
"""

from typing import Optional, Union
from marimo._messaging.mimetypes import KnownMimeType

def build_data_url(mimetype: KnownMimeType, data: bytes) -> str:
    ...

def flatten_string(text: str) -> str:
    ...

def create_style(pairs: dict[str, Union[str, int, float, None]]) -> Optional[str]:
    ...

def uri_encode_component(code: str) -> str:
    """Equivalent to `encodeURIComponent` in JavaScript."""
    ...

def normalize_dimension(value: Union[int, float, str, None]) -> Optional[str]:
    """Normalize dimension value to CSS string.

    Handles:
    - Integers (converted to px)
    - Strings (passed through if they have units, converted to px if just number)
    - None (returns None)
    """
    ...
