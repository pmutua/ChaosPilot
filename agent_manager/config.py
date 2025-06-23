# agent.py

import os
import re
from dotenv import load_dotenv
from toolbox_core import ToolboxSyncClient

# Load .env file
load_dotenv()

# --- App Configuration ---
APP_NAME = os.getenv("APP_NAME", "agent_manager")
VERSION = os.getenv("VERSION", "0.1.0")
MODEL = os.getenv("MODEL")
TOOLBOX_URL = os.getenv("TOOLBOX_URL", "http:localhost:5000")

# --- Model Patterns ---
GEMINI_MODEL_PATTERN = r"\bgemini-[\w-]+"
AZURE_OPENAI_MODEL_PATTERN = r"\bazure\w*"

# --- Keys/Secrets (optional until model matches) ---
AZURE_API_KEY = None
AZURE_API_BASE = None
AZURE_API_VERSION = None
GOOGLE_API_KEY = None

toolbox = None

toolbox = ToolboxSyncClient(TOOLBOX_URL)

# --- Load API Keys based on model pattern ---
if re.findall(GEMINI_MODEL_PATTERN, MODEL):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

elif re.findall(AZURE_OPENAI_MODEL_PATTERN, MODEL):
    AZURE_API_KEY = os.getenv("AZURE_API_KEY")
    AZURE_API_BASE = os.getenv("AZURE_API_BASE")
    AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
