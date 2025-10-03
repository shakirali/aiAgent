# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data Science Agent V2: generate nl2py and use code interpreter to run the code."""
import os
from google.adk.agents import Agent
from .prompts import return_instructions_ds
import google.genai as genai
import subprocess
import tempfile
import os
import docker
from google.adk.tools import ToolContext

def generate_python_from_nl(natural_language: str, tool_context: ToolContext = None) -> str:
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
        prompt = f"""Generate clean, executable Python code for the following request: {natural_language}{context_info}
        
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
        
        response = model.generate_content(prompt)
        
        # Clean up the response
        code = response.text.strip()
        
        # Remove markdown formatting if present
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        
        return code.strip()
        
    except Exception as e:
        return f"Error generating code: {str(e)}"

def execute_python_code(code: str, tool_context: ToolContext = None) -> str:
    """Execute Python code in a Docker container."""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run in Docker container
        client = docker.from_env()
        container = client.containers.run(
            'python:3.9-slim',
            f'python {os.path.basename(temp_file)}',
            volumes={os.path.dirname(temp_file): {'bind': '/tmp', 'mode': 'rw'}},
            working_dir='/tmp',
            remove=True,
            stdout=True,
            stderr=True,
            timeout=30  # 30 second timeout
        )
        
        # Clean up
        os.unlink(temp_file)
        
        execution_result = container.decode('utf-8')

        if tool_context:
            tool_context.state["result"] = execution_result

        return execution_result
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        
        # Set error in context as well
        if tool_context:
            tool_context.state["result"] = error_message
            
        return error_message

root_agent = Agent(
    model=os.getenv("ANALYTICS_AGENT_MODEL"),
    name="data_science_agent",
    instruction=return_instructions_ds(),
    tools = [
        generate_python_from_nl,
        execute_python_code,
    ]    
)