from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Equipment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def all_equipment(request):
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        equip_list = Equipment.objects.filter(display_name__contains=search_query)
        page = request.GET.get('page', 1)
        paginator = Paginator(equip_list, 6)

        try:
            equipments = paginator.page(page)
        except PageNotAnInteger:
            equipments = paginator.page(1)
        except EmptyPage:
            equipments = paginator.page(paginator.num_pages)

        return render(request, 'inventory/inventory.html', {'query':search_query, 'equipments': equipments})
    if request.GET.get('locationsort'):
        locationsort = request.GET.get('locationsort')
        equip_list = Equipment.objects.filter(location=locationsort)
        page = request.GET.get('page', 1)

        paginator = Paginator(equip_list, 6)
                
        try:
            equipments = paginator.page(page)
        except PageNotAnInteger:
            equipments = paginator.page(1)
        except EmptyPage:
            equipments = paginator.page(paginator.num_pages)

        return render(request, 'inventory/inventory.html', {'query':locationsort, 'equipments': equipments})

    else:
        equip_list = Equipment.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(equip_list, 6)
        
        try:
            equipments = paginator.page(page)
        except PageNotAnInteger:
            equipments = paginator.page(1)
        except EmptyPage:
            equipments = paginator.page(paginator.num_pages)

        return render(request, 'inventory/inventory.html', { 'equipments': equipments } )

def detail(request, equipment_id):
    equipment = get_object_or_404(Equipment,pk=equipment_id)
    return render(request, 'inventory/detail.html', {'equipment':equipment})