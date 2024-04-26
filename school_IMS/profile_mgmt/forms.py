from django.contrib.auth.models import User
from django import forms
from .models import Profile



class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'formm-control','placeholder':'Phone'}), required=False)
    address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'formm-control','placeholder':'Address 1'}), required=False)
    address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'formm-control','placeholder':'Address 2'}), required=False)
    postcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'formm-control','placeholder':'PostCode'}), required=False)
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'formm-control','placeholder':'City'}), required=False)
    
    class Meta:
        model = Profile
        fields = ('phone', 'address1','address2','postcode','city',)