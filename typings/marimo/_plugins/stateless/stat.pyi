"""
This type stub file was generated by pyright.
"""

from typing import Literal, Optional, Union
from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc

@mddoc
def stat(value: Union[str, int, float], label: Optional[str] = ..., caption: Optional[str] = ..., direction: Optional[Literal["increase", "decrease"]] = ..., bordered: bool = ...) -> Html:
    """Display a statistic.

    Optionally include a label, caption, and direction.

    **Args.**

    - `value`: the value to display
    - `label`: the label to display
    - `caption`: the caption to display
    - `direction`: the direction of the statistic,
        either `increase` or `decrease`
    - `bordered`: whether to display a border around the statistic

    **Returns.**

    An `Html` object representing the statistic.
    """
    ...
