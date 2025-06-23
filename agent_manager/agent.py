import asyncio
import re
import uuid
from typing import Any, Dict, Optional

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from .config import APP_NAME, MODEL
from .sub_agents.action_recommender.agent import action_recommender_agent
from .sub_agents.detector.agent import detector_agent
from .sub_agents.fixer.agent import fixer_agent
from .sub_agents.notifier.agent import notifier_agent
from .sub_agents.planner.agent import planner_agent

# --- Constants ---
AZURE_OPENAI_MODEL_PATTERN = r"\bazure\S*"
GEMINI_MODEL_PATTERN = r"\bgemini\S*"
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

class SessionManager:
    """Manages session lifecycle for Google ADK with proper error handling and cleanup."""
    
    def __init__(self, session_service: DatabaseSessionService):
        self.session_service = session_service
        self._active_sessions: Dict[str, Any] = {}
    
    async def get_or_create_session(self, app_name: str, user_id: str, session_id: Optional[str] = None) -> tuple:
        """
        Get existing session or create new one.
        Returns (session, session_id)
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session_key = f"{app_name}_{user_id}_{session_id}"
        
        # Check if session already exists in memory
        if session_key in self._active_sessions:
            return self._active_sessions[session_key], session_id
        
        try:
            # Try to get existing session from database
            session = await self.session_service.get_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id
            )
            
            if not session:
                # Create new session if it doesn't exist
                session = await self.session_service.create_session(
                    app_name=app_name,
                    user_id=user_id,
                    session_id=session_id,
                    state={"initialized_at": asyncio.get_event_loop().time()}
                )
                print(f"Created new session: {session_id}")
            else:
                print(f"Retrieved existing session: {session_id}")
            
            # Cache the session
            self._active_sessions[session_key] = session
            return session, session_id
            
        except Exception as e:
            print(f"Error managing session {session_id}: {e}")
            raise
    
    async def update_session_state(self, app_name: str, user_id: str, session_id: str, state_updates: Dict[str, Any]):
        """Update session state with new data."""
        try:
            session_key = f"{app_name}_{user_id}_{session_id}"
            
            # Update cached session if it exists
            if session_key in self._active_sessions:
                current_state = self._active_sessions[session_key].state or {}
                current_state.update(state_updates)
                
                # Update in database
                await self.session_service.update_session_state(
                    app_name=app_name,
                    user_id=user_id,
                    session_id=session_id,
                    state=current_state
                )
                
                print(f"Updated session state for {session_id}")
        except Exception as e:
            print(f"Error updating session state: {e}")
            raise
    
    async def cleanup_session(self, app_name: str, user_id: str, session_id: str):
        """Clean up session resources."""
        session_key = f"{app_name}_{user_id}_{session_id}"
        
        # Remove from active sessions
        if session_key in self._active_sessions:
            del self._active_sessions[session_key]
            print(f"Cleaned up session: {session_id}")
    
    def get_active_session_count(self) -> int:
        """Get count of active sessions."""
        return len(self._active_sessions)

# --- Initialize Session Manager ---
session_manager = SessionManager(session_service)

# --- Helper: Convert dict to types.Content ---
def dict_to_content(new_message_dict: Dict[str, Any]) -> types.Content:
    """Convert a dict with keys 'role' and 'parts' to types.Content."""
    role = new_message_dict.get("role", "user")
    parts_data = new_message_dict.get("parts", [])
    
    # Handle different part formats
    parts = []
    for part in parts_data:
        if isinstance(part, dict):
            parts.append(types.Part(**part))
        else:
            # Assume it's a text string
            parts.append(types.Part(text=str(part)))
    
    return types.Content(role=role, parts=parts)

# --- Validate Payload ---
def validate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize payload structure."""
    required_fields = ['appName', 'userId']
    
    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Missing required field in payload: {field}")
    
    # Normalize payload
    normalized = {
        'appName': payload['appName'],
        'userId': payload['userId'],
        'sessionId': payload.get('sessionId'),  # Optional, will be generated if not provided
        'newMessage': payload.get('newMessage', {})
    }
    
    # Validate newMessage structure
    if normalized['newMessage'] and not isinstance(normalized['newMessage'], dict):
        raise ValueError("newMessage must be a dictionary")
    
    return normalized

