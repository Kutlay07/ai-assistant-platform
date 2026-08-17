# System Architecture

Deployment and component overview of the stack started by `docker compose up`.

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

`*` `LocalProvider` is a placeholder and raises `NotImplementedError`.
Tool execution is implemented but the API constructs `ChatWorkflow` without a
`ToolExecutor`, so tools are library-level only in this release.
