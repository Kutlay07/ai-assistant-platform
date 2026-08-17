# Workflows

## Overview

Workflows define how requests are processed.

Each workflow implements a specific execution strategy while exposing the same interface through `BaseWorkflow`.

The Assistant delegates execution to the configured workflow without knowing its implementation details.

The HTTP API constructs `ChatWorkflow` and `RAGWorkflow`. `AgentWorkflow` is available at
library level and is covered by tests, but it is not exposed through an endpoint in the
current release.



## BaseWorkflow

`BaseWorkflow` defines the common contract implemented by every workflow.

Each workflow is responsible for orchestrating reusable components such as memory, prompt generation, retrieval, planning, and language model interaction.



## ChatWorkflow

### Overview

`ChatWorkflow` is the default conversational workflow.

It coordinates memory, prompt construction, and language model generation while remaining focused on orchestration.

### Responsibilities

- Receive a request.
- Retrieve conversation history.
- Build a prompt.
- Generate a response.
- Store conversation history.
- Return the response.

### Dependencies

- `PromptBuilder`
- `BaseMemory`
- `BaseLLM`



## RAGWorkflow

### Overview

`RAGWorkflow` augments requests with retrieved context before generating a response.

It coordinates retrieval, prompt construction, language model generation, and memory through shared abstractions.

```text
User
   │
   ▼
RAGWorkflow
   │
   ▼
SearchService
   │
   ▼
HybridRetriever (semantic + BM25, reciprocal rank fusion)
   │
   ▼
Embedder / Vector Store
   │
   ▼
PromptBuilder
   │
   ▼
LLM
```

### Responsibilities

- Receive a request.
- Retrieve relevant document chunks.
- Build a retrieval-augmented prompt.
- Generate a response.
- Store conversation history.
- Return the response.

### Dependencies

- `SearchService`
- `PromptBuilder`
- `BaseLLM`
- `BaseMemory`



## AgentWorkflow

### Overview

`AgentWorkflow` extends the execution model by introducing planning and tool usage.

Instead of directly generating a response, the workflow creates an execution plan, performs reasoning step-by-step, invokes tools when necessary, and stores intermediate results in memory.

### Execution Flow

```text
Request
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
Tool Executor
   │
   ▼
Memory
```

### Responsibilities

- Receive a request.
- Generate an execution plan.
- Build prompts.
- Generate tool calls.
- Parse tool calls.
- Execute tools.
- Store intermediate results.
- Return the final response.

### Dependencies

- `BasePlanner`
- `PromptBuilder`
- `BaseMemory`
- `BaseLLM`
- `ToolCallParser`
- Tool Executor