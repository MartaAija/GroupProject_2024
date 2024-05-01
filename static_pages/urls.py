from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name = "home"),
    path("termsnconditions/", views.termsnconditions, name = "termsnconditions"),
    path("contactus/", views.contactus, name = "contactus"),
    path("about/", views.about, name = "about"),
    path("faq/", views.faq, name = "faq"),
    path("history/", views.history, name = "history"),
    path("privacy/", views.privacy, name = "privacy"),
    path("contactus/contactus", views.contactus, name = "contactus"),
]

