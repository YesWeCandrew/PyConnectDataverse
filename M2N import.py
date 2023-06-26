# pip install adal # if needed
# pip install pyDataverse # if needed
# pip install pandas # if needed
# pip install python-dotenv # if needed

import adal
import requests
import pandas as pd
from dotenv import dotenv_values

# Global configs loaded from .env file. See EXAMPLE.env for info
config = dotenv_values(".env") 
CLIENT_ID = config.get('CLIENT_ID')
RESOURCE_URI = config.get('RESOURCE_URI')
AUTHORITY_URI = config.get('AUTHORITY_URI')
CLIENT_SECRET = config.get('CLIENT_SECRET')

# Parameters
entity_m = 'systemusers'
entity_n = 'teams'
m_to_n_relationship = 'teammembership_association'
path_to_csv = 'M to N.csv' 
# Column names in CSV must match entity_m and entity_n above

# Getting access token.
context = adal.AuthenticationContext(AUTHORITY_URI, api_version=None)
token = context.acquire_token_with_client_credentials(RESOURCE_URI, CLIENT_ID, CLIENT_SECRET)
session = requests.Session()
session.headers.update(dict(Authorization='Bearer {}'.format(token.get('accessToken'))))
session.headers.update({'OData-MaxVersion': '4.0', 'OData-Version': '4.0', 'If-None-Match': 'null', 'Accept': 'application/json'})

# reading the CSV
df = pd.read_csv(path_to_csv)

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():
    record_m = row[entity_m]
    record_n = row[entity_n]
    
    request_uri = f'{RESOURCE_URI}/api/data/v9.2/{entity_m}({record_m})/{m_to_n_relationship}/$ref'
    odata_id = f'{RESOURCE_URI}/api/data/v9.2/{entity_n}({record_n})'
    post_json = { "@odata.id": odata_id }

    r = session.post(request_uri, json = post_json)
    
    if r.status_code != 204:
        failures += 1
        raw = r.content.decode('utf-8')
        print(f'Error linking {record_m} to {record_n}. Error {r.status_code}: \n{raw}\n')
    
    else:
        successful_updates += 1

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES.\n{failures} FAILURES.') 