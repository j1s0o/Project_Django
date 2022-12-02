from django.urls import path , re_path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('rules/' , views.rules , name='rules'),
    path('sponsors/' , views.sponsors , name='sponsors'),
    path('scoreboard/' , views.scoreboard , name='scoreboard'),
    path('team/', views.teams , name='team'),
    path('chall/<str:pk>/', views.chall , name='chall'),
    path('create_team/', views.create_team , name='create_team'),
    path('join_team/', views.join_team , name='join_team'),
    path('update_team/<str:pk>/', views.update_team, name='update_team'),
    path('register/', views.register , name='register'),
    path('login/', views.login , name='login'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.Users , name='users'),
    path('userprofile/<str:pk>/', views.UserProfile , name='userprofile'),
    path('team/<str:pk>/', views.TeamProfile , name='teamprofile'),
    
]