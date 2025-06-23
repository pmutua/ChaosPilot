@echo off
SET PROJECT_ID=aceti-462716
SET SERVICE_ACCOUNT_NAME=cloud-run-svc
SET SERVICE_ACCOUNT_EMAIL=%SERVICE_ACCOUNT_NAME%@%PROJECT_ID%.iam.gserviceaccount.com

echo Enabling required GCP services...
gcloud services enable ^
    logging.googleapis.com ^
    bigquery.googleapis.com ^
    run.googleapis.com ^
    cloudbuild.googleapis.com ^
    artifactregistry.googleapis.com ^
    iam.googleapis.com ^
    secretmanager.googleapis.com

echo Creating service account: %SERVICE_ACCOUNT_NAME%
gcloud iam service-accounts create %SERVICE_ACCOUNT_NAME% ^
    --project=%PROJECT_ID% ^
    --display-name="Cloud Run Logging Service Account"

echo Granting IAM roles to: %SERVICE_ACCOUNT_EMAIL%

REM Allow deployment to Cloud Run
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/run.developer"

REM Allow log writing to Cloud Logging
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/logging.logWriter"

REM Allow access to Secret Manager
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/secretmanager.secretAccessor"

REM Allow writing logs to BigQuery via sink
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/bigquery.dataEditor"

REM Allow this service account to be used by other services
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/iam.serviceAccountUser"

echo.
echo ✅ Setup complete.
echo You can now deploy your Cloud Run service using:
echo.
echo gcloud run deploy [YOUR_SERVICE_NAME] ^
    --image=gcr.io/%PROJECT_ID%/[YOUR_IMAGE] ^
    --region=us-central1 ^
    --platform=managed ^
    --service-account=%SERVICE_ACCOUNT_EMAIL% ^
    --allow-unauthenticated ^
    --project=%PROJECT_ID%
echo.
pause
