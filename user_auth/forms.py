# WORKED ON THIS FILE
#    - DOMINIC JOBSON (w1892005)

from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserAuthForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields =["username","first_name","last_name", "email","password1", "password2"]