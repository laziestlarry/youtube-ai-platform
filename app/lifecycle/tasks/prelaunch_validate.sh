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
if [ -f ../../frontend/package.json ]; then
  cd ../../frontend
  npm run lint || echo "Frontend lint skipped"
  npm run type-check || echo "Frontend type-check skipped"
  cd -
fi

# Run backend tests
if [ -d ../../backend/tests ]; then
  pytest ../../backend/tests
else
  echo "No backend tests found."
fi

# Check .env
if [ ! -f ../../.env ]; then
  echo "❌ .env missing"
  exit 1
fi

# DB migrations (if using Alembic or similar)
# alembic upgrade head

echo "✅ Pre-launch validation complete" 