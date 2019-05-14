from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from main.models import Guide, Tours, Review, Countries, States, Cities, Visitors, VisitorReview, Disputes
from rest_framework import status
from mysite.serializer import VisitorReview
import json
from django.core import serializers

@csrf_exempt
def userreview(request):
        if(not request.user.is_authenticated):
                return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
        if(request.method == "GET"):
            currentProf = Visitors.objects.get(user=request.user)
            print(currentProf)
            if(currentProf == None):
                return HttpResponse("You have to be a visitor to view visitor review.", status=status.HTTP_401_UNAUTHORIZED)
            print("I'm out")
            curReview = VisitorReview.objects.get(visitor=currentProf)
            cur_dict = json.loads(serializers.serialize('json', [curReview, ]))[0]['fields']
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, content_type="application/json", status=status.HTTP_200_OK)
        elif(request.method == "POST"):
            if(not request.user.is_authenticated):
                return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.", status=status.HTTP_401_UNAUTHORIZED)
            data = checkValidJSONInput(request)
            #if(allReviews != None):
            #    return HttpResponse("You have already written review for this visitor", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
            if(not "visitorName" in data.keys()):
                return HttpResponse("visitorName is required", 
                    content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
            if(not "content" in data.keys()):
                return HttpResponse("Review Content is required", 
                    content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
            newReview = VisitorReview(visitor=Visitors.objects.get(name=data["visitorName"]), content=data["content"])
            if("title" in data.keys()):
                newReview.title = data["title"]
            if("stars" in data.keys()):
                newReview.stars = data["stars"]
            newReview.save()
            cur_dict = json.loads(serializers.serialize('json', [newReview, ]))[0]['fields']
            cur_dict["visitor_name"] = data["visitorName"]
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
        elif(request.method == "DELETE"):
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.")
            data = checkValidJSONInput(request)
            if(not "visitorName" in data.keys()):
                return HttpResponse("visitorName is required", 
                    content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
            allReviews = VisitorReview.objects.filter(visitor=Visitors.objects.get(name=data["visitorName"]))
            allReviews.delete()
            return HttpResponse("All Reviews Deleted.", content_type="plain/text",status=status.HTTP_200_OK)
        elif(request.method == "PATCH"):
            if(not request.user.is_authenticated):
                return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.", status=status.HTTP_401_UNAUTHORIZED)
            data = checkValidJSONInput(request)
            if(not "visitorName" in data.keys()):
                return HttpResponse("visitorName is required", 
                    content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
            allReviews = VisitorReview.objects.get(visitor=Visitors.objects.get(name=data["visitorName"]))
            if("content" in data.keys()):
                allReviews.content = data["content"]
            if("title" in data.keys()):
                allReviews.title = data["title"]
            if("stars" in data.keys()):
                allReviews.stars = data["stars"]
            allReviews.save()
            cur_dict = json.loads(serializers.serialize('json', [allReviews, ]))[0]['fields']
            cur_dict["visitor_name"] = data["visitorName"]
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)

@csrf_exempt
def disputes(request, disputeID):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    if(request.method == "GET"):
        try:
            curCase = Disputes.objects.get(id=disputeID)
        except:
            return HttpResponse("Dispute with the given ID doesn't exist.", status=status.HTTP_400_BAD_REQUEST)
        if(curCase.guide.creator != request.user and curCase.visitor.user != request.user and (not request.user.is_superuser)):
            return HttpResponse("You don't have permission to view this dispute", status=status.HTTP_401_UNAUTHORIZED)
        cur_dict = json.loads(serializers.serialize('json', [curCase, ]))[0]['fields']
        print(Visitors.objects.get(id=cur_dict['visitor']).user)
        cur_dict["visitor"] = Visitors.objects.get(id=cur_dict['visitor']).user
        cur_dict["guide"] = Guide.objects.get(id=cur_dict['guide']).creator
        return render(request, '../templates/main/disputes.html', {'dispute': cur_dict}, status=200)
    elif(request.method == "POST"):
        data = checkValidJSONInput(request)
        if("visitorID" not in data.keys()):
            return HttpResponse("Input valid visitorID",  status=status.HTTP_400_BAD_REQUEST)
        if("guideID" not in data.keys()):
            return HttpResponse("Input valid guideID", status=status.HTTP_400_BAD_REQUEST)
        if("description" not in data.keys()):
            return HttpResponse("Input valid description",status=status.HTTP_400_BAD_REQUEST)
        try:
            guide = Guide.objects.get(id=data["guideID"])
            visitor = Visitors.objects.get(id=data["visitorID"])
        except:
            return HttpResponse("Guide or visitor not found.", status=status.HTTP_400_BAD_REQUEST)
        newDispute = Disputes(visitor=visitor, 
                                guide=guide, description=data["description"])
        newDispute.save()
        cur_dict = json.loads(serializers.serialize('json', [newDispute, ]))[0]['fields']
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    elif(request.method == "DELETE"):
        data = checkValidJSONInput(request)
        if("disputeID" not in data.keys()):
            return HttpResponse("Input valid disputeID", status=status.HTTP_400_BAD_REQUEST)
        try:
            curCase = Disputes.objects.get(id=data["disputeID"])
        except:
            return HttpResponse("Dispute with the given ID doesn't exist.", status=status.HTTP_400_BAD_REQUEST)
        if(curCase.guide.creator != request.user and curCase.visitor.user != request.user and (not request.user.is_superuser)):
            return HttpResponse("You don't have permission to view this dispute", status=status.HTTP_401_UNAUTHORIZED)
        curCase.delete()
        return HttpResponse("Dispute successfully resolved", status=status.HTTP_200_OK)

@csrf_exempt
def visitors(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    if(request.method == "GET"):
        try:
            currentProf = Visitors.objects.get(user=request.user)
        except:
            return HttpResponse("You have to be a visitor to view visitor review.")
        cur_dict = json.loads(serializers.serialize('json', [currentProf, ]))[0]['fields']
        print(cur_dict)
        print(json.loads(serializers.serialize('json', [User.objects.get(id=cur_dict['user']), ]))[0]['fields']['username'])
        tourObj = []
        for tour in cur_dict["tour"]:
            currentTour = Tours.objects.get(id=tour)
            cur_dict2 = json.loads(serializers.serialize('json', [currentTour, ]))[0]['fields']
            cur_dict2["guide"] = currentTour.Guide.creator
            cur_dict2["start"] = str(currentTour.Start)
            cur_dict2["end"] = str(currentTour.End)
            tourObj.append(cur_dict2)
        return render(request, '../templates/main/profile.html', {'visitor': currentProf, 'tourArr': tourObj}, status=200)
    elif(request.method == "PATCH"):
        data = checkValidJSONInput(request)
        try:
            currentProf = Visitors.objects.get(user=request.user)
        except:
            return HttpResponse("You have to be a visitor to modify visitor profile.")
        if("description" in data.keys()):
            currentProf.description = data["description"]
        if("sex" in data.keys()):
            currentProf.sex = data["sex"]
        currentProf.save()
        cur_dict = json.loads(serializers.serialize('json', [currentProf, ]))[0]['fields']
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
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
        if("tour" in data.keys()):
            newVisitor.tour = data["tour"]
        newVisitor.save()
        cur_dict = json.loads(serializers.serialize('json', [newVisitor, ]))[0]['fields']
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    elif(request.method == "DELETE"):
        data = checkValidJSONInput(request)
        if(not "visitorID" in data.keys()):
            return HttpResponse("visitorName is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        try:
            userToBeDeleted = Visitors.objects.get(id=data["visitorID"])
        except:
            return HttpResponse("Visitor with the given ID doesn't exist", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        if(not request.user.is_superuser and userToBeDeleted.user != request.user):
            return HttpResponse("You have to be an administrator or owner to delete a user", content_type="plain/text", status=status.HTTP_401_UNAUTHORIZED)
        userToBeDeleted.delete()
        return HttpResponse("User Deleted", status=status.HTTP_200_OK)


def checkValidJSONInput(request):
    try:
        data = json.loads(request.body.decode("utf-8"))   
    except:
        return HttpResponse("Valid JSON Input required", status=status.HTTP_400_BAD_REQUEST)
    return data












                
                
