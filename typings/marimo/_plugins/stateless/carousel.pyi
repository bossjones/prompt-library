"""
This type stub file was generated by pyright.
"""

from typing import Sequence
from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc

@mddoc
def carousel(items: Sequence[object]) -> Html:
    """Create a carousel of items.

    **Example.**

    ```python3
    mo.carousel([mo.md("..."), mo.ui.text_area()])
    ```

    **Args.**

    - `items`: A list of items.

    **Returns.**

    - An `Html` object.
    """
    ...