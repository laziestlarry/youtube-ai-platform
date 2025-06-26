#!/bin/bash
# Auto-fix Python style issues in app/ using black and isort, then run flake8

set -e

# Format with black
echo "Running black..."
black app/

# Sort imports with isort
echo "Running isort..."
isort app/

# Run flake8 to show remaining issues
echo "Running flake8 (remaining issues):"
flake8 app/

echo "\nAuto-formatting complete. Review any remaining flake8 issues above." 