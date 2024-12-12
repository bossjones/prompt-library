"""Test for anomalous backslash escapes in strings"""

from __future__ import annotations

import glob
import importlib
import os
import re

from datetime import datetime
from pathlib import Path

import marimo
import pytz


__generated_with = "0.8.18"
app = marimo.App(width="full")  # Use full width for side-by-side comparison


@app.cell
def __():
    import os  # noqa: F811

    return (os,)


@app.cell
def __(os, unused_param):  # [unused-cell-parameter]  # noqa: F811
    result = os.path.join("/tmp")
    return (result,)


if __name__ == "__main__":
    app.run()
