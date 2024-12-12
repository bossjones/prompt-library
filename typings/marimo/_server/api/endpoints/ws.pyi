"""
This type stub file was generated by pyright.
"""

from enum import IntEnum
from typing import Callable
from starlette.websockets import WebSocket
from marimo._messaging.ops import MessageOperation
from marimo._messaging.types import KernelMessage
from marimo._server.file_router import MarimoFileKey
from marimo._server.model import ConnectionState, SessionConsumer, SessionMode
from marimo._server.sessions import SessionManager

LOGGER = ...
router = ...
SESSION_QUERY_PARAM_KEY = ...
FILE_QUERY_PARAM_KEY = ...
KIOSK_QUERY_PARAM_KEY = ...
class WebSocketCodes(IntEnum):
    ALREADY_CONNECTED = ...
    NORMAL_CLOSE = ...
    FORBIDDEN = ...


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    responses:
        200:
            description: Websocket endpoint
    """
    ...

KIOSK_ONLY_OPERATIONS = ...
KIOSK_EXCLUDED_OPERATIONS = ...
class WebsocketHandler(SessionConsumer):
    """WebSocket that sessions use to send messages to frontends.

    Each new socket gets a unique session. At most one session can exist when
    in edit mode.
    """
    def __init__(self, websocket: WebSocket, manager: SessionManager, session_id: str, mode: SessionMode, file_key: MarimoFileKey, kiosk: bool) -> None:
        ...

    async def start(self) -> None:
        ...

    def on_start(self) -> Callable[[KernelMessage], None]:
        ...

    def write_operation(self, op: MessageOperation) -> None:
        ...

    def on_stop(self) -> None:
        ...

    def connection_state(self) -> ConnectionState:
        ...



HAS_TOASTED = ...
