"""
This type stub file was generated by pyright.
"""

import dataclasses
from dataclasses import dataclass
from typing import Any, Callable, Dict, Final, List, Literal, Optional, Sequence, Tuple, TypeVar, Union
from marimo._data.series import DataFrameSeries
from marimo._output.rich_help import mddoc
from marimo._plugins.core.web_component import JSONType
from marimo._plugins.ui._core.ui_element import S as JSONTypeBound, UIElement
from marimo._server.models.files import FileInfo

LOGGER = ...
Numeric = Union[int, float]
@mddoc
class number(UIElement[Optional[Numeric], Optional[Numeric]]):
    """
    A number picker over an interval.

    **Example.**

    ```python
    number = mo.ui.number(start=1, stop=10, step=2)
    ```

    Or for integer-only values:

    ```python
    number = mo.ui.number(step=1)
    ```

    Or from a dataframe series:

    ```python
    number = mo.ui.number.from_series(df["column_name"])
    ```

    **Attributes.**

    - `value`: the value of the number, possibly `None`
    - `start`: the minimum value of the interval
    - `stop`: the maximum value of the interval
    - `step`: the number increment

    **Initialization Args.**

    - `start`: optional, the minimum value of the interval
    - `stop`: optional, the maximum value of the interval
    - `step`: the number increment
    - `value`: default value
    - `debounce`: whether to debounce (rate-limit) value
        updates from the frontend
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    """
    _name: Final[str] = ...
    def __init__(self, start: Optional[float] = ..., stop: Optional[float] = ..., step: Optional[float] = ..., value: Optional[float] = ..., debounce: bool = ..., *, label: str = ..., on_change: Optional[Callable[[Optional[Numeric]], None]] = ..., full_width: bool = ...) -> None:
        ...

    @staticmethod
    def from_series(series: DataFrameSeries, **kwargs: Any) -> number:
        """Create a number picker from a dataframe series."""
        ...



@mddoc
class slider(UIElement[Numeric, Numeric]):
    """
    A numeric slider over an interval.

    **Example.**

    ```python
    slider = mo.ui.slider(start=1, stop=10, step=2)
    ```

    Or from a dataframe series:

    ```python
    slider = mo.ui.slider.from_series(df["column_name"])
    ```

    Or using numpy arrays:

    ```python
    import numpy as np

    # linear steps
    steps = np.array([1, 2, 3, 4, 5])
    slider = mo.ui.slider(steps=steps)
    # log steps
    log_slider = mo.ui.slider(steps=np.logspace(0, 3, 4))
    # power steps
    power_slider = mo.ui.slider(steps=np.power([1, 2, 3], 2))
    ```

    **Attributes.**

    - `value`: the current numeric value of the slider
    - `start`: the minimum value of the interval
    - `stop`: the maximum value of the interval
    - `step`: the slider increment
    - `steps`: list of steps

    **Initialization Args.**

    - `start`: the minimum value of the interval
    - `stop`: the maximum value of the interval
    - `step`: the slider increment
    - `value`: default value
    - `debounce`: whether to debounce the slider to only send
        the value on mouse-up or drag-end
    - `orientation`: the orientation of the slider,
        either "horizontal" or "vertical"
    - `show_value`: whether to display the current value of the slider
    - `steps`: list of steps to customize the slider, mutually exclusive
        with `start`, `stop`, and `step`
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    """
    _name: Final[str] = ...
    _mapping: Optional[Dict[int, Numeric]] = ...
    def __init__(self, start: Optional[Numeric] = ..., stop: Optional[Numeric] = ..., step: Optional[Numeric] = ..., value: Optional[Numeric] = ..., debounce: bool = ..., orientation: Literal["horizontal", "vertical"] = ..., show_value: bool = ..., steps: Optional[Sequence[Numeric]] = ..., *, label: str = ..., on_change: Optional[Callable[[Optional[Numeric]], None]] = ..., full_width: bool = ...) -> None:
        ...

    @staticmethod
    def from_series(series: DataFrameSeries, **kwargs: Any) -> slider:
        """Create a slider from a dataframe series."""
        ...



