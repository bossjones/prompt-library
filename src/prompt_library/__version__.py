"""A module for storing version number."""

from __future__ import annotations

import sys


__version__ = "0.1.0"
__version_info__ = tuple(map(int, __version__.split(".")))

PYENV = sys.version_info
