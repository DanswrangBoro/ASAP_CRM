from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
import requests
import os
from django.http import FileResponse
from .models import APIRequest, AdditionCharge, Booking, Center, Payment, Plans, Refund, Validity
from datetime import datetime, timedelta
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
from .models import Sale
from django.db.models import Sum
from .models import Chargeback,Center
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from .models import Invoice
import uuid
import random
from django.core.serializers import serialize
from pprint import pprint
from django.core.files.storage import FileSystemStorage
from dropbox_sign import \
    ApiClient, ApiException, Configuration, apis, models

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.sessions.models import Session

configuration = Configuration(
    # Configure HTTP basic authorization: api_key
    username="8b0a24b667d452502026dde34a7e83e7dc821a6a6e935df11f2af2bbe023ad39",

    # or, configure Bearer (JWT) authorization: oauth2
    # access_token="YOUR_ACCESS_TOKEN",
)


logger = logging.getLogger(__name__)
    
CLIENT_ID = os.environ.get('AMADEUS_CLIENT_ID','')
CLIENT_SECRET_ID = os.environ.get('AMADEUS_CLIENT_SECRET','')

amadeus = Client(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET_ID
)

@receiver(post_migrate)
def create_main_center(sender, **kwargs):
    if sender.name == get_user_model()._meta.app_label:
        main_center, created = Center.objects.get_or_create(
            name='Main',
            email='',
            address='',
            phone='',
            contact_person='Admin',
            status='active'
        )
        if created:
            print('Main center created successfully.')



def get_location_suggestions(request):
    print("inside this ")
    keyword = request.GET.get('keyword', '')
    amadeus = AmadeusClient(
        client_id=os.environ.get('AMADEUS_CLIENT_ID', ''),
        client_secret=os.environ.get('AMADEUS_CLIENT_SECRET', '')
    )

    try:
        response = amadeus.reference_data.locations.get(keyword=keyword, subType='AIRPORT')
        term = "location and iataCode"
        requestCounter(request.user.center,term)
        print(response)
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
        from_location = request.GET.get('from')
        to_location = request.GET.get('to')
        departure_date = request.GET.get('departureDate')
        return_date = request.GET.get('returnDate')
        print("return",return_date)
        adults = request.GET.get('adult')
        child = request.GET.get('child')
        infants = request.GET.get('infant')
        class_type = request.GET.get('flightClass')

        print("From Location:", from_location)
        print("To Location:", to_location)
        print("Departure Date:", departure_date)
        print("Adults:", adults)
        print("Child:", child)
        print("Infants:", infants)
        print("Class Type:", class_type)

        # Query Amadeus for flight data
        try:
            print("inside try")
            if return_date == "":
                response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=from_location,
                destinationLocationCode=to_location,
                departureDate=departure_date,
                adults=adults,
                children=child,
                infants=infants,
                travelClass=class_type
                ).data
                term = "one way flight search"
                requestCounter(request.user.center,term)
                # Store the response as JSON format
                context = {
                    "flights" : response,
                    "flights1" : json.dumps(response),

                }
                file_path = "temp.txt"
                with open(file_path, "w") as file:
                    json.dump(context, file, indent= 4)
                # with open(file_path, "r") as file:
                #     context = json.load(file)
                return render(request, 'result1.html', context)

            else:
                response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=from_location,
                destinationLocationCode=to_location,
                departureDate=departure_date,
                adults=adults,
                children=child,
                infants=infants,
                travelClass=class_type
                ).data
                term = "round trip"
                requestCounter(request.user.center,term)
                response_return = amadeus.shopping.flight_offers_search.get(
                originLocationCode=to_location,
                destinationLocationCode=from_location,
                departureDate=return_date,
                adults=adults,
                children=child,
                infants=infants,
                travelClass=class_type
                ).data
                requestCounter(request.user.center,term)

                # Store the response as JSON format
                context = {
                    "flights_departure" : response,
                    "flights_return": response_return,
                    "flights_departure1" : json.dumps(response),
                    "flights_return1" : json.dumps(response_return),
                }
                print(context)
                file_path = "round.txt"
                with open(file_path, "w") as file:
                    json.dump(context, file, indent= 4)
                # with open(file_path, "r") as file:
                #     context = json.load(file)
            # Pass the stringified JSON data to the template
            # print(context)
                return render(request, 'roundtrip.html', context)
        except ResponseError as error:
            # print(error["error"])
            return render(request, 'error.html', {'error': error.response.result["errors"]})
    else:
        return render(request, 'result1.html')
    
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

# def flight_book(request):
#     return render(request, "base.html")

from decimal import Decimal

from django.db.models import Case, Value, When

