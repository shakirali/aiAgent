from typing import Optional
from google.adk.tools import ToolContext
import os
import google.genai as genai

def _code_generation_prompt(natural_language: str, context_info: str = "") -> str:
    """Build the prompt for code generation."""
    return f"""Generate clean, executable Python code for the following request: {natural_language}{context_info}
    
    Requirements:
    - Return only the Python code, no explanations or markdown formatting
    - Use standard libraries (pandas, numpy, matplotlib, seaborn, scipy, sklearn, etc.)
    - Include all necessary imports at the top
    - Make the code self-contained and executable
    - Include print statements to show results and outputs
    - Handle data parsing if data is provided in the request
    - Use proper error handling where appropriate
    - Follow Python best practices
    - If working with data, always explore it first (show shape, head, info)
    - For visualizations, use clear titles and labels
    
    Code:"""

def _clean_response_code(code: str) -> str:
    """Clean up the response code by removing markdown formatting."""
    code = code.strip()
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()

def generate_python_from_nl(natural_language: str, tool_context: Optional[ToolContext] = None) -> str:
    """Generate Python code from natural language using Google's Gemini."""
    try:
        # Check for API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY environment variable not set"
        
        # Use the same model as the agent for consistency
        model_name = os.getenv("ANALYTICS_AGENT_MODEL", "gemini-pro")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # Build context-aware prompt
        context_info = ""
        if tool_context and "query_result" in tool_context.state:
            context_info = f"\n\nContext: You have access to data from a previous query: {tool_context.state['query_result']}"
        
        # Enhanced prompt for better code generation
        prompt = _code_generation_prompt(natural_language, context_info)
        
        response = model.generate_content(prompt)
        
        code = _clean_response_code(response.text)
        return code.strip()
        
    except Exception as e:
        return f"Error generating code: {str(e)}"