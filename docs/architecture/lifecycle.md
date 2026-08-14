# Lifecycle

## Overview

This document describes the major execution flows inside the assistant.

It focuses on how requests, dependencies, and retrieval move through the system rather than describing individual components.



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
SemanticRetriever
   │
   ▼
Vector Store
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