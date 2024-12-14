from __future__ import annotations

import json
import logging
import os

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import pytz

from dotenv import load_dotenv
from loguru import logger

from prompt_library.bot_logger import get_logger, global_log_config
from prompt_library.common.typings import ModelRanking, MultiLLMPromptExecution


global_log_config(
    log_level=logging.getLevelName("DEBUG"),
    json=False,
)

load_dotenv()


def save_comparison(mo, save_data, preview, save_button):
    # Get current time in EDT
    edt = pytz.timezone("America/New_York")
    now = datetime.now(edt)
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S-%Z")

    # Generate markdown content
    content = f"""# Prompt Comparison - {now.strftime("%Y-%m-%d %H:%M:%S %Z")}

## Original Question
```
{save_data["question_input"]}
```

## First Prompt (Model: {save_data["model_name_1"]})
```xml
{save_data["final_prompt_1"]}
```

### Generated Response
```
{save_data["prompt_response_1"]}
```

## Second Prompt (Model: {save_data["model_name_2"]})
```xml
{save_data["final_prompt_2"]}
```

### Generated Response
```
{save_data["prompt_response_2"]}
```
"""

    # Save file
    filename = f"{timestamp}_comparison.md"
    filepath = Path(save_data["COMPARE_DIR"]) / filename
    filepath.write_text(content)

    save_preview(mo, preview, save_data["styles"], filepath, content, save_button)

    return save_button


def save_preview(mo, preview, styles, filepath, content, save_button):
    # Update preview
    preview.value = f"""### Preview of file to be saved:
```markdown
{content}
```"""
    # Show success message
    preview.value += f"\n\n✅ Saved to: {filepath}"
    preview.style(styles["success"])  # type: ignore

    mo.md("### Save Comparison")
    mo.vstack([save_button, preview]).style(styles["container"])  # type: ignore


# Function to read markdown file content
def read_question_file(filename: str, questions_dir: str) -> str:
    if filename == "None":
        return ""
    file_path = os.path.join(questions_dir, filename)
    with open(file_path) as f:
        return f.read().strip()


def pull_in_dir_recursively(directory: str) -> dict[str, str]:
    """Recursively read all files in a directory and its subdirectories.

    Args:
        directory: The directory path to read from.

    Returns:
        A dictionary mapping relative file paths to their contents.
    """
    logger.info(f"Attempting to read directory recursively: {directory}")

    if not os.path.exists(directory):
        logger.warning(f"Directory does not exist: {directory}")
        try:
            logger.info(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)
        except (OSError, PermissionError) as e:
            logger.error(f"Failed to create directory {directory}: {e!s}")
            return {}

    result: dict[str, str] = {}

    def recursive_read(current_dir: str, prefix: str = "") -> None:
        try:
            items = os.listdir(current_dir)
            logger.info(f"Reading {len(items)} items in {current_dir}")

            for item in items:
                item_path = os.path.join(current_dir, item)
                if os.path.isfile(item_path):
                    if prefix:
                        relative_path = os.path.join(prefix, item)
                    else:
                        relative_path = os.path.relpath(item_path, directory)

                    try:
                        with open(item_path, encoding="utf-8") as f:
                            logger.info(f"Reading file: {item_path}")
                            result[relative_path] = f.read()
                    except Exception as e:
                        logger.error(f"Failed to read file {item_path}: {e!s}")
                        continue

                elif os.path.isdir(item_path):
                    new_prefix = os.path.join(prefix, item) if prefix else item
                    recursive_read(item_path, new_prefix)

        except (OSError, PermissionError) as e:
            logger.error(f"Failed to read directory {current_dir}: {e!s}")

    recursive_read(directory)
    logger.info(f"Successfully read {len(result)} files from {directory}")
    return result


def pull_in_prompt_library() -> dict[str, str]:
    """Load all prompt library files from the configured directory.

    Returns:
        A dictionary mapping relative file paths to their contents.
    """
    prompt_library_dir = os.getenv("PROMPT_LIBRARY_DIR", "./src/prompt_library/data/prompt_lib")
    logger.info(f"Loading prompt library from: {prompt_library_dir}")

    try:
        result = pull_in_dir_recursively(prompt_library_dir)
        if not result:
            logger.warning("No prompt library files found")
        else:
            logger.info(f"Successfully loaded {len(result)} prompt library files")
            logger.debug(f"Loaded files: {list(result.keys())}")
        return result
    except Exception as e:
        logger.error(f"Failed to load prompt library: {e!s}")
        return {}


def pull_in_testable_prompts() -> dict[str, str]:
    """Load all testable prompt files from the configured directory.

    Returns:
        A dictionary mapping relative file paths to their contents.
    """
    testable_prompts_dir = os.getenv("TESTABLE_PROMPTS_DIR", "./src/prompt_library/data/testable_prompts")
    return pull_in_dir_recursively(testable_prompts_dir)


