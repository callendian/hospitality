from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from main.models import *
from rest_framework import status
from mysite.serializer import VisitorReview
import json
from .forms import DisputeForm, DisputeID, VisitorReviewForm, contactUSForm
from django.core import serializers
from django.core.mail import send_mail

'''Responsible for creating, editing, deleting and viewing user review. Only the visitor can view
the user review and only the guide can write the user review. '''
@csrf_exempt
def userreview(request):
    if(not request.user.is_authenticated):
            return HttpResponse("Unauthorized. Please Sign in", 
                                status=status.HTTP_401_UNAUTHORIZED)
    if(request.method == "GET"):
        form = VisitorReviewForm()
        return render(request, '../templates/main/newUserReview.html', {'form': form}, status=200)
    elif(request.method == "POST"):
        form = VisitorReviewForm(request.POST)
        if(not form.is_valid()):
            return HttpResponse("Invalid Dispute Request.", status=status.HTTP_400_BAD_REQUEST)
        try:
            curGuide = Guide.objects.get(user=request.user)
            curBooking = Booking.objects.get(id=form.cleaned_data["bookingID"])
        except:
            return HttpResponse("The booking with the given ID doesn't exist")
        if(curBooking.tour.guide != curGuide):
            return HttpResponse("You have to be a guide for this tour!", status=status.HTTP_400_BAD_REQUEST)
        newReview = VisitorReview(visitor=Visitor.objects.get(
                                                            user=curBooking.visitor.user),
                                                            content=form.cleaned_data["description"],
                                                            reviewer=curGuide,
                                                            booking=curBooking,
                                                            rating=form.cleaned_data["rating"])
        newReview.save()
        return HttpResponseRedirect("/profile")
    #Delete a dispute given a dispute ID. 
    #Returns the review of the logged in user. 
    elif(request.method == "DELETE"):
        isGuide = Guide.objects.filter(user=request.user)
        if(len(isGuide) == 0):
            return HttpResponse("You have to be a guide to write visitor review.")
        data = checkValidJSONInput(request)
        if(not "visitorName" in data.keys()):
            return HttpResponse("visitorName is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        allReviews = VisitorReview.objects.filter(visitor=Visitor.objects.get(
                                                    user=User.objects.get(
                                                            username=data["visitorName"])))
        allReviews.delete()
        return HttpResponse("The given reviews is deleted.", 
                            content_type="plain/text",
                            status=status.HTTP_200_OK)
    #Edit a previously written review. 
    elif(request.method == "PATCH"):
        if(not request.user.is_authenticated):
            return HttpResponse("Unauthorized. Please Sign in", 
                                status=status.HTTP_401_UNAUTHORIZED)
        isGuide = Guide.objects.filter(user=request.user)
        if(len(isGuide) == 0):
            return HttpResponse("You have to be a guide to write visitor review.", 
                                status=status.HTTP_401_UNAUTHORIZED)
        data = checkValidJSONInput(request)
        if(not "visitorName" in data.keys()):
            return HttpResponse("visitorName is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        allReviews = VisitorReview.objects.get(visitor=Visitor.objects.get(
                                                        user=User.objects.get(
                                                            username=data["visitorName"])))
        #Handle the optional parameters
        if("content" in data.keys()):
            allReviews.content = data["content"]
        if("rating" in data.keys()):
            allReviews.rating = data["rating"]
        allReviews.save()
        cur_dict = json.loads(serializers.serialize('json', [allReviews, ]))[0]['fields']
        cur_dict["visitor"] = formatUser(User.objects.get(id=cur_dict["visitor"]))
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)

