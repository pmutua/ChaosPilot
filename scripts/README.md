# ChaosPilot Scripts

This folder contains utility scripts for setting up, running, and testing the ChaosPilot platform on Google Cloud Platform (GCP).

## Script Index

| Script Name                        | Platform      | Purpose                                                                 |
|-------------------------------------|--------------|-------------------------------------------------------------------------|
| assign_iam_roles.bat                | Windows      | Assigns all required IAM roles to the service account for GCP deployment|
| assign_iam_roles.sh                 | Linux/macOS  | Same as above, for Unix-like systems                                    |
| setup-toolbox-service-account.bat   | Windows      | Sets up a service account for MCP Toolbox (local/independent use)       |
| setup-toolbox-service-account.sh    | Linux/macOS  | Same as above, for Unix-like systems                                    |
| run-all.bat                         | Windows      | Starts MCP Toolbox, ADK API server, and frontend for local development  |
| run-all.sh                          | Linux/macOS  | Same as above, for Unix-like systems                                    |
| inject_logs_gcp.py                  | Python       | Injects fake logs into GCP Logging for testing/demo purposes            |

## Usage

- **IAM Role Assignment:**
  - Use `assign_iam_roles.bat` (Windows) or `assign_iam_roles.sh` (Linux/macOS) to set up all required IAM roles for your GCP service account.

- **Toolbox Service Account Setup:**
  - Use `setup-toolbox-service-account.bat` or `.sh` if you need a dedicated service account for MCP Toolbox.

- **Run All Services:**
  - Use `run-all.bat` or `run-all.sh` to start MCP Toolbox, ADK API server, and the frontend in one step for local development.

- **Inject Test Logs:**
  - Use `inject_logs_gcp.py` to simulate error and warning logs in GCP for testing and demo purposes.

## See Also

- [../README.md](../README.md) — Main project overview
- [../docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md](../docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md) — Full setup & deployment guide 