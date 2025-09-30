"""Utility functions for the RAG agent"""

from google.adk.tools.tool_context import ToolContext
from vertexai import rag
from typing import Optional, Dict, Any
import logging

def get_corpus(corpus_name: str) -> Optional[Any]:
    """Get a corpus by display name.
    
    Args:
        corpus_name (str): The display name of the corpus to find
        
    Returns:
        Optional[Any]: The corpus object if found, None otherwise
    """
    try:
        corpora_pager = rag.list_corpora()
        for corpus in corpora_pager:
            if corpus.display_name == corpus_name:
                print(corpus)
                return corpus
        return None
    except Exception as e:
        logging.error(f"Error getting corpus '{corpus_name}': {str(e)}")
        return None

def get_corpus_by_name(corpus_name: str) -> Optional[Any]:
    """Get a corpus by its resource name.
    
    Args:
        corpus_name (str): The resource name of the corpus to find
        
    Returns:
        Optional[Any]: The corpus object if found, None otherwise
    """
    try:
        return rag.get_corpus(name=corpus_name)
    except Exception as e:
        logging.error(f"Error getting corpus by name '{corpus_name}': {str(e)}")
        return None

def create_error_response(error_message: str, context: str = "") -> Dict[str, Any]:
    """Create a standardized error response.
    
    Args:
        error_message (str): The error message
        context (str): Additional context about where the error occurred
        
    Returns:
        Dict[str, Any]: Standardized error response
    """
    response = {"error": error_message}
    if context:
        response["context"] = context
    return response

def create_success_response(message: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a standardized success response.
    
    Args:
        message (str): The success message
        data (Dict[str, Any]): Additional data to include in the response
        
    Returns:
        Dict[str, Any]: Standardized success response
    """
    response = {
        "status": "success",
        "message": message
    }
    if data:
        response.update(data)
    return response

def validate_corpus_name(corpus_name: str) -> bool:
    """Validate that a corpus name is not empty or None.
    
    Args:
        corpus_name (str): The corpus name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return corpus_name is not None and corpus_name.strip() != ""

def normalize_corpus_name(corpus_name: str) -> str:
    """Normalize a corpus name by stripping whitespace.
    
    Args:
        corpus_name (str): The corpus name to normalize
        
    Returns:
        str: The normalized corpus name
        
    Raises:
        ValueError: If the corpus name is empty after normalization
    """
    if not validate_corpus_name(corpus_name):
        raise ValueError("corpus_name is required and must be non-empty")
    return corpus_name.strip()

class CorpusManager:
    """A class to manage corpus operations with consistent error handling."""
    
    @staticmethod
    def get_corpus_by_display_name(corpus_name: str) -> Optional[Any]:
        """Get a corpus by its display name using the utility function."""
        return get_corpus(corpus_name)
    
    @staticmethod
    def get_corpus_by_resource_name(corpus_name: str) -> Optional[Any]:
        """Get a corpus by its resource name using the utility function."""
        return get_corpus_by_name(corpus_name)
    
    @staticmethod
    def validate_and_get_corpus(corpus_name: str) -> tuple[Optional[Any], Optional[Dict[str, Any]]]:
        """Validate corpus name and get corpus object.
        
        Returns:
            tuple: (corpus_object, error_response) - one will be None
        """
        if not validate_corpus_name(corpus_name):
            error = create_error_response(
                f"Invalid corpus name: '{corpus_name}'", 
                "corpus_validation"
            )
            return None, error
        
        corpus = get_corpus(corpus_name)
        if corpus is None:
            error = create_error_response(
                f"Corpus '{corpus_name}' not found", 
                "corpus_lookup"
            )
            return None, error
        
        return corpus, None

class ResponseFormatter:
    """A class to handle consistent response formatting across all tools."""
    
    @staticmethod
    def format_corpus_list(corpora_list: list) -> Dict[str, Any]:
        """Format a list of corpora for consistent response structure."""
        return create_success_response(
            f"Successfully listed {len(corpora_list)} corpora",
            {"corpora": corpora_list}
        )
    
    @staticmethod
    def format_file_list(corpus_name: str, files_list: list) -> Dict[str, Any]:
        """Format a list of files for consistent response structure."""
        return create_success_response(
            f"Successfully listed files for corpus '{corpus_name}'",
            {
                "corpus_name": corpus_name,
                "files": files_list,
                "total_files": len(files_list),
            }
        )
    
    @staticmethod
    def format_query_results(corpus_name: str, query: str, results: list) -> Dict[str, Any]:
        """Format query results for consistent response structure."""
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