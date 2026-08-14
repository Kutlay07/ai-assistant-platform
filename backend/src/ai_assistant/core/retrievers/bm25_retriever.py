from rank_bm25 import BM25Okapi
import numpy as np

from ..models import Chunk, RetrievalOptions
from .base_retriever import BaseRetriever


class BM25Retriever(BaseRetriever):
    
    def __init__(self):
        self.bm25 = None
        self.chunks = []
        
    def build_index(self, chunks: list[Chunk]):
        self.chunks = chunks
        
        tokenized_chunks = [
            chunk.content.lower().split()
            for chunk in chunks
        ]
        
        self.bm25 = BM25Okapi(tokenized_chunks)
        
    def retrieve(
        self, 
        query: str, 
        options: RetrievalOptions | None = None
        )-> list[Chunk]:
        
        if options is None:
            options = RetrievalOptions()
        
        query_tokens = query.lower().split()
        
        if self.bm25 is None:
            raise ValueError("BM25 index has not been built.")
        
        scores = self.bm25.get_scores(query_tokens)
        
        top_indices = np.argsort(scores)[::-1][:options.top_k]
        
        results = [
            self.chunks[i]
            for i in top_indices
        ]
        
        return results