from django.urls import path
from user_auth import views as V 

urlpatterns = [
path("SignUp/", V.UserAuth, name='SignUp'),
path("logout/", V.logout_user, name='logout'),
]

