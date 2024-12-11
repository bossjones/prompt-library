"""
This type stub file was generated by pyright.
"""

from typing import List, Literal, Optional, Union
from marimo._server.files.file_system import FileSystem
from marimo._server.models.files import FileDetailsResponse, FileInfo

IGNORE_LIST = ...
DISALLOWED_NAMES = ...
class OSFileSystem(FileSystem):
    def get_root(self) -> str:
        ...

    def list_files(self, path: str) -> List[FileInfo]:
        ...

    def get_details(self, path: str, encoding: str | None = ...) -> FileDetailsResponse:
        ...

    def open_file(self, path: str, encoding: str | None = ...) -> str:
        ...

    def create_file_or_directory(self, path: str, file_type: Literal["file", "directory"], name: str, contents: Optional[bytes]) -> FileInfo:
        ...

    def delete_file_or_directory(self, path: str) -> bool:
        ...

    def move_file_or_directory(self, path: str, new_path: str) -> FileInfo:
        ...

    def update_file(self, path: str, contents: str) -> FileInfo:
        ...



def natural_sort_file(file: FileInfo) -> List[Union[int, str]]:
    ...

def natural_sort(filename: str) -> List[Union[int, str]]:
    ...