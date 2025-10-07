""" Stores and verifies the information from a .env file needed to connect to the Dynamics API """

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

@dataclass(frozen = True)
class DynamicsConfig:
    """Stores and verifies the parameters for the Dynamics API as an immutable object"""

    tenant_id: str
    environment_uri: str
    client_id: str = "51f81489-12ee-4a9e-aaae-a2591f45987d" # Default Dynamics Developer GUID
    authority_base: str = "https://login.microsoftonline.com/"
    scope_suffix: str = "user_impersonation"

    def __post_init__(self):
        """Validates the configuration after initialization."""
        self._validate_config()

    def _validate_config(self):
        """Validate required configuration fields."""
        if not self.client_id:
            raise ValueError("CLIENT_ID is required")

        if not self.tenant_id:
            raise ValueError("TENANT_ID is required")

        if not self.environment_uri:
            raise ValueError("ENVIRONMENT_URI is required")

        # Validate URI format
        if not self.environment_uri.startswith('https://'):
            raise ValueError("ENVIRONMENT_URI must start with 'https://'")

    @property
    def scope(self) -> str:
        """Generate the full OAuth scope for authentication."""
        return f"{self.environment_uri.rstrip('/')}/{self.scope_suffix}"

    @property
    def authority_url(self) -> str:
        """Generate the full authority URL for authentication."""
        return f"{self.authority_base.rstrip('/')}/{self.tenant_id}"

    @property
    def api_base_url(self) -> str:
        """Generate the base URL for API calls."""
        return f"{self.environment_uri.rstrip('/')}/api/data/v9.2/"

class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""

def get_config(env_file: str = None) -> DynamicsConfig:
    """
    Get the singleton configuration instance.

    Args:
        env_file: Optional path to .env file. If None, looks for .env in current / parent directory.
    
    Returns:
        DynamicsConfig: Validated configuration object
    
    Raises:
        ConfigurationError: If required configuration is missing or invalid
    """
    if not hasattr(get_config, '_config'):
        get_config._config = load_config(env_file)
    return get_config._config



def load_config(env_file: str = None) -> DynamicsConfig:
    """
    Load configuration from a .env file.
    
    Args:
        env_file: Optional path to .env file. If None, looks for .env in current / parent directory.
    
    Returns:
        DynamicsConfig: Validated configuration object
    
    Raises:
        ConfigurationError: If required configuration is missing or invalid
    """
    try:
        # Load .env file
        if env_file:
            load_dotenv(env_file)
        else:
            # Look for .env in current directory and parent directories
            env_path = Path('.env')
            if not env_path.exists():
                env_path = Path('../.env')

            if env_path.exists():
                load_dotenv(env_path)

        # Strips, then adds trailing slashes from the URIs for consistency
        environment_uri = os.getenv('ENVIRONMENT_URI', '').rstrip('/') + "/"
        authority_base = os.getenv('AUTHORITY_BASE', 'https://login.microsoftonline.com').rstrip('/') + "/"

        # Create configuration from environment variables
        config = DynamicsConfig(
            client_id = os.getenv('CLIENT_ID', '51f81489-12ee-4a9e-aaae-a2591f45987d'),
            tenant_id = os.getenv('TENANT_ID', ''),
            environment_uri = environment_uri,
            authority_base = authority_base,
            scope_suffix = os.getenv('SCOPE_SUFFIX', 'user_impersonation')
        )

        return config

    except ValueError as e:
        raise ConfigurationError(f"Invalid configuration: {e}") from e
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}") from e

# Example usage
if __name__ == "__main__":
    try:
        example_config = get_config("env.example")
        print("Configuration loaded successfully!")
        print(f"API Base URL: {example_config.api_base_url}")
        print(f"Authority URL: {example_config.authority_url}")
        print(f"Scope: {example_config.scope}")

    except ConfigurationError as e:
        print(f"Configuration error: {e}")
