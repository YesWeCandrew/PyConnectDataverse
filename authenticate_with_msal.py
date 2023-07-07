import msal
import requests 
import json
import logging

# Optional logging
# logging.basicConfig(level=logging.DEBUG)  # Enable DEBUG log for entire script
# logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs

def getAuthenticatedSession(envJson: str):

    config = json.load(open(envJson))

    environmentURI = config["environmentURI"]
    scope = [environmentURI + '/' + config["scopeSuffix"]]
    clientID = config["clientID"]
    authority = config["authorityBase"] + config["tenantID"]

    app = msal.PublicClientApplication(
        clientID, authority=authority,
        # allow_broker=True,  # If opted in, you will be guided to meet the prerequisites, when applicable
                            # See also: https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-desktop-acquire-token-wam#wam-value-proposition
        )

    # The pattern to acquire a token looks like this.
    result = None

    logging.info("Obtaining new token from AAD.")
    print("A local browser window will open for you to sign in. CTRL+C to cancel.")
    result = app.acquire_token_interactive(  # Only works if your app is registered with redirect_uri as http://localhost
        scope,
        #parent_window_handle=...,  # If broker is enabled, you will be guided to provide a window handle
        # login_hint=username,  # Optional.
            # If you know the username ahead of time, this parameter can pre-fill
            # the username (or email address) field of the sign-in page for the user,
            # Often, apps use this parameter during reauthentication,
            # after already extracting the username from an earlier sign-in
            # by using the preferred_username claim from returned id_token_claims.

        # prompt=msal.Prompt.SELECT_ACCOUNT,  # Or simply "select_account". Optional. It forces to show account selector page
        #prompt=msal.Prompt.CREATE,  # Or simply "create". Optional. It brings user to a self-service sign-up flow.
            # Prerequisite: https://docs.microsoft.com/en-us/azure/active-directory/external-identities/self-service-sign-up-user-flow
        )

    if "access_token" in result:
        # Calling graph using the access token
        print("Token received successfully")
        session = requests.Session()
        session.headers.update(dict(Authorization='Bearer {}'.format(result['access_token'])))
        session.headers.update({'OData-MaxVersion': '4.0', 'OData-Version': '4.0', 'If-None-Match': 'null', 'Accept': 'application/json'})

        return session, environmentURI

    else:
        print(result("error"))
        print(result("error_description"))
        print(result("correlation_id"))