'''Responsible for rendering a webpage that displays dispute information given a disputeID.'''
@csrf_exempt
def showDisputes(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    if(request.method == "GET"):
        disputeObj = []
        try:
            allDisputesVisitors = Dispute.objects.filter(visitor=Visitor.objects.get(user=request.user))
            allDisputeGuide = Dispute.objects.filter(guide=Guide.objects.get(user=request.user))
        except:
            return HttpResponse("Error querying disputes for this visitor",
                                status=status.HTTP_400_BAD_REQUEST)

        if allDisputesVisitors.exists():
            for dispute in allDisputesVisitors:
                cur_dict2 = json.loads(serializers.serialize('json', [dispute, ]))[0]['fields']
                cur_dict2["visitor"] = Visitor.objects.get(id=cur_dict2['visitor']).user
                cur_dict2["guide"] = Guide.objects.get(id=cur_dict2['guide']).user
                cur_dict2["bookingID"] = dispute.booking.id
                disputeObj.append(cur_dict2)   
            print(disputeObj)
        if allDisputeGuide.exists():
            for dispute in allDisputeGuide:
                cur_dict2 = json.loads(serializers.serialize('json', [dispute, ]))[0]['fields']
                cur_dict2["visitor"] = Visitor.objects.get(id=cur_dict2['visitor']).user
                cur_dict2["guide"] = Guide.objects.get(id=cur_dict2['guide']).user
                cur_dict2["bookingID"] = dispute.booking.id
                disputeObj.append(cur_dict2)   
        return render(request, 'main/disputes.html', {'disputeObj': disputeObj})

@csrf_exempt
def contact_us(request):
    if(request.method == "GET"):
        form = contactUSForm()
        return render(request, '../templates/main/contact_us.html', {'form': form}, status=200)
    elif(request.method == "POST"):
        form = contactUSForm(request.POST)
        if(not form.is_valid()):
            return HttpResponse("Invalid Form.", status=status.HTTP_400_BAD_REQUEST)
        try:
            newContactUs = ContactUs(
                name=form.cleaned_data["name"],
                description = form.cleaned_data["description"],
                email = form.cleaned_data["email"]
            )
            newContactUs.save()
        except:
            return HttpResponse("Error interacting with Database",
                 status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse("Message sent")

def about_us(request):
    if(request.method == "GET"):
        return render(request, '../templates/main/about_us.html', {}, status=200)

def homepage(request):
    if(request.method == "GET"):
        return render(request, '../templates/main/homepage.html', {}, status=200)


'''Responsible for creating and resolving a dispute between guide and visitors. Only accessible
to the visitor and the guide implicated on the dispute'''
@csrf_exempt
def disputes(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    #Create a new dispute that takes in the visitor's Username and guide's username
    if(request.method == "GET"):
        form = DisputeForm()
        form2 = DisputeID()
        return render(request, '../templates/main/newDispute.html', {'form': form, 'form2': form2}, status=200)
    elif(request.method == "POST"):
        form = DisputeForm(request.POST)
        if(not form.is_valid()):
            return HttpResponse("Invalid Dispute Request.", status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(id=form.cleaned_data["bookingID"], visitor=Visitor.objects.get(user=request.user))
            newDispute = Dispute(visitor=booking.visitor, 
                                guide=booking.tour.guide, description=form.cleaned_data["description"], booking=booking)
            newDispute.save()
        except:
            return HttpResponse("Booking id invalid. You already have a dispute, or booking id is not associated to your account",
                 status=status.HTTP_400_BAD_REQUEST)

        return HttpResponseRedirect("/allDisputes")

    #Delete a dispute given a dispute ID. 
    elif(request.method == "DELETE"):
        data = checkValidJSONInput(request)
        if("disputeID" not in data.keys()):
            return HttpResponse("Input valid disputeID", status=status.HTTP_400_BAD_REQUEST)
        try:
            curCase = Dispute.objects.get(id=data["disputeID"])
        except:
            return HttpResponse("Dispute with the given ID doesn't exist.", 
                                status=status.HTTP_400_BAD_REQUEST)
        if(curCase.guide.user != request.user 
            and curCase.visitor.user != request.user 
            and (not request.user.is_superuser)):
            return HttpResponse("You don't have permission to view this dispute", 
                                status=status.HTTP_401_UNAUTHORIZED)
        curCase.delete()
        return HttpResponse("Dispute successfully resolved", status=status.HTTP_200_OK)

'''Responsible for creating a new visitor instance in the database, editing a visitor's
instance and deleting a visitor's instance. It is also resposible for populating
a webpage with the data from the database.
'''
@csrf_exempt
def profile(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    
    # Responsible for populating a webpage with the data from the database. 
    if(request.method == "GET"):
        try:
            currentProf = Visitor.objects.get(user=request.user)
            guideBio = Guide.objects.get(user=request.user).bio
        except:
            return HttpResponse("You have to be a visitor to view visitors information.", 
                                status=status.HTTP_401_UNAUTHORIZED)
        cur_dict = json.loads(serializers.serialize('json', [currentProf, ]))[0]['fields']
        bookingObj = []
        allBooking = Booking.objects.filter(visitor=Visitor.objects.get(user=request.user))
        cur_dict = None
        print(cur_dict)
        for booking in allBooking:
            try:
                curReview = VisitorReview.objects.get(visitor=currentProf, booking=booking)
                cur_dict = json.loads(serializers.serialize('json', [curReview, ]))[0]['fields']
                cur_dict["visitor"] = formatUser(User.objects.get(id=cur_dict["visitor"]))
            except:
                pass
            curBooking = booking.tour
            print(booking.tour.city.name)
            cur_dict2 = json.loads(serializers.serialize('json', [booking, ]))[0]['fields']
            cur_dict2["Guest"] = cur_dict2["visitor"]
            cur_dict2["tourType"] = curBooking.tourType
            cur_dict2["city"] = curBooking.city.name
            cur_dict2["description"] = curBooking.description
            cur_dict2["days"] = curBooking.days
            cur_dict2["price"] = curBooking.price
            if(cur_dict != None):
                cur_dict2["guideReview"] = cur_dict['content']
                cur_dict2["guideRating"] = cur_dict["rating"]
            else:
                cur_dict2["guideReview"] = "None"
                cur_dict2["guideRating"] = "None"
            bookingObj.append(cur_dict2)
        return render(request, '../templates/main/profile.html', 
                        {
                            'visitor': currentProf, 
                            'guideBio': guideBio, 
                            'bookingObj': bookingObj
                        }, status=200)
    #Responsible for changing an instance of a visitor with the data inputted in the request
    elif(request.method == "PATCH"):
        data = checkValidJSONInput(request)
        try:
            currentProf = Visitor.objects.get(user=request.user)
        except:
            return HttpResponse("You have to be a visitor to modify visitor profile.", 
                                status=status.HTTP_401_UNAUTHORIZED)
        if("first_name" in data.keys()):
            currentProf.first_name = data["first_name"]
        if("last_name" in data.keys()):
            currentProf.first_name = data["last_name"]
        if("email" in data.keys()):
            currentProf.email = data["email"]
        if("gender" in data.keys()):
            currentProf.gender = data["gender"]
        currentProf.save()
        cur_dict = json.loads(serializers.serialize('json', [currentProf, ]))[0]['fields']
        cur_dict["user"] = formatUser(User.objects.get(id=cur_dict["user"]))
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    #Responsible for deleting a new visitor instance given a visitor ID
    elif(request.method == "DELETE"):
        data = checkValidJSONInput(request)
        if(not "visitorID" in data.keys()):
            return HttpResponse("visitorName is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        try:
            userToBeDeleted = Visitor.objects.get(id=data["visitorID"])
        except:
            return HttpResponse("Visitor with the given ID doesn't exist", 
                                content_type="plain/text", 
                                status=status.HTTP_400_BAD_REQUEST)
        if(not request.user.is_superuser and userToBeDeleted.user != request.user):
            return HttpResponse("You have to be an administrator or owner to delete a user", 
                                content_type="plain/text", 
                                status=status.HTTP_401_UNAUTHORIZED) 
        userToBeDeleted.delete()
        return HttpResponse("User Deleted", status=status.HTTP_200_OK)


#Check if the JSON input in the request is valid json. 
def checkValidJSONInput(request):
    try:
        data = json.loads(request.body.decode("utf-8"))   
    except:
        return HttpResponse("Valid JSON Input required", status=status.HTTP_400_BAD_REQUEST)
    return data

# helper function that formats user data into a dictionary
def formatUser(user):
    return ({'username' : user.username, 
            'first_name' : user.first_name,  
            'last_name' : user.last_name, 
            'email' : user.email})

def formatBooking(booking):
    return ({'tour' : booking.tour.title, 
        'visitor' : formatUser(booking.visitor),  
        'start_date' : str(booking.start_date), 
        'end_date' : str(booking.end_date)})

def convertDatetimeToString(o):
	DATE_FORMAT = "%Y-%m-%d" 
	TIME_FORMAT = "%H:%M:%S"

	if isinstance(o, datetime.date):
	    return o.strftime(DATE_FORMAT)
	elif isinstance(o, datetime.time):
	    return o.strftime(TIME_FORMAT)
	elif isinstance(o, datetime.datetime):
	    return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))








                
                
