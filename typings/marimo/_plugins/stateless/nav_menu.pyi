"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import List, Literal, Optional, Union
from marimo._output.hypertext import Html
from marimo._output.rich_help import mddoc
from marimo._plugins.core.web_component import JSONType

@mddoc
def nav_menu(menu: dict[str, JSONType], *, orientation: Literal["horizontal", "vertical"] = ...) -> Html:
    """
    Navigation menu component.

    This is useful for creating a navigation menu with hyperlinks,
    most used when creating multi-page applications, with
    `marimo.create_asgi_app` ([docs](https://docs.marimo.io/guides/deploying/programmatically.html)).

    **Examples.**

    ```python
    nav_menu = mo.nav_menu(
        {
            "/overview": "Overview",
            "/sales": f"{mo.icon('lucide:shopping-cart')} Sales",
            "/products": f"{mo.icon('lucide:package')} Products",
        }
    )
    ```

    # You can also nest dictionaries to create submenus
    ```python
    nav_menu = mo.nav_menu(
        {
            "/overview": "Overview",
            "Sales": {
                "/sales": "Overview",
                "/sales/invoices": {
                    "label": "Invoices",
                    "description": "View invoices",
                },
                "/sales/customers": {
                    "label": "Customers",
                    "description": "View customers",
                },
            },
        }
    )
    ```

    **Args.**

    - `menu`: a dictionary of tab names to tab content;
        the content can also be nested dictionaries (one level deep)
        strings are interpreted as markdown

    **Returns.**

    - An `Html` object.
    """
    ...

@dataclass
class NavMenu:
    items: List[Union[NavMenuItemLink, NavMenuItemGroup]]
    ...


@dataclass
class NavMenuItemLink:
    label: str
    href: str
    description: Optional[str] = ...


@dataclass
class NavMenuItemGroup:
    label: str
    items: List[NavMenuItemLink]
    ...