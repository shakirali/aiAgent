from google.adk.tools.tool_context import ToolContext
from vertexai import rag
from .utils import normalize_corpus_name, create_success_response, create_error_response


def create_corpus(
    corpus_name: str, 
    tool_context: ToolContext
) -> dict:
    """Create a new corpus with the specified name for RAG ingestion.

    Args:
    corpus_name (str): The name for the new corpus
    tool_context (ToolContext): The tool context for the state management

    """
    try:
        normalized_name = normalize_corpus_name(corpus_name)

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

        return create_success_response(
            f"Corpus '{normalized_name}' created successfully",
            {
                "name": normalized_name,
                "status": "created"
            }
        )
    except Exception as e:
        return create_error_response(str(e), "create_corpus")


