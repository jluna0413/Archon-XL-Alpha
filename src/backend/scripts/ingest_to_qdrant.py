"""Simple Qdrant ingestion PoC for Phase 1.

This script attempts to connect to a local Qdrant instance and insert one sample vector.
It is intentionally tolerant of connection failures for environments without Qdrant running.
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
import uuid
import random


def ingest_sample():
    try:
        client = QdrantClient(host="localhost", port=6333)
        collection_name = "phase1_docs"
        vector = [random.random() for _ in range(64)]
        payload = {"text": "Sample doc for Archon-XL Phase1"}

        # Recreate collection (idempotent for PoC)
        try:
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=rest.VectorParams(size=len(vector), distance=rest.Distance.COSINE),
            )
        except Exception:
            # older client versions or server settings may not allow recreate; ignore
            pass

        point = rest.PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload)
        client.upsert(collection_name=collection_name, points=[point])
        print(f"Ingested sample to Qdrant (collection={collection_name})")
    except Exception as e:
        print("QDRANT_INGEST_FAILED:", e)


if __name__ == "__main__":
    ingest_sample()
