from django.shortcuts import render , redirect
from django.http import JsonResponse ,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth , login as auth_login , logout as auth_logout
from .models import Team , Chall , CustomUser as User
from  .forms import TeamForm
from json import dumps , loads
from django.views.decorators.csrf import csrf_exempt

#Paginator 
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    user = User.objects.all() # show all challenges
    context = {'user': user}
    return render(request, 'base/navbar/home.html', context)
    
def rules(request):
    return render(request, 'base/navbar/rules.html')

def sponsors(request):
    return render(request, 'base/navbar/sponsors.html')

def scoreboard(request):
    teams  = Team.objects.all().order_by("-score") # get all teams
    paginator = Paginator(teams, 15) # Show 15 team per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'teams': teams,'page_obj': page_obj}
    return render(request, 'base/navbar/scoreboard.html' , context)





