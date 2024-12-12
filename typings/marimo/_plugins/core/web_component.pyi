"""
This type stub file was generated by pyright.
"""

from typing import Optional, TYPE_CHECKING, TypeVar

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
JSONType: TypeAlias = ...
S = TypeVar("S", bound=JSONType)
def build_ui_plugin(component_name: str, initial_value: Optional[JSONType], label: Optional[str], args: dict[str, JSONType], slotted_html: str = ...) -> str:
    """
    Build HTML for a UI (stateful) plugin.

    Args:
    ----
    component_name: tag name of the component
    initial_value: JSON-serializable initial value of the component
    label: markdown string that component may use a text label
    args: mapping from arg names to JSON-serializable value
    slotted_html: HTML to slot in the component

    Returns:
    -------
    HTML text for the component
    """
    ...

def build_stateless_plugin(component_name: str, args: dict[str, JSONType], slotted_html: str = ...) -> str:
    """
    Build HTML for a stateless plugin.

    Args:
    ----
    component_name: tag name of the component
    args: mapping from arg names to JSON-serializable value
    slotted_html: HTML to slot in the component

    Returns:
    -------
    HTML text for the component
    """
    ...

def parse_initial_value(text: str) -> JSONType:
    """Get initial value from HTML for a UI element."""
    ...

