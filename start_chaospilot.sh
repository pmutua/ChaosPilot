#!/bin/bash

echo "========================================"
echo "    ChaosPilot Startup Script"
echo "========================================"
echo

echo "[1/3] Starting ADK API Server..."
echo "Starting agent_manager on http://localhost:8000 with CORS enabled"
cd agent_manager
gnome-terminal --title="ADK API Server" -- bash -c "python -m agent_manager.agent; exec bash" &
cd ..

echo
echo "[2/3] Waiting for ADK server to start..."
sleep 5

echo
echo "[3/3] Starting Angular Frontend..."
echo "Starting ChaosPilot UI on http://localhost:4200"
cd web
gnome-terminal --title="ChaosPilot Frontend" -- bash -c "npm start; exec bash" &
cd ..

echo
echo "========================================"
echo "    ChaosPilot is starting up!"
echo "========================================"
echo
echo "🌐 Frontend: http://localhost:4200"
echo "🔧 Backend:  http://localhost:8000"
echo
echo "📖 Documentation: docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md"
echo
echo "Press Enter to exit this script..."
read 