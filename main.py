import os

import uvicorn
import fastapi.middleware.cors import CORMiddleware
from google.adk.cli.fast_api import get_fast_api_app

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Example session DB URL (e.g., SQLite)
# SESSION_DB_URL = "sqlite:///./sessions.db"
# Example allowed origins for CORS
ALLOWED_ORIGINS = ["https://chaos-pilot.vercel.app", "http://localhost:4200"]
# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True


# Call the function to get the FastAPI app instance
# Ensure the agent directory name ('capital_agent') matches your agent folder
app = get_fast_api_app(
    CORMiddleware,
    agents_dir=AGENT_DIR,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))