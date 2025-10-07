import time
import uuid
import json
import pandas as pd
from requests import Request
from utils.session_manager import SessionManager
from utils.dynamics_config import get_config

# Imports using the batch function which is faster for big imports
# https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/execute-batch-operations-using-web-api

# Known issue: the last record in the batch will fail to import. I am still determining the cause of this.

# When importing a lookup column:
#   Use the logical name of the RELATIONSHIP and "@odatabind" as the column name
#   Wrap each GUID in the logical name of the entity it references for example: accounts(GUID)

# Parameters
PathToDotEnv = "env.example"
EntityBeingAddedTo = "contacts"
PathToCSVOfRecords = "data\pcd_create_records.csv"
BatchSize = 500 # can be up to 1000 requests per batch

# The Pandas data types of the columns imported to avoid import issues
dtypes = {
    "parentcustomerid_account@odata.bind": "object",
    "lastname": "object",
    "firstname": "object"
}

# Getting authenticated Requests object.
config = get_config(PathToDotEnv)
manager = SessionManager(config)
session = manager.get_authenticated_session()

# choose how you would like to act on errors
session.headers.update({"Prefer" : "odata.continue-on-error"})

# the post uri
batch_uri = f'{config.api_base_url}$batch'
request_uri = f'/api/data/v9.2/{EntityBeingAddedTo}'

base_preamble = """
Content-Type: application/http
Content-Transfer-Encoding: binary

POST """ + request_uri + """ HTTP/1.1
Content-Type: application/json; type=entry

"""

# read the CSV and convert to dataframe
df = pd.read_csv(PathToCSVOfRecords, dtype = dtypes)

first = 0
last = BatchSize - 1

resultdf = df.copy()
resultdf['codes'] = ""
resultdf['messages'] = ""
resultdf['batch'] = ""

timeStart = time.perf_counter()

while first < len(df.index):

    boundary = f"batch_{str(uuid.uuid4())}"
    session.headers.update({"Content-Type" : f'multipart/mixed; boundary="{boundary}"'})
    boundary = ("--"+boundary).encode()
    preamble = boundary + base_preamble.encode()

    requestdf = df.loc[first:last]
    body = "".encode()
    records = json.loads(requestdf.to_json(orient = "records"))

    for record in records:
        body = body + preamble + json.dumps(record).encode()

    body = body + "\n".encode() + boundary + "--".encode()

    req = Request(
        'POST', 
        batch_uri, 
        data = body, 
        headers = session.headers
        ).prepare()

    r = session.send(req)

    response = r.content.decode('utf-8')
    delimiter = response[0:52]

    responses = response.split(delimiter)

    codes = []
    messages = []

    for i in range(1,len(responses)-1):
        responses[i] = responses[i].removeprefix("\r\nContent-Type: application/http\r\nContent-Transfer-Encoding: binary\r\n\r\nHTTP/1.1 ")
        responses[i] = responses[i].split('\r\n',1)
        codes.append(responses[i][0])
        messages.append(responses[i][1])
        i += 1
    
    resultdf.loc[first:last,'codes'] = codes
    resultdf.loc[first:last,'messages'] = messages
    resultdf.loc[first:last,'batch'] = boundary.decode()

    resultdf.loc[first:last].to_csv(f"output\{boundary.decode()}.csv")

    successes =  sum(1 for i in codes if i == "204 No Content")
    sent = len(requestdf.index)

    print(f"Records {first} : {last} sent for import. {sent - successes} failures.")

    first = last + 1
    last = min(last + BatchSize,len(df.index))

print(f'IMPORTING TOOK: {round(time.perf_counter() - timeStart,0)} SECONDS ')
resultdf.to_csv("output\imported.csv")
