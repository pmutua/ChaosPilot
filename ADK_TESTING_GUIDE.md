# Testing your Agent

Before you deploy your agent, you should test it to ensure that it is working as intended. The easiest way to test your agent in your development environment is to use the ADK web UI with the following commands.

```bash
adk api_server
```

This command will launch a local web server, where you can run cURL commands or send API requests to test your agent.

## Local testing

Local testing involves launching a local web server, creating a session, and sending queries to your agent.

### 1. Launch the Local Server

First, ensure you are in the `agent_manager` directory. Then, launch the local server:

```bash
cd agent_manager
adk api_server
```

The output should appear similar to:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

Your server is now running locally. Ensure you use the correct port number in all the subsequent commands.

### 2. Create a new session

With the API server still running, open a **new terminal window or tab** and create a new session with the agent using:

```bash
curl -X POST http://localhost:8000/apps/agent_manager/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{"state": {"key1": "value1", "key2": 42}}'
```

Let's break down what's happening:

*   `http://localhost:8000/apps/agent_manager/users/u_123/sessions/s_123`: This creates a new session for your `agent_manager`, for a user ID (`u_123`) and for a session ID (`s_123`).
*   `{"state": ...}}`: This is optional. You can use this to customize the agent's pre-existing state.

This should return the session information if it was created successfully. The output should appear similar to:

```json
{"id":"s_123","appName":"agent_manager","userId":"u_123","state":{"state":{"key1":"value1","key2":42}},"events":[],"lastUpdateTime":1743711430.022186}
```

> **Info**
> You cannot create multiple sessions with exactly the same user ID and session ID. If you try to, you may see a response like: `{"detail":"Session already exists: s_123"}`. To fix this, you can either delete that session or choose a different session ID.

### 3. Send a query

There are two ways to send queries via `POST` to your agent, via the `/run` or `/run_sse` routes.

*   **`POST /run`**: Collects all events as a list and returns the list all at once. Suitable for most users.
*   **`POST /run_sse`**: Returns a stream of Server-Sent-Events. Suitable for those who want to be notified as soon as an event is available.

#### Using `/run`

```bash
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
"appName": "agent_manager",
"userId": "u_123",
"sessionId": "s_123",
"newMessage": {
    "role": "user",
    "parts": [{
    "text": "Use the detector agent to analyze the latest logs for anomalies."
    }]
}
}'
```

If using `/run`, you will see the full output of events at the same time, as a list.

#### Using `/run_sse`

```bash
curl -X POST http://localhost:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
"appName": "agent_manager",
"userId": "u_123",
"sessionId": "s_123",
"newMessage": {
    "role": "user",
    "parts": [{
    "text": "Use the detector agent to analyze the latest logs for anomalies."
    }]
},
"streaming": false
}'
```

If you are using `/run_sse`, you should see each event as soon as it becomes available. 