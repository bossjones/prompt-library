from __future__ import annotations

import json
import os

from datetime import datetime
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from loguru import logger

from prompt_library.common.typings import ModelRanking, MultiLLMPromptExecution


load_dotenv()


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
