from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import authenticate as auth , login as auth_login , logout as auth_logout
from .models import Team , Chall 
from .forms import TeamForm 
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
    return render(request, 'base/navbar/scoreboard.html')

def teams(request):
    team  = Team.objects.all() # get all teams
    context = {'team': team}
    return render(request, 'base/teams/teams.html' , context)


def chall(request ):
    chall = Chall.objects.all() # get all
    web = Chall.objects.filter(type="Web exploit")
    crypto = Chall.objects.filter(type="Cryptography")
    pwn = Chall.objects.filter(type="Pwnable")
    re = Chall.objects.filter(type="Reverse")
    type_chall = ("Web exploit" , "Cryptography" , "Pwnable" , "Reverse")
    context = {'chall' : chall , 'web' : web , 'crypto' : crypto , 'pwn' : pwn , 're' : re , 'type_chall' : type_chall}
    return render(request ,  'base/chall/chall.html' , context)
    
def web(request):
    web = Chall.objects.filter(type="Web exploit")
    context = {'web': web}
    return render(request, 'base/chall/web.html', context)
def crypto(request):
    crypto = Chall.objects.filter(type="Cryptography")
    context = {'crypto': crypto}
    return render(request, 'base/chall/crypto.html', context)
def pwn(request):
    pwn = Chall.objects.filter(type="Pwnable")
    context = {'pwn': pwn}
    return render(request, 'base/chall/pwn.html', context)
def re(request):
    re = Chall.objects.filter(type="Reverse")
    context = {'re': re}
    return render(request, 'base/chall/re.html', context)



def create_team(request):
    form = TeamForm()
    context = {'form': form}
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chall')
    return render(request, 'base/teams/create_team.html' , context) 

def update_team(request , pk):
    team = Team.objects.get(id=pk)
    form = TeamForm(instance=team)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('chall')
    context = {'form': form}
    return render(request, 'base/teams/create_team.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if username == "" or  password == "" or confirm_password == "" or email == "":
            messages.error(request, 'Something missing or invalid')
            return redirect('register')
        elif password != confirm_password :
            messages.error(request,'Password does not match')
            return redirect('register')
        elif User.objects.get(username=username) is not None:
            messages.error(request , "User have already exists")
            return redirect('register')
        else:
            user = User.objects.create_user(username , password , email)
            user.save()
            auth_login(request, user)
            return redirect('chall')
    return render(request , 'base/navbar/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if password == "" or username =="":
            messages.error(request, 'Please enter username or password')
            return redirect('login')
        else:    
            user = auth(request , username=username, password=password)        
        if user is not None :
            auth_login(request, user)
            return redirect('chall')
        else:
            messages.error(request, "Invalid username or password!!!")

    return render(request, 'base/navbar/login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')