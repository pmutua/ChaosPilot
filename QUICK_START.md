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

## 🚀 Quick Start with uv

### ✅ Step 1: Install dependencies with uv
Since your `pyproject.toml` already defines dependencies, just run:

```bash
uv pip install -r pyproject.toml
```
This will:
- Install all dependencies in your current environment (or virtual environment).
- Respect your `[project.dependencies]` and optionally `[project.optional-dependencies]`.

### ✅ Step 2: Optional – Create uv.lock for reproducibility
If you want to lock all dependencies:

```bash
uv pip compile pyproject.toml > uv.lock
```
This generates a `uv.lock` file — similar to `poetry.lock` or `Pipfile.lock` — so your team or CI installs the exact same versions.

### ✅ Step 3: Install optional dependencies (like lint)
If you want to install the `lint` group too:

```bash
uv pip install -r pyproject.toml --extra lint
```
Or if you have multiple groups:

```bash
uv pip install -r pyproject.toml --extra lint --extra dev
```

### ✅ Step 4: Running the project
How you run the project depends on your entry point. For example, if you have a `main.py` or are using `uvicorn`, you can do:

```bash
uvicorn agent_manager.main:app --reload
```
Replace `agent_manager.main:app` with your actual entry point if different (e.g., `agent_manager.agent:main`).

### ✅ Step 5: (Optional) Use hatch
If you're also using hatch, you can activate the environment like this:

```bash
hatch shell
```
Then just run Python commands normally.

You can also define a custom script in `pyproject.toml` under `[tool.hatch.envs.default.scripts]` like:

```toml
[tool.hatch.envs.default.scripts]
start = "uvicorn agent_manager.main:app --reload"
```
Then run:

```bash
hatch run start
```

### Summary of Commands
| Purpose                        | Command                                             |
|--------------------------------|-----------------------------------------------------|
| Install dependencies           | `uv pip install -r pyproject.toml`                  |
| Install optional groups        | `uv pip install -r pyproject.toml --extra lint`     |
| Lock deps                      | `uv pip compile pyproject.toml > uv.lock`           |
| Run app with uvicorn           | `uvicorn agent_manager.main:app --reload`           |
| Open shell with hatch          | `hatch shell`                                       |
| Run custom script (if defined) | `hatch run start`                                   |

## Quick Commands

uv pip install -r pyproject.toml


### 1. Start ADK API Server (with CORS)
```bash
cd agent_manager
adk api_server --allow_origins="*"
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