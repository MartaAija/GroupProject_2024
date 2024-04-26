from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, reverse
from .models import Profile, User
from .forms import UserInfoForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def user_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user_id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated" )
            return redirect('/')
        return render(request, "user_info.html", {'form':form})
    else:
        messages.success(request= "You must be logged in to view this page...")
        return redirect('/')

#--------------------------------------------------------------------------------------------------
# STATUS UPDATE FOR ADMIN
def statusUpdate(request):
    currentUser = request.user
    users_list = User.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(users_list, 6)
        
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "statusUpdate.html", {"currentUser" : currentUser, "users" : users})

#--------------------------------------------------------------------------------------------------
# EDIT STATUS VIEW FOR ADMIN
def editStatusPage(request, id):
    users = User.objects.get(id=id)
    currentUser = request.user
    return render(request, "editStatusPage.html", {"currentUser" : currentUser, "users" : users})

#--------------------------------------------------------------------------------------------------
# THIS FUNCTION UPDATES THE STATUS OF THE BOOKING IN "ReservationDetails" TABLE ACORDING THE CHANGES THE ADMIN MADE
def updateStatus(request, id):
    statusUpdate = request.POST["statusUpdate"]
    user = User.objects.get(id=id)
    user.is_active = statusUpdate
    user.save()
    return HttpResponseRedirect(reverse("statusUpdate"))