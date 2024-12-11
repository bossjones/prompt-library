"""
This type stub file was generated by pyright.
"""

import argparse
from collections.abc import Callable, Sequence
from re import Pattern
from typing import Any, Literal, Union
from pylint.config.callback_actions import _CallbackAction

"""Definition of an Argument class and transformers for various argument types.

An Argument instance represents a pylint option to be handled by an argparse.ArgumentParser
"""
_ArgumentTypes = Union[str, int, float, bool, Pattern[str], Sequence[str], Sequence[Pattern[str]], tuple[int, ...],]
YES_VALUES = ...
NO_VALUES = ...
_TYPE_TRANSFORMERS: dict[str, Callable[[str], _ArgumentTypes]] = ...
class _Argument:
    """Class representing an argument to be parsed by an argparse.ArgumentsParser.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], arg_help: str, hide_help: bool, section: str | None) -> None:
        ...



class _BaseStoreArgument(_Argument):
    """Base class for store arguments to be parsed by an argparse.ArgumentsParser.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], action: str, default: _ArgumentTypes, arg_help: str, hide_help: bool, section: str | None) -> None:
        ...



class _StoreArgument(_BaseStoreArgument):
    """Class representing a store argument to be parsed by an argparse.ArgumentsParser.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], action: str, default: _ArgumentTypes, arg_type: str, choices: list[str] | None, arg_help: str, metavar: str, hide_help: bool, section: str | None) -> None:
        ...



class _StoreTrueArgument(_BaseStoreArgument):
    """Class representing a 'store_true' argument to be parsed by an
    argparse.ArgumentsParser.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], action: Literal["store_true"], default: _ArgumentTypes, arg_help: str, hide_help: bool, section: str | None) -> None:
        ...



class _DeprecationArgument(_Argument):
    """Store arguments while also handling deprecation warnings for old and new names.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], action: type[argparse.Action], default: _ArgumentTypes, arg_type: str, choices: list[str] | None, arg_help: str, metavar: str, hide_help: bool, section: str | None) -> None:
        ...



class _ExtendArgument(_DeprecationArgument):
    """Class for extend arguments to be parsed by an argparse.ArgumentsParser.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], action: Literal["extend"], default: _ArgumentTypes, arg_type: str, metavar: str, arg_help: str, hide_help: bool, section: str | None, choices: list[str] | None, dest: str | None) -> None:
        ...



class _StoreOldNamesArgument(_DeprecationArgument):
    """Store arguments while also handling old names.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], default: _ArgumentTypes, arg_type: str, choices: list[str] | None, arg_help: str, metavar: str, hide_help: bool, kwargs: dict[str, Any], section: str | None) -> None:
        ...



class _StoreNewNamesArgument(_DeprecationArgument):
    """Store arguments while also emitting deprecation warnings.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], default: _ArgumentTypes, arg_type: str, choices: list[str] | None, arg_help: str, metavar: str, hide_help: bool, kwargs: dict[str, Any], section: str | None) -> None:
        ...



class _CallableArgument(_Argument):
    """Class representing an callable argument to be parsed by an
    argparse.ArgumentsParser.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """
    def __init__(self, *, flags: list[str], action: type[_CallbackAction], arg_help: str, kwargs: dict[str, Any], hide_help: bool, section: str | None, metavar: str) -> None:
        ...