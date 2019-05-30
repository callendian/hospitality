from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from main.models import *
from rest_framework import status
from mysite.serializer import VisitorReview
import json
from django.core import serializers

'''Responsible for creating, editing, deleting and viewing user review. Only the visitor can view
the user review and only the guide can write the user review. '''
@csrf_exempt
def userreview(request):
        if(not request.user.is_authenticated):
                return HttpResponse("Unauthorized. Please Sign in", 
                                    status=status.HTTP_401_UNAUTHORIZED)
        #Returns the review of the logged in user. 
        if(request.method == "GET"):
            currentProf = Visitors.objects.get(user=request.user)
            if(currentProf == None):
                return HttpResponse("You have to be a visitor to view visitor review.", 
                                    status=status.HTTP_401_UNAUTHORIZED)
            try:
                curReview = VisitorReview.objects.get(visitor=currentProf)
            except:
                return HttpResponse("The current user has no reviews", status=status.HTTP_200_OK)
            cur_dict = json.loads(serializers.serialize('json', [curReview, ]))[0]['fields']
            cur_dict["visitor"] = formatUser(User.objects.get(id=cur_dict["visitor"]))
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, 
                                content_type="application/json", status=status.HTTP_200_OK)
        #Write a review for a particular user (for Guides)
        elif(request.method == "POST"):
            if(not request.user.is_authenticated):
                return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
            isGuide = Guide.objects.filter(user=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.", 
                                        status=status.HTTP_401_UNAUTHORIZED)
            data = checkValidJSONInput(request)
            if (not "bookingID" in data.keys()):
                return HttpResponse("Review Content is required.", content_type="text/plain",
                status=status.HTTP_400_BAD_REQUEST)
            curGuide = Guide.objects.get(user=request.user)
            curBooking = Booking.objects.get(id=data["bookingID"])
            try:
                newReview = VisitorReview(visitor=Visitors.objects.get(
                                            user=User.objects.get(username=data["visitorName"])),
                                                                  content=data["content"],
                                                                  reviewer=curGuide,
                                                                  booking=curBooking,
                                                                  rating=data["rating"])
            except:
                return HttpResponse("Enter valid json input", status=status.HTTP_400_BAD_REQUEST)
            try:
                newReview.save()
            except:
                return HttpResponse("You have already written a review for this person", 
                                    status=status.HTTP_400_BAD_REQUEST)
            cur_dict = json.loads(serializers.serialize('json', [newReview, ]))[0]['fields']
            cur_dict["visitor"] = formatUser(User.objects.get(id=cur_dict["visitor"]))
            cur_dict["reviewer"] = formatUser(curGuide.reviewer)
            cur_dict["booking"] = formatBooking(curBooking)
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
        #Delete a previously written review
        elif(request.method == "DELETE"):
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.")
            data = checkValidJSONInput(request)
            if(not "visitorName" in data.keys()):
                return HttpResponse("visitorName is required", 
                    content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
            allReviews = VisitorReview.objects.filter(visitor=Visitors.objects.get(
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
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.", 
                                    status=status.HTTP_401_UNAUTHORIZED)
            data = checkValidJSONInput(request)
            if(not "visitorName" in data.keys()):
                return HttpResponse("visitorName is required", 
                    content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
            allReviews = VisitorReview.objects.get(visitor=Visitors.objects.get(
                                                            user=User.objects.get(
                                                                username=data["visitorName"])))
            #Handle the optional parameters
            if("content" in data.keys()):
                allReviews.content = data["content"]
            if("title" in data.keys()):
                allReviews.title = data["title"]
            if("stars" in data.keys()):
                allReviews.stars = data["stars"]
            allReviews.save()
            cur_dict = json.loads(serializers.serialize('json', [allReviews, ]))[0]['fields']
            cur_dict["visitor"] = formatUser(User.objects.get(id=cur_dict["visitor"]))
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)

'''Responsible for rendering a webpage that displays dispute information given a disputeID.'''
@csrf_exempt
def showDisputes(request, disputeID):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    if(request.method == "GET"):
        try:
            curCase = Disputes.objects.get(id=disputeID)
        except:
            return HttpResponse("Dispute with the given ID doesn't exist.", status=status.HTTP_400_BAD_REQUEST)
        if(curCase.guide.creator != request.user 
                and curCase.visitor.user != request.user 
                and (not request.user.is_superuser)):
            return HttpResponse("You don't have permission to view this dispute", 
                                status=status.HTTP_401_UNAUTHORIZED)
        cur_dict = json.loads(serializers.serialize('json', [curCase, ]))[0]['fields']
        cur_dict["visitor"] = Visitors.objects.get(id=cur_dict['visitor']).user
        cur_dict["guide"] = Guide.objects.get(id=cur_dict['guide']).creator
        return render(request, '../templates/main/disputes.html', {'dispute': cur_dict}, status=200)
    
'''Responsible for creating and resolving a dispute between guide and visitors. Only accessible
to the visitor and the guide implicated on the dispute'''
@csrf_exempt
def disputes(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    #Create a new dispute that takes in the visitor's Username and guide's username
    if(request.method == "POST"):
        data = checkValidJSONInput(request)
        if("visitorUsername" not in data.keys()):
            return HttpResponse("Input valid visitor name",  status=status.HTTP_400_BAD_REQUEST)
        if("guideUsername" not in data.keys()):
            return HttpResponse("Input valid guide name", status=status.HTTP_400_BAD_REQUEST)
        if("description" not in data.keys()):
            return HttpResponse("Input valid description",status=status.HTTP_400_BAD_REQUEST)
        try:
            guide = Guide.objects.get(user=User.objects.get(username=data["guideUsername"]))
            visitor = Visitors.objects.get(user=User.objects.get(username=data["visitorUsername"]))
        except:
            return HttpResponse("Guide or visitor not found.", status=status.HTTP_400_BAD_REQUEST)
        newDispute = Dispute(visitor=visitor, 
                                guide=guide, description=data["description"])
        newDispute.save()
        cur_dict = json.loads(serializers.serialize('json', [newDispute, ]))[0]['fields']
        cur_dict["guide"] = formatUser(guide.creator)
        cur_dict["visitor"] = formatUser(visitor.user)
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    #Delete a dispute given a dispute ID. 
    elif(request.method == "DELETE"):
        data = checkValidJSONInput(request)
        if("disputeID" not in data.keys()):
            return HttpResponse("Input valid disputeID", status=status.HTTP_400_BAD_REQUEST)
        try:
            curCase = Disputes.objects.get(id=data["disputeID"])
        except:
            return HttpResponse("Dispute with the given ID doesn't exist.", 
                                status=status.HTTP_400_BAD_REQUEST)
        if(curCase.guide.creator != request.user 
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
def visitors(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    #Responsible for populating a webpage with the data from the database. 
    if(request.method == "GET"):
        try:
            currentProf = Visitors.objects.get(user=request.user)
        except:
            return HttpResponse("You have to be a visitor to view visitors information.", 
                                status=status.HTTP_401_UNAUTHORIZED)
        cur_dict = json.loads(serializers.serialize('json', [currentProf, ]))[0]['fields']
        tourObj = []
        allTours = Tour.objects.filter(Guest=currentProf)
        for tour in allTours:
            cur_dict2 = json.loads(serializers.serialize('json', [tour, ]))[0]['fields']
            cur_dict2["Guest"] = Visitors.objects.get(id=cur_dict2["Guest"]).user.username
            cur_dict2["Guide"] = Guide.objects.get(id=cur_dict2["Guide"]).creator.username
            tourObj.append(cur_dict2)    
        return render(request, '../templates/main/profile.html', 
                     {'visitor': currentProf, 'tourArr': tourObj}, 
                     status=200)
    #Responsible for changing an instance of a visitor with the data inputted in the request
    elif(request.method == "PATCH"):
        data = checkValidJSONInput(request)
        try:
            currentProf = Visitors.objects.get(user=request.user)
        except:
            return HttpResponse("You have to be a visitor to modify visitor profile.", 
                                status=status.HTTP_401_UNAUTHORIZED)
        if("description" in data.keys()):
            currentProf.description = data["description"]
        if("sex" in data.keys()):
            currentProf.sex = data["sex"]
        currentProf.save()
        cur_dict = json.loads(serializers.serialize('json', [currentProf, ]))[0]['fields']
        cur_dict["user"] = formatUser(User.objects.get(id=cur_dict["user"]))
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    #Resposible for creating a new visitor instance with the data inputted in the request. 
    elif(request.method == "POST"):
        data = checkValidJSONInput(request)
        try:
            Visitors.objects.get(user=request.user)
            return HttpResponse("You are already a visitor.", status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        if(not "description" in data.keys()):
            return HttpResponse("description is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        if(not "sex" in data.keys()):
            return HttpResponse("User Sex is Required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        newVisitor = Visitors(description=data["description"], sex=data["sex"], user=request.user)
        newVisitor.save()
        cur_dict = json.loads(serializers.serialize('json', [newVisitor, ]))[0]['fields']
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
            userToBeDeleted = Visitors.objects.get(id=data["visitorID"])
        except:
            return HttpResponse("Visitor with the given ID doesn't exist", 
                                content_type="plain/text", 
                                status=status.HTTP_400_BAD_REQUEST)
        if(not request.user.is_superuser and userToBeDeleted.user != request.user):
            return HttpResponse("You have to be an administrator or owner to delete a user", 
                                content_type="plain/text", 
                                status=status.HTTP_401_UNAUTHORIZED)
        try:
            relevantTours = Tours.objects.get(Guest=userToBeDeleted)
            relevantTours.delete()
        except:
            pass    
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











                
                
