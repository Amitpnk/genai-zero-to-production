import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY

response = client.models.generate_content(
    model=os.environ["GEMINI_MODEL"],
    contents="Say hello in one sentence.",
    config=types.GenerateContentConfig(max_output_tokens=200),
)
print(response.text)
