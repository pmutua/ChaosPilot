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

### ✅ Using uv without a virtual environment

If you want to install dependencies **globally** (not recommended for production, but useful for quick experiments or local scripts), just run:

```bash
uv pip install -r pyproject.toml --system
```

This will install all dependencies into your global Python environment. Be aware this can affect other Python projects on your system.

### ✅ Using a Virtual Environment vs. hatch shell

If you already have a virtual environment active (e.g., you see something like `(AI-Chaos-Engineering-Team)` in your terminal prompt), you do **not** need to use `hatch shell`. Just install dependencies and run your project as usual:

```bash
uv pip install -r pyproject.toml
python agent_manager/agent.py
```

#### When to use `hatch shell`
- Use `hatch shell` if you want Hatch to manage your environment for you, or if you want to use Hatch's features (like environment scripts, reproducibility, etc.).
- If you run `hatch shell` while another venv is active, Hatch will warn you and may use its own environment instead.

#### Best Practice
- **Pick one environment manager per terminal session:**
  - If you're using your own venv (e.g., `.venv`), just activate it and use it.
  - If you want to use Hatch, deactivate your current venv (`deactivate`), then run `hatch shell`.

#### Example: Using your current venv
```bash
# If you see (AI-Chaos-Engineering-Team) in your prompt, you're already in your venv!
uv pip install -r pyproject.toml
python agent_manager/agent.py
```

#### Example: Switching to Hatch
```bash
deactivate  # Leave your current venv
hatch shell # Enter Hatch-managed environment
uv pip install -r pyproject.toml
python agent_manager/agent.py
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

### ✅ Running the Agent with ADK (Recommended)

This project uses the ADK CLI for running the agent, not direct `uvicorn` or `python` commands.

To run your agent with the ADK Runtime, use:

```bash
adk run --core
```

- The `--core` flag ensures the agent runs with the core ADK runtime engine.
- This will automatically discover your agent in `agent_manager/agent.py` and start the event loop as described in the documentation.

> **Note:** You can still use `uv`, `venv`, or `hatch` for dependency management and environment setup, but always use the ADK CLI to run the agent. 