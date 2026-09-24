from google import genai
from google.genai import types
from google.genai import errors

from app.config import Config


class LLMService:

    def __init__(self):
        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

    def generate(self, prompt: str) -> str:

        try:
            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=800,
                ),
            )

            return response.text.strip()

        except errors.ServerError as error:

            if error.code == 503:
                return (
                    "The AI service is temporarily busy. "
                    "Please try again in a few moments."
                )

            raise

        except errors.ClientError as error:

            return (
                "The AI service could not process this request. "
                "Please try again later."
            )