from django.shortcuts import render
from .models import Equipment

# Create your views here.
def all_equipment(request):
    equipments = Equipment.objects.all()
    return render(request, 'inventory/inventory.html', {'equipments': equipments})
