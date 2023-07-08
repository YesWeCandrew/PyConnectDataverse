# PyConnectDataverse

This Python program enables you to connect with the [oData Web API](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview) for Dynamics, Power Apps and Dataverse.

Detailed instructions on how to get started can be found on [andyhowes.co](https://andyhowes.co/easily-connect-to-dataverse-microsoft-dynamics-with-python/)

This program can be used for:
- Securely accessing all functions of the OData Dataverse API OData Dataverse API with an authenticated Python session.
- Downloading Dynamics 365 data using Python for efficient analysis.
- Adding many-to-many relationship data to Dataverse.
- Automating tedious manual processes such as populating option sets and choices.
- Anything you can think of using the OData API and Python!

To write your own functions, use any of pcd python files as a template to get an authenticated session with the API and then make requests over HTTPs as needed. Basic operations can be found [here](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/web-api-basic-operations-sample).

An Azure Application with access to Dynamics is required to authorise the app. Authorisation details are stored in a env.json file an example is saved in example-env.json. Find instructions on [andyhowes.co](https://andyhowes.co/easily-connect-to-dataverse-microsoft-dynamics-with-python/).

Further information can be found in these resources, which I used to develop the system.
- https://www.c-sharpcorner.com/article/generate-access-token-for-dynamics-365-single-tenant-server-to-server-authentica/
- https://community.dynamics.com/blogs/post/?postid=587e704d-7272-4507-8a89-b4dd538e831c
- https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/dev/sample/interactive_sample.py
- https://emilycheyne.medium.com/using-msal-to-connect-to-microsofts-common-data-service-fc6e2ce9d0a1
