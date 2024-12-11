from __future__ import annotations

import json
import os

from datetime import datetime
from typing import List

from dotenv import load_dotenv

from prompt_library.common.typings import ModelRanking, MultiLLMPromptExecution


load_dotenv()


def pull_in_dir_recursively(directory: str) -> dict[str, str]:
    """Recursively read all files in a directory and its subdirectories.

    Args:
        directory: The directory path to read from.

    Returns:
        A dictionary mapping relative file paths to their contents.
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        return {}

    result: dict[str, str] = {}

    def recursive_read(current_dir: str) -> None:
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isfile(item_path):
                relative_path = os.path.relpath(item_path, directory)
                with open(item_path, encoding="utf-8") as f:
                    result[relative_path] = f.read()
            elif os.path.isdir(item_path):
                recursive_read(item_path)

    recursive_read(directory)
    return result


def pull_in_prompt_library() -> dict[str, str]:
    """Load all prompt library files from the configured directory.

    Returns:
        A dictionary mapping relative file paths to their contents.
    """
    prompt_library_dir = os.getenv("PROMPT_LIBRARY_DIR", "./src/prompt_library/data/prompt_lib")
    return pull_in_dir_recursively(prompt_library_dir)


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
