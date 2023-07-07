# pip install pandas # if needed

import pandas as pd
import authenticate_with_msal

# Parameters
entity_m = 'systemusers'
entity_n = 'teams'
m_to_n_relationship = 'teammembership_association'
path_to_csv = 'data/M to N.csv' 
# Column names in CSV must match entity_m and entity_n above

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession("env.json")
session = authentication[0]
environmentURI = authentication[1]

# reading the CSV
df = pd.read_csv(path_to_csv)

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():
    record_m = row[entity_m]
    record_n = row[entity_n]
    
    request_uri = f'{environmentURI}api/data/v9.2/{entity_m}({record_m})/{m_to_n_relationship}/$ref'
    odata_id = f'{environmentURI}api/data/v9.2/{entity_n}({record_n})'
    post_json = { "@odata.id": odata_id }

    r = session.post(request_uri, json = post_json)
    
    if r.status_code != 204:
        failures += 1
        raw = r.content.decode('utf-8')
        print(f'Error linking {record_m} to {record_n}. Error {r.status_code}: \n{raw}\n')
    
    else:
        successful_updates += 1

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES.\n{failures} FAILURES.') 