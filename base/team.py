from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Team  , CustomUser as User
from  .forms import TeamForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#Paginator 
from django.core.paginator import Paginator

# Create your views here.
#Team
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


@login_required(login_url='login')
def update_team(request):
    team = Team.objects.get(name=request.user.team)
    form = TeamForm(instance=team)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('/chall/all/')
    context = {'form': form}
    return render(request, 'base/teams/update_team.html', context)


@csrf_exempt
def teams(request):
    teams  = Team.objects.all() # get all teams
    paginator = Paginator(teams, 15) # Show 15 team per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    if request.GET.get('search')!=None:
        path = request.GET.get('search')
        url = '/team/' + path
        if Team.objects.filter(name = path).exists():
            return redirect(url)
        else:
            return redirect('/team')
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

