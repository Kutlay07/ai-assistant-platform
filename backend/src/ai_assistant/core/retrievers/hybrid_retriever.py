from ..models import Chunk, RetrievalOptions
from .semantic_retriever import SemanticRetriever
from .bm25_retriever import BM25Retriever
from .base_retriever import BaseRetriever


class HybridRetriever(BaseRetriever):
    
    def __init__(
        self,
        vector_retriever: SemanticRetriever,
        bm25_retriever: BM25Retriever
    ):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        
        
    def build_index(self, chunks: list[Chunk]):
        self.bm25_retriever.build_index(chunks)
        
        
    def retrieve(
        self,
        query: str,
        options: RetrievalOptions | None = None
    ) -> list[Chunk]:
        
        if options is None:
            options = RetrievalOptions()
            
        candidate_options = RetrievalOptions(
            top_k=options.candidate_k
        )
        
        vector_results = self.vector_retriever.retrieve(
            query, 
            candidate_options
        )
        
        bm25_results = self.bm25_retriever.retrieve(
            query,
            candidate_options
        )
        
        rrf_scores = {}
        
        k = 60
        
        for rank, chunk in enumerate(vector_results, start=1):
            key = chunk.chunk_id
            
            rrf_scores[key] = {
                "chunk": chunk,
                "score": 1 / (k + rank)
            }
            
            
        for rank, chunk in enumerate(bm25_results, start=1):
            key = chunk.chunk_id
            
            score = 1 / (k + rank)
            
            if key in rrf_scores:
                rrf_scores[key]["score"] += score
            else:
                rrf_scores[key] = {
                    "chunk": chunk,
                    "score": score,
                }
                
        sorted_results = sorted(
            rrf_scores.values(),
            key=lambda item: item["score"],
            reverse=True,
        )
        
        return [item["chunk"] for item in sorted_results[:options.top_k]]