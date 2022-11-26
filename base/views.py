from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth , login as auth_login , logout as auth_logout
from .models import Team , Chall , CustomUser as User
from  .forms import TeamForm
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

@login_required(login_url='login')
def chall(request):
    if request.user.team is not None:
        chall = Chall.objects.all() # get all
        web = Chall.objects.filter(type="Web exploit")
        crypto = Chall.objects.filter(type="Cryptography")
        pwn = Chall.objects.filter(type="Pwnable")
        re = Chall.objects.filter(type="Reverse")
        type_chall = ("Web exploit" , "Cryptography" , "Pwnable" , "Reverse")
        context = {'chall' : chall , 'web' : web , 'crypto' : crypto , 'pwn' : pwn , 're' : re , 'type_chall' : type_chall}
    else:
        return redirect('/create_team')
    return render(request ,  'base/chall/chall.html' , context)

@login_required(login_url='login')    
def web(request):
    if request.user.team is not None:
        web = Chall.objects.filter(type="Web exploit")
        context = {'web': web}
    else:
        return redirect('/create_team')
    return render(request, 'base/chall/web.html', context)

@login_required(login_url='login')
def crypto(request):
    if request.user.team is not None:
        crypto = Chall.objects.filter(type="Cryptography")
        context = {'crypto': crypto}
    else:
        return redirect('/create_team')
    return render(request, 'base/chall/crypto.html', context)

@login_required(login_url='login')
def pwn(request):
    if request.user.team is not None:
        pwn = Chall.objects.filter(type="Pwnable")
        context = {'pwn': pwn}
    else:
        return redirect('/create_team')
    return render(request, 'base/chall/pwn.html', context)

@login_required(login_url='login')
def re(request):
    if request.user.team is not None:
        re = Chall.objects.filter(type="Reverse")
        context = {'re': re}
    else:
        return redirect('/create_team')
    return render(request, 'base/chall/re.html', context)

@login_required(login_url='login')
def create_team(request):
    form = TeamForm()
    context = {'form': form}
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            if  Team.objects.filter(name = form.cleaned_data['name']).exists():
                return redirect('create_team')
            else:
                form.save()
                team = Team.objects.get(name = form.cleaned_data['name'])
                User.objects.filter(username = request.user.username).update(team=team)
                return redirect('chall')
    return render(request, 'base/teams/create_team.html' , context) 

@login_required(login_url='login')
def join_team(request):
    form = TeamForm()
    context = {'form': form}
    if request.method == 'POST':
        form = TeamForm(request.POST)
    if form.is_valid():
        if  Team.objects.filter(name = form.cleaned_data['name'] , password=form.cleaned_data['password']).exists():
            team = Team.objects.get(name = form.cleaned_data['name'])
            User.objects.filter(username = request.user.username).update(team=team)
            return redirect('/chall')
        else:
            messages.error(request,'Your team\'s password is incorrect , if you don\'t have team please create')
    return render(request, 'base/teams/join_team.html' , context)

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

def register(request ):
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
        else:
            try:
                user = User.objects.create_user(username , password , email)
                user.save()
                auth_login(request, user)
                return redirect('chall')
            except:
                messages.error(request, 'Something missing or invalid')
                return redirect('register')

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


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('home')

def Users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'base/user/user.html', context)

def teams(request):
    teams  = Team.objects.all() # get all teams
    context = {'teams': teams}
    return render(request, 'base/teams/teams.html' , context)


def TeamProfile(request , pk):
    team = None
    teams = Team.objects.all()
    for i in teams:
        if i.name == pk:
            team = i
    user = []
    users = User.objects.all()
    for i in users:
        if i.team.filter(name=team).exists():
            user.append(i.username)
    context = {'team': team , "user" : user}
    return render(request , 'base/teams/teamprofile.html', context)