@mddoc
class range_slider(UIElement[List[Numeric], Sequence[Numeric]]):
    """
    A numeric slider for specifying a range over an interval.

    **Example.**

    ```python
    range_slider = mo.ui.range_slider(start=1, stop=10, step=2, value=[2, 6])
    ```

    Or from a dataframe series:

    ```python
    range_slider = mo.ui.range_slider.from_series(df["column_name"])
    ```

    Or using numpy arrays:

    ```python
    import numpy as np

    steps = np.array([1, 2, 3, 4, 5])
    # linear steps
    range_slider = mo.ui.range_slider(steps=steps)
    # log steps
    log_range_slider = mo.ui.range_slider(steps=np.logspace(0, 3, 4))
    # power steps
    power_range_slider = mo.ui.range_slider(steps=np.power([1, 2, 3], 2))
    ```

    **Attributes.**

    - `value`: the current range value of the slider
    - `start`: the minimum value of the interval
    - `stop`: the maximum value of the interval
    - `step`: the slider increment
    - `steps`: list of steps

    **Initialization Args.**

    - `start`: the minimum value of the interval
    - `stop`: the maximum value of the interval
    - `step`: the slider increment
    - `value`: default value
    - `debounce`: whether to debounce the slider to only send
        the value on mouse-up or drag-end
    - `orientation`: the orientation of the slider,
        either "horizontal" or "vertical"
    - `show_value`: whether to display the current value of the slider
    - `steps`: list of steps to customize the slider, mutually exclusive
        with `start`, `stop`, and `step`
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    """
    _name: Final[str] = ...
    _mapping: Optional[dict[int, Numeric]] = ...
    def __init__(self, start: Optional[Numeric] = ..., stop: Optional[Numeric] = ..., step: Optional[Numeric] = ..., value: Optional[Sequence[Numeric]] = ..., debounce: bool = ..., orientation: Literal["horizontal", "vertical"] = ..., show_value: bool = ..., steps: Optional[Sequence[Numeric]] = ..., *, label: str = ..., on_change: Optional[Callable[[Sequence[Numeric]], None]] = ..., full_width: bool = ...) -> None:
        ...

    @staticmethod
    def from_series(series: DataFrameSeries, **kwargs: Any) -> range_slider:
        """Create a range slider from a dataframe series."""
        ...



@mddoc
class checkbox(UIElement[bool, bool]):
    """
    A boolean checkbox.

    **Example.**

    ```python
    checkbox = mo.ui.checkbox()
    ```

    **Attributes.**

    - `value`: a boolean, `True` if checked

    **Initialization Args.**

    - `value`: default value, True or False
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    """
    _name: Final[str] = ...
    def __init__(self, value: bool = ..., *, label: str = ..., on_change: Optional[Callable[[bool], None]] = ...) -> None:
        ...



@mddoc
class radio(UIElement[Optional[str], Any]):
    """
    A radio group.

    **Example.**

    ```python
    radiogroup = mo.ui.radio(
        options=["a", "b", "c"], value="a", label="choose one"
    )
    ```

    ```python
    radiogroup = mo.ui.radio(
        options={"one": 1, "two": 2, "three": 3},
        value="one",
        label="pick a number",
    )
    ```

    Or from a dataframe series:

    ```python
    radiogroup = mo.ui.radio.from_series(df["column_name"])
    ```

    **Attributes.**

    - `value`: the value of the selected radio option
    - `options`: a dict mapping option name to option value

    **Initialization Args.**

    - `options`: sequence of text options, or dict mapping option name
                 to option value
    - `value`: default option name, if None, starts with nothing checked
    - `label`: optional markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    """
    _name: Final[str] = ...
    def __init__(self, options: Sequence[str] | dict[str, Any], value: Optional[str] = ..., inline: bool = ..., *, label: str = ..., on_change: Optional[Callable[[Any], None]] = ...) -> None:
        ...

    @staticmethod
    def from_series(series: DataFrameSeries, **kwargs: Any) -> radio:
        """Create a radio group from a dataframe series."""
        ...



@mddoc
class text(UIElement[str, str]):
    """
    A text input.

    **Example.**

    ```python
    text = mo.ui.text(value="Hello, World!")
    ```

    **Attributes.**

    - `value`: a string of the input's contents

    **Initialization Args.**

    - `value`: default value of text box
    - `placeholder`: placeholder text to display when the text area is empty
    - `kind`: input kind, one of `"text"`, `"password"`, `"email"`, or `"url"`
        defaults to `"text"`
    - `max_length`: maximum length of input
    - `disabled`: whether the input is disabled
    - `debounce`: whether the input is debounced. If number, debounce by
        that many milliseconds. If True, then value is only emitted on Enter
        or when the input loses focus.
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    """
    _name: Final[str] = ...
    def __init__(self, value: str = ..., placeholder: str = ..., kind: Literal["text", "password", "email", "url"] = ..., max_length: Optional[int] = ..., disabled: bool = ..., debounce: bool | int = ..., *, label: str = ..., on_change: Optional[Callable[[str], None]] = ..., full_width: bool = ...) -> None:
        ...



