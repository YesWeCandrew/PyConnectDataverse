# PyConnectDataverse

This Python program enables easy connection to the [oData Web API](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview) for Dynamics, Power Apps and Dataverse.

In addition, example functions have been prepared that enable users to:
- Bind two records in an Many-to-Many relationship in Dataverse. This can streamline and automate the process of linking relationships, which is time-consuming when done manually.
- Download data from Dataverse in JSON format
- Add new options to an existing option set

Many more functions are possible. Anything that can be done with the Dataverse Web API can be done in Python here. Use any of pcd python files as a template to get an authenticated session with the API and then make requests over HTTPs as needed. Basic operations can be found [here](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/web-api-basic-operations-sample).

An Azure Application with access to Dynamics is required to authorise the app. Authorisation details are stored in a env.json file an example is saved in example-env.json.

A blog explaining the program will be available on my website shortly. In the meantime, I recommend the following sources, which I used to create the program:

https://www.c-sharpcorner.com/article/generate-access-token-for-dynamics-365-single-tenant-server-to-server-authentica/

https://community.dynamics.com/blogs/post/?postid=587e704d-7272-4507-8a89-b4dd538e831c

https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/dev/sample/interactive_sample.py

https://emilycheyne.medium.com/using-msal-to-connect-to-microsofts-common-data-service-fc6e2ce9d0a1