# Architecture Overview

## Overview

AI Assistant is a production-oriented, provider-independent AI assistant framework built around clean architecture principles and organized as a monorepo with a FastAPI backend and a Vite + React frontend.

The system supports multiple operational workflows—conversational chat, Retrieval-Augmented Generation (RAG), and multi-step agent execution—while remaining highly modular and extensible.

The HTTP API currently exposes the chat and RAG workflows. The agent components (`AgentWorkflow`, `AgentExecutionLoop`, planners, tools) are part of the core library and are exercised by tests, but they are not served through an endpoint in this release.

All core components communicate exclusively through clean abstractions, allowing vector stores, memory backends, LLM providers, and other infrastructure components to be replaced without affecting the rest of the application.

---

## Design Principles

- **Modular Architecture**: Decoupled components with single, well-defined responsibilities.
- **Provider Independence**: Core domain and workflow layers depend only on abstract interfaces (`BaseLLM`, `BaseMemory`, `BaseRetriever`, `BaseTool`, `BasePlanner`).
- **Dependency Injection**: Dependencies are passed into constructors or route handlers rather than hardcoded.
- **Full-Stack End-to-End Execution**: Seamless integration between the React UI streaming client and the FastAPI streaming endpoints (chunked HTTP responses).
- **Clean Interfaces & Contracts**: Strong typing with Pydantic schemas and TypeScript interfaces.
- **Incremental Development**: Features are implemented iteratively with corresponding automated tests and documentation.

---



## High-Level Architecture

The following diagram illustrates the overall architecture of the AI Assistant and the relationships between its major components.

See [System Architecture](../diagrams/system-architecture.md) for the current diagram.

Requests enter through the FastAPI API layer, are routed to the appropriate workflow by the Assistant, and interact with shared services such as memory, prompt building, retrieval, and LLM providers. The frontend communicates with the backend through JSON REST calls and chunked streaming responses read with `fetch` + `ReadableStream` (the streaming endpoints return `text/plain`, not Server-Sent Events).

---

## Core Subsystems & Components

| Component | Module Location | Responsibility |
|---|---|---|
| **Assistant** | `backend/src/ai_assistant/core/assistant.py` | Top-level orchestrator executing configured workflows via dependency injection |
| **Workflows** | `backend/src/ai_assistant/core/workflows/` | Workflow strategies (`ChatWorkflow`, `RAGWorkflow`, `AgentWorkflow`) |
| **LLM Engine** | `backend/src/ai_assistant/core/llms/` | `BaseLLM` interface, the `create_llm()` factory, and concrete providers (`GroqProvider`, `MockLLM`, and the `LocalProvider` placeholder) |
| **Memory** | `backend/src/ai_assistant/core/memory/` | `BaseMemory` with `FileMemory` (JSON, wired by default), `RedisMemory`, `MockMemory`, and the `SummarizingMemory` decorator |
| **Document Loaders** | `backend/src/ai_assistant/core/loaders/` | Document ingestion (`PDFLoader`, `TextLoader`) producing domain `Document` models |
| **Text Splitter** | `backend/src/ai_assistant/core/splitters/` | Splitting document content into overlapping `Chunk` domain models |
| **Embeddings & Vector Stores** | `backend/src/ai_assistant/core/embedders/`, `vector_stores/` | Vector representation generation and chunk similarity search |
| **Retrievers & Services** | `backend/src/ai_assistant/core/retrievers/`, `services/` | `SemanticRetriever`, `BM25Retriever`, and `HybridRetriever` (reciprocal rank fusion) behind `SearchService` |
| **Tools & Validation** | `backend/src/ai_assistant/core/tools/` | `BaseTool`, `ToolRegistry`, and `ToolCallValidator` for safe function execution |
| **Planners** | `backend/src/ai_assistant/core/planners/` | `BasePlanner` and `RuleBasedPlanner` for multi-step agent task decomposition |
| **API Layer** | `backend/src/ai_assistant/api/` | FastAPI application exposing `/api/v1/chat`, `/api/v1/chat/stream`, `/api/v1/chat/history`, `/api/v1/rag`, `/api/v1/rag/stream`, and `/api/v1/health` |
| **Frontend UI** | `frontend/src/` | Vite + React 19 + TypeScript web application consuming the chunked streaming responses |

---

## Architecture Decision Records (ADRs)

- [ADR-0001: Project Philosophy](../decisions/ADR-0001-project-philosophy.md)
- [ADR-0002: Provider Independence](../decisions/ADR-0002-provider-independence.md)

---

## Documentation Structure

For a deeper discussion of each subsystem, see:
- [Assistant Architecture](assistant.md)
- [Workflows Specification](workflows.md)
- [Memory Persistence Architecture](memory.md)
- [LLM Abstraction & Providers](llm.md)
- [Retrieval & RAG Pipeline](retrieval.md)
- [Planner & Multi-Step Reasoning](planner.md)
- [Tools Framework](tools.md)
- [Request Lifecycle](lifecycle.md)