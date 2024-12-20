"""
This type stub file was generated by pyright.
"""

from mako import util

"""provides runtime services for templates, including Context,
Namespace, and various helper functions."""
class Context:
    """Provides runtime namespace, output buffer, and various
    callstacks for templates.

    See :ref:`runtime_toplevel` for detail on the usage of
    :class:`.Context`.

    """
    def __init__(self, buffer, **data) -> None:
        ...

    @property
    def lookup(self):
        """Return the :class:`.TemplateLookup` associated
        with this :class:`.Context`.

        """
        ...

    @property
    def kwargs(self): # -> dict[str, Any]:
        """Return the dictionary of top level keyword arguments associated
        with this :class:`.Context`.

        This dictionary only includes the top-level arguments passed to
        :meth:`.Template.render`.  It does not include names produced within
        the template execution such as local variable names or special names
        such as ``self``, ``next``, etc.

        The purpose of this dictionary is primarily for the case that
        a :class:`.Template` accepts arguments via its ``<%page>`` tag,
        which are normally expected to be passed via :meth:`.Template.render`,
        except the template is being called in an inheritance context,
        using the ``body()`` method.   :attr:`.Context.kwargs` can then be
        used to propagate these arguments to the inheriting template::

            ${next.body(**context.kwargs)}

        """
        ...

    def push_caller(self, caller): # -> None:
        """Push a ``caller`` callable onto the callstack for
        this :class:`.Context`."""
        ...

    def pop_caller(self): # -> None:
        """Pop a ``caller`` callable onto the callstack for this
        :class:`.Context`."""
        ...

    def keys(self): # -> list[str]:
        """Return a list of all names established in this :class:`.Context`."""
        ...

    def __getitem__(self, key): # -> Any:
        ...

    def get(self, key, default=...):
        """Return a value from this :class:`.Context`."""
        ...

    def write(self, string): # -> None:
        """Write a string to this :class:`.Context` object's
        underlying output buffer."""
        ...

    def writer(self):
        """Return the current writer function."""
        ...



class CallerStack(list):
    def __init__(self) -> None:
        ...

    def __nonzero__(self): # -> bool:
        ...

    def __bool__(self): # -> bool:
        ...

    def __getattr__(self, key): # -> Any:
        ...



class Undefined:
    """Represents an undefined value in a template.

    All template modules have a constant value
    ``UNDEFINED`` present which is an instance of this
    object.

    """
    def __str__(self) -> str:
        ...

    def __nonzero__(self): # -> Literal[False]:
        ...

    def __bool__(self): # -> Literal[False]:
        ...



UNDEFINED = ...
STOP_RENDERING = ...
class LoopStack:
    """a stack for LoopContexts that implements the context manager protocol
    to automatically pop off the top of the stack on context exit
    """
    def __init__(self) -> None:
        ...

    def __getattr__(self, key):
        ...

    def __iter__(self):
        ...



class LoopContext:
    """A magic loop variable.
    Automatically accessible in any ``% for`` block.

    See the section :ref:`loop_context` for usage
    notes.

    :attr:`parent` -> :class:`.LoopContext` or ``None``
        The parent loop, if one exists.
    :attr:`index` -> `int`
        The 0-based iteration count.
    :attr:`reverse_index` -> `int`
        The number of iterations remaining.
    :attr:`first` -> `bool`
        ``True`` on the first iteration, ``False`` otherwise.
    :attr:`last` -> `bool`
        ``True`` on the last iteration, ``False`` otherwise.
    :attr:`even` -> `bool`
        ``True`` when ``index`` is even.
    :attr:`odd` -> `bool`
        ``True`` when ``index`` is odd.
    """
    def __init__(self, iterable) -> None:
        ...

    def __iter__(self): # -> Generator[Any, Any, None]:
        ...

    @util.memoized_instancemethod
    def __len__(self): # -> int:
        ...

    @property
    def reverse_index(self): # -> int:
        ...

    @property
    def first(self): # -> bool:
        ...

    @property
    def last(self): # -> bool:
        ...

    @property
    def even(self): # -> bool:
        ...

    @property
    def odd(self): # -> bool:
        ...

    def cycle(self, *values):
        """Cycle through values as the loop progresses."""
        ...



class _NSAttr:
    def __init__(self, parent) -> None:
        ...

    def __getattr__(self, key): # -> Any:
        ...