# --- Enhanced Main Runner ---
async def run_with_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhanced runner with proper session management and error handling.
    Returns response data for Angular frontend.
    """
    try:
        # Validate payload
        validated_payload = validate_payload(payload)
        
        app_name = validated_payload['appName']
        user_id = validated_payload['userId']
        session_id = validated_payload['sessionId']
        new_message_dict = validated_payload['newMessage']
        
        # Get or create session
        session, session_id = await session_manager.get_or_create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        print(f"SESSION READY - ID: {session_id}")
        
        # Create runner
        runner = Runner(
            agent=root_agent,
            app_name=app_name,
            session_service=session_service
        )
        
        # Process message if provided
        responses = []
        if new_message_dict:
            new_message = dict_to_content(new_message_dict)
            
            # Update session state with message timestamp
            await session_manager.update_session_state(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                state_updates={
                    "last_message_at": asyncio.get_event_loop().time(),
                    "message_count": session.state.get("message_count", 0) + 1
                }
            )
            
            # Run agent and collect responses
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message
            ):
                if event.is_final_response():
                    final_response = event.content.parts[0].text
                    responses.append({
                        "type": "final",
                        "content": final_response,
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    print("Final Response:", final_response)
                else:
                    # Handle intermediate responses
                    responses.append({
                        "type": "intermediate",
                        "content": str(event.content),
                        "timestamp": asyncio.get_event_loop().time()
                    })
        
        # Return structured response for Angular
        return {
            "success": True,
            "sessionId": session_id,
            "responses": responses,
            "activeSessionCount": session_manager.get_active_session_count(),
            "sessionState": session.state
        }
        
    except Exception as e:
        print(f"Error in run_with_payload: {e}")
        return {
            "success": False,
            "error": str(e),
            "sessionId": session_id if 'session_id' in locals() else None
        }

# --- Session Management API Functions ---
async def get_session_info(app_name: str, user_id: str, session_id: str) -> Dict[str, Any]:
    """Get session information for Angular frontend."""
    try:
        session, _ = await session_manager.get_or_create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        return {
            "success": True,
            "sessionId": session_id,
            "state": session.state,
            "createdAt": session.state.get("initialized_at"),
            "lastMessageAt": session.state.get("last_message_at"),
            "messageCount": session.state.get("message_count", 0)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

async def cleanup_user_sessions(app_name: str, user_id: str) -> Dict[str, Any]:
    """Clean up all sessions for a user."""
    try:
        # This would need to be implemented based on your session service capabilities
        # For now, we'll clean up from our active sessions
        sessions_cleaned = 0
        keys_to_remove = []
        
        for key in session_manager._active_sessions.keys():
            if key.startswith(f"{app_name}_{user_id}_"):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del session_manager._active_sessions[key]
            sessions_cleaned += 1
        
        return {
            "success": True,
            "sessionsCleanedUp": sessions_cleaned
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# --- Synchronous wrapper for API integration ---
def run_agent_with_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Sync wrapper for running the agent with a full payload."""
    return asyncio.run(run_with_payload(payload))

def get_session_info_sync(app_name: str, user_id: str, session_id: str) -> Dict[str, Any]:
    """Sync wrapper for getting session info."""
    return asyncio.run(get_session_info(app_name, user_id, session_id))

def cleanup_user_sessions_sync(app_name: str, user_id: str) -> Dict[str, Any]:
    """Sync wrapper for cleaning up user sessions."""
    return asyncio.run(cleanup_user_sessions(app_name, user_id))

# --- Example usage for Angular integration ---
"""
Example payload structure for Angular:

{
    "appName": "chaos_engineering_app",
    "userId": "user123",
    "sessionId": "optional-session-id",  // If not provided, will be auto-generated
    "newMessage": {
        "role": "user",
        "parts": [
            {"text": "Hello, I need to analyze system failures"}
        ]
    }
}

Response structure:
{
    "success": true,
    "sessionId": "generated-or-provided-session-id",
    "responses": [
        {
            "type": "final",
            "content": "Agent response text",
            "timestamp": 1234567890.123
        }
    ],
    "activeSessionCount": 5,
    "sessionState": {
        "initialized_at": 1234567890.123,
        "last_message_at": 1234567890.456,
        "message_count": 3
    }
}
"""