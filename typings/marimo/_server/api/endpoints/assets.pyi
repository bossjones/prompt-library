"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from starlette.authentication import requires
from starlette.responses import FileResponse, HTMLResponse, Response
from starlette.requests import Request

if TYPE_CHECKING:
    ...
LOGGER = ...
router = ...
root = ...
config = ...
FILE_QUERY_PARAM_KEY = ...
@router.get("/")
@requires("read", redirect="auth:login_page")
async def index(request: Request) -> HTMLResponse:
    ...

STATIC_FILES = ...
@router.get("/@file/{filename_and_length:path}")
@requires("read")
def virtual_file(request: Request) -> Response:
    """
    parameters:
        - in: path
          name: filename_and_length
          required: true
          schema:
            type: string
          description: The filename and byte length of the virtual file
    responses:
        200:
            description: Get a virtual file
            content:
                application/octet-stream:
                    schema:
                        type: string
        404:
            description: Invalid virtual file request
        404:
            description: Invalid byte length in virtual file request
    """
    ...

@router.get("/{path:path}")
async def serve_static(request: Request) -> FileResponse:
    ...