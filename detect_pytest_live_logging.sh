#!/usr/bin/env bash
# shellcheck shell=bash
# The purpose of this file is to make sure live logging is NOT enabled when committing.
# It is very verbose and we haven't done enough work to ensure secrets are not leaked in the logs.

if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_pyproject_file>"
    exit 1
fi

set -e
if grep -q "^log_cli = true$" "${1}"; then
  exit 3
else
  exit 0
fi
