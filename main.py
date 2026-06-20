from google import genai

from models import gemini_models
from config import GEMINI_API_KEY

MODEL: gemini_models = "gemini-2.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model=MODEL,
    contents="Any word for your friend claude?"
)

print(response.text)