from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

# renders the home page with links to other parts of the webpage
@csrf_exempt
def home(request):
        if request.method == 'GET':
                return render(request, 'main/homepage.html')
        else:
                return HttpResponse('Method not allowed on /.', status=405)
