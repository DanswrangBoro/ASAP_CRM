from django.contrib import admin
from .models import Booking, Refund, RejectedBooking
from .models import Sale

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'passenger_name', 'departure_date', 'arrival_date', 'price','phone_number','email','mco']
    search_fields = ['booking_id', 'passenger_name']
    list_filter = ['departure_date', 'arrival_date']
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['booking_id','passenger_name']

# @admin.register(Person)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('user_name', 'email', 'phone_number', 'role', 'team','password')

@admin.register(RejectedBooking)
class RejectedBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'customer_name', 'reason', 'rejection_date')


from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'phoneNumber', 'role', 'team')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phoneNumber', 'role', 'team', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'phoneNumber', 'role', 'team', 'is_staff')
    search_fields = ('username', 'email', 'phoneNumber', 'role', 'team')
    ordering = ('username',)

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)


class SalesAdmin(admin.ModelAdmin):
    list_display = ('agent', 'sale_date', 'amount')
    search_fields = ('agent__username',)  # Enables searching by agent username

# Register your models here.
admin.site.register(Sale, SalesAdmin)


