import logging

from flask import Blueprint, jsonify, request

from app.config import Config
from app.services.rag_service import RAGService


chat_bp = Blueprint("chat", __name__)

logger = logging.getLogger(__name__)

rag_service = RAGService()


@chat_bp.post("/api/chat")
def chat():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be valid JSON"
            }), 400

        message = data.get("message")

        if not isinstance(message, str):
            return jsonify({
                "error": "message is required and must be a string"
            }), 400

        message = message.strip()

        if not message:
            return jsonify({
                "error": "message cannot be empty"
            }), 400

        if len(message) > Config.MAX_MESSAGE_LENGTH:
            return jsonify({
                "error": (
                    f"message must not exceed "
                    f"{Config.MAX_MESSAGE_LENGTH} characters"
                )
            }), 400

        session_id = data.get("session_id")

        if session_id is not None:
            if not isinstance(session_id, str):
                return jsonify({
                    "error": "session_id must be a string"
                }), 400

            session_id = session_id.strip()

            if not session_id:
                return jsonify({
                    "error": "session_id cannot be empty"
                }), 400

        result = rag_service.answer(
            message,
            session_id
        )

        return jsonify(result), 200

    except Exception:
        logger.exception(
            "Unexpected error while processing chat request"
        )

        return jsonify({
            "error": (
                "The assistant could not process your request "
                "right now. Please try again later."
            )
        }), 500