from django.urls import path , re_path
from . import views , team , user , chall

urlpatterns = [
    path('', views.home , name='home'),
    path('rules/' , views.rules , name='rules'),
    path('sponsors/' , views.sponsors , name='sponsors'),
    path('scoreboard/' , views.scoreboard , name='scoreboard'),
    path('team/', team.teams , name='team'),
    path('chall/<str:pk>/', chall.chall , name='chall'),
    path('create_team/', team.create_team , name='create_team'),
    path('join_team/', team.join_team , name='join_team'),
    path('update_team/', team.update_team, name='update_team'),
    path('register/', user.register , name='register'),
    path('login/', user.login , name='login'),
    path('logout/', user.logout, name='logout'),
    path('users/', user.Users , name='users'),
    path('userprofile/<str:pk>/', user.UserProfile , name='userprofile'),
    path('team/<str:pk>/', team.TeamProfile , name='teamprofile'),
    
]