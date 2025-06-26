#!/bin/bash
# Script to set GitHub Actions secrets to a repo using GitHub CLI
# Usage: bash set_github_secrets.sh

REPO="laziestlarry/youtube-ai-platform"

# Prompt for the actual provider ID
read -p "Enter your GCP Workload Identity Provider ID (e.g., my-provider-id): " PROVIDER_ID

# Set secrets

gh secret set GCP_PROJECT_ID --repo $REPO --body "youtube-ai-platform-464016"
gh secret set GCP_WIF_PROVIDER --repo $REPO --body "projects/35665695231/locations/global/workloadIdentityPools/github-actions-pool/providers/gha-oidc"
gh secret set GCP_SERVICE_ACCOUNT --repo $REPO --body "github-actions-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set API_SERVICE_ACCOUNT_EMAIL --repo $REPO --body "api-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set WORKER_SERVICE_ACCOUNT_EMAIL --repo $REPO --body "worker-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set DATABASE_URL --repo $REPO --body "postgresql+asyncpg://admin:lakakula@/youtube-ai-db?host=/cloudsql/youtube-ai-platform-464016:us-central1:youtube-ai-db"
gh secret set GCS_BUCKET_NAME --repo $REPO --body "youtube-ai-platform-464016-youtube-ai-media"
gh secret set SECRET_KEY --repo $REPO --body "lakakula"
gh secret set GEMINI_API_KEY --repo $REPO --body "AIzaSyB1Oh_KvLKItMqztDSKkTfU9BXFG2UgJEw"
gh secret set SERPER_API_KEY --repo $REPO --body "aafeed3bb1ed082b59c6c44b0d6fad60d12799fa"
gh secret set TASK_QUEUE_NAME --repo $REPO --body "youtube-ai-pipeline-queue"

echo "All secrets set for $REPO." 