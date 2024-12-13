import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    """Interact with OpenAI API"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
