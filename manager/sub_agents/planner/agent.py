# chaos_commander.py

import os
from datetime import datetime, timedelta
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

load_dotenv()


AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

planner_agent = None
# --- Agent: Planner ---
# This agent is responsible for generating recovery plans based on chaos reports and detected system issues.
# It synthesizes short-term actions and long-term strategies from the chaos report, \
# and uses the context from the chaos report to validate or enrich actions.

instruction = """
    You are a Resilience Planning Agent.

    Your task is to generate a clear, recovery plan based on the provided:
    
    **Detector Agent Summary**
    
    ```json
    
    {detector_summary}
    
    ```
    
    **Recovery Plan Actions**
    
    1. Analyze services with CRITICAL or ERROR levels.
    2. Recommend immediate recovery actions.
    3. Suggest long-term resilience strategies.
    4. Provide a confidence score for the plan.
    5. Justify the plan based on data from the chaos report and service metrics.

    
    **Output:**
    
    Output *only* in JSON format example:
    
    ```json
{
  "plan_generated_at": "2025-06-18T22:20:00Z",
  "summary": {
    "critical_services_detected": false,
    "error_services_detected": true,
    "total_error_events": 1,
    "regions_impacted": ["us-central1"],
    "failure_types": ["disk_stall"]
  },
  "analysis": {
    "services_affected": ["unknown"],  // no explicit service name in chaos log
    "error_severity_distribution": {
      "CRITICAL": 0,
      "ERROR": 1
    },
    "dominant_failure_type": "disk_stall"
  },
  "immediate_recovery_actions": [
    {
      "action": "Restart disk subsystem or shift workloads to healthy zone in us-central1",
      "applicable_regions": ["us-central1"],
      "impact_scope": "infrastructure",
      "reason": "Disk I/O stall detected during chaos experiment; severity: ERROR; impact_level: high",
      "urgency": "high"
    }
  ],
  "long_term_resilience_strategies": [
    {
      "strategy": "Introduce automated disk health monitoring and failover mechanisms",
      "goal": "Early detection and fast remediation of I/O stalls",
      "reason": "Disk stall was injected and successfully caused disruption — indicates lack of automated mitigation"
    },
    {
      "strategy": "Upgrade storage layer to resilient SSD with replication in multi-zone",
      "goal": "Avoid single-point failures during I/O bursts or chaos testing",
      "reason": "Chaos experiment succeeded in affecting disk subsystem, revealing insufficient storage redundancy"
    }
  ],
  "confidence_score": 0.87,
  "justification": {
    "data_sources_used": [
      "chaos_logs.analysis",
      "severity_levels.ERROR",
      "region_impact: us-central1",
      "failure_type: disk_stall"
    ],
    "rationale": "Plan based on consistent ERROR-level disk_stall failure in us-central1 during chaos experiment exp0001. The failure was injected and confirmed with high impact, indicating both immediate risk and long-term architectural weakness."
  }
}

"""
planner_agent = Agent(
    name="planner",
    model=LiteLlm(model="azure/gpt-4o"),
    output_key="recovery_plan",
    description="Agent responsible for generating recovery plans based on chaos reports and detected system issues.",
    instruction=instruction,
    tools=[],
)
