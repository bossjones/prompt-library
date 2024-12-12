"""
This type stub file was generated by pyright.
"""

from typing import Any, Optional
from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc

@mddoc
class sidebar(Html):
    """
    Displays content in a sidebar. This is a special layout component that
    will display the content in a sidebar layout, rather than below/above
    the cell.

    This component still needs to be the last expression in the cell,
    in order to display correctly.

    You may use more than one `mo.sidebar` - they will be displayed in the
    order they are called.

    **Examples.**

    ```python
    mo.sidebar(
        [
            mo.md("# marimo"),
            mo.nav_menu(
                {
                    "#home": f"{mo.icon('lucide:home')} Home",
                    "#about": f"{mo.icon('lucide:user')} About",
                    "#contact": f"{mo.icon('lucide:phone')} Contact",
                    "Links": {
                        "https://twitter.com/marimo_io": "Twitter",
                        "https://github.com/marimo-team/marimo": "GitHub",
                    },
                },
                orientation="vertical",
            ),
        ]
    )
    ```

    **Args.**

    - `item`: the content to display in the sidebar
    - `footer`: the content to display at the bottom of the sidebar

    **Returns.**

    - An `Html` object.
    """
    def __init__(self, item: object, footer: Optional[object] = ...) -> None:
        ...

    def batch(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def center(self, *args: Any, **kwargs: Any) -> Html:
        ...

    def right(self, *args: Any, **kwargs: Any) -> Html:
        ...

    def left(self, *args: Any, **kwargs: Any) -> Html:
        ...

    def callout(self, *args: Any, **kwargs: Any) -> Html:
        ...

    def style(self, *args: Any, **kwargs: Any) -> Html:
        ...
