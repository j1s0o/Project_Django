from django.shortcuts import render , redirect
from django.http import JsonResponse ,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth , login as auth_login , logout as auth_logout
from .models import Team , Chall , CustomUser as User
from  .forms import TeamForm
from json import dumps , loads
from django.views.decorators.csrf import csrf_exempt
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
    context = {'teams': teams}
    return render(request, 'base/navbar/scoreboard.html' , context)


@csrf_exempt
@login_required(login_url='login')
def chall(request , pk):
    if request.user.team is not None:
        if request.method == 'GET':
            type_chall = ("Web exploit" , "Cryptography" , "Pwnable" , "Reverse")
            if pk == "all":
                chall = Chall.objects.all() # get all
            elif pk == "web":
                chall = Chall.objects.filter(type="Web exploit")
            elif pk == "crypto":
                chall = Chall.objects.filter(type="Cryptography")
            elif pk == "pwn":
                chall = Chall.objects.filter(type="Pwnable")
            elif pk == "re":
                chall = Chall.objects.filter(type="Reverse")
            data = dumps(
                [
                    {
                        'chall_name' : obj.chall_name,
                        'point' : obj.point,
                        'team_solved' : [
                            {
                                'team_name' : i.name
                            }
                            for i in obj.team_solved.filter(name = request.user.team)
                        ]
                    }
                    for obj in chall
                ]
            )
            
        elif request.method == 'POST' and pk =='solved':
            data = request.body
            data = loads(data)
            team = request.user.team
            point = data['point']
            chall_name = data['chall_name']
            chall = Chall.objects.get(chall_name = chall_name)
            user = User.objects.get(username = request.user.username)
            # team = chall.team_solved.all()[0]
            team_solved = chall.team_solved.filter(name = team)
            if team_solved.exists():
                context = {'msg' : 'false'}
                return JsonResponse(context)
            elif data['user_flag'] == chall.flag:
                score = User.objects.get(username = request.user.username).score
                score = point + score
                User.objects.filter(username = request.user.username).update(score=score)
                user.solved.add(chall)
                chall.team_solved.add(team)
                team_score = Team.objects.get(name=team).score + point
                Team.objects.filter(name=team).update(score=team_score)
                context = {'msg' : 'done'}
                return JsonResponse(context)
    else:
        return redirect('/create_team')
    context = {'chall' : chall , 'type_chall' : type_chall , 'data' : data }
    return render(request ,  'base/chall/chall.html' , context )


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
                return redirect('/chall/all/')
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
            return redirect('/chall/all/')
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
            return redirect('/chall/all/')
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
                return redirect('create_team')
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
            return redirect('/chall/all/')
        else:
            messages.error(request, "Invalid username or password!!!")

    return render(request, 'base/navbar/login.html')


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('home')

def Users(request):
    users = User.objects.all().order_by('-score')
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
        if i.team == team:
            user.append(i)
    context = {'team': team , "user" : user }
    return render(request , 'base/teams/teamprofile.html', context)


def UserProfile(request , pk):
    user = User.objects.get(username=pk)
    context = {'user': user}
    return render(request , 'base/user/userprofile.html' , context)