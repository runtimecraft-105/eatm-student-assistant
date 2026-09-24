from google import genai

from app.config import Config


class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def embed(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model=Config.EMBEDDING_MODEL,
            contents=text,
        )

        return response.embeddings[0].values