from ..core.embedders import SentenceTransformerEmbedder
from ..core.llms import MockLLM
from ..core.memory import MockMemory
from ..core.prompts import PromptBuilder
from ..core.retrievers import SemanticRetriever
from ..core.services import SearchService
from ..core.vector_stores import MockVectorStore
from ..core.workflows import RAGWorkflow


embedder = SentenceTransformerEmbedder()

vector_store = MockVectorStore()

retriever = SemanticRetriever(
    embedder=embedder,
    vector_store=vector_store,
)

search_service = SearchService(
    retriever=retriever,
)

llm = MockLLM()
prompt_builder = PromptBuilder()
memory = MockMemory()

rag_workflow = RAGWorkflow(
    llm=llm,
    prompt_builder=prompt_builder,
    search_service=search_service,
    memory=memory,
)