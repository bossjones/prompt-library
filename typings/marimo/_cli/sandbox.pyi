"""
This type stub file was generated by pyright.
"""

from typing import List, Optional

LOGGER = ...
REGEX = ...
def get_dependencies_from_filename(name: str) -> List[str]:
    ...

def prompt_run_in_sandbox(name: str | None) -> bool:
    ...

def run_in_sandbox(args: List[str], name: Optional[str] = ...) -> int:
    ...
