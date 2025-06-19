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
instruction="""
You are the Detector agent.
Based on on **only** user request, provide an analysis of all chaos logs and telemetry data stored in the database.

Output **ONLY** in json FORMAT:
Do not add any other text before or after the json.

Output json example:

```json

{
    "report_generated_at": "2025-06-18T21:50:00Z",
    "total_error_logs": 1,
    "environments_considered": ["prod"],
    "errors_grouped_by_region": {
    "us-central1": {
        "ERROR": 1
    }
  },
  "errors_grouped_by_severity": {
    "ERROR": 1
  },
  "most_frequent_error_types": [
    {
      "failure_type": "disk_stall",
      "count": 1,
      "regions": ["us-central1"]
    }
  ],
  "recent_errors": [
    {
      "id": 1,
      "experiment_id": "exp0001",
      "failure_type": "disk_stall",
      "severity": "ERROR",
      "impact_level": "high",
      "region": "us-central1",
      "timestamp": "2025-06-18T05:07:52.413101+00:00"
    }
  ]
}

```
"""
detector_agent = Agent(
    name="detector",
    model=LiteLlm(model="azure/gpt-4o"),
    output_key="detector_summary",
    description="Forensic observer agent that analyzes operational chaos logs.",
    instruction=instruction,
    tools=tools
)

print(f"✅ Agent '{detector_agent.name}' created using model '{detector_agent.model}'.")




