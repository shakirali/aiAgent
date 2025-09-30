from google.adk.tools.tool_context import ToolContext
from vertexai import rag
import tempfile
import os
import requests
from .utils import get_corpus, create_error_response, create_success_response

PDF_URL = "https://abc.xyz/assets/77/51/9841ad5c4fbe85b4440c47a4df8d/goog-10-k-2024.pdf"
PDF_FILENAME = "goog-10-k-2024.pdf"

def add_data(
    corpus_name: str,
    tool_context: ToolContext
) -> dict:
    """Add data to a corpus."""
    try:
        # Use utility function to get corpus
        corpus = get_corpus(corpus_name)
        print(corpus)
        if corpus is None:
            return create_error_response(f"Corpus {corpus_name} not found", "add_data")
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, PDF_FILENAME)
            download_pdf_from_url(PDF_URL, pdf_path)
            upload_pdf_to_corpus(
                corpus_name=corpus.name, 
                pdf_path=pdf_path, 
                display_name=PDF_FILENAME, 
                description="Google 10-K 2024"
            )
            return create_success_response(
                f"Successfully added {PDF_FILENAME} to corpus '{corpus_name}'",
                {
                    "corpus_name": corpus_name,
                    "file_name": PDF_FILENAME,
                    "status": "added"
                }
            )
    except Exception as e:
        return create_error_response(str(e), "add_data")

def download_pdf_from_url(url: str, output_path: str) -> None:
    response =requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path,"wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"PDF file downloaded successfully to {output_path}")
    return output_path

def upload_pdf_to_corpus(corpus_name, pdf_path, display_name, description):
    try:
        rag_file =rag.upload_file(
            corpus_name=corpus_name,
            path=pdf_path,
            display_name=display_name,
            description=description
        )
        return rag_file
    except Exception as e:
        return {"error": str(e)}


