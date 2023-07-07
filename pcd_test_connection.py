import authenticate_with_msal

# Parameters
PathToEnvironmentJSON = "example-env.json"

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession(PathToEnvironmentJSON)
session = authentication[0]
environmentURI = authentication[1]

# a test request to the URI
request_uri = f'{environmentURI}api/data/v9.2/systemusers?$top=1&$select=internalemailaddress'

r = session.get(request_uri)

if r.status_code != 200:
    print("Request failed. Error code:")
    raw = r.content.decode('utf-8')
    print(raw)

else:
    print("Connection successful")