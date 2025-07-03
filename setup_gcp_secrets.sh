#!/bin/bash

# GCP Secrets Setup Script
# This script creates all required secrets in Google Secret Manager for the YouTube AI Platform

set -e

PROJECT_ID=${1:-"youtube-ai-platform-464016"}
REGION=${2:-"us-central1"}

echo "Setting up GCP secrets for project: $PROJECT_ID"

# Required secrets for the application
SECRETS=(
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

# Create secrets (will prompt for values or read from environment)
for secret in "${SECRETS[@]}"; do
    if gcloud secrets describe "$secret" --project="$PROJECT_ID" >/dev/null 2>&1; then
        echo "Secret $secret already exists, skipping creation..."
    else
        echo "Creating secret: $secret"
        if [ -n "${!secret}" ]; then
            echo "Using value from environment variable $secret"
            echo -n "${!secret}" | gcloud secrets create "$secret" --project="$PROJECT_ID" --data-file=-
        else
            echo "Please enter value for $secret:"
            read -s value
            echo -n "$value" | gcloud secrets create "$secret" --project="$PROJECT_ID" --data-file=-
        fi
        echo "Created secret: $secret"
    fi
done

echo "✅ All secrets have been created in Secret Manager"
echo ""
echo "Next steps:"
echo "1. Ensure your service accounts have access to these secrets"
echo "2. Update GitHub repository secrets for CI/CD"
echo "3. Test your deployment workflows"

# Grant access to service accounts
API_SA="api-service-sa@$PROJECT_ID.iam.gserviceaccount.com"
WORKER_SA="worker-service-sa@$PROJECT_ID.iam.gserviceaccount.com"

echo "Granting secret access to service accounts..."

for secret in "${SECRETS[@]}"; do
    echo "Granting access to $secret..."
    gcloud secrets add-iam-policy-binding "$secret" \
        --project="$PROJECT_ID" \
        --member="serviceAccount:$API_SA" \
        --role="roles/secretmanager.secretAccessor"
    
    gcloud secrets add-iam-policy-binding "$secret" \
        --project="$PROJECT_ID" \
        --member="serviceAccount:$WORKER_SA" \
        --role="roles/secretmanager.secretAccessor"
done

echo "✅ Service account permissions granted"
