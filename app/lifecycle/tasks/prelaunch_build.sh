#!/bin/bash
set -e
echo "🔨 Building backend and frontend..."

# Backend: (add build steps if needed)
echo "Backend: nothing to build (Python source)."

# Frontend:
if [ -f ../../frontend/package.json ]; then
  cd ../../frontend
  npm install
  npm run build
  cd -
fi

echo "✅ Build complete" 