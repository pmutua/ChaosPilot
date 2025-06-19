# Google Cloud Platform Setup Guide

## Prerequisites
- Google Cloud SDK installed
- gcloud CLI authenticated
- Project with billing enabled

## 1. Initial Setup

```powershell
# Set project
gcloud config set project your-project-id

# Enable required APIs
gcloud services enable `
    aiplatform.googleapis.com `
    cloudsql.googleapis.com `
    storage.googleapis.com
```

## 2. Service Account Setup

```powershell
# Create service account
gcloud iam service-accounts create adk-agents `
    --display-name="ADK Agents Service Account"

# Download key
gcloud iam service-accounts keys create service-account-key.json `
    --iam-account=adk-agents@your-project-id.iam.gserviceaccount.com

# Grant permissions
gcloud projects add-iam-policy-binding your-project-id `
    --member="serviceAccount:adk-agents@your-project-id.iam.gserviceaccount.com" `
    --role="roles/aiplatform.user"
```

## 3. Vertex AI Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Update `.env` with the key:
```plaintext
VERTEX_API_KEY=your-api-key
```

## 4. Verification

Run the verification script:
```powershell
python scripts/verify_gcp.py
```