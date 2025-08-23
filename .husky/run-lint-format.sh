#!/usr/bin/env sh

# Get staged Python files in src/ or tests/ directories
files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^(src)/.*\.py$')

if [ -z "$files" ]; then
  echo "No Python files in src/ staged, skipping lint/format."
  exit 0
fi

echo "Running format & lint on staged files:"
echo "$files"

# Format only staged files
black $files
isort $files

# Stage formatted files
git add $files

# Run lint only on staged files
flake8 $files
