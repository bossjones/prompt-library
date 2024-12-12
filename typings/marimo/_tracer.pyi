"""
This type stub file was generated by pyright.
"""

from contextlib import contextmanager
from typing import Any, TYPE_CHECKING
from opentelemetry import trace

"""
This type stub file was generated by pyright.
"""
LOGGER = ...
if TYPE_CHECKING:
    ...
class MockSpan:
    @contextmanager
    def as_current_span(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def set_attribute(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def set_status(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def update_name(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def end(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def add_event(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def add_link(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def set_attributes(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def record_exception(self, *args: Any, **kwargs: Any) -> Any:
        ...
    


class MockTracer:
    @contextmanager
    def start_span(self, *args: Any, **kwargs: Any) -> Any:
        ...
    
    @contextmanager
    def start_as_current_span(self, *args: Any, **kwargs: Any) -> Any:
        ...
    


TRACE_FILENAME = ...
def create_tracer(trace_name: str) -> trace.Tracer:
    """
    Creates a tracer that logs to a file.

    This lazily loads opentelemetry.
    """
    ...

server_tracer = ...
kernel_tracer = ...
