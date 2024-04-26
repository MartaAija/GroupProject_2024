from django.urls import path
from .views import reportItems

urlpatterns = [
    path('', reportItems, name = "report"),
]