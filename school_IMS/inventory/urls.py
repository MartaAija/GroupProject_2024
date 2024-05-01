#    WORKED ON FILE:
#       - NOEL VARGA (w1932378)
#       - Emina Asherbekova (w1830501)

from django.urls import path
from . import views
from .views import all_equipment, addProduct, addRecord, editProduct, updateRecord, removeProduct


urlpatterns = [
    path('', all_equipment, name='inventory'),
    path('<int:equipment_id>', views.detail,name='detail'),
    path('addProduct/', addProduct, name = "addProduct"),
    path('addProduct/addRecord/', addRecord, name = "addRecord"),
    path('editProduct/<int:id>', editProduct, name = "editProduct"),
    path('editProduct/updateRecord/<int:id>', updateRecord, name='updateRecord'),
    path('removeProduct/<int:id>', removeProduct, name = "removeProduct"),
]