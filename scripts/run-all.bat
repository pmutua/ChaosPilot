@echo off
REM === Start MCP Toolbox ===
start "MCP Toolbox" app\mcp-toolbox\toolbox.exe

REM === Wait a few seconds to ensure MCP Toolbox is up ===
timeout /t 3

REM === Start Backend (ADK Agent/FastAPI) ===
start "Backend" cmd /k "uv run adk api_server app --allow_origins=*"

REM === Start Frontend (Angular) ===
start "Frontend" cmd /k "npm --prefix frontend run start"

echo All services started! 