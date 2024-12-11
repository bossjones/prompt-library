"""
This type stub file was generated by pyright.
"""

from typing import Dict
from marimo._ast.cell import CellId_t

LOGGER = ...
CellCodes = Dict[CellId_t, str]
class Formatter:
    def __init__(self, line_length: int) -> None:
        ...

    def format(self, codes: CellCodes) -> CellCodes:
        ...



class DefaultFormatter(Formatter):
    """
    Tries ruff, then black, then no formatting.
    """
    def format(self, codes: CellCodes) -> CellCodes:
        ...



class RuffFormatter(Formatter):
    def format(self, codes: CellCodes) -> CellCodes:
        ...



class BlackFormatter(Formatter):
    def format(self, codes: CellCodes) -> CellCodes:
        ...



class FormatError(Exception):
    ...
