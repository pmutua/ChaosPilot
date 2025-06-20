#!/bin/bash

set -e

# Set variables
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_NAME="cloud-run-svc"
SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"

echo "🔧 Enabling required services..."
gcloud services enable \
    logging.googleapis.com \
    bigquery.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    iam.googleapis.com \
    secretmanager.googleapis.com

echo "👤 Creating service account: $SERVICE_ACCOUNT_NAME"
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --project=$PROJECT_ID \
    --display-name="Cloud Run Logging Service Account" || echo "ℹ️ Service account already exists."

echo "🔐 Granting IAM roles to $SERVICE_ACCOUNT_EMAIL..."

# Allow deployment to Cloud Run
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/run.developer"

# Allow Cloud Run service to write logs
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/logging.logWriter"

# Allow access to Secret Manager
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/secretmanager.secretAccessor"

# Allow BigQuery sink write access
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/bigquery.dataEditor"

# Allow querying BigQuery
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/bigquery.jobUser"

# Allow the service account to be used
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/iam.serviceAccountUser"

echo "✅ Setup complete."
echo "You can now deploy to Cloud Run using:"
echo
echo "gcloud run deploy [YOUR_SERVICE_NAME] \\"
echo "  --image=gcr.io/$PROJECT_ID/[YOUR_IMAGE] \\"
echo "  --region=us-central1 \\"
echo "  --platform=managed \\"
echo "  --service-account=$SERVICE_ACCOUNT_EMAIL \\"
echo "  --allow-unauthenticated \\"
echo "  --project=$PROJECT_ID"
