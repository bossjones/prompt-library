"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar
from pylint.reporters.ureports.base_writer import BaseWriter

"""
This type stub file was generated by pyright.
"""
_T = TypeVar("_T")
_VNodeT = TypeVar("_VNodeT", bound="VNode")
VisitLeaveFunction = Callable[[_T, Any, Any], None]
class VNode:
    def __init__(self) -> None:
        ...

    def __iter__(self) -> Iterator[VNode]:
        ...

    def accept(self: _VNodeT, visitor: BaseWriter, *args: Any, **kwargs: Any) -> None:
        ...

    def leave(self: _VNodeT, visitor: BaseWriter, *args: Any, **kwargs: Any) -> None:
        ...



class BaseLayout(VNode):
    """Base container node.

    attributes
    * children : components in this table (i.e. the table's cells)
    """
    def __init__(self, children: Iterable[Text | str] = ...) -> None:
        ...

    def append(self, child: VNode) -> None:
        """Add a node to children."""
        ...

    def insert(self, index: int, child: VNode) -> None:
        """Insert a child node."""
        ...

    def parents(self) -> list[BaseLayout]:
        """Return the ancestor nodes."""
        ...

    def add_text(self, text: str) -> None:
        """Shortcut to add text data."""
        ...



class Text(VNode):
    """A text portion.

    attributes :
    * data : the text value as an encoded or unicode string
    """
    def __init__(self, data: str, escaped: bool = ...) -> None:
        ...



class VerbatimText(Text):
    """A verbatim text, display the raw data.

    attributes :
    * data : the text value as an encoded or unicode string
    """
    ...


class Section(BaseLayout):
    """A section.

    attributes :
    * BaseLayout attributes

    a title may also be given to the constructor, it'll be added
    as a first element
    a description may also be given to the constructor, it'll be added
    as a first paragraph
    """
    def __init__(self, title: str | None = ..., description: str | None = ..., children: Iterable[Text | str] = ...) -> None:
        ...



class EvaluationSection(Section):
    def __init__(self, message: str, children: Iterable[Text | str] = ...) -> None:
        ...



class Title(BaseLayout):
    """A title.

    attributes :
    * BaseLayout attributes

    A title must not contain a section nor a paragraph!
    """
    ...


class Paragraph(BaseLayout):
    """A simple text paragraph.

    attributes :
    * BaseLayout attributes

    A paragraph must not contains a section !
    """
    ...


class Table(BaseLayout):
    """Some tabular data.

    attributes :
    * BaseLayout attributes
    * cols : the number of columns of the table (REQUIRED)
    * rheaders : the first row's elements are table's header
    * cheaders : the first col's elements are table's header
    * title : the table's optional title
    """
    def __init__(self, cols: int, title: str | None = ..., rheaders: int = ..., cheaders: int = ..., children: Iterable[Text | str] = ...) -> None:
        ...
