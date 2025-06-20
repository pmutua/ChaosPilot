# agent.py

import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .sub_agents.detector.agent import detector_agent
from .sub_agents.planner.agent import planner_agent
from .sub_agents.fixer.agent import fixer_agent
from .sub_agents.notifier.agent import notifier_agent
from .sub_agents.action_recommender.agent import action_recommender_agent

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")


# --- Agent Definition ---
# The ADK framework automatically discovers this instance of an `agent`
# in the `agent.py` file and builds a server around it.
# The name of the parent folder ('agent_manager') will be used as the app name.

root_agent = Agent(
    name="agent_manager", # The internal name for the agent
    model=LiteLlm(model="azure/gpt-4o"),
    description="Orchestration layer for the chaos engineering system.",
    sub_agents=[
        detector_agent,
        planner_agent,
        action_recommender_agent,
        fixer_agent,
        notifier_agent,
    ],
)
