# pip install pandas # if needed

import pandas as pd
import json
from utils.session_manager import SessionManager
from utils.dynamics_config import get_config

# Parameters
PathToDotEnv = "env.example"
EntityBeingAddedTo = "contacts"
PathToCSVOfRecords = "data\pcd_update_records.csv"
# Column names in CSV must match EntityM and EntityN above

# Getting authenticated Requests object.
config = get_config(PathToDotEnv)
manager = SessionManager(config)
session = manager.get_authenticated_session()
session.headers.update({'If-Match': '*'})

# reading the CSV
df = pd.read_csv(PathToCSVOfRecords)
records = json.loads(df.drop(columns='GUID').to_json(orient = "records"))

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():
    
    guid = row['GUID']
    request_uri = f'{config.api_base_url}{EntityBeingAddedTo}({guid})'
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