def record_llm_execution(prompt: str, list_model_execution_dict: list[dict], prompt_template: str | None = None) -> str:
    """Record the execution results of multiple LLM models for a given prompt.

    Args:
        prompt: The prompt text that was executed.
        list_model_execution_dict: List of execution results from different models.
        prompt_template: Optional template name used for the prompt.

    Returns:
        The filepath where the execution record was saved.
    """
    execution_dir = os.getenv("PROMPT_EXECUTIONS_DIR", "./src/prompt_library/data/prompt_executions")
    os.makedirs(execution_dir, exist_ok=True)

    if prompt_template:
        filename_base = prompt_template.replace(" ", "_").lower()
    else:
        filename_base = prompt[:50].replace(" ", "_").lower()

    # Clean up filename_base to ensure it's alphanumeric only
    filename_base = "".join(char for char in filename_base if char.isalnum() or char == "_")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_base}_{timestamp}.json"
    filepath = os.path.join(execution_dir, filename)

    execution_record = MultiLLMPromptExecution(
        prompt=prompt,
        prompt_template=prompt_template,
        prompt_responses=list_model_execution_dict,
    )

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(execution_record.model_dump(), f, indent=2)

    return filepath


def get_rankings() -> list[ModelRanking]:
    """Load model rankings from the configured rankings file.

    Returns:
        A list of ModelRanking objects representing the current rankings.
    """
    rankings_file = os.getenv(
        "LANGUAGE_MODEL_RANKINGS_FILE", "./src/prompt_library/data/language_model_rankings/rankings.json"
    )
    if not os.path.exists(rankings_file):
        return []
    with open(rankings_file, encoding="utf-8") as f:
        rankings_data = json.load(f)
    return [ModelRanking(**ranking) for ranking in rankings_data]


def save_rankings(rankings: list[ModelRanking]) -> None:
    """Save model rankings to the configured rankings file.

    Args:
        rankings: List of ModelRanking objects to save.
    """
    rankings_file = os.getenv(
        "LANGUAGE_MODEL_RANKINGS_FILE", "./src/prompt_library/data/language_model_rankings/rankings.json"
    )
    os.makedirs(os.path.dirname(rankings_file), exist_ok=True)
    rankings_dict = [ranking.model_dump() for ranking in rankings]
    with open(rankings_file, "w", encoding="utf-8") as f:
        json.dump(rankings_dict, f, indent=2)


def reset_rankings(model_ids: list[str]) -> list[ModelRanking]:
    """Reset rankings for the specified models to zero.

    Args:
        model_ids: List of model IDs to reset rankings for.

    Returns:
        A list of new ModelRanking objects with reset scores.
    """
    new_rankings = [ModelRanking(llm_model_id=model_id, score=0) for model_id in model_ids]
    save_rankings(new_rankings)
    return new_rankings


def get_question_files(questions_dir: str) -> list[str]:
    """Get list of markdown files in questions directory.

    Args:
        questions_dir: Path to questions directory

    Returns:
        List of markdown filenames without path
    """
    import glob
    import os

    question_files = glob.glob(os.path.join(questions_dir, "*.md"))
    return [os.path.basename(f) for f in question_files]


def pull_in_multiple_prompt_libraries(
    directories: list[Union[str, Path]], file_type: Optional[str] = None
) -> dict[str, str]:
    """Load and merge prompt library files from multiple directories.

    This function recursively reads all files from the provided directories and merges
    their contents into a single dictionary. If a file exists in multiple directories,
    the last occurrence (based on directory order) will be used.

    Args:
        directories: List of directory paths to read from.
        file_type: Optional file extension to filter results (e.g., 'xml', 'md').
                  If provided, only returns files with matching extension.
                  Case-insensitive. Do not include the dot.

    Returns:
        A dictionary mapping relative file paths to their contents.
    """
    logger.info(f"Loading prompt libraries from {len(directories)} directories")
    if file_type:
        logger.info(f"Filtering for .{file_type.lower()} files")

    merged_results: dict[str, str] = {}

    for directory in directories:
        directory_str = str(directory)
        logger.debug(f"Processing directory: {directory_str}")

        if not os.path.exists(directory_str):
            logger.warning(f"Directory does not exist: {directory_str}")
            continue

        try:
            current_results = pull_in_dir_recursively(directory_str)
            logger.info(f"Found {len(current_results)} files in {directory_str}")

            # Filter by file type if specified
            if file_type:
                filtered_results = {
                    k: v for k, v in current_results.items() if Path(k).suffix.lower() == f".{file_type.lower()}"
                }
                logger.debug(
                    f"Filtered {len(current_results)} files to {len(filtered_results)} "
                    f".{file_type.lower()} files in {directory_str}"
                )
                current_results = filtered_results

            # Track any overwritten files for debugging
            overlapping_files = set(merged_results.keys()) & set(current_results.keys())
            if overlapping_files:
                logger.debug(
                    f"Overwriting {len(overlapping_files)} files from previous directories: {overlapping_files}"
                )

            merged_results.update(current_results)

        except Exception as e:
            logger.error(f"Failed to process directory {directory_str}: {e!s}")
            continue

    if file_type:
        logger.info(f"Successfully loaded {len(merged_results)} .{file_type.lower()} files from all directories")
    else:
        logger.info(f"Successfully loaded {len(merged_results)} total files from all directories")

    logger.debug(f"Final loaded files: {list(merged_results.keys())}")

    return merged_results
