# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-08-17

### Added

- Model Context Protocol support with MCP server and client integration.
- PostgreSQL vector storage with pgvector for persistent retrieval.
- SentenceTransformer-based embeddings for semantic retrieval.
- BM25 and hybrid retrieval with reciprocal rank fusion.
- Productionized RAG pipeline using PostgreSQL, semantic search, and hybrid search.
- LLM tool calling support through the provider abstraction.
- Iterative agent execution loop for multi-step tool-using workflows.
- Conversation summarization for long-running conversations.

### Changed

- Updated memory implementations with Redis-backed memory and summary persistence.
- Integrated conversation summaries into chat and RAG workflows.
- Improved backend configuration through centralized settings.
- Expanded backend and frontend containerization with Docker and Docker Compose.

### Testing

- Backend test suite expanded to 202 passing tests.
