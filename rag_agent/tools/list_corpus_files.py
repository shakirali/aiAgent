from vertexai import rag
from google.adk.tools.tool_context import ToolContext
from .utils import get_corpus, create_error_response, create_success_response

def list_corpus_files(corpus_name: str, tool_context: ToolContext) -> dict:
    """List all files in a corpus."""
    try:
        # Use utility function to get corpus
        corpus = get_corpus(corpus_name)
        print(corpus)
        if corpus is None:
            return create_error_response(f"Corpus {corpus_name} not found", "list_corpus_files")
        
        # Get files from the corpus
        files = list(rag.list_files(corpus_name=corpus.name))
        files_list = [file.display_name for file in files]
        
        return create_success_response(
            f"Successfully listed files for corpus '{corpus_name}'",
            {
                "corpus_name": corpus_name,
                "files": files_list,
                "total_files": len(files),
            }
        )
    except Exception as e:
        return create_error_response(str(e), "list_corpus_files")