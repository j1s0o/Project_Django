from django.shortcuts import render , redirect
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from .models import Team , Chall , CustomUser as User
from json import dumps , loads
from django.views.decorators.csrf import csrf_exempt
#Paginator 
from django.core.paginator import Paginator

@csrf_exempt
@login_required(login_url='login')
def chall(request , pk):
    if request.user.team is not None:
        if request.method == 'GET':
            type_chall = ("Web exploit" , "Cryptography" , "Pwnable" , "Reverse")
            if pk == "all":
                chall = Chall.objects.all() # get all
                paginator = Paginator(chall, 12) # Show 12 contacts per page.

                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            elif pk == "web":
                chall = Chall.objects.filter(type="Web exploit")
                paginator = Paginator(chall, 12) # Show 12 contacts per page.

                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                #return render(request, 'list.html', {'page_obj': page_obj})
            elif pk == "crypto":
                chall = Chall.objects.filter(type="Cryptography")
                paginator = Paginator(chall, 12) # Show 12 contacts per page.

                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            elif pk == "pwn":
                chall = Chall.objects.filter(type="Pwnable")
                paginator = Paginator(chall, 12) # Show 12 contacts per page.

                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            elif pk == "re":
                chall = Chall.objects.filter(type="Reverse")
                paginator = Paginator(chall, 12) # Show 12 contacts per page.

                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
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
    context = {'chall' : chall , 'type_chall' : type_chall , 'data' : data, 'page_obj': page_obj}
    return render(request ,  'base/chall/chall.html' , context )

