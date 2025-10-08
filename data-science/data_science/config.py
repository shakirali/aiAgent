import os
from typing import Optional
from dotenv import load_dotenv
from data_science.exceptions import ConfigurationException

load_dotenv()

def get_env_var(var_name: str) -> str:
    """Get required environment variable."""
    value = os.getenv(var_name)
    if not value or not value.strip():
        raise ConfigurationException(f'Missing required environment variable: {var_name}')
    return value.strip()

def get_optional_env_var(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """Get optional environment variable."""
    value = os.getenv(var_name, default)
    return value.strip() if value else value