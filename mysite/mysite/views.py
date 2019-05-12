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
                return HttpResponse("You have to be a visitor to view visitor review.")
            print("I'm out")
            curReview = VisitorReview.objects.get(visitor=currentProf)
            cur_dict = json.loads(serializers.serialize('json', [curReview, ]))[0]['fields']
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, content_type="application/json", status=status.HTTP_200_OK)
        elif(request.method == "POST"):
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.")
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
            if("content" in data.keys()):
                newReview.content = data["content"]
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
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.")
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
def disputes(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
    if(request.method == "GET"):
        data = checkValidJSONInput(request)
        try:
            curCase = Disputes.objects.get(id=data["disputeID"])
        except:
            return HttpResponse("Dispute with the given ID doesn't exist.", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        print(request.user)
        print(curCase.guide.creator)
        if(curCase.guide.creator != request.user and curCase.visitor.user != request.user and (not request.user.is_superuser)):
            return HttpResponse("You don't have permission to view this dispute", content_type="plain/text", status=status.HTTP_401_UNAUTHORIZED)
        cur_dict = json.loads(serializers.serialize('json', [curCase, ]))[0]['fields']
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    elif(request.method == "POST"):
        data = checkValidJSONInput(request)
        if("visitorID" not in data.keys()):
            return HttpResponse("Input valid visitorID", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        if("guideID" not in data.keys()):
            return HttpResponse("Input valid guideID", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        if("description" not in data.keys()):
            return HttpResponse("Input valid description", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        try:
            guide = Guide.objects.get(id=data["guideID"])
            visitor = Visitors.objects.get(id=data["visitorID"])
        except:
            return HttpResponse("Guide or visitor not found.", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        newDispute = Disputes(visitor=visitor, 
                                guide=guide, description=data["description"])
        newDispute.save()
        cur_dict = json.loads(serializers.serialize('json', [newDispute, ]))[0]['fields']
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    elif(request.method == "DELETE"):
        data = checkValidJSONInput(request)
        if("disputeID" not in data.keys()):
            return HttpResponse("Input valid disputeID", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        try:
            curCase = Disputes.objects.get(id=data["disputeID"])
        except:
            return HttpResponse("Dispute with the given ID doesn't exist.", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
        if(curCase.guide.creator != request.user and curCase.visitor.user != request.user and (not request.user.is_superuser)):
            return HttpResponse("You don't have permission to view this dispute", content_type="plain/text", status=status.HTTP_401_UNAUTHORIZED)
        curCase.delete()
        return HttpResponse("Dispute successfully resolved", content_type="plain/text", status=status.HTTP_200_OK)
def visitors(request):
    if(not request.user.is_authenticated):
        return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)

    if(request.method == "GET"):
        currentProf = Visitors.objects.get(user=request.user)
        print(currentProf)
        if(currentProf == None):
            return HttpResponse("You have to be a visitor to view visitor review.")
        cur_dict = json.loads(serializers.serialize('json', [currentProf, ]))[0]['fields']
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, content_type="application/json", status=status.HTTP_200_OK)
    elif(request.method == "PATCH"):
        data =checkValidJSONInput(request)
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
        if(not "description" in data.keys()):
            return HttpResponse("visitorName is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        if(not "sex" in data.keys()):
            return HttpResponse("Review Content is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        newVisitor = Visitors(description=data["description"], sex=data["sex"], user=request.user)
        if("tour" in data.keys()):
            newVisitor.tour = data["tour"]
        newVisitor.save()
        cur_dict = json.loads(serializers.serialize('json', [newVisitor, ]))[0]['fields']
        serializedObj = json.dumps(cur_dict)
        return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
    elif(request.method == "DELETE"):
        if(not request.user.is_superuser):
            return HttpResponse("You have to be an administrator to delete a user", content_type="plain/text", status=status.HTTP_401_UNAUTHORIZED)
        data = checkValidJSONInput(request)
        if(not "visitorID" in data.keys()):
            return HttpResponse("visitorName is required", 
                content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
        userToBeDeleted = Visitors.objects.filter(id=data["visitorID"])
        userToBeDeleted.delete()
        return HttpResponse("User Deleted", content_type="plain/text",status=status.HTTP_200_OK)

def checkValidJSONInput(request):
    try:
        data = json.loads(request.body.decode("utf-8"))   
    except:
        return HttpResponse("Valid JSON Input required", content_type="plain/text", status=status.HTTP_400_BAD_REQUEST)
    return data












                
                
