#!/bin/bash
# Auto-fix flake8 F401 (unused imports) and E501 (line too long) in app/ using autoflake and autopep8

set -e

# Install required tools if not present
echo "Ensuring autoflake and autopep8 are installed..."
pip install autoflake autopep8 flake8

# Remove unused imports (F401)
echo "Running autoflake to remove unused imports..."
autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive app/

# Attempt to auto-wrap long lines (E501)
echo "Running autopep8 to wrap long lines..."
autopep8 --in-place --aggressive --aggressive --max-line-length=79 --recursive app/

# Run flake8 to show remaining issues
echo "Running flake8 (remaining issues):"
flake8 app/

echo "\nAuto-fix complete. Review any remaining flake8 issues above and fix manually if needed." 