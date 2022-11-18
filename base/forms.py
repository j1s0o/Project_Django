from django.forms import ModelForm
from django.contrib.auth.models import Group

class TeamForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"

