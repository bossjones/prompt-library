"""
This type stub file was generated by pyright.
"""

from typing import Literal, Optional
from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc

extension_configs = ...
MarkdownSize = Literal["sm", "base", "lg", "xl", "2xl"]
class _md(Html):
    def __init__(self, text: str, *, apply_markdown_class: bool = ..., size: Optional[MarkdownSize] = ...) -> None:
        ...



@mddoc
def md(text: str) -> Html:
    r"""Write markdown

    This function takes a string of markdown as input and returns an Html
    object. Output the object as the last expression of a cell to render
    the markdown in your app.

    **Interpolation.**

    You can interpolate Python values into your markdown strings, for example
    using f-strings. Html objects and UI elements can be directly interpolated.
    For example:

    ```python3
    text_input = mo.ui.text()
    md(f"Enter some text: {text_input}")
    ```

    For other objects, like plots, use marimo's `as_html` method to embed
    them in markdown:

    ```python3
    import matplotlib.pyplot as plt

    plt.plot([1, 2])
    axis = plt.gca()
    md(f"Here's a plot: {mo.as_html(axis)}")
    ```

    **LaTeX.**

    Enclose LaTeX in single '\$' signs for inline math, and double '\$\$' for
    display math or square brackets for display math. (Use raw strings,
    prefixed with an "r", to use single backslashes.) For example:

    ```python3
    mo.md(
        r'''
        The exponential function $f(x) = e^x$ can be represented as

        \[
            f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
        \]
        '''
    )
    ```
    renders:

    The exponential function $f(x) = e^x$ can be represented as

    $$
    f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
    $$


    **Args**:

    - `text`: a string of markdown

    **Returns**:

    - An `Html` object.
    """
    ...
