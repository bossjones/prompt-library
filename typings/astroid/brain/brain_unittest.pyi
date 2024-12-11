"""
This type stub file was generated by pyright.
"""

from astroid.manager import AstroidManager

"""Astroid hooks for unittest module."""
def IsolatedAsyncioTestCaseImport(): # -> Module:
    """
    In the unittest package, the IsolatedAsyncioTestCase class is imported lazily.

    I.E. only when the ``__getattr__`` method of the unittest module is called with
    'IsolatedAsyncioTestCase' as argument. Thus the IsolatedAsyncioTestCase
    is not imported statically (during import time).
    This function mocks a classical static import of the IsolatedAsyncioTestCase.

    (see https://github.com/pylint-dev/pylint/issues/4060)
    """
    ...

def register(manager: AstroidManager) -> None:
    ...
