import os
from dotenv import load_dotenv

from core.gemini_models import gemini_models

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL: gemini_models = os.environ["GEMINI_MODEL"]
