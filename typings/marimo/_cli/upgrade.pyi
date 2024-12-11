"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import Callable, Optional
from marimo._tracer import server_tracer

FETCH_TIMEOUT = ...
@dataclass
class MarimoCLIState:
    latest_version: Optional[str] = ...
    last_checked_at: Optional[str] = ...


def print_latest_version(current_version: str, latest_version: str) -> None:
    ...

@server_tracer.start_as_current_span("check_for_updates")
def check_for_updates(on_update: Callable[[str, str], None]) -> None:
    ...