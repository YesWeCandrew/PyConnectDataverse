import authenticate_with_msal
import json
import pandas as pd
import time
from requests import Request 

# Parameters
PathToEnvironmentJSON = "example-env.json"
PathToCSVOfRecords = "data\pcd_merge_records.csv"
RecordType = 'Microsoft.Dynamics.CRM.contact' # The record type you are merging together
PerformParentingCheck = False # Whether you want to check they share the same parent

# Useful to ensure some columns get imported as expected to avoid failures
dtypes = {
    "mobilephone": "string"
}

# read the CSV and convert to dataframe
df = pd.read_csv(PathToCSVOfRecords, dtype = dtypes)

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession(PathToEnvironmentJSON)
session = authentication[0]
environmentURI = authentication[1]
session.headers.update({"Content-Type" : "application/json; charset=utf-8", "Accept": "application/json"})

# the post uri
request_uri = f'{environmentURI}api/data/v9.2/Merge'

records = []

for _, row in df.iterrows():
    # Get the additional columns (exclude Duplicate group, Target, Subordinate)
    # Only include non-null values
    update_content = {}
    for col in df.columns:
        if col not in ['target', 'subordinate']:
            if pd.notna(row[col]):  # Only include non-null values
                update_content[col] = row[col]
    
    # Build the merge JSON payload
    merge_payload = {
        "Target": {
            "contactid": row['target'],
            "@odata.type": RecordType
        },
        "Subordinate": {
            "contactid": row['subordinate'],
            "@odata.type": RecordType
        },
        "PerformParentingChecks": PerformParentingCheck
    }
    
    # Only add UpdateContent if there are non-null values
    if update_content:
        update_content["@odata.type"] = RecordType
        merge_payload["UpdateContent"] = update_content
    
    records.append(merge_payload)

row = 0
successful_updates = 0
failures = 0
expected_updates = len(df)
percent_complete = 0
timeStart = time.perf_counter()

for record in records:
    req = Request('POST', request_uri, json=record, headers = session.headers).prepare()
    

    r = session.send(req)
    record['HTTP_RESPONSE'] = r.status_code
    record['HTTP_CONTENT'] = r.content

    if r.status_code != 204:
        failures += 1

    else:
        successful_updates +=1 

    row += 1
    if round(row/expected_updates * 100,0) != percent_complete:
        percent_complete = round(row/expected_updates * 100,0)
        print(f"{percent_complete}% complete")

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES. {failures} FAILURES.') 
print(f'IMPORTING TOOK: {round(time.perf_counter() - timeStart,0)} SECONDS ')

# Writing to output.json
with open("output/output.json", "w") as outfile:
    json.dump(records, outfile, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))