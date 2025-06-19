set PROJECT_ID=my-project-id
set SERVICE_ACCOUNT_EMAIL=cloud-run-svc@%PROJECT_ID%.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SERVICE_ACCOUNT_EMAIL%" ^
    --role="roles/bigquery.dataEditor"
