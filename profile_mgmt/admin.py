# WORKED ON THIS FILE
#    - DOMINIC JOBSON (w1892005)


from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Profile)

#MIX PROFILE INFO AND USER INFO
class ProfileInline(admin.StackedInline):
    model = Profile
    
#EXTEND USER MODEL
class UserAdmin(admin.ModelAdmin):
    model = User
    field =["username","first_name","last_name","email",]
    inlines = [ProfileInline]
    

#UNRESGISTER OLD METHOD
admin.site.unregister(User)

#RE-REGISTER NEW METHOD
admin.site.register(User,UserAdmin)