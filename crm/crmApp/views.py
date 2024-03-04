from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Booking
from datetime import datetime
from django.db.models import Sum

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

def fetch_passenger_name(request):
    if request.method == 'GET':
        booking_id = request.GET.get('booking_id')
        print(booking_id)
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            passenger_name = booking.passenger_name
            return JsonResponse({'passenger_name': passenger_name})
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking ID not found'}, status=404)

# =============================================(retrieve customer name using booking id)==========================
