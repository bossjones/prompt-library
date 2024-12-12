"""
This type stub file was generated by pyright.
"""

import abc
from contextlib import contextmanager
from typing import Generator, List, Optional, TYPE_CHECKING
from marimo._config.config import WidthType
from marimo._server.file_manager import AppFileManager
from marimo._server.models.files import FileInfo
from marimo._server.models.home import MarimoFile
from marimo._utils.marimo_path import MarimoPath

if TYPE_CHECKING:
    ...
LOGGER = ...
MarimoFileKey = str
class AppFileRouter(abc.ABC):
    """
    Abstract class for routing files to an AppFileManager.
    """
    NEW_FILE: MarimoFileKey = ...
    @property
    def directory(self) -> str | None:
        ...

    @staticmethod
    def infer(path: str) -> AppFileRouter:
        ...

    @staticmethod
    def from_filename(file: MarimoPath) -> AppFileRouter:
        ...

    @staticmethod
    def from_directory(directory: str) -> AppFileRouter:
        ...

    @staticmethod
    def from_files(files: List[MarimoFile]) -> AppFileRouter:
        ...

    @staticmethod
    def new_file() -> AppFileRouter:
        ...

    def get_single_app_file_manager(self, default_width: WidthType | None = ...) -> AppFileManager:
        ...

    def get_file_manager(self, key: MarimoFileKey, default_width: WidthType | None = ...) -> AppFileManager:
        """
        Given a key, return an AppFileManager.
        """
        ...

    @abc.abstractmethod
    def get_unique_file_key(self) -> Optional[MarimoFileKey]:
        """
        If there is a unique file key, return it. Otherwise, return None.
        """
        ...

    @abc.abstractmethod
    def maybe_get_single_file(self) -> Optional[MarimoFile]:
        """
        If there is a single file, return it. Otherwise, return None.
        """
        ...

    @property
    @abc.abstractmethod
    def files(self) -> List[FileInfo]:
        """
        Get all files in a recursive tree.
        """
        ...



class NewFileAppFileRouter(AppFileRouter):
    def get_unique_file_key(self) -> Optional[MarimoFileKey]:
        ...

    def maybe_get_single_file(self) -> Optional[MarimoFile]:
        ...

    @property
    def files(self) -> List[FileInfo]:
        ...



class ListOfFilesAppFileRouter(AppFileRouter):
    def __init__(self, files: List[MarimoFile]) -> None:
        ...

    @property
    def files(self) -> List[FileInfo]:
        ...

    def get_unique_file_key(self) -> Optional[MarimoFileKey]:
        ...

    def maybe_get_single_file(self) -> Optional[MarimoFile]:
        ...



class LazyListOfFilesAppFileRouter(AppFileRouter):
    def __init__(self, directory: str, include_markdown: bool) -> None:
        ...

    @property
    def directory(self) -> str:
        ...

    def toggle_markdown(self, include_markdown: bool) -> LazyListOfFilesAppFileRouter:
        ...

    def mark_stale(self) -> None:
        ...

    @property
    def files(self) -> List[FileInfo]:
        ...

    def get_unique_file_key(self) -> str | None:
        ...

    def maybe_get_single_file(self) -> MarimoFile | None:
        ...



@contextmanager
def timeout(seconds: int, message: str) -> Generator[None, None, None]:
    ...
