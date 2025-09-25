from typing import Optional, TypedDict

class CreateCorpusResult(TypedDict):
    name: str
    description: str
    status: str


class ToolContext(TypedDict, total=False):
    description: str


def create_corpus(corpus_name: str, tool_context: ToolContext) -> CreateCorpusResult:
    """Create a new (logical) corpus for RAG ingestion.

    This is a lightweight stub that validates inputs and returns a structured
    response. It does not perform any remote calls yet.
    """
    if not corpus_name or not corpus_name.strip():
        raise ValueError("corpus_name is required and must be non-empty")

    normalized_name = corpus_name.strip()
    corpus_description = ""
    desc = tool_context.get("description")
    if isinstance(desc, str):
        corpus_description = desc.strip()

    return {
        "name": normalized_name,
        "description": corpus_description,
        "status": "created",
    }


