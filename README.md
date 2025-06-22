# Project Journal: AI Chaos Engineering Team

This journal documents the major changes, improvements, and decisions made during the current development session.

---

## 2025-06-22 — Session Journal

### ✅ Dependency Management Modernization
- Added and documented usage of `uv` for fast, modern Python dependency management.
- Provided clear instructions for installing dependencies, locking them (`uv.lock`), and installing optional groups.
- Added guidance for using `hatch` and virtual environments, including best practices for not mixing environment managers.
- Updated `QUICK_START.md` to reflect all of the above.

### ✅ Tools and Toolsets Refactor
- Refactored `mcp-toolbox/tools.yaml` to:
  - Use only fields present in the actual BigQuery schema (no more references to non-existent fields).
  - Move all tool definitions under the `tools:` section, with toolsets as lists of tool names under `toolsets:`.
  - Fixed YAML structure errors (mapping vs. sequence) so Toolbox loads without error.
  - Ensured all toolsets (`detector_toolset`, `planner_toolset`, `action_recommender_toolset`) are schema-compliant and functional.

### ✅ Agent Code Modernization
- Refactored `agent_manager/agent.py` to:
  - Use the async ADK Runtime pattern (`async def main()`, `await session_service.create_session`, `async for event in runner.run_async(...)`).
  - Remove legacy synchronous helpers (like `run_local_query`).
  - Ensure all session and event handling is fully async and ADK-compliant.
- Verified that all sub-agents (detector, planner, action_recommender) only use schema-compliant fields.

### ✅ Documentation Improvements
- Added clear, step-by-step quick start for:
  - Using `uv` and `hatch` for dependency management.
  - Running the project with or without a virtual environment.
  - Best practices for environment management.
  - How to install dependencies globally (not recommended for production).
- Clarified that the project does **not** use the ADK CLI for running the agent, but rather standard Python entry points.

### ✅ Error Fixes and Troubleshooting
- Fixed YAML parsing errors in `tools.yaml` by correcting toolset structure.
- Fixed async/sync issues in agent code (e.g., coroutine not awaited, attribute errors).
- Provided schema-compliant queries for all toolsets, ensuring all BigQuery queries run without missing field errors.

---

## Summary
- The project is now fully modernized for Python dependency management, ADK async runtime, and schema-compliant BigQuery analytics.
- All documentation is up to date and user-friendly.
- The codebase is ready for further development, deployment, or onboarding new contributors.

---

*This journal will help future maintainers understand the evolution of the project and the rationale behind key changes.*
