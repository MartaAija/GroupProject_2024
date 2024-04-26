from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ReservationDetails, Equipment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

def reservations(request):
    # RETRIEVING CURRENT LOGGED IN USER AND PASSING IT TO "reservations.html"
    currentUser = request.user
    return render(request, 'reservations.html', { "currentUser" : currentUser })

@login_required
def reservation_status(request):
    if request.method == 'POST':
        # Handle the POST request to create a reservation
        cart_items = request.session.get('cart_items', {})
        for equipment_id, item in cart_items.items():
            quantity_key = f'quantity_{equipment_id}'
            quantity = item.get('quantity', 1)  # Default quantity is 1
            equipment = Equipment.objects.get(id=equipment_id)
            ReservationDetails.objects.create(
                equipment=equipment,
                quantity=quantity,
                user=request.user  # Assign the reservation to the logged-in user
            )
        request.session.pop('cart_items', None)
        return redirect('reservation_status')

    # Retrieve the currently logged-in user and their hidden reservations
    user = request.user
    hidden_reservations = request.session.get('hidden_reservations', [])
    hidden_reservations = [int(reservation_id) for reservation_id in hidden_reservations]
    
    # Filter reservations based on the currently logged-in user
    all_reservations = ReservationDetails.objects.filter(user=user)\
        .exclude(status__in=[ReservationDetails.CANCELLED, ReservationDetails.COMPLETED])\
        .exclude(id__in=hidden_reservations)
    not_approved_reservations = all_reservations.filter(status=ReservationDetails.NOT_APPROVED)
    
    # Pagination
    items_per_page = 3
    paginator = Paginator(all_reservations, items_per_page)
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)

    #----------------------------------------------------------------------------------------------
    # GET CURRENT DATE AND TIME FOR RETURN VALIDATION
    currentDateAndTime = datetime.now().strftime("%Y-%m-%d")
    #----------------------------------------------------------------------------------------------
    
    return render(request, 'reservation_status.html', {'reservations': reservations, 'not_approved_reservations': not_approved_reservations, 'hidden_reservations': hidden_reservations, "currentDateAndTime" : currentDateAndTime})

@login_required
def reservation_history(request):
    # Retrieve the currently logged-in user
    user = request.user
    
    # Filter history reservations based on the currently logged-in user
    all_history_reservations = ReservationDetails.objects.filter(user=user, status__in=[ReservationDetails.CANCELLED, ReservationDetails.NOT_APPROVED, ReservationDetails.COMPLETED])
    
    # Pagination
    items_per_page = 3
    paginator = Paginator(all_history_reservations, items_per_page)
    page_number = request.GET.get('page')
    history_reservations = paginator.get_page(page_number)
    
    return render(request, 'reservation_history.html', {'history_reservations': history_reservations})

def view_booking_cart(request):
    cart_items = request.session.get('cart_items', {})
    equipment_ids = cart_items.keys()
    cart_item_objects = Equipment.objects.filter(id__in=equipment_ids)
    cart_item_details = {}

    # Paginate the list of cart items
    paginator = Paginator(cart_item_objects, 4)  # Change 10 to the desired number of items per page
    page_number = request.GET.get('page')
    cart_items_page = paginator.get_page(page_number)

    for item_obj in cart_items_page:
        item_id = str(item_obj.id)
        quantity = cart_items[item_id]['quantity'] if item_id in cart_items else 1
        cart_item_details[item_id] = {
            'id': item_obj.id,
            'name': item_obj.display_name,
            'type': item_obj.asset_type,
            'quantity': quantity,
            'available_stock': range(1, item_obj.quantity + 1)
        }

    return render(request, 'booking_cart.html', {'cart_items': cart_item_details, 'cart_items_page': cart_items_page})

