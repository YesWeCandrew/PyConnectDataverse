# pip install pandas # if needed

import pandas as pd
import authenticate_with_msal

# Parameters
PathToEnvironmentJSON = "example-env.json"
PathToCSV = 'data\M to N.csv' 
EntityM = 'systemusers'
EntityN = 'teams'
MToNRelationship = 'teammembership_association'
# Column names in CSV must match EntityM and EntityN above

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession(PathToEnvironmentJSON)
session = authentication[0]
environmentURI = authentication[1]

# reading the CSV
df = pd.read_csv(PathToCSV)

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():
    record_m = row[EntityM]
    record_n = row[EntityN]
    
    request_uri = f'{environmentURI}api/data/v9.2/{EntityM}({record_m})/{MToNRelationship}/$ref'
    odata_id = f'{environmentURI}api/data/v9.2/{EntityN}({record_n})'
    post_json = { "@odata.id": odata_id }

    r = session.post(request_uri, json = post_json)
    
    if r.status_code != 204:
        failures += 1
        raw = r.content.decode('utf-8')
        print(f'Error linking {record_m} to {record_n}. Error {r.status_code}: \n{raw}\n')
    
    else:
        successful_updates += 1

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES.\n{failures} FAILURES.') 