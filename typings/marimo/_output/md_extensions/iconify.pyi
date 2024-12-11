"""
This type stub file was generated by pyright.
"""

import re
from typing import TYPE_CHECKING
from xml.etree.ElementTree import Element
from markdown import Extension, Markdown, inlinepatterns

if TYPE_CHECKING:
    ...
class IconifyPattern(inlinepatterns.InlineProcessor):
    """
    Converts ::icon-set:icon-name:: to an iconify-icon element.
    """
    def __init__(self, pattern: str, md: Markdown) -> None:
        ...

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[Element, int, int]:
        ...



class IconifyExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        ...