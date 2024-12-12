"""
This type stub file was generated by pyright.
"""

import gettext
import locale
import os.path
import sys
from typing import List, Optional, cast
from .. import package_dir

translator: gettext.NullTranslations = ...
def _(message) -> str:
    ...

def ngettext(singular, plural, n): # -> str:
    ...

def init(locale_dir: Optional[str] = ..., languages: Optional[List[str]] = ...) -> None:
    ...

