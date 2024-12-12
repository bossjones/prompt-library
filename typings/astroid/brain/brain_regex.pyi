"""
This type stub file was generated by pyright.
"""

from astroid import context, nodes
from astroid.manager import AstroidManager

CLASS_GETITEM_TEMPLATE = ...
def infer_pattern_match(node: nodes.Call, ctx: context.InferenceContext | None = ...): # -> Iterator[ClassDef]:
    """Infer regex.Pattern and regex.Match as classes.

    For PY39+ add `__class_getitem__`.
    """
    ...

def register(manager: AstroidManager) -> None:
    ...
