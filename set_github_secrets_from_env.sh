#!/bin/bash
# Usage: ./set_github_secrets_from_env.sh path/to/.env

REPO="laziestlarry/youtube-ai-platform"
ENV_FILE="${1:-.env}"

if [ ! -f "$ENV_FILE" ]; then
  echo "File $ENV_FILE not found!"
  exit 1
fi

while IFS='=' read -r key value; do
  # Skip comments and empty lines
  [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
  # Remove possible quotes and whitespace
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | sed -e 's/^["'\'']//;s/["'\'']$//')
  gh secret set "$key" --repo "$REPO" --body "$value"
  echo "Set secret: $key"
done < "$ENV_FILE"

echo "✅ All secrets from $ENV_FILE set for $REPO." 