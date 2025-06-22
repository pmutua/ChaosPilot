#!/usr/bin/env python3
"""
Test script for ADK API integration with ChaosPilot agent_manager
This script tests the API endpoints as described in the ADK documentation
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
APP_NAME = "agent_manager"  # Using agent_manager as specified
USER_ID = "test_user_123"
SESSION_ID = "test_session_123"

def test_session_creation():
    """Test creating a new session"""
    print("🔧 Testing session creation...")
    
    session_url = f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
    session_data = {
        "state": {
            "test_key": "test_value",
            "timestamp": time.time()
        }
    }
    
    try:
        response = requests.post(session_url, json=session_data)
        if response.status_code == 200:
            print("✅ Session created successfully")
            print(f"   Session ID: {response.json().get('id')}")
            return True
        elif response.status_code == 409:
            print("ℹ️  Session already exists, continuing...")
            return True
        else:
            print(f"❌ Failed to create session: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return False

def test_agent_run(agent_name, user_input):
    """Test running an agent with the /run endpoint"""
    print(f"\n🤖 Testing {agent_name} agent...")
    
    run_data = {
        "appName": APP_NAME,
        "userId": USER_ID,
        "sessionId": SESSION_ID,
        "newMessage": {
            "role": "user",
            "parts": [{
                "text": f"Use the {agent_name} agent to: {user_input}"
            }]
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/run", json=run_data)
        if response.status_code == 200:
            events = response.json()
            print(f"✅ {agent_name} agent responded successfully")
            print(f"   Number of events: {len(events)}")
            
            # Extract text responses
            text_events = [event for event in events if 
                          event.get('content', {}).get('parts') and 
                          any(part.get('text') for part in event['content']['parts'])]
            
            if text_events:
                final_text_event = text_events[-1]
                text_part = next((part for part in final_text_event['content']['parts'] if part.get('text')), None)
                if text_part:
                    print(f"   Response: {text_part['text'][:100]}...")
            
            # Extract function calls
            function_events = [event for event in events if 
                              event.get('content', {}).get('parts') and 
                              any(part.get('functionCall') for part in event['content']['parts'])]
            
            if function_events:
                print(f"   Function calls: {len(function_events)}")
                for event in function_events:
                    for part in event['content']['parts']:
                        if part.get('functionCall'):
                            print(f"     - {part['functionCall'].get('name', 'unknown')}")
            
            return events
        else:
            print(f"❌ Failed to run {agent_name} agent: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error running {agent_name} agent: {e}")
        return None

def test_streaming_agent(agent_name, user_input):
    """Test running an agent with the /run_sse endpoint"""
    print(f"\n🌊 Testing {agent_name} agent with streaming...")
    
    run_data = {
        "appName": APP_NAME,
        "userId": USER_ID,
        "sessionId": SESSION_ID,
        "newMessage": {
            "role": "user",
            "parts": [{
                "text": f"Use the {agent_name} agent to: {user_input}"
            }]
        },
        "streaming": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/run_sse", json=run_data)
        if response.status_code == 200:
            print(f"✅ {agent_name} agent streaming test successful")
            return True
        else:
            print(f"❌ Failed to test streaming for {agent_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing streaming for {agent_name}: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 ChaosPilot ADK API Integration Test")
    print("=" * 50)
    
    # Test session creation
    if not test_session_creation():
        print("❌ Session creation failed, aborting tests")
        return
    
    # Test different agents
    test_cases = [
        ("detector", "Analyze recent error logs and identify any critical issues"),
        ("planner", "Create a recovery plan for database connection issues"),
        ("action_recommender", "Recommend fixes for high memory usage"),
    ]
    
    for agent_name, user_input in test_cases:
        # Test regular run
        events = test_agent_run(agent_name, user_input)
        
        # Test streaming
        test_streaming_agent(agent_name, user_input)
        
        if events:
            print(f"   ✅ {agent_name} integration working")
        else:
            print(f"   ❌ {agent_name} integration failed")
    
    print("\n" + "=" * 50)
    print("🎉 ADK API Integration Test Complete!")
    print("\nNext steps:")
    print("1. Ensure your agent_manager is running with: adk api_server")
    print("2. The Angular frontend should now be able to communicate with the backend")
    print("3. Test the full integration through the web UI")

if __name__ == "__main__":
    main() 