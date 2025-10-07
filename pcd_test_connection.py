from utils.session_manager import SessionManager
from utils.dynamics_config import get_config

# Parameters
PathToDotEnv = "env.example"

# Getting authenticated Requests object.
config = get_config(PathToDotEnv)
manager = SessionManager(config)
session = manager.get_authenticated_session()

# a test request to the URI
request_uri = f'{config.api_base_url}WhoAmI'

r = session.get(request_uri)

if r.status_code != 200:
    print("Request failed. Error code:")
    raw = r.content.decode('utf-8')
    print(raw)

else:
    print("Connection successful")