import os

from models import gemini_models

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL: gemini_models = "gemini-3.1-flash-lite"