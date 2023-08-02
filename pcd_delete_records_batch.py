import authenticate_with_msal
import json
import pandas as pd
import time
import uuid
from requests import Request

# Known issue: the last record in the batch will fail to import. I am still determining the cause of this.

# Parameters
PathToEnvironmentJSON = "example-env.json"
EntityOfRecordsToDelete = "contacts"
PathToCSVOfRecords = "data\pcd_delete_records.csv"
BatchSize = 950

# Getting access token.
authentication = authenticate_with_msal.getAuthenticatedSession(PathToEnvironmentJSON)
session = authentication[0]
environmentURI = authentication[1]
# choose how you would like to act on errors
session.headers.update({"Prefer" : "odata.continue-on-error"})

# the post uri
batch_uri = f'{environmentURI}api/data/v9.2/$batch'
request_uri = f'/api/data/v9.2/{EntityOfRecordsToDelete}'

# read the CSV and convert to dataframe
df = pd.read_csv(PathToCSVOfRecords)

first = 0
last = BatchSize - 1

resultdf = df.copy()
resultdf['codes'] = ""
resultdf['messages'] = ""
resultdf['batch'] = ""

timeStart = time.perf_counter()

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
    boundary = "--"+boundary

    requestdf = df.loc[first:last]
    body = ""

    records = json.loads(requestdf.drop(columns='GUID').to_json(orient = "records"))

    for index, row in requestdf.iterrows():
        guid = row['GUID']
        record = records[index % len(requestdf.index)]

        request = boundary + """
Content-Type: application/http
Content-Transfer-Encoding: binary

PATCH """ + request_uri + "(" + guid + ")" + """ HTTP/1.1
Content-Type: application/json
If-Match: *

"""

        body = body + request + json.dumps(record)

    body = (body + "\n" + boundary + "--").encode()

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
    resultdf.loc[first:last,'batch'] = boundary

    resultdf.loc[first:last].to_csv(f"output\{boundary}.csv")

    successes =  sum(1 for i in codes if i == "204 No Content")
    sent = len(requestdf.index)

    print(f"Records {first} : {last} sent for import. {sent - successes} failures.")

    first = last + 1
    last = min(last + BatchSize,len(df.index))

print(f'IMPORTING TOOK: {round(time.perf_counter() - timeStart,0)} SECONDS ')
resultdf.to_csv("output\changes.csv")
