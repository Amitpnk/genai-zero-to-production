import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()  # reads OPENAI_API_KEY

response = client.responses.create(
    model=os.environ["OPENAI_MODEL"],
    max_output_tokens=200,
    input="Say hello in one sentence.",
)
print(response.output_text)
