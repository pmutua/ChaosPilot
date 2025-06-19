PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_EMAIL=cloud-run-svc@$PROJECT_ID.iam.gserviceaccount.com

# Allow writing logs
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/logging.logWriter"

# Allow querying BigQuery
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/bigquery.jobUser"

# (Optional) Allow writing to BigQuery
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/bigquery.dataEditor"
