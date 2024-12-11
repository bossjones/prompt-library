"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from starlette.authentication import requires
from starlette.responses import JSONResponse
from marimo._server.models.home import MarimoFile, RecentFilesResponse, RunningNotebooksResponse, WorkspaceFilesResponse
from starlette.requests import Request

if TYPE_CHECKING:
    ...
LOGGER = ...
router = ...
@router.post("/recent_files")
@requires("edit")
async def read_code(*, request: Request) -> RecentFilesResponse:
    """
    responses:
        200:
            description: Get the recent files
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/RecentFilesResponse"
    """
    ...

@router.post("/workspace_files")
@requires("edit")
async def workspace_files(*, request: Request) -> WorkspaceFilesResponse:
    """
    requestBody:
        content:
            application/json:
                schema:
                    $ref: "#/components/schemas/WorkspaceFilesRequest"
    responses:
        200:
            description: Get the files in the workspace
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/WorkspaceFilesResponse"
    """
    ...

@router.post("/running_notebooks")
@requires("edit")
async def running_notebooks(*, request: Request) -> RunningNotebooksResponse:
    """
    responses:
        200:
            description: Get the running files
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/RunningNotebooksResponse"
    """
    ...

@router.post("/shutdown_session")
@requires("edit")
async def shutdown_session(*, request: Request) -> RunningNotebooksResponse:
    """
    requestBody:
        content:
            application/json:
                schema:
                    $ref: "#/components/schemas/ShutdownSessionRequest"
    responses:
        200:
            description: Shutdown the current session
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/RunningNotebooksResponse"
    """
    ...

@router.post("/tutorial/open")
@requires("edit")
async def tutorial(*, request: Request) -> MarimoFile | JSONResponse:
    """
    requestBody:
        content:
            application/json:
                schema:
                    $ref: "#/components/schemas/OpenTutorialRequest"
    responses:
        200:
            description: Open a new tutorial
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/MarimoFile"
    """
    ...