from ai_assistant.core.config import settings
from ai_assistant.core.embedders.sentence_transformers_embedder import SentenceTransformerEmbedder
from ai_assistant.core.loaders.text_loader import TextLoader
from ai_assistant.core.splitters.text_splitter import TextSplitter
from ai_assistant.core.vector_stores.postgresql_vector_store import PostgreSQLVectorStore


loader = TextLoader()

document = loader.load(
    "data\\test.txt"
)

splitter = TextSplitter(
    chunk_size=100,
    overlap=20,
)

chunks = splitter.split(document)

embedder = SentenceTransformerEmbedder()

for chunk in chunks:
    chunk.embedding = embedder.embed(chunk.content)

vector_store = PostgreSQLVectorStore(
    "postgresql://ai_assistant:ai_assistant@localhost:5432/ai_assistant"
)

vector_store.add(chunks)