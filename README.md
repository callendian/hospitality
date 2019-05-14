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


## UserReview
### '/userreview'
#### GET:
The GET end point will return the review for the current user that is logged in. This review will include information such as the visitor's name, the title of the review, the description of the review and the star rating. This review would be written by the guide after the end of a tour for the visitors. This data would be returned in a JSON format.

Possible Errors:
1) 401, Unauthorized access: The user is not logged in, or if the logged in user is not a visitor. 


#####POST:
The post endpoint will take in JSON data and parse it and use it to create a new user review. The required information is visitorName and content, the optional paramenters are title and star rating. When guides write a review about the user, they will use this method. 

Possible Errors:
1. 400, Bad request when content or description is not included in the JSON parameters
2. 401, When the users is not logged in or if they are not a guide then they shouldn't be able to write a review

Example Interaction:
Input:
{
	"visitorName": "csofian", 
	"content": "he is da best"
}

Output: 
{
    "title": null,
    "createdAt": "2019-05-13T21:40:56.990",
    "stars": "",
    "content": "he is da best",
    "visitor": {
        "username": "csofian",
        "last_name": "",
        "email": "cns24@uw.edu",
        "first_name": ""
    },
    "editedAt": "2019-05-14T04:41:08.286Z"
}

####PATCH:
The patch endpoint will allow the existing guide to edit the review they wrote of a particular user. It will modify the existing records for the userreview table. 

Possible Errors:
1). 401 - when the user is not logged in or the user is not a guide
2). 400 - If required parameters (visitorName) is not included in the input.

Example Interaction:
Input:
{
	"visitorName": "csofian", 
	"content": "he is not da best",
	"stars": "5",
	"title": "Chris is the best"
}
Output:
{
    "title": "Chris is the best",
    "createdAt": "2019-05-13T21:40:56.990Z",
    "stars": "5",
    "content": "he is not da best",
    "visitor": {
        "username": "csofian",
        "last_name": "",
        "email": "cns24@uw.edu",
        "first_name": ""
    },
    "editedAt": "2019-05-14T04:41:43.501Z"
}

###DELETE:
The delete method will allow the existing guide to delete their review of a particular users. It will take in a dispute id and it will delete that particular dispute. The only person that can delete this dispute is the user that file the dispute or the guide in the dispute.

Possible Errors:
1). 400 - If the required parameters (visitorName) is not included in the input.

Example Interaction:
Input:
{
	"visitorName": "csofian"
}

Output:
The given reviews is deleted.


## Disputes
### '/disputes/<int:disputeID>'
#### GET:
The GET end point will return the dispute that whose ID is included in the path parameter. The dispute will include information such as the visitors implicated, the guide, and the description of the dispute. This method will be the page where the detailed information about a particular dispute. 

Possible Errors:
1) 400, if the dispute with the given id doesn't exist
1) 401, Unauthorized access: The user is not logged in, or if the logged in user is not the implicated visitor or guide. 



## Disputes
### '/disputes/'
#####POST:
This POST end point will create a dispute that will take in the visitor username and the guide username. It will also take in the description of the dispute between the two people. It will return a JSON form of the dispute that is being added to the database. This will be the main way the guide and the users file a complain about the other party. 
Possible Errors:
1. 400, Bad request when the required parameters is not included in the JSON parameters or when the guide or visitors with the given parameters can't be found
2. 401, When the users is not logged in or if they are not a guide then they shouldn't be able to write a review

Example Interaction:
Input:
{
	"visitorName": "csofian", 
	"content": "he is da best"
}

Output: 
{
    "editedAt": "2019-05-14T05:27:20.067Z",
    "createdAt": "2019-05-13T22:26:10.127",
    "visitor": {
        "last_name": "",
        "first_name": "",
        "email": "cns24@uw.edu",
        "username": "csofian"
    },
    "guide": {
        "last_name": "wei",
        "first_name": "wei",
        "email": "wei",
        "username": "wei"
    },
    "description": "He is not handsome"
}


###DELETE:
The delete method will allow either the user, the guide or the admin to delete the dispute. This will serve as a dispute resolution function in our website. If it is successful, the user will get a message saying that the dispute has been resolved. 

Possible Errors:
1). 400 - if the dispute with the given doesn't exist, or if it is not included in the parameters. 
2). 401 - If the user is not the guide or the visitor implicated, or the admin. 





