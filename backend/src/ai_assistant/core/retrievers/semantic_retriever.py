import hashlib
from dataclasses import asdict

from ..cache.base_cache import BaseCache
from ..embedders import BaseEmbedder
from ..models import Chunk
from ..models import RetrievalOptions
from ..vector_stores import BaseVectorStore
from .base_retriever import BaseRetriever


class SemanticRetriever(BaseRetriever):

    def __init__(
        self,
        embedder: BaseEmbedder,
        vector_store: BaseVectorStore,
        cache: BaseCache | None = None,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.cache = cache

    def retrieve(
        self,
        query: str,
        options: RetrievalOptions | None = None,
    ) -> list[Chunk]:

        if options is None:
            options = RetrievalOptions()

        key = hashlib.sha256(
            f"{query}:{options.top_k}".encode()
        ).hexdigest()

        key = "retrieval:" + key

        if self.cache is not None:
            cached = self.cache.get(key)

            if cached is not None:
                return [
                    Chunk(**item)
                    for item in cached
                ]

        embedding = self.embedder.embed(query)

        results = self.vector_store.search(
            embedding=embedding,
            top_k=options.top_k,
        )

        if self.cache is not None:
            self.cache.set(
                key,
                [asdict(chunk) for chunk in results],
            )

        return results