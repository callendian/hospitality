# hospitality

## Guides
### '/guides'
#### GET:
The GET endpoint will return a list of all guides in the app along with the information associated with them including their name, description, and other user information like their email and username. This would be used by a search feature on the site to return relavent guides back to the user who might be interested in getting a tour from them.

Possible Errors:
1) 404, problems interacting with the database when querying it.

#####POST:
The Post endpoint will take in JSON data and use it to create a new Guide in the Guide table. It takes two parameters name (required) and description (optional). People who want to become guides will use this endpoint to add themselves to the guide DB.

Possible Errors:
1) 400, Bad request since a required parameter was not included in the JSON data passsed in
2) 404, problems interacting with the database when trying to add a new Guide
3) 401, Unauthorized, i.e. you must be logged in as a standard user before you can sign up to be a guide
4) 400, Error decoding JSON body, or another issue connecting with database

Example Interaction:
Input:
{
	"name" : "Mr. Callender",
	"description" : "I live in Seattle. I have a car. I know the Ballard area well."
}

Output:
{
    "name": "Mr. Callender",
    "description": "I live in Seattle. I have a car. I know the Ballard area well.",
    "createdAt": "2019-05-12T08:02:07.280",
    "editedAt": "2019-05-12T08:02:07.280",
    "creator": {
        "username": "callendian",
        "first_name": "Ian",
        "last_name": "Callender",
        "email": "callendian@gmail.com"
    }
}

####PATCH:
The Patch endpoint will allow existing guides to edit the name they go by or the description of themselves. So it will modify existing records in the Guide Table.

Possible Errors:
1) 405, If this endpoint was requested a method other than GET, POST, or PATCH this error will be thrown
2) 404, problems interacting with the database when trying to update an existing Guide
3) 401, Unauthorized, i.e. you must be logged in as a standard user before you can sign up to be a guide and you must also be the creator of the profile to edit it
4) 400, Error decoding JSON body, or another issue connecting with database

Example Interaction:
Input:
{
	"name" : "Mr. Callender",
	"description" : "I live in Seattle. I have a car. I know the Fremont area well."
}

Output:
{
    "name": "Mr. Callender",
    "description": "I live in Seattle. I have a car. I know the Fremont area well.",
    "createdAt": "2019-05-11T08:51:49.685Z",
    "editedAt": "2019-05-11T08:51:49.685Z",
    "creator": {
        "username": "callendian",
        "first_name": "Ian",
        "last_name": "Callender",
        "email": "callendian@gmail.com"
    }
}

## Reviews
### '/reviews/<int>'
#### GET:
When given a specific Guide through an int parameter in the URL, this will pull up and display all reviews about them. This is for users that want to see reviews on guides before they book tours with them. The only interaction with the database that it will have is to query it for the reviews.

Possible Errors:
1) 404, problems interacting with the database when querying it.

#####POST:
When given JSON data, this endpoint will post new reviews about the specified guide. This is for users who want to write reviews about guides. One restriction is that a user is only allowed to write a review once for an individual guide. The user must enter a title, text content, and a star rating for this endpoint to work. The only change to the Datebase that will occur is that new records to the Reviews table will be added.

Possible Errors:
1) 400, Bad request since a required parameter was not included in the JSON data passsed in
2) 404, problems interacting with the database when trying to add a new Guide
3) 401, Unauthorized, i.e. you must be logged in in order to write a review
4) 400, Error decoding JSON body, or another issue connecting with database

Example Interaction:
Input:
{
	"title" : "horrible experience",
	"stars" : "2",
	"content" : "Would not do again."
}

Output:
{
    "creator": {
        "username": "chacha",
        "first_name": "char",
        "last_name": "callender",
        "email": "cha@uw.edu"
    },
    "Guide": {
        "username": "callendian",
        "first_name": "Ian",
        "last_name": "Callender",
        "email": "callendian@gmail.com"
    },
    "title": "great experience",
    "content": "Would do again.",
    "stars": "5",
    "createdAt": "2019-05-12T09:13:48.847",
    "editedAt": "2019-05-12T09:13:48.847"
}


####PATCH
This endpoint is in charge of editing existing reviews. It is intended for users to be able to change their old reviews if they have a change of heart or different experience. The effect that it will have on the database is that it can edit existing reviews.

Possible Errors:
1) 405, If this endpoint was requested a method other than GET, POST, or PATCH this error will be thrown
2) 404, problems interacting with the database when trying to update an existing Guide
3) 401, Unauthorized, i.e. you must be logged in to edit your old reviews
4) 400, Error decoding JSON body, or another issue connecting with database

Example Interaction:
Input:
{
	"title" : "horrible experience",
	"content" : "Would not do again."
}

Output:
{
    "creator": {
        "username": "chacha",
        "first_name": "char",
        "last_name": "callender",
        "email": "cha@uw.edu"
    },
    "Guide": {
        "username": "callendian",
        "first_name": "Ian",
        "last_name": "Callender",
        "email": "callendian@gmail.com"
    },
    "title": "great experience",
    "content": "Would do again.",
    "stars": "4",
    "createdAt": "2019-05-12T09:13:48.847Z",
    "editedAt": "2019-05-12T09:13:48.847Z"
}

## Tours
### '/tours/<int>'
#### GET:
This endpoint will display all the tours for the specified Guide. It is intended for Guides to be able to see what tours they have. The only interaction it has with the database is to query it to get a set of all their tours.

Possible Errors:
1) 401, Unauthorized, i.e. you must be a guide who is signed in in order to see your tours

#### Post:
This endpoint is for adding new tours between a guide and a user. The data is passed in as a JSON body and the 2 required parameters are a start and end time however it also accepts a parameter containing notes that a user has for the guide. Theres also is a parameter in the url, an int representing the id of the guide who will lead the tour. Once it has this information, it can create a new record in the Tours table.

Possible Errors:
1) 400, Bad request since a required parameter was not included in the JSON data passsed in
2) 404, problems interacting with the database when trying to add a new Guide
3) 401, Unauthorized, i.e. you must be logged in before you can add a new tour
4) 400, Error decoding JSON body, or another issue connecting with database

Example Interaction:
Input:
{
	"Start" : "2011-10-01 16:26",
	"End" : "2011-10-01 16:50",
	"notesToGuide" : "I am allergic to nutts."
}

Output:
{
    "creator": {
        "username": "chacha",
        "first_name": "char",
        "last_name": "callender",
        "email": "cha@uw.edu"
    },
    "Guide": "Mr. Callender",
    "Start": "2011-10-01T16:26:00",
    "End": "2011-10-01T16:50:00",
    "createdAt": "2019-05-12T09:23:46.667",
    "editedAt": "2019-05-12T09:23:46.667",
    "notesToGuide": "I am allergic to nutts."
}

#### DELETE:
The last endpoint allows a logged in guide to delete one of their own tours. This give guides the power to control which tours they want. The 2 parameters that this method takes is the id of the guide stored in the url and the id of the tour that the guide wants to delete stored in the JSON body. This endpoint will interact with the database by deleting a record from the tours table.

Possible Errors:
1) 405, If this endpoint was requested a method other than GET, POST, or PATCH this error will be thrown
2) 400, Bad request since a required parameter was not included in the JSON data passsed in
3) 401, Unauthorized, i.e. you must be logged in to edit your old reviews

Example Interaction:
Input:
{
    "id" : "2"
}

output:
"Tour Deleted"

