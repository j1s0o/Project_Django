from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as auth , login as auth_login , logout as auth_logout
from .models import   CustomUser as User


#Paginator 
from django.core.paginator import Paginator

# Create your views here.
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
    paginator = Paginator(users, 15) # Show 15 team per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'users': users, 'page_obj': page_obj}
    if request.GET.get('search')!=None:
        path = request.GET.get('search')
        url = '/userprofile/' + path
        if User.objects.filter(username = path).exists():
            return redirect(url)
        else:
            return redirect('/users')
    return render(request, 'base/user/user.html', context)

def UserProfile(request , pk):
    user = User.objects.get(username=pk)
    context = {'user': user}
    return render(request , 'base/user/userprofile.html' , context)