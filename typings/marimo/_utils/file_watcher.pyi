"""
This type stub file was generated by pyright.
"""

import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Coroutine

Callback = Callable[[Path], Coroutine[None, None, None]]
class FileWatcher(ABC):
    @staticmethod
    def create(path: Path, callback: Callback) -> FileWatcher:
        ...

    def __init__(self, path: Path, callback: Callback) -> None:
        ...

    async def on_file_changed(self) -> None:
        ...

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...



class PollingFileWatcher(FileWatcher):
    POLL_SECONDS = ...
    def __init__(self, path: Path, callback: Callback, loop: asyncio.AbstractEventLoop) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...
