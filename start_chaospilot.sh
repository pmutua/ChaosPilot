#!/bin/bash

echo "========================================"
echo "    ChaosPilot Startup Script"
echo "========================================"
echo

echo "[1/4] Starting ADK API Server..."
echo "Starting agent_manager on http://localhost:8000 with CORS enabled"
cd agent_manager
gnome-terminal --title="ADK API Server" -- bash -c "adk api_server --allow_origins=\"*\"; exec bash" &
cd ..

echo
echo "[2/4] Waiting for ADK server to start..."
sleep 5

echo
echo "[3/4] Testing ADK Integration..."
python3 test_adk_integration.py

echo
echo "[4/4] Starting Angular Frontend..."
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
echo "🧪 Test Script:  test_adk_integration.py"
echo
echo "Press Enter to exit this script..."
read 