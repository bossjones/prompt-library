"""
This type stub file was generated by pyright.
"""

import sys

"""
Shim to support Python versions < 3.10 that don't have sys.stdlib_module_names

These values were created by cherry-picking the commits from
https://bugs.python.org/issue42955 into each version, but may be updated
manually if changes are needed.
"""
PY_3_7 = ...
PY_3_8 = ...
PY_3_9 = ...
if sys.version_info[: 2] == (3, 9):
    stdlib_module_names = ...
else:
    ...
