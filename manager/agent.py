# chaos_commander.py

import os
from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner # Use InMemoryRunner
from google.genai import types
from google.adk.runners import Runner
from dotenv import load_dotenv
from .sub_agents.detector.agent import detector_agent
from .sub_agents.planner.agent import planner_agent
from .sub_agents.fixer.agent import fixer_agent
from .sub_agents.notifier.agent import notifier_agent
from .sub_agents.action_recommender.agent import action_recommender_agent

from typing import Optional

from toolbox_core import ToolboxSyncClient

load_dotenv()


AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

APP_NAME = "chaos_commander"
USER_ID = "chaos_commander_user"
SESSION_ID = "chaos_commander_session"
session_id_run = "session_will_run"
session_id_skip = "session_will_skip"

# toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
# Load all the tools
# tools = toolbox.load_toolset('detector_toolset')

tool=ToolboxSyncClient("http://localhost:5000") 
# Load all the tools
recent_errors = tool.load_tool('recent_errors')
errors_logs_grouped_by_severity = tool.load_tool('errors_logs_grouped_by_severity')
critical_error_logs_grouped_by_region = tool.load_tool('critical_error_logs_grouped_by_region')
total_error_logs = tool.load_tool('total_error_logs')
most_frequent_error_types = tool.load_tool('most_frequent_error_types')
errors_logs_grouped_by_severity = tool.load_tool('errors_logs_grouped_by_severity')
total_error_logs = tool.load_tool('total_error_logs')

recent_errors_tool = recent_errors()
errors_logs_grouped_by_severity_tool = errors_logs_grouped_by_severity()
critical_error_logs_grouped_by_region_tool = critical_error_logs_grouped_by_region()
total_error_logs_tool = total_error_logs()
most_frequent_error_types_tool = most_frequent_error_types()

# total_errors_tool = client.load_tool('total_critical_error_logs')
# region_tool = client.load_tool('critical_error_logs_grouped_by_region')
# severity_tool = client.load_tool('errors_logs_grouped_by_severity')
# frequent_error_tool = client.load_tool('most_frequent_error_types')
# recent_errors_tool = client.load_tool('recent_errors')
print("Loaded Tools:...............................................")
print("Loaded Tools:...............................................")
# print(tool())
    # print(total_errors_tool)    
    # print(region_tool)
    # print(severity_tool)
    # print(frequent_error_tool)
    # print(recent_errors_tool)


# --- 1. Define the Callback Function ---
def check_if_agent_should_run(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Logs entry and checks 'skip_llm_agent' in session state.
    If True, returns Content to skip the agent's execution.
    If False or not present, returns None to allow execution.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    # Check the condition in session state dictionary
    if current_state.get("skip_llm_agent", False):
        print(f"[Callback] State condition 'skip_llm_agent=True' met: Skipping agent {agent_name}.")
        # Return Content to skip the agent's run
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} skipped by before_agent_callback due to state.")],
            role="model" # Assign model role to the overriding response
        )
    else:
        print(f"[Callback] State condition not met: Proceeding with agent {agent_name}.")
        # Return None to allow the LlmAgent's normal execution
        return None

