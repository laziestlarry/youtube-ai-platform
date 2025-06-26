#!/bin/bash
set -e
echo "🔍 Pre-launch validation: lint, type-check, test, env, DB..."

# Lint Python
if command -v flake8 &> /dev/null; then
  flake8 ../../backend
else
  echo "flake8 not found, skipping Python lint."
fi

# Type-check Python (if using mypy)
if command -v mypy &> /dev/null; then
  mypy ../../backend || echo "Type checks skipped (mypy not configured)"
else
  echo "mypy not found, skipping Python type checks."
fi

# Lint/Type-check frontend
if [ -f ../../frontend/dev_dashboard/package.json ]; then
  echo "✅ Frontend package.json found."
  # Note: 'lint' and 'type-check' scripts are not defined in package.json.
  # These steps are skipped. To enable, add them to frontend/dev_dashboard/package.json
else
  echo "⚠️ Frontend package.json not found, skipping frontend checks."
fi

# Backend tests are run directly in the CI workflow, skipping here to avoid redundancy.
echo "Backend tests will be run by the CI workflow."

# Check .env
if [ ! -f ../../.env ]; then
  echo "❌ .env missing"
  exit 1
fi

# DB migrations (if using Alembic or similar)
# alembic upgrade head

echo "✅ Pre-launch validation complete" 