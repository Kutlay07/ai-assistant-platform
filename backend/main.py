from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_assistant.api.v1 import router as v1_router
from ai_assistant.core.config import settings
from ai_assistant.core.embedders import SentenceTransformerEmbedder
from ai_assistant.core.retrievers import (
    BM25Retriever,
    HybridRetriever,
    SemanticRetriever,
)
from ai_assistant.core.services import SearchService
from ai_assistant.core.vector_stores import PostgreSQLVectorStore
from ai_assistant.core.memory import FileMemory


@asynccontextmanager
async def lifespan(app: FastAPI):

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
    if chunks:
        bm25_retriever.build_index(chunks)

    hybrid_retriever = HybridRetriever(
        vector_retriever=semantic_retriever,
        bm25_retriever=bm25_retriever,
    )

    memory = FileMemory(settings.memory_path)

    search_service = SearchService(
        retriever=hybrid_retriever,
    )

    app.state.search_service = search_service
    app.state.memory = memory

    yield

    if hasattr(vector_store, "close"):
        vector_store.close()


app = FastAPI(
    title="AI Assistant",
    summary="Production-ready AI assistant",
    description=(
        "A production-ready AI assistant built from scratch with a modular "
        "architecture, supporting chat, RAG, agent workflows, tool calling, "
        "and modern LLM integrations."
    ),
    version="1.0.0",
    contact={
        "name": "Kutlay",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )