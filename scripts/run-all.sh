#!/bin/bash
# === Start MCP Toolbox ===
./mcp-toolbox/toolbox.exe &
MCP_PID=$!

echo "Started MCP Toolbox (PID $MCP_PID)"

# === Wait a few seconds to ensure MCP Toolbox is up ===
sleep 3

# === Start Backend (ADK Agent) ===
cd agent_manager
adk api_server --allow_origins="*" &
cd ..
BACKEND_PID=$!
echo "Started Backend (PID $BACKEND_PID)"

# === Start Frontend (Angular) ===
cd web
npm start &
cd ..
FRONTEND_PID=$!
echo "Started Frontend (PID $FRONTEND_PID)"

wait $MCP_PID $BACKEND_PID $FRONTEND_PID 