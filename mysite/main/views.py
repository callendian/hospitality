from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import datetime
from django.db import DatabaseError
from rest_framework import status
import json
from main.models import Guide, Tours, Review, Visitors

# Create your views here.


JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
DatabaseErrorMessage = "Error interacting with database."
BadRequestMessage = "Error interacting with database."

# renders the home page with links to other parts of the webpage
@csrf_exempt
def home(request):
        if request.method == 'GET':
                return render(request, 'main/homepage.html')
        else:
                return HttpResponse('Method not allowed on /.', status=405)

# Responsible for creating new Tour Guides and allows them to update their profile when they want,
# also can return a list of all guides that exist in the DB
@csrf_exempt
def tourGuides(request):

        # returns a list of all the guides and information related to them including their
        # first and last name, username, and email
        if request.method == 'GET':
                try:
                        guides = Guide.objects.all()
                except DatabaseError: # If database throws an error
                                return HttpResponse(DatabaseErrorMessage, 
                                        status=status.HTTP_400_BAD_REQUEST)
                result = []
                for guide in guides:

                        result.append({
                                'id' : guide.id,
                                'name' : guide.name,
                                'description' : guide.description,
                                'user' : formatUser(guide.creator)
                        })
                return JsonResponse(result, safe=False)

        # creates a new guide and adds it to the database
        elif request.method == 'POST':
                if request.user.is_authenticated:
                        # retrieve input from JSON request
                        data = callDataBase(request)
                        if isinstance(data, HttpResponse):
                                return data
                        # makes sure name parameter was passed in
                        if 'name' not in data:
                                return HttpResponse('name is a requaired field', 
                                        status=status.HTTP_400_BAD_REQUEST)
                        if 'description' not in data:
                                description = ""
                        else :
                                description = data['description']
                        try:
                                newGuide = Guide(name=data['name'],
                                                description=description,
                                                createdAt=datetime.datetime.now(), 
                                                editedAt=datetime.datetime.now(),
                                                creator=request.user)
                                newGuide.save()
                        except DatabaseError: # If database throws an error
                                return HttpResponse(DatabaseErrorMessage, 
                                        status=status.HTTP_400_BAD_REQUEST)
                        
                        result = {
                                'name' : newGuide.name, 
                                'description' : newGuide.description,
                                'createdAt' : newGuide.createdAt,
                                'editedAt' : newGuide.editedAt,
                                'creator' : formatUser(newGuide.creator)
                        }
                        return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)
                else:
                        return HttpResponse('Must be logged in', status=status.HTTP_401_UNAUTHORIZED)

        # allows a guide to update information about their account
        elif request.method == 'PATCH':
                if request.user.is_authenticated:
                        guide = Guide.objects.get(creator=request.user)
                        if not guide:
                                return HttpResponse('Can only edit your own profile', 
                                        status=status.HTTP_401_UNAUTHORIZED)
                        # retrieve input from JSON request
                        data = callDataBase(request)
                        if isinstance(data, HttpResponse):
                                return data
                        # updates name value
                        if 'name' not in data:
                                name = guide.name
                        else:
                                name = data['name']
                        # updates description value
                        if 'description' not in data:
                                description = guide.description
                        else:
                                description = data['description']
                        try:
                                newGuide = Guide(id=guide.id,
                                                name=name,
                                                description=description,
                                                createdAt=guide.createdAt, 
                                                editedAt=datetime.datetime.now(),
                                                creator=request.user)
                                newGuide.save()
                        except DatabaseError: # If database throws an error
                                return HttpResponse(DatabaseErrorMessage, 
                                        status=status.HTTP_400_BAD_REQUEST)
                        result = {
                                'name' : newGuide.name,
                                'description' : newGuide.description,
                                'createdAt' : newGuide.createdAt,
                                'editedAt' : newGuide.createdAt,
                                'creator' : formatUser(newGuide.creator)
                        }
                        return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)
                        
                else:
                        return HttpResponse('Must be logged in', 
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
                return HttpResponse('Method not allowed', 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Creates a new review and allows user to update them later on if they want to change something,
# also when given a guide, displays all reviews about them
@csrf_exempt
def reviews(request, id):
        if request.user.is_authenticated:
                if request.method == 'POST':
                        # check to make sure the specified guide exists
                        guide = Guide.objects.get(id=id)
                        if not guide:
                                return HttpResponse("Guide doesn't exist", 
                                        status=status.HTTP_400_BAD_REQUESTD)
                        # retrieve input from JSON request
                        data = callDataBase(request)
                        if isinstance(data, HttpResponse):
                                return data
                        # checks to make sure each field was filled out in the JSON request
                        if 'title' not in data:
                                return HttpResponse('title is a requaired field', 
                                        status=status.HTTP_400_BAD_REQUEST)
                        if 'content' not in data:
                                return HttpResponse('content is a requaired field', 
                                        status=status.HTTP_400_BAD_REQUEST)
                        if 'stars' not in data:
                                return HttpResponse('stars is a requaired field', 
                                        status=status.HTTP_400_BAD_REQUEST)
                        try:
                                newReview = Review(creator=request.user,
                                                Guide=guide,
                                                title=data['title'],
                                                content=data['content'],
                                                stars=data['stars'],
                                                createdAt=datetime.datetime.now(),
                                                editedAt=datetime.datetime.now())
                                newReview.save()
                        except DatabaseError: # If database throws an error
                                return HttpResponse(DatabaseErrorMessage, 
                                        status=status.HTTP_400_BAD_REQUEST)
                        # format and return response
                        result = {
                                'creator' : formatUser(newReview.creator),
                                'Guide' : formatUser(guide.creator),
                                'title' : newReview.title,
                                'content' : newReview.content,
                                'stars' : newReview.stars,
                                'createdAt' : newReview.createdAt,
                                'editedAt' : newReview.editedAt
                        }
                        return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)
                elif request.method =='PATCH':
                        guide = Guide.objects.get(id=id)
                        oldReview = Review.objects.get(Guide = guide, creator=request.user)
                        if not oldReview:
                                return HttpResponse("Specified Review doesn't exist", 
                                        status=status.HTTP_400_BAD_REQUEST)
                        # retrieve input from JSON request
                        data = callDataBase(request)
                        if isinstance(data, HttpResponse):
                                return data
                        if 'title' not in data:
                                title = oldReview.title
                        else:
                                title = data['title']
                        if 'content' not in data:
                                content = oldReview.content
                        else:
                                content = data['content']
                        if 'stars' not in data:
                                stars = oldReview.stars
                        else:
                                stars = data['stars']
                        try:
                                newReview = Review(id=oldReview.id,
                                                creator=oldReview.creator,
                                                Guide=oldReview.Guide,
                                                title=title,
                                                content=content,
                                                stars=stars,
                                                createdAt=oldReview.createdAt, 
                                                editedAt=datetime.datetime.now())
                                newReview.save()
                        except DatabaseError: # If database throws an error
                                return HttpResponse(DatabaseErrorMessage, 
                                        status=status.HTTP_400_BAD_REQUEST)
                        result = {
                                'creator' : formatUser(request.user),
                                'Guide' : formatUser(guide.creator),
                                'title' : newReview.title,
                                'content' : newReview.content,
                                'stars' : newReview.stars,
                                'createdAt' : newReview.createdAt,
                                'editedAt' : newReview.createdAt,
                        }
                        return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)

                
                elif request.method == 'GET':
                        try:
                                reviews = Review.objects.filter(id=id)
                                guide = Guide.objects.get(id=id)
                        except DatabaseError: # If database throws an error
                                return HttpResponse(DatabaseErrorMessage, 
                                        status=status.HTTP_400_BAD_REQUEST)
                        result = []
                        for review in reviews:
                                result.append({
                                        'title' : review.title,
                                        'content' : review.content,
                                        'stars' : range(int(review.stars)),
                                        'user' : formatUser(review.creator),
                                        'Guide' : guide.name,
                                        'createdAt' : review.createdAt,
                                        'editedAt' : review.editedAt
                                })
                        return render(request, 'main/reviews.html', {'subject' : guide.name, 
                                'reviews': result})

                else:
                        return HttpResponse('Method not allowed', 
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
                return HttpResponse('Must be logged in', status=status.HTTP_401_UNAUTHORIZED)

# Creates new tour appointments and allows guides to delete their tours if they want. Also
# pulls up all tours that a specific guide has.
@csrf_exempt
def tours(request, id):
        if request.user.is_authenticated:
                if request.method == 'GET':
                        try:
                                guide = Guide.objects.get(creator=request.user)
                        except:
                                return HttpResponse('Must be a guide to access', 
                                        status=status.HTTP_401_UNAUTHORIZED)
                        upcomingTours = Tours.objects.filter(Guide=guide)
                        result = []
                        for tour in upcomingTours:
                                result.append({
                                        'Guest' : formatUser(tour.Guest),
                                        'Start' : tour.Start,
                                        'End' : tour.End,
                                        'notesToGuide' : tour.notesToGuide,
                                        'id' : tour.id
                                })
                        return render(request, 'main/tours.html', {'tours': result, 
                                'guide' : guide.name})
                elif request.method == 'POST':
                        # check to make sure the specified guide exists
                        try:
                                guide = Guide.objects.get(id=id)
                        except:
                                return HttpResponse("Guide doesn't exist", 
                                        status=status.HTTP_400_BAD_REQUEST)
                        try:
                                print(request.user)
                                guest = Visitors.objects.get(user=request.user)
                                print(guest)
                        except:
                                return HttpResponse("Visitor doesn't exist", 
                                        status=status.HTTP_400_BAD_REQUEST)     
                        # retrieve input from JSON request
                        data = callDataBase(request)
                        print(data)
                        if isinstance(data, HttpResponse):
                                return data
                        # checks to make sure each field was filled out in the JSON request
                        if 'Start' not in data:
                                return HttpResponse('Start is a requaired field', 
                                        status=status.HTTP_400_BAD_REQUEST)
                        if 'End' not in data:
                                return HttpResponse('End is a requaired field', 
                                        status=status.HTTP_400_BAD_REQUEST)
                        if 'notesToGuide' not in data:
                                notesToGuide = ""
                        else:
                                notesToGuide = data['notesToGuide']
                        try:
                                newTour = Tours(Guest=guest,
                                                Guide=guide,
                                                Start=datetime.datetime.strptime(data['Start'], 
                                                        "%Y-%m-%d %H:%M"),
                                                End=datetime.datetime.strptime(data['End'], 
                                                        "%Y-%m-%d %H:%M"),
                                                createdAt=datetime.datetime.now(),
                                                editedAt=datetime.datetime.now(),
                                                notesToGuide=notesToGuide)
                                newTour.save()
                        except DatabaseError: # If database throws an error
                                return HttpResponse(DatabaseErrorMessage, 
                                        status=status.HTTP_400_BAD_REQUEST)
                        result = {
                                'creator/visitor' : formatUser(request.user),
                                'Guide' : guide.name,
                                'Start' : newTour.Start,
                                'End' : newTour.End,
                                'createdAt' : newTour.createdAt,
                                'editedAt' : newTour.editedAt,
                                'notesToGuide' : newTour.notesToGuide,
                        }
                        return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)
                elif(request.method == "DELETE"):
                        try:
                                guide = Guide.objects.get(creator=request.user)
                        except:
                                return HttpResponse("Must be Guide of Tour to delete", 
                                        status=status.HTTP_401_UNAUTHORIZED)
                        # retrieve input from JSON request
                        data = callDataBase(request)
                        if isinstance(data, HttpResponse):
                                return data
                        if 'id' not in data:
                                return HttpResponse('id is a requaired field', 
                                        status=status.HTTP_400_BAD_REQUEST)
                        tour = Tours.objects.get(id=data['id'])
                        tour.delete()
                        return HttpResponse("Tour Deleted", content_type="plain/text", 
                                status=status.HTTP_200_OK)
                else:
                        return HttpResponse('Method not allowed', 
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
                return HttpResponse('Must be logged in', status=status.HTTP_401_UNAUTHORIZED)

# helper function that formats user data into a dictionary
def formatUser(user):
    return ({'username' : user.username, 
            'first_name' : user.first_name,  
            'last_name' : user.last_name, 
            'email' : user.email})

# calls Database and either returns data passed in by user or an error that occured
def callDataBase(request):
    try: # Decode post body into JSON
         data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError: # If JSON failed to decode
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception: # Any other exception
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)
    return data    
