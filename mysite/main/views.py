from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import DatabaseError
from rest_framework import status
import datetime
import json
from urllib.parse import parse_qs
from main.models import *
from .forms import *

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
DatabaseErrorMessage = "Error interacting with database."
BadRequestMessage = "Error interacting with database."

# renders the home page with links to other parts of the webpage
@csrf_exempt
def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/search')
        else:
            return render(request, 'main/homepage.html')
    else:
        return HttpResponse('Method not allowed on /.', status=405)


@csrf_exempt
def visitor(request):
    return HttpResponse('visitor page.')


# Creates a new review and allows user to update them later on if they want to change something,
# also when given a guide, displays all reviews about them
@csrf_exempt
def guide_reviews(request, id):
    if request.user.is_authenticated:
        # check to make sure the specified guide exists
        guide = Guide.objects.get(id=id)
        if not guide:
            return HttpResponse(
                "Guide doesn't exist", 
                status=status.HTTP_400_BAD_REQUESTD
            )

        if request.method == 'POST':
            # retrieve input from JSON request
            data = callDataBase(request)
            if isinstance(data, HttpResponse):
                return data
            # checks to make sure each field was filled out in the JSON request
            if 'content' not in data:
                return HttpResponse('content is a requaired field', 
                    status=status.HTTP_400_BAD_REQUEST)
            if 'stars' not in data:
                return HttpResponse('stars is a requaired field', 
                    status=status.HTTP_400_BAD_REQUEST)
            if 'booking' not in data:
                return HttpResponse('booking is a requaired field',
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                review = Review(
                    reviewer=Visitor.objects.get(user=request.user),
                    guide=guide,
                    booking=data['booking'],
                    content=data['content'],
                    stars=data['stars']
                )
                review.save()
            except DatabaseError: # If database throws an error
                return HttpResponse(DatabaseErrorMessage, 
                    status=status.HTTP_400_BAD_REQUEST)

            # format and return response
            result = {
                'id' : review.id, 
                'reviewer' : formatRole(request.reviewer), 
                'guide' : formatRole(review.guide), 
                'booking_id' : review.booking.id, 
                'content' : review.content,
                'rating' : review.stars,
                'createdAt' : review.createdAt,
                'editedAt' : review.createdAt,
            }
            return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)
        
        elif request.method =='PATCH':
            review = TourReview.objects.select_related('reviewer__user').get(
                guide=guide, 
                reviewer__user=request.user
            )

            if not review:
                return HttpResponse("Specified Review doesn't exist", 
                    status=status.HTTP_400_BAD_REQUEST)

            # retrieve input from JSON request
            data = callDataBase(request)
            if isinstance(data, HttpResponse):
                return data

            review.content = data['content'] if 'content' in data else review.content
            review.stars = data['stars'] if 'stars' in data else review.stars

            try:
                review.save()
            except DatabaseError: # If database throws an error
                return HttpResponse(DatabaseErrorMessage, 
                    status=status.HTTP_400_BAD_REQUEST)

            result = {
                'id' : review.id, 
                'guide' : formatRole(review.guide), 
                'booking_id' : review.booking.id, 
                'content' : review.content,
                'rating' : review.stars,
                'createdAt' : review.createdAt,
                'editedAt' : review.createdAt,
            }
            return JsonResponse(result, safe=False, status=status.HTTP_201_CREATED)

        elif request.method == 'GET':
            try:
                reviews = TourReview.object\
                    .select_related('reviewer')\
                    .select_related('guide')\
                    .select_related('booking__tour')\
                    .filter(guide__id=id)
            except DatabaseError: # If database throws an error
                return HttpResponse(DatabaseErrorMessage, 
                    status=status.HTTP_400_BAD_REQUEST)

            result = []

            for review in reviews:
                result.append({
                    'reviewer': formatRole(review.reviewer),
                    'tour': {
                        'id': review.booking.tour.id, 
                        'desc': review.booking.tour.description
                    }, 
                    'content': review.content, 
                    'rating': int(review.rating), 
                    'createdAt': review.createdAt, 
                    'editedAt': review.editedAt 
                })

            return render(request, 'main/reviews.html', {'subject' : guide, 
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
    if not request.user.is_authenticated:
        return HttpResponse('Must be logged in', status=status.HTTP_401_UNAUTHORIZED)

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


@csrf_exempt
def search(request):
    if not request.user or not request.user.is_authenticated:
        return HttpResponse("Unauthorized.", status=401)

    if request.method == "GET":
        # GET: form for searching trips
        form = TourSearchForm()
        return render(request, "main/search.html", {"form": form})

    elif request.method == "POST":
        # POST: search trips with given form data
        data = parseForm(request)

        tourType = data["tourType"][0]
        city = data["city"][0]
        min_days = int(data["min_days"][0])
        max_days = int(data["max_days"][0])

        search_results = Tour.objects.select_related('guide')\
            .filter(
                tourType__name=tourType, 
                city__name=city, 
                days__gte=min_days, 
                days__lte=max_days
            ).values(
                'id', 'description', 
                'days', 'price', 
                'guide__first_name', 
                'guide__last_name', 
                'guide__email', 
                'guide__gender'
            )

        visitor = Visitor.objects.get(user=request.user)
        saved = getSavedToursForVisitor(visitor=visitor)
        saved = map(lambda x: x['tour_id'], saved)

        return render(
            request, 
            "main/search.html", 
            {
                "form": TourSearchForm(), 
                "search_results": list(search_results), 
                "saved": list(saved)
            }
        )

    else:
        return HttpResponse("Method not allowed on this route", status=405)


@csrf_exempt
def saved(request):
    if not request.user or not request.user.is_authenticated:
        return HttpResponse("Unauthorized.", status=401)
   
    visitor = Visitor.objects.get(user=request.user)

    if request.method == "GET":
        # GET: form for searching trips
        saved = getSavedToursForVisitor(visitor)
        return render(request, "main/saved.html", {"saved": list(saved)})

    elif request.method == "POST":
        # POST: search trips with given form data
        data = parseForm(request)
        
        tour_id = int(data["tour_id"][0])
        tour = Tour.objects.get(pk=tour_id)
        savedTour = SavedTour.objects.filter(visitor=visitor, tour=tour)

        if savedTour.exists():
            savedTour.delete()
        else:
            savedTour = SavedTour(
                visitor=visitor, 
                tour=tour
            )

            try:
                savedTour.save()
            except:
                return HttpResponse("Error saving tour.", status=400)
        
        saved = getSavedToursForVisitor(visitor)
        return render(request, "main/saved.html", {"saved": list(saved)})
   
    elif request.method == "DELETE":
        # DELETE: remove from bookmarked tours
        data = callDataBase(request)
        savedTour_id = data["savedtour_id"]

        try:
            savedTour = SavedTour.objects.select_related('visitor').get(pk=savedTour_id)
            if savedTour.visitor != visitor:
                return HttpResponse("Forbidden.", status=403)
            else:
                savedTour.delete()
      
        except:
            saved = getSavedToursForVisitor(visitor)
            return render(request, "main/saved.html", {"saved": list(saved)})

    else:
        return HttpResponse("Method not allowed on this route", status=405)


@csrf_exempt
def request_tour(request, t_id):
    if not request.user or not request.user.is_authenticated:
        return HttpResponse("Unauthorized.", status=401)
    
    try:
        visitor = Visitor.objects.get(user=request.user)
        tour = Tour.objects.get(pk=t_id)
    except:
        return HttpResponse('Invalid request.', status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        form = TourRequestForm()
        return render(request, "main/request_tour.html", { "form": form, "t_id": t_id })

    elif request.method == 'POST':
        data = parseForm(request)

        start_date = '-'.join(
            [data['start_date_month'][0],
            data['start_date_day'][0], 
            data['start_date_year'][0]])

        end_date = '-'.join(
            [data['end_date_month'][0],
            data['end_date_day'][0], 
            data['end_date_year'][0]])
        
        tourRequest = TourRequest(
            visitor=visitor, 
            tour=tour, 
            start_date=datetime.datetime.strptime(start_date, "%m-%d-%Y").date(),
            end_date=datetime.datetime.strptime(end_date, "%m-%d-%Y").date()
        )

        try:
            tourRequest.save()
        except:
            return HttpResponse('Failed to request tour.', status=status.HTTP_400_BAD_REQUEST)
        
        return HttpResponseRedirect('/visitor')

    else:
        return HttpResponse("Method not allowed on this route", status=405)


@csrf_exempt
def requested(request):
    if not request.user or not request.user.is_authenticated:
        return HttpResponse("Unauthorized.", status=401)

    elif request.method == "POST":
        # POST: accepts or declines a request and updates db accordingly
        guide = Guide.objects.get(user=request.user)
        data = parseForm(request)

        req_pk = int(data["request_id"][0])
        decision = int(data["decision"][0])

        req = TourRequest.objects.get(pk=req_pk)

        if decision:
            booking = Booking(
                tour=req.tour, 
                visitor=req.visitor, 
                start_date=req.start_date, 
                end_date=req.end_date
            )
        
        req.delete()

        try:
            savedTour.save()
        except:
            return HttpResponse("Error saving tour.", status=400)

        return HttpResponseRedirect('/guide')

    else:
        return HttpResponse("Method not allowed on this route", status=405)


@csrf_exempt
def guide(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized. Please Sign in.", status=status.HTTP_401_UNAUTHORIZED)

    try:
        guide = Guide.objects.get(user=request.user)
    except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        reqs = getToursRequestedFromGuide(guide)
        bookings = Booking.objects.select_related(
            'visitor').select_related('tour').filter(tour__guide=guide)

        jobs = []
        for b in bookings:
            review = VisitorReview.objects.filter(booking=b, reviewer=guide)

            jobs.append({
                'booking_id': b.id,
                'tour_id': b.tour_id,
                'tour_title': b.tour.title,
                'tour_desc': b.tour_description,
                'tour_price': b.tour_price,
                'visitor_name': b.visitor.first_name + ' ' + b.visitor.last_name,
                'start_date': b.start_date,
                'end_date': b.end_date,
                'date_booked': b.createdAt,
                'review': review
            })

        return render(request, 'main/profile_guide.html', {
            'guide': guide,
            'reqs': reqs,
            'jobs': jobs
        })

    # allows a guide to update bio
    elif request.method == 'POST':
        data = parseForm(request)
        guide.bio = data['bio'][0]
        guide.save()

        return HttpResponseRedirect('/guide')

    else:
        return HttpResponse('Method not allowed',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


######################
## HELPER FUNCTIONS ##
######################

# helper function that formats user data into a dictionary
def formatUser(user):
    return ({'username': user.username,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'email': user.email})


def formatRole(user):
    return ({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'gender': user.gender
    })

# calls Database and either returns data passed in by user or an error that occured
def callDataBase(request):
    try:  # Decode post body into JSON
        data = json.loads(request.body.decode("utf-8"))
        return data
    except json.JSONDecodeError:  # If JSON failed to decode
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception:  # Any other exception
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)


def parseForm(request):
    try:
        data = parse_qs(request.body.decode("utf-8"))
        return data
    except:
        return HttpResponse('Failed to parse request', status=status.HTTP_400_BAD_REQUEST)

def getSavedToursForVisitor(visitor):
    saved = SavedTour.objects.select_related('tour__city').select_related('tour__guide').filter(visitor=visitor).values(
        'id',
        'tour_id', 
        'tour__city__name',
        'tour__description',
        'tour__days',
        'tour__price',
        'tour__guide__first_name',
        'tour__guide__last_name',
        'tour__guide__email',
        'tour__guide__gender'
    )
    return saved

def getToursRequestedFromGuide(guide):
    reqs = TourRequest.objects.select_related('tour__city').select_related('visitor').filter(tour__guide=guide).values(
        'id', 
        'tour_id', 
        'tour__title', 
        'tour__city__name', 
        'tour__price', 
        'visitor_id', 
        'visitor__first_name', 
        'visitor__last_name', 
        'start_date', 
        'end_date', 
        'last_modified', 
    )
    return reqs