instruction = """
            # 🧠 Root Agent: Multi-Agent Coordination Protocol

            ## 🎯 Mission
            You are the **orchestration layer** of a distributed chaos engineering system.  
            You **do not analyze, plan, fix, or optimize issues** yourself.  
            Your role is to delegate work to the appropriate agent, enforce strict execution order, and monitor system flow.

            ---

            ## 🧭 Role & Responsibilities
            - Route all system- or user-triggered inputs to the correct downstream agent.
            - Ensure agents execute in correct sequence.
            - Escalate when agent outputs are insufficient, ambiguous, or risky.
            - Maintain end-to-end visibility across the chaos response pipeline.

            ---

            ## 🚦 Startup Sequence

            1. On system boot, immediately trigger `detector_agent` to collect baseline chaos log metrics.
            2. Present user with this menu when idle or waiting:

                👋 Hello! What would you like to do?
                🔘 [1] 📊 Review Chaos Logs  
                🔘 [2] 🧪 Analyze Chaos Logs  
                🔘 [3] 🚨 View Detected Anomalies  
                🔘 [4] 📋 View Recovery Plan  
                🔘 [5] 🛠 Recommend Fixes  
                🔘 [6] 📣 View Notifications  

            3. Await user selection or continue the automatic agent chain if anomalies are detected.

            ---

            ## 🔁 Flow Initiation Logic

            Upon system boot or user interaction, determine how to begin the recovery flow:

            ### 🔄 Automatic Trigger (Anomalies Detected)
            If `detector_agent` output includes confirmed anomalies:
            - Automatically trigger:
                1. `planner_agent`
                2. `action_recommender_agent`
                3. `fixer_agent`
                4. `notifier_agent` (only if risk or ambiguity is detected)

            ### 🧭 Manual Trigger (User Selection)
            If user selects from the menu:
            - [1] → Call `detector_agent` (summary mode)
            - [2] → Call `detector_agent` (anomaly mode)
            - [3] → Fetch/display recent anomaly output
            - [4] → Trigger `planner_agent` to generate/view recovery plan
            - [5] → Manually trigger recovery sequence:
                - `planner_agent` → `action_recommender_agent` → `fixer_agent`
            - [6] → Show latest messages from `notifier_agent`

            Continue only if each agent returns valid, confident output. Escalate if any output is ambiguous, incomplete, or risky.

            ---

            ## 🔁 Execution Flow (Strict Sequence)

            ### Step 1: Detection
            - 🔄 Agent: `detector_agent`
            - 🔁 Trigger: On boot or user input
            - ✅ Output: Structured metrics and anomaly report

            ### Step 2: Recovery Planning
            - 🔄 Agent: `planner_agent`
            - 🔁 Trigger: When anomalies are detected
            - ✅ Output: Structured recovery plan with confidence score and justifications

            ### Step 3: Action Recommendation
            - 🔄 Agent: `action_recommender_agent`
            - 🔁 Trigger: Plan is available
            - ✅ Output: Task list with urgency, scope, teams, and time estimates

            ### Step 4: Fix Advising
            - 🔄 Agent: `fixer_agent`
            - 🔁 Trigger: Action plan is ready
            - ✅ Output: Safe fix strategy or escalation advisory

            ### Step 5: Notification
            - 🔄 Agent: `notifier_agent`
            - 🔁 Trigger:
                - Fixer flags ambiguity or risk
                - Planner confidence < 60%
                - Detector flags unknown anomaly
                - Any agent fails or returns uncertain output
            - ✅ Output: Human-readable operator message

            ### Step 6: Standby
            - 🔁 Trigger: No anomalies or after successful fix plan
            - 🔄 Action: Return to idle and show user menu

            ---

            ## 📌 Delegation Matrix

            | Scenario                        | Agent                    | Trigger Condition                                           |
            |---------------------------------|--------------------------|-------------------------------------------------------------|
            | Detect and analyze chaos logs  | `detector_agent`         | On boot or user request                                    |
            | Create recovery plan           | `planner_agent`          | If anomalies found                                         |
            | Recommend recovery tasks       | `action_recommender_agent`| When plan is ready                                       |
            | Advise safe fixes              | `fixer_agent`            | When actions are available                                |
            | Notify operator                | `notifier_agent`         | When confidence is low or ambiguity exists                 |

            ---

            ## 🚨 Escalation Protocol

            Always escalate to `notifier_agent` if:
            - Planner or Fixer confidence < 60%
            - `fixer_agent` detects ambiguity or high risk
            - Detector flags unknown anomaly
            - Any agent fails, crashes, or returns invalid output

            ---

            ## 📨 Agent Message Format

            All agent-to-agent messages must include:
            - `timestamp`
            - `priority` → [low | normal | high | critical]
            - `previous_agent_output` (if available)
            - `metrics_snapshot` (optional, from `stats_agent`)

            ---

            ## ⚠️ Limitations

            - Do **not** perform detection, planning, fixing, or notifications yourself.
            - Do **not** override any agent’s output or confidence score.
            - Always delegate based on defined flow and trigger conditions.
            - Escalate immediately if results are unclear, missing, or risky.

"""