@mddoc
class text_area(UIElement[str, str]):
    """
    A text area that is larger than `ui.text`.

    **Example.**

    ```python
    text_area = mo.ui.text_area()
    ```

    **Attributes.**

    - `value`: a string of the text area contents

    **Initialization Args.**

    - `value`: initial value of the text area
    - `placeholder`: placeholder text to display when the text area is empty
    - `max_length`: maximum length of input
    - `disabled`: whether the input is disabled
    - `debounce`: whether the input is debounced. If number, debounce by that
        many milliseconds. If True, then value is only emitted on Ctrl+Enter
        or when the input loses focus.
    - `rows`: number of rows of text to display
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    """
    _name: Final[str] = ...
    def __init__(self, value: str = ..., placeholder: str = ..., max_length: Optional[int] = ..., disabled: bool = ..., debounce: bool | int = ..., rows: Optional[int] = ..., *, label: str = ..., on_change: Optional[Callable[[str], None]] = ..., full_width: bool = ...) -> None:
        ...



@mddoc
class code_editor(UIElement[str, str]):
    """
    A code editor.

    **Example.**

    ```python
    code_editor = mo.ui.code_editor()
    ```

    **Attributes.**

    - `value`: a string of the code editor contents

    **Initialization Args.**

    - `value`: initial value of the code editor
    - `language`: language of the code editor, defaults to `"python"`; most
        major languages are supported, including "sql", "javascript",
        "typescript", "html", "css", "c", "cpp", "rust", and more
    - `placeholder`: placeholder text to display when the code editor is empty
    - `theme`: theme of the code editor, defaults to the editor's default
    - `disabled`: whether the input is disabled
    - `min_height`: minimum height of the code editor in pixels
    - `max_height`: maximum height of the code editor in pixels
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    """
    _name: Final[str] = ...
    def __init__(self, value: str = ..., language: str = ..., placeholder: str = ..., theme: Optional[Literal["light", "dark"]] = ..., disabled: bool = ..., min_height: Optional[int] = ..., max_height: Optional[int] = ..., *, label: str = ..., on_change: Optional[Callable[[str], None]] = ...) -> None:
        ...



@mddoc
class dropdown(UIElement[List[str], Any]):
    """
    A dropdown menu.

    **Example.**

    ```python
    dropdown = mo.ui.dropdown(
        options=["a", "b", "c"], value="a", label="choose one"
    )
    ```

    ```python
    dropdown = mo.ui.dropdown(
        options={"one": 1, "two": 2, "three": 3},
        value="one",
        label="pick a number",
    )
    ```

    Or from a dataframe series:

    ```python
    dropdown = mo.ui.dropdown.from_series(df["column_name"])
    ```

    **Attributes.**

    - `value`: the selected value, or `None` if no selection
    - `options`: a dict mapping option name to option value
    - `selected_key`: the selected option's key, or `None` if no selection

    **Initialization Args.**

    - `options`: sequence of text options, or dict mapping option name
                 to option value
    - `value`: default option name
    - `allow_select_none`: whether to include special option (`"--"`) for a
                           `None` value; when `None`, defaults to `True` when
                           `value` is `None`
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    """
    _MAX_OPTIONS: Final[int] = ...
    _name: Final[str] = ...
    _selected_key: Optional[str] = ...
    def __init__(self, options: Sequence[str] | dict[str, Any], value: Optional[str] = ..., allow_select_none: Optional[bool] = ..., *, label: str = ..., on_change: Optional[Callable[[Any], None]] = ..., full_width: bool = ...) -> None:
        ...

    @staticmethod
    def from_series(series: DataFrameSeries, **kwargs: Any) -> dropdown:
        """Create a dropdown from a dataframe series."""
        ...

    @property
    def selected_key(self) -> Optional[str]:
        """The selected option's key, or `None` if no selection."""
        ...



