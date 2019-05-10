from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from main.models import Guide, Tours, Review, Countries, States, Cities, Visitors, VisitorReview
from rest_framework import status
@csrf_exempt
def userreview(request):
        if(not request.user.is_authenticated):
                return HttpResponse("Unauthorized. Please Sign in", status=status.HTTP_401_UNAUTHORIZED)
        if(request.method == "GET"):
                isVisitor = (len(Visitors.objects.filter(id=request.user.id)) != 0)
                if(not isVisitor):
                    return HttpResponse("You have to be a visitor to view visitor review.")
                curReview = VisitorReview.objects.filter(visitor=Visitors.objects.filter(id=request.user.id))[0])
                
                
                
