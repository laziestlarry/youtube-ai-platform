#!/bin/bash

# A script to find and delete lingering resources from a previous project name.
# WARNING: This script performs destructive actions. Review each prompt carefully.

# --- Configuration ---
# The name or prefix of the old resources you want to find and delete.
OLD_PROJECT_PREFIX="youtube-monetization-mvp"

# --- Automatic Configuration ---
# It's recommended to set this explicitly to avoid errors.
GCP_PROJECT_ID=$(gcloud config get-value project)
# Change if your resources are in a different region
GCP_REGION=$(gcloud config get-value run/region 2>/dev/null || echo "us-central1") 

echo "--- GCP Cleanup Script ---"
echo "Project: $GCP_PROJECT_ID"
echo "Region:  $GCP_REGION"
echo "Target:  Resources containing the name '$OLD_PROJECT_PREFIX'"
echo "--------------------------"
echo "WARNING: This script will propose to PERMANENTLY DELETE resources."
read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Function to prompt for deletion
confirm_and_delete() {
    local resource_type=$1
    local resource_name=$2
    local delete_command=$3

    read -p "--> Found ${resource_type}: '${resource_name}'. Delete it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Deleting ${resource_name}..."
        # Use eval to correctly execute the command string with arguments
        eval $delete_command
        if [ $? -eq 0 ]; then
            echo "Successfully deleted."
        else
            echo "ERROR: Failed to delete ${resource_name}."
        fi
    else
        echo "Skipping."
    fi
}

# 1. Cloud Run Services
echo -e "\n--- Searching for Cloud Run Services ---"
SERVICES=$(gcloud run services list --platform=managed --region=$GCP_REGION --filter="service:${OLD_PROJECT_PREFIX}" --format="value(name)")
if [ -z "$SERVICES" ]; then
    echo "No matching Cloud Run services found."
else
    for service in $SERVICES; do
        confirm_and_delete "Cloud Run Service" "$service" "gcloud run services delete $service --platform=managed --region=$GCP_REGION --quiet"
    done
fi

# 2. Artifact Registry Repositories
echo -e "\n--- Searching for Artifact Registry Repositories ---"
REPOS=$(gcloud artifacts repositories list --location=$GCP_REGION --filter="name~${OLD_PROJECT_PREFIX}" --format="value(repository)")
if [ -z "$REPOS" ]; then
    echo "No matching Artifact Registry repositories found."
else
    for repo in $REPOS; do
        echo "--> Found Artifact Registry Repo: '${repo}'. Note: This will delete the repo and all images inside."
        confirm_and_delete "Artifact Registry Repo" "$repo" "gcloud artifacts repositories delete $repo --location=$GCP_REGION --quiet"
    done
fi

# 3. Cloud SQL Instances
echo -e "\n--- Searching for Cloud SQL Instances ---"
SQL_INSTANCES=$(gcloud sql instances list --filter="name~${OLD_PROJECT_PREFIX}" --format="value(name)")
if [ -z "$SQL_INSTANCES" ]; then
    echo "No matching Cloud SQL instances found."
else
    for instance in $SQL_INSTANCES; do
        echo "--> Found Cloud SQL Instance: '${instance}'. Note: You may need to disable deletion protection first."
        confirm_and_delete "Cloud SQL Instance" "$instance" "gcloud sql instances delete $instance --quiet"
    done
fi

# 4. GCS Buckets
echo -e "\n--- Searching for GCS Buckets ---"
BUCKETS=$(gcloud storage buckets list --format="value(name)" | grep "${OLD_PROJECT_PREFIX}")
if [ -z "$BUCKETS" ]; then
    echo "No matching GCS buckets found."
else
    for bucket in $BUCKETS; do
        echo "--> Found GCS Bucket: '${bucket}'. This will delete the bucket and ALL its contents."
        confirm_and_delete "GCS Bucket" "$bucket" "gcloud storage rm -r $bucket"
    done
fi

# 5. IAM Service Accounts
echo -e "\n--- Searching for IAM Service Accounts ---"
SERVICE_ACCOUNTS=$(gcloud iam service-accounts list --filter="displayName~${OLD_PROJECT_PREFIX} OR email~${OLD_PROJECT_PREFIX}" --format="value(email)")
if [ -z "$SERVICE_ACCOUNTS" ]; then
    echo "No matching IAM service accounts found."
else
    for sa in $SERVICE_ACCOUNTS; do
        confirm_and_delete "IAM Service Account" "$sa" "gcloud iam service-accounts delete $sa --quiet"
    done
fi

echo -e "\n--- Cleanup Script Finished ---"
