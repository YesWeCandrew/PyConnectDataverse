# M2N Relationship Dataverse Import

This Python program enables the quick binding of two records in an Many-to-Many relationship in Dataverse. This can streamline and automate the process of linking relationships, which is time-consuming when done manually.

The program requires a CSV files with the GUID of the two records to be linked. An Azure Application with access to Dynamics is required to authorise the app. Authorisation details are stored in a .env file.

A blog explaining the program will be available on my website shortly. In the meantime, I recommend the following sources, which I used to create the program:

https://www.c-sharpcorner.com/article/generate-access-token-for-dynamics-365-single-tenant-server-to-server-authentica/

https://community.dynamics.com/blogs/post/?postid=587e704d-7272-4507-8a89-b4dd538e831c