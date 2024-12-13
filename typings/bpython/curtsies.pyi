"""
This type stub file was generated by pyright.
"""

import curtsies
import curtsies.events
from .config import Config
from .curtsiesfrontend import events
from .curtsiesfrontend.interpreter import Interp
from .curtsiesfrontend.repl import BaseRepl
from typing import Any, Dict, List, Optional, Tuple, Union
from ._typing_compat import Protocol

logger = ...
class SupportsEventGeneration(Protocol):
    def send(self, timeout: Optional[float]) -> Union[str, curtsies.events.Event, None]:
        ...
    
    def __iter__(self) -> SupportsEventGeneration:
        ...
    
    def __next__(self) -> Union[str, curtsies.events.Event, None]:
        ...
    


class FullCurtsiesRepl(BaseRepl):
    def __init__(self, config: Config, locals_: Optional[Dict[str, Any]] = ..., banner: Optional[str] = ..., interp: Optional[Interp] = ...) -> None:
        ...
    
    def interrupting_refresh(self) -> None:
        ...
    
    def request_undo(self, n: int = ...) -> None:
        ...
    
    def get_term_hw(self) -> Tuple[int, int]:
        ...
    
    def get_cursor_vertical_diff(self) -> int:
        ...
    
    def get_top_usable_line(self) -> int:
        ...
    
    def on_suspend(self) -> None:
        ...
    
    def after_suspend(self) -> None:
        ...
    
    def process_event_and_paint(self, e: Union[str, curtsies.events.Event, None]) -> None:
        """If None is passed in, just paint the screen"""
        ...
    
    def mainloop(self, interactive: bool = ..., paste: Optional[curtsies.events.PasteEvent] = ...) -> None:
        ...
    


def main(args: Optional[List[str]] = ..., locals_: Optional[Dict[str, Any]] = ..., banner: Optional[str] = ..., welcome_message: Optional[str] = ...) -> Any:
    """
    banner is displayed directly after the version information.
    welcome_message is passed on to Repl and displayed in the statusbar.
    """
    ...

def combined_events(event_provider: SupportsEventGeneration, paste_threshold: int = ...) -> SupportsEventGeneration:
    ...

if __name__ == "__main__":
    ...