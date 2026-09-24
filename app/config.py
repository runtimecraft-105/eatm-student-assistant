import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "gemini-embedding-001"
    )

    EMBEDDING_DIMENSION = int(
        os.getenv("EMBEDDING_DIMENSION", "768")
    )

    VECTOR_STORE_PATH = os.getenv(
        "VECTOR_STORE_PATH",
        "data/vector_store"
    )

    KNOWLEDGE_DIR = os.getenv(
        "KNOWLEDGE_DIR",
        "knowledge"
    )

    TOP_K = int(os.getenv("TOP_K", "5"))
    RAG_DISTANCE_THRESHOLD = float(
        os.getenv("RAG_DISTANCE_THRESHOLD", "1.2")
    )

    MAX_MESSAGE_LENGTH = int(
        os.getenv("MAX_MESSAGE_LENGTH", "4000")
    )

    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

    FLASK_DEBUG = (
        os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )


def validate_config():
    if not Config.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add it to your .env file."
        )

    if not Config.ADMIN_TOKEN:
        raise RuntimeError(
            "ADMIN_TOKEN is missing. "
            "Add it to your .env file."
        )