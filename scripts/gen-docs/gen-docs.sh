#!/bin/bash

# ========================================================================================================
# Script Purpose:
# --------------------------------------------------------------------------------------------------------
# This script processes the commit history of a base Git branch and generates new commits on a tracking
# branch (`gen-commits`). Each new commit will have two parents: the current base commit and the last
# generated commit on the tracking branch. The script runs a specified external command to generate files
# based on the diff between the base commit and its parent, then stages and commits the generated files.
#
# ========================================================================================================
# Usage:
# --------------------------------------------------------------------------------------------------------
# 1. Configure the base branch (default: 'remotes/origin/main') and tracking branch (default: 'gen-commits').
# 2. Run the script in a Git repository with the external command specified.
# 3. The script processes one commit at a time from the base branch, generates new files, and commits them
#    to the tracking branch with the correct parentage.
#
# Example:
#    ./this-script.sh
#
# ========================================================================================================
# General Strategy:
# --------------------------------------------------------------------------------------------------------
# 1. The script checks if the tracking branch exists, creates it from the first commit on the base branch
#    if necessary.
# 2. Iterates over the commits in the base branch. For each commit, generates files based on the commit's
#    changes, then commits these files to the tracking branch.
# 3. Keeps track of the last generated base commit, allowing for incremental runs.
#
# ========================================================================================================

# Configuration
tracking_branch="gen-commits"
base_branch="remotes/origin/main"

# Check for clean working directory
if [[ -n $(git status --porcelain) ]]; then
    echo "Error: Working directory is not clean. Please commit or stash your changes before running this script."
    exit 1
fi

# Ensure the branch exists, or create it from scratch
if ! git show-ref --verify --quiet refs/heads/$tracking_branch; then
    echo "Tracking branch $tracking_branch does not exist, creating it..."

    # Start at the first commit of $base_branch
    first_commit_on_base=$(git rev-list --reverse $base_branch | head -n 1)

    # Create the tracking branch from the first commit of the base branch
    git checkout -b $tracking_branch $first_commit_on_base
    last_generated_commit=""
else
    echo "Tracking branch $tracking_branch found, checking out..."
    git checkout $tracking_branch
    # Find the last generated commit on the tracking branch
    last_generated_commit=$(git rev-parse HEAD)

    # Extract the last base commit processed by getting the first parent of the last generated commit
    last_base_commit=$(git rev-parse ${last_generated_commit}^1)
fi

# Determine the next commit to process from the base branch
if [[ -z "$last_generated_commit" ]]; then
    # No generated commits yet, start from the first commit on the base branch
    start_commit=$(git rev-list --reverse $base_branch | head -n 1)
else
    # Find the last base commit processed
    # If last_base_commit is not set (e.g., tracking branch was just created with initial commit),
    # derive it from the first parent of the last_generated_commit
    if [[ -z "$last_base_commit" ]]; then
        last_base_commit=$(git rev-parse ${last_generated_commit}^1)
    fi

    # Find the next commit after last_base_commit on the base branch
    start_commit=$(git rev-list --reverse $base_branch --ancestry-path ${last_base_commit}..$base_branch | head -n 1)
fi

# Check if there's a commit to process
if [[ -z "$start_commit" ]]; then
    echo "No new commits to process. All caught up."
    exit 0
fi

# Create a temporary file for the diff
diff_file=$(mktemp)

# Process the next commit in line
git log --oneline -1 "$start_commit"

# Get the diff of the start_commit against its parent
git log -p -1 $start_commit > "$diff_file"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Path to the target script
TARGET_SCRIPT="$SCRIPT_DIR/llm-gen-docs.sh"
"$TARGET_SCRIPT" "$diff_file" "$(pwd)"

# Check if the generation command succeeded
if [[ $? -ne 0 ]]; then
    echo "Error: Generation command failed for commit $start_commit. Aborting."
    rm -f "$diff_file"  # Clean up the temporary file
    exit 1
fi

# Add the newly generated files to the staging area
git add docs/

# Create a tree object from the index
tree=$(git write-tree)

# Create the commit with specified parents
if [[ -n "$last_generated_commit" ]]; then
    new_generated_commit=$(echo "Generated files for $start_commit" | git commit-tree $tree -p $start_commit -p $last_generated_commit)
else
    new_generated_commit=$(echo "Generated files for $start_commit" | git commit-tree $tree -p $start_commit)
fi

# Update the tracking branch with the new generated commit
git update-ref refs/heads/$tracking_branch $new_generated_commit

# Reset HEAD to the new commit
git reset --hard $new_generated_commit

# Update last_generated_commit and last_base_commit
last_generated_commit=$new_generated_commit
last_base_commit=$start_commit

# Clean up the temporary file
rm -f "$diff_file"

echo "Processed and committed $start_commit. Tracking branch updated."
