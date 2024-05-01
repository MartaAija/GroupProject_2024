# WORKED ON THIS FILE
#    - DOMINIC JOBSON (w1892005)

from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UpdateUserForm(UserChangeForm):
    password = None
    username = None
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email Address'}), required=True)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}), required=True)
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}), required=True)
    class Meta:
        model = User
        fields =["first_name","last_name", "email"]
    



class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}), required=False)
    address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 1'}), required=False)
    address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 2'}), required=False)
    postcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'PostCode'}), required=False)
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}), required=False)
    
    class Meta:
        model = Profile
        fields = ('phone', 'address1','address2','postcode','city',)