from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from .models import Booking, Refund
from datetime import datetime
from django.db.models import Sum
from .models import Refund
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import os
from amadeus import Client, ResponseError, Location
import amadeus
from amadeus import Client as AmadeusClient
import logging

# Configure logging
logger = logging.getLogger(__name__)
    
CLIENT_ID = os.environ.get('AMADEUS_CLIENT_ID','')
CLIENT_SECRET_ID = os.environ.get('AMADEUS_CLIENT_SECRET','')

amadeus = Client(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET_ID
)

def get_location_suggestions(request):
    keyword = request.GET.get('keyword', '')
    amadeus = AmadeusClient(
        client_id=os.environ.get('AMADEUS_CLIENT_ID', ''),
        client_secret=os.environ.get('AMADEUS_CLIENT_SECRET', '')
    )

    try:
        response = amadeus.reference_data.locations.get(keyword=keyword, subType='CITY')

        locations = []
        for location in response.data:
            locations.append({
                'name': location['name'],
                'iataCode': location['iataCode'],
                'cityName': location['address']['cityName'],
                'airportName': location['name']
            })

        return JsonResponse({'locations': locations})
    except Exception as e:
        return JsonResponse({'error': str(e)})



def flight_results(request):
    if request.method == 'GET':
        # Get form data
        from_location = request.GET.get('fromLocation')
        to_location = request.GET.get('toLocation')
        departure_date = request.GET.get('departureDate')

        # Query Amadeus for flight data
        try:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=from_location,
                destinationLocationCode=to_location,
                departureDate=departure_date
            )
            # Store the response as JSON format
            response_json = json.dumps(response.data)
            # Pass the stringified JSON data to the template
            return render(request, 'result.html', {'flights': response_json})
        except ResponseError as error:
            return render(request, 'error.html', {'error': error})
    else:
        return render(request, 'result.html')  # Render an empty template for other request methods
    
# def flight_results(request):
#     from_location = request.GET.get('fromLocation', '')
#     to_location = request.GET.get('toLocation', '')
#     departure_date = request.GET.get('departureDate', '')
#     return_date = request.GET.get('returnDate', '')
#     trip_type = request.GET.get('tripType', 'roundTrip')
#     flight_class = request.GET.get('flightClass', 'economy')
#     passenger_count = request.GET.get('passengerCount', '1')

#     amadeus = AmadeusClient(
#         client_id=os.environ.get('AMADEUS_CLIENT_ID', ''),
#         client_secret=os.environ.get('AMADEUS_CLIENT_SECRET', '')
#     )

#     try:
#         response = amadeus.shopping.flight_offers_search.get(
#             originLocationCode=from_location,
#             destinationLocationCode=to_location,
#             departureDate=departure_date,
#             returnDate=return_date if trip_type == 'roundTrip' else None,
#             adults=int(passenger_count),
#             travelClass=flight_class
#         )

#         flights = response.data
#         print(flights)  # For debugging purposes

#         # Convert flights data to JSON format
#         flights_json = json.dumps(flights)

#         return render(request, 'result.html', {'flights_json': flights_json})
#     except Exception as e:
#         return render(request, 'result.html', {'error': str(e)})

def flight_book(request):
    # Total sales
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    total_sales = confirmed_bookings.aggregate(total_sales=Sum('price'))['total_sales'] or 0

    # Monthly income
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    monthly_income = Booking.objects.filter(departure_date__month=current_month, departure_date__year=current_year, status='confirmed').aggregate(monthly_income=Sum('price'))['monthly_income'] or 0

    # Annual income
    annual_income = Booking.objects.filter(departure_date__year=current_year, status='confirmed').aggregate(annual_income=Sum('price'))['annual_income'] or 0
    userN = request.session.get('userN')
    context = {
        'total_sales': total_sales,
        'monthly_income': monthly_income,
        'annual_income': annual_income,
        'user' : userN
    }
    
    return render(request, "base.html", context)

