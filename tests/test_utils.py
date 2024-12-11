from __future__ import annotations

import datetime
import json
import os

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List

import pytest

from prompt_library.common.utils import (
    build_file_name_session,
    build_file_path,
    current_date_str,
    current_date_time_str,
    dict_item_diff_by_set,
    to_json_file_pretty,
)


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Fixture providing sample data for JSON serialization tests.

    Returns:
        Dict[str, Any]: A dictionary containing sample test data.
    """
    return {"name": "test", "value": 123, "nested": {"key": "value"}}


@pytest.fixture
def mock_model_object() -> Any:
    """Fixture providing a mock object with model_dump method.

    Returns:
        Any: A mock object that simulates a Pydantic-like model.
    """

    class MockModel:
        def model_dump(self) -> dict:
            return {"mock": "data"}

    return MockModel()


def test_build_file_path(tmp_path: Path) -> None:
    """Test building file path in output directory.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
    """
    test_name = "test_file"
    expected_path = os.path.join("output", test_name)
    result = build_file_path(test_name)
    assert result == expected_path
    assert os.path.dirname(result) == "output"


def test_build_file_path_with_special_chars(tmp_path: Path) -> None:
    """Test building file path with special characters.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
    """
    test_name = "test/file:with*special?chars"
    result = build_file_path(test_name)
    assert os.path.dirname(result) == "output/test"
    assert test_name in result


def test_build_file_name_session(tmp_path: Path) -> None:
    """Test building file path with session directory.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
    """
    test_name = "test_file"
    session_id = "test_session"
    expected_path = os.path.join("output", session_id, test_name)
    result = build_file_name_session(test_name, session_id)
    assert result == expected_path
    assert os.path.dirname(result) == os.path.join("output", session_id)


def test_build_file_name_session_nested(tmp_path: Path) -> None:
    """Test building file path with nested session directory.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
    """
    test_name = "test_file"
    session_id = "nested/session/dir"
    expected_path = os.path.join("output", session_id, test_name)
    result = build_file_name_session(test_name, session_id)
    assert result == expected_path
    assert os.path.dirname(result) == os.path.join("output", session_id)


def test_to_json_file_pretty(tmp_path: Path, sample_data: dict[str, Any]) -> None:
    """Test JSON file writing with pretty formatting.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
        sample_data: Fixture providing sample test data.
    """
    os.chdir(tmp_path)
    filename = "test"
    to_json_file_pretty(filename, sample_data)

    # Verify file exists and content is correct
    with open(f"{filename}.json") as f:
        content = json.load(f)
    assert content == sample_data


def test_to_json_file_pretty_list(tmp_path: Path) -> None:
    """Test JSON file writing with list data.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
    """
    os.chdir(tmp_path)
    filename = "test_list"
    test_data = [1, 2, {"key": "value"}]
    to_json_file_pretty(filename, test_data)

    with open(f"{filename}.json") as f:
        content = json.load(f)
    assert content == test_data


def test_to_json_file_pretty_with_model(tmp_path: Path, mock_model_object: Any) -> None:
    """Test JSON serialization of objects with model_dump method.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
        mock_model_object: Fixture providing a mock model object.
    """
    os.chdir(tmp_path)
    filename = "test_model"
    to_json_file_pretty(filename, {"model": mock_model_object})

    with open(f"{filename}.json") as f:
        content = json.load(f)
    assert content == {"model": {"mock": "data"}}


def test_to_json_file_pretty_invalid_object(tmp_path: Path) -> None:
    """Test JSON serialization with non-serializable object.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
    """
    os.chdir(tmp_path)
    filename = "test_invalid"

    class NonSerializable:
        pass

    with pytest.raises(TypeError) as exc_info:
        to_json_file_pretty(filename, {"invalid": NonSerializable()})
    assert "is not JSON serializable" in str(exc_info.value)


def test_current_date_time_str(monkeypatch: MonkeyPatch) -> None:
    """Test current date time string formatting.

    Args:
        monkeypatch: Pytest fixture for mocking.
    """
    mock_now = datetime.datetime(2024, 1, 1, 12, 30, 45)
    monkeypatch.setattr(datetime, "datetime", type("MockDateTime", (), {"now": lambda: mock_now}))

    result = current_date_time_str()
    assert result == "2024-01-01_12-30-45"


def test_current_date_str(monkeypatch: MonkeyPatch) -> None:
    """Test current date string formatting.

    Args:
        monkeypatch: Pytest fixture for mocking.
    """
    mock_now = datetime.datetime(2024, 1, 1, 12, 30, 45)
    monkeypatch.setattr(datetime, "datetime", type("MockDateTime", (), {"now": lambda: mock_now}))

    result = current_date_str()
    assert result == "2024-01-01"


def test_dict_item_diff_by_set() -> None:
    """Test finding differences between lists of dictionaries."""
    previous_list = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    current_list = [{"id": 2, "name": "B"}, {"id": 3, "name": "C"}]

    # Test with 'id' as the set key
    diff_ids = dict_item_diff_by_set(previous_list, current_list, "id")
    assert diff_ids == [3]

    # Test with 'name' as the set key
    diff_names = dict_item_diff_by_set(previous_list, current_list, "name")
    assert diff_names == ["C"]


def test_dict_item_diff_by_set_empty_lists() -> None:
    """Test dictionary difference with empty lists."""
    assert dict_item_diff_by_set([], [], "key") == []
    assert dict_item_diff_by_set([{"key": 1}], [], "key") == []
    assert dict_item_diff_by_set([], [{"key": 1}], "key") == [1]


def test_dict_item_diff_by_set_missing_key() -> None:
    """Test dictionary difference with missing keys."""
    previous_list = [{"id": 1}]
    current_list = [{"different_key": 2}]

    with pytest.raises(KeyError):
        dict_item_diff_by_set(previous_list, current_list, "id")
