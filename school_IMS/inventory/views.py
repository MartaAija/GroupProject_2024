from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Equipment
from report.models import reports
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
        #-----------------------------------------------------------------------------------------------------
        # RETURNS THE REPORT OBJECT WHICH STORES THE REPORT INFO
        report = reports.objects.get(id=1)
        # THE FIRST AND LAST OBJECT IS RETRIEVED TO GO THROUGH THE LOOP CORRECTLY
        firstObject = Equipment.objects.all().first()
        lastObject = Equipment.objects.all().last()
        # THE LAST OBJECTS ID IS STORED AS THE LOOPS ITERATION LIMIT THE REPORTS "totalItems" IS SET TO 0
        # AND THE INDEX "i" VARIABLE IS SET TO THE FIRST OBJECTS ID
        iterationCount = lastObject.id
        report.totalItems = 0
        i = firstObject.id
        # THE LOOP ITERATES THROUGH ALL THE OBJECTS AND TRIES TO ADD THEIR QUANTITY TO THE "totalItems"
        # IF THERE IS NO OBJECT WITH THE ID THEN IT WONT TRY TO ADD IT TO THE "totalItems"
        while i <= iterationCount:
            try:
                currentObject = Equipment.objects.get(id=i)
                report.totalItems = report.totalItems + currentObject.quantity
                i = i + 1
            except:
                i = i + 1
                continue
        # TO FINALIZE THIS IT GETS SAVED
        report.save()

        # RETRIEVING CURRENT LOGGED IN USER AND PASSING IT TO "reservations.html"
        currentUser = request.user
        #-----------------------------------------------------------------------------------------------------
        equip_list = Equipment.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(equip_list, 6)
        
        try:
            equipments = paginator.page(page)
        except PageNotAnInteger:
            equipments = paginator.page(1)
        except EmptyPage:
            equipments = paginator.page(paginator.num_pages)

        return render(request, 'inventory/inventory.html', { 'equipments': equipments,  "currentUser" : currentUser} )

def detail(request, equipment_id):
    equipment = get_object_or_404(Equipment,pk=equipment_id)
    return render(request, 'inventory/detail.html', {'equipment':equipment})

#--(ADDIG THE "addProduct" VIEW)------------------------------------------------------------------------------
    # - RENDERS THE "addProduct.html" AND PASSES THE RANGE FUNCTION
def addProduct(request):
    return render(request, 'inventory/addProduct.html',{'range': range(100)})

#--(ADDIG THE "updateRECORD" VIEW)----------------------------------------------------------------------------
    # - A NEW ID IS GENERATED USING THE "largestID" WHICH STORES THE LAST ID NUMBER AND ADDS 1 TO IT
    # - RETRIEVES THE POSTED VALUE OF THE FORM FIELDS FROM THE "addProduct.html" FILE
    # - THESE VALUES ARE STORED IN VARIABLES AND THEN USED TO CREATE A NEW RECORD FOR THE "Equipment" TABLE
    # - THE CHANGES ARE SAVED AND REDIRECTS THE USER TO THE INVENTORY
# REFERENCE: https://www.w3schools.com/django/django_add_record.php
def addRecord(request):
    largestID = Equipment.objects.latest("id").id
    generatedID = largestID + 1
    displayName = request.POST["displayName"]
    assetType = request.POST["assetType"]
    location = request.POST["location"]
    quantity = request.POST["quantity"]
    equipment = Equipment(generatedID, displayName, assetType, location, quantity)
    equipment.save()
    return HttpResponseRedirect(reverse("inventory"))

#--(ADDIG THE "editProduct" VIEW)-----------------------------------------------------------------------------
    # - RETRIEVES THE SELECTED EQUIPMENT USING ITS ID,
    # - RENDERS THE "editProduct.html" AND PASSES THE SELECTED EQUIPMENT AND A RANGE FUNCTION
def editProduct(request, id):
    equipment = Equipment.objects.get(id=id)
    return render(request, 'inventory/editProduct.html',{'equipment': equipment, 'range': range(100)})

#--(ADDIG THE "updateRECORD" VIEW)----------------------------------------------------------------------------
    # - RETRIEVES THE POSTED VALUE OF THE FORM FIELDS FROM THE "editProduct.html" FILE
    # - THESE VALUES ARE STORED IN VARIABLES
    # - CREATES AN "equipment" OBJECT THAT STORES THE SELECTED EQUIPMENT USING ITS ID
    # - THE SELECTED EQUIPMENTS INFO IS CHANGED TO THE NEW PROVIDED INFO
    # - SAVES THE EQUIPMENT
    # - IT REDIRECTS THE USER TO THE ORIGINAL PAGE OF THE INVENTORY
# REFERENCE: https://www.w3schools.com/django/django_update_record.php
def updateRecord(request, id):
    new_name = request.POST['new_name']
    new_asset_type = request.POST['new_asset_type']
    new_location = request.POST['new_location']
    new_quantity = request.POST['new_quantity']
    equipment = Equipment.objects.get(id = id)
    equipment.display_name = new_name
    equipment.asset_type = new_asset_type
    equipment.location = new_location
    equipment.quantity = new_quantity
    equipment.save()
    return HttpResponseRedirect(reverse('inventory'))


#--(DELETING PRODUCTS:)---------------------------------------------------------------------------------------
    # - RETRIEVING THE SELECTED PRODUCT
    # - DELETING THE SELECTED PRODUCT AND REDIRECTING THE USER TO THE "inventory" PAGE
# REFERENCE: https://www.w3schools.com/django/django_delete_record.php
def removeProduct(request, id):
    itemToDelete = Equipment.objects.get(id=id)
    itemToDelete.delete()
    return HttpResponseRedirect(reverse("inventory"))