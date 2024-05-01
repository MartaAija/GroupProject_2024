#    WORKED ON FILE:
#       - NOEL VARGA (w1932378) (Added admin views and functionalities)
#       - DOMINIC JOBSON (w1892005) (Created user profile and details functionalities)

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, reverse
from .models import Profile, User
from .forms import UserInfoForm, UpdateUserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# Create your views here.
#--------------------------------------------------------------------------------------------------
# User Profile page
@login_required
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        currentUser = request.user
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            return redirect('/')
        return render(request,"update_user.html",{'user_form': user_form, "currentUser" : currentUser})
    else:
        return redirect('/')

#--------------------------------------------------------------------------------------------------
# User information page
@login_required
def user_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user_id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        currentUser = request.user
        
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, "user_info.html", {'form':form, "currentUser" : currentUser})
    else:
        return redirect('/')

#--------------------------------------------------------------------------------------------------
# STATUS UPDATE FOR ADMIN
@login_required
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
@login_required
def editStatusPage(request, id):
    users = User.objects.get(id=id)
    currentUser = request.user
    return render(request, "editStatusPage.html", {"currentUser" : currentUser, "users" : users})

#--------------------------------------------------------------------------------------------------
# THIS FUNCTION UPDATES THE STATUS OF THE BOOKING IN "ReservationDetails" TABLE ACORDING THE CHANGES THE ADMIN MADE
@login_required
def updateStatus(request, id):
    statusUpdate = request.POST["statusUpdate"]
    user = User.objects.get(id=id)
    user.is_active = statusUpdate
    user.save()
    return HttpResponseRedirect(reverse("statusUpdate"))