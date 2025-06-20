# chaos_commander.py

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv


load_dotenv()



AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

action_recommender_agent = None
# --- Agent: Action Recommender ---
# This agent generates actionable, automation-ready system tasks from recovery plans and chaos analysis.
# It synthesizes short-term actions and long-term strategies from the recovery plan,    
# and uses the context from the chaos report to validate or enrich actions.
# It outputs a structured JSON object with key `action_recommendations` that contains a list    
action_recommender_agent = Agent(
    name="action_recommender",
    model=LiteLlm(model="azure/gpt-4o"),
    output_key="action_recommendations",
    description="Agent that generates actionable, automation-ready system tasks from recovery plans from planner agent",
    instruction="""
You are an Action Recommender Agent.

Your task is to provide actionable tasks for system recovery based on the provided recovery plan:

**Recovery Plan**

```json

{recovery_plan}

```

**Output Requirements:**
- For each task, include:
  - Verification steps (how to confirm success)
  - Required permissions/roles
  - Suggest automation scripts or playbooks if available
  - Task prioritization (high/medium/low, based on urgency and business impact)
- If information is missing, flag ambiguity and specify which fields are missing.
- Do NOT invent data. Only use what is available from the tools and schema.

Output *only* the final, json object.
Do not add any other text before or after the json object.

Output example:

```json
{
  "actions_generated_at": "2025-06-18T22:25:00Z",
  "source_plan_id": "2025-06-18T22:20:00Z",
  "recovery_tasks": [
    {
      "task_id": "task-001",
      "description": "Restart the affected disk subsystem in us-central1",
      "region": "us-central1",
      "component_scope": "infrastructure",
      "urgency": "high",
      "priority": "high",
      "steps": [
        "Identify nodes experiencing disk I/O stall in us-central1",
        "Gracefully drain traffic from affected nodes",
        "Restart disk subsystem or related virtual disks",
        "Verify disk health post-restart"
      ],
      "verification_steps": [
        "Check disk health metrics after restart",
        "Ensure error rate returns to baseline"
      ],
      "required_permissions": ["infrastructure_admin"],
      "automation_script": "restart_disk_subsystem.sh",
      "assigned_team": "infrastructure_team",
      "estimated_time_minutes": 30
    },
    {
      "task_id": "task-002",
      "description": "Shift workloads from affected zone to healthy zone in us-central1",
      "region": "us-central1",
      "component_scope": "orchestration",
      "urgency": "high",
      "priority": "high",
      "steps": [
        "Mark affected zone as degraded in orchestration layer",
        "Re-route service traffic to healthy availability zones",
        "Monitor error rate and latency post shift"
      ],
      "verification_steps": [
        "Confirm traffic is routed only to healthy zones",
        "Monitor for new errors in target zone"
      ],
      "required_permissions": ["orchestration_admin"],
      "automation_script": null,
      "assigned_team": "site_reliability_engineering",
      "estimated_time_minutes": 45
    }
  ],
  "notes": [
    "Tasks derived from planner's immediate recovery actions.",
    "No explicit service name provided — actions target infrastructure-level faults."
  ],
  "ambiguous": false
}


``` 
""",
    tools=[]
)

