"""
This type stub file was generated by pyright.
"""

from typing import Optional
from marimo._ast.cell import CellConfig, CellId_t
from marimo._config.manager import MarimoConfigReader
from marimo._messaging.ops import Alert, MessageOperation
from marimo._messaging.types import KernelMessage
from marimo._runtime import requests
from marimo._runtime.requests import AppMetadata, SerializedCLIArgs, SerializedQueryParams
from marimo._server.file_manager import AppFileManager
from marimo._server.file_router import AppFileRouter, MarimoFileKey
from marimo._server.ids import ConsumerId, SessionId
from marimo._server.model import ConnectionState, SessionConsumer, SessionMode
from marimo._server.models.models import InstantiateRequest
from marimo._server.session.session_view import SessionView
from marimo._server.tokens import AuthToken
from marimo._tracer import server_tracer
from marimo._utils.disposable import Disposable
from marimo._utils.typed_connection import TypedConnection

"""Client session management

This module encapsulates session management: each client gets a unique session,
and each session wraps a Python kernel and a websocket connection through which
the kernel can send messages to the frontend. Sessions do not share kernels or
websockets.

In run mode, in which we may have many clients connected to the server, a
session is closed as soon as its websocket connection is severed. In edit mode,
in which we have at most one connected client, a session may be kept around
even if its socket is closed.
"""
LOGGER = ...
SESSION_MANAGER: Optional[SessionManager] = ...
class QueueManager:
    """Manages queues for a session."""
    def __init__(self, use_multiprocessing: bool) -> None:
        ...

    def close_queues(self) -> None:
        ...



class KernelManager:
    def __init__(self, queue_manager: QueueManager, mode: SessionMode, configs: dict[CellId_t, CellConfig], app_metadata: AppMetadata, user_config_manager: MarimoConfigReader, virtual_files_supported: bool, redirect_console_to_browser: bool = ...) -> None:
        ...

    def start_kernel(self) -> None:
        ...

    @property
    def profile_path(self) -> str | None:
        ...

    def is_alive(self) -> bool:
        ...

    def interrupt_kernel(self) -> None:
        ...

    def close_kernel(self) -> None:
        ...

    @property
    def kernel_connection(self) -> TypedConnection[KernelMessage]:
        ...



class Room:
    """
    A room is a collection of SessionConsumers
    that can be used to broadcast messages to all
    of them.
    """
    def __init__(self) -> None:
        ...

    def add_consumer(self, consumer: SessionConsumer, dispose: Disposable, consumer_id: ConsumerId, main: bool) -> None:
        ...

    def remove_consumer(self, consumer: SessionConsumer) -> None:
        ...

    def broadcast(self, operation: MessageOperation) -> None:
        ...

    def close(self) -> None:
        ...



class Session:
    """A client session.

    Each session has its own Python kernel, for editing and running the app,
    and its own websocket, for sending messages to the client.
    """
    TTL_SECONDS = ...
    @classmethod
    def create(cls, initialization_id: str, session_consumer: SessionConsumer, mode: SessionMode, app_metadata: AppMetadata, app_file_manager: AppFileManager, user_config_manager: MarimoConfigReader, virtual_files_supported: bool, redirect_console_to_browser: bool) -> Session:
        """
        Create a new session.
        """
        ...

    def __init__(self, initialization_id: str, session_consumer: SessionConsumer, queue_manager: QueueManager, kernel_manager: KernelManager, app_file_manager: AppFileManager) -> None:
        """Initialize kernel and client connection to it."""
        ...

    def try_interrupt(self) -> None:
        """Try to interrupt the kernel."""
        ...

    def put_control_request(self, request: requests.ControlRequest) -> None:
        """Put a control request in the control queue."""
        ...

    def put_completion_request(self, request: requests.CodeCompletionRequest) -> None:
        """Put a code completion request in the completion queue."""
        ...

    def put_input(self, text: str) -> None:
        """Put an input() request in the input queue."""
        ...

    def disconnect_consumer(self, session_consumer: SessionConsumer) -> None:
        """
        Stop the session consumer but keep the kernel running.

        This will disconnect the main session consumer,
        or a kiosk consumer.
        """
        ...

    def maybe_disconnect_consumer(self) -> None:
        """
        Disconnect the main session consumer if it connected.
        """
        ...

    def connect_consumer(self, session_consumer: SessionConsumer, *, main: bool) -> None:
        """
        Connect or resume the session with a new consumer.

        If its the main consumer and one already exists,
        an exception is raised.
        """
        ...

    def get_current_state(self) -> SessionView:
        """Return the current state of the session."""
        ...

    def connection_state(self) -> ConnectionState:
        """Return the connection state of the session."""
        ...

    def write_operation(self, operation: MessageOperation) -> None:
        """Write an operation to the session consumer and the session view."""
        ...

    def close(self) -> None:
        """
        Close the session.

        This will close the session consumer, kernel, and all kiosk consumers.
        """
        ...

    def instantiate(self, request: InstantiateRequest) -> None:
        """Instantiate the app."""
        ...

    def __repr__(self) -> str:
        ...



class SessionManager:
    """Mapping from client session IDs to sessions.

    Maintains a mapping from client session IDs to client sessions;
    there is exactly one session per client.

    The SessionManager also encapsulates state common to all sessions:
    - the app filename
    - the app mode (edit or run)
    - the auth token
    - the skew-protection token
    """
    def __init__(self, file_router: AppFileRouter, mode: SessionMode, development_mode: bool, quiet: bool, include_code: bool, lsp_server: LspServer, user_config_manager: MarimoConfigReader, cli_args: SerializedCLIArgs, auth_token: Optional[AuthToken], redirect_console_to_browser: bool = ...) -> None:
        ...

    def app_manager(self, key: MarimoFileKey) -> AppFileManager:
        """
        Get the app manager for the given key.
        """
        ...

    def create_session(self, session_id: SessionId, session_consumer: SessionConsumer, query_params: SerializedQueryParams, file_key: MarimoFileKey) -> Session:
        """Create a new session"""
        ...

    def get_session(self, session_id: SessionId) -> Optional[Session]:
        ...

    def get_session_by_file_key(self, file_key: MarimoFileKey) -> Optional[Session]:
        ...

    def maybe_resume_session(self, new_session_id: SessionId, file_key: MarimoFileKey) -> Optional[Session]:
        """
        Try to resume a session if one is resumable.
        If it is resumable, return the session and update the session id.
        """
        ...

    def any_clients_connected(self, key: MarimoFileKey) -> bool:
        """Returns True if at least one client has an open socket."""
        ...

    async def start_lsp_server(self) -> None:
        """Starts the lsp server if it is not already started.

        Doesn't start in run mode.
        """
        ...

    def close_session(self, session_id: SessionId) -> bool:
        ...

    def close_all_sessions(self) -> None:
        ...

    def shutdown(self) -> None:
        ...

    def should_send_code_to_frontend(self) -> bool:
        """Returns True if the server can send messages to the frontend."""
        ...

    def start_file_watcher(self) -> Disposable:
        """Starts the file watcher if it is not already started"""
        ...



class LspServer:
    def __init__(self, port: int) -> None:
        ...

    @server_tracer.start_as_current_span("lsp_server.start")
    def start(self) -> Optional[Alert]:
        ...

    def is_running(self) -> bool:
        ...

    def stop(self) -> None:
        ...



class NoopLspServer(LspServer):
    def __init__(self) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...
