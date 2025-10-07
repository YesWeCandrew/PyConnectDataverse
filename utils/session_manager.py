"""This module uses the information stored in the .env to create an authenticated 
interactive session which is used to make requests to Dynamics 365"""

import msal
import requests

class AuthenticationError(Exception):
    """Raised when authentication fails."""

class SessionManager:
    """Manages authentication and session creation for Dynamics 365."""

    def __init__(self, config):
        """
        Initialize the SessionManager given the passed config.

        Args:
            config (dynamics_config.DynamicsConfig): A configuration instance
        """
        self.config = config
        self._session: requests.Session = None
        self._app: msal.PublicClientApplication = None

    def _create_msal_app(self) -> msal.PublicClientApplication:
        """Create and configure MSAL application."""
        if not self._app:
            self._app = msal.PublicClientApplication(
                client_id = self.config.client_id,
                authority = self.config.authority_url,
                # Uncomment if you want to enable broker authentication
                # allow_broker=True,
            )
        return self._app

    def _acquire_token_interactive(self) -> dict:
        """
        Acquire token using interactive authentication.
        
        Returns:
            dict: Token result from MSAL
            
        Raises:
            AuthenticationError: If authentication fails
        """
        app = self._create_msal_app()
        scope = [self.config.scope]

        print("A local browser window will open for you to sign in. CTRL+C to cancel.")

        try:
            result = app.acquire_token_interactive(
                scopes=scope,
                # Optional parameters:
                # login_hint="user@domain.com",  # Pre-fill username
                # prompt=msal.Prompt.SELECT_ACCOUNT,  # Force account selector
            )

            if "access_token" not in result:
                raise AuthenticationError(result)

            return result

        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {e}") from e

    def _create_authenticated_session(self, access_token: str) -> requests.Session:
        """
        Create requests session with authentication headers.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            requests.Session: Configured session object
        """
        session = requests.Session()

        # Set authentication header
        session.headers.update({
            'Authorization': f'Bearer {access_token}'
        })

        # Set OData headers for Dynamics 365
        session.headers.update({
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'If-None-Match': 'null'
        })

        return session

    def validate_session(self) -> bool:
        """
        Validate the session by making a test API call.

        Returns:
            bool: Whether the response to WhoAmI is 200 or not.
        """
        test_url = f"{self.config.api_base_url}WhoAmI"
        response = self._session.get(test_url, timeout=30)

        if response.status_code == 200:
            return True
        else:
            print(f"Session validation failed: {response.status_code} - {response.text}")
            return False

    def get_authenticated_session(self) -> requests.Session:
        """
        Get authenticated requests session. Tests the session by making a WhoAmI request.
        If timed out or unauthorised, attempts to acquire a new interactive token.
            
        Returns:
            requests.Session: Authenticated session ready for API calls
            
        Raises:
            AuthenticationError: If authentication fails
        """
        if not self._session or not self.validate_session():

            # Acquire token
            token_result = self._acquire_token_interactive()
            access_token = token_result["access_token"]

            # Create session
            self._session = self._create_authenticated_session(access_token)

        return self._session

    def close_session(self) -> None:
        """Close the current session."""
        if self._session:
            self._session.close()
            self._session = None

# Example usage
if __name__ == "__main__":
    
    from dynamics_config import get_config
    example_config = get_config("env.example")

    manager = SessionManager(example_config)
    example_session = manager.get_authenticated_session()
    if manager.validate_session():
        print("Session created successfully")
    else:
        print("Session was not created successfully")
