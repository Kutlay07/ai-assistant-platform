# Retrieval

## Overview

The retrieval pipeline is responsible for preparing, indexing, and retrieving external knowledge independently from workflow logic.

Each component has a single responsibility and communicates through abstractions, allowing implementations to evolve independently.

The retrieval system consists of:

- `Documents`
- `TextSplitter`
- `Embedder`
- `VectorStore`
- `SemanticRetriever`, `BM25Retriever`, and `HybridRetriever`
- `SearchService`

See [RAG Pipeline](../diagrams/rag-pipeline.md) for the diagram.



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

`MockEmbedder` is intended for testing only and is not used by the running application.

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



## Retrievers

Retrievers locate the most relevant document chunks for a query.

The assistant communicates through the `BaseRetriever` abstraction.

### Current Implementations

- `SemanticRetriever`
- `BM25Retriever`
- `HybridRetriever` (used by the running application)

### Planned Implementations

- `MultiVectorRetriever`



### SemanticRetriever

`SemanticRetriever` embeds the query through a `BaseEmbedder` and performs a vector
similarity search through a `BaseVectorStore`.

Dependencies:

- `BaseEmbedder`
- `BaseVectorStore`



### BM25Retriever

`BM25Retriever` performs lexical ranking over an in-memory BM25 index. The index is built
at application startup from the chunks already stored in the vector store.



### HybridRetriever

`HybridRetriever` queries both the semantic and the BM25 retriever and merges the two
result lists using reciprocal rank fusion. It is the retriever wired into the FastAPI
application and is consumed by workflows through `SearchService`.



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