@echo off
REM === Start MCP Toolbox ===
start "MCP Toolbox" mcp-toolbox\toolbox.exe

REM === Wait a few seconds to ensure MCP Toolbox is up ===
timeout /t 3

REM === Start Backend (ADK Agent) ===
cd agent_manager
start "Backend" cmd /k "adk api_server --allow_origins=*"
cd ..

REM === Start Frontend (Angular) ===
cd web
start "Frontend" cmd /k "npm start"
cd ..

echo All services started! 