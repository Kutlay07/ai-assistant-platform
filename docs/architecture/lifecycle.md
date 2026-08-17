# Lifecycle

## Overview

This document describes the major execution flows inside the assistant.

It focuses on how requests, dependencies, and retrieval move through the system rather than describing individual components.

For the end-to-end sequence of an HTTP request, including the streaming and tool-calling
branches, see [Request Lifecycle](../diagrams/request-lifecycle.md).



## Dependency Graph

```text
                 Assistant
                     │
                     ▼
                BaseWorkflow
        ┌────────────┼──────────────┐
        │            │              │
        ▼            ▼              ▼
 ChatWorkflow   RAGWorkflow   AgentWorkflow
        │            │              │
        │            │              ▼
        │            │         BasePlanner
        │            │              │
        │            │              ▼
        │            │            Plan
        │            │              │
        │            │              ▼
        │            │       ToolCallParser
        │            │              │
        │            │              ▼
        │            │          ToolCall
        │            │              │
        │            │              ▼
        │            │     ToolCallValidator
        │            │              │
        │            │              ▼
        │            │        ToolRegistry
        │            │              │
        │            │              ▼
        │            │           BaseTool
        │            │
        └────────────┼──────────────────────┐
                     ▼                      ▼
                PromptBuilder          BaseMemory
                     │
                     ▼
                  BaseLLM
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   MockLLM    GroqProvider   LocalProvider
```



## Chat Request Lifecycle

```text
User
  │
  ▼
HTTP Request
  │
  ▼
FastAPI
  │
  ▼
Pydantic Validation
  │
  ▼
Assistant
  │
  ▼
Workflow
  │
  ├────────► Memory
  ├────────► PromptBuilder
  └────────► LLM
                 │
                 ▼
            Provider
                 │
                 ▼
           HTTP Response
                 │
                 ▼
               User
```



## RAG Request Lifecycle

```text
User
   │
   ▼
Assistant
   │
   ▼
RAGWorkflow
   │
   ▼
SearchService
   │
   ▼
HybridRetriever
   │
   ├────────► SemanticRetriever ──► Embedder ──► Vector Store
   │
   └────────► BM25Retriever ──► In-memory BM25 index
   │
   ▼
PromptBuilder
   │
   ▼
LLM
   │
   ▼
Response
```



## Agent Request Lifecycle

The agent flow is available at library level only; no HTTP endpoint constructs an
`AgentWorkflow` in the current release.

```text
User
   │
   ▼
Assistant
   │
   ▼
AgentWorkflow
   │
   ▼
Planner
   │
   ▼
Plan
   │
   ▼
PromptBuilder
   │
   ▼
LLM
   │
   ▼
ToolCallParser
   │
   ▼
ToolCallValidator
   │
   ▼
ToolRegistry
   │
   ▼
Tool
   │
   ▼
Memory
   │
   ▼
Response
```



## Related Documentation

Document ingestion is part of the retrieval subsystem.

For details about document ingestion and retrieval, see:

- [Retrieval Architecture](retrieval.md)