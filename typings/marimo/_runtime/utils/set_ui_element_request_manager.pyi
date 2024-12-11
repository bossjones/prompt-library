"""
This type stub file was generated by pyright.
"""

import asyncio
from typing import TYPE_CHECKING
from marimo._runtime.requests import SetUIElementValueRequest
from marimo._server.types import QueueType

if TYPE_CHECKING:
    ...
class SetUIElementRequestManager:
    def __init__(self, set_ui_element_queue: QueueType[SetUIElementValueRequest] | asyncio.Queue[SetUIElementValueRequest]) -> None:
        ...

    def process_request(self, request: SetUIElementValueRequest) -> SetUIElementValueRequest | None:
        ...
