import logging
import subprocess
import sys
from pathlib import Path

from flask import Blueprint, jsonify, request

from app.config import Config


admin_bp = Blueprint("admin", __name__)

logger = logging.getLogger(__name__)


@admin_bp.post("/api/admin/ingest")
def ingest():
    token = request.headers.get("X-Admin-Token")

    if not token or token != Config.ADMIN_TOKEN:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    project_root = Path(__file__).resolve().parents[2]

    ingest_script = project_root / "scripts" / "ingest.py"

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(ingest_script)
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:

            logger.error(
                "Knowledge-base ingestion failed: %s",
                result.stderr
            )

            return jsonify({
                "error": "Knowledge-base ingestion failed"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Knowledge base ingested successfully"
        }), 200

    except subprocess.TimeoutExpired:

        logger.error(
            "Knowledge-base ingestion timed out"
        )

        return jsonify({
            "error": "Knowledge-base ingestion timed out"
        }), 500

    except Exception:

        logger.exception(
            "Unexpected error during knowledge-base ingestion"
        )

        return jsonify({
            "error": "Unable to run knowledge-base ingestion"
        }), 500