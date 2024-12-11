from __future__ import annotations

import json
import logging
import os
import shutil
import sys

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Generator, List

from _pytest.monkeypatch import MonkeyPatch
from loguru import logger

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


@pytest.fixture(autouse=True)
def setup_logger(caplog: LogCaptureFixture) -> Generator[None, None, None]:
    """Configure loguru to use pytest's logging handler.

    Args:
        caplog: Pytest fixture for capturing log messages.

    Yields:
        None
    """
    # Remove default handler
    logger.remove()

    # Add handler that writes to pytest's caplog
    logger.add(
        lambda msg: caplog.handler.emit(
            logging.LogRecord(
                name=msg.record["name"],
                level=msg.record["level"].no,
                pathname=msg.record["file"].name,
                lineno=msg.record["line"],
                msg=msg.record["message"],
                args=(),
                exc_info=None,
            )
        ),
        format="{message}",
    )
    yield
    logger.remove()


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


def test_pull_in_dir_recursively_with_logging(temp_dir_with_files: Path, caplog: LogCaptureFixture) -> None:
    """Test pull_in_dir_recursively with logging verification.

    Args:
        temp_dir_with_files: Fixture providing temporary directory with test files.
        caplog: Pytest fixture for capturing log messages.
    """
    result = pull_in_dir_recursively(str(temp_dir_with_files))

    assert len(result) == 3
    assert "file1.txt" in result
    assert os.path.join("subdir1", "file2.txt") in result
    assert os.path.join("subdir1", "subdir2", "file3.txt") in result

    # Verify logging messages
    assert "Attempting to read directory recursively" in caplog.text
    assert "Successfully read 3 files" in caplog.text


def test_pull_in_dir_recursively_nonexistent_dir(tmp_path: Path, caplog: LogCaptureFixture) -> None:
    """Test pull_in_dir_recursively with a nonexistent directory.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
        caplog: Pytest fixture for capturing log messages.
    """
    nonexistent_dir = tmp_path / "nonexistent"
    result = pull_in_dir_recursively(str(nonexistent_dir))

    assert result == {}
    assert "Directory does not exist" in caplog.text
    assert "Creating directory" in caplog.text


def test_pull_in_dir_recursively_with_unreadable_file(temp_dir_with_files: Path, caplog: LogCaptureFixture) -> None:
    """Test pull_in_dir_recursively with an unreadable file.

    Args:
        temp_dir_with_files: Fixture providing temporary directory with test files.
        caplog: Pytest fixture for capturing log messages.
    """
    # Create an unreadable file
    unreadable_file = temp_dir_with_files / "unreadable.txt"
    unreadable_file.write_text("test")
    os.chmod(str(unreadable_file), 0o000)

    try:
        result = pull_in_dir_recursively(str(temp_dir_with_files))

        assert len(result) == 3  # Original 3 files should still be read
        assert "unreadable.txt" not in result
        assert "Failed to read file" in caplog.text
    finally:
        os.chmod(str(unreadable_file), 0o644)  # Restore permissions for cleanup


def test_pull_in_prompt_library_with_files(mock_env_paths: dict[str, Path], caplog: LogCaptureFixture) -> None:
    """Test pull_in_prompt_library with existing files.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
        caplog: Pytest fixture for capturing log messages.
    """
    # Create some test prompt files
    prompt_dir = mock_env_paths["PROMPT_LIBRARY_DIR"]
    prompt_dir.mkdir(parents=True, exist_ok=True)
    (prompt_dir / "test1.xml").write_text("test1 content")
    (prompt_dir / "test2.xml").write_text("test2 content")

    result = pull_in_prompt_library()

    assert len(result) == 2
    assert "test1.xml" in result
    assert "test2.xml" in result
    assert "Successfully loaded 2 prompt library files" in caplog.text


def test_pull_in_prompt_library_empty_dir(mock_env_paths: dict[str, Path], caplog: LogCaptureFixture) -> None:
    """Test pull_in_prompt_library with an empty directory.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
        caplog: Pytest fixture for capturing log messages.
    """
    result = pull_in_prompt_library()

    assert result == {}
    assert "No prompt library files found" in caplog.text


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


