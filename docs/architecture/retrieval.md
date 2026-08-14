# Retrieval

## Overview

The retrieval pipeline is responsible for preparing, indexing, and retrieving external knowledge independently from workflow logic.

Each component has a single responsibility and communicates through abstractions, allowing implementations to evolve independently.

The retrieval system consists of:

- `Documents`
- `TextSplitter`
- `Embedder`
- `VectorStore`
- `SemanticRetriever`



## Documents

Documents provide provider-independent domain models shared across the retrieval pipeline.

They represent textual knowledge before and after chunking.

### Current Models

- `Document`
- `Chunk`

### Planned Extensions

Future document models may include:

- Metadata
- Source information
- Chunk relationships
- Embedding references



## Text Splitter

`TextSplitter` is responsible for dividing documents into overlapping chunks before indexing.

Chunking is isolated from retrieval and embedding logic to keep each component focused on a single responsibility.

The generated chunks become the input for the embedding pipeline.



## Embedder

Embedders generate vector representations of text for semantic search.

The assistant communicates with embedding providers exclusively through the `BaseEmbedder` abstraction.

### Current Implementations

- `SentenceTransformerEmbedder`

### Planned Implementations

- `OpenAIEmbedder`
- `VoyageAIEmbedder`



### MockEmbedder

`MockEmbedder` is intended for development and testing.

Characteristics:

- Deterministic embeddings
- No external dependencies
- Fast execution



## Vector Store

Vector stores are responsible for storing embeddings and performing similarity search.

The assistant communicates with vector storage providers through the `BaseVectorStore` abstraction.

### Current Implementations

- `PostgreSQLVectorStore`

### Planned Implementations

- `ChromaVectorStore`
- `FAISSVectorStore`
- `PineconeVectorStore`



### MockVectorStore

`MockVectorStore` is an in-memory implementation intended for testing.

Characteristics:

- Stores chunks in memory
- Deterministic search
- No external database



## SemanticRetriever

SemanticRetrievers locate the most relevant document chunks for a query.

They combine embedding generation and vector search while remaining independent from concrete providers.

The assistant communicates through the `BaseRetriever` abstraction.

### Dependencies

- `BaseEmbedder`
- `BaseVectorStore`

### Current Implementations

- `SemanticRetriever`

### Planned Implementations

- `SemanticSemanticRetriever`
- `HybridSemanticRetriever`
- `MultiVectorSemanticRetriever`



### SemanticRetriever

`SemanticRetriever` is intended for development and testing.

It retrieves chunks by combining the configured embedder and vector store without relying on external retrieval systems.



## Document Ingestion Pipeline

The ingestion pipeline prepares external knowledge for semantic retrieval.

```text
Document Source
      │
      ▼
    Indexer
      │
      ▼
    Loader
      │
      ▼
   Document
      │
      ▼
 TextSplitter
      │
      ▼
    Chunks
      │
      ▼
   Embedder
      │
      ▼
 Vector Store
```



## Retrieval API

The retrieval layer supports configurable search parameters such as `top_k`, allowing workflows to control retrieval behavior independently from implementation details.