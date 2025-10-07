# pip install pandas # if needed

import pandas as pd
from utils.session_manager import SessionManager
from utils.dynamics_config import get_config

# Parameters
PathToDotEnv = "env.example"
PathToOptionSetCSV = "data\OptionsToAdd.csv"
ValueOfFirstAddedOption = 201300004
OptionSetLogicalName = "OPTION SET NAME"
LanguageCode = 1033
UniqueSolutionName = "SOLUTION NAME"

# Getting authenticated Requests object.
config = get_config(PathToDotEnv)
manager = SessionManager(config)
session = manager.get_authenticated_session()

# reading the CSV
df = pd.read_csv(PathToOptionSetCSV)

successful_updates = 0
expected_updates = len(df)

request_uri = f'{config.api_base_url}/InsertOptionValue'

print("Adding...")

for index, row in df.iterrows():
    label = row["Label"]
    color = row["Color"]
    
    post_json = {
                "OptionSetName": OptionSetLogicalName,
                "Value": ValueOfFirstAddedOption,
                "Color": color,
                "Label": {
                    "@odata.type": "Microsoft.Dynamics.CRM.Label",
                    "LocalizedLabels": [
                    {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": label,
                        "LanguageCode": LanguageCode,
                        "IsManaged": 'false'
                    }
                    ],
                    "UserLocalizedLabel": {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": label,
                        "LanguageCode": LanguageCode,
                        "IsManaged": 'false'
                    }
                },
                "SolutionUniqueName": UniqueSolutionName
                }

    r = session.post(request_uri, json = post_json)

    if r.status_code != 200:
        raw = r.content.decode('utf-8')
        print(raw)
        break

    else:
        print(label)
        successful_updates += 1
        ValueOfFirstAddedOption += 1

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES')
