from django.urls import path
from . import views
from .views import all_equipment


urlpatterns = [
    path('', all_equipment, name='inventory'),
    path('<int:equipment_id>', views.detail,name='detail')
]