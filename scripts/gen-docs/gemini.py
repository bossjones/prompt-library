# USAGE: python gemini.py config.yaml < input.txt
# SOURCE: https://github.com/dstoc/gen-docs/tree/00bd651872141dec56b6d27983ed9d9db1b56123
from __future__ import annotations

import os
import sys
from typing import Any, NoReturn, Optional, TypeVar, cast

import llm
import yaml
from dotenv import load_dotenv

T = TypeVar('T')

def read_stdin() -> str:
    """Read data from stdin until EOF.

    Returns:
        str: The data read from stdin.

    Raises:
        SystemExit: If there is an error reading from stdin.
    """
    try:
        return sys.stdin.read().strip()
    except Exception as e:
        print(f"Error reading from stdin: {e}", file=sys.stderr)
        sys.exit(1)


def load_yaml_config(config_path: str) -> dict[str, Any]:
    """Load and validate YAML configuration file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        dict[str, Any]: Parsed YAML configuration containing model and generation settings.

    Raises:
        SystemExit: If config is invalid, missing required fields, or file cannot be loaded.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Validate required properties
        if not config.get('model'):
            print("Configuration file must include a 'model' property.", file=sys.stderr)
            sys.exit(1)

        if not config.get('generationConfig'):
            print("Configuration file must include a 'generationConfig' property.", file=sys.stderr)
            sys.exit(1)

        return config
    except Exception as e:
        print(f"Error loading config file: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> NoReturn:
    """Main entry point for the script.

    Reads configuration and input, initializes Gemini model, and generates response.

    Environment Variables:
        GEMINI_API_KEY: Required API key for accessing Gemini model.

    Raises:
        SystemExit: If required args/env vars are missing or on any error.
    """
    # Load environment variables
    load_dotenv()

    # Check command line args
    if len(sys.argv) != 2:
        print("Usage: python gemini.py <config-file.yaml>", file=sys.stderr)
        sys.exit(1)

    # Get config path
    config_path = os.path.abspath(sys.argv[1])

    # Load config
    config = load_yaml_config(config_path)

    # Initialize Gemini model
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Environment variable GEMINI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    # Get the model
    model: llm.Model = llm.get_model(config['model'])
    model.key = gemini_api_key

    # Read input
    user_input = read_stdin()
    if not user_input:
        print("No input received from stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        # Send message and get response
        result = model.prompt(user_input, stream=False)
        print(cast(str, result.response), file=sys.stderr)
        print(result.text())
        sys.exit(0)  # Explicitly exit
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
