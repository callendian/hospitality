from django.http import HttpResponse
from .forms import RegistrationForm, SigninForm
from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from main.models import *

@csrf_exempt
def register(request):
    if(request.method == "GET"):
        form = RegistrationForm()
        return render(request, '../templates/auth/register.html', {'form': form}, status=200)
    elif(request.method == "POST"):
        form = RegistrationForm(request.POST)
        if(not form.is_valid()):
            return HttpResponse("Invalid Registration Request.", status=400)
        print(form.cleaned_data)
        if(form.cleaned_data['password'] != form.cleaned_data['passwordconf']):
            return HttpResponse("Password did not match.", status=400)
        newUser = User.objects.create_user(
            username=form.cleaned_data['username'], 
            email=form.cleaned_data['email'], 
            password=form.cleaned_data['passwordconf'], 
            first_name=form.cleaned_data['first_name'], 
            last_name=form.cleaned_data['last_name'])
        newGuide = Guide(
            user = newUser, 
            first_name = form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'])
        newVisitor = Visitor(
            user = newUser, 
            first_name = form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
            )
        try:
            newGuide.save()
            newVisitor.save()
        except:
            return HttpResponse("Error in creating new user and guide")            
        return HttpResponseRedirect("/auth/signin")
    return HttpResponse("Method not allowed on /auth/register", status=405)

@sensitive_post_parameters()
@csrf_exempt
def signin(request):
    if(request.method == "GET"):
        form = SigninForm()
        return render(request, '../templates/auth/signin.html', {'form': form}, status=200)
    elif(request.method == "POST"):
        form = SigninForm(request.POST)
        if(not form.is_valid()):
            return HttpResponse("Bad login form", status=400)
        user = authenticate(
            request, 
            username=form.cleaned_data['username'], 
            password=form.cleaned_data['password'])
        if(user == None):
            return HttpResponse("Invalid Credentials.", status=401)
        else:
            login(request, user)
        return HttpResponseRedirect("/")
    return HttpResponse("Method not allowed on auth/signin.", status=405)

@sensitive_post_parameters()
@csrf_exempt
def signout(request):
    if(request.method == "GET"):
        if(request.user.is_authenticated):
            logout(request)
            return HttpResponse("Sign out successful.", status=200)
        return HttpResponse("Not logged in.", status=200)
    else:
        return HttpResponse("Method not allowed on auth/signout", status=405)