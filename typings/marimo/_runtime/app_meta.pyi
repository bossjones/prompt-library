"""
This type stub file was generated by pyright.
"""

from typing import Literal, Optional

class AppMeta:
    """
    Metadata about the app.

    This class provides access to runtime metadata about a marimo app, such as
    its display theme and execution mode.
    """
    @property
    def theme(self) -> str:
        """The display theme of the app.

        Returns either "light" or "dark". If the user's configuration is set to
        "system", currently returns "light".

        **Examples**:

        Get the current theme and conditionally set a plotting library's theme:

        ```python
        import altair as alt

        # Enable dark theme for Altair when marimo is in dark mode
        alt.themes.enable(
            "dark" if mo.app_meta().theme == "dark" else "default"
        )
        ```

        **Returns**:

        - "light" or "dark", indicating the app's display theme
        """
        ...

    @property
    def mode(self) -> Optional[Literal["edit", "run", "script"]]:
        """The execution mode of the app.

         **Examples**:

        Show content only in edit mode:

        ```python
        # Only show this content when editing the notebook
        mo.md("# Developer Notes") if mo.app_meta().mode == "edit" else None
        ```

        **Returns**:

        - "edit": The notebook is being edited in the marimo editor
        - "run": The notebook is being run as an app
        - "script": The notebook is being run as a script
        - None: The mode could not be determined
        """
        ...