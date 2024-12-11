"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import Any, Callable, Literal, Optional, Union
from xml.etree.ElementTree import Element
from markdown import Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from marimo._ast.app import App, _AppConfig
from marimo._ast.cell import CellConfig

MARIMO_MD = ...
MARIMO_CODE = ...
ConvertKeys = Union[Literal["marimo"], Literal["marimo-app"]]
def formatted_code_block(code: str, attributes: Optional[dict[str, str]] = ...) -> str:
    """Wraps code in a fenced code block with marimo attributes."""
    ...

def app_config_from_root(root: Element) -> _AppConfig:
    ...

def get_source_from_tag(tag: Element) -> str:
    ...

def get_cell_config_from_tag(tag: Element, **defaults: bool) -> CellConfig:
    ...

@dataclass
class SafeWrap:
    app: App
    def strip(self) -> App:
        ...



class IdentityParser(Markdown):
    """Leaves markdown unchanged."""
    output_formats: dict[Literal["identity"], Callable[[Element], str]] = ...
    def build_parser(self) -> IdentityParser:
        """
        Creates blank registries as a base.
        """
        ...

    def convert(self, text: str) -> str:
        """Override the convert method to return the parsed text.

        Note that evoked by itself, would create an infinite loop, since
        block-parsers will never dequeue the extracted blocks.
        """
        ...



class MarimoParser(IdentityParser):
    """Parses Markdown to marimo notebook string."""
    meta: dict[str, Any]
    output_formats: dict[ConvertKeys, Callable[[Element], Union[str, App]]] = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...



class SanitizeParser(IdentityParser):
    """Sanitizes Markdown to non-executable string."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...



class FrontMatterPreprocessor(Preprocessor):
    """Preprocessor for to extract YAML front matter.

    The built-in MetaPreprocessor does not handle frontmatter yaml properly, so
    this is a custom implementation.

    Like the built-in MetaPreprocessor, this preprocessor extracts yaml and
    stores it in the Markdown's metadata attribute. Inspired by conversation
    and linked project in github/Python-Markdown/markdown/497. See docdown
    (BSD-3) or python-frontmatter (MIT) for similar implementations.
    """
    def __init__(self, md: MarimoParser) -> None:
        ...

    def run(self, lines: list[str]) -> list[str]:
        ...



class SanitizeProcessor(Preprocessor):
    """Prevent unintended executable code block injection.

    Typically run on Markdown fragments (e.g. cells) to prevent code injection.
    **Note***: Must run after SuperFencesCodeExtension.
    """
    stash: dict[str, Any]
    def run(self, lines: list[str]) -> list[str]:
        ...



class IdentityProcessor(BlockProcessor):
    """Leaves markdown unchanged."""
    def test(*_args: Any) -> bool:
        ...

    def run(self, parent: Element, blocks: list[str]) -> None:
        ...



class ExpandAndClassifyProcessor(BlockProcessor):
    """Separates code blocks and markdown blocks."""
    stash: dict[str, Any]
    def test(*_args: Any) -> bool:
        ...

    def run(self, parent: Element, blocks: list[str]) -> None:
        ...



def convert_from_md_to_app(text: str) -> App:
    ...

def convert_from_md(text: str) -> str:
    ...

def sanitize_markdown(text: str) -> str:
    ...

def is_sanitized_markdown(text: str) -> bool:
    ...