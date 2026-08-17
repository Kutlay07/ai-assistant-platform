# AI Assistant

> An AI assistant framework built from first principles, with a strong focus on clean architecture, modularity, provider independence, and full-stack integration.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL%20%2B%20pgvector-4169E1?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Demo

![AI Assistant Demo](docs/images/demo.png)

*A real-time conversation in the React frontend, streamed token by token over a chunked HTTP response.*

---

## What this is

A monorepo containing a FastAPI backend (the assistant engine) and a React 19 frontend.
Every subsystem — memory, retrieval, embeddings, vector storage, tools, planning, LLM
access — is implemented from scratch behind an abstract interface, so concrete providers
are interchangeable.

**Exposed over HTTP today:**

| Endpoint | Description |
|---|---|
| `POST /api/v1/chat` | Chat completion with persistent conversation memory |
| `POST /api/v1/chat/stream` | Same, streamed as a chunked `text/plain` body |
| `GET /api/v1/chat/history` | Stored conversation history |
| `POST /api/v1/rag` | Retrieval-augmented answer over the indexed knowledge base |
| `POST /api/v1/rag/stream` | Same, streamed |
| `GET /api/v1/health` | Health check |

Agent components (`AgentWorkflow`, `AgentExecutionLoop`, planners, the tool registry and
executor) are implemented and unit-tested as part of the core library, but they are **not
exposed as HTTP endpoints in this release**.

---

## 🚀 Quick Start

Requirements: Docker and Docker Compose.

```bash
git clone https://github.com/Kutlay07/ai-assistant-platform.git
cd ai-assistant-platform

cp .env.example .env      # runs on the mock provider; set LLM_API_KEY + LLM_PROVIDER=groq for real answers

docker compose up
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL + pgvector | `localhost:5432` |

The backend waits for PostgreSQL to become healthy, creates the `vector` extension and the
`chunks` table on startup, and downloads the sentence-transformers model on first run
(cached in a Docker volume).

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `mock` | `groq`, `mock`, or `local` (placeholder, not implemented) |
| `LLM_API_KEY` | – | Required for `groq` |
| `LLM_MODEL` | – | e.g. `llama-3.3-70b-versatile` |
| `LLM_BASE_URL` | – | e.g. `https://api.groq.com/openai/v1` |
| `MEMORY_PATH` | `conversation.json` | Conversation file used by `FileMemory` |
| `POSTGRES_CONNECTION_STRING` | `postgresql://ai_assistant:ai_assistant@localhost:5432/ai_assistant` | Compose overrides the host with the `postgres` service |
| `ENVIRONMENT` | `development` | `development` or `production` |

Set `LLM_PROVIDER=mock` to run the whole stack without any API key.

---

## 🏛️ Architecture

```mermaid
flowchart TB
    subgraph Client["Browser"]
        UI["React 19 UI<br/>ChatWindow / ChatInput"]
        SVC["chatService.ts<br/>fetch + ReadableStream"]
    end

    subgraph API["FastAPI (backend/main.py)"]
        R["Router /api/v1<br/>chat · chat/stream · chat/history<br/>rag · rag/stream · health"]
        DEP["dependencies.py<br/>get_assistant / get_rag_assistant"]
        ST["app.state (built in lifespan)<br/>SearchService · FileMemory"]
    end

    subgraph Core["Core"]
        AS["Assistant"]
        CW["ChatWorkflow"]
        RW["RAGWorkflow"]
        PB["PromptBuilder<br/>chat.txt / rag.txt"]
        MEM["FileMemory (BaseMemory)"]
        TOOLS["ToolRegistry · ToolExecutor<br/>ToolCallValidator"]
    end

    subgraph Retrieval["Retrieval"]
        SS["SearchService"]
        HR["HybridRetriever (RRF)"]
        SR["SemanticRetriever"]
        BM["BM25Retriever"]
        EMB["SentenceTransformerEmbedder"]
    end

    LLM["BaseLLM via create_llm()<br/>GroqProvider · MockLLM · LocalProvider*"]
    PG[("PostgreSQL + pgvector<br/>chunks")]
    FS[("conversation.json<br/>conversation_summary.json")]

    UI --> SVC
    SVC -->|"HTTP JSON / chunked text stream"| R
    R --> DEP
    DEP --> ST
    DEP --> AS
    AS --> CW
    AS --> RW
    CW --> PB
    RW --> PB
    CW --> MEM
    RW --> MEM
    CW -.->|"optional, not wired by the API"| TOOLS
    CW --> LLM
    RW --> LLM
    RW --> SS
    SS --> HR
    HR --> SR
    HR --> BM
    SR --> EMB
    SR --> PG
    MEM --> FS

    linkStyle default stroke:#1E90FF,stroke-width:1.6px
    classDef box fill:#F7F9FC,stroke:#C9D4E3,stroke-width:1px,rx:6,ry:6,color:#1F2937
    class UI,SVC,R,DEP,ST,AS,CW,RW,PB,MEM,TOOLS,SS,HR,SR,BM,EMB,LLM,PG,FS box
```

`*` `LocalProvider` reserves the extension point for locally hosted models and currently
raises `NotImplementedError`.

### Request lifecycle

