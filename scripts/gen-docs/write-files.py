#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, NoReturn, TypedDict


class FileUpdate(TypedDict):
    """Type definition for file update data structure.

    Attributes:
        filename: Path to the file relative to current directory
        new_content: New content to write to file, empty string means delete
    """

    filename: str
    new_content: str


class FileUpdates(TypedDict):
    """Type definition for the complete file updates structure.

    Attributes:
        files: List of file updates to process
    """

    files: List[FileUpdate]


def read_stdin() -> str:
    """Read all data from stdin until EOF.

    Returns:
        str: The complete input data as a string.

    Raises:
        SystemExit: If there is an error reading from stdin.
    """
    try:
        return sys.stdin.read()
    except Exception as e:
        print(f"Error reading from stdin: {e}", file=sys.stderr)
        sys.exit(1)


def validate_file_path(current_dir: Path, file_path: Path) -> None:
    """Validate that the file path is within the allowed directory.

    Args:
        current_dir: The current working directory path
        file_path: The file path to validate

    Raises:
        ValueError: If the file path is outside the allowed directory
    """
    if not file_path.resolve().is_relative_to(current_dir):
        raise ValueError(f"File path '{file_path}' is outside the allowed directory.")


def process_file_updates(data: FileUpdates, current_dir: Path) -> None:
    """Process the file updates from the input data.

    Args:
        data: The parsed input data containing file updates
        current_dir: The current working directory path

    Raises:
        ValueError: If there are issues with file paths or operations
    """
    for file_update in data["files"]:
        file_path = current_dir / file_update["filename"]
        validate_file_path(current_dir, file_path)

        if not file_update["new_content"]:
            if file_path.exists():
                file_path.unlink()
                print(f"Deleted empty file: {file_update['filename']}")
        else:
            # Ensure the directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the content to the file
            file_path.write_text(file_update["new_content"], encoding="utf-8")
            print(f"Wrote file: {file_update['filename']}")


def main() -> NoReturn:
    """Main entry point for the script.

    Reads JSON input from stdin and processes file updates.
    Each update can either create/modify a file or delete it if content is empty.

    The JSON input should have the following structure:
    {
        "files": [
            {
                "filename": "path/to/file",
                "new_content": "content"
            }
        ]
    }

    Raises:
        SystemExit: If there are any errors during processing
    """
    try:
        input_data = read_stdin()
        data = json.loads(input_data)

        if not isinstance(data, dict) or "files" not in data or not isinstance(data["files"], list):
            raise ValueError("Invalid input format: 'files' should be an array.")

        current_dir = Path.cwd()
        process_file_updates(data, current_dir)
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
