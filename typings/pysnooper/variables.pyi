"""
This type stub file was generated by pyright.
"""

from . import pycompat

"""
This type stub file was generated by pyright.
"""
def needs_parentheses(source):
    ...

class BaseVariable(pycompat.ABC):
    def __init__(self, source, exclude=...) -> None:
        ...

    def items(self, frame, normalize=...):
        ...

    def __hash__(self) -> int:
        ...

    def __eq__(self, other) -> bool:
        ...



class CommonVariable(BaseVariable):
    ...


class Attrs(CommonVariable):
    ...


class Keys(CommonVariable):
    ...


class Indices(Keys):
    _slice = ...
    def __getitem__(self, item):
        ...



class Exploding(BaseVariable):
    ...
