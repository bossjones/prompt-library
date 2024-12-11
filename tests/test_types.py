from __future__ import annotations

import pathlib

from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Type, Union

import numpy as np

from pydantic import BaseModel

import pytest

from prompt_library.types import (
    JSON,
    TYPES,
    AnyImage,
    AnyImage2D,
    Coords,
    DataCmdOptionalProps,
    DataCmdRequiredProps,
    ExcInfo,
    FullLayerData,
    HttpConfig,
    Image,
    Image2D,
    ImageCh,
    ImageCh2D,
    InheritsGeneric,
    JSON_v,
    LayerData,
    MessageLikeRepresentation,
    Method,
    Pathlib,
    PathLike,
    ReqAndOptional,
    Sigma,
    Spacing,
    UnsafeJSON,
    load_type,
)


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


@pytest.fixture
def sample_array() -> np.ndarray:
    """Create a sample numpy array for testing.

    Returns:
        np.ndarray: Sample array.
    """
    return np.array([[1, 2], [3, 4]])


@pytest.fixture
def sample_multichannel_array() -> np.ndarray:
    """Create a sample multichannel numpy array for testing.

    Returns:
        np.ndarray: Sample multichannel array.
    """
    return np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])


def test_image_types(sample_array: np.ndarray, sample_multichannel_array: np.ndarray) -> None:
    """Test image type definitions.

    Args:
        sample_array: Sample 2D array.
        sample_multichannel_array: Sample multichannel array.
    """
    # Test basic image types
    image: Image = Image(sample_array)
    assert isinstance(image, np.ndarray)

    image_2d: Image2D = Image2D(sample_array)
    assert isinstance(image_2d, np.ndarray)
    assert image_2d.ndim == 2

    # Test multichannel image types
    image_ch: ImageCh = ImageCh(sample_multichannel_array)
    assert isinstance(image_ch, np.ndarray)

    image_ch_2d: ImageCh2D = ImageCh2D(sample_multichannel_array[:, :, :2])
    assert isinstance(image_ch_2d, np.ndarray)
    assert image_ch_2d.ndim == 3

    # Test union types
    any_image: AnyImage = AnyImage(sample_array)
    assert isinstance(any_image, np.ndarray)

    any_image_2d: AnyImage2D = image_2d
    assert isinstance(any_image_2d, np.ndarray)
    any_image_2d = image_ch_2d
    assert isinstance(any_image_2d, np.ndarray)


def test_coords(sample_array: np.ndarray) -> None:
    """Test Coords type.

    Args:
        sample_array: Sample array.
    """
    coords: Coords = Coords(sample_array)
    assert isinstance(coords, np.ndarray)


def test_layer_data(sample_array: np.ndarray) -> None:
    """Test layer data types.

    Args:
        sample_array: Sample array.
    """
    # Test basic layer data
    layer_data: LayerData = (sample_array,)
    assert isinstance(layer_data, tuple)
    assert len(layer_data) == 1

    # Test layer data with metadata
    layer_data_meta: LayerData = (sample_array, {"key": "value"})
    assert isinstance(layer_data_meta, tuple)
    assert len(layer_data_meta) == 2

    # Test full layer data
    full_layer: FullLayerData = (sample_array, {"key": "value"}, "type")
    assert isinstance(full_layer, tuple)
    assert len(full_layer) == 3


def test_path_types() -> None:
    """Test path-related types."""
    # Test PathLike
    path_str: PathLike = "path/to/file"
    assert isinstance(path_str, str)

    path_list: PathLike = ["path1", "path2"]
    assert isinstance(path_list, list)

    # Test Pathlib
    path_str_lib: Pathlib = "path/to/file"
    assert isinstance(path_str_lib, str)

    path_obj: Pathlib = pathlib.Path("path/to/file")
    assert isinstance(path_obj, pathlib.Path)


