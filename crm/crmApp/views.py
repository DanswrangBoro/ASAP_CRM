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

    context = {
        'total_sales': total_sales,
        'monthly_income': monthly_income,
        'annual_income': annual_income
    }
    
    return render(request, "base.html", context)

def total_booking(request):
    return render(request,"total_booking.html")

def total_user(request):
    return render(request,"total_users.html")

def booking(request):
    original = Booking.objects.all()
    context = {
        "original" : original
    }
    return render(request,"bookings.html", context)

def refund(request):
    return render(request,"refunds.html")

def chargeback(request):
    return render(request,"chargeback.html")

def rejected(request):
    return render(request,"rejected.html")

def mco(request):
    return render(request,"mco.html")

def cancellation(request):
    return render(request,"cancellation.html")

def ecredit(request):
    return render(request,"ecredit.html")

def update_booking_status(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        status = request.POST.get('status')
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            booking.status = status
            booking.save()
            # Redirect to the same page or any other appropriate page after updating the status
            return redirect('crmApp:booking')
        except Booking.DoesNotExist:
            # Handle case where the booking ID does not exist
            pass
    # Handle GET requests or any other scenario
    # You can redirect to another page or render a template
    return redirect('crmApp:booking')


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
