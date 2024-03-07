from django.contrib import admin
from .models import Booking, Refund
from .models import User

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'passenger_name', 'departure_date', 'arrival_date', 'price','phone_number','email']
    search_fields = ['booking_id', 'passenger_name']
    list_filter = ['departure_date', 'arrival_date']
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['booking_id','passenger_name']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'phone_number', 'role', 'team','password')