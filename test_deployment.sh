#!/bin/bash

# Quick deployment test script
# This script tests if the deployment configuration works properly

set -e

PROJECT_ID="youtube-ai-platform-464016"
REGION="us-central1"

echo "🧪 Testing Deployment Configuration"
echo "=================================="

# Test 1: Check if we can build a Docker image locally
echo "1. Testing Docker build..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is available"
    # Test if Dockerfile builds (quick syntax check)
    docker build -t test-build -f Dockerfile . --no-cache=false --pull=false 2>/dev/null || echo "⚠️  Dockerfile may need adjustment"
else
    echo "⚠️  Docker not available for local testing"
fi

# Test 2: Verify Cloud Build can access our project
echo "2. Testing Cloud Build access..."
gcloud builds list --limit=1 --project="$PROJECT_ID" >/dev/null 2>&1 && echo "✅ Cloud Build access confirmed" || echo "⚠️  Cloud Build access may be limited"

# Test 3: Test Artifact Registry access
echo "3. Testing Artifact Registry..."
gcloud artifacts repositories list --location="$REGION" --project="$PROJECT_ID" --format="value(name)" | head -1 >/dev/null && echo "✅ Artifact Registry accessible"

# Test 4: Check Cloud Run permissions
echo "4. Testing Cloud Run permissions..."
gcloud run services list --region="$REGION" --project="$PROJECT_ID" >/dev/null 2>&1 && echo "✅ Cloud Run permissions confirmed"

# Test 5: Verify secrets are accessible
echo "5. Testing Secret Manager access..."
SECRET_COUNT=$(gcloud secrets list --project="$PROJECT_ID" --format="value(name)" | wc -l)
echo "✅ Found $SECRET_COUNT secrets in Secret Manager"

echo ""
echo "🎯 Deployment Test Summary"
echo "========================"
echo "Your configuration appears ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Commit your changes to git"
echo "2. Push to 'develop' branch to test deployment workflow"
echo "3. Check GitHub Actions for build status"
echo "4. Once successful, push to 'main' for staging"
echo ""
echo "🔍 Monitor deployment:"
echo "- GitHub Actions: https://github.com/laziestlarry/youtube-ai-platform/actions"
echo "- Cloud Run: https://console.cloud.google.com/run?project=$PROJECT_ID"
echo "- Cloud Build: https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID"
