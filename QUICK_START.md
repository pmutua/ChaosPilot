# 🚀 ChaosPilot Quick Start

## Prerequisites
- Python with ADK installed
- Node.js and npm
- agent_manager backend configured

## ⚠️ **CRITICAL: Enable GCP Services First**

**Before any Cloud Run deployment, you MUST enable these services:**

```bash
export PROJECT_ID="your-gcp-project-id"
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    iam.googleapis.com \
    secretmanager.googleapis.com \
    cloudresourcemanager.googleapis.com \
    containerregistry.googleapis.com
```

**Why this is critical:**
- ❌ Deployment will **FAIL** without these services enabled
- ✅ Only need to do this **once per project**

## Quick Commands

### 1. Start ADK API Server (with CORS)
```bash
cd agent_manager
adk api_server --allow_origins="*"
```

### 2. Test Integration
```bash
python test_adk_integration.py
```

### 3. Start Frontend
```bash
cd web
npm start
```

## One-Click Startup

### Windows
```bash
start_chaospilot.bat
```

### Linux/Mac
```bash
chmod +x start_chaospilot.sh
./start_chaospilot.sh
```

## URLs
- **Frontend**: http://localhost:4200
- **Backend**: http://localhost:8000

## Important Notes
- ✅ Always use `--allow_origins="*"` to avoid CORS errors
- ✅ The agent_manager folder name is used as the app name
- ✅ Session management is handled automatically
- ✅ All 5 agents (detector, planner, action_recommender, fixer, notifier) are available

## Troubleshooting
- **CORS Error**: Make sure you're using the correct ADK command with `--allow_origins="*"`
- **Connection Refused**: Check that the ADK server is running on port 8000
- **Agent Not Found**: Verify agent names match exactly (detector, planner, etc.)
- **GCP Services Not Enabled**: Run the service enablement commands above first 