#!/usr/bin/env python3

import os
import sys
import argparse
import glob
import tiktoken

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process files in a directory")
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument("--include", default="*.*", help="File pattern to include (default: *.*)")
    args = parser.parse_args()

    directory = args.directory
    pattern = args.include

    # Validate directory
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    # Load .gitignore if it exists
    ignores = []
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            ignores = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # Set the working directory
    os.chdir(directory)

    # Glob the directory
    glob_pattern = f"**/{pattern}"
    files = glob.glob(glob_pattern, recursive=True)

    files_count = 0
    bytes_count = 0
    full_content = ""

    for file in files:
        if not any(file.endswith(ignore.strip()) for ignore in ignores):
            print(f'<embedded-file path="{file}">')
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
            print("</embedded-file>")

            files_count += 1
            bytes_count += len(content.encode('utf-8'))
            full_content += content

    print(f"\nProcessed {files_count}, skipped {len(files) - files_count}, total bytes: {bytes_count}", file=sys.stderr)
    print(f"Glob pattern: {glob_pattern}", file=sys.stderr)

    # Initialize the tiktoken encoder
    encoder = tiktoken.encoding_for_model("gpt-4")

    print(f"Total tokens (gpt-4): {len(encoder.encode(full_content))}", file=sys.stderr)

if __name__ == "__main__":
    main()
