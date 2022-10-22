from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('rules/' , views.rules , name='rules'),
    path('sponsors/' , views.sponsors , name='sponsors'),
    path('scoreboard/' , views.scoreboard , name='scoreboard'),
    path('teams/', views.teams , name='teams'),
    path('chall/', views.chall , name='chall'),
    path('chall/web/', views.web , name='challweb'),
    path('chall/crypto/', views.crypto , name='challcrypto'),
    path('chall/pwn/', views.pwn , name='challpwn'),
    path('chall/re/', views.re , name='challre'),
    path('create_team/', views.create_team , name='create_team'),
    path('update_team/<str:pk>/', views.update_team, name='update_team'),
    path('register/', views.register , name='register'),
    path('login/', views.login , name='login'),
    path('logout/', views.logout, name='logout'),
]