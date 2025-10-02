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
from google.adk.code_executors import VertexAiCodeExecutor
from google.adk.agents import Agent
from .prompts import return_instructions_ds
import google.genai as genai
import subprocess
import tempfile
import os
import docker
from google.adk.tools import ToolContext

def generate_python_from_nl(natural_language: str, tool_context: ToolContext = None) -> str:
    """Generate Python code using Google's Gemini."""
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("MODEL")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    
    prompt = f"Generate Python code for: {natural_language}"
    response = model.generate_content(prompt)
    return response.text

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
        
        return container.decode('utf-8')
        
    except Exception as e:
        return f"Error: {str(e)}"

root_agent = Agent(
    model=os.getenv("ANALYTICS_AGENT_MODEL"),
    name="data_science_agent",
    instruction=return_instructions_ds(),
    tools = [
        generate_python_from_nl,
        execute_python_code,
    ]    
)