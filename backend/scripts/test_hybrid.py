from ai_assistant.api.dependencies import create_search_service
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
    "postgresql://ai_assistant:ai_assistant@localhost:5432/ai_assistant"
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

results = retriever.retrieve(
    "What is FastAPI?"
)

for chunk in results:
    print(
        chunk.chunk_id,
        chunk.content,
        )