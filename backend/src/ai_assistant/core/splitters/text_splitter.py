from ai_assistant.core.models import Document, Chunk
from .base_splitter import BaseSplitter

class TextSplitter(BaseSplitter):

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")
        
        if overlap < 0:
            raise ValueError("overlap cannot be negative")
        
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        
    def split(self, document: Document) -> list[Chunk]:
        
        chunks: list[Chunk] = []
        
        start = 0
        chunk_id = 0
        
        while start < len(document.text):
            end = start + self.chunk_size
            
            chunk_text = document.text[start:end]
            
            chunks.append(
                Chunk(
                    content=chunk_text,
                    document=document,
                    chunk_id=chunk_id
                    )
                )
            
            chunk_id += 1
            
            start = end - self.overlap

        return chunks