"""
Application Configuration Module.

Handles environment variable loading, OpenAI client initialization,
and application-wide constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------------------------
# Walk up from /app to project root to find .env
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. "
        "Create a .env file in the project root with your key."
    )

# ---------------------------------------------------------------------------
# OpenAI Client (modern SDK — singleton)
# ---------------------------------------------------------------------------
openai_client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ---------------------------------------------------------------------------
# AI Model Settings
# ---------------------------------------------------------------------------
AI_MODEL: str = "llama3-70b-8192"
AI_TEMPERATURE_LOW: float = 0.1          # Structured extraction / parsing
AI_TEMPERATURE_MEDIUM: float = 0.5       # Enhancement / rewriting
AI_TEMPERATURE_HIGH: float = 0.7         # Creative suggestions
MAX_TOKENS_PARSE: int = 2000
MAX_TOKENS_ATS: int = 2500
MAX_TOKENS_ENHANCE: int = 1500
MAX_RETRIES: int = 2

# ---------------------------------------------------------------------------
# File Upload Constraints
# ---------------------------------------------------------------------------
MAX_PDF_SIZE_MB: int = 5
ALLOWED_FILE_TYPES: list[str] = ["pdf"]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASE_PATH: str = str(_PROJECT_ROOT / "resumes.db")

# ---------------------------------------------------------------------------
# PDF Templates
# ---------------------------------------------------------------------------
AVAILABLE_TEMPLATES: dict[str, str] = {
    "tech_minimalist": "Tech Minimalist",
    "corporate_executive": "Corporate Executive",
    "modern_developer": "Modern Developer",
}

# ---------------------------------------------------------------------------
# Application Metadata
# ---------------------------------------------------------------------------
APP_NAME: str = "ResumeForge AI"
APP_VERSION: str = "2.0.0"
APP_ICON: str = "⚡"
APP_DESCRIPTION: str = "AI-Powered Resume Builder & ATS Optimizer"
