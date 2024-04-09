from django.urls import path
from .views import all_equipment


urlpatterns = [
    path('', all_equipment, name='inventory'),
]