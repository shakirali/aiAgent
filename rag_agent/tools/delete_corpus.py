from google.adk.tools.tool_context import ToolContext
from vertexai import rag
from .utils import get_corpus, create_error_response, create_success_response

def delete_corpus(corpus_name: str, tool_context: ToolContext) -> dict:
    """Delete a corpus."""
    try:
        corpus = get_corpus(corpus_name)
        if corpus is None:
            return create_error_response(f"Corpus {corpus_name} not found", "delete_corpus")
        
        rag.delete_corpus(corpus_name=corpus.name)
        return create_success_response(f"Corpus {corpus_name} deleted successfully")
    except Exception as e:
        return create_error_response(str(e), "delete_corpus")