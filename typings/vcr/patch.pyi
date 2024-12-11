"""
This type stub file was generated by pyright.
"""

import contextlib
import http.client as httplib
import urllib3.connection as conn
import urllib3.connectionpool as cpool

"""Utilities for patching in cassettes"""
log = ...
_HTTPConnection = httplib.HTTPConnection
_HTTPSConnection = httplib.HTTPSConnection
cpool = ...
conn = ...
class CassettePatcherBuilder:
    def __init__(self, cassette) -> None:
        ...

    def build(self): # -> chain[tuple[ModuleType, Literal['HTTPConnection'], type[VCRHTTPConnection]] | tuple[ModuleType, Literal['HTTPSConnection'], type[VCRHTTPSConnection]] | _patch[dict[Any, Any] | Any] | ConnectionRemover | tuple[type[AWSHTTPConnectionPool], Literal['ConnectionCls'], type[VCRRequestsHTTPConnection]] | tuple[type[AWSHTTPSConnectionPool], Literal['ConnectionCls'], type[VCRRequestsHTTPSConnection]] | tuple[ModuleType, Literal['HTTPConnectionWithTimeout'], type[VCRHTTPConnectionWithTimeout]] | tuple[ModuleType, Literal['HTTPSConnectionWithTimeout'], type[VCRHTTPSConnectionWithTimeout]] | tuple[ModuleType, Literal['SCHEME_TO_CONNECTION'], dict[str, Any]] | tuple[Any, Literal['fetch_impl'], _Wrapped[Callable[..., Any], Any, Callable[..., Any], Any | None]] | tuple[type[ClientSession], Literal['_request'], _Wrapped[Callable[..., Any], Coroutine[Any, Any, ClientResponse], Callable[..., Any], Coroutine[Any, Any, MockClientResponse | ClientResponse]]] | tuple[type[AsyncClient], Literal['_send_single_request'], _Wrapped[Callable[..., Any], Coroutine[Any, Any, Response], Callable[..., Any], Coroutine[Any, Any, Any]]] | tuple[type[Client], Literal['_send_single_request'], _Wrapped[Callable[..., Any], Response, Callable[..., Any], Any]]]:
        ...



class ConnectionRemover:
    def __init__(self, connection_class) -> None:
        ...

    def add_connection_to_pool_entry(self, pool, connection): # -> None:
        ...

    def __enter__(self): # -> Self:
        ...

    def __exit__(self, *args): # -> None:
        ...



def reset_patchers(): # -> Generator[_patch[_HTTPConnection] | _patch[_HTTPSConnection] | _patch[_VerifiedHTTPSConnection] | _patch[_connHTTPConnection] | _patch[_cpoolBoto3HTTPConnection] | _patch[_cpoolBoto3HTTPSConnection] | _patch[_HTTPConnectionWithTimeout] | _patch[_HTTPSConnectionWithTimeout] | _patch[Any], Any, None]:
    ...

@contextlib.contextmanager
def force_reset(): # -> Generator[None, Any, None]:
    ...
