from django.contrib import admin

# Register your models here.
from .models import Team , Chall , UserProfile

admin.site.register(Team)
admin.site.register(Chall)
admin.site.register(UserProfile)

