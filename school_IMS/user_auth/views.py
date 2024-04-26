from django.shortcuts import render, redirect
from .forms import UserAuthForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request,("There was an error logging in, please try again..."))
            return redirect('login')
   
    return render(request,'registration/login.html',{} )

def UserAuth(request):
    if request.method == "POST":
        form = UserAuthForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,'Sign up successful...')
            return redirect('user_info')    
        
    else:
        form = UserAuthForm()
        
    return render(request,"UserAuth/UserAuth.html",{"form":form})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect('/')