from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Equipment
from django.core.paginator import Paginator

# Create your views here.
def all_equipment(request):
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        p = Paginator(Equipment.objects.filter(display_name__contains=search_query), 7)
        page = request.GET.get('page')
        equipments = p.get_page(page)

        return render(request, 'inventory/inventory.html', {'query':search_query, 'equipments': equipments})
    else:
        p = Paginator(Equipment.objects.all(), 7)
        page = request.GET.get('page')
        equipments = p.get_page(page)

        return render(request, 'inventory/inventory.html',{ 'equipments': equipments, })

def detail(request, equipment_id):
    equipment = get_object_or_404(Equipment,pk=equipment_id)
    return render(request, 'inventory/detail.html', {'equipment':equipment})