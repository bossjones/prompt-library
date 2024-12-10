from __future__ import annotations

import datetime
import json
import os

from typing import Dict, List, Union


OUTPUT_DIR = "output"


def build_file_path(name: str) -> str:
    """Build a file path in the output directory.

    Args:
        name: The name of the file.

    Returns:
        The complete file path within the output directory.
    """
    session_dir = f"{OUTPUT_DIR}"
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, f"{name}")


def build_file_name_session(name: str, session_id: str) -> str:
    """Build a file path within a session-specific subdirectory.

    Args:
        name: The name of the file.
        session_id: The session identifier for the subdirectory.

    Returns:
        The complete file path within the session subdirectory.
    """
    session_dir = f"{OUTPUT_DIR}/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, f"{name}")


def to_json_file_pretty(name: str, content: Union[dict, list]) -> None:
    """Write content to a JSON file with pretty formatting.

    Args:
        name: The name of the file (without .json extension).
        content: The data to write to the JSON file.

    Raises:
        TypeError: If an object in the content is not JSON serializable.
    """

    def default_serializer(obj: object) -> dict:
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    with open(f"{name}.json", "w") as outfile:
        json.dump(content, outfile, indent=2, default=default_serializer)


def current_date_time_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def current_date_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")


def dict_item_diff_by_set(previous_list: list[dict], current_list: list[dict], set_key: str) -> list[str]:
    """Find new items in current_list that weren't in previous_list based on a key.

    Args:
        previous_list: The original list of dictionaries.
        current_list: The new list of dictionaries to compare against.
        set_key: The dictionary key to use for comparison.

    Returns:
        A list of values that are present in current_list but not in previous_list.
    """
    previous_set = {item[set_key] for item in previous_list}
    current_set = {item[set_key] for item in current_list}
    return list(current_set - previous_set)
