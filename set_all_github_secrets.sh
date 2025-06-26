#!/bin/bash
# Set all required GitHub Actions secrets for youtube-ai-platform, stripping spaces from names

REPO="laziestlarry/youtube-ai-platform"

# Prompt for DATABASE_URL
read -p "Enter your DATABASE_URL (or press Enter to use the recommended default): " DBURL
if [ -z "$DBURL" ]; then
  DBURL="postgresql+asyncpg://admin:lakakula@/youtube-ai-db?host=/cloudsql/youtube-ai-platform-464016:us-central1:youtube-ai-db"
fi

# Set secrets (strip spaces from names)
gh secret set GCP_WIF_PROVIDER --repo $REPO --body "projects/35665695231/locations/global/workloadIdentityPools/github-actions-pool/providers/gha-oidc"
gh secret set GCP_SERVICE_ACCOUNT --repo $REPO --body "github-actions-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set API_SERVICE_ACCOUNT_EMAIL --repo $REPO --body "api-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set WORKER_SERVICE_ACCOUNT_EMAIL --repo $REPO --body "worker-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set GCP_PROJECT_ID --repo $REPO --body "youtube-ai-platform-464016"
gh secret set GCS_BUCKET_NAME --repo $REPO --body "youtube-ai-platform-464016-youtube-ai-media"
gh secret set TASK_QUEUE_NAME --repo $REPO --body "youtube-ai-pipeline-queue"
gh secret set SECRET_KEY --repo $REPO --body "lakakula"
gh secret set GEMINI_API_KEY --repo $REPO --body "AIzaSyDYIXAH_YQ_mbVIdrlBEvxHM-GosTCwR1o"
gh secret set SERPER_API_KEY --repo $REPO --body "807f4d9723e8aec44b2b725647e69ec656e0b5be"
gh secret set DATABASE_URL --repo $REPO --body "$DBURL"

echo "All secrets set for $REPO (with names stripped of spaces)."