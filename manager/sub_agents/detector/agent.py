# chaos_commander.py

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

from toolbox_core import ToolboxSyncClient

load_dotenv()


toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
# Load all the tools
tools = toolbox.load_toolset('detector_toolset')


AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")


detector_agent = None
# --- Agent: Detector ---
# This agent analyzes chaos logs and system health metrics to detect anomalies and summarize findings.
# It is responsible for identifying patterns, frequencies, and severities of events across the system.
# It also provides actionable recommendations based on the analysis.
# It does not perform any actions itself, but provides structured data for other agents to act upon
# (e.g., action_recommender, planner).
# It is designed to work in conjunction with other agents like stats_agent, planner_agent, fixer_agent, and cost_optimizer_agent.
# It is the first step in the incident response workflow, providing the necessary data for further analysis
# and action planning.
instruction = """
You are the Detector agent.

Your task is to analyze chaos logs and telemetry data stored in the BigQuery table `aceti-462716.bqexport.chaospilot_fake_logs_20250620`.

Use ONLY the following fields from the dataset (nested inside `jsonPayload` unless specified otherwise):

- `jsonPayload.experiment_id`
- `jsonPayload.agent_id`
- `jsonPayload.message`
- `jsonPayload.region`
- `jsonPayload.timestamp`
- `severity` (top-level)
- `jsonPayload.details.user_id`
- `jsonPayload.httprequest.*`
- `jsonPayload.status_code`

Respond **only** when explicitly asked by the user. Do not trigger analysis independently.

You MUST output your response in **JSON format only** — with no explanation, logs, or comments before or after. The structure should match the sample below.

Ensure all fields are extracted using the correct BigQuery schema. Format timestamps in ISO 8601 (UTC). Aggregate, count, group, and deduplicate where necessary.

Example output:

```json
{
  "report_generated_at": "2025-06-20T10:15:00Z",
  "total_error_logs": 3,
  "environments_considered": ["prod"],
  "errors_grouped_by_region": {
    "us-central1": {
      "CRITICAL": 2,
      "ERROR": 1
    }
  },
  "errors_grouped_by_severity": {
    "CRITICAL": 2,
    "ERROR": 1
  },
  "most_frequent_error_types": [
    {
      "failure_type": "database crash",
      "count": 2,
      "regions": ["us-central1"]
    },
    {
      "failure_type": "out of memory",
      "count": 1,
      "regions": ["us-central1"]
    }
  ],
  "recent_errors": [
    {
      "experiment_id": "exp4851",
      "failure_type": "database crash",
      "severity": "CRITICAL",
      "impact_level": "high",
      "region": "us-central1",
      "timestamp": "2025-06-20T01:14:59.147Z"
    },
    {
      "experiment_id": "exp4851",
      "failure_type": "out of memory",
      "severity": "ERROR",
      "impact_level": "medium",
      "region": "us-central1",
      "timestamp": "2025-06-20T00:12:45.983Z"
    }
  ]
}
⚠️ Do not include fields that are not present in the BigQuery schema.
⚠️ Only use jsonPayload keys for nested values.
⚠️ Do not invent values. Use real data and proper aggregation from the query tools.
"""
detector_agent = Agent(
    name="detector",
    model=LiteLlm(model="azure/gpt-4o"),
    output_key="detector_summary",
    description="The Detector Agent is an AI-powered bot that analyzes chaos logs in BigQuery to identify critical errors, failure patterns, and system anomalies in real time.",
    instruction=instruction,
    tools=tools
)

print(f"✅ Agent '{detector_agent.name}' created using model '{detector_agent.model}'.")




