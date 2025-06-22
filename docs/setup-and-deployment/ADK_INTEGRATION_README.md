# ChaosPilot ADK API Integration

This document explains how ChaosPilot integrates with the Google ADK (Agent Development Kit) API for autonomous log analysis and incident response.

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    ADK API    ┌─────────────────┐
│   Angular UI    │ ──────────────► │   AgentService  │ ─────────────► │  agent_manager  │
│   (Frontend)    │                 │   (Frontend)    │                │   (Backend)     │
└─────────────────┘                 └─────────────────┘                └─────────────────┘
```

## 🔧 ADK API Integration

### Session Management

The application uses ADK's session-based architecture for maintaining conversation state:

```typescript
// Session creation
POST /apps/agent_manager/users/{userId}/sessions/{sessionId}
{
  "state": {
    "initialized": true,
    "timestamp": 1234567890
  }
}
```

### Message Format

Messages follow the ADK standard format:

```typescript
interface ADKMessage {
  role: 'user' | 'model';
  parts: Array<{
    text?: string;
    functionCall?: any;
    functionResponse?: any;
  }>;
}
```

### Agent Execution

Two endpoints are supported:

1. **Batch Processing** (`/run`): Returns all events at once
2. **Streaming** (`/run_sse`): Returns events as they become available

```typescript
// Example request
{
  "appName": "agent_manager",
  "userId": "chaospilot_user",
  "sessionId": "chaospilot_session",
  "newMessage": {
    "role": "user",
    "parts": [{
      "text": "Use the detector agent to: Analyze recent error logs"
    }]
  }
}
```

## 🤖 Available Agents

The `agent_manager` contains 5 specialized agents:

| Agent | Purpose | ADK Name |
|-------|---------|----------|
| 🔍 Log Analyzer | Analyzes logs and detects patterns | `detector` |
| 📋 Response Planner | Creates recovery strategies | `planner` |
| 🛠️ Fix Recommender | Recommends specific fixes | `action_recommender` |
| ⚡ Auto-Fixer | Applies fixes automatically | `fixer` |
| 📢 Alert Manager | Manages notifications | `notifier` |

## 🚀 Getting Started

### 1. Start the ADK API Server

```bash
# Navigate to your agent_manager directory
cd agent_manager

# Start the ADK API server with CORS enabled
adk api_server app --allow_origins="*"
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

**Important**: The `--allow_origins="*"` flag is required to allow the Angular frontend to communicate with the ADK API server and avoid CORS errors.

### 2. Test the Integration

Run the test script to verify everything works:

```bash
python test_adk_integration.py
```

### 3. Start the Frontend

```bash
cd web
npm start
```

## 📡 API Endpoints

### Session Management

- `POST /apps/agent_manager/users/{userId}/sessions/{sessionId}` - Create session
- `GET /apps/agent_manager/users/{userId}/sessions/{sessionId}` - Get session info
- `DELETE /apps/agent_manager/users/{userId}/sessions/{sessionId}` - Delete session

### Agent Execution

- `POST /run` - Execute agent (batch mode)
- `POST /run_sse` - Execute agent (streaming mode)

## 🔄 Response Processing

The frontend processes ADK responses to extract:

1. **Text Content**: Final response text from the agent
2. **Function Calls**: Tools and functions used by the agent
3. **Structured Data**: JSON responses from function calls
4. **Confidence Scores**: Agent confidence in the response

### Example Response Processing

```typescript
// ADK Event Structure
{
  "content": {
    "parts": [{
      "text": "Analysis complete. Found 3 critical errors."
    }]
  },
  "author": "detector",
  "timestamp": 1234567890
}
```

## 🛠️ Frontend Integration

### AgentService

The `AgentService` handles all ADK API communication:

```typescript
// Initialize session
await agentService.initSession();

// Run agent
const result = await agentService.runAgent('detector', 'Analyze logs');

// Get streaming response
const stream = await agentService.runAgentStreaming('detector', 'Analyze logs');
```

### ChatService

The `ChatService` processes ADK responses for the UI:

```typescript
// Send message and get response
await chatService.sendMessage('Analyze recent errors', 'detector');

// Subscribe to messages
chatService.messages$.subscribe(messages => {
  // Handle real-time updates
});
```

## 🔍 Testing

### Manual Testing with cURL

```bash
# Create session
curl -X POST http://localhost:8000/apps/agent_manager/users/test_user/sessions/test_session \
  -H "Content-Type: application/json" \
  -d '{"state": {"test": true}}'

# Run detector agent
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "agent_manager",
    "userId": "test_user",
    "sessionId": "test_session",
    "newMessage": {
      "role": "user",
      "parts": [{"text": "Use the detector agent to: Analyze logs"}]
    }
  }'
```

**Note**: Make sure the ADK API server is running with `adk api_server app --allow_origins="*"` to avoid CORS issues.

### Automated Testing

Use the provided test script:

```bash
python test_adk_integration.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Session Already Exists (409)**
   - This is normal, the session will be reused
   - Delete the session if you need a fresh start

2. **Connection Refused**
   - Ensure the ADK API server is running on port 8000
   - Check that `agent_manager` is properly configured

3. **CORS Errors**
   - Make sure you're using `adk api_server app --allow_origins="*"`
   - Check that the frontend is running on the correct port (4200)
   - Verify the API server is accessible from the frontend

4. **Agent Not Found**
   - Verify the agent name matches exactly (detector, planner, etc.)
   - Check that the agent is properly registered in `agent_manager`

### Debug Mode

Enable debug logging in the frontend:

```typescript
// In AgentService
console.log('ADK Request:', request);
console.log('ADK Response:', response);
```

## 📊 Monitoring

The dashboard shows real-time metrics:

- Agent performance and success rates
- Recent activities and responses
- System health and status
- Tool usage statistics

## 🔐 Security

- All API calls use HTTP (for local development)
- Session management prevents unauthorized access
- User and session IDs are managed securely
- No sensitive data is logged

## 🚀 Production Deployment

For production deployment:

1. Use HTTPS for all API calls
2. Implement proper authentication
3. Use environment variables for configuration
4. Set up monitoring and logging
5. Configure CORS properly

## 📚 Additional Resources

- [ADK Documentation](https://developers.google.com/ai/agents)
- [Agent Development Guide](https://developers.google.com/ai/agents/develop)
- [API Reference](https://developers.google.com/ai/agents/reference) 