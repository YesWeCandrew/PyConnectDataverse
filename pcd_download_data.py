import authenticate_with_msal
import json

# Parameters
PathToEnvironmentJSON = "example-env.json"
EntityToDownload = "systemusers"

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession(PathToEnvironmentJSON)
session = authentication[0]
environmentURI = authentication[1]

# an example download request to the URI
request_uri = f'{environmentURI}api/data/v9.2/{EntityToDownload}?$top=10&$select=firstname,lastname,internalemailaddress'

r = session.get(request_uri)

if r.status_code != 200:
    print("Request failed. Error code:")

else:
    print("Request successful")

raw = json.dumps(json.loads(r.content.decode('utf-8')), indent = True)
# Writing to output.json
with open("output/output.json", "w") as outfile:
    outfile.write(raw)