from decimal import Decimal

def total_booking(request):
    original = Booking.objects.filter(status__in=['inprocess', 'rejected', 'confirmed', 'cancelled'])
    confirmed_bookings = original.filter(status='confirmed')

    total_price = Decimal(0.0)
    total_mco = Decimal(0.0)
    for booking in confirmed_bookings:
        total_price += Decimal(booking.price)
        total_mco += Decimal(booking.mco)
    
    total_revenue = total_price + total_mco
    total_price_str = "${:.2f}".format(total_price)  # Formatting total price as a string
    total_mco_str = "${:.2f}".format(total_mco)  # Formatting total MCO as a string
    total_revenue_str = "${:.2f}".format(total_revenue)  # Formatting total revenue as a string

    context = {
        "original": original,
        "length": original.count(),
        "total_price": total_price_str,
        "total_mco": total_mco_str,
        "total_revenue": total_revenue_str
    }
    return render(request, "total_booking.html", context)

# =================================================================================dashboard======================================

def dashboard(request):
    return render(request,'dashboard.html')
# =================================================================================end dashboard==================================

def total_user(request):
    user_data = User.objects.all()  # Fetch all User objects
    context = {
        "users": user_data,  # Rename the context variable to avoid confusion
    }
    return render(request, "total_users.html", context)

def booking(request):
    original = Booking.objects.all()
    context = {
        "original" : original
    }
    return render(request,"bookings.html", context)

def refund(request):
    refund_data = Refund.objects.all()
    booking_data = Booking.objects.all()
    context = {
        "refund": refund_data,
        "booking": booking_data
    }
    return render(request,"refunds.html",context)

def chargeback(request):
    return render(request,"chargeback.html")

def rejected(request):
    rejected_bookings = Booking.objects.filter(status='rejected')
    return render(request, "rejected.html", {'rejected_bookings': rejected_bookings})

def mco(request):
    mco = Booking.objects.filter(status='confirmed')
    context = {
        "mco": mco
    }
    return render(request, "mco.html", context)

def cancellation(request):
    cancelled_bookings = Booking.objects.filter(status='cancelled')
    context = {
        "cancel": cancelled_bookings
    }
    return render(request, "cancellation.html", context)


def ecredit(request):
    return render(request,"ecredit.html")

# ==============================================( update booking status )==================================================

from django.utils import timezone
from datetime import date
def update_booking_status(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        status = request.POST.get('status')
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            booking.status = status
            if status == 'rejected':
                booking.rejection_date = timezone.now()
                # booking.rejection_date = date.today()
            booking.save()

            if status == 'rejected':
                return redirect('crmApp:total_booking')
            elif status == 'confirmed':
                return redirect('crmApp:total_booking')
            elif status == 'inprocess':
                return redirect('crmApp:total_booking')
            elif status == 'cancelled':
                return redirect('crmApp:cancellation')
            else:
                return redirect('crmApp:booking')
        except Booking.DoesNotExist:
            # Handle case where the booking ID does not exist
            pass

    # Handle GET requests or any other scenario
    # You can redirect to another page or render a template
    return redirect('crmApp:booking')

# ==============================================( end update booking status )==================================================


# =============================================(retrieve customer name using booking id)==========================

def fetch_passenger_data(request):
    if request.method == 'GET':
        booking_id = request.GET.get('booking_id')
        passenger_name = request.GET.get('passenger_name')
        phone_number = request.GET.get('phone_number')
        email = request.GET.get('email')

        try:
            if booking_id:
                booking = Booking.objects.get(booking_id=booking_id)
                passenger_name = booking.passenger_name
                phone_number = booking.phone_number
                email = booking.email
            elif passenger_name or phone_number or email:
                # Construct a query with provided parameters
                query = Booking.objects.filter(
                    passenger_name=passenger_name,
                    phone_number=phone_number,
                    email=email
                )

                # Check if the query returned any results
                if not query.exists():
                    raise Booking.DoesNotExist

                booking = query.first()
                booking_id = booking.booking_id
            else:
                return JsonResponse({'error': 'Invalid request parameters'}, status=400)

            return JsonResponse({
                'booking_id': booking_id,
                'passenger_name': passenger_name,
                'phone_number': phone_number,
                'email': email
            })
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)




