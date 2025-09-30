from google.adk.tools.tool_context import ToolContext
from vertexai import rag
import logging
from .utils import get_corpus, create_error_response, create_success_response

DEFAULT_TOP_K = 3
DEFAULT_DISTANCE_THRESHOLD = 0.5

def rag_query(
    corpus_name: str, 
    query: str, 
    tool_context: ToolContext
    ) -> dict:

    """Query a corpus and return the results"""
    try:
        # Use utility function to get corpus
        corpus = get_corpus(corpus_name)
        if corpus is None:
            return create_error_response(f"Corpus {corpus_name} not found", "rag_query")
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=DEFAULT_TOP_K,
            filter=rag.Filter(vector_distance_threshold=DEFAULT_DISTANCE_THRESHOLD),
        )
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=corpus.name,
                )
            ],
            text=query,
            rag_retrieval_config=rag_retrieval_config
        )
        results = []
        if hasattr(response, "contexts") and response.contexts:
            for ctx_group in response.contexts.contexts:
                result = {
                    "source_uri": (
                        ctx_group.source_uri if hasattr(ctx_group, "source_uri") else ""
                    ),
                    "source_name": (
                        ctx_group.source_display_name
                        if hasattr(ctx_group, "source_display_name")
                        else ""
                    ),
                    "text": ctx_group.text if hasattr(ctx_group, "text") else "",
                    "score": ctx_group.score if hasattr(ctx_group, "score") else 0.0,
                }
                results.append(result)

        # If we didn't find any results
        if not results:
            return {
                "status": "warning",
                "message": f"No results found in corpus '{corpus_name}' for query: '{query}'",
                "query": query,
                "corpus_name": corpus_name,
                "results": [],
                "results_count": 0,
            }

        return create_success_response(
            f"Successfully queried corpus '{corpus_name}'",
            {
                "query": query,
                "corpus_name": corpus_name,
                "results": results,
                "results_count": len(results),
            }
        )
    except Exception as e:
        error_msg = f"Error querying corpus: {str(e)}"
        logging.error(error_msg)
        return create_error_response(error_msg, "rag_query")