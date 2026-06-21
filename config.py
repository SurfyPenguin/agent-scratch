import os

from core.gemini_models import gemini_models

try:
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError:
    print("Error: gemini api key not found in environment")

# TODO: don't hardcode model in code
GEMINI_MODEL: gemini_models = "gemini-3.1-flash-lite"
