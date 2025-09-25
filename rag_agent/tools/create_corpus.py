from typing import Optional, TypedDict
from google.adk.tools.tool_context import ToolContext
from vertexai import rag

class CreateCorpusResult(TypedDict):
    name: str
    status: str


class ToolContext(TypedDict, total=False):
    description: str


def create_corpus(corpus_name: str, tool_context: ToolContext) -> CreateCorpusResult:
    """Create a new corpus with the specified name for RAG ingestion.

    Args:
    corpus_name (str): The name for the new corpus
    tool_context (ToolContext): The tool context for the state management

    """
    if not corpus_name or not corpus_name.strip():
        raise ValueError("corpus_name is required and must be non-empty")

    normalized_name = corpus_name.strip()

    EMBEDDING_MODEL = "publishers/google/models/text-embedding-005"  # @param {type:"string", isTemplate: true}  # fmt: skip

    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model=EMBEDDING_MODEL
        )
    )
    rag_corpus = rag.create_corpus(
        display_name=normalized_name,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        )
    )

    return {
        "name": normalized_name,
        "status": "created"
    }


