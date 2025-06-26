#!/bin/bash
set -e
echo "🏗️ Running build validation..."

echo "Validating API Dockerfile..."
docker build -f Dockerfile.api -t api-ci-validation .

echo "Validating Worker Dockerfile..."
# Assuming Dockerfile.worker exists as it's in deploy.yml
if [ -f Dockerfile.worker ]; then
  docker build -f Dockerfile.worker -t worker-ci-validation .
else
  echo "⚠️ Dockerfile.worker not found, skipping."
fi


echo "Validating Mini-App Dockerfile..."
docker build -f Dockerfile.mini_app -t mini-app-ci-validation .

echo "✅ Build validation complete."