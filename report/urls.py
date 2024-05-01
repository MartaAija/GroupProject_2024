#   WORKED ON FILE:
#        - NOEL VARGA (w1932378)

from django.urls import path
from .views import reportItems

urlpatterns = [
    path('', reportItems, name = "report"),
]