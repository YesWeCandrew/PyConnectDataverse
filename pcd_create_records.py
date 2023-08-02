import authenticate_with_msal
import json
import pandas as pd
import time
from requests import Request, Session 

# Parameters
PathToEnvironmentJSON = "example-env.json"
EntityBeingAddedTo = "contacts"
PathToCSVOfRecords = "data\pcd_create_records.csv"
AttributesToReturn = "?$select=lastname" # optionally include the attributes to return, otherwise all are returned

# The Pandas data types of the columns imported to avoid import issues
dtypes = {
    "parentcustomerid_account@odata.bind": "object",
    "lastname": "object",
    "firstname": "object"
}

# read the CSV and convert to dataframe
df = pd.read_csv(PathToCSVOfRecords, dtype = dtypes)

records = json.loads(df.to_json(orient = "records"))

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession(PathToEnvironmentJSON)
session = authentication[0]
environmentURI = authentication[1]
session.headers.update({"Prefer" : "return=representation"})

# the post uri
request_uri = f'{environmentURI}api/data/v9.2/{EntityBeingAddedTo}{AttributesToReturn}'

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
    record['HTTP_CONTENT'] = json.loads(r.content.decode('utf-8'))

    if r.status_code != 201:
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
    outfile.write(json.dumps(records))