import json
import os

import faiss
import numpy as np

from app.config import Config


class RetrievalService:

    def __init__(self):
        self.index = None
        self.documents = []

        self.index_path = os.path.join(
            Config.VECTOR_STORE_PATH,
            "index.faiss"
        )

        self.documents_path = os.path.join(
            Config.VECTOR_STORE_PATH,
            "documents.json"
        )

        self._load()

    def _load(self):
        if not os.path.exists(self.index_path):
            return

        if not os.path.exists(self.documents_path):
            return

        self.index = faiss.read_index(
            self.index_path
        )

        with open(
            self.documents_path,
            "r",
            encoding="utf-8"
        ) as file:
            self.documents = json.load(file)

    def search(
        self,
        embedding: list[float],
        top_k: int | None = None
    ):
        if self.index is None:
            return []

        if not self.documents:
            return []

        top_k = top_k or Config.TOP_K

        search_count = min(
            top_k,
            len(self.documents)
        )

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            vector,
            search_count
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):
            if index < 0:
                continue

            if index >= len(self.documents):
                continue

            if float(distance) > Config.RAG_DISTANCE_THRESHOLD:
                continue

            document = self.documents[index].copy()

            document["score"] = float(distance)

            results.append(document)

        results.sort(
            key=lambda document: document["score"]
        )

        return results