```mermaid
%%{init: {"theme":"base","themeVariables":{"signalColor":"#1E90FF","signalTextColor":"#1F2937","lineColor":"#1E90FF","actorBorder":"#1E90FF","actorBkg":"#F7F9FC","activationBorderColor":"#1E90FF","noteBkgColor":"#EEF4FF","noteBorderColor":"#1E90FF"}}}%%
sequenceDiagram
    autonumber
    participant UI as React UI (chatService)
    participant API as FastAPI /api/v1
    participant A as Assistant
    participant W as ChatWorkflow / RAGWorkflow
    participant MEM as FileMemory
    participant S as SearchService
    participant L as BaseLLM
    participant T as ToolExecutor

    UI->>API: POST /chat/stream (or /chat, /rag, /rag/stream)
    API->>A: build via Depends(get_assistant / get_rag_assistant)
    A->>W: handle() -> run()  |  stream()
    W->>MEM: get_history() + get_summary()
    MEM-->>W: messages + summary

    opt RAG endpoints only
        W->>S: search(query)
        S-->>W: top-k chunks
    end

    W->>L: generate() / generate_with_tools() / stream(prompt)

    opt ChatWorkflow.run() with a tool executor configured
        L-->>W: ToolCall
        W->>T: execute(tool_call) [validate -> registry -> tool]
        T-->>W: ToolResult
        W->>L: generate_with_tools(messages + tool result)
    end

    alt streaming endpoint
        L-->>W: token chunks
        W-->>API: yield chunk
        API-->>UI: chunked text/plain body
    else non-streaming endpoint
        L-->>W: full text
        W-->>API: Response(output)
        API-->>UI: JSON response
    end

    W->>MEM: add_message(user) + add_message(assistant)
```

The remaining diagrams live in [docs/diagrams/](docs/diagrams/):
[Agent Workflow](docs/diagrams/agent-workflow.md) ·
[RAG Pipeline](docs/diagrams/rag-pipeline.md) ·
[Memory Architecture](docs/diagrams/memory-architecture.md) ·
[Provider Independence](docs/diagrams/provider-independence.md)

---

## ✨ Features

- **Provider-independent LLM engine** — `BaseLLM` with `GroqProvider` (OpenAI-compatible),
  `MockLLM`, and a `LocalProvider` placeholder, selected by `create_llm()`.
- **Hybrid RAG** — `SentenceTransformerEmbedder` (384-d) + `PostgreSQLVectorStore` (pgvector)
  combined with an in-memory BM25 index through reciprocal rank fusion.
- **Persistent, role-aware memory** — `FileMemory` (JSON) and `RedisMemory`, plus an opt-in
  `SummarizingMemory` decorator that compacts old turns via `LLMSummarizer`.
- **Streaming** — token-by-token chunked HTTP responses consumed by the React UI.
- **Agent core (library-level)** — `AgentWorkflow`, `AgentExecutionLoop`/`PlanExecutor`,
  `RuleBasedPlanner`, `ToolRegistry`, `ToolCallValidator`, `ToolExecutor`.
- **Clean architecture** — the core depends only on abstractions; concrete infrastructure is
  injected at the API boundary.

---

## 📁 Monorepo Structure

```text
ai-assistant-platform/
├── docker-compose.yml        # Full stack: backend, frontend, postgres (pgvector)
├── .env.example              # Environment template
├── backend/                  # FastAPI backend & core AI engine
│   ├── main.py               # Application entry point and lifespan wiring
│   ├── pyproject.toml        # Dependencies and pytest configuration
│   ├── src/ai_assistant/
│   │   ├── api/              # FastAPI routers (/api/v1) and schemas
│   │   ├── core/             # Workflows, LLMs, memory, retrieval, tools, planners
│   │   └── mcp/              # Experimental, not part of the release (see below)
│   └── tests/                # Unit and integration tests
├── frontend/                 # React 19 + Vite + Tailwind v4 chat UI
└── docs/                     # Architecture docs, ADRs, Mermaid diagrams
```

---

## 🛠️ Local Development

Docker Compose is the primary way to run the stack. For iterating on a single component,
the backend and frontend can also run directly — see [docs/development.md](docs/development.md).

```bash
# Backend (Python 3.11+)
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python main.py            # http://127.0.0.1:8000/docs

# Frontend (Node.js 22+)
cd frontend
npm install
npm run dev               # http://localhost:5173
```

A reachable PostgreSQL instance is required; the easiest option is
`docker compose up postgres`.

---

## 🧪 Testing

```bash
cd backend
python -m pytest          # 202 tests (199 passed, 3 skipped)

cd ../frontend
npm run lint
npm run build
```

---

## ⚠️ Known limitations

- A single global conversation is stored; there are no per-user sessions yet.
- Tool calling and the agent workflows are not reachable through the HTTP API.
- `RedisMemory` and `RedisCache` are implemented and tested but not wired into the running
  application, so Redis is not part of the Compose stack.
- `backend/src/ai_assistant/mcp/` is an experimental, incomplete MCP server sketch. It is
  not installed, not tested, and not part of the release surface.
- `LocalProvider` is a placeholder.

---

## 🗺️ Roadmap

Current version: **v1.2.0**. See [docs/roadmap.md](docs/roadmap.md).

---

## 📄 License

MIT — see [LICENSE](LICENSE).