@mddoc
class multiselect(UIElement[List[str], List[object]]):
    """
    A multiselect input.

    **Example.**

    ```python
    multiselect = mo.ui.multiselect(
        options=["a", "b", "c"], label="choose some options"
    )
    ```

    Or from a dataframe series:

    ```python
    multiselect = mo.ui.multiselect.from_series(df["column_name"])
    ```

    **Attributes.**

    - `value`: the selected values, or `None` if no selection
    - `options`: a dict mapping option name to option value

    **Initialization Args.**

    - `options`: sequence of text options, or dict mapping option name
                 to option value
    - `value`: a list of initially selected options
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    - `max_selections`: maximum number of items that can be selected
    """
    _MAX_OPTIONS: Final[int] = ...
    _name: Final[str] = ...
    def __init__(self, options: Sequence[str] | dict[str, Any], value: Optional[Sequence[str]] = ..., *, label: str = ..., on_change: Optional[Callable[[List[object]], None]] = ..., full_width: bool = ..., max_selections: Optional[int] = ...) -> None:
        ...

    @staticmethod
    def from_series(series: DataFrameSeries, **kwargs: Any) -> multiselect:
        """Create a multiselect from a dataframe series."""
        ...



@mddoc
class button(UIElement[Any, Any]):
    """
    A button with an optional callback and optional value.

    **Example.**

    ```python
    # a button that when clicked will execute
    # any cells referencing that button
    button = mo.ui.button()
    ```

    ```python
    # a counter implementation
    counter_button = mo.ui.button(
        value=0, on_click=lambda value: value + 1, label="increment"
    )

    # adding intent
    delete_button = mo.ui.button(
        label="Do not click",
        kind="danger",
    )
    ```

    **Attributes.**

    - `value`: the value of the button

    **Initialization Args.**

    - `on_click`: a callable called on click that takes the current
       value of the button and returns a new value
    - `value`: an initial value for the button
    - `kind`: 'neutral', 'success', 'warn', or 'danger'
    - `disabled`: whether the button is disabled
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    - `full_width`: whether the input should take up the full width of its
        container
    - `keyboard_shortcut`: keyboard shortcut to trigger the button (e.g. 'Ctrl-L')
    """
    _name: Final[str] = ...
    def __init__(self, on_click: Optional[Callable[[Any], Any]] = ..., value: Optional[Any] = ..., kind: Literal["neutral", "success", "warn", "danger"] = ..., disabled: bool = ..., tooltip: Optional[str] = ..., *, label: str = ..., on_change: Optional[Callable[[Any], None]] = ..., full_width: bool = ..., keyboard_shortcut: Optional[str] = ...) -> None:
        ...



@dataclass
class FileUploadResults:
    """A file's name and its contents."""
    name: str
    contents: bytes
    def __repr__(self) -> str:
        ...



@mddoc
class file(UIElement[List[Tuple[str, str]], Sequence[FileUploadResults]]):
    """
    A button or drag-and-drop area to upload a file.

    Once a file is uploaded, the UI element's value is a list of
    `namedtuples (name, contents)`, where `name` is the filename and
    `contents` is the contents of the file. Alternatively, use the methods
    `name(index: int = 0)` and `contents(index: int = 0)` to retrieve the
    name or contents of the file at a specified index.

    Use the `kind` argument to switch between a button and a drag-and-drop
    area.

    The maximum file size is 100MB.

    **Examples.**

    Uploading a single file:

    ```python
    f = mo.ui.file()

    # access the uploaded file's name
    f.value[0].name
    # or
    f.name()

    # access the uploaded file's contents
    f.value[0].contents
    # or
    f.contents()
    ```

    Uploading multiple files, accepting only .png and .jpg extensions:

    ```python
    f = mo.ui.file(filetypes=[".png", ".jpg"], multiple=True)

    # access an uploaded file's name
    f.value[index].name
    # or
    f.name(index)

    # access the uploaded file's contents
    f.value[index].contents
    # or
    f.contents(index)
    ```

    **Attributes.**

    - `value`: a sequence of `FileUploadResults`, which have string `name` and
               `bytes` `contents` fields

    **Methods.**

    - `name(self, index: int = 0) -> Optional[str]`: Get the name of the
      uploaded file at `index`.
    - `contents(self, index: int = 0) -> Optional[bytes]`: Get the contents of
      the uploaded file at `index`.

    **Initialization Args.**

    - `filetypes`: the file types accepted; for example,
       `filetypes=[".png", ".jpg"]`. If `None`, all files are accepted.
       In addition to extensions, you may provide `"audio/*"`, `"video/*"`,
       or `"image/*"` to accept any audio, video, or image file.
    - `multiple`: if True, allow the user to upload multiple files
    - `kind`: `"button"` or `"area"`
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    """
    _name: Final[str] = ...
    def __init__(self, filetypes: Optional[Sequence[str]] = ..., multiple: bool = ..., kind: Literal["button", "area"] = ..., *, label: str = ..., on_change: Optional[Callable[[Sequence[FileUploadResults]], None]] = ...) -> None:
        ...

    def name(self, index: int = ...) -> Optional[str]:
        """Get file name at index."""
        ...

    def contents(self, index: int = ...) -> Optional[bytes]:
        """Get file contents at index."""
        ...



