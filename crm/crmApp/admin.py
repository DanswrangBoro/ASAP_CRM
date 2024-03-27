from django.contrib import admin
from .models import MCO, APIRequest, Payment, Center, Plans, Validity
from .models import  AdditionCharge, Booking, Refund, RejectedBooking, CustomUser

from .models import Sale
from .models import Invoice

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id','booking_id', 'passenger_name', 'departure_date', 'arrival_date', 'price','phone_number','email','change_date']
    search_fields = ['booking_id', 'passenger_name']
    list_filter = ['departure_date', 'arrival_date']

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['booking_id']

@admin.register(RejectedBooking)
class RejectedBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'reason', 'rejection_date')
    
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'phoneNumber', 'role', 'blocked', 'center')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phoneNumber', 'role', 'password1', 'password2', 'center'),
        }),
    )
    list_display = ('username', 'email', 'phoneNumber', 'role', 'is_staff')
    search_fields = ('username', 'email', 'phoneNumber', 'role')
    ordering = ('username',)
    def add_view(self, request, form_url='', extra_context=None):
        self.form = self.add_form  # Set the form to your custom form
        return super().add_view(request, form_url, extra_context)

# Register the CustomUser model with the CustomUserAdmin



class SalesAdmin(admin.ModelAdmin):
    list_display = ('agent', 'sale_date', 'amount')
    search_fields = ('agent__username',)  # Enables searching by agent username

# Register your models here.
admin.site.register(Sale, SalesAdmin)


from .models import Chargeback

@admin.register(Chargeback)
class ChargebackAdmin(admin.ModelAdmin):
    list_display = (  'chargeback_status','chargeback_lead_status')
    search_fields = ('booking_confirmation_no', 'customer_name')
    list_filter = ('chargeback_status', 'chargeback_received_date')
    date_hierarchy = 'chargeback_received_date'



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'base_price', 'markup_price', 'description1', 'total1', 'tax', 'description2', 'total2', 'discount', 'total_discount', 'grand_total','status']
    list_filter = ['base_price', 'markup_price', 'total1', 'tax', 'total2', 'discount', 'total_discount', 'grand_total']
    search_fields = ['description1', 'description2']


@admin.register(AdditionCharge)
class  AdditionalChargeAdmin(admin.ModelAdmin):
    list_display = ['price','description']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'transaction_id', 'transaction_status', 'amount', 'payment_date', 'cardholder_name', 'card_number', 'expiry_date', 'cvv', 'card_type')
    search_fields = ['booking_id__booking_id', 'transaction_id', 'cardholder_name', 'card_number']
    list_filter = ('transaction_status', 'payment_date')

admin.site.register(Payment, PaymentAdmin)

admin.site.register(MCO)

@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'phone', 'contact_person', 'document', 'status','acknowledgment_status','signed_at')

@admin.register(Validity)
class ValidityAdmin(admin.ModelAdmin):
    list_display = ['center', 'start_date', 'end_date','expiry_value']

# Register your models here.
admin.site.register(Plans)

@admin.register(APIRequest)
class APIRequestAdmin(admin.ModelAdmin):
    list_display = ('center', 'request_date', 'request_time','type')