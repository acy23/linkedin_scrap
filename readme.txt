How to get linkedin urls of the connections:
    1- Go to connections page under network tab
    2- Pick the GET request while sliding down to the screen
    3- Manipulate the request by using POSTMAN (for each request at most 2K data will return)
    4- Save response json documents
    5- Insert it using responseService.py
    6- Convert the data inside the collection to the excel file and save the same directory with the project.

How to scrap detailed info for each connection:
    Here is the api request that used to render profile page: 
    https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(memberIdentity:fetdane-azimova-52761138)&&queryId=voyagerIdentityDashProfiles.84cab0be7183be5d0b8e79cd7d5ffb7b

    1- In main.py get the data by filtering created_by property. (It is assigning while getting the user's connections linkedin urls) line 91
    2- Update header dictionary on main.py by calling the api from the linkedin UI.
    2- Run main.py