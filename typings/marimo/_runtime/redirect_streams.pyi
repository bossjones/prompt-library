"""
This type stub file was generated by pyright.
"""

import contextlib
from typing import Iterator
from marimo._ast.cell import CellId_t
from marimo._messaging.types import Stderr, Stdin, Stdout, Stream

def forward_os_stream(stream_object: Stdout | Stderr, fd: int) -> None:
    ...

def dup2newfd(fd: int) -> tuple[int, int, int]:
    """Create a pipe, with `fd` at the write end of it.

    Returns
    - duplicate (os.dup) of `fd`
    - read end of pipe
    - fd (which now points to the file referenced by the write end of the pipe)

    When done with the pipe, the write-end of the pipe should be closed
    and remapped to point to the saved duplicate. The read end should
    also be closed, as should the saved duplicate.
    """
    ...

@contextlib.contextmanager
def redirect_streams(cell_id: CellId_t, stream: Stream, stdout: Stdout | None, stderr: Stderr | None, stdin: Stdin | None) -> Iterator[None]:
    ...