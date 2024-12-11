"""
This type stub file was generated by pyright.
"""

from typing import Callable, Final, Optional, Union
from marimo._output.rich_help import mddoc
from marimo._plugins.ui._core.ui_element import UIElement

@mddoc
class refresh(UIElement[int, int]):
    """
    A refresh button that will auto-refresh its descendants for a
    given interval.

    Each option value can either be a number (int or float) in seconds or a
    human-readable string (e.g. "1s", "10s", "1m").

    You can also combine multiple time units (e.g. "1m 30s").

    Note: The refresh interval may not be exact, as it depends on the
    time it takes to render the content and the time it takes to send
    the content to the client. Also, due to the buffering of UI element
    changes, if the downstream cells take a long time to render, the
    refresh interval may be longer than expected.

    **Example.**

    ```python
    refresh_button = mo.ui.refresh(
        options=["1m", "5m 30s", "10m"],
        default_interval="10m",
    )
    refresh_button
    ```

    **Attributes.**

    - `value`: The time in seconds since the refresh has been activated.

    **Initialization Args.**

    - `options`: The options for the refresh interval, as a list of
    human-readable strings or numbers (int or float) in seconds.
    If no options are provided and default_interval is provided,
    the options will be generated automatically.
    If no options are provided and default_interval is not provided,
    the refresh button will not be displayed with a dropdown for auto-refresh.
    - `default_interval`: The default value of the refresh interval.
    - `label`: optional markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    """
    name: Final[str] = ...
    def __init__(self, options: Optional[list[Union[int, float, str]]] = ..., default_interval: Optional[Union[int, float, str]] = ..., *, label: str = ..., on_change: Optional[Callable[[int], None]] = ...) -> None:
        ...