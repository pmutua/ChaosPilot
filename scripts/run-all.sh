#!/bin/bash
# === Start MCP Toolbox ===
./app/mcp-toolbox/toolbox.exe &
MCP_PID=$!

echo "Started MCP Toolbox (PID $MCP_PID)"

# === Wait a few seconds to ensure MCP Toolbox is up ===
sleep 3

# === Start Backend (ADK Agent/FastAPI) ===
uv run adk api_server app --allow_origins="*" &
BACKEND_PID=$!
echo "Started Backend (PID $BACKEND_PID)"

# === Start Frontend (Angular) ===
npm --prefix frontend run start &
FRONTEND_PID=$!
echo "Started Frontend (PID $FRONTEND_PID)"

wait $MCP_PID $BACKEND_PID $FRONTEND_PID 