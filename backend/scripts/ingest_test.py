"""Development helper: index a text file into the pgvector knowledge base.

Usage:
    python scripts/ingest_test.py path/to/document.txt
"""

import sys

from ai_assistant.core.config import settings
from ai_assistant.core.embedders.sentence_transformers_embedder import SentenceTransformerEmbedder
from ai_assistant.core.loaders.text_loader import TextLoader
from ai_assistant.core.splitters.text_splitter import TextSplitter
from ai_assistant.core.vector_stores.postgresql_vector_store import PostgreSQLVectorStore


if len(sys.argv) < 2:
    raise SystemExit("Usage: python scripts/ingest_test.py <path-to-text-file>")

path = sys.argv[1]

loader = TextLoader()

document = loader.load(path)

splitter = TextSplitter(
    chunk_size=100,
    overlap=20,
)

chunks = splitter.split(document)

embedder = SentenceTransformerEmbedder()

for chunk in chunks:
    chunk.embedding = embedder.embed(chunk.content)

vector_store = PostgreSQLVectorStore(
    settings.postgres_connection_string,
)

vector_store.add(chunks)

print(f"Indexed {len(chunks)} chunks from {path}.")