def total_booking(request):
    if request.user.is_superuser:
        original = Booking.objects.filter(status__in=['inprocess', 'rejected', 'confirmed', 'cancelled'])
        agents = CustomUser.objects.filter(role='agent')
        confirmed_bookings = original.filter(status='confirmed')

        total_price = Decimal(0.0)
        total_mco = Decimal(0.0)
        for booking in confirmed_bookings:
            total_price += Decimal(booking.price)
        
        total_revenue = total_price + total_mco
        # Rounding to two decimal points
        total_price_str = "${:.2f}".format(round(total_price, 2))
        total_mco_str = "${:.2f}".format(round(total_mco, 2))
        total_revenue_str = "${:.2f}".format(round(total_revenue, 2))

        context = {
            "original": original,
            "length": original.count(),
            "total_price": total_price_str,
            "total_mco": total_mco_str,
            "total_revenue": total_revenue_str,
            "agents": agents
        }
        return render(request, "total_booking.html", context)
    else:
        original = Booking.objects.filter(status__in=['inprocess', 'rejected', 'confirmed', 'cancelled'], center=request.user.center)
        # Reorder queryset to place entries with center name "Main" at the top
        original = original.annotate(
            is_main=Case(
                When(center__name='Main', then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField(),
            )
        ).order_by('-is_main')
        
        agents = CustomUser.objects.filter(role='agent')
        confirmed_bookings = original.filter(status='confirmed')

        total_price = Decimal(0.0)
        total_mco = Decimal(0.0)
        for booking in confirmed_bookings:
            total_price += Decimal(booking.price)
        
        total_revenue = total_price + total_mco
        # Rounding to two decimal points
        total_price_str = "${:.2f}".format(round(total_price, 2))
        total_mco_str = "${:.2f}".format(round(total_mco, 2))
        total_revenue_str = "${:.2f}".format(round(total_revenue, 2))

        context = {
            "original": original,
            "length": original.count(),
            "total_price": total_price_str,
            "total_mco": total_mco_str,
            "total_revenue": total_revenue_str,
            "agents": agents
        }
        return render(request, "total_booking.html", context)



# =================================================================================dashboard======================================

def format_price(price):
    if price >= 1000:
        return "${:.1f}K".format(price / 1000)
    else:
        return "${:.2f}".format(price)

def dashboard(request):
    # Total sales
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    total_sales = confirmed_bookings.aggregate(total_sales=Sum('price'))['total_sales'] or 0
    total_sales_str = format_price(total_sales)

    # Monthly income
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    monthly_income = Booking.objects.filter(departure_date__month=current_month, departure_date__year=current_year, status='confirmed').aggregate(monthly_income=Sum('price'))['monthly_income'] or 0
    monthly_income_str = format_price(monthly_income)

    # Annual income
    annual_income = Booking.objects.filter(departure_date__year=current_year, status='confirmed').aggregate(annual_income=Sum('price'))['annual_income'] or 0
    annual_income_str = format_price(annual_income)

    userN = request.session.get('userN')
    pending_chargebacks = Chargeback.objects.filter(chargeback_lead_status='pending')

    context = {
        'total_sales': total_sales_str,
        'monthly_income': monthly_income_str,
        'annual_income': annual_income_str,
        'user': userN,
        'pending_chargebacks': pending_chargebacks,
    }
    return render(request, 'dashboard.html', context)

# =================================================================================end dashboard==================================


def total_user(request):
    if request.user.is_superuser:
        user_data = CustomUser.objects.all()  # Fetch all User objects
        centers = Center.objects.all()  # Fetch all Center objects
        form = UserCreationForm()
        context = {
            "users": user_data,  # Rename the context variable to avoid confusion
            'form': form,
            'centers': centers,  # Pass the centers data to the template context
        }
        return render(request, "total_users.html", context)
    elif request.user.role == 'manager':
        print(request.user.center.pk)
        # center = get_object_or_404(Center,pk = request.user.center.pk)
        user_data = CustomUser.objects.filter(center = request.user.center.pk)  # Fetch all User objects
        print(user_data)
        centers = Center.objects.filter(pk = request.user.center.pk)
        form = UserCreationForm()
        context = {
            "users": user_data,  # Rename the context variable to avoid confusion
            'form': form,
            'centers': centers,  # Pass the centers data to the template context
        }
        return render(request, "total_users.html", context)


def sales_view(request):
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    print(confirmed_bookings)
    context = {
        'sale_data': confirmed_bookings
    }

    return render(request, 'sales.html', context)

def booking(request):
    user_center = request.user.center

    # Check if the user's center is a main center
    if user_center.name == 'Main':
        original = Booking.objects.filter(center=user_center)
        context = {
            "original": original
        }
        return render(request, "bookings.html", context)
    else:
        original = Booking.objects.filter(center=user_center)
        exp = get_object_or_404(Validity, center=user_center)
        context = {
            "original": original,
            "exp": exp
        }
        return render(request, "bookings.html", context)

def refund(request):
    refund_data = Refund.objects.all()
    context = {
        "refund": refund_data,
    }
    return render(request,"refunds.html",context)

from django.http import JsonResponse

def book_view(request):
    if request.method == 'GET' and 'booking_id' in request.GET:
        booking_id = request.GET['booking_id']
        # Retrieve relevant data based on the booking ID
        # For example:
        booking = Booking.objects.get(id=booking_id)
        data = {
            'passenger_name': booking.passenger_name,
            'phone_number': booking.phone_number,
            # Add other relevant fields here
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request'})


def chargeback(request):
    chargebacks = Chargeback.objects.all()
    highest_chargebacks = Chargeback.objects.order_by('-Booking__price')[:5]
    total_chargeback_amount = chargebacks.aggregate(
        total_chargeback=Sum('Booking__price')
    )['total_chargeback']
    return render(request, "chargeback.html", {'chargebacks': chargebacks, 'highest_chargebacks': highest_chargebacks, 'total_chargeback_amount': total_chargeback_amount})

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from django.utils import timezone

@login_required
def update_booking_status(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        status = request.POST.get('status')
        
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            
            if status == 'inprocess':
                # Check if the logged-in user's role is 'agent', 'manager', or is a superuser
                if request.user.role in ['agent', 'manager'] or request.user.is_superuser:
                    # Assign the currently logged-in user as the lead agent
                    booking.lead_agent = request.user
                else:
                    messages.error(request, 'You do not have permission to update this booking status.')
                    return redirect('crmApp:total_booking')
            
            booking.status = status
            booking.change_date = timezone.now()
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
            messages.error(request, 'The booking does not exist.')
            return redirect('crmApp:sales')

    # Handle GET requests or any other scenario
    # You can redirect to another page or render a template
    return redirect('crmApp:sales')


# ==============================================( end update booking status )==================================================
def reassign_lead_agent(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        print(booking_id)
        new_lead_agent_id = request.POST.get('lead_agent')

        # Fetch booking object
        booking = Booking.objects.get(booking_id=booking_id)

        # Update lead agent
        booking.lead_agent_id = new_lead_agent_id
        booking.save()

        # Redirect to some page or return a response
        return redirect('crmApp:total_booking')  # Adjust the URL name as per your project

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
        refund_type = request.POST.get('refundType')
        refund_amount = request.POST.get('refundAmount')
        refund_reason = request.POST.get('refundReason')

        # Retrieve the Booking object based on the booking_id
        try:
            booking = Booking.objects.get(booking_id=booking_id)
                # Create a Refund object and save it to the database
            refund = Refund(
                booking_id=booking,
                refund_amount=refund_amount,
                refund_type = refund_type,
                refund_reason=refund_reason
            )
            refund.save()

            # Set a success message
            success_message = "Refund form submitted successfully"
        except Booking.DoesNotExist:
            return HttpResponse("Invalid Booking ID", status=400)

     

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
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password

# @csrf_exempt
# @require_http_methods(["GET", "POST"])
# def create_user(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('userName')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phoneNumber')
#         role = request.POST.get('role')
#         team = request.POST.get('team')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirmPassword')

#         # Check if passwords match
#         if password != confirm_password:
#             messages.error(request, 'Passwords do not match')
#         else:
#             # Hash the password
#             hashed_password = make_password(password)

#             # Create user instance
#             new_user = Person(
#                 user_name=user_name,
#                 email=email,
#                 phone_number=phone_number,
#                 role=role,
#                 team=team,
#                 password=hashed_password
#             )
#             try:
#                 # Save user to database
#                 new_user.save()
#                 messages.success(request, 'User created successfully')
#             except Exception as e:
#                 # Handle any database or validation errors
#                 messages.error(request, f'Failed to create user: {str(e)}')

#         return redirect('crmApp:create_user')  

#     return render(request, 'total_users.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserCreationForm
from .models import CustomUser

from django.contrib import messages

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            phoneNumber = form.cleaned_data['phoneNumber']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirmPassword']
            center = form.cleaned_data['center']  # Get the selected center from the form

            print("Email:", email)
            print("Username:", username)
            print("Phone Number:", phoneNumber)
            print("Role:", role)
            print("Password:", password)
            print("Confirm Password:", confirm_password)
            print("Center:", center)

            if password == confirm_password:
                user = CustomUser.objects.create_user(email=email, username=username, phoneNumber=phoneNumber, role=role,password=password)
                user.center = center  # Assign the selected center to the user
                user.save()
                messages.success(request, "User created successfully!")
                return redirect('crmApp:total_user')
            else:
                messages.warning(request, "Password does not match!")
                return redirect('crmApp:total_user')
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
            messages.warning(request, "Form is not valid!")
            return redirect('crmApp:total_user')
    return redirect('crmApp:total_user')



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
from django.shortcuts import render, redirect
# from .models import Custom  # Import your custom user model

def login_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # Redirect to the dashboard if the user is already logged in
        return redirect('crmApp:dashboard')

    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        active_sessions = Session.objects.all()
        for active in active_sessions:
            print("Session data before authentication:", active.get_decoded())
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            active_sessions = Session.objects.all()
            for active in active_sessions:
                print("Session data before authentication:", active.get_decoded())
            if not user.blocked:  # Check if user is not blocked
                login(request, user)  # Django will handle session management
                return redirect('crmApp:dashboard')  # Redirect to base URL after successful login
            else:
                error_message = 'This user is blocked'
        else:
            error_message = 'Invalid username or password'

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
    user = CustomUser.objects.get(pk=user_id)
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
            user = CustomUser.objects.get(pk=user_id)
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
        except CustomUser.DoesNotExist:
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

# =========================================================( invoice )=============================================


# ================================================================================(end invoice)===============================

def lead_agent_and_price(request):
    try:
        # Retrieve confirmed bookings
        confirmed_bookings = Booking.objects.filter(status='confirmed')

        lead_agents_and_prices = []
        for booking in confirmed_bookings:
            lead_agents_and_prices.append({
                'agent': booking.lead_agent,
                'sale_date': booking.booking_date,
                'amount': booking.price
                # Add other fields as needed
            })

        context = {
            'lead_agents_and_prices': lead_agents_and_prices
        }

        return render(request, 'your_template.html', context)
    except Exception as e:
        messages.error(request, f'Error occurred: {str(e)}')
        return render(request, 'error_template.html')
    
    # =====================================================================agent data=========================

from django.http import JsonResponse

def get_agent_data(request):
    username = request.POST.get('username')
    
    # Retrieve the agent object based on the provided username
    try:
        agent = CustomUser.objects.get(username=username)
        
        # Filter the bookings for the agent where status is 'confirmed'
        confirmed_bookings = Booking.objects.filter(
            lead_agent=agent,  # Filter by lead_agent matching the agent
            status='confirmed'  # Filter by status being 'confirmed'
        )
        
        # Aggregate the total price of confirmed bookings
        total_price = confirmed_bookings.aggregate(total_price=Sum('price'))['total_price'] or 0
        
        # Print the total price for testing
        print('Total Price:', total_price)
        
        # Return the total price as a JSON response
        return JsonResponse({'total_price': total_price})
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Agent not found'}, status=404)



# ==================================================================================end agent data================================
    
# views.py

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse

# def generate_invoice(request):
#     # Retrieve all invoices and their associated addition charges
#     invoices = Invoice.objects.all().select_related('booking')
#     for invoice in invoices:
#         invoice.addition_charges = list(invoice.additioncharge_set.all())

#     # Serialize the invoices to JSON
#     invoices_json = serialize('json', invoices, use_natural_foreign_keys=True, use_natural_primary_keys=True)

#     # Pass the retrieved data to the template context
#     context = {
#         'invoices': invoices,
#         'invoices_json': invoices_json,
#     }

#     # Render the generate_invoice.html template with the context
#     return render(request, 'generate_invoice.html', context)

def generate_invoice(request):
    # Retrieve sent invoices
    sent_invoices = Invoice.objects.filter(status='sent').select_related('booking')

    # Serialize sent invoices and related addition charges
    sent_invoice_data = []
    for invoice in sent_invoices:
        # Serialize the invoice
        invoice_dict = {
            'invoice_id': invoice.invoice_id,
            'booking': {
                'booking_id': invoice.booking.booking_id,
                'confirmation_no': invoice.booking.confirmation_no,
                'passenger_name': invoice.booking.passenger_name,
                'phone_number': invoice.booking.phone_number,
                'email': invoice.booking.email,
                'trip_type': invoice.booking.trip_type,
                'reference_id': invoice.booking.reference_id,
                'departure': invoice.booking.departure,
                'departure_date': invoice.booking.departure_date.isoformat(),
                'arrival': invoice.booking.arrival,
                'arrival_date': invoice.booking.arrival_date.isoformat(),
                'num_passengers': invoice.booking.num_passengers,
                'price': str(invoice.booking.price),
                'status': invoice.booking.status,
                'change_date': invoice.booking.change_date.isoformat() if invoice.booking.change_date else None,
                'lead_agent': invoice.booking.lead_agent.natural_key() if invoice.booking.lead_agent else None,
                'card_number': invoice.booking.card_number,
            },
            'base_price': str(invoice.base_price),
            'markup_price': str(invoice.markup_price),
            'description1': invoice.description1,
            'total1': str(invoice.total1),
            'tax': str(invoice.tax),
            'description2': invoice.description2,
            'total2': str(invoice.total2),
            'discount': str(invoice.discount),
            'total_discount': str(invoice.total_discount),
            'grand_total': str(invoice.grand_total),
        }
        
        # Retrieve and serialize addition charges for the invoice
        addition_charges = AdditionCharge.objects.filter(invoice=invoice)
        addition_charges_data = []
        for charge in addition_charges:
            charge_data = {
                'price': str(charge.price),
                'description': charge.description,
            }
            addition_charges_data.append(charge_data)
        
        # Include addition charges data in the invoice dictionary
        invoice_dict['addition_charges'] = addition_charges_data
        
        # Add the serialized invoice dictionary to the list
        sent_invoice_data.append(invoice_dict)
    
    # Convert the list of dictionaries to JSON
    sent_invoices_json = json.dumps(sent_invoice_data)

    # Pass the JSON data to the template context
    context = {
        'invoices_json': sent_invoices_json,
        'invoices' : sent_invoices
    }

    # Render the generate_invoice.html template with the context
    return render(request, 'generate_invoice.html', context)


def pending_invoices(request):
    # Retrieve pending invoices
    pending_invoices = Invoice.objects.filter(status='pending').select_related('booking')

    # Serialize pending invoices and related addition charges
    pending_invoice_data = []
    for invoice in pending_invoices:
        # Serialize the invoice
        invoice_dict = {
            'invoice_id': invoice.invoice_id,
            'booking': {
                'booking_id': invoice.booking.booking_id,
                'confirmation_no': invoice.booking.confirmation_no,
                'passenger_name': invoice.booking.passenger_name,
                'phone_number': invoice.booking.phone_number,
                'email': invoice.booking.email,

                'trip_type': invoice.booking.trip_type,
                'reference_id': invoice.booking.reference_id,
                'departure': invoice.booking.departure,
                'departure_date': invoice.booking.departure_date.isoformat(),
                'arrival': invoice.booking.arrival,
                'arrival_date': invoice.booking.arrival_date.isoformat(),
                'num_passengers': invoice.booking.num_passengers,
                'price': str(invoice.booking.price),
                'status': invoice.booking.status,
                'change_date': invoice.booking.change_date.isoformat() if invoice.booking.change_date else None,
                'lead_agent': invoice.booking.lead_agent.natural_key() if invoice.booking.lead_agent else None,
                'card_number': invoice.booking.card_number,
            },
            'base_price': str(invoice.base_price),
            'markup_price': str(invoice.markup_price),
            'description1': invoice.description1,
            'total1': str(invoice.total1),
            'tax': str(invoice.tax),
            'description2': invoice.description2,
            'total2': str(invoice.total2),
            'discount': str(invoice.discount),
            'total_discount': str(invoice.total_discount),
            'grand_total': str(invoice.grand_total),
        }
        
        # Retrieve and serialize addition charges for the invoice
        addition_charges = AdditionCharge.objects.filter(invoice=invoice)
        addition_charges_data = []
        for charge in addition_charges:
            charge_data = {
                'price': str(charge.price),
                'description': charge.description,
            }
            addition_charges_data.append(charge_data)
        
        # Include addition charges data in the invoice dictionary
        invoice_dict['addition_charges'] = addition_charges_data
        
        # Add the serialized invoice dictionary to the list
        pending_invoice_data.append(invoice_dict)
    
    # Convert the list of dictionaries to JSON
    pending_invoices_json = json.dumps(pending_invoice_data)

    # Pass the JSON data to the template context
    context = {
        'invoices_json': pending_invoices_json,
        'invoices' : pending_invoices
    }

    # Render the template with the context
    return render(request, 'invoice_pending.html', context)

def send_email(request):
    if request.method == 'POST':
        id = request.POST.get("invoice_id")
        print(id)
        invoices = get_object_or_404(Invoice, invoice_id=id)

        # Calculate total price including base price and markup price
        total_price = invoices.base_price + invoices.markup_price

        # Loop through addition charges and calculate total
        addition_charges_total = 0.00
        addition_charges = invoices.addition_charges()
        for addition_charge in addition_charges:
            addition_charges_total += float(str(addition_charge.price))

        # Calculate grand total
        grand_total = (total_price + addition_charges_total + invoices.tax) - invoices.discount

        # Prepare context for rendering email template
        context = {
            'invoices': invoices,
            'total_price': total_price,
            'missceleneous': addition_charges_total,
            'grand_total': grand_total
        }

        # Render the invoice HTML content
        invoice_html = render_to_string('invoice_template.html', context)

        # Create a text/plain version of the HTML email content
        text_content = strip_tags(invoice_html)

        # Create the email object
        email = EmailMultiAlternatives(
            subject='Your Invoice',
            body=text_content,
            from_email='www.swrang.123@gmail.com',
            to=['danswrang@adventurecode.io'],  # Replace with the recipient's email address
            # to=[invoices.booking.email],  # Replace with the recipient's email address
        )

        # Attach the HTML content
        email.attach_alternative(invoice_html, "text/html")

        # Send the email
        email.send()

        # Update status to 'sent' after email is sent
        invoices.status = 'sent'
        invoices.save()

        # Redirect to the page indicating that the email has been sent
        return redirect('crmApp:generate_invoice')
    else:
        return HttpResponse("Error: Invalid request method.")
    

def check_flight(request):
    if request.method == 'POST':
        json_data_str = request.POST.get('json_data')
        flight = json.loads(json_data_str)
        # Process the JSON data as needed
        # print(flight)
        try:
            response = amadeus.shopping.flight_offers.pricing.post(flight).data
            term="check flight availability"
            requestCounter(request.user.center,term)
            validating_airline_codes_set = set()
            
            for data in response["flightOffers"]:
                for dats in data["itineraries"]:
                    for segment in dats["segments"]:
                        # print(segment["carrierCode"])
                        validating_airline_codes_set.add(segment["carrierCode"])

            # Convert the set to a list if needed
            validating_airline_codes_list = list(validating_airline_codes_set)
            airline_codes_string = ','.join(validating_airline_codes_list)
            airlines = amadeus.reference_data.airlines.get(airlineCodes=airline_codes_string).data
            # print(airlines)
            result_dict = {item['iataCode']: item["businessName"] for item in airlines}
            result_dict2 = {item['iataCode']: item.get('icaoCode', item['iataCode']) for item in airlines}
            print(result_dict2)
            context = {
                'flight' : response,
                'flight1' : json.dumps(response),
                "airlines":result_dict,
                "airlines2":result_dict2,
            }
            file_path = "temp_ite.txt"
            with open(file_path, "w") as file:
                json.dump(context, file, indent= 4)
            # with open(file_path, "r") as file:
            #     context = json.load(file)
            # return HttpResponse({"success":"success"})
            return render(request,'itinery.html',context)
        except ResponseError as e:
             # error = ClientError(e)
            print(e.response.result["errors"][0]["detail"])
            print(f"catch Error: {type(e)}")
            # error_message = {"error": str(e.response.result["errors"])}
            return HttpResponse(e.response.result["errors"])

    
# ============================================================================( Chargeback View)==============================
    
def submit_chargeback(request):
    if request.method == 'POST':
        booking_confirmation_no = request.POST.get('booking_confirmation_no')
        print(booking_confirmation_no)
        reason = request.POST.get('reason')
        print(reason)
        chargeback_received_date = request.POST.get('chargeback_received_date')
        print(chargeback_received_date)
        
        booking = get_object_or_404(Booking, booking_id=booking_confirmation_no)
        print(booking)
        
        chargeback = Chargeback.objects.create(
            Booking=booking,
            reason=reason,
            chargeback_received_date=chargeback_received_date,
            # Add other fields as needed
        )
        
        messages.success(request, 'Chargeback Submitted Successfully!')
        
    return redirect('crmApp:chargeback')

# =================================================================================( update lead_chargeback_status)=========================

def update_chargeback_lead_status(request):
    if request.method == 'POST':
        chargeback_id = request.POST.get('chargeback_id')
        new_lead_status = request.POST.get('chargeback_lead_status')
        
        try:
            chargeback = Chargeback.objects.get(pk=chargeback_id)
            chargeback.chargeback_lead_status = new_lead_status
            chargeback.save()
        except Chargeback.DoesNotExist:
            pass  # Handle the case where the chargeback does not exist
        
    return redirect('crmApp:chargeback')

def update_chargeback_status(request):
    if request.method == 'POST':
        chargeback_id = request.POST.get('chargeback_id')
        new_status = request.POST.get('chargeback_status')
        print(new_status)
        try:
            chargeback = Chargeback.objects.get(pk=chargeback_id)
            chargeback.chargeback_status = new_status
            chargeback.save()
            return redirect('crmApp:chargeback')
        except Chargeback.DoesNotExist:
            return HttpResponseBadRequest("Chargeback does not exist")
    
    return HttpResponseBadRequest("Invalid request")


# ==========================================================================(chargeback_details)==============================

# def chargeback_details(request, chargeback_id):
#     try:
#         chargeback = Chargeback.objects.get(pk=chargeback_id)
#         return redirect('crmApp:dashboard', {'chargeback': chargeback})
#     except Chargeback.DoesNotExist:
#         return render(request, 'chargeback_not_found.html')

# =========================================================================(invoice creation)===================================

def invoiceCreate(request):
     # Retrieve all bookings with status 'confirmed'
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    return render(request,'invoicelists.html', {'bookings': confirmed_bookings})
# =========================================================================(invoice creation)===================================

def submit_invoice(request):
    if request.method == 'POST':
        booking = request.POST.get('bookingId')
        print("Booking Id:", booking)

        base_price = request.POST.get('basePrice')
        print("Base Price:", base_price)

        markup_price = request.POST.get('markupPrice')
        print("Markup Price:", markup_price)

        description1 = request.POST.get('description1')
        print("Description 1:", description1)

        total1 = request.POST.get('total1')
        print("Total 1:", total1)

        tax = request.POST.get('tax')
        print("Tax:", tax)

        description2 = request.POST.get('description2')
        print("Description 2:", description2)

        total2 = request.POST.get('total2')
        print("Total 2:", total2)

        additional_charges = request.POST.getlist('additionalCharges[]')
        print("Additional Charges:", additional_charges)

        additional_description = request.POST.getlist('additionalDescription[]')
        print("Additional Description:", additional_description)

        discount = request.POST.get('discount')
        print("Discount:", discount)

        total_discount = request.POST.get('totalDiscount')
        print("Total Discount:", total_discount)

        grand_total = request.POST.get('grandTotal')
        print("Grand Total:", grand_total)

        booking_instance = get_object_or_404(Booking, pk = booking)
        # Create an Invoice object
        invoice = Invoice.objects.create(
            invoice_id = random_invoice_no(),
            booking = booking_instance,
            base_price=base_price,
            markup_price=markup_price,
            description1=description1,
            total1=total1,
            tax=tax,
            description2=description2,
            total2=total2,
            discount=discount,
            total_discount=total_discount,
            grand_total=grand_total
        )

        # Create an AdditionalCharge object
        for p,des in zip(additional_charges,additional_description):
            charges = AdditionCharge.objects.create(
                invoice = invoice,
                price = p,
                description = des
            )
            charges.save()
        # # Optionally, you can save the AdditionalCharge object
        invoice.save()
        
        # Optionally, you can add a success message
        messages.success(request, 'Invoice submitted successfully!')
        
        # Redirect to a success page or a desired URL
        return redirect('crmApp:invoice')  # Adjust the URL name as per your project
    
def random_invoice_no():
    # Generate a random UUID
    random_uuid = uuid.uuid4()

    # Convert UUID to a string with uppercase letters only
    uuid_string = str(random_uuid).upper()

    # Remove dashes and take the first 6 characters
    invoice_number = ''.join(random.choices(uuid_string, k=6))
    
    return invoice_number

# Example usage
invoice_number = random_invoice_no()
print("Random Invoice Number:", invoice_number)




def invoice_details_fetch(request):
    if  request.method == "POST":
        id = request.POST.get("invoiceid")
        invoice_details = get_object_or_404(Invoice, invoice_id = id)
        context = {
            "data" : json.dumps(invoice_details)
        }
        return render("new.html",context)
    
def submit_cutomer(request):
    if request.method == 'POST':
        # Get the list of first names
        first_names = request.POST.getlist('firstName[]')
        middle_names = request.POST.getlist('middleName[]')
        last_names = request.POST.getlist('lastName[]')
        Sex = request.POST.getlist('Sex[]')
        DOB = request.POST.getlist('DOB[]')
        email = request.POST.get('email')
        countryCode = request.POST.get('countryCode')
        phone = request.POST.get('phone')
        json_data_str = request.POST.get('json_data')
        flight = json.loads(json_data_str)
        # Process the JSON data as needed
        # print(flight)
        # Process the data as needed
        print(first_names)
        traveler_details = []
        for index,(fname,lname,dob,sex) in enumerate(zip(first_names,last_names,DOB,Sex)):
            formatted_person = {
                "id": str(index+1),  # You can adjust the ID logic as needed
                "dateOfBirth": dob,  # You might want to provide the actual date of birth
                "name": {"firstName": fname.upper(), "lastName": lname.upper()},
                "gender": sex.upper(),  # Assuming 'MALE' or 'FEMALE' format
                "contact": {
                    "emailAddress": email,  # Add the actual email address
                    "phones": [
                        {
                            "deviceType": "MOBILE",
                            "countryCallingCode": countryCode,  # Add the actual country calling code
                            "number": phone  # Add the actual phone number
                        }
                    ],
                }
            }
            traveler_details.append(formatted_person)
        print(traveler_details)
        fullname = f'{traveler_details[0]["name"]["firstName"]} {traveler_details[0]["name"]["firstName"]}'

        try:
            response = amadeus.booking.flight_orders.post(flight, traveler_details).data
            term = "create order"
            requestCounter(request.user.center,term)
            context = {
                "data":response
            }
            file_path = 'order.txt'
            with open(file_path, "w") as file:
                    json.dump(context, file, indent= 4)
            # with open(file_path, "r") as file:
            #         context = json.load(file)
            response = context["data"]
            booking_id = response.get("id")
            passenger_name = fullname
            phone_number = phone
            email = email
            flight_details = None  # Not provided in the response
            trip_type = None  # Not provided in the response
            # print(response["flightOffers"][0]["itineraries"])
            if len(response["flightOffers"]) == 1:
                trip_type = "One way"
            elif len(response["flightOffers"]) > 2:
                trip_type = "multi-city"
            else:
                trip_type = "Round Trip"
            reference_id = response.get("id")
            departure = response["flightOffers"][0]["itineraries"][0]["segments"][0]['departure']["iataCode"]
            departure_date = date_format(response["flightOffers"][0]["itineraries"][0]["segments"][0]['departure']["at"])
            arrival = response["flightOffers"][0]["itineraries"][0]["segments"][-1]['arrival']["iataCode"]
            arrival_date = date_format(response["flightOffers"][0]["itineraries"][0]["segments"][-1]['arrival']["at"])
            num_passengers = len(traveler_details)
            price = response["flightOffers"][0]["price"]["grandTotal"]
            center_instance = get_object_or_404(Center, pk = request.user.center.pk)
            user_instance = get_object_or_404(CustomUser, pk = request.user.pk)
            booking_instance = Booking.objects.create(
                booking_id=booking_id,
                passenger_name=passenger_name,
                phone_number=phone_number,
                email=email,
                trip_type=trip_type,
                reference_id=reference_id,
                departure=departure,
                departure_date=departure_date,
                arrival=arrival,
                arrival_date=arrival_date,
                num_passengers=num_passengers,
                price=price,
                center = center_instance,
                lead_agent = user_instance
            )
            # Add more fields from the response as needed
            return redirect('crmApp:booking')
        except ResponseError as e:
            print(e.response.result["errors"][0]["detail"])
            print(f"catch Error: {type(e)}")
            return HttpResponse(e.response.result["errors"][0]["detail"])
        

    return HttpResponse("success")


def date_format(datetime_str):
    datetime_obj = datetime.fromisoformat(datetime_str)
    
    # Extract the date part
    date_only = datetime_obj.date()
    
    # Convert date to string in YYYY-MM-DD format
    date_str = date_only.isoformat()
    
    return date_str

    # if request.method == "POST":
    #     # Get the data from the POST request
    #     center_id = request.POST.get("centerId")
        
    #     # Get the center object
    #     center = Center.objects.get(pk=center_id)
        
    #     # Render the agreement email HTML content
    #     context = {'center': center}
    #     agreement_html = render_to_string('agreement_email.html', context)
        
    #     # Create a text/plain version of the HTML email content
    #     text_content = strip_tags(agreement_html)
        
    #     # Create the email object
    #     email = EmailMultiAlternatives(
    #         subject='Agreement for Center Authorization',
    #         body=text_content,
    #         from_email='www.swrang.123@gmail.com',
    #         to=[center.email],  # Assuming center has an email field
    #     )
        
    #     # Attach the HTML content
    #     email.attach_alternative(agreement_html, "text/html")
        
    #     # Send the email
    #     email.send()
        
    #     return HttpResponseRedirect(reverse('crmApp:centers_list'))



def send_signature_request(request):
    if request.method=="POST":
            bookingId = request.POST.get("bookingId")
            booking = get_object_or_404(Booking, booking_id=bookingId)
            email = booking.email
            booking_info = f"Booking ID: {bookingId}, Email: {email}"
            print(booking_info)
            # with ApiClient(configuration) as api_client:
            #     signature_request_api = apis.SignatureRequestApi(api_client)

            #     signer_1 = models.SubSignatureRequestTemplateSigner(
            #         role="Payment Authorization",
            #         email_address=email,
            #         name="Danswrang Boro",
            #     )

            #     # cc_1 = models.SubCC(
            #     #     role="Accounting",
            #     #     email_address="danswrang@adventurecode.io",
            #     # )

            #     custom_field_1 = models.SubCustomField(
            #         name="cost",
            #         value="$20,000",
            #         editor="Payment Authorization",
            #         required=True,
            #     )

            #     signing_options = models.SubSigningOptions(
            #         draw=True,
            #         type=True,
            #         upload=True,
            #         phone=False,
            #         default_type="draw",
            #     )

            #     data = models.SignatureRequestSendWithTemplateRequest(
            #         template_ids=["25f361d637eda607cdbe16150d4ffa4727d27b12"],
            #         subject="Purchase Order",
            #         message="Glad we could come to an agreement.",
            #         signers=[signer_1],
            #         # ccs=[cc_1],
            #         custom_fields=[custom_field_1],
            #         signing_options=signing_options,
            #         test_mode=True,
            #     )

            #     try:
            #         response = signature_request_api.signature_request_send_with_template(data)
            #         pprint(response)
            #         return HttpResponse("sent successful")
            #     except ApiException as e:
            #         print(e)
            #         return HttpResponse("something went wrong")
                #     # Render the agreement email HTML content
            context = {'booking': booking}
            agreement_html = render_to_string('acknowledge_customer.html', context)
            
            # Create a text/plain version of the HTML email content
            text_content = strip_tags(agreement_html)
            
            # Create the email object
            email = EmailMultiAlternatives(
                subject='Agreement for paymwent authorization',
                body=text_content,
                from_email='www.swrang.123@gmail.com',
                to=[email],
            )
            
            # Attach the HTML content
            email.attach_alternative(agreement_html, "text/html")
            
            # Send the email
            email.send()

            return redirect('crmApp:invoice')

def flight_search_multi(request):
    if request.method == 'GET':
        # Retrieve data from the GET request
        departure_cities = request.GET.getlist('departureCity[]')
        arrival_cities = request.GET.getlist('arrivalCity[]')
        departure_dates = request.GET.getlist('departureDate[]')
        adult = request.GET.get('adult')
        childrens = request.GET.get('child')
        infant = request.GET.get('infant')
        travel_class = request.GET.get('flightClass')

        print("Departure Cities:", departure_cities)
        print("Arrival Cities:", arrival_cities)
        print("Departure Dates:", departure_dates)
        print("Passenger Count:", adult)
        print("Travel Class:", travel_class)

        
        resultLists = []
        id = 1
        for index, (departure_city, arrival_city, departure_date) in enumerate(zip(departure_cities, arrival_cities, departure_dates)):
            data = []
            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=departure_city,
                    destinationLocationCode=arrival_city,
                    departureDate=departure_date,
                    adults=adult,
                    children=childrens,
                    infants=infant,
                    travelClass=travel_class
                    ).data
                requestCounter(request.user.center)
                print(response)
                for fdata in response:
                    fdata["id"] = f'{id}'
                    id = id + 1
                # response = {"flight":"flight"}
                # data.append(response)
                resultLists.append(response)    
            except ResponseError as e:
                print(e["error"])
        file_path = 'multiResult.txt'
        with open(file_path,'w') as file:
            json.dump(resultLists,file, indent=2)

        validating_airline_codes_set = set()
        for flightDatas in resultLists:
            for offers in flightDatas:
                for dats in offers["itineraries"]:
                    for segment in dats["segments"]:
                        validating_airline_codes_set.add(segment["carrierCode"])
        validating_airline_codes_list = list(validating_airline_codes_set)
        airline_codes_string = ','.join(validating_airline_codes_list)
        airlines = amadeus.reference_data.airlines.get(airlineCodes=airline_codes_string).data
        result_dict = {item['iataCode']: item['businessName'] for item in airlines}
        result_dict2 = {item['iataCode']: item.get('icaoCode', item['iataCode']) for item in airlines}
        context = {
            "flightOffers": resultLists,
            "flightOffers1": json.dumps(resultLists),
            "airlines2": result_dict2,
            "airlines3": json.dumps(result_dict2),
            "airlines":result_dict,
        }
        return render(request,"multi_result.html",context)

    else:
        # If the request method is not GET, return an error response or redirect to an error page
        return HttpResponse('Error: Only GET requests are allowed for this view.')
      
def payment(request):
    payments = Payment.objects.all()
    formatted_payments = []
    for payment in payments:
        card_number = str(payment.card_number)
        formatted_card_number = '**** **** **** ' + card_number[-4:]
        payment.card_number = formatted_card_number
        formatted_payments.append(payment)
    context = {
                'payments': formatted_payments,
                }
    return render(request, 'payment.html', context)

def relatedBooking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        print("printing this",booking_id)
        response = amadeus.booking.flight_order(booking_id).get()
        print(response.data)
        booking = Booking.objects.get(booking_id=booking_id)
        context = {
                    'booking': booking,
                    'itineries' : response.data
                   }
        return render(request,'pay_rleated_booking.html', context)
    

def initiatePayment(request):
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    for  booking in confirmed_bookings:
            print(booking)
    context={
        "book": confirmed_bookings
    }
    return render(request,'initiatePayment.html', context)


def gateway(request):
    return render(request, 'gateway.html')







# =========================================================================( Centers Start )================================================



def centersList(request):
    main_center = Center.objects.filter(name="Main").first()
    other_centers = Center.objects.exclude(name="Main").order_by('name')
    centers = [main_center] + list(other_centers)
    return render(request, 'centers_list.html', {'centers': centers})


def invoice_form(request):
    if request.method == 'POST':
        bookingid = request.POST.get('bookingId')
        print(bookingid)
        try:
            response = amadeus.booking.flight_order(bookingid).get().data
            booking = get_object_or_404(Booking, booking_id = bookingid)
            validating_airline_codes_set = set()
            
            for data in response["flightOffers"]:
                for dats in data["itineraries"]:
                    for segment in dats["segments"]:
                        # print(segment["carrierCode"])
                        validating_airline_codes_set.add(segment["carrierCode"])

            # Convert the set to a list if needed
            validating_airline_codes_list = list(validating_airline_codes_set)
            airline_codes_string = ','.join(validating_airline_codes_list)
            airlines = amadeus.reference_data.airlines.get(airlineCodes=airline_codes_string).data
            # print(airlines)
            result_dict = {item['iataCode']: item["businessName"] for item in airlines}
            result_dict2 = {item['iataCode']: item.get('icaoCode', item['iataCode']) for item in airlines}
            print(result_dict2)
            total_price = 0
            for flight in response["flightOffers"]:
                # print(flight["price"]["grandTotal"])
                total_price = total_price + float(flight["price"]["grandTotal"])
            context ={
                'flight' : response,
                'booking' : booking,
                "airlines":result_dict,
                "airlines2":result_dict2,
                "airline_price":total_price
            }
        except ReferenceError as e :
            print(e["error"])
        return render(request, 'invoiceForm.html', context)
    else:
        return redirect('crmApp:invocie')

def add_center(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        contact_person = request.POST['contact_person']
        
        # Handle file upload
        document = None
        if 'document' in request.FILES:
            uploaded_document = request.FILES['document']
            fs = FileSystemStorage()
            document = fs.save(uploaded_document.name, uploaded_document)
        
        # Create Center object
        center = Center.objects.create(
            name=name,
            email=email,
            address=address,
            phone=phone,
            contact_person=contact_person,
            document=document
        )
        
        return redirect('crmApp:centers_list')
    

def view_pdf(request, id):
    # Retrieve the Center instance or return a 404 error if not found
    center = get_object_or_404(Center, pk=id)
    
    # Get the path to the PDF file
    pdf_path = center.document.path
    
    # Print the PDF path for debugging
    print("PDF Path:", pdf_path)

    # Check if the PDF file exists
    if os.path.exists(pdf_path):
        # Open the PDF file in binary mode and return it as a FileResponse
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    else:
        # Return a 404 error if the PDF file does not exist
        return HttpResponse("PDF file not found", status=404)

# =========================================================================( center agreement email )

from django.core.mail import send_mail
# from django.template.loader import render_to_string

def authorize_center(request):
    if request.method == "POST":
        # Get the data from the POST request
        center_id = request.POST.get("centerId")
        
        # Get the center object
        center = Center.objects.get(pk=center_id)
        
        # Render the agreement email HTML content
        context = {'center': center}
        agreement_html = render_to_string('agreement_email.html', context)
        
        # Create a text/plain version of the HTML email content
        text_content = strip_tags(agreement_html)
        
        # Create the email object
        email = EmailMultiAlternatives(
            subject='Agreement for Center Authorization',
            body=text_content,
            from_email='www.swrang.123@gmail.com',
            to=[center.email],  # Assuming center has an email field
        )
        
        # Attach the HTML content
        email.attach_alternative(agreement_html, "text/html")
        
        # Send the email
        email.send()
        
        return HttpResponseRedirect(reverse('crmApp:centers_list'))
    
    

# def ack_agree(request, center_id):
#     # Get the client's IP address from the request object
#     # client_ip_address = request.META.get('REMOTE_ADDR')
#     client_ip_address = '103.219.61.205'
#     api_url = f"http://ipinfo.io/{client_ip_address}/json"
#     ipDetails = requests.get(api_url).json()
#     print(ipDetails)
    
#     print("Client IP Address:", client_ip_address)
    
#     # Retrieve the Center object based on the center_id
#     center = get_object_or_404(Center, pk=center_id)
    
#     context = {
#         'center': center,
#         'client_ip_address': client_ip_address
#     }
    
#     return render(request, 'ack_agree.html', context)
import re

def detect_os(user_agent):
    if 'Windows' in user_agent:
        return 'Windows'
    elif 'Macintosh' in user_agent:
        return 'Macintosh'
    # elif 'Linux' in user_agent:
    #     return 'Linux'
    elif re.search(r'Android', user_agent):
        return 'Android'
    elif re.search(r'iPad|iPhone', user_agent):
        return 'iOS'
    else:
        return 'Linux'

def detect_browser(user_agent):
    if 'Chrome' in user_agent:
        return 'Chrome'
    elif 'Firefox' in user_agent:
        return 'Firefox'
    elif 'Safari' in user_agent:
        return 'Safari'
    else:
        return 'Unknown'

def detect_device(user_agent):
    if re.search(r'Mobile|Android|iPhone|iPad', user_agent):
        return 'Mobile'
    elif re.search(r'Tablet|iPad', user_agent):
        return 'Tablet'
    else:
        return 'Desktop'


def ack_agree(request, center_id):
    # Get the client's IP address from the request object
    client_ip_address = '103.219.61.205'  # Example IP address for testing
    api_url = f"http://ipinfo.io/{client_ip_address}/json"
    ipDetails = requests.get(api_url).json()
    print(ipDetails)
    
    print("Client IP Address:", client_ip_address)
    
    # Get the user-agent string from the request headers
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Extracting operating system, browser, and device information from the user-agent string
    os_info = detect_os(user_agent)
    browser_info = detect_browser(user_agent)
    device_info = detect_device(user_agent)
    # user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

    # Retrieve the Center object based on the center_id
    center = get_object_or_404(Center, pk=center_id)
    center.status = 'active'
    center.acknowledgment_status = 'acknowledged'
    center.signed_at = datetime.now()
    center.save()
    
    context = {
        # 'SERVER_USER_AGENT': user_agent,
        'center': center,
        'client_ip_address': client_ip_address,
        'os_info': os_info,
        'browser_info': browser_info,
        'device_info': device_info,
        'ip': ipDetails
    }
    
    return render(request, 'ack_agree.html', context)


def customer_authorization(request, pk):
    # Get the client's IP address from the request object
    client_ip_address = '103.219.61.205'  # Example IP address for testing
    api_url = f"http://ipinfo.io/{client_ip_address}/json"
    ipDetails = requests.get(api_url).json()
    print(ipDetails)
    print("its comming here", pk)
    print("Client IP Address:", client_ip_address)
    
    # Get the user-agent string from the request headers
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Extracting operating system, browser, and device information from the user-agent string
    os_info = detect_os(user_agent)
    browser_info = detect_browser(user_agent)
    device_info = detect_device(user_agent)
    # user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

    # Retrieve the Center object based on the center_id
    booking = get_object_or_404(Booking, pk = pk)
    booking.auth = 'authorized'
    # center.acknowledgment_status = 'acknowledged'
    # center.signed_at = datetime.now()
    booking.save()
    
    context = {
        # 'SERVER_USER_AGENT': user_agent,
        'booking': booking,
        'client_ip_address': client_ip_address,
        'os_info': os_info,
        'browser_info': browser_info,
        'device_info': device_info,
        'ip': ipDetails
    }
    
    return render(request, 'customer_agreement.html', context)

def track(request):
    # Log the email open event
    print("Email is opened")
    # You can save this event to your database or perform any other necessary actions

    # Return a JSON response indicating the event was logged successfully
    return JsonResponse({"message": "Email open event logged"})

# totalchargeback table pages

def total_chargeback(request):
    return render(request,'total_chargeback.html')

def total_leads(request):
    return render(request,'total_leads.html')

def total_refund(request):
    return render(request,'total_refund.html')

def income(request):
    return render(request,'income.html')

def new_booking(request):
    pending_bookings = Booking.objects.filter(status='pending')
    return render(request, 'new_booking.html', {'pending_bookings': pending_bookings})

def center_related(request):
    if request.method == 'GET':
        print("inside post")
        center_name = request.GET.get('center')
        center_instance = get_object_or_404(Center, name=center_name)

        try:
            # Filter bookings by center
            bookings = Booking.objects.filter(center=center_instance)
            refunds = Refund.objects.filter(booking_id__center__name=center_name)
            api_requests = APIRequest.objects.filter(center=center_instance)
            total_api_requests = api_requests.count()
            refund_count = refunds.count()
            booking_count = bookings.count()
            pending_count = bookings.filter(status='pending').count()
            confirmed_count = bookings.filter(status='confirmed').count()
            cancelled_count = bookings.filter(status='cancelled').count()

           # Check if the center is the main center
            main_center = Center.objects.filter(name = 'Main').exists()

            if main_center:
                validity = None
                remaining_time = None
            else:
                # Retrieve validity for the center
                validity = center_instance.subscription_validity

                # Calculate remaining time
                current_date = timezone.now().date()
                remaining_days = (validity.end_date - current_date).days
                remaining_time = str(timedelta(days=remaining_days)) if remaining_days > 0 else "Subscription Expired"
                
                # Update expiry value if subscription has expired
                if remaining_days <= 0:
                    validity.expiry_value = "expired"
                    validity.save()
        except Booking.DoesNotExist:
            # No booking found
            bookings = None
            refund_count = 0
            booking_count = 0
            pending_count = 0
            confirmed_count = 0
            cancelled_count = 0
            validity = None
            remaining_time = None
            total_api_requests = 0

        print("Center name received: ", center_name)
        # Check if a center with the received name exists
        center = get_object_or_404(Center, name=center_name)

        # Pass all fields of the Center object as context to the template
        return render(request, 'center_track.html', {
            'center': center,
            'bookings': bookings,
            'refund_count': refund_count,
            'booking_count': booking_count,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
            'cancelled_count': cancelled_count,
            'validity': validity,
            'remaining_time': remaining_time,
            'total_api_requests': total_api_requests
        })
    return HttpResponse("something went wrong")
    

def centers_related_booking(request, center_name):
    # Assuming 'center_name' is unique, otherwise filter as per your requirement
    bookings = Booking.objects.filter(center__name=center_name)
    return render(request, 'center_related_booking.html', {'bookings': bookings})

def centers_related_pending(request, center_name):
    pending_bookings = Booking.objects.filter(center__name=center_name, status='pending')
    return render(request, 'center_related_pending.html', {'pending_bookings': pending_bookings})

def centers_related_confirmed(request, center_name):
    confirmed_bookings = Booking.objects.filter(center__name=center_name, status='confirmed')
    return render(request, 'center_related_confirmed.html', {'confirmed_bookings': confirmed_bookings})

def centers_related_cancel(request, center_name):
    # Retrieve canceled status bookings related to the specified center
    canceled_bookings = Booking.objects.filter(center__name=center_name, status='cancelled')
    return render(request, 'center_related_cancel.html', {'canceled_bookings': canceled_bookings})

def centers_related_refund(request, center_name):
    # Retrieve refund-related data related to the specified center
    refund_data = Refund.objects.filter(booking_id__center__name=center_name)
    return render(request, 'center_related_refund.html', {'refund_data': refund_data})

def centers_related_apiRequest(request, center_name):
    # Retrieve refund-related data related to the specified center
    api = APIRequest.objects.filter(center__name=center_name)
    return render(request, 'api_request.html', {'api': api})

def renew_plan(request):
    return render(request,'renew_plan.html')

def renew_plan_submit(request):
    if request.method == 'POST':
        # Assuming you have a form field named 'plan' in your HTML form
        plan = request.POST.get('plan')

        # Process the plan renewal logic here
        # For demonstration, let's just show a success message
        messages.success(request, f'Successfully renewed {plan} plan.')

        # Redirect to a success page or any other appropriate page
        return redirect('success_page')  

    return redirect('renew_plan')

def subscription_plans(request):
    return render(request, 'plans.html')

def basic_plan(request):
    centers = Center.objects.filter(status='active')
    print(centers)
    return render(request, 'basic_plan.html', {'centers': centers})

def standard_plan(request):
    return render(request, 'standard_plan.html')

def premium_plan(request):
    return render(request, 'premium_plan.html')

def assign_plan(request):
    if request.method == 'POST':
        center_name = request.POST.get('center')
        type = request.POST.get('type')
        duration = request.POST.get('plan_type')
        center = Center.objects.get(name=center_name)

        plan = Plans(center=center, type = type, duration = duration)
        
        plan.save()

        # return redirect('success_url_name')

    # If the request method is not POST, render the form template again
    # return redirect(request, 'plans.html', {'centers': Center.objects.all()})
    return redirect('crmApp:subscription_plans')



def requestCounter(center,term):
    try:
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        print("Request made by:", center)
        print("Date:", current_date)
        print("Time:", current_time)

        # Create an instance of the Center model
        center_instance = Center.objects.get(name=center)

        # Create an instance of the APIRequest model and save it to the database
        api_request = APIRequest.objects.create(center=center_instance, request_date=current_date, request_time=current_time,type=term)
        api_request.save()
    except Exception as e:
        print("excepton has occured", e)


#### veiw selected invoice ###########
def view_invoice(request, pk):
    print(pk)
    invoice = get_object_or_404(Invoice, pk = pk)
    context={
        "invoice":invoice
    }
    return render(request,'view_invoice.html', context)