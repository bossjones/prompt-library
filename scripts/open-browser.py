#!/usr/bin/env python
"""open-browser script opens any file inside of a browser. We will mainly use this to look at unit tests locally"""
from typing import Final
import sys
import webbrowser

URL: Final[str] = sys.argv[1]
FINAL_ADDRESS: Final[str] = f"{URL}"

print(f"FINAL_ADDRESS: {FINAL_ADDRESS}")

# Use Firefox
FIREFOX_PATH: Final[str] = "firefox"

webbrowser.get(FIREFOX_PATH).open(FINAL_ADDRESS)