def test_json_types() -> None:
    """Test JSON type definitions."""
    # Test basic JSON value types
    json_value: JSON_v = "string"
    assert isinstance(json_value, str)
    json_value = 123
    assert isinstance(json_value, int)
    json_value = 123.45
    assert isinstance(json_value, float)
    json_value = True
    assert isinstance(json_value, bool)
    json_value = None
    assert json_value is None

    # Test nested JSON types
    json_data: JSON = {
        "string": "value",
        "number": 123,
        "nested": {
            "list": [1, 2, 3],
            "dict": {"key": "value"},
        },
    }
    assert isinstance(json_data, dict)

    # Test unsafe JSON types
    unsafe_json: UnsafeJSON = {
        "deeply": {
            "nested": {
                "data": {
                    "beyond": {
                        "normal": "limits",
                    },
                },
            },
        },
    }
    assert isinstance(unsafe_json, dict)


def test_http_config() -> None:
    """Test HttpConfig type."""
    config: HttpConfig = {
        "http1": True,
        "http2": False,
        "trust_env": True,
        "max_redirects": 5,
    }
    assert isinstance(config, dict)
    assert "http1" in config
    assert "http2" in config


def test_data_cmd_types() -> None:
    """Test DataCmd related types."""
    # Test required props
    required: DataCmdRequiredProps = {"name": "test"}
    assert isinstance(required, dict)
    assert "name" in required

    # Test optional props
    optional: DataCmdOptionalProps = {"cmd": "test", "uri": "http://test.com"}
    assert isinstance(optional, dict)
    assert "cmd" in optional
    assert "uri" in optional

    # Test combined props
    combined: ReqAndOptional = {
        "name": "test",
        "cmd": "test",
        "uri": "http://test.com",
    }
    assert isinstance(combined, dict)
    assert "name" in combined
    assert "cmd" in combined
    assert "uri" in combined


def test_sigma_spacing_types() -> None:
    """Test Sigma and Spacing types."""
    # Test Sigma
    sigma_float: Sigma = 1.0
    assert isinstance(sigma_float, float)

    sigma_seq: Sigma = [1.0, 2.0, 3.0]
    assert isinstance(sigma_seq, (list, tuple))

    # Test Spacing
    spacing_float: Spacing = 1.0
    assert isinstance(spacing_float, float)

    spacing_seq: Spacing = [1.0, 2.0, 3.0]
    assert isinstance(spacing_seq, (list, tuple))


def test_load_type() -> None:
    """Test load_type function."""
    # Test loading a valid type
    dict_type = load_type("builtins.dict")
    assert dict_type is dict

    # Test loading with parent type check
    mapping_type = load_type("builtins.dict", Mapping)
    assert mapping_type is dict

    # Test invalid module
    with pytest.raises(ModuleNotFoundError):
        load_type("nonexistent.module.Type")

    # Test invalid class
    with pytest.raises(ValueError):
        load_type("builtins.NonexistentClass")

    # Test invalid parent type
    with pytest.raises(ValueError):
        load_type("builtins.str", dict)


def test_method_literal() -> None:
    """Test Method literal type."""
    method: Method = "GET"
    assert method == "GET"
    method = "POST"
    assert method == "POST"

    # This would fail type checking but not runtime
    # method = "INVALID"


def test_exc_info_type() -> None:
    """Test ExcInfo type."""
    # Test empty exc_info
    exc_info: ExcInfo = (None, None, None)
    assert isinstance(exc_info, tuple)
    assert all(x is None for x in exc_info)

    # Test actual exception info
    try:
        raise ValueError("test")
    except ValueError:
        import sys

        exc_info = sys.exc_info()
        assert isinstance(exc_info, tuple)
        assert len(exc_info) == 3
        assert issubclass(exc_info[0], BaseException)
        assert isinstance(exc_info[1], BaseException)


def test_message_like_representation() -> None:
    """Test MessageLikeRepresentation type."""
    # Test string representation
    msg: MessageLikeRepresentation = "test message"
    assert isinstance(msg, str)

    # Test tuple representation
    msg = ("type", "content")
    assert isinstance(msg, tuple)
    assert len(msg) == 2

    msg = ("type", [{"key": "value"}])
    assert isinstance(msg, tuple)
    assert isinstance(msg[1], list)
