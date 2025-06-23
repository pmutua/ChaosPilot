import uuid
import re
import asyncio
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from .sub_agents.detector.agent import detector_agent
from .sub_agents.planner.agent import planner_agent
from .sub_agents.fixer.agent import fixer_agent
from .sub_agents.notifier.agent import notifier_agent
from .sub_agents.action_recommender.agent import action_recommender_agent
from .config import MODEL, APP_NAME

# --- Constants ---
AZURE_OPENAI_MODEL_PATTERN = r"\bazure\S*"
GEMINI_MODEL_PATTERN = r"\bgemini\S*"
USER_ID = "chaospilot_user"
SESSION_ID = str(uuid.uuid4())
DB_URL = "sqlite:///./agent_Manager_data.db"

# --- Model Selection ---
if re.findall(AZURE_OPENAI_MODEL_PATTERN, MODEL):
    model_instance = LiteLlm(model="azure/gpt-4o")
elif re.findall(GEMINI_MODEL_PATTERN, MODEL):
    model_instance = MODEL  # MODEL is assumed to be a valid Gemini string
else:
    raise ValueError(f"Unsupported model format: {MODEL}")

# --- Root Agent Definition ---
root_agent = Agent(
    name="agent_manager",
    model=model_instance,
    description="Orchestration layer for the chaos engineering system.",
    sub_agents=[
        detector_agent,
        planner_agent,
        action_recommender_agent,
        fixer_agent,
        notifier_agent,
    ],
)

# --- Session Service ---
session_service = DatabaseSessionService(db_url=DB_URL)


# --- Main Runner ---
async def run():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={"initialized_at_startup": True},
    )

    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    new_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text="Use the detector agent to: Analyze the latest logs for anomalies"
            )
        ],
    )

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=new_message
    ):
        if event.is_final_response():
            print("Final Response:", event.content.parts[0].text)

    print("=========FINAL SESSION STATE==============")

