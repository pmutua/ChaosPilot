@echo off
echo ========================================
echo    ChaosPilot Startup Script
echo ========================================
echo.

echo [1/4] Starting ADK API Server...
echo Starting agent_manager on http://localhost:8000 with CORS enabled
cd agent_manager
start "ADK API Server" cmd /k "adk api_server --allow_origins=\"*\""
cd ..

echo.
echo [2/4] Waiting for ADK server to start...
timeout /t 5 /nobreak > nul

echo.
echo [3/4] Testing ADK Integration...
python test_adk_integration.py

echo.
echo [4/4] Starting Angular Frontend...
echo Starting ChaosPilot UI on http://localhost:4200
cd web
start "ChaosPilot Frontend" cmd /k "npm start"
cd ..

echo.
echo ========================================
echo    ChaosPilot is starting up!
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:4200
echo 🔧 Backend:  http://localhost:8000
echo.
echo 📖 Documentation: docs/setup-and-deployment/HOW_TO_RUN_AND_DEPLOY_THE_APPLICATION.md
echo 🧪 Test Script:  test_adk_integration.py
echo.
echo Press any key to exit this script...
pause > nul 