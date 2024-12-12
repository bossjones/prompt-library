"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, Optional
from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc
from marimo._plugins.ui._core.ui_element import UIElement
from marimo._plugins.ui._impl.batch import _batch_base

"""
This type stub file was generated by pyright.
"""
@mddoc
class dictionary(_batch_base):
    """
    A dictionary of UI elements.

    Use a dictionary to

    - create a set of UI elements at runtime
    - group together logically related UI elements
    - keep the number of global variables in your program small

    Access the values of the elements using the `value` attribute of the
    dictionary.

    The elements in the dictionary can be accessed using square brackets
    (`dictionary[key]`) and embedded in other marimo outputs. You can also
    iterate over the UI elements using the same syntax used for Python dicts.

    Note: The UI elements in the dictionary are clones of the original
    elements: interacting with the dictionary will _not_ update the original
    elements, and vice versa.

    The main reason to use mo.ui.dictionary is for reactive execution — when you
    interact with an element in a mo.ui.dictionary, all cells that reference the
    mo.ui.dictionary run automatically, just like all other ui elements. When you
    use a regular dictionary, you don't get this reactivity.

    **Examples.**

    A heterogeneous collection of UI elements:

    ```python
    d = mo.ui.dictionary(
        {
            "slider": mo.ui.slider(1, 10),
            "text": mo.ui.text(),
            "date": mo.ui.date(),
        }
    )
    ```

    Get the values of the `slider`, `text`, and `date` elements via
    `d.value`:

    ```python
    # d.value returns a dict with keys "slider", "text", "date"
    d.value
    ```

    Access and output a UI element in the array:

    ```python
    mo.md(f"This is a slider: {d['slider']}")
    ```

    Some number of UI elements, determined at runtime:

    ```python
    mo.ui.dictionary(
        {
            f"option {i}": mo.ui.slider(1, 10)
            for i in range(random.randint(4, 8))
        }
    )
    ```

    Quick layouts of UI elements:

    ```python
    mo.ui.dictionary(
        {
            f"option {i}": mo.ui.slider(1, 10)
            for i in range(random.randint(4, 8))
        }
    ).vstack()  # Can also use `hstack`, `callout`, `center`, etc.
    ```

    **Attributes.**

    - `value`: a dict holding the values of the UI elements, keyed by
               their names.
    - `elements`: a dict of the wrapped elements (clones of the originals)
    - `on_change`: optional callback to run when this element's value changes

    **Initialization Args.**

    - `elements`: a dict mapping names to UI elements to include
    - `label`: a descriptive name for the dictionary
       to trigger value updates
    """
    def __init__(self, elements: dict[str, UIElement[Any, Any]], *, label: str = ..., on_change: Optional[Callable[[dict[str, object]], None]] = ...) -> None:
        ...
    
    def hstack(self, **kwargs: Any) -> Html:
        """
        Stack the elements horizontally.

        For kwargs, see `marimo.hstack`.
        """
        ...
    
    def vstack(self, **kwargs: Any) -> Html:
        """
        Stack the elements vertically.

        For kwargs, see `marimo.vstack`.
        """
        ...
    