# =============================================(retrieve customer name using booking id)==========================


# =============================================(submit refund data)===============================================
        
@csrf_exempt
@require_POST
def submit_refund_form(request):
    if request.method == 'POST':
        # Get form data from the POST request
        booking_id = request.POST.get('bookingId')
        passenger_name = request.POST.get('passengerName')
        phone_number = request.POST.get('phoneNumber')
        email = request.POST.get('email')
        refund_type = request.POST.get('refundType')
        refund_amount = request.POST.get('refundAmount')
        refund_reason = request.POST.get('refundReason')

        # Retrieve the Booking object based on the booking_id
        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return HttpResponse("Invalid Booking ID", status=400)

        # Create a Refund object and save it to the database
        refund = Refund(
            booking=booking,
            passenger_name=passenger_name,
            phone_number=phone_number,
            email=email,
            refund_amount=refund_amount,
            refund_reason=refund_reason
        )
        refund.save()

        # Set a success message
        success_message = "Refund form submitted successfully"

        # Redirect back to the 'booking' page with the success message as a query parameter
        booking_url = reverse('crmApp:booking')  # Replace 'booking' with your actual URL name
        return redirect(f"{booking_url}?success_message={success_message}")

    return HttpResponse("Invalid request method", status=400)


# =============================================(submit refund data)===============================================


# ===========================================(update refund status)===============================================


def update_refund_status(request):
    if request.method == 'POST':
        refund_id = request.POST.get('refund_id')
        status = request.POST.get('status')
        
        try:
            refund = Refund.objects.get(id=refund_id)
            booking = refund.booking  # Assuming there's a foreign key field named 'booking' in the Refund model
            
            if refund.status != status:
                if status == 'confirmed':
                    # If status is changed to confirmed, update booking price
                    refund_amount = refund.refund_amount
                    updated_price = booking.price - refund_amount
                    booking.price = updated_price
                elif refund.status == 'confirmed':
                    # If status was confirmed and now changed back, revert booking price
                    refund_amount = refund.refund_amount
                    updated_price = booking.price + refund_amount
                    booking.price = updated_price
                
                refund.status = status
                refund.save()
                booking.save()

            # Redirect to the same page or any other appropriate page after updating the status
            return redirect('crmApp:refund')
        
        except Refund.DoesNotExist:
            # Handle cases where the refund doesn't exist
            pass
        except Booking.DoesNotExist:
            # Handle cases where the associated booking doesn't exist
            pass

    # Handle GET requests or any other scenario
    # You can redirect to another page or render a template
    return redirect('crmApp:refund')


# ==============================================End refund status ===============================================






# ===============================================test data fetch==================================================



# =================================================create user====================================================
from .models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password

