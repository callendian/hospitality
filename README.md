# hospitality
## Search
### '/search/'
#### GET:
This endpoint will display a form through which visitors can look for tours/guides.

Possible Errors:
1) 401, Unauthorized, i.e. you must be a user who is signed in in order to look for tours

#### Post:
This endpoint will process the search form filled in by the users and return in HTML the 
formatted search results.

Possible Errors:
1) 401, Unauthorized, i.e. you must be a user who is signed in in order to look for tours

Example Interaction: 
Input:
{
    "tourType": "General",
    "city": "Seattle",
    "min_days": "2",
    "max_days": "4",
}

Output: HTML, only results section shown for example

<h2>Results</h2>
<ul>
    <li style="background-color:lightblue">
        <p>
            <strong>Guide</strong>: Vincent Widjaya, M,
            vwidjaya@uw.edu
            <br><strong>Description</strong>: Testing
            <br><strong>Duration</strong>: 3 days
            <br><strong>Price</strong>: $100.00
        </p>
        <form action="/saved/" method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="xZ68yfcSxFiLlnSB9Atoc5YI5ttemWpKS6hF86W3GXLPCZkLrz3iHj2fOCaZstv5">
            <input type="hidden" name="tour_id" value="1">
            <input type="submit" value="Save">
        </form>
        <br>
        <form action="/tour/1" method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="xZ68yfcSxFiLlnSB9Atoc5YI5ttemWpKS6hF86W3GXLPCZkLrz3iHj2fOCaZstv5">
            <input type="submit" value="Book This Guide">
        </form>
    </li>
    
</ul>

## Saved
### '/saved/'
#### GET:
This endpoint will display the list of the user's saved tours.

Possible Errors:
1) 401, Unauthorized, i.e. you must be a user who is signed in in order to have saved tours

#### Post:
This endpoint will save a tour and refresh the list of saved tours through an HTML response.
This is normally accessed through a Saved button from something like the search page.

Possible Errors:
1) 401, Unauthorized, i.e. you must be a user who is signed in in order to have saved tours
2) 400, Bad Request, error saving database for some reason (invalid params)

Example Interaction: 
Input:
{
    "tour_id_": 1
}

Output: HTML, only saved section shown for example

<h1>Saved</h1>
<ul>
    <li style="background-color:lightblue">
        <p>
            <strong>Guide</strong>: Vincent Widjaya, 
            M, vwidjaya@uw.edu
            <br><strong>City</strong>: Seattle
            <br><strong>Description</strong>: Testing
            <br><strong>Duration</strong>: 3 days
            <br><strong>Price</strong>: $100.00
        </p>
        <form action="/saved/" method="get">
            <!-- supposed to be delete but tbd in future, instead delete through api endpoint -->
            <input type="hidden" name="savedtour_id" value="6">
            <input type="submit" value="Unsave">
        </form>
        <br>
        <form action="/tour/1" method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="Z4mHxzGCZ2khTbugoAH17WJHLUhUG0sMkbxe7qqN8kNlaNWqGzhVCaNeu3YFMxy7">
            <input type="submit" value="Book This Tour">
        </form>
    </li>
</ul>


#### DELETE:
The last endpoint removes a tour from the list of saved ones. 

Possible Errors:
1) 401, Unauthorized, i.e. you must be a user who is signed in in order to have saved tours
2) 403, Forbidden, user is not the visitor that saved the specified tour

Example Interaction:
Input:
{
<<<<<<< HEAD
    "visitorID": 3
}

Output:
User Deleted

##AUTH

###'auth/signin'

#### GET:
Returns a form with two fields, a username and password field

#### POST:
Attempts to sign the user in using parameters passed in

Possible Errors:
1) 400, returns if the form wasn't valid
2) 401, return if the login information was inncorrect

###'auth/register'

#### GET:
Returns a form with 6 fields: username, password, password confirmation, email, first name, and last name

#### POST:
Attemps to register the new user using the parameters passed in

Possible Error:
1) 400, returns if form wasn't valid, ex. password and password confirmation didn't match

###'auth/signout'

#### GET:
Attemps to sign the user out

##Visitor
###'/guide/'
#### GET

## Home
### /home/
Checks if the user is signed in if not redirects to the login page, if is, redirects to the search page

##Profile
###'/profile'

####GET
Querys the database to return information about the current user including their username, sex, guide biography,
and their current bookings.

Possible Errors:
1) 401, must be signed in as a user

####PATCH
Allows a user to edit information abou their profile including their first name, last name, email, and gender,
and their current bookings

####DELETE
When given a visitor ID, deletes the visitor from the Database
Possible Errors:
1) 401, must be an adminitrator to delete a vistor
2) 400, visitor with given visitor ID doesn't exist

##User Reviews
###'/userreview'

####GET
Returns a form with the fields: Booking ID, Description, and a rating

Possible Errors:
1) 401, must be signed in as a user

####POST
Takes the inforrmation from the form and creates a new userreview object and adds it to the database

Possible Errors:
1) 401, must be signed in as a user
2) 400, if the form is invalid or if the user isn't the guide of the tour

####PATCH
Allows a guide to update their userreview
Possible Errors:
1) 401, must be signed in as a user
2) 400, must fill at the username parameter o

####DELETE
The delete method will allow the existing guide to delete their review of a particular users. It will take in a dispute id and it will delete that particular dispute. The only person that can delete this dispute is the user that file the dispute or the guide in the dispute.

Possible Errors:
1). 400 - If the required parameters (visitorName) is not included in the input.

##Guides
###'/guide/'

####GET
This endpoint allows guides to find information about their account like their username, etc. It also allows them to see
all their booking requests from users and the bookings that they have already approved.

Possible Errors:
1) 401, must be signed in as a user
2) 400, error connecting with the database

####POST
Allows a guide to update their bio

Possible Errors:
1) 401, must be signed in as a user

## Disputes:
### '/disputes/<int:disputeID>':
#### GET:
This end point will return a form for the user to fill out with fields including booking ID and description

Possible Errors:
1) 400, if the dispute with the given id doesn't exist
1) 401, Unauthorized access: The user is not logged in, or if the logged in user is not the implicated visitor or guide. 

#### POST:
This POST end point will create a dispute with the paramenters passed in the form. This will be the main way the guide and the users file a complain about the other party. 
Possible Errors:
1. 400, Bad request when the required parameters is not included in the form or when the guide or visitors with the given parameters can't be found
2. 401, When the users is not logged in or if they are not a guide then they shouldn't be able to write a review

### DELETE:
The delete method will allow either the user, the guide or the admin to delete the dispute. This will serve as a dispute resolution function in our website. If it is successful, the user will get a message saying that the dispute has been resolved. 

Possible Errors:
1). 400 - if the dispute with the given doesn't exist, or if it is not included in the parameters. 
2). 401 - If the user is not the guide or the visitor implicated, or the admin. 

### '/allDisputes'
#### GET:
Shows all the disputes that the current user is involed in
1. 400, Error interacting with the database
2. 401, When the users is not logged in or if they are not a guide then they shouldn't be able to write a review