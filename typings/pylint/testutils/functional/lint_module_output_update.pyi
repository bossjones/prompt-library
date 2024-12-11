"""
This type stub file was generated by pyright.
"""

import csv
from pylint.testutils.lint_module_test import LintModuleTest

class LintModuleOutputUpdate(LintModuleTest):
    """Class to be used if expected output files should be updated instead of
    checked.
    """
    class TestDialect(csv.excel):
        """Dialect used by the csv writer."""
        delimiter = ...
        lineterminator = ...
