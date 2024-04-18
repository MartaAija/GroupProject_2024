from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Equipment

# Create your views here.
def all_equipment(request):
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        equipments = Equipment.objects.filter(display_name__contains=search_query)
        return render(request, 'inventory/inventory.html', {'query':search_query, 'equipments': equipments})
    else:
        equipments = Equipment.objects.all()
        return render(request, 'inventory/inventory.html',{ 'equipments': equipments})

def detail(request, equipment_id):
    equipment = get_object_or_404(Equipment,pk=equipment_id)
    return render(request, 'inventory/detail.html', {'equipment':equipment})