"""Development helper: run a hybrid retrieval query against the knowledge base.

Usage:
    python scripts/test_hybrid.py "What is FastAPI?"
"""

import sys

from ai_assistant.core.config import settings
from ai_assistant.core.embedders.sentence_transformers_embedder import SentenceTransformerEmbedder
from ai_assistant.core.retrievers import (
BM25Retriever, 
SemanticRetriever,
HybridRetriever,
)
from ai_assistant.core.vector_stores.postgresql_vector_store import PostgreSQLVectorStore



embedder = SentenceTransformerEmbedder()

vector_store = PostgreSQLVectorStore(
    settings.postgres_connection_string,
)

chunks = vector_store.get_all_chunks()

semantic_retriever = SemanticRetriever(
    embedder=embedder,
    vector_store=vector_store,
)

bm25_retriever = BM25Retriever()

bm25_retriever.build_index(chunks)

retriever = HybridRetriever(
    vector_retriever=semantic_retriever,
    bm25_retriever=bm25_retriever,
)

query = sys.argv[1] if len(sys.argv) > 1 else "What is FastAPI?"

results = retriever.retrieve(query)

for chunk in results:
    print(
        chunk.chunk_id,
        chunk.content,
        )