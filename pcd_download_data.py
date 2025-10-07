import json
from utils.session_manager import SessionManager
from utils.dynamics_config import get_config

# Parameters
PathToDotEnv = "env.example"
EntityToDownload = "systemusers"

# Getting authenticated Requests object.
config = get_config(PathToDotEnv)
manager = SessionManager(config)
session = manager.get_authenticated_session()

# an example download request to the URI
request_uri = f'{config.api_base_url}{EntityToDownload}?$top=10&$select=firstname,lastname,internalemailaddress'

r = session.get(request_uri)

if r.status_code != 200:
    print("Request failed. Error code:")

else:
    print("Request successful")

raw = json.dumps(json.loads(r.content.decode('utf-8')), indent = True)
# Writing to output.json
with open("output/output.json", "w") as outfile:
    outfile.write(raw)