import tempfile
import docker
import os
from typing import Optional
from google.adk.tools import ToolContext

class AnalyticsConfig:
    """Configuration for analytics agent."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("ANALYTICS_AGENT_MODEL", "gemini-pro")
        self.docker_timeout = int(os.getenv("DOCKER_TIMEOUT", "30"))
        self.docker_image = os.getenv("DOCKER_IMAGE", "python:3.9-slim")
    
    def validate(self) -> None:
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

def _create_docker_container(client: docker.DockerClient, temp_file: str) -> docker.models.containers.Container:
    """Create and return a Docker container for code execution."""
    config = AnalyticsConfig()
    return client.containers.run(
        config.docker_image,
        f'python {os.path.basename(temp_file)}',
        volumes={os.path.dirname(temp_file): {'bind': '/tmp', 'mode': 'rw'}},
        working_dir='/tmp',
        remove=True,
        stdout=True,
        stderr=True,
        timeout=config.docker_timeout
    )

def execute_python_code(code: str, tool_context: Optional[ToolContext] = None) -> str:
    """Execute Python code in a Docker container."""
    temp_file = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run in Docker container
        client = docker.from_env()
        container = _create_docker_container(client, temp_file)
        execution_result = container.decode('utf-8')

        if tool_context:
            tool_context.state["result"] = execution_result
            
        return execution_result

    except Exception as e:
        error_message = f"Error: {str(e)}"
        if tool_context:
            tool_context.state["result"] = error_message
        return error_message
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)