#!/bin/bash

# Deployment Configuration Validation Script
# This script validates that all deployment prerequisites are met

set -e

PROJECT_ID=${1:-"youtube-ai-platform-464016"}
REGION="us-central1"

echo "🔍 Validating deployment configuration for project: $PROJECT_ID"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if gcloud is authenticated
echo "Checking gcloud authentication..."
if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_status "gcloud authenticated" 0
else
    print_status "gcloud authentication" 1
    echo "Run: gcloud auth login"
    exit 1
fi

# Check project configuration
echo "Checking project configuration..."
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ "$CURRENT_PROJECT" = "$PROJECT_ID" ]; then
    print_status "Project configured correctly" 0
else
    print_warning "Current project: $CURRENT_PROJECT, Expected: $PROJECT_ID"
    echo "Run: gcloud config set project $PROJECT_ID"
fi

# Check required APIs
echo "Checking enabled APIs..."
REQUIRED_APIS=(
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "secretmanager.googleapis.com"
    "artifactregistry.googleapis.com"
)

for api in "${REQUIRED_APIS[@]}"; do
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        print_status "$api enabled" 0
    else
        print_status "$api enabled" 1
        echo "Run: gcloud services enable $api"
    fi
done

# Check service accounts
echo "Checking service accounts..."
SERVICE_ACCOUNTS=(
    "api-service-sa"
    "worker-service-sa"
    "github-actions-sa"
)

for sa in "${SERVICE_ACCOUNTS[@]}"; do
    if gcloud iam service-accounts describe "$sa@$PROJECT_ID.iam.gserviceaccount.com" >/dev/null 2>&1; then
        print_status "$sa service account exists" 0
    else
        print_status "$sa service account exists" 1
        echo "Run: gcloud iam service-accounts create $sa"
    fi
done

# Check Artifact Registry repositories
echo "Checking Artifact Registry repositories..."
REPOSITORIES=(
    "creator-cmd-center-staging"
    "creator-cmd-center-prod"
    "creator-cmd-center-test"
)

for repo in "${REPOSITORIES[@]}"; do
    if gcloud artifacts repositories describe "$repo" --location="$REGION" >/dev/null 2>&1; then
        print_status "Repository $repo exists" 0
    else
        print_status "Repository $repo exists" 1
        echo "Run: gcloud artifacts repositories create $repo --repository-format=docker --location=$REGION"
    fi
done

# Check secrets
echo "Checking Secret Manager secrets..."
REQUIRED_SECRETS=(
    "DATABASE_URL"
    "REDIS_URL"
    "SECRET_KEY"
    "GOOGLE_CLIENT_ID"
    "GOOGLE_CLIENT_SECRET"
    "GEMINI_API_KEY"
    "SERPER_API_KEY"
    "GCS_BUCKET_NAME"
    "TASK_QUEUE_NAME"
    "WORKER_SA_EMAIL"
)

for secret in "${REQUIRED_SECRETS[@]}"; do
    if gcloud secrets describe "$secret" >/dev/null 2>&1; then
        print_status "Secret $secret exists" 0
    else
        print_status "Secret $secret exists" 1
        echo "Run: ./setup_gcp_secrets.sh"
    fi
done

# Check Workload Identity
echo "Checking Workload Identity Federation..."
if gcloud iam workload-identity-pools describe "github-actions" --location="global" >/dev/null 2>&1; then
    print_status "Workload Identity Pool exists" 0
else
    print_status "Workload Identity Pool exists" 1
    echo "Setup Workload Identity Federation (see deployment guide)"
fi

# Check GitHub repository (if gh CLI is available)
if command -v gh &> /dev/null; then
    echo "Checking GitHub repository secrets..."
    GITHUB_SECRETS=(
        "GCP_PROJECT_ID"
        "GCP_WORKLOAD_IDENTITY_PROVIDER"
        "GCP_SERVICE_ACCOUNT_EMAIL"
    )
    
    for secret in "${GITHUB_SECRETS[@]}"; do
        if gh secret list | grep -q "$secret"; then
            print_status "GitHub secret $secret exists" 0
        else
            print_status "GitHub secret $secret exists" 1
            echo "Add GitHub secret: $secret"
        fi
    done
else
    print_warning "GitHub CLI not available - manually check repository secrets"
fi

# Check workflow files
echo "Checking workflow files..."
WORKFLOW_FILES=(
    ".github/workflows/deploy-staging.yml"
    ".github/workflows/deploy-production.yml"
    ".github/workflows/deploy-test.yml"
    ".github/workflows/staging-test.yml"
)

for workflow in "${WORKFLOW_FILES[@]}"; do
    if [ -f "$workflow" ]; then
        print_status "Workflow file $workflow exists" 0
    else
        print_status "Workflow file $workflow exists" 1
    fi
done

# Summary
echo ""
echo "🎯 Validation Summary"
echo "===================="
echo "Review any ❌ items above and follow the suggested actions."
echo "Once all items are ✅, your deployment configuration is ready!"
echo ""
echo "Next steps:"
echo "1. Fix any failing validation checks"
echo "2. Test deployment to test environment"
echo "3. Deploy to staging and run validation tests"
echo "4. Deploy to production when ready"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
