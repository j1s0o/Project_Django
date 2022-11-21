from django.forms import ModelForm
from django.contrib.auth.models import Group
from .models import UserProfile

class TeamForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name' , 'password']
        
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields= "__all__"

