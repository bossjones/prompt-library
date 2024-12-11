"""
This type stub file was generated by pyright.
"""

from typing import Any, TYPE_CHECKING
from marimo._ast.cell import CellId_t
from marimo._runtime.app.common import RunOutput
from marimo._runtime.requests import FunctionCallRequest, SetUIElementValueRequest
from marimo._ast.app import InternalApp
from marimo._messaging.ops import HumanReadableStatus
from marimo._plugins.core.web_component import JSONType

if TYPE_CHECKING:
    ...
class AppKernelRunner:
    """Runs an app in a kernel context; used for composition."""
    def __init__(self, app: InternalApp) -> None:
        ...

    @property
    def outputs(self) -> dict[CellId_t, Any]:
        ...

    @property
    def globals(self) -> dict[CellId_t, Any]:
        ...

    async def run(self, cells_to_run: set[CellId_t]) -> RunOutput:
        ...

    async def set_ui_element_value(self, request: SetUIElementValueRequest) -> bool:
        ...

    async def function_call(self, request: FunctionCallRequest) -> tuple[HumanReadableStatus, JSONType, bool]:
        ...