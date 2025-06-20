@echo off
setlocal

REM Set your GCP project ID
set PROJECT_ID=aceti-462716
set SA_NAME=toolbox-identity
set SA_EMAIL=%SA_NAME%@%PROJECT_ID%.iam.gserviceaccount.com

echo 🔧 Creating service account: %SA_NAME%
gcloud iam service-accounts create %SA_NAME% --project=%PROJECT_ID%

echo 🔐 Granting Secret Manager access...
gcloud projects add-iam-policy-binding %PROJECT_ID% --member=serviceAccount:%SA_EMAIL% --role=roles/secretmanager.secretAccessor

echo 💾 Granting Cloud SQL Client access...
gcloud projects add-iam-policy-binding %PROJECT_ID% --member=serviceAccount:%SA_EMAIL% --role=roles/cloudsql.client

echo ✅ Done configuring service account: %SA_EMAIL%
endlocal