def add_to_cart(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('equipment_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if equipment_id:
            cart_items = request.session.get('cart_items', {})
            
            if equipment_id in cart_items:
                return JsonResponse({'added': False})  # Item already in cart
            else:
                equipment = get_object_or_404(Equipment, id=equipment_id)
                cart_items[equipment_id] = {
                    'name': equipment.display_name,
                    'type': equipment.asset_type,
                    'quantity': quantity
                }
                request.session['cart_items'] = cart_items
                return JsonResponse({'added': True})  # Item added to cart
                
    return redirect('inventory')

def rebook_item(request, reservation_id):
    # Retrieve the reservation object based on the reservation ID
    reservation = get_object_or_404(ReservationDetails, id=reservation_id)
    
    # Retrieve the equipment details from the reservation
    equipment = reservation.equipment
    
    # Check if the equipment is already in the shopping cart
    cart_items = request.session.get('cart_items', {})
    if str(equipment.id) in cart_items:
        # If the equipment is already in the shopping cart, redirect back to history page with already_in_cart parameter
        return HttpResponseRedirect(reverse('reservation_history') + '?already_in_cart=true')

    # Add the equipment to the shopping cart
    cart_items[str(equipment.id)] = {
        'name': equipment.display_name,
        'type': equipment.asset_type,
        'quantity': reservation.quantity
    }
    request.session['cart_items'] = cart_items
    
    # Redirect back to the history page with a parameter indicating the rebooking action
    return HttpResponseRedirect(reverse('reservation_history') + '?rebooked=true')

def update_cart_item(request, equipment_id):
    if request.method == 'POST':
        cart_items = request.session.get('cart_items', {})
        new_quantity_str = request.POST.get('quantity')
        
        if new_quantity_str:
            new_quantity = int(new_quantity_str)
            cart_item = cart_items.get(str(equipment_id))
            
            if cart_item:
                cart_item['quantity'] = new_quantity
                request.session['cart_items'] = cart_items
                
    return redirect('view_booking_cart')

def remove_from_cart(request, equipment_id):
    if request.method == 'POST':
        cart_items = request.session.get('cart_items', {})
        
        if str(equipment_id) in cart_items:
            del cart_items[str(equipment_id)]
            request.session['cart_items'] = cart_items
            
    return redirect('view_booking_cart')

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(ReservationDetails, id=reservation_id)
    
    if request.method == 'POST':
        if reservation.status == ReservationDetails.PENDING:
            reservation.status = ReservationDetails.CANCELLED
            reservation.save()
            return redirect('reservation_history')
        
    return redirect('reservation_status')

def remove_not_approved(request, reservation_id):
    # Exclude the reservation permanently by adding its ID to the session
    hidden_reservations = request.session.get('hidden_reservations', [])
    hidden_reservations.append(reservation_id)
    request.session['hidden_reservations'] = hidden_reservations
    return redirect('reservation_status')

#--------------------------------------------------------------------------------------------------
# RETURNS THE "manageBookings.html" FILE TO BE RENDERED ON THE SCREEN WITH CORRECT OBJECTS FROM THE "ReservationDetails" TABLE
def manageBookings(request):
    reservationDetail_list = ReservationDetails.objects.all()
    equipments = Equipment.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(reservationDetail_list, 5)
        
    try:
        reservationDetails = paginator.page(page)
    except PageNotAnInteger:
        reservationDetails = paginator.page(1)
    except EmptyPage:
        reservationDetails = paginator.page(paginator.num_pages)

    # RETRIEVING CURRENT LOGGED IN USER AND PASSING IT TO "reservations.html"
    currentUser = request.user
    return render(request, "manageBookings.html", {"reservationDetails" : reservationDetails, "equipments" : equipments, "currentUser" : currentUser})
#--------------------------------------------------------------------------------------------------
# USING THE PROVIDED ID (CHOSEN ITEM) IT RETURNS THE "editStatus.html" FILE TO RENDER WITH THE SELECTED ITEMS INFO
def editStatus(request, id):
    reservationDetail = ReservationDetails.objects.get(id=id)
    equipments = Equipment.objects.all()
    currentUser = request.user
    return render(request, 'editStatus.html', {'reservationDetail': reservationDetail, "equipments" : equipments, "currentUser" : currentUser})
#--------------------------------------------------------------------------------------------------
# THIS FUNCTION UPDATES THE STATUS OF THE BOOKING IN "ReservationDetails" TABLE ACORDING THE CHANGES THE ADMIN MADE
def updateStatus(request, id):
    statusUpdate = request.POST["statusUpdate"]
    reservationDetail = ReservationDetails.objects.get(id=id)
    reservationDetail.status = statusUpdate
    reservationDetail.save()
    return HttpResponseRedirect(reverse("reservations"))