@dataclass
class ListDirectoryArgs:
    path: str
    ...


@dataclass
class ListDirectoryResponse:
    files: List[FileInfo]
    ...


@mddoc
class file_browser(UIElement[List[Dict[str, Any]], Sequence[FileInfo]]):
    """
    File browser for browsing and selecting server-side files.

    **Examples.**

    Selecting multiple files:

    ```python
    file_browser = mo.ui.file_browser(
        initial_path="path/to/dir", multiple=True
    )

    # Access the selected file path(s):
    file_browser.path(index)

    # Get name of selected file(s)
    file_browser.name(index)
    ```

    **Attributes.**

    - `value`: a sequence of file paths representing selected files.

    **Initialization Args.**

    - `initial_path`: starting directory, default current working directory.
    - `filetypes`: the file types to display in each directory; for example,
       `filetypes=[".txt", ".csv"]`. If `None`, all files are displayed.
    - `selection_mode`: either "file" or "directory".
    - `multiple`: if True, allow the user to select multiple files.
    - `restrict_navigation`: if True, prevent the user from navigating
       any level above the given path.
    - `label`: markdown label for the element
    - `on_change`: optional callback to run when this element's value changes
    """
    _name: Final[str] = ...
    def __init__(self, initial_path: str = ..., filetypes: Optional[Sequence[str]] = ..., selection_mode: str = ..., multiple: bool = ..., restrict_navigation: bool = ..., *, label: str = ..., on_change: Optional[Callable[[Sequence[FileInfo]], None]] = ...) -> None:
        ...

    def list_directory(self, args: ListDirectoryArgs) -> ListDirectoryResponse:
        ...

    def name(self, index: int = ...) -> Optional[str]:
        """Get file name at index."""
        ...

    def path(self, index: int = ...) -> Optional[str]:
        """Get file path at index."""
        ...



T = TypeVar("T")
@dataclasses.dataclass
class ValueArgs:
    value: Optional[JSONType] = ...


@mddoc
class form(UIElement[Optional[JSONTypeBound], Optional[T]]):
    """
    A submittable form linked to a UIElement.

    Use a `form` to prevent sending UI element values to Python until a button
    is clicked.

    The value of a `form` is the value of the underlying
    element the last time the form was submitted.

    **Example.**

    ```python
    # Create a form with chaining
    form = mo.ui.slider(1, 100).form()
    ```

    ```python
    # Create a form with multiple elements
    form = (
        mo.md('''
        **Your form.**

        {name}

        {date}
    ''')
        .batch(
            name=mo.ui.text(label="name"),
            date=mo.ui.date(label="date"),
        )
        .form(show_clear_button=True, bordered=False)
    )
    ```

    ```python
    # Instantiate a form directly
    form = mo.ui.form(element=mo.ui.slider(1, 100))
    ```

    **Attributes.**

    - `value`: the value of the wrapped element when the form's submit button
      was last clicked
    - `element`: a copy of the wrapped element

    **Initialization Args.**

    - `element`: the element to wrap
    - `bordered`: whether the form should have a border
    - `loading`: whether the form should be in a loading state
    - `submit_button_label`: the label of the submit button
    - `submit_button_tooltip`: the tooltip of the submit button
    - `submit_button_disabled`: whether the submit button should be disabled
    - `clear_on_submit`: whether the form should clear its contents after
        submitting
    - `show_clear_button`: whether the form should show a clear button
    - `clear_button_label`: the label of the clear button
    - `clear_button_tooltip`: the tooltip of the clear button
    - `validate`: a function that takes the form's value and returns an error
        message if the value is invalid, or `None` if the value is valid
    - `label`: markdown label for the form
    - `on_change`: optional callback to run when this element's value changes
    """
    _name: Final[str] = ...
    def __init__(self, element: UIElement[JSONTypeBound, T], *, bordered: bool = ..., loading: bool = ..., submit_button_label: str = ..., submit_button_tooltip: Optional[str] = ..., submit_button_disabled: bool = ..., clear_on_submit: bool = ..., show_clear_button: bool = ..., clear_button_label: str = ..., clear_button_tooltip: Optional[str] = ..., validate: Optional[Callable[[Optional[JSONType]], Optional[str]]] = ..., label: str = ..., on_change: Optional[Callable[[Optional[T]], None]] = ...) -> None:
        ...