# agent.py

import os
import uuid
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
import asyncio

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


# --- Server and Session Configuration ---

# These must match the values used in the frontend's agent.service.ts
APP_NAME = "agent_manager"
USER_ID = "chaospilot_user"
SESSION_ID = str(uuid.uuid4())

# 1. Use persistent SQLite-backed session service 
db_url = "sqlite:///./agent_Manager_data.db"
session_service = DatabaseSessionService(db_url=db_url)

async def main():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={"initialized_at_startup": True}
    )

    print("CREATED NEW SESSION:")
    print("---------------Examining Session Properties------------------------")
    print("Session ID............................{}".format(session.id))
    print("Application name.............................{}".format(session.app_name))
    print("User ID.........................................{}".format(session.user_id))
    print("Sate:................................................".format(session.state))
    print("Events:........................................".format(session.events))

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service)

    new_message = types.Content(
        role="user", parts=[types.Part(text="Use the detector agent to: Analyze the latest logs for anomalies")]
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message
    ):
        if event.is_final_response():
            print("Final Response: {}".format(event.content.parts[0].text))

    print("=========FINAL SESSIONS STATE==============")

# Example usage in a local script
if __name__ == "__main__":
    asyncio.run(main())