# Create the sequential Agent
root_agent = SequentialAgent(
    name="manager",
    description="The Orchestrator Agent is the central coordination layer in a distributed chaos engineering system. It acts as a flow controller, ensuring that all specialized agents (detection, planning, fixing, and notification) operate in the correct sequence with clear delegation boundaries.",
    before_agent_callback=check_if_agent_should_run, # Assign the callback
    sub_agents=[
        detector_agent,
        planner_agent,
        action_recommender_agent,
        fixer_agent,
        notifier_agent,
    ],
)



# Use InMemoryRunner - it includes InMemorySessionService
runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)


# --- 3. Setup Runner and Sessions using InMemoryRunner ---
async def main():
    session_id_run = "session_will_run"
    session_id_skip = "session_will_skip"

    # Use InMemoryRunner - it includes InMemorySessionService
    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    # Get the bundled session service to create sessions
    session_service = runner.session_service

    # Create session 1: Agent will run (default empty state)
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id_run
        # No initial state means 'skip_llm_agent' will be False in the callback check
    )

    # Create session 2: Agent will be skipped (state has skip_llm_agent=True)
    # session_service.create_session(
    #     app_name=APP_NAME,
    #     user_id=USER_ID,
    #     session_id=session_id_skip,
    #     state={"skip_llm_agent": True} # Set the state flag here
    # )
    
    import json
    inline_data = str(json.dumps({
        "recent_errors": recent_errors,
        "errors_logs_grouped_by_severity": errors_logs_grouped_by_severity,
        "critical_error_logs_grouped_by_region": critical_error_logs_grouped_by_region,
        "most_frequent_error_types": most_frequent_error_types,
        "errors_logs_grouped_by_severity": errors_logs_grouped_by_severity,
        "total_error_logs": total_error_logs,
        
    }))
    
    print("Inline Data for Agent Execution:................................................")

    print(inline_data)
    # --- Scenario 1: Run where callback allows agent execution ---
    print("\n" + "="*20 + f" SCENARIO 1: Running Agent on Session '{session_id_run}' (Should Proceed) " + "="*20)
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id_run,
        new_message=types.Content(role="user", parts=[types.Part(text="Analyze chaos log")]),
    ):
        # Print final output (either from LLM or callback override)
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")
        elif event.is_error():
                print(f"Error Event: {event.error_details}")
                
                
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

    # --- Scenario 2: Run where callback intercepts and skips agent ---
    # print("\n" + "="*20 + f" SCENARIO 2: Running Agent on Session '{session_id_skip}' (Should Skip) " + "="*20)
    # async for event in runner.run_async(
    #     user_id=user_id,
    #     session_id=session_id_skip,
    #     new_message=types.Content(role="user", parts=[types.Part(text="This message won't reach the LLM.")])
    # ):
    #      # Print final output (either from LLM or callback override)
    #      if event.is_final_response() and event.content:
    #         print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")
    #      elif event.is_error():
    #          print(f"Error Event: {event.error_details}")

# --- 4. Execute ---
# In a Python script:
# import asyncio
# if __name__ == "__main__":
#     # Make sure GOOGLE_API_KEY environment variable is set if not using Vertex AI auth
#     # Or ensure Application Default Credentials (ADC) are configured for Vertex AI
#     asyncio.run(main())

# Get the bundled session service to create sessions
# session_service = runner.session_service


# Create session 2: Agent will be skipped (state has skip_llm_agent=True)
# session_service.create_session(
#     app_name=APP_NAME,
#     user_id=USER_ID,
#     session_id=session_id_skip,
#     state={"skip_llm_agent": False} # Set the state flag here
# )

# session_service = InMemorySessionService()
# session = session_service.create_session(
#     app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
# )

# # Use InMemoryRunner - it includes InMemorySessionService
# runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


# # Agent Interaction
# def call_agent(query: str):
#     content = types.Content(role="user", parts=[types.Part(text=query)])
#     events = runner.run(
#         user_id=USER_ID, session_id=SESSION_ID, new_message=content
#     )

#     for event in events:
#         if event.is_final_response():
#             final_response = event.content.parts[0].text
#             print(f"Agent Response:", final_response)


# call_agent(instruction)
