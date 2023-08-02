# pip install pandas # if needed

import pandas as pd
import authenticate_with_msal
import json

# Parameters
PathToEnvironmentJSON = "example-env.json"
EntityBeingAddedTo = "contacts"
PathToCSVOfRecords = "data\pcd_update_records.csv"
# Column names in CSV must match EntityM and EntityN above

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession(PathToEnvironmentJSON)
session = authentication[0]
environmentURI = authentication[1]
session.headers.update({'If-Match': '*'})

# reading the CSV
df = pd.read_csv(PathToCSVOfRecords)
records = json.loads(df.drop(columns='GUID').to_json(orient = "records"))

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():
    
    guid = row['GUID']
    request_uri = f'{environmentURI}api/data/v9.2/{EntityBeingAddedTo}({guid})'
    post_json = records[index]

    r = session.patch(request_uri, json = post_json)
    
    if r.status_code != 204:
        failures += 1
        raw = r.content.decode('utf-8')
        print(f'Error updating {guid}. Error {r.status_code}: \n{raw}\n')
    
    else:
        successful_updates += 1
        
    if index % 10 == 0:
        print(f"Processed: {index + 1}")
        
print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES.\n{failures} FAILURES.') 