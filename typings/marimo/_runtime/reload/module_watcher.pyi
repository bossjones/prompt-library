"""
This type stub file was generated by pyright.
"""

import threading
from typing import Callable, Literal, TYPE_CHECKING
from marimo._messaging.types import Stream
from marimo._runtime import dataflow
from marimo._runtime.reload.autoreload import ModuleReloader

if TYPE_CHECKING:
    ...
LOGGER = ...
def is_submodule(src_name: str, target_name: str) -> bool:
    """Returns True if src_name is a parent of target_name

    eg: "marimo.plugins" is a parent of "marimo.plugins.ui", returns True
    """
    ...

MODULE_WATCHER_SLEEP_INTERVAL = ...
_TEST_SLEEP_INTERVAL: float | None = ...
def watch_modules(graph: dataflow.DirectedGraph, reloader: ModuleReloader, mode: Literal["lazy", "autorun"], enqueue_run_stale_cells: Callable[[], None], should_exit: threading.Event, run_is_processed: threading.Event, stream: Stream) -> None:
    """Watches for changes to modules used by graph

    The modules used by the graph are determined statically, by analyzing the
    modules imported by the notebook as well as the modules imported by those
    modules, recursively.
    """
    ...

class ModuleWatcher:
    def __init__(self, graph: dataflow.DirectedGraph, reloader: ModuleReloader, mode: Literal["lazy", "autorun"], enqueue_run_stale_cells: Callable[[], None], stream: Stream) -> None:
        ...

    def stop(self) -> None:
        ...
