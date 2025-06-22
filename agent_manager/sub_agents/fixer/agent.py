# chaos_commander.py

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv


load_dotenv()



AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")


fixer_agent = None
# --- Agent: Fixer ---
# This agent is responsible for advising on cost-optimized recovery actions when the recovery plan has high confidence.
# It synthesizes inputs from the planner agent, action recommender agent, and cost optimizer agent to produce clear, cost-aware fix recommendations.
# It outputs a structured JSON object with key `recommended_fixes` that contains a list of recommended fixes.
# It is designed to work in conjunction with other agents like planner_agent, action_recommender_agent, and cost_optimizer_agent.
# It is the final step in the incident response workflow, providing cost-aware recommendations based on the planned recovery actions
# and operational data.
# It is not responsible for executing any actions itself, but provides structured data for other agents to
# act upon (e.g., execution agents or human engineers).
# It is designed to work in conjunction with other agents like planner_agent, action_recommender_agent, and cost_optimizer_agent.
# It is the final step in the incident response workflow, providing
# cost-aware recommendations based on the planned recovery actions and operational data.
# It is not responsible for executing any actions itself, but provides structured data for other agents to
# act upon (e.g., execution agents or human engineers).
# It is designed to work in conjunction with other agents like planner_agent, action_recommender_agent, and cost_optimizer_agent.
# It is the final step in the incident response workflow, providing
# cost-aware recommendations based on the planned recovery actions and operational data.
# It is not responsible for executing any actions itself, but provides structured data for other agents to
# act upon (e.g., execution agents or human engineers).
# It is designed to work in conjunction with other agents like planner_agent, action_recommender_agent, and cost_optimizer_agent.
# It is the final step in the incident response workflow, providing                     
fixer_agent = Agent(
    name="fixer",
    output_key="fixer_summary",
    model=LiteLlm(model="azure/gpt-4o"),
    description="Agent responsible for advising the possible fixes for the actions recommended by the action recommender agent then send to notifier agent.",
    instruction="""
You are the Fixer Agent.

Your task is to:
- Recommend safe, cost-efficient fixes for high-confidence recovery scenarios
- For each fix, include:
  - Cost estimate (if data available)
  - Fallback action if the fix fails
  - Suggested monitoring metrics to watch after applying the fix
- Escalate only when ambiguity, conflict, or high risk is detected
- If ambiguity is detected or information is missing, specify which context is missing and suggest a query to resolve it
- Do NOT invent data. Only use what is available from the tools and schema.

The user will provide the action recommendations in their message. Look for JSON content or structured action recommendations information in the user's message.

Output *only* in JSON format. 
Do not add any other text before or after the json.

Output example:

```json
{
  "fix_execution_reviewed_at": "2025-06-18T22:30:00Z",
  "source_actions_id": "2025-06-18T22:25:00Z",
  "safe_to_execute_tasks": [
    {
      "task_id": "task-001",
      "description": "Restart the affected disk subsystem in us-central1",
      "execution_mode": "auto",
      "justification": "Low risk. Task steps are clearly defined, target is infrastructure, and estimated time is within tolerance.",
      "expected_cost_impact": "minimal",
      "cost_estimate_usd": 10.0,
      "risk_level": "low",
      "fallback_action": "Escalate to SRE if restart fails",
      "monitoring_metrics": ["disk_health", "error_rate"]
    }
  ],
  "escalation_required": [
    {
      "task_id": "task-002",
      "description": "Shift workloads from affected zone to healthy zone in us-central1",
      "reason": "Potential conflict: current orchestration health state unknown. Risk of traffic instability or cascading failure.",
      "recommended_escalation_team": "SRE escalation group",
      "urgency": "high",
      "risk_level": "moderate",
      "ambiguity_detected": [
        "Unclear zone health status",
        "Potential traffic routing conflict"
      ],
      "missing_context_query": "Query orchestration layer for current zone health status."
    }
  ],
  "summary": {
    "total_tasks_analyzed": 2,
    "tasks_safe_to_execute": 1,
    "tasks_escalated": 1
  },
  "ambiguous": false
}

""",
    tools=[]
)

print(f"✅ Agent '{fixer_agent.name}' created using model '{fixer_agent.model}'.")


