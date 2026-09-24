import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import json
import re

import faiss
import numpy as np

from app.config import Config
from app.services.embedding_service import EmbeddingService


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def split_into_chunks(text: str):
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        if len(current) + len(paragraph) + 2 <= CHUNK_SIZE:
            current += paragraph + "\n\n"
            continue

        if current:
            chunks.append(current.strip())

        overlap = current[-CHUNK_OVERLAP:] if current else ""

        current = overlap + paragraph + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks


def extract_date(text: str):
    """
    Extract a document date from markdown content.

    Supported format:

        Date: 2026-09-20

    Returns None when no valid date is found.
    """

    match = re.search(
        r"(?im)^\s*date\s*:\s*(\d{4}-\d{2}-\d{2})\s*$",
        text
    )

    if match:
        return match.group(1)

    return None


def load_documents():
    documents = []

    knowledge_path = Path(Config.KNOWLEDGE_DIR)

    for file_path in knowledge_path.rglob("*.md"):

        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            continue

        category = file_path.parent.name
        title = file_path.stem.replace("_", " ").title()

        document_date = extract_date(content)

        chunks = split_into_chunks(content)

        for number, chunk in enumerate(chunks, start=1):

            documents.append({
                "source": str(file_path),
                "title": title,
                "category": category,
                "date": document_date,
                "chunk_id": f"{file_path.stem}-{number:03d}",
                "content": chunk,
            })

    return documents


def build_index(documents):

    embedding_service = EmbeddingService()

    vectors = []

    for number, document in enumerate(
        documents,
        start=1
    ):

        print(
            f"Embedding {number}/{len(documents)}: "
            f"{document['chunk_id']}"
        )

        vector = embedding_service.embed(
            document["content"]
        )

        vectors.append(vector)

    if not vectors:
        raise RuntimeError(
            "No embeddings were generated."
        )

    matrix = np.array(
        vectors,
        dtype="float32"
    )

    embedding_dimension = matrix.shape[1]

    print(
        f"Embedding dimension detected: "
        f"{embedding_dimension}"
    )

    index = faiss.IndexFlatL2(
        embedding_dimension
    )

    index.add(matrix)

    output_path = Path(
        Config.VECTOR_STORE_PATH
    )

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(output_path / "index.faiss")
    )

    with open(
        output_path / "documents.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            documents,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\nSaved {len(documents)} chunks."
    )

    print(
        f"Saved FAISS index to: "
        f"{output_path / 'index.faiss'}"
    )

    print(
        f"Saved document metadata to: "
        f"{output_path / 'documents.json'}"
    )


def main():

    print(
        "Starting chunked knowledge-base ingestion..."
    )

    documents = load_documents()

    print(
        f"Found {len(documents)} chunks."
    )

    if not documents:
        raise RuntimeError(
            "No non-empty markdown files found."
        )

    build_index(documents)

    print(
        "\nRAG vector store created successfully."
    )


if __name__ == "__main__":
    main()