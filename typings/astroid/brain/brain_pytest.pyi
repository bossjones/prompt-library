"""
This type stub file was generated by pyright.
"""

from astroid.manager import AstroidManager

"""Astroid hooks for pytest."""
def pytest_transform(): # -> Module:
    ...

def register(manager: AstroidManager) -> None:
    ...