@csrf_exempt
@require_http_methods(["GET", "POST"])
def create_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('userName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        role = request.POST.get('role')
        team = request.POST.get('team')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        else:
            # Hash the password
            hashed_password = make_password(password)

            # Create user instance
            new_user = User(
                user_name=user_name,
                email=email,
                phone_number=phone_number,
                role=role,
                team=team,
                password=hashed_password
            )
            try:
                # Save user to database
                new_user.save()
                messages.success(request, 'User created successfully')
            except Exception as e:
                # Handle any database or validation errors
                messages.error(request, f'Failed to create user: {str(e)}')

        return redirect('crmApp:create_user')  

    return render(request, 'total_users.html')


# ==========================================================login===============================

# from django.contrib.auth import authenticate, login

# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def login_view(request):
#     error_message = None
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         role = request.POST.get('role')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_superuser:
#                 if role == 'superuser':
#                     login(request, user)
#                     return redirect('crmApp:base')  # Redirect to base URL after successful login
#                 else:
#                     error_message = 'Invalid role for this user'
#             elif user.blocked:
#                 error_message = 'This user is blocked'
#             else:
#                 if role == 'manager' and user.role == 'manager':
#                     login(request, user)
#                     return redirect('crmApp:base')  # Redirect to base URL after successful login
#                 elif role == 'agent' and user.role == 'agent':
#                     login(request, user)
#                     return redirect('crmApp:base')  # Redirect to base URL after successful login
#                 else:
#                     error_message = 'Invalid role for this user'
#         else:
#             # Invalid login
#             error_message = 'Invalid username or password'
#     return render(request, 'login.html', {'error_message': error_message})

from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import User

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Check if the user is a superuser
        if role == 'superuser':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['userN'] = user.username
                print(request.session['userN'])
                return redirect('crmApp:dashboard')  # Redirect to base URL after successful login
            else:
                error_message = 'Invalid username or password'
        else:
            # Check if the user with specified role exists
            try:
                user = User.objects.get(user_name=username, role=role, password=password)
                if user.password == password:
                    if user.blocked:
                        error_message = 'This user is blocked'
                    else:
                        login(request, user)
                        request.session['userN'] = user.user_name
                        return redirect('crmApp:dashboard')  # Redirect to base URL after successful login
                else:
                    error_message = 'Invalid password'
            except User.DoesNotExist:
                error_message = 'User with specified role not found'

    return render(request, 'login.html', {'error_message': error_message})


# ==========================================================end login===============================
# =======================================logout===================

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('crmApp:login') 

#  ========================================end logout====================

# block user========================================================================================

def block_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.blocked = not user.blocked  # Toggle block status
    user.save()
    return redirect('crmApp:total_user')

# ==========================================================update users==========================
from django.http import HttpResponseRedirect
@csrf_exempt
@require_POST
def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('userName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        role = request.POST.get('role')
        team = request.POST.get('team')
        password = request.POST.get('password')

        try:
            # Retrieve the user instance from the database using user_id
            user = User.objects.get(pk=user_id)
            # Update user data
            user.user_name = user_name
            user.email = email
            user.phone_number = phone_number
            user.role = role
            user.team = team
            user.password = password
            # Save the updated user data
            user.save()
            return HttpResponseRedirect(reverse('crmApp:total_user') + '?success_message=User updated successfully.')
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('crmApp:total_user') + '?error_message=User not found.')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



# ==========================================================end update users==========================



# ==========================delete booking status==================
@csrf_exempt
@require_POST
def delete_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            if booking.status == 'cancelled':
                logger.info(f"Booking with ID {booking_id} is cancelled. Redirecting to cancellation.")
                booking.delete()
                return HttpResponseRedirect(reverse('crmApp:cancellation'))
            else:
                booking.delete()
                logger.info(f"Booking with ID {booking_id} is deleted.")
        except Booking.DoesNotExist:
            logger.warning(f"Booking with ID {booking_id} does not exist.")
    return redirect('crmApp:total_booking')
# ===============================end  delete booking status===================

# =========================================================( grant_permission)=============================================

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def grant_permissions(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)
        privileges = request.POST.getlist('privileges[]')
        # Here, you would implement your logic to update the user's permissions
        # For example, you might have a UserProfile model with a ManyToManyField for privileges
        # userProfile = UserProfile.objects.get(user=user)
        # userProfile.privileges.clear()
        # for privilege in privileges:
        #     userProfile.privileges.add(privilege)
        # Save the user profile or whatever logic you have
        
        messages.success(request, f'Permissions granted successfully for {user.username}')
        return redirect('some_redirect_view')  # Redirect to a success page or wherever you want to go after granting permissions
    else:
        return redirect('some_error_view')  # Redirect to an error page or handle it in your frontend

# Define other views as needed for your application

# ================================================================================end permission===============================