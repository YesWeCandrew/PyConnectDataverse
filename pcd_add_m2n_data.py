# pip install pandas # if needed

import pandas as pd
from utils.session_manager import SessionManager
from utils.dynamics_config import get_config

# Parameters
PathToDotEnv = "env.example"
PathToCSV = 'data\M to N.csv' 
EntityM = 'systemusers'
EntityN = 'teams'
MToNRelationship = 'teammembership_association'
# Column names in CSV must match EntityM and EntityN above

# Getting authenticated Requests object.
config = get_config(PathToDotEnv)
manager = SessionManager(config)
session = manager.get_authenticated_session()

# reading the CSV
df = pd.read_csv(PathToCSV)

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():
    record_m = row[EntityM]
    record_n = row[EntityN]

    request_uri = f'{config.api_base_url}{EntityM}({record_m})/{MToNRelationship}/$ref'
    odata_id = f'{config.api_base_url}{EntityN}({record_n})'
    post_json = { "@odata.id": odata_id }

    r = session.post(request_uri, json = post_json)

    if r.status_code != 204:
        failures += 1
        raw = r.content.decode('utf-8')
        print(f'Error linking {record_m} to {record_n}. Error {r.status_code}: \n{raw}\n')

    else:
        successful_updates += 1

    if index % 10 == 0:
        print(f"Processed: {index + 1}")

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES.\n{failures} FAILURES.')