@pytest.fixture
def mock_one_off_tasks(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory mimicking the one-off-tasks folder structure.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.

    Yields:
        Path: Path to the temporary one-off-tasks directory.
    """
    one_off_tasks = tmp_path / "one-off-tasks"

    # Create main subdirectories
    dirs = ["code-generation", "code-review", "image-generation", "lore-writing/helldivers2/johnhelldiver/examples"]

    for dir_path in dirs:
        (one_off_tasks / dir_path).mkdir(parents=True, exist_ok=True)

    # Create README files
    readme_contents = {
        "code-generation/README.md": """# One-Off Code Generation Prompts

This directory contains prompts for specific, single-use code generation tasks.

## Purpose
- Generate code for specific project requirements
- Create one-time scripts or utilities
- Produce custom implementations

## Contents
- Project-specific code generators
- Custom implementation templates
- Specialized utility scripts
- One-time automation tools
""",
        "code-review/README.md": """# One-Off Code Review Prompts

This directory contains prompts for specific, single-instance code review tasks.

## Purpose
- Perform one-time code reviews
- Analyze specific code implementations
- Review particular pull requests
- Assess individual components

## Contents
- Project-specific review templates
- Custom review checklists
- Special case review guides
- Security audit templates
""",
        "image-generation/README.md": """# One-Off Image Generation Prompts

This directory contains prompts for single-use image generation tasks, optimized for specific use cases.

## Purpose
- Generate specific, one-time images
- Create custom artwork for particular projects
- Produce unique visual content

## Contents
- Project-specific image prompts
- Custom artwork generators
- Special effect templates
- Style transfer examples
""",
        "lore-writing/README.md": """# Lore Writing Prompts

This directory contains prompts for creating specific pieces of lore and backstories for various projects and universes.

## Purpose
- Create detailed backstories for characters
- Generate world-building content
- Develop fictional histories
- Craft universe-specific lore

## Contents
- Character backstory prompts
- World history generators
- Mythology creators
- Cultural development templates

## Projects
- Helldivers 2
  - Character backstories
  - World-building elements
  - Military histories
""",
    }

    for file_path, content in readme_contents.items():
        (one_off_tasks / file_path).write_text(content)

    # Create Helldivers2 specific files
    helldivers_path = one_off_tasks / "lore-writing/helldivers2/johnhelldiver"

    # Write example files
    for i in range(1, 5):
        with open(helldivers_path / "examples" / f"example{i}.md", "w", encoding="utf-8") as f:
            f.write(f"# Example {i} content")

    # Write other Helldivers2 files
    (helldivers_path / "Justfile").write_text("""lint:
    xmllint --schema prompt_schema.xsd prompt.xml --noout

ping:
    uv run llm "ping"

run:
    uv run llm -m gpt-4o < prompt.xml
""")

    # Write metadata.json
    (helldivers_path / "metadata.json").write_text("""{"promptName": "JohnHelldiverBackstory"}""")

    # Write prompt.xml with full content
    prompt_xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<prompt xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="prompt_schema.xsd">
  <purpose>
    You are a skilled lore writer for the Helldivers 2 universe. Your task is to create a compelling fan fiction story about John Helldiver, a figure steeped in mystery and legend.
  </purpose>

  <instructions>
    <instruction>Write a brief but engaging backstory for John Helldiver</instruction>
    <instruction>Include origin and early life</instruction>
    <instruction>Highlight key missions and accomplishments</instruction>
  </instructions>

  <examples>
    <example>
      Sarah "Stormbreaker" Chen, born on a remote Super Earth colony, joined the Helldivers at 18 after her home was destroyed by Terminid forces.
    </example>
  </examples>

  <output_format>Provide a cohesive narrative of 200-300 words</output_format>

  <character-characterization>
    <trait>
      <name>Stoic yet Self-Aware</name>
      <description>John embodies the ideal Helldiver but secretly questions the meaning of his unending missions.</description>
    </trait>
  </character-characterization>
</prompt>"""
    (helldivers_path / "prompt.xml").write_text(prompt_xml_content)

    # Write prompt_schema.xsd with full content
    schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:complexType name="instructionType">
    <xs:simpleContent>
      <xs:extension base="xs:string"/>
    </xs:simpleContent>
  </xs:complexType>

  <xs:complexType name="instructionsType">
    <xs:sequence>
      <xs:element name="instruction" type="instructionType" minOccurs="1" maxOccurs="unbounded"/>
    </xs:sequence>
  </xs:complexType>

  <xs:complexType name="exampleType">
    <xs:simpleContent>
      <xs:extension base="xs:string"/>
    </xs:simpleContent>
  </xs:complexType>

  <xs:complexType name="examplesType">
    <xs:sequence>
      <xs:element name="example" type="exampleType" minOccurs="1" maxOccurs="unbounded"/>
    </xs:sequence>
  </xs:complexType>

  <xs:complexType name="traitType">
    <xs:sequence>
      <xs:element name="name" type="xs:string"/>
      <xs:element name="description" type="xs:string"/>
    </xs:sequence>
  </xs:complexType>

  <xs:complexType name="characterCharacterizationType">
    <xs:sequence>
      <xs:element name="trait" type="traitType" minOccurs="1" maxOccurs="unbounded"/>
    </xs:sequence>
  </xs:complexType>

  <xs:element name="prompt">
    <xs:complexType>
      <xs:all>
        <xs:element name="purpose" type="xs:string"/>
        <xs:element name="instructions" type="instructionsType"/>
        <xs:element name="examples" type="examplesType"/>
        <xs:element name="character-characterization" type="characterCharacterizationType" minOccurs="0"/>
        <xs:element name="output_format" type="xs:string"/>
      </xs:all>
    </xs:complexType>
  </xs:element>
</xs:schema>"""
    (helldivers_path / "prompt_schema.xsd").write_text(schema_content)

    yield one_off_tasks


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


def test_one_off_tasks_structure(mock_one_off_tasks: Path) -> None:
    """Test the one-off-tasks directory structure.

    Args:
        mock_one_off_tasks: Fixture providing mock one-off-tasks directory.
    """
    # Verify main directories exist
    assert (mock_one_off_tasks / "code-generation").is_dir()
    assert (mock_one_off_tasks / "code-review").is_dir()
    assert (mock_one_off_tasks / "image-generation").is_dir()
    assert (mock_one_off_tasks / "lore-writing").is_dir()

    # Verify README files exist and have content
    assert (mock_one_off_tasks / "code-generation/README.md").is_file()
    assert (mock_one_off_tasks / "code-review/README.md").is_file()
    assert (mock_one_off_tasks / "image-generation/README.md").is_file()
    assert (mock_one_off_tasks / "lore-writing/README.md").is_file()

    # Verify Helldivers2 structure
    helldivers_path = mock_one_off_tasks / "lore-writing/helldivers2/johnhelldiver"
    assert helldivers_path.is_dir()
    assert (helldivers_path / "examples").is_dir()
    assert (helldivers_path / "Justfile").is_file()
    assert (helldivers_path / "metadata.json").is_file()
    assert (helldivers_path / "prompt.xml").is_file()
    assert (helldivers_path / "prompt_schema.xsd").is_file()

    # Verify example files
    for i in range(1, 5):
        assert (helldivers_path / "examples" / f"example{i}.md").is_file()


def test_prompt_library_with_one_off_tasks(
    mock_env_paths: dict[str, Path],
    mock_one_off_tasks: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test combining prompt library with one-off tasks.

    This test verifies that we can successfully pull in both prompt library content
    and one-off tasks content, ensuring they don't interfere with each other.

    Args:
        mock_env_paths: Fixture providing mock environment paths.
        mock_one_off_tasks: Fixture providing mock one-off tasks directory.
        monkeypatch: Pytest monkeypatch fixture.
    """
    # Set up prompt library with some content
    lib_dir = mock_env_paths["PROMPT_LIBRARY_DIR"]
    lib_dir.mkdir(parents=True, exist_ok=True)
    (lib_dir / "prompt1.txt").write_text("prompt content 1")

    # Create subdir and its content
    subdir = lib_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)
    (subdir / "prompt2.txt").write_text("prompt content 2")

    # Point the PROMPT_LIBRARY_DIR to include both directories
    combined_dir = mock_env_paths["PROMPT_LIBRARY_DIR"].parent / "combined"
    combined_dir.mkdir(parents=True, exist_ok=True)

    # Create directories and copy files instead of symlinks
    prompt_lib_dir = combined_dir / "prompt_lib"
    one_off_tasks_dir = combined_dir / "one_off_tasks"

    # Copy prompt library files
    os.makedirs(prompt_lib_dir, exist_ok=True)
    for item in os.listdir(lib_dir):
        src = lib_dir / item
        dst = prompt_lib_dir / item
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        else:
            os.makedirs(dst, exist_ok=True)
            for root, _, files in os.walk(src):
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst, os.path.relpath(src_file, src))
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)

    # Copy one-off tasks files
    os.makedirs(one_off_tasks_dir, exist_ok=True)
    for item in os.listdir(mock_one_off_tasks):
        src = mock_one_off_tasks / item
        dst = one_off_tasks_dir / item
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        else:
            os.makedirs(dst, exist_ok=True)
            for root, _, files in os.walk(src):
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst, os.path.relpath(src_file, src))
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)

    # Update the environment variable
    monkeypatch.setenv("PROMPT_LIBRARY_DIR", str(combined_dir))

    # Pull in all content
    result = pull_in_prompt_library()

    # Verify prompt library content
    assert "prompt_lib/prompt1.txt" in result
    assert "prompt_lib/subdir/prompt2.txt" in result
    assert result["prompt_lib/prompt1.txt"] == "prompt content 1"
    assert result["prompt_lib/subdir/prompt2.txt"] == "prompt content 2"

    # Verify one-off tasks content
    helldivers_path = "one_off_tasks/lore-writing/helldivers2/johnhelldiver"
    assert f"{helldivers_path}/prompt.xml" in result
    assert f"{helldivers_path}/metadata.json" in result
    assert f"{helldivers_path}/prompt_schema.xsd" in result

    # Verify content of specific files
    metadata_path = f"{helldivers_path}/metadata.json"
    prompt_path = f"{helldivers_path}/prompt.xml"
    schema_path = f"{helldivers_path}/prompt_schema.xsd"

    assert "JohnHelldiverBackstory" in result[metadata_path]
    assert "<?xml version=" in result[prompt_path]
    assert "xs:schema" in result[schema_path]
