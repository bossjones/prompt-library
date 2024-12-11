# INSPIRATION  from https://github.com/RobertCraigie/prisma-client-py/blob/da53c4280756f1a9bddc3407aa3b5f296aa8cc10/src/prisma/_types.py
# pyright: reportMissingImports=false
# pyright: reportUnusedVariable=warning
# pyright: reportUntypedBaseClass=error
# pyright: reportGeneralTypeIssues=false
# pyright: reportAttributeAccessIssue=false


"""prompt_library.types"""

from __future__ import annotations

import pathlib

from collections.abc import Callable, Coroutine, Mapping
from collections.abc import Sequence as Seq
from importlib import import_module
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    NewType,
    Protocol,
    Tuple,
    Type,
    TypeAlias,
    TypedDict,
    TypeGuard,
    TypeVar,
    Union,
    get_args,
)
from typing import runtime_checkable as runtime_checkable

import httpx
import numpy as np

from langchain_core.prompts.chat import BaseChatPromptTemplate, BaseMessage, BaseMessagePromptTemplate
from loguru import logger
from pydantic import BaseModel, Field


if TYPE_CHECKING:
    from prompt_library.gen_ai.vectorstore import ChromaDatabase, PGVectorDatabase, PineconeDatabase
    from prompt_library.models.vectorstores import ChromaIntegration, PgvectorIntegration, PineconeIntegration

    ActorInputsDb: TypeAlias = ChromaIntegration | PgvectorIntegration | PineconeIntegration
    VectorDb: TypeAlias = ChromaDatabase | PGVectorDatabase | PineconeDatabase


T = TypeVar("T")
Coro = Coroutine[Any, Any, T]


Method = Literal["GET", "POST"]

CallableT = TypeVar("CallableT", bound="FuncType")
BaseModelT = TypeVar("BaseModelT", bound=BaseModel)

# TODO: use a TypeVar everywhere
FuncType = Callable[..., object]
CoroType = Callable[..., Coroutine[Any, Any, object]]


@runtime_checkable
class InheritsGeneric(Protocol):
    __orig_bases__: tuple[_GenericAlias]


class _GenericAlias(Protocol):
    __origin__: type[object]


# NOTE: we don't support some options as their type hints are not publicly exposed
# https://github.com/encode/httpx/discussions/1977
class HttpConfig(TypedDict, total=False):
    app: Callable[[Mapping[str, Any], Any], Any]
    http1: bool
    http2: bool
    limits: httpx.Limits
    timeout: None | float | httpx.Timeout
    trust_env: bool
    max_redirects: int


SortMode = Literal["default", "insensitive"]
SortOrder = Literal["asc", "desc"]

MetricsFormat = Literal["json", "prometheus"]


class _DatasourceOverrideOptional(TypedDict, total=False):
    env: str
    name: str


class DatasourceOverride(_DatasourceOverrideOptional):
    url: str


class _DatasourceOptional(TypedDict, total=False):
    env: str


class Datasource(_DatasourceOptional):
    name: str
    url: str


TransactionId = NewType("TransactionId", str)


# Human-readable type names.
TYPES = {
    "mp3": "MP3",
    "aac": "AAC",
    "alac": "ALAC",
    "ogg": "OGG",
    "opus": "Opus",
    "flac": "FLAC",
    "ape": "APE",
    "wv": "WavPack",
    "mpc": "Musepack",
    "asf": "Windows Media",
    "aiff": "AIFF",
    "dsf": "DSD Stream File",
}

PREFERRED_IMAGE_EXTENSIONS = {"jpeg": "jpg"}


# for type hinting
# SOURCE: https://stackoverflow.com/questions/51291722/define-a-jsonable-type-using-mypy-pep-526
# SOURCE: https://github.com/python/typing/issues/182
# currently not supported by mypy
JSONType = Union[str, int, float, bool, None, dict[str, Any], list[Any]]

##########################################################
# alternative #2 json type hinting
##########################################################
# Values for JSON that aren't nested
JSON_v = Union[str, int, float, bool, None]

# If MyPy ever permits recursive definitions, just uncomment this:
# JSON = Union[List['JSON'], Mapping[str, 'JSON'], JSON_v]

# Until then, here's a multi-layer way to represent any (reasonable) JSON we
# might send or receive.  It terminates at JSON_4, so the maximum depth of
# the JSON is 5 dicts/lists, like: {'a': {'b': {'c': {'d': {'e': 'f'}}}}}.

JSON_5 = JSON_v
JSON_4 = Union[JSON_v, list[JSON_5], Mapping[str, JSON_5]]
JSON_3 = Union[JSON_v, list[JSON_4], Mapping[str, JSON_4]]
JSON_2 = Union[JSON_v, list[JSON_3], Mapping[str, JSON_3]]
JSON_1 = Union[JSON_v, list[JSON_2], Mapping[str, JSON_2]]
JSON = Union[JSON_v, list[JSON_1], Mapping[str, JSON_1]]

# To allow deeper nesting, you can of course expand the JSON definition above,
# or you can keep typechecking for the first levels but skip typechecking
# at the deepest levels by using UnsafeJSON:

UnsafeJSON_5 = Union[JSON_v, list[Any], Mapping[str, Any]]
UnsafeJSON_4 = Union[JSON_v, list[UnsafeJSON_5], Mapping[str, UnsafeJSON_5]]
UnsafeJSON_3 = Union[JSON_v, list[UnsafeJSON_4], Mapping[str, UnsafeJSON_4]]
UnsafeJSON_2 = Union[JSON_v, list[UnsafeJSON_3], Mapping[str, UnsafeJSON_3]]
UnsafeJSON_1 = Union[JSON_v, list[UnsafeJSON_2], Mapping[str, UnsafeJSON_2]]
UnsafeJSON = Union[JSON_v, list[UnsafeJSON_1], Mapping[str, UnsafeJSON_1]]
##########################################################

