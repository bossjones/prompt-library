from __future__ import annotations

import json
import os

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Generator, List

from _pytest.monkeypatch import MonkeyPatch

import pytest

from prompt_library.common.prompt_library_module import (
    get_rankings,
    pull_in_dir_recursively,
    pull_in_prompt_library,
    pull_in_testable_prompts,
    record_llm_execution,
    reset_rankings,
    save_rankings,
)
from prompt_library.common.typings import ModelRanking


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture

    from pytest_mock.plugin import MockerFixture


@pytest.fixture
def temp_dir_with_files(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory with test files.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.

    Yields:
        Path: Path to the temporary directory containing test files.
    """
    # Create test files in different subdirectories
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "subdir1").mkdir()
    (tmp_path / "subdir1" / "file2.txt").write_text("content2")
    (tmp_path / "subdir1" / "subdir2").mkdir()
    (tmp_path / "subdir1" / "subdir2" / "file3.txt").write_text("content3")
    yield tmp_path


@pytest.fixture
def mock_env_paths(monkeypatch: MonkeyPatch, tmp_path: Path) -> dict[str, Path]:
    """Set up mock environment variables for file paths.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
        tmp_path: Pytest fixture providing temporary directory path.

    Returns:
        Dict[str, Path]: Dictionary mapping environment variable names to paths.
    """
    paths = {
        "PROMPT_LIBRARY_DIR": tmp_path / "prompt_lib",
        "TESTABLE_PROMPTS_DIR": tmp_path / "testable_prompts",
        "PROMPT_EXECUTIONS_DIR": tmp_path / "prompt_executions",
        "LANGUAGE_MODEL_RANKINGS_FILE": tmp_path / "rankings" / "rankings.json",
    }

    for env_var, path in paths.items():
        monkeypatch.setenv(env_var, str(path))
        path.parent.mkdir(parents=True, exist_ok=True)

    return paths


@pytest.fixture
def sample_rankings() -> list[ModelRanking]:
    """Create sample model rankings for testing.

    Returns:
        List[ModelRanking]: List of sample ModelRanking objects.
    """
    return [
        ModelRanking(llm_model_id="model1", score=10),
        ModelRanking(llm_model_id="model2", score=5),
        ModelRanking(llm_model_id="model3", score=8),
    ]


def test_pull_in_dir_recursively(temp_dir_with_files: Path) -> None:
    """Test recursive directory reading.

    Args:
        temp_dir_with_files: Fixture providing directory with test files.
    """
    result = pull_in_dir_recursively(str(temp_dir_with_files))

    assert len(result) == 3
    assert "file1.txt" in result
    assert os.path.join("subdir1", "file2.txt") in result
    assert os.path.join("subdir1", "subdir2", "file3.txt") in result
    assert result["file1.txt"] == "content1"
    assert result[os.path.join("subdir1", "file2.txt")] == "content2"
    assert result[os.path.join("subdir1", "subdir2", "file3.txt")] == "content3"


def test_pull_in_dir_recursively_nonexistent_dir() -> None:
    """Test handling of nonexistent directory."""
    result = pull_in_dir_recursively("/nonexistent/directory")
    assert result == {}


def test_pull_in_prompt_library(mock_env_paths: dict[str, Path]) -> None:
    """Test loading prompt library files.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
    """
    lib_dir = mock_env_paths["PROMPT_LIBRARY_DIR"]
    lib_dir.mkdir(parents=True, exist_ok=True)
    (lib_dir / "prompt1.txt").write_text("prompt content 1")
    (lib_dir / "prompt2.txt").write_text("prompt content 2")

    result = pull_in_prompt_library()
    assert len(result) == 2
    assert "prompt1.txt" in result
    assert "prompt2.txt" in result
    assert result["prompt1.txt"] == "prompt content 1"
    assert result["prompt2.txt"] == "prompt content 2"


def test_pull_in_testable_prompts(mock_env_paths: dict[str, Path]) -> None:
    """Test loading testable prompt files.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
    """
    test_dir = mock_env_paths["TESTABLE_PROMPTS_DIR"]
    test_dir.mkdir(parents=True, exist_ok=True)
    (test_dir / "test1.txt").write_text("test content 1")
    (test_dir / "test2.txt").write_text("test content 2")

    result = pull_in_testable_prompts()
    assert len(result) == 2
    assert "test1.txt" in result
    assert "test2.txt" in result
    assert result["test1.txt"] == "test content 1"
    assert result["test2.txt"] == "test content 2"


def test_record_llm_execution(mock_env_paths: dict[str, Path], mocker: MockerFixture) -> None:
    """Test recording LLM execution results.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
        mocker: Pytest mocker fixture.
    """
    # Mock datetime to get consistent filenames
    mock_now = datetime(2024, 1, 1, 12, 30, 0)
    mocker.patch("prompt_library.common.prompt_library_module.datetime")
    mocker.patch("prompt_library.common.prompt_library_module.datetime.now", return_value=mock_now)

    prompt = "Test prompt"
    executions = [
        {"model_id": "model1", "response": "response1"},
        {"model_id": "model2", "response": "response2"},
    ]

    # Test with template
    filepath = record_llm_execution(prompt, executions, "test_template")
    assert os.path.exists(filepath)
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    assert data["prompt"] == prompt
    assert data["prompt_template"] == "test_template"
    assert data["prompt_responses"] == executions

    # Test without template
    filepath = record_llm_execution(prompt, executions)
    assert os.path.exists(filepath)
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    assert data["prompt"] == prompt
    assert data["prompt_template"] is None
    assert data["prompt_responses"] == executions


def test_get_rankings_empty(mock_env_paths: dict[str, Path]) -> None:
    """Test getting rankings when file doesn't exist.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
    """
    rankings = get_rankings()
    assert rankings == []


def test_get_rankings(mock_env_paths: dict[str, Path], sample_rankings: list[ModelRanking]) -> None:
    """Test getting rankings from file.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
        sample_rankings: Fixture providing sample rankings.
    """
    rankings_file = mock_env_paths["LANGUAGE_MODEL_RANKINGS_FILE"]
    rankings_data = [ranking.model_dump() for ranking in sample_rankings]
    with open(rankings_file, "w", encoding="utf-8") as f:
        json.dump(rankings_data, f)

    rankings = get_rankings()
    assert len(rankings) == len(sample_rankings)
    for actual, expected in zip(rankings, sample_rankings, strict=False):
        assert actual.llm_model_id == expected.llm_model_id
        assert actual.score == expected.score


def test_save_rankings(mock_env_paths: dict[str, Path], sample_rankings: list[ModelRanking]) -> None:
    """Test saving rankings to file.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
        sample_rankings: Fixture providing sample rankings.
    """
    save_rankings(sample_rankings)
    rankings_file = mock_env_paths["LANGUAGE_MODEL_RANKINGS_FILE"]
    assert os.path.exists(rankings_file)

    with open(rankings_file, encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == len(sample_rankings)
    for actual, expected in zip(data, sample_rankings, strict=False):
        assert actual["llm_model_id"] == expected.llm_model_id
        assert actual["score"] == expected.score


def test_reset_rankings(mock_env_paths: dict[str, Path]) -> None:
    """Test resetting model rankings.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
    """
    model_ids = ["model1", "model2", "model3"]
    rankings = reset_rankings(model_ids)

    assert len(rankings) == len(model_ids)
    for ranking, model_id in zip(rankings, model_ids, strict=False):
        assert ranking.llm_model_id == model_id
        assert ranking.score == 0

    # Verify rankings were saved
    saved_rankings = get_rankings()
    assert len(saved_rankings) == len(model_ids)
    for ranking, model_id in zip(saved_rankings, model_ids, strict=False):
        assert ranking.llm_model_id == model_id
        assert ranking.score == 0
