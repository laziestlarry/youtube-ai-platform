steps:
  # --- Build Stage (Parallel) ---
  # Build the API image
  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-api'
    args:
      - 'build'
      - '-t'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/api:${SHORT_SHA}'
      - '--cache-from'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/api:buildcache'
      - '-f'
      - 'Dockerfile.api'
      - '.'

  # Build the Worker image
  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-worker'
    args:
      - 'build'
      - '-t'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/worker:${SHORT_SHA}'
      - '--cache-from'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/worker:buildcache'
      - '-f'
      - 'Dockerfile.worker'
      - '.'

  # Build the Mini-App image
  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-mini-app'
    args:
      - 'build'
      - '-t'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/mini-app:${SHORT_SHA}'
      - '--cache-from'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/mini-app:buildcache'
      - '-f'
      - 'Dockerfile.mini_app'
      - '.'

  # Build the DB Migration image
  - name: 'gcr.io/cloud-builders/docker'
    id: 'build-db-migrate'
    args:
      - 'build'
      - '-t'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/db-migrate:${SHORT_SHA}'
      - '--cache-from'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/db-migrate:buildcache'
      - '-f'
      - 'Dockerfile.db_migrate'
      - '.'

  # --- DB Migration Stage ---
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'update-db-migration-job'
    # This step implicitly depends on the images being built and pushed
    # because they are listed in the top-level 'images' section.
    entrypoint: gcloud
    args:
      - 'run'
      - 'jobs'
      - 'update'
      - '${PROJECT_ID}-db-migrate'
      - '--image'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/db-migrate:${SHORT_SHA}'
      - '--region'
      - '${_GCP_REGION}'

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'run-db-migration'
    waitFor: ['update-db-migration-job']
    entrypoint: gcloud
    args:
      - 'run'
      - 'jobs'
      - 'execute'
      - '${PROJECT_ID}-db-migrate'
      - '--region'
      - '${_GCP_REGION}'
      - '--wait'

  # --- Deploy Stage ---
  # Deploy the Worker Service
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'deploy-worker'
    waitFor: ['run-db-migration']
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - '${_WORKER_SERVICE_NAME}'
      - '--image'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/worker:${SHORT_SHA}'
      - '--region'
      - '${_GCP_REGION}'
      - '--no-allow-unauthenticated'
      - '--service-account'
      - '${_WORKER_SERVICE_ACCOUNT_EMAIL}'
      - '--update-env-vars=GCP_PROJECT_ID=${PROJECT_ID},GCP_REGION=${_GCP_REGION}'
      - '--set-secrets=DATABASE_URL=DATABASE_URL:latest,GCS_BUCKET_NAME=GCS_BUCKET_NAME:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest,SERPER_API_KEY=SERPER_API_KEY:latest'

  # Deploy the API Service
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'deploy-api'
    waitFor: ['deploy-worker'] # Deploy API after worker to get its URL
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - '${_API_SERVICE_NAME}'
      - '--image'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/api:${SHORT_SHA}'
      - '--region'
      - '${_GCP_REGION}'
      - '--allow-unauthenticated'
      - '--service-account'
      - '${_API_SERVICE_ACCOUNT_EMAIL}'
      - '--update-env-vars=WORKER_URL=$(gcloud run services describe ${_WORKER_SERVICE_NAME} --region=${_GCP_REGION} --format="value(status.url)"),GCP_PROJECT_ID=${PROJECT_ID},GCP_REGION=${_GCP_REGION},TASK_QUEUE_LOCATION=${_GCP_REGION}'
      - '--set-secrets=DATABASE_URL=DATABASE_URL:latest,SECRET_KEY=SECRET_KEY:latest,GCS_BUCKET_NAME=GCS_BUCKET_NAME:latest,TASK_QUEUE_NAME=TASK_QUEUE_NAME:latest,WORKER_SA_EMAIL=WORKER_SA_EMAIL:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest,SERPER_API_KEY=SERPER_API_KEY:latest'

  # Deploy the Mini-App Service
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'deploy-mini-app'
    waitFor: ['deploy-api'] # Deploy Mini-App after API to get its URL
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - '${_MINI_APP_SERVICE_NAME}'
      - '--image'
      - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/mini-app:${SHORT_SHA}'
      - '--region'
      - '${_GCP_REGION}'
      - '--allow-unauthenticated'
      - '--service-account'
      - '${_API_SERVICE_ACCOUNT_EMAIL}'
      - '--update-env-vars=MAIN_PLATFORM_URL=$(gcloud run services describe ${_API_SERVICE_NAME} --region=${_GCP_REGION} --format="value(status.url)"),GCP_PROJECT_ID=${PROJECT_ID},GCP_REGION=${_GCP_REGION}'
      - '--set-secrets=GEMINI_API_KEY=GEMINI_API_KEY:latest,SERPER_API_KEY=SERPER_API_KEY:latest'

images:
  - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/api:${SHORT_SHA}'
  - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/worker:${SHORT_SHA}'
  - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/mini-app:${SHORT_SHA}'
  - '${_GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_IMAGE_NAME}/db-migrate:${SHORT_SHA}'

options:
  logging: CLOUD_LOGGING_ONLY

substitutions:
  _GCP_REGION: 'us-central1'
  _GAR_LOCATION: 'us-central1'
  _API_SERVICE_NAME: 'youtube-ai-platform'
  _MINI_APP_SERVICE_NAME: 'youtube-ai-platform-mini-app'
  _WORKER_SERVICE_NAME: 'youtube-ai-platform-worker'
  _IMAGE_NAME: 'youtube-ai-platform'
  # These secrets need to be configured in the Cloud Build trigger
  _API_SERVICE_ACCOUNT_EMAIL: 'api-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com'
  _WORKER_SERVICE_ACCOUNT_EMAIL: 'worker-service-sa@youtube-ai-platform-464016.iam.gserviceaccount.com'