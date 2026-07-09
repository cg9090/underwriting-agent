import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from config import get_secret

load_dotenv()

class LLMClient:

    def __init__(self):

        self.client = Anthropic(
            api_key=get_secret("ANTHROPIC_API_KEY")
        )


    def generate(
        self,
        prompt: str
    ):

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=20000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text