"""
This type stub file was generated by pyright.
"""

from . import pycompat

if pycompat.PY2:
    ...
ipython_filename_pattern = ...
ansible_filename_pattern = ...
ipykernel_filename_pattern = ...
RETURN_OPCODES = ...
def get_local_reprs(frame, watch=..., custom_repr=..., max_length=..., normalize=...): # -> OrderedDict[Any, str | Any]:
    ...

class UnavailableSource:
    def __getitem__(self, i): # -> Literal['SOURCE IS UNAVAILABLE']:
        ...



source_and_path_cache = ...
def get_path_and_source_from_frame(frame): # -> tuple[Any, list | UnavailableSource | list[str | Any] | list[str] | Any | list[bytes]]:
    ...

def get_write_function(output, overwrite): # -> Callable[..., None]:
    ...

class FileWriter:
    def __init__(self, path, overwrite) -> None:
        ...

    def write(self, s): # -> None:
        ...



thread_global = ...
DISABLED = ...
class Tracer:
    '''
    Snoop on the function, writing everything it's doing to stderr.

    This is useful for debugging.

    When you decorate a function with `@pysnooper.snoop()`
    or wrap a block of code in `with pysnooper.snoop():`, you'll get a log of
    every line that ran in the function and a play-by-play of every local
    variable that changed.

    If stderr is not easily accessible for you, you can redirect the output to
    a file::

        @pysnooper.snoop('/my/log/file.log')

    See values of some expressions that aren't local variables::

        @pysnooper.snoop(watch=('foo.bar', 'self.x["whatever"]'))

    Expand values to see all their attributes or items of lists/dictionaries:

        @pysnooper.snoop(watch_explode=('foo', 'self'))

    (see Advanced Usage in the README for more control)

    Show snoop lines for functions that your function calls::

        @pysnooper.snoop(depth=2)

    Start all snoop lines with a prefix, to grep for them easily::

        @pysnooper.snoop(prefix='ZZZ ')

    On multi-threaded apps identify which thread are snooped in output::

        @pysnooper.snoop(thread_info=True)

    Customize how values are represented as strings::

        @pysnooper.snoop(custom_repr=((type1, custom_repr_func1),
                         (condition2, custom_repr_func2), ...))

    Variables and exceptions get truncated to 100 characters by default. You
    can customize that:

        @pysnooper.snoop(max_variable_length=200)

    You can also use `max_variable_length=None` to never truncate them.

    Show timestamps relative to start time rather than wall time::

        @pysnooper.snoop(relative_time=True)

    The output is colored for easy viewing by default, except on Windows.
    Disable colors like so:

        @pysnooper.snoop(color=False)

    '''
    def __init__(self, output=..., watch=..., watch_explode=..., depth=..., prefix=..., overwrite=..., thread_info=..., custom_repr=..., max_variable_length=..., normalize=..., relative_time=..., color=...) -> None:
        ...

    def __call__(self, function_or_class): # -> type[Any] | _Wrapped[Callable[..., Any], Any, Callable[..., Any], Generator[Any, Any, None]] | _Wrapped[Callable[..., Any], Any, Callable[..., Any], Any]:
        ...

    def write(self, s): # -> None:
        ...

    def __enter__(self): # -> None:
        ...

    def __exit__(self, exc_type, exc_value, exc_traceback): # -> None:
        ...

    def set_thread_info_padding(self, thread_info):
        ...

    def trace(self, frame, event, arg):
        ...