Pathlib = Union[str, pathlib.Path]  # typed from memory, may be wrong.

# This is a WOEFULLY inadequate stub for a duck-array type.
# Mostly, just a placeholder for the concept of needing an ArrayLike type.
# Ultimately, this should come from https://github.com/napari/image-types
# and should probably be replaced by a typing.Protocol
# note, numpy.typing.ArrayLike (in v1.20) is not quite what we want either,
# since it includes all valid arguments for np.array() ( int, float, str...)
# ArrayLike = Union[np.ndarray, 'dask.array.Array', 'zarr.Array']
ArrayLike = np.ndarray


# layer data may be: (data,) (data, meta), or (data, meta, layer_type)
# using "Any" for the data type until ArrayLike is more mature.
FullLayerData = tuple[Any, dict, str]
LayerData = Union[tuple[Any], tuple[Any, dict], FullLayerData]

PathLike = Union[str, list[str]]
ReaderFunction = Callable[[PathLike], list[LayerData]]
WriterFunction = Callable[[str, list[FullLayerData]], list[str]]

ExcInfo = Union[
    tuple[type[BaseException], BaseException, TracebackType],
    tuple[None, None, None],
]

# # Types for GUI HookSpecs
# # WidgetCallable = Callable[..., Union['FunctionGui', 'QWidget']]
# WidgetCallable = Callable[
#     ..., Union["Widget", "ScrollMenu", "CheckBoxMenu", "TextBox", "ScrollTextBlock"]
# ]
# AugmentedWidget = Union[WidgetCallable, Tuple[WidgetCallable, dict]]


# these types are mostly "intentionality" placeholders.  While it's still hard
# to use actual types to define what is acceptable data for a given layer,
# these types let us point to a concrete namespace to indicate "this data is
# intended to be (and is capable of) being turned into X layer type".
# while their names should not change (without deprecation), their typing
# implementations may... or may be rolled over to napari/image-types

if tuple(np.__version__.split(".")) < ("1", "20"):
    # this hack is because NewType doesn't allow `Any` as a base type
    # and numpy <=1.20 didn't provide type stubs for np.ndarray
    # https://github.com/python/mypy/issues/6701#issuecomment-609638202
    class ArrayBase(np.ndarray):
        def __getattr__(self, name: str) -> Any:
            # Super of 'ArrayBase' has no '__getattr__' member (no-member)
            return super().__getattr__(name)  # pylint: disable=no-member

else:
    ArrayBase = np.ndarray  # type: ignore

# SOURCE: https://github.com/napari/image-types/blob/master/imtypes/_types.py
# Base image type: an Image is just a NumPy array
AnyImage = NewType("AnyImage", np.ndarray)

# Single Channel image
Image = NewType("Image", AnyImage)


class Image2D(np.ndarray):
    """2D image type: a subtype of Image that is 2D only."""

    def __new__(cls, input_array: np.ndarray) -> Image2D:
        """Create a new Image2D instance.

        Args:
            input_array: Input numpy array

        Returns:
            Image2D: New Image2D instance
        """
        obj = np.asarray(input_array).view(cls)
        if obj.ndim != 2:
            raise ValueError(f"Expected 2D array, got {obj.ndim}D array")
        return obj


class ImageCh(np.ndarray):
    """Multichannel image type."""

    def __new__(cls, input_array: np.ndarray) -> ImageCh:
        """Create a new ImageCh instance.

        Args:
            input_array: Input numpy array

        Returns:
            ImageCh: New ImageCh instance
        """
        return np.asarray(input_array).view(cls)


class ImageCh2D(ImageCh):
    """Multichannel 2D image type: a subtype of ImageCh restricted to 3D arrays (channels, height, width)."""

    def __new__(cls, input_array: np.ndarray) -> ImageCh2D:
        """Create a new ImageCh2D instance.

        Args:
            input_array: Input numpy array

        Returns:
            ImageCh2D: New ImageCh2D instance
        """
        obj = super().__new__(cls, input_array)
        if obj.ndim != 3:
            raise ValueError(f"Expected 3D array, got {obj.ndim}D array")
        return obj


AnyImage2D = Union[Image2D, ImageCh2D]


Coords = NewType("Coords", np.ndarray)


Sigma = Union[float, Seq[float]]

Spacing = Union[float, Seq[float]]


# NOTE: https://stackoverflow.com/questions/37031928/type-annotations-for-args-and-kwargs
# NOTE: If one wants to describe specific named arguments expected in kwargs, one can instead pass in a TypedDict(which defines required and optional parameters). Optional parameters are what were the kwargs. Note: TypedDict is in python >= 3.8 See this example:
class DataCmdRequiredProps(TypedDict):
    # all of these must be present
    name: str


class DataCmdOptionalProps(TypedDict, total=False):
    # these can be included or they can be omitted
    cmd: str
    uri: str


class ReqAndOptional(DataCmdRequiredProps, DataCmdOptionalProps):
    pass


MessageLikeRepresentation = Union[
    BaseMessagePromptTemplate | BaseMessage | BaseChatPromptTemplate,
    tuple[
        str | type,
        str | list[dict] | list[object],
    ],
    str,
]


def load_type(name: str, parent_type: type | None = None) -> type:
    """Return a type from a string with a python module path"""
    module_name, class_name = name.rsplit(".", 1)
    module = import_module(module_name)
    if not hasattr(module, class_name):
        raise ValueError(f'Class "{class_name}" not found in "{module}"')
    new_class = getattr(module, class_name)
    if parent_type and not issubclass(new_class, parent_type):
        raise ValueError(f'Class "{class_name}" must extend "{parent_type}"')

    return new_class
