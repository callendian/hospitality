from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from main.models import Guide, Tours, Review, Countries, States, Cities, Visitors, VisitorReview
from rest_framework import status
from mysite.serializer import VisitorReview
import json
from django.core import serializers
@csrf_exempt
def userreview(request):
        if(not request.user.is_authenticated):
                return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
        if(request.method == "GET"):
            isVisitor = (len(Visitors.objects.filter(user=request.user)) != 0)
            if(not isVisitor):
                return HttpResponse("You have to be a visitor to view visitor review.")
            print("I'm out")
            curReview = VisitorReview.objects.filter(visitor=Visitors.objects.filter(id=request.user.id))[0]
            print(curReview)
            return HttpResponse("hihi", content_type="plain/text", status=status.HTTP_200_OK)
        elif(request.method == "POST"):
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.")
            data = json.loads(request.body.decode("utf-8"))
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
                newReview.content = data["stars"]
            newReview.save()
            cur_dict = json.loads(serializers.serialize('json', [newReview, ]))[0]['fields']
            cur_dict["visitor_name"] = data["visitorName"]
            serializedObj = json.dumps(cur_dict)
            return HttpResponse(serializedObj, "application/json", status=status.HTTP_201_CREATED)
        elif(request.method == "DELETE"):
            isGuide = Guide.objects.filter(creator=request.user)
            if(len(isGuide) == 0):
                return HttpResponse("You have to be a guide to write visitor review.")
            data = json.loads(request.body.decode("utf-8"))
            if(not "visitorName" in data.keys()):
                return HttpResponse("visitorName is required", 
                    content_type="text/plain", status=status.HTTP_400_BAD_REQUEST)
            allReviews = VisitorReview.objects.filter(visitor=Visitors.objects.get(name=data["visitorName"]))
            allReviews.delete()
            return HttpResponse("All Reviews Deleted.", content_type="plain/text",status=status.HTTP_200_OK)





                
                