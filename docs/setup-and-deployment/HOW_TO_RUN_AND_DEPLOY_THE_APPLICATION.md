# ChaosPilot Setup & Deployment Guide

This document provides a comprehensive guide to set up, run, and deploy the ChaosPilot application for autonomous log analysis and incident response.

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [GCP Setup](#-gcp-setup)
3. [Local Development Setup](#-local-development-setup)
4. [Running the Application](#-running-the-application)
5. [Testing with Simulated Logs](#-testing-with-simulated-logs)
6. [Production Deployment](#-production-deployment)
7. [Troubleshooting](#-troubleshooting)

---

## ✅ Prerequisites

### Required Software
- **Google Cloud CLI** - [Install Guide](https://cloud.google.com/sdk/docs/install-sdk)
- **Python 3.8+** with virtual environment support
- **Node.js 16+** and npm
- **Git**

### Required Python Libraries
```bash
google-adk==1.3.0
toolbox==1.11.0
google-cloud-logging==3.12.1
```

### Required Tools
- [MCP Toolbox for Databases](https://googleapis.github.io/genai-toolbox/getting-started/local_quickstart/) (platform-specific)

---

## 🏗️ GCP Setup

### Step 1: Initialize Google Cloud CLI

```bash
# Install and initialize gcloud CLI
gcloud init

# Set your project (create new or use existing)
gcloud projects create chaos-lab --set-as-default
# OR use existing project
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Enable Required APIs

```bash
# Enable all required services
gcloud services enable \
    logging.googleapis.com \
    bigquery.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    iam.googleapis.com \
    secretmanager.googleapis.com \
    serviceusage.googleapis.com
```

### Step 3: Set Up Billing

**Critical**: Billing must be enabled for API activation.

```bash
# Check if billing is enabled
gcloud beta billing projects describe YOUR_PROJECT_ID

# If billing is not enabled, link a billing account
gcloud beta billing accounts list
gcloud beta billing projects link YOUR_PROJECT_ID \
    --billing-account=YOUR_BILLING_ACCOUNT_ID
```

### Step 4: Create Service Account and Assign IAM Roles

**Option A: Use Automated Scripts**

**Windows:**
```bash
# Update PROJECT_ID in the script first, then run:
scripts/assign_iam_roles.bat
```

**Linux/macOS:**
```bash
chmod +x scripts/assign_iam_roles.sh
./scripts/assign_iam_roles.sh
```

**Option B: Manual Setup**

```bash
# Create service account
gcloud iam service-accounts create cloud-run-svc \
    --display-name="Cloud Run Logging Service Account"

# Assign required roles
SERVICE_ACCOUNT="cloud-run-svc@YOUR_PROJECT_ID.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/run.developer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/iam.serviceAccountUser"
```

---

## 💻 Local Development Setup

### Step 1: Clone and Navigate to Project

```bash
git clone https://github.com/pmutua/ChaosPilot
cd ChaosPilot
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure MCP Toolbox

**Windows:** Use the provided `mcp-toolbox/toolbox.exe`
**Linux/macOS:** Download the appropriate binary from [MCP Toolbox](https://googleapis.github.io/genai-toolbox/getting-started/local_quickstart/)

### Step 4: Set Up Frontend

```bash
cd web
npm install
cd ..
```

---

## 🚀 Running the Application

### Option 1: One-Click Startup (Recommended)

**Windows:**
```bash
start_chaospilot.bat
```

**Linux/macOS:**
```bash
chmod +x start_chaospilot.sh
./start_chaospilot.sh
```

### Option 2: Utility Scripts (Alternative)

- **Run All Services for Local Dev:**
  - Use `scripts/run-all.bat` (Windows) or `scripts/run-all.sh` (Linux/macOS) to start MCP Toolbox, ADK API server, and the frontend in one step.

- **Setup Toolbox Service Account:**
  - Use `scripts/setup-toolbox-service-account.bat` (Windows) or `scripts/setup-toolbox-service-account.sh` (Linux/macOS) if you need a dedicated service account for MCP Toolbox.

### Option 3: Manual Startup

#### Step 1: Start MCP Toolbox

```bash
cd mcp-toolbox

# Windows
toolbox

# Linux/macOS
./toolbox --tools-file="tools.yaml"
```

#### Step 2: Start ADK API Server (with CORS)

```bash
cd agent_manager
adk api_server --allow_origins="*"
```

#### Step 3: Start Frontend

```bash
cd web
npm start
```

### Option 4: Development UI

```bash
# In the root directory
adk web
```

Then:
1. Open http://localhost:8000 in your browser
2. Select "agent_manager" from the dropdown
3. Start MCP Toolbox in a separate terminal
4. Chat with your agent

### Option 5: Direct Agent Interaction

```bash
# Make sure MCP Toolbox is running first
adk run agent_manager
```

---

## 🧪 Testing with Simulated Logs

### Generate Test Logs

```bash
# Inject simulated error and warning logs
python scripts/inject_logs_gcp.py
```

### Verify Logs in GCP Console

1. Go to **Google Cloud Console** → **Logging** → **Logs Explorer**
2. Filter by: `severity = ("ERROR" OR "WARNING")`
3. Verify logs are visible

### Export Logs to BigQuery

1. Go to **Log Router**: https://console.cloud.google.com/logs/routing
2. Click **"Create Sink"**
3. Configure:
   - **Sink Name**: `warnings-errors-sink`
   - **Sink Destination**: `BigQuery dataset`
   - **Inclusion Filter**: `severity = ("ERROR" OR "WARNING")`
4. Click **"Create Sink"**

### Verify BigQuery Export

1. Go to **BigQuery** in GCP Console
2. Check your dataset for the exported logs
3. Wait a few minutes for logs to appear

---

## 🚀 Production Deployment to Google Cloud Run

### ⚠️ **CRITICAL: Enable Required Services FIRST**

**Before any deployment can work, you MUST enable these Google Cloud services in your project:**

```bash
# Set your project ID
export PROJECT_ID="your-gcp-project-id"

# Enable ALL required services (DO THIS FIRST!)
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    iam.googleapis.com \
    secretmanager.googleapis.com \
    cloudresourcemanager.googleapis.com \
    containerregistry.googleapis.com
```

**Why this is critical:**
- ❌ Cloud Run deployment will **FAIL** if services aren't enabled
- ❌ Build processes will **FAIL** without Cloud Build
- ❌ Container registry access will **FAIL** without Artifact Registry
- ❌ Service account operations will **FAIL** without IAM
- ✅ Enabling services can take a few minutes
- ✅ You only need to do this **once per project**

### 8.1 Deploy Agent Manager to Cloud Run

#### Step 1: Set Environment Variables
```bash
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export AGENT_PATH="./agent_manager"
export SERVICE_NAME="chaospilot-agent-service"
export APP_NAME="chaospilot-agent-app"
export GOOGLE_GENAI_USE_VERTEXAI=True
```

#### Step 2: Authenticate and Configure
```bash
# Authenticate with Google Cloud
gcloud auth login

# Set the active project
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Verify services are enabled
gcloud services list --enabled --filter="name:run.googleapis.com OR name:cloudbuild.googleapis.com"
```

#### Step 3: Deploy Agent Manager
```bash
# Deploy with ADK CLI (recommended)
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=$SERVICE_NAME \
  --app_name=$APP_NAME \
  --with_ui \
  $AGENT_PATH
```

**When prompted:** Enter `y` to allow unauthenticated invocations for public access.

#### Step 4: Verify Deployment
After successful deployment, you'll get a service URL like:
```
Service URL: https://chaospilot-agent-service-xxxxxx-uc.a.run.app
```

Test the deployment:
- Visit the URL in your browser to access the ADK dev UI
- Test agent functionality through the web interface

### 8.2 Deploy MCP Toolbox to Cloud Run

#### Step 1: Create Service Account for Toolbox
```bash
# Create dedicated service account for toolbox
gcloud iam service-accounts create toolbox-identity \
  --display-name="MCP Toolbox Service Account"

# Assign required roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/cloudsql.client
```

#### Step 2: Upload Configuration
```bash
# Upload tools.yaml as a secret
cd mcp-toolbox
gcloud secrets create tools --data-file=tools.yaml

# Set toolbox image
export IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest
```

#### Step 3: Deploy MCP Toolbox
```bash
gcloud run deploy toolbox \
  --image $IMAGE \
  --service-account toolbox-identity \
  --region us-central1 \
  --set-secrets "/app/tools.yaml=tools:latest" \
  --args="--tools_file=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
  --allow-unauthenticated
```

#### Step 4: Verify Toolbox Deployment
After deployment, you'll get a service URL like:
```
Service URL: https://toolbox-xxxxxx-uc.a.run.app
```

Test the toolbox:
- Visit `https://toolbox-xxxxxx-uc.a.run.app/api/toolset` to see available tools
- The page should display the tools configuration

### 8.3 Integrate Agent with Cloud Toolbox

#### Update Agent Configuration
In your `agent_manager/agent.py`, update the toolbox URL to point to the Cloud Run service:

```python
# Replace localhost URL with Cloud Run URLFIX this 
toolbox = ToolboxTool("https://toolbox-xxxxxx-uc.a.run.app")
```

#### Redeploy Agent (if needed)
If you updated the agent configuration, redeploy:
```bash
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=$SERVICE_NAME \
  --app_name=$APP_NAME \
  --with_ui \
  $AGENT_PATH
```

### 8.4 Production URLs

After successful deployment, you'll have:

| Service | URL Pattern | Purpose |
|---------|-------------|---------|
| **Agent Manager** | `https://chaospilot-agent-service-xxxxxx-uc.a.run.app` | Main agent API and UI |
| **MCP Toolbox** | `https://toolbox-xxxxxx-uc.a.run.app` | Database and tool services |

### 8.5 Troubleshooting Cloud Run Deployment

#### Common Issues:

1. **"Service not enabled" errors:**
   ```bash
   # Re-enable services
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com
   ```

2. **Authentication errors:**
   ```bash
   # Re-authenticate
   gcloud auth login
   gcloud auth application-default login
   ```

3. **Permission errors:**
   ```bash
   # Check if you have the Cloud Run Admin role
   gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" --format="table(bindings.role)" --filter="bindings.members:$(gcloud config get-value account)"
   ```

4. **Build failures:**
   - Check Cloud Build logs in the Google Cloud Console
   - Verify your `requirements.txt` or `pyproject.toml` is correct
   - Ensure all dependencies are available

#### Monitoring:
- **Cloud Run Console:** Monitor service health and logs
- **Cloud Build:** Check build logs for deployment issues
- **IAM & Admin:** Verify service account permissions

### 8.6 Cost Optimization

- **Cloud Run:** Pay only for actual usage (scales to zero)
- **Cloud Build:** Free tier includes 120 build-minutes/day
- **Secret Manager:** First 6,000 operations/month are free
- **IAM:** No additional cost

### 8.7 Security Best Practices

1. **Use service accounts** (already configured above)
2. **Store secrets in Secret Manager** (already done for tools.yaml)
3. **Consider removing `--allow-unauthenticated`** for production
4. **Set up proper IAM roles** for your team members
5. **Enable audit logging** for security monitoring

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Service Enablement Errors

**Error**: `FAILED_PRECONDITION` or permission denied

**Solution**:
- Ensure billing is enabled: `gcloud beta billing projects describe YOUR_PROJECT_ID`
- Link billing account if needed
- Verify you have `roles/serviceusage.serviceUsageAdmin` role

#### 2. CORS Errors

**Error**: Frontend can't connect to ADK API

**Solution**:
- Use `adk api_server app --allow_origins="*"`
- Ensure frontend is running on port 4200
- Check that ADK server is accessible

#### 3. Service Account Not Found

**Error**: `Service account does not exist`

**Solution**:
- Run the IAM role assignment scripts again
- Verify service account name matches exactly
- Check project ID is correct

#### 4. Agent Not Found

**Error**: Agent not available in dropdown

**Solution**:
- Ensure you're running `adk web` from the parent directory of `agent_manager`
- Check that `agent_manager` folder contains valid agent code
- Verify all dependencies are installed

#### 5. MCP Toolbox Connection Issues

**Error**: Toolbox not connecting

**Solution**:
- Ensure toolbox is running before starting ADK
- Check `tools.yaml` configuration
- Verify network connectivity

### Debug Commands

```bash
# Check enabled services
gcloud services list --enabled

# Verify service account
gcloud iam service-accounts describe cloud-run-svc@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Test ADK API
curl -X POST http://localhost:8000/apps/agent_manager/users/test/sessions/test \
    -H "Content-Type: application/json" \
    -d '{"state": {"test": true}}'

# Check logs
gcloud logging read "resource.type=cloud_run_revision" --limit=10
```

---

## 📚 Additional Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [MCP Toolbox Guide](https://googleapis.github.io/genai-toolbox/)
- [Cloud Run Deployment](https://cloud.google.com/run/docs/deploy)
- [BigQuery Export](https://cloud.google.com/logging/docs/export/configure_export_v2)

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Start everything (Windows)
start_chaospilot.bat

# Start everything (Linux/macOS)
./start_chaospilot.sh

# Manual startup
cd mcp-toolbox && toolbox &  # Start toolbox
cd agent_manager && adk api_server app --allow_origins="*" &  # Start ADK
cd web && npm start  # Start frontend

# Test integration
python test_adk_integration.py
```

### Key URLs
- **Frontend**: http://localhost:4200
- **ADK API**: http://localhost:8000
- **Dev UI**: http://localhost:8000 (when using `adk web`)

### Important Notes
- ✅ Always use `--allow_origins="*"` for ADK API server
- ✅ Start MCP Toolbox before ADK server
- ✅ Ensure billing is enabled for GCP services
- ✅ Use the correct service account for deployments 