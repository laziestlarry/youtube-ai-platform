#!/bin/bash
# Set all required GitHub Actions secrets for a specific environment.
# Usage: ./set_all_github_secrets.sh <environment_name>
# Example: ./set_all_github_secrets.sh production

set -e

REPO="laziestlarry/youtube-ai-platform"
ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  echo "Error: No environment name provided."
  echo "Usage: $0 <environment_name> (e.g., staging, production, test)"
  exit 1
fi

echo "--- Setting secrets for environment: '$ENVIRONMENT' in repo: '$REPO' ---"

# --- GCP & Deployment Secrets (Usually the same across environments) ---
gh secret set GCP_WORKLOAD_IDENTITY_PROVIDER --repo $REPO --env "$ENVIRONMENT" --body "projects/35665695231/locations/global/workloadIdentityPools/github-actions-pool/providers/gha-oidc"
gh secret set GCP_SERVICE_ACCOUNT_EMAIL --repo $REPO --env "$ENVIRONMENT" --body "github-actions-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set API_SERVICE_ACCOUNT_EMAIL --repo $REPO --env "$ENVIRONMENT" --body "api-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set WORKER_SERVICE_ACCOUNT_EMAIL --repo $REPO --env "$ENVIRONMENT" --body "worker-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com"
gh secret set GCP_PROJECT_ID --repo $REPO --env "$ENVIRONMENT" --body "youtube-ai-platform-464016"

# --- Application & Environment-Specific Secrets (Prompt for values) ---

# Function to prompt for a secret
prompt_for_secret() {
  local secret_name=$1
  local current_value
  read -p "Enter value for $secret_name: " current_value
  gh secret set "$secret_name" --repo "$REPO" --env "$ENVIRONMENT" --body "$current_value"
}

# Prompt for DATABASE_URL
echo "Please provide the DATABASE_URL for the '$ENVIRONMENT' environment."
echo "Example: postgresql+asyncpg://user:password@private-ip:5432/database_name"
prompt_for_secret "DATABASE_URL"

prompt_for_secret "GCS_BUCKET_NAME"
prompt_for_secret "TASK_QUEUE_NAME"
prompt_for_secret "SECRET_KEY"
prompt_for_secret "GEMINI_API_KEY"
prompt_for_secret "SERPER_API_KEY"
prompt_for_secret "REDIS_URL"
prompt_for_secret "GOOGLE_CLIENT_ID"
prompt_for_secret "GOOGLE_CLIENT_SECRET"

echo "✅ Secrets have been sent to GitHub."

echo "--- Verifying secrets for environment: '$ENVIRONMENT' ---"
echo "The following secrets are now configured for the '$ENVIRONMENT' environment:"
gh secret list --repo $REPO --env "$ENVIRONMENT"