class Namespace:
    """Provides access to collections of rendering methods, which
    can be local, from other templates, or from imported modules.

    To access a particular rendering method referenced by a
    :class:`.Namespace`, use plain attribute access:

    .. sourcecode:: mako

      ${some_namespace.foo(x, y, z)}

    :class:`.Namespace` also contains several built-in attributes
    described here.

    """
    def __init__(self, name, context, callables=..., inherits=..., populate_self=..., calling_uri=...) -> None:
        ...

    callables = ...
    module = ...
    template = ...
    context = ...
    filename = ...
    uri = ...
    _templateuri = ...
    @util.memoized_property
    def attr(self): # -> _NSAttr:
        """Access module level attributes by name.

        This accessor allows templates to supply "scalar"
        attributes which are particularly handy in inheritance
        relationships.

        .. seealso::

            :ref:`inheritance_attr`

            :ref:`namespace_attr_for_includes`

        """
        ...

    def get_namespace(self, uri): # -> TemplateNamespace:
        """Return a :class:`.Namespace` corresponding to the given ``uri``.

        If the given ``uri`` is a relative URI (i.e. it does not
        contain a leading slash ``/``), the ``uri`` is adjusted to
        be relative to the ``uri`` of the namespace itself. This
        method is therefore mostly useful off of the built-in
        ``local`` namespace, described in :ref:`namespace_local`.

        In
        most cases, a template wouldn't need this function, and
        should instead use the ``<%namespace>`` tag to load
        namespaces. However, since all ``<%namespace>`` tags are
        evaluated before the body of a template ever runs,
        this method can be used to locate namespaces using
        expressions that were generated within the body code of
        the template, or to conditionally use a particular
        namespace.

        """
        ...

    def get_template(self, uri):
        """Return a :class:`.Template` from the given ``uri``.

        The ``uri`` resolution is relative to the ``uri`` of this
        :class:`.Namespace` object's :class:`.Template`.

        """
        ...

    def get_cached(self, key, **kwargs):
        """Return a value from the :class:`.Cache` referenced by this
        :class:`.Namespace` object's :class:`.Template`.

        The advantage to this method versus direct access to the
        :class:`.Cache` is that the configuration parameters
        declared in ``<%page>`` take effect here, thereby calling
        up the same configured backend as that configured
        by ``<%page>``.

        """
        ...

    @property
    def cache(self):
        """Return the :class:`.Cache` object referenced
        by this :class:`.Namespace` object's
        :class:`.Template`.

        """
        ...

    def include_file(self, uri, **kwargs): # -> None:
        """Include a file at the given ``uri``."""
        ...

    def __getattr__(self, key): # -> tuple[()] | Any:
        ...



class TemplateNamespace(Namespace):
    """A :class:`.Namespace` specific to a :class:`.Template` instance."""
    def __init__(self, name, context, template=..., templateuri=..., callables=..., inherits=..., populate_self=..., calling_uri=...) -> None:
        ...

    @property
    def module(self):
        """The Python module referenced by this :class:`.Namespace`.

        If the namespace references a :class:`.Template`, then
        this module is the equivalent of ``template.module``,
        i.e. the generated module for the template.

        """
        ...

    @property
    def filename(self):
        """The path of the filesystem file used for this
        :class:`.Namespace`'s module or template.
        """
        ...

    @property
    def uri(self):
        """The URI for this :class:`.Namespace`'s template.

        I.e. whatever was sent to :meth:`.TemplateLookup.get_template()`.

        This is the equivalent of :attr:`.Template.uri`.

        """
        ...

    def __getattr__(self, key): # -> partial[Any] | Any:
        ...



class ModuleNamespace(Namespace):
    """A :class:`.Namespace` specific to a Python module instance."""
    def __init__(self, name, context, module, callables=..., inherits=..., populate_self=..., calling_uri=...) -> None:
        ...

    @property
    def filename(self): # -> Any:
        """The path of the filesystem file used for this
        :class:`.Namespace`'s module or template.
        """
        ...

    def __getattr__(self, key): # -> partial[Any] | Any:
        ...



def supports_caller(func): # -> Callable[..., Any]:
    """Apply a caller_stack compatibility decorator to a plain
    Python function.

    See the example in :ref:`namespaces_python_modules`.

    """
    ...

def capture(context, callable_, *args, **kwargs):
    """Execute the given template def, capturing the output into
    a buffer.

    See the example in :ref:`namespaces_python_modules`.

    """
    ...
