from vertexai import rag
from google.adk.tools.tool_context import ToolContext
from .utils import create_error_response, create_success_response

def list_corpora(tool_context: ToolContext) -> dict:
    """List all corpora in the project."""
    try:
        corpora_pager = rag.list_corpora()
        corpora_list = []
        
        # Convert pager to list first to avoid serialization issues
        for corpus in corpora_pager:
            # Extract only serializable data
            corpus_data = {
                "display_name": str(corpus.display_name) if corpus.display_name else "",
                "name": str(corpus.name) if hasattr(corpus, 'name') and corpus.name else "",
            }
            corpora_list.append(corpus_data)
        
        return create_success_response(
            f"Successfully listed {len(corpora_list)} corpora",
            {"corpora": corpora_list}
        )
    except Exception as e:
        return create_error_response(f"Failed to list corpora: {str(e)}", "list_corpora")

