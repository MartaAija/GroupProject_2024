# AUTHORSHIP: MARTA ZIGURE (w1888516)
#   WORKED ON FILE:
#       - NOEL VARGA (w1932378) (Admin view aspects)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .models import ReservationDetails, Equipment
from django.contrib.auth.decorators import login_required
from datetime import datetime

def reservations(request):
    """
    Renders the 'reservations.html' template, passing the current user object as context.
    """
    currentUser = request.user
    return render(request, 'reservations.html', {"currentUser": currentUser})

@login_required
def reservation_status(request):
    """
    Handles the reservation status page logic:
    - Handles POST requests to create reservations from the booking cart.
    - Retrieves reservations based on the currently logged-in user, excluding certain statuses.
    - Paginates the list of reservations.
    - Retrieves the current date and time for return validation.
    """
    if request.method == 'POST':
        # Handle POST request to create reservations from the booking cart
        cart_items = request.session.get('cart_items', {})
        for equipment_id, item in cart_items.items():
            quantity_key = f'quantity_{equipment_id}'
            quantity = item.get('quantity', 1) 
            equipment = Equipment.objects.get(id=equipment_id)
            ReservationDetails.objects.create(
                equipment=equipment,
                quantity=quantity,
                user=request.user 
            )
        request.session.pop('cart_items', None)
        return redirect('reservation_status')

    # Retrieve reservations based on the currently logged-in user
    user = request.user
    hidden_reservations = request.session.get('hidden_reservations', [])
    hidden_reservations = [int(reservation_id) for reservation_id in hidden_reservations]
    
    all_reservations = ReservationDetails.objects.filter(user=user)\
        .exclude(status__in=[ReservationDetails.CANCELLED, ReservationDetails.COMPLETED])\
        .exclude(id__in=hidden_reservations)
    not_approved_reservations = all_reservations.filter(status=ReservationDetails.NOT_APPROVED)
    
    # Pagination
    items_per_page = 2
    paginator = Paginator(all_reservations, items_per_page)
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)

    currentDateAndTime = datetime.now().strftime("%Y-%m-%d")  # Get current date and time
    
    return render(request, 'reservation_status.html', {
        'reservations': reservations,
        'not_approved_reservations': not_approved_reservations,
        'hidden_reservations': hidden_reservations,
        "currentDateAndTime": currentDateAndTime
    })

@login_required
def reservation_history(request):
    """
    Handles the reservation history page logic:
    - Retrieves history reservations based on the currently logged-in user.
    - Paginates the list of history reservations.
    """
    user = request.user
    all_history_reservations = ReservationDetails.objects.filter(
        user=user, status__in=[ReservationDetails.CANCELLED, ReservationDetails.NOT_APPROVED, ReservationDetails.COMPLETED]
    )
    
    # Pagination
    items_per_page = 2
    paginator = Paginator(all_history_reservations, items_per_page)
    page_number = request.GET.get('page')
    history_reservations = paginator.get_page(page_number)
    
    return render(request, 'reservation_history.html', {'history_reservations': history_reservations})

@login_required
def view_booking_cart(request):
    """
    Handles rendering the booking cart page:
    - Retrieves cart items from the session.
    - Retrieves equipment details for each item.
    - Paginates the list of cart items.
    """
    cart_items = request.session.get('cart_items', {})
    equipment_ids = cart_items.keys()
    cart_item_objects = Equipment.objects.filter(id__in=equipment_ids)
    cart_item_details = {}

# Pagination
    paginator = Paginator(cart_item_objects, 3)  
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

@login_required
def add_to_cart(request):
    """
    Handles adding items to the booking cart:
    - Handles POST requests to add items to the session-based booking cart.
    - Checks if the equipment quantity is greater than zero before adding to cart.
    - Displays a prompt if the item is not added due to zero quantity.
    """
    if request.method == 'POST':
        equipment_id = request.POST.get('equipment_id')
        quantity = int(request.POST.get('quantity', 1))

        if equipment_id:
            equipment = get_object_or_404(Equipment, id=equipment_id)

            if equipment.quantity <= 0:
                # Item is unavailable due to zero quantity
                return JsonResponse({'added': False, 'unavailable': True})

            cart_items = request.session.get('cart_items', {})
            if equipment_id in cart_items:
                # Item is already in the cart
                return JsonResponse({'added': False})

            # Add item to cart
            cart_items[equipment_id] = {
                'name': equipment.display_name,
                'type': equipment.asset_type,
                'quantity': quantity
            }
            request.session['cart_items'] = cart_items
            return JsonResponse({'added': True})

    # Redirect to inventory page if not a POST request or invalid equipment ID
    return redirect('inventory')

@login_required
def rebook_item(request, reservation_id):
    """
    Handles rebooking a reservation:
    - Retrieves the reservation based on the reservation ID.
    - Checks if the associated equipment is available for rebooking.
    - Adds the equipment to the booking cart if available; otherwise, displays an error message.
    """
    reservation = get_object_or_404(ReservationDetails, id=reservation_id)
    equipment = reservation.equipment
    
    if equipment.quantity > 0:
        cart_items = request.session.get('cart_items', {})
        if str(equipment.id) in cart_items:
            return HttpResponseRedirect(reverse('reservation_history') + '?already_in_cart=true')

        cart_items[str(equipment.id)] = {
            'name': equipment.display_name,
            'type': equipment.asset_type,
            'quantity': reservation.quantity
        }
        request.session['cart_items'] = cart_items
        return HttpResponseRedirect(reverse('reservation_history') + '?rebooked=true')
    else:
        return HttpResponseRedirect(reverse('reservation_history') + '?unavailable_to_rebook=true')

@login_required
def update_cart_item(request, equipment_id):
    """
    Handles updating items in the booking cart:
    - Handles POST requests to update quantities of items in the booking cart.
    """
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

@login_required
def remove_from_cart(request, equipment_id):
    """
    Handles removing items from the booking cart:
    - Handles POST requests to remove items from the session-based booking cart.
    """
    if request.method == 'POST':
        cart_items = request.session.get('cart_items', {})
        
        if str(equipment_id) in cart_items:
            del cart_items[str(equipment_id)]
            request.session['cart_items'] = cart_items
            
    return redirect('view_booking_cart')

@login_required
def cancel_reservation(request, reservation_id):
    """
    Handles canceling a reservation:
    - Retrieves the reservation based on the reservation ID.
    - Cancels the reservation if it is pending.
    """
    reservation = get_object_or_404(ReservationDetails, id=reservation_id)
    
    if request.method == 'POST':
        if reservation.status == ReservationDetails.PENDING:
            reservation.status = ReservationDetails.CANCELLED
            reservation.save()
            return redirect('reservation_history')
        
    return redirect('reservation_status')

@login_required
def remove_not_approved(request, reservation_id):
    """
    Handles permanently removing a not-approved reservation from view:
    - Adds the reservation ID to the hidden_reservations